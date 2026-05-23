#!/usr/bin/env python3
"""
ask_graph.py

Ask questions about the knowledge graph in MarketingControlPlane.

Two graph sources are supported:
- semantic     (default)  -> graphify-out/graph.json   (concepts, communities, typed
                                                          relations with confidence)
- deterministic           -> graph/nodes.ndjson + graph/edges.ndjson (file-level graph)

Two retrieval strategies are supported:
- hybrid    (default) -> embedding similarity + lexical keyword score
- embedding           -> embedding similarity only
- lexical             -> keyword score only (no embedding calls)

Two answering modes are supported:
- local  -> retrieve the most relevant nodes, attach a snippet of each node's real
            source-file content, and answer from those.
- global -> answer from community summaries (clusters of related nodes across the
            whole graph). Good for "what are the main themes?" questions.
- auto   (default) -> pick global for big-picture questions, local otherwise.

Usage:
    python scripts/ask_graph.py --repo-root . "What grounds the bad news posts?"
    python scripts/ask_graph.py --repo-root . "What are the main themes overall?"
    python scripts/ask_graph.py --repo-root . --interactive
    python scripts/ask_graph.py --repo-root . --graph deterministic --retrieval lexical "..."

Requires:
    pip install openai
    export OPENAI_API_KEY=...

Notes:
- Embeddings are cached on disk (.ask_graph_embeddings.json) keyed by content hash,
  so only new/changed node text is re-embedded on later runs.
- This script does local retrieval over the graph, then sends a compact context to the model.
- It does not modify the repo graph.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

DEFAULT_MODEL = os.getenv("OPENAI_MODEL", "gpt-5.4")
DEFAULT_EMBED_MODEL = os.getenv("OPENAI_EMBED_MODEL", "text-embedding-3-small")
EMBED_CACHE_NAME = ".ask_graph_embeddings.json"
TEXT_EXTENSIONS = {".md", ".markdown", ".txt", ".rst", ".py", ".json", ".ndjson", ".yaml", ".yml"}
GLOBAL_HINTS = [
    "big picture", "overall", "across everything", "across the", "high level", "high-level",
    "overview", "main themes", "major themes", "key themes", "what are the themes",
    "what is this about", "what is the corpus", "communities", "clusters", "landscape", "map of",
    "recurring themes", "common themes", "what themes",
]

CREATIVITY_PROMPT = (
    "Be weird. Look for unexpected combinations of source material that haven't been tried. "
    "Favour lateral connections over obvious ones — if two nodes share a surprising metaphor or theme, say so. "
    "Be speculative and experimental rather than safe or conservative. "
    "Suggest ideas that might feel slightly wrong or uncomfortable before they feel right. "
    "Avoid recommending the most obvious next step. If you notice an unusual edge or an underused source file, follow it."
)


def get_openai_client():
    # Imported lazily so graph loading and lexical retrieval work without the openai package.
    from openai import OpenAI

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is not set.")
    return OpenAI(api_key=api_key)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("question", nargs="?", help="Question to ask about the graph")
    parser.add_argument("--repo-root", default=".", help="Path to repo root")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="OpenAI chat model name")
    parser.add_argument("--embed-model", default=DEFAULT_EMBED_MODEL, help="OpenAI embedding model name")
    parser.add_argument(
        "--graph",
        choices=["semantic", "deterministic"],
        default="semantic",
        help="Which graph to query (default: semantic / graphify-out/graph.json)",
    )
    parser.add_argument(
        "--retrieval",
        choices=["hybrid", "embedding", "lexical"],
        default="hybrid",
        help="Retrieval strategy for selecting seed nodes (default: hybrid)",
    )
    parser.add_argument(
        "--mode",
        choices=["auto", "local", "global"],
        default="auto",
        help="Answering mode: local (nodes+content), global (community summaries), or auto",
    )
    parser.add_argument("--max-nodes", type=int, default=12, help="Max nodes to include in context")
    parser.add_argument("--max-edges", type=int, default=20, help="Max edges to include in context")
    parser.add_argument("--max-communities", type=int, default=14, help="Max communities in global context")
    parser.add_argument("--content-chars", type=int, default=700, help="Max chars of file content per node")
    parser.add_argument("--no-content", action="store_true", help="Do not attach source-file snippets")
    parser.add_argument("--interactive", action="store_true", help="Run an interactive REPL")
    return parser.parse_args()


# --------------------------------------------------------------------------- #
# Graph loading                                                               #
# --------------------------------------------------------------------------- #


def read_ndjson(path: Path) -> List[Dict[str, Any]]:
    items: List[Dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                items.append(json.loads(line))
    return items


def load_deterministic_graph(repo_root: Path) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    nodes_path = repo_root / "graph" / "nodes.ndjson"
    edges_path = repo_root / "graph" / "edges.ndjson"
    if not nodes_path.exists() or not edges_path.exists():
        raise FileNotFoundError(
            f"Missing graph files:\n  {nodes_path}\n  {edges_path}\n"
            "Run build_markdown_graph.py first."
        )
    return read_ndjson(nodes_path), read_ndjson(edges_path)


def _normalize_semantic_node(n: Dict[str, Any]) -> Dict[str, Any]:
    source_file = n.get("source_file") or ""
    label = n.get("label") or n.get("id") or ""
    tags = [n.get("file_type"), n.get("author")]
    if n.get("community") is not None:
        tags.append(f"community:{n.get('community')}")
    return {
        "id": n.get("id"),
        "path": source_file,
        "file_name": source_file.split("/")[-1] if source_file else "",
        "node_type": n.get("file_type") or "unknown",
        "title": label,
        "status": "unknown",
        "tags": [t for t in tags if t],
        "themes": [],
        "metaphors": [],
        "topics": [],
        "channel": None,
        "summary": label,
        "community": n.get("community"),
        "source_location": n.get("source_location"),
    }


def _normalize_semantic_edge(l: Dict[str, Any]) -> Dict[str, Any]:
    src = l.get("source") or l.get("_src")
    tgt = l.get("target") or l.get("_tgt")
    relation = l.get("relation") or "related"
    weight = l.get("weight")
    if weight is None:
        weight = l.get("confidence_score", 1.0)
    return {
        "id": f"edge:{src}->{relation}->{tgt}",
        "from": src,
        "to": tgt,
        "type": relation,
        "weight": weight,
        "evidence": {
            "confidence": l.get("confidence"),
            "confidence_score": l.get("confidence_score"),
            "source_file": l.get("source_file"),
        },
    }


def load_semantic_graph(path: Path) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    nodes = [_normalize_semantic_node(n) for n in data.get("nodes", [])]
    edges = [_normalize_semantic_edge(l) for l in data.get("links", [])]
    node_ids = {n["id"] for n in nodes}
    edges = [e for e in edges if e["from"] in node_ids and e["to"] in node_ids]
    return nodes, edges


def load_graph(repo_root: Path, source: str) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    if source == "deterministic":
        return load_deterministic_graph(repo_root)
    semantic_path = repo_root / "graphify-out" / "graph.json"
    if semantic_path.exists():
        return load_semantic_graph(semantic_path)
    print(
        f"warning: semantic graph not found at {semantic_path}; falling back to deterministic graph.",
        file=sys.stderr,
    )
    return load_deterministic_graph(repo_root)


# --------------------------------------------------------------------------- #
# Text + lexical scoring                                                       #
# --------------------------------------------------------------------------- #


def tokenize(text: str) -> List[str]:
    text = text.lower()
    text = re.sub(r"[^a-z0-9_/\- ]+", " ", text)
    return [t for t in text.split() if len(t) > 1]


def node_text(node: Dict[str, Any]) -> str:
    parts = [
        node.get("path", ""),
        node.get("file_name", ""),
        node.get("node_type", ""),
        node.get("title", ""),
        node.get("summary", ""),
        " ".join(node.get("tags", []) or []),
        " ".join(node.get("themes", []) or []),
        " ".join(node.get("metaphors", []) or []),
        " ".join(node.get("topics", []) or []),
        str(node.get("channel") or ""),
    ]
    return " ".join(p for p in parts if p).strip()


def edge_text(edge: Dict[str, Any], node_by_id: Dict[str, Dict[str, Any]]) -> str:
    from_node = node_by_id.get(edge["from"], {})
    to_node = node_by_id.get(edge["to"], {})
    parts = [
        edge.get("type", ""),
        from_node.get("path", ""),
        from_node.get("title", ""),
        to_node.get("path", ""),
        to_node.get("title", ""),
        json.dumps(edge.get("evidence", {}), ensure_ascii=False),
    ]
    return " ".join(parts)


def score_text(query_tokens: List[str], text: str) -> float:
    tokens = tokenize(text)
    if not tokens or not query_tokens:
        return 0.0

    counts = Counter(tokens)
    score = 0.0
    for qt in query_tokens:
        if qt in counts:
            score += 1.0 + math.log1p(counts[qt])

    joined = " ".join(tokens)
    query_joined = " ".join(query_tokens)
    if query_joined and query_joined in joined:
        score += 3.0

    return score


# --------------------------------------------------------------------------- #
# Source-file content snippets (local mode)                                    #
# --------------------------------------------------------------------------- #


def _cap(text: str, max_chars: int) -> str:
    text = text.strip()
    if len(text) <= max_chars:
        return text
    return text[:max_chars].rstrip() + " …"


def _read_text_file(repo_root: Path, rel_path: str, cache: Dict[str, Optional[str]]) -> Optional[str]:
    if rel_path in cache:
        return cache[rel_path]
    text: Optional[str] = None
    if rel_path and Path(rel_path).suffix.lower() in TEXT_EXTENSIONS:
        full = repo_root / rel_path
        if full.exists() and full.is_file():
            try:
                text = full.read_text(encoding="utf-8", errors="replace")
            except Exception:
                text = None
    cache[rel_path] = text
    return text


def _line_window(text: str, location: Any, max_chars: int) -> Optional[str]:
    m = re.match(r"[Ll](\d+)", str(location or ""))
    if not m:
        return None
    line_no = int(m.group(1))
    lines = text.splitlines()
    if line_no < 1 or line_no > len(lines):
        return None
    lo = max(0, line_no - 8)
    hi = min(len(lines), line_no + 8)
    return _cap("\n".join(lines[lo:hi]), max_chars)


def _paragraph_window(text: str, query_tokens: List[str], max_chars: int) -> str:
    paras = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    if not paras:
        return _cap(text, max_chars)
    qset = set(query_tokens)
    best_i, best_score = 0, -1
    for i, p in enumerate(paras):
        s = sum(1 for t in set(tokenize(p)) if t in qset)
        if s > best_score:
            best_score, best_i = s, i
    if best_score <= 0:
        return _cap("\n\n".join(paras[:3]), max_chars)
    chosen = [paras[best_i]]
    if best_i + 1 < len(paras):
        chosen.append(paras[best_i + 1])
    return _cap("\n\n".join(chosen), max_chars)


def attach_content(
    nodes: List[Dict[str, Any]],
    repo_root: Path,
    question: str,
    max_chars: int,
) -> None:
    """Set node['content'] to a relevant snippet of each node's real source file."""
    cache: Dict[str, Optional[str]] = {}
    qtokens = tokenize(question)
    for node in nodes:
        rel_path = node.get("path")
        if not rel_path:
            continue
        text = _read_text_file(repo_root, rel_path, cache)
        if not text:
            continue
        snippet = _line_window(text, node.get("source_location"), max_chars)
        if not snippet:
            snippet = _paragraph_window(text, qtokens + tokenize(node.get("title") or ""), max_chars)
        if snippet:
            node["content"] = snippet


# --------------------------------------------------------------------------- #
# Communities (global mode)                                                    #
# --------------------------------------------------------------------------- #


def _load_community_names(repo_root: Path) -> Dict[int, str]:
    path = repo_root / "graphify-out" / "GRAPH_REPORT.md"
    names: Dict[int, str] = {}
    if not path.exists():
        return names
    try:
        for line in path.read_text(encoding="utf-8").splitlines():
            m = re.match(r'#+\s*Community\s+(\d+)\s*-\s*"(.+?)"', line.strip())
            if m:
                names[int(m.group(1))] = m.group(2)
    except Exception:
        return {}
    return names


def build_communities(
    nodes: List[Dict[str, Any]],
    edges: List[Dict[str, Any]],
    repo_root: Path,
) -> Dict[Any, Dict[str, Any]]:
    by_comm: Dict[Any, List[Dict[str, Any]]] = {}
    for n in nodes:
        c = n.get("community")
        if c is None:
            continue
        by_comm.setdefault(c, []).append(n)
    if not by_comm:
        return {}

    degree: Counter = Counter()
    for e in edges:
        degree[e["from"]] += 1
        degree[e["to"]] += 1

    names = _load_community_names(repo_root)
    comms: Dict[Any, Dict[str, Any]] = {}
    for c, members in by_comm.items():
        members_sorted = sorted(members, key=lambda n: (-degree[n["id"]], n.get("title") or ""))
        fallback = members_sorted[0].get("title") if members_sorted else f"community {c}"
        comms[c] = {
            "id": c,
            "size": len(members),
            "name": names.get(c) or fallback,
            "members": members_sorted,
        }
    return comms


def looks_global(question: str) -> bool:
    q = question.lower()
    return any(hint in q for hint in GLOBAL_HINTS)


def rank_communities(
    comms: Dict[Any, Dict[str, Any]],
    node_scores: Dict[str, float],
) -> List[Tuple[float, Dict[str, Any]]]:
    ranked = []
    for info in comms.values():
        member_scores = sorted(
            (node_scores.get(m["id"], 0.0) for m in info["members"]), reverse=True
        )[:5]
        ranked.append((sum(member_scores), info))
    ranked.sort(key=lambda x: (-x[0], -x[1]["size"]))
    return ranked


def render_global_context(
    ranked_comms: List[Tuple[float, Dict[str, Any]]],
    members_per: int = 7,
) -> str:
    lines = ["COMMUNITIES (clusters of related nodes across the whole graph):"]
    for _, info in ranked_comms:
        top_members = [m.get("title") for m in info["members"][:members_per]]
        lines.append(
            json.dumps(
                {
                    "community": info["id"],
                    "name": info["name"],
                    "size": info["size"],
                    "top_members": top_members,
                },
                ensure_ascii=False,
            )
        )
    return "\n".join(lines)


# --------------------------------------------------------------------------- #
# Embeddings (with on-disk cache)                                             #
# --------------------------------------------------------------------------- #


def _embed_key(model: str, text: str) -> str:
    return hashlib.sha256((model + "\x00" + text).encode("utf-8")).hexdigest()


def load_embed_cache(path: Path) -> Dict[str, List[float]]:
    if path.exists():
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {}


def save_embed_cache(path: Path, cache: Dict[str, List[float]]) -> None:
    try:
        path.write_text(json.dumps(cache), encoding="utf-8")
    except Exception as e:
        print(f"warning: could not save embedding cache: {e}", file=sys.stderr)


def embed_texts(
    client: Any,
    model: str,
    texts: List[str],
    cache: Dict[str, List[float]],
    batch_size: int = 256,
) -> List[List[float]]:
    """Return one embedding vector per input text, fetching only uncached texts."""
    out: List[Optional[List[float]]] = [None] * len(texts)
    missing_idx: List[int] = []
    missing_text: List[str] = []
    for i, t in enumerate(texts):
        safe = t if t.strip() else " "
        key = _embed_key(model, safe)
        if key in cache:
            out[i] = cache[key]
        else:
            missing_idx.append(i)
            missing_text.append(safe)

    for start in range(0, len(missing_text), batch_size):
        chunk = missing_text[start : start + batch_size]
        resp = client.embeddings.create(model=model, input=chunk)
        for j, item in enumerate(resp.data):
            vec = list(item.embedding)
            idx = missing_idx[start + j]
            out[idx] = vec
            cache[_embed_key(model, chunk[j])] = vec

    return [v if v is not None else [] for v in out]


def cosine(a: List[float], b: List[float]) -> float:
    if not a or not b:
        return 0.0
    dot = 0.0
    na = 0.0
    nb = 0.0
    for x, y in zip(a, b):
        dot += x * y
        na += x * x
        nb += y * y
    if na == 0.0 or nb == 0.0:
        return 0.0
    return dot / math.sqrt(na * nb)


# --------------------------------------------------------------------------- #
# Ranking + retrieval                                                          #
# --------------------------------------------------------------------------- #


def rank_nodes(
    question: str,
    nodes: List[Dict[str, Any]],
    mode: str = "lexical",
    node_embs: Optional[Dict[str, List[float]]] = None,
    query_emb: Optional[List[float]] = None,
) -> List[Tuple[float, Dict[str, Any]]]:
    qtokens = tokenize(question)
    lex = {n["id"]: score_text(qtokens, node_text(n)) for n in nodes}

    use_emb = mode in ("embedding", "hybrid") and bool(node_embs) and bool(query_emb)
    emb: Dict[str, float] = {}
    if use_emb:
        emb = {n["id"]: max(0.0, cosine(query_emb, node_embs.get(n["id"], []))) for n in nodes}

    def _norm(d: Dict[str, float]) -> Dict[str, float]:
        m = max(d.values()) if d else 0.0
        return {k: (v / m if m > 0 else 0.0) for k, v in d.items()}

    if mode == "lexical" or not use_emb:
        combined = {n["id"]: lex[n["id"]] for n in nodes}
    elif mode == "embedding":
        combined = emb
    else:  # hybrid
        ln, en = _norm(lex), _norm(emb)
        combined = {n["id"]: 0.65 * en[n["id"]] + 0.35 * ln[n["id"]] for n in nodes}

    ranked = [(combined[n["id"]], n) for n in nodes if combined[n["id"]] > 0]
    ranked.sort(key=lambda x: (-x[0], x[1].get("path") or ""))
    return ranked


def rank_edges(
    question: str,
    edges: List[Dict[str, Any]],
    node_by_id: Dict[str, Dict[str, Any]],
    selected_node_ids: set[str],
) -> List[Tuple[float, Dict[str, Any]]]:
    qtokens = tokenize(question)
    ranked = []
    for edge in edges:
        base = score_text(qtokens, edge_text(edge, node_by_id))
        if edge["from"] in selected_node_ids or edge["to"] in selected_node_ids:
            base += 1.5
        if base > 0:
            base += 0.5 * float(edge.get("weight") or 0.0)
            ranked.append((base, edge))
    ranked.sort(key=lambda x: (-x[0], x[1].get("type", "")))
    return ranked


def expand_with_neighbors(
    selected_nodes: List[Dict[str, Any]],
    ranked_edges: List[Tuple[float, Dict[str, Any]]],
    node_by_id: Dict[str, Dict[str, Any]],
    max_nodes: int,
) -> List[Dict[str, Any]]:
    chosen = {n["id"]: n for n in selected_nodes}
    for _, edge in ranked_edges:
        for nid in (edge["from"], edge["to"]):
            if len(chosen) >= max_nodes:
                break
            if nid not in chosen and nid in node_by_id:
                chosen[nid] = node_by_id[nid]
        if len(chosen) >= max_nodes:
            break
    return list(chosen.values())


def render_context(
    nodes: List[Dict[str, Any]],
    edges: List[Dict[str, Any]],
    node_by_id: Dict[str, Dict[str, Any]],
) -> str:
    node_lines = []
    for node in nodes:
        entry = {
            "id": node.get("id"),
            "path": node.get("path"),
            "node_type": node.get("node_type"),
            "title": node.get("title"),
            "status": node.get("status"),
            "themes": node.get("themes", []),
            "metaphors": node.get("metaphors", []),
            "channel": node.get("channel"),
            "summary": node.get("summary", ""),
        }
        if node.get("community") is not None:
            entry["community"] = node.get("community")
        if node.get("content"):
            entry["content"] = node.get("content")
        node_lines.append(json.dumps(entry, ensure_ascii=False))

    edge_lines = []
    for edge in edges:
        edge_lines.append(
            json.dumps(
                {
                    "type": edge.get("type"),
                    "from_path": node_by_id.get(edge["from"], {}).get("path"),
                    "from_title": node_by_id.get(edge["from"], {}).get("title"),
                    "to_path": node_by_id.get(edge["to"], {}).get("path"),
                    "to_title": node_by_id.get(edge["to"], {}).get("title"),
                    "weight": edge.get("weight"),
                    "evidence": edge.get("evidence", {}),
                },
                ensure_ascii=False,
            )
        )

    return "\n".join(["NODES:", *node_lines, "", "EDGES:", *edge_lines])


def ask_model(model: str, question: str, context: str, global_mode: bool = False) -> str:
    client = get_openai_client()
    if global_mode:
        instructions = (
            "You answer questions about a knowledge graph built from markdown files. "
            "You are given COMMUNITY SUMMARIES of the entire graph — clusters of related nodes, "
            "each listed with its most-connected members — not individual files. "
            "Use only the supplied summaries. Name the major themes across the whole corpus, "
            "describe the through-lines, and call out surprising bridges between communities. "
            + CREATIVITY_PROMPT
        )
        user_input = (
            f"Question:\n{question}\n\n"
            f"Whole-graph community summaries:\n{context}\n\n"
            "Answer in plain English: name the major themes and how they connect. "
            "End with a short 'Communities referenced' section listing the community names you used."
        )
    else:
        instructions = (
            "You answer questions about a repo graph built from markdown files. "
            "Use only the supplied graph context (node summaries, snippets of file content, and typed edges). "
            "Be concrete: mention file paths and relationship types when relevant. "
            "If the graph context is insufficient, say so clearly. "
            + CREATIVITY_PROMPT
        )
        user_input = (
            f"Question:\n{question}\n\n"
            f"Graph context:\n{context}\n\n"
            "Answer in plain English. Include a short 'Relevant files' section at the end. "
            "If your suggestion surprises you, that's a good sign."
        )
    response = client.responses.create(model=model, instructions=instructions, input=user_input)
    return response.output_text


def answer_question(
    question: str,
    nodes: List[Dict[str, Any]],
    edges: List[Dict[str, Any]],
    max_nodes: int,
    max_edges: int,
    model: str,
    retrieval: str = "lexical",
    client: Any = None,
    node_embs: Optional[Dict[str, List[float]]] = None,
    embed_model: str = DEFAULT_EMBED_MODEL,
    embed_cache: Optional[Dict[str, List[float]]] = None,
    mode: str = "auto",
    repo_root: Optional[Path] = None,
    with_content: bool = True,
    content_chars: int = 700,
    communities: Optional[Dict[Any, Dict[str, Any]]] = None,
    max_communities: int = 14,
) -> str:
    node_by_id = {n["id"]: n for n in nodes}

    # Resolve answering mode.
    eff_mode = mode
    if mode == "auto":
        eff_mode = "global" if (communities and looks_global(question)) else "local"
    elif mode == "global" and not communities:
        eff_mode = "local"

    # Resolve retrieval + query embedding.
    effective = retrieval
    query_emb: Optional[List[float]] = None
    if retrieval in ("embedding", "hybrid"):
        if client is None or node_embs is None:
            effective = "lexical"
        else:
            try:
                query_emb = embed_texts(
                    client, embed_model, [question], embed_cache if embed_cache is not None else {}
                )[0]
            except Exception as e:
                print(f"warning: query embedding failed ({e}); using lexical retrieval.", file=sys.stderr)
                effective = "lexical"
                query_emb = None

    if eff_mode == "global":
        node_scores = {n["id"]: s for s, n in rank_nodes(question, nodes, effective, node_embs, query_emb)}
        ranked_comms = rank_communities(communities, node_scores)[:max_communities]
        context = render_global_context(ranked_comms)
        return ask_model(model, question, context, global_mode=True)

    # Local mode.
    ranked_nodes = rank_nodes(question, nodes, effective, node_embs, query_emb)
    seed_nodes = [node for _, node in ranked_nodes[: max(4, max_nodes // 2)]]
    seed_ids = {n["id"] for n in seed_nodes}

    ranked_edges = rank_edges(question, edges, node_by_id, seed_ids)
    chosen_edges = [edge for _, edge in ranked_edges[:max_edges]]

    chosen_nodes = expand_with_neighbors(seed_nodes, ranked_edges, node_by_id, max_nodes)
    if with_content and repo_root is not None:
        attach_content(chosen_nodes, repo_root, question, content_chars)
    context = render_context(chosen_nodes, chosen_edges, node_by_id)
    return ask_model(model, question, context, global_mode=False)


def interactive_loop(
    nodes: List[Dict[str, Any]],
    edges: List[Dict[str, Any]],
    args: argparse.Namespace,
    client: Any,
    node_embs: Optional[Dict[str, List[float]]],
    embed_cache: Dict[str, List[float]],
    cache_path: Path,
    communities: Dict[Any, Dict[str, Any]],
    repo_root: Path,
    retrieval: str,
) -> None:
    print("Graph question mode. Type 'exit' to quit.\n")

    while True:
        try:
            question = input("graph> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if not question:
            continue
        if question.lower() in {"exit", "quit"}:
            break

        try:
            answer = answer_question(
                question, nodes, edges, args.max_nodes, args.max_edges, args.model,
                retrieval=retrieval, client=client, node_embs=node_embs,
                embed_model=args.embed_model, embed_cache=embed_cache,
                mode=args.mode, repo_root=repo_root, with_content=not args.no_content,
                content_chars=args.content_chars, communities=communities,
                max_communities=args.max_communities,
            )
            print("\n" + answer + "\n")
        except Exception as e:
            print(f"\nError: {e}\n", file=sys.stderr)

    save_embed_cache(cache_path, embed_cache)


def main() -> int:
    args = parse_args()

    if not os.getenv("OPENAI_API_KEY"):
        print("OPENAI_API_KEY is not set.", file=sys.stderr)
        return 2

    repo_root = Path(args.repo_root).resolve()

    try:
        nodes, edges = load_graph(repo_root, args.graph)
    except FileNotFoundError as e:
        print(str(e), file=sys.stderr)
        return 2

    if not nodes:
        print("Graph has no nodes.", file=sys.stderr)
        return 2

    communities = build_communities(nodes, edges, repo_root)
    print(
        f"Loaded {args.graph} graph: {len(nodes)} nodes, {len(edges)} edges, "
        f"{len(communities)} communities.",
        file=sys.stderr,
    )

    retrieval = args.retrieval
    client: Any = None
    node_embs: Optional[Dict[str, List[float]]] = None
    cache_path = repo_root / EMBED_CACHE_NAME
    embed_cache: Dict[str, List[float]] = {}

    if retrieval in ("embedding", "hybrid"):
        try:
            client = get_openai_client()
            embed_cache = load_embed_cache(cache_path)
            texts = [node_text(n) for n in nodes]
            n_missing = sum(
                1 for t in texts if _embed_key(args.embed_model, t if t.strip() else " ") not in embed_cache
            )
            if n_missing:
                print(
                    f"Embedding {n_missing} new/changed nodes (cached: {len(nodes) - n_missing})...",
                    file=sys.stderr,
                )
            vecs = embed_texts(client, args.embed_model, texts, embed_cache)
            node_embs = {n["id"]: v for n, v in zip(nodes, vecs)}
            save_embed_cache(cache_path, embed_cache)
        except Exception as e:
            print(f"warning: embeddings unavailable ({e}); using lexical retrieval.", file=sys.stderr)
            retrieval = "lexical"
            client = None
            node_embs = None

    # A client is still needed for answering even in lexical mode.
    if client is None:
        client = get_openai_client()

    if args.interactive:
        interactive_loop(
            nodes, edges, args, client, node_embs, embed_cache, cache_path,
            communities, repo_root, retrieval,
        )
        return 0

    if not args.question:
        print("Provide a question or use --interactive.", file=sys.stderr)
        return 2

    answer = answer_question(
        args.question, nodes, edges, args.max_nodes, args.max_edges, args.model,
        retrieval=retrieval, client=client, node_embs=node_embs,
        embed_model=args.embed_model, embed_cache=embed_cache,
        mode=args.mode, repo_root=repo_root, with_content=not args.no_content,
        content_chars=args.content_chars, communities=communities,
        max_communities=args.max_communities,
    )
    save_embed_cache(cache_path, embed_cache)
    print(answer)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
