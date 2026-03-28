#!/usr/bin/env python3
"""
ask_graph.py

Ask questions about the markdown graph in MarketingControlPlane.

Expected inputs:
- graph/nodes.ndjson
- graph/edges.ndjson

Usage:
    python scripts/ask_graph.py --repo-root . "What source files most often ground candidate posts?"
    python scripts/ask_graph.py --repo-root . --interactive

Requires:
    pip install openai
    export OPENAI_API_KEY=...

Notes:
- This script does simple local retrieval over the graph, then sends a compact context to ChatGPT.
- It does not modify the repo.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List, Tuple

from openai import OpenAI

DEFAULT_MODEL = os.getenv("OPENAI_MODEL", "gpt-5.4")


def get_openai_client() -> OpenAI:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is not set.")
    return OpenAI(api_key=api_key)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("question", nargs="?", help="Question to ask about the graph")
    parser.add_argument("--repo-root", default=".", help="Path to repo root")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="OpenAI model name")
    parser.add_argument("--max-nodes", type=int, default=12, help="Max nodes to include in context")
    parser.add_argument("--max-edges", type=int, default=20, help="Max edges to include in context")
    parser.add_argument("--interactive", action="store_true", help="Run an interactive REPL")
    return parser.parse_args()


def read_ndjson(path: Path) -> List[Dict[str, Any]]:
    items: List[Dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                items.append(json.loads(line))
    return items


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
    return " ".join(parts)


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


def rank_nodes(question: str, nodes: List[Dict[str, Any]]) -> List[Tuple[float, Dict[str, Any]]]:
    qtokens = tokenize(question)
    ranked = []
    for node in nodes:
        score = score_text(qtokens, node_text(node))
        if score > 0:
            ranked.append((score, node))
    ranked.sort(key=lambda x: (-x[0], x[1].get("path", "")))
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
        node_lines.append(
            json.dumps(
                {
                    "id": node.get("id"),
                    "path": node.get("path"),
                    "node_type": node.get("node_type"),
                    "title": node.get("title"),
                    "status": node.get("status"),
                    "themes": node.get("themes", []),
                    "metaphors": node.get("metaphors", []),
                    "channel": node.get("channel"),
                    "summary": node.get("summary", ""),
                },
                ensure_ascii=False,
            )
        )

    edge_lines = []
    for edge in edges:
        edge_lines.append(
            json.dumps(
                {
                    "type": edge.get("type"),
                    "from_path": node_by_id.get(edge["from"], {}).get("path"),
                    "to_path": node_by_id.get(edge["to"], {}).get("path"),
                    "weight": edge.get("weight"),
                    "evidence": edge.get("evidence", {}),
                },
                ensure_ascii=False,
            )
        )

    return "\n".join(
        [
            "NODES:",
            *node_lines,
            "",
            "EDGES:",
            *edge_lines,
        ]
    )


def ask_model(model: str, question: str, context: str) -> str:
    client = get_openai_client()
    response = client.responses.create(
        model=model,
        instructions=(
            "You answer questions about a repo graph built from markdown files. "
            "Use only the supplied graph context. "
            "Be concrete: mention file paths and relationship types when relevant. "
            "If the graph context is insufficient, say so clearly. "
            "Be weird. Look for unexpected combinations of source material that haven't been tried. "
            "Favour lateral connections over obvious ones — if two nodes share a surprising metaphor or theme, say so. "
            "Be speculative and experimental rather than safe or conservative. "
            "Suggest ideas that might feel slightly wrong or uncomfortable before they feel right. "
            "Avoid recommending the most obvious next step. If you notice an unusual edge or an underused source file, follow it."
        ),
        input=(
            f"Question:\n{question}\n\n"
            f"Graph context:\n{context}\n\n"
            "Answer in plain English. Include a short 'Relevant files' section at the end. "
            "If your suggestion surprises you, that's a good sign."
        ),
    )
    return response.output_text


def answer_question(
    question: str,
    nodes: List[Dict[str, Any]],
    edges: List[Dict[str, Any]],
    max_nodes: int,
    max_edges: int,
    model: str,
) -> str:
    node_by_id = {n["id"]: n for n in nodes}

    ranked_nodes = rank_nodes(question, nodes)
    seed_nodes = [node for _, node in ranked_nodes[: max(4, max_nodes // 2)]]
    seed_ids = {n["id"] for n in seed_nodes}

    ranked_edges = rank_edges(question, edges, node_by_id, seed_ids)
    chosen_edges = [edge for _, edge in ranked_edges[:max_edges]]

    chosen_nodes = expand_with_neighbors(seed_nodes, ranked_edges, node_by_id, max_nodes)
    context = render_context(chosen_nodes, chosen_edges, node_by_id)
    return ask_model(model, question, context)


def interactive_loop(
    nodes: List[Dict[str, Any]],
    edges: List[Dict[str, Any]],
    max_nodes: int,
    max_edges: int,
    model: str,
) -> None:
    print("Graph question mode. Type 'exit' to quit.\n")

    while True:
        try:
            question = input("graph> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return

        if not question:
            continue
        if question.lower() in {"exit", "quit"}:
            return

        try:
            answer = answer_question(question, nodes, edges, max_nodes, max_edges, model)
            print("\n" + answer + "\n")
        except Exception as e:
            print(f"\nError: {e}\n", file=sys.stderr)


def main() -> int:
    args = parse_args()

    if not os.getenv("OPENAI_API_KEY"):
        print("OPENAI_API_KEY is not set.", file=sys.stderr)
        return 2

    repo_root = Path(args.repo_root).resolve()
    nodes_path = repo_root / "graph" / "nodes.ndjson"
    edges_path = repo_root / "graph" / "edges.ndjson"

    if not nodes_path.exists() or not edges_path.exists():
        print(
            "Missing graph files. Expected:\n"
            f"  {nodes_path}\n"
            f"  {edges_path}\n"
            "Run build_markdown_graph.py first.",
            file=sys.stderr,
        )
        return 2

    nodes = read_ndjson(nodes_path)
    edges = read_ndjson(edges_path)

    if args.interactive:
        interactive_loop(nodes, edges, args.max_nodes, args.max_edges, args.model)
        return 0

    if not args.question:
        print("Provide a question or use --interactive.", file=sys.stderr)
        return 2

    answer = answer_question(args.question, nodes, edges, args.max_nodes, args.max_edges, args.model)
    print(answer)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
