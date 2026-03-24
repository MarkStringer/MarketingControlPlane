#!/usr/bin/env python3
"""
build_markdown_graph.py

Walk the MarketingControlPlane repo, turn every markdown file into a node,
and emit a first-pass graph as:

- graph/nodes.ndjson
- graph/edges.ndjson

Usage:
    python build_markdown_graph.py --repo-root .
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Set, Tuple


@dataclass
class Node:
    id: str
    path: str
    file_name: str
    node_type: str
    title: str
    status: str
    tags: List[str]
    themes: List[str]
    metaphors: List[str]
    topics: List[str]
    channel: Optional[str]
    date_published: Optional[str]
    risk: Optional[str]
    cta: Optional[str]
    trigger_type: Optional[str]
    source_docs: List[str]
    summary: str
    meta: Dict[str, Any]


@dataclass
class Edge:
    id: str
    from_id: str
    to_id: str
    edge_type: str
    weight: float
    evidence: Dict[str, Any]


SKIP_PARTS = {
    ".git",
    ".venv",
    "venv",
    "__pycache__",
    "node_modules",
    "graph",
}

THEME_FIELDS = ["themes", "book_themes", "topics"]
METAPHOR_FIELDS = ["metaphors", "related_metaphors"]
PATH_HEADING_PATTERNS = [
    "Candidate files written",
    "Items reviewed",
    "Hooks created",
    "Replies drafted",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".", help="Path to repo root")
    parser.add_argument("--out-dir", default="graph", help="Output directory")
    return parser.parse_args()


def should_skip(path: Path) -> bool:
    return any(part in SKIP_PARTS for part in path.parts)


def normalize_list(value: Any) -> List[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(v).strip() for v in value if str(v).strip()]
    if isinstance(value, str):
        value = value.strip()
        if not value:
            return []
        return [value]
    return [str(value).strip()]


def parse_scalar(value: str) -> Any:
    raw = value.strip()
    if not raw:
        return ""
    if raw.lower() in {"true", "false"}:
        return raw.lower() == "true"
    if raw.lower() in {"null", "none"}:
        return None
    if re.fullmatch(r"-?\d+", raw):
        try:
            return int(raw)
        except ValueError:
            return raw
    if re.fullmatch(r"-?\d+\.\d+", raw):
        try:
            return float(raw)
        except ValueError:
            return raw
    if (raw.startswith('"') and raw.endswith('"')) or (raw.startswith("'") and raw.endswith("'")):
        return raw[1:-1]
    return raw


def parse_frontmatter(text: str) -> Tuple[Dict[str, Any], str]:
    if not text.startswith("---\n"):
        return {}, text

    end = text.find("\n---\n", 4)
    if end == -1:
        return {}, text

    fm_text = text[4:end]
    body = text[end + 5 :]

    meta: Dict[str, Any] = {}
    current_list_key: Optional[str] = None

    for line in fm_text.splitlines():
        if not line.strip():
            continue

        if re.match(r"^\s*-\s+", line) and current_list_key:
            item = re.sub(r"^\s*-\s+", "", line).strip()
            meta.setdefault(current_list_key, []).append(parse_scalar(item))
            continue

        m = re.match(r"^([A-Za-z0-9_\-]+)\s*:\s*(.*)$", line)
        if not m:
            current_list_key = None
            continue

        key, value = m.group(1), m.group(2)
        if value == "":
            meta[key] = []
            current_list_key = key
        else:
            meta[key] = parse_scalar(value)
            current_list_key = None

    return meta, body


def derive_title(path: str, meta: Dict[str, Any], body: str) -> str:
    if meta.get("title"):
        return str(meta["title"]).strip()

    for line in body.splitlines():
        if line.startswith("# "):
            return line[2:].strip()

    return Path(path).stem.replace("-", " ").replace("_", " ").strip().title()


def short_summary(body: str, max_len: int = 240) -> str:
    text = re.sub(r"\s+", " ", body).strip()
    return text[:max_len].rsplit(" ", 1)[0] + "…" if len(text) > max_len else text


def normalize_path(path: Path, repo_root: Path) -> str:
    return str(path.relative_to(repo_root)).replace("\\", "/")


def infer_node_type(relpath: str) -> str:
    if relpath == "desired-state/launch-goals.md":
        return "desired_goal"
    if relpath == "desired-state/audiences.md":
        return "desired_audience"
    if relpath == "desired-state/message-house.md":
        return "desired_message_house"
    if relpath == "desired-state/channel-strategy.md":
        return "desired_channel_strategy"
    if relpath == "desired-state/content-policy.md":
        return "desired_content_policy"
    if relpath == "desired-state/cadence.md":
        return "desired_cadence"
    if relpath.startswith("desired-state/"):
        return "desired_goal"

    if relpath == "source/book/full-manuscript.md":
        return "source_book"
    if relpath.startswith("source/book/chapter-summaries/"):
        return "source_chapter_summary"
    if relpath == "source/book/key-quotes.md":
        return "source_quote_bank"
    if relpath == "source/book/metaphors.md":
        return "source_metaphor_index"
    if relpath.startswith("source/bibliography/"):
        return "source_bibliography_note"
    if relpath.startswith("source/youtube-transcripts/"):
        return "source_transcript"
    if relpath.startswith("source/posts/"):
        return "source_post"
    if relpath == "source/author-bio.md":
        return "source_author_bio"
    if relpath == "source/show-connections.md":
        return "source_show_connection"
    if relpath.startswith("source/"):
        return "source_document"

    if relpath.startswith("observed/posts/"):
        return "observed_post"
    if relpath.startswith("observed/replies/"):
        return "observed_reply"
    if relpath.startswith("observed/news/"):
        return "observed_news"
    if relpath.startswith("observed/conversations/"):
        return "observed_conversation"
    if relpath.startswith("observed/metrics/"):
        return "observed_metric"
    if relpath.startswith("observed/themes/"):
        return "observed_theme_coverage"

    if relpath.startswith("queue/post-candidates/"):
        return "candidate_post"
    if relpath.startswith("queue/reply-candidates/"):
        return "candidate_reply"
    if relpath.startswith("queue/news-hooks/"):
        return "candidate_news_hook"
    if relpath.startswith("queue/meme-ideas/"):
        return "candidate_meme"
    if relpath.startswith("queue/experiments/"):
        return "candidate_experiment"

    if relpath.startswith("decisions/approved/"):
        return "decision_approved"
    if relpath.startswith("decisions/rejected/"):
        return "decision_rejected"
    if relpath.startswith("decisions/rationale/"):
        return "decision_rationale"

    if relpath.startswith("agent-logs/content-scout/"):
        return "log_content_scout"
    if relpath.startswith("agent-logs/news-scout/"):
        return "log_news_scout"
    if relpath.startswith("agent-logs/reply-scout/"):
        return "log_reply_scout"
    if relpath.startswith("agent-logs/editor/"):
        return "log_editor"
    if relpath.startswith("agent-logs/drift-reports/"):
        return "log_drift_report"
    if relpath.startswith("agent-logs/"):
        return "log_agent"

    return "markdown_document"


def collect_markdown_files(repo_root: Path) -> List[Path]:
    files = []
    for path in repo_root.rglob("*.md"):
        if path.is_file() and not should_skip(path):
            files.append(path)
    return sorted(files)


def derive_tags(relpath: str, node_type: str) -> List[str]:
    tags = {node_type}
    parts = relpath.split("/")
    tags.update(p for p in parts[:-1] if p)
    stem = Path(relpath).stem
    tags.add(stem)
    return sorted(tags)


def build_node(path: Path, repo_root: Path) -> Node:
    raw = path.read_text(encoding="utf-8", errors="replace")
    meta, body = parse_frontmatter(raw)
    relpath = normalize_path(path, repo_root)
    node_type = infer_node_type(relpath)
    title = derive_title(relpath, meta, body)

    themes: Set[str] = set()
    for field in THEME_FIELDS:
        themes.update(normalize_list(meta.get(field)))

    metaphors: Set[str] = set()
    for field in METAPHOR_FIELDS:
        metaphors.update(normalize_list(meta.get(field)))

    topics = normalize_list(meta.get("topics"))
    source_docs = normalize_list(meta.get("source_docs"))

    return Node(
        id=f"node:{relpath}",
        path=relpath,
        file_name=path.name,
        node_type=node_type,
        title=title,
        status=str(meta.get("status", "unknown")),
        tags=derive_tags(relpath, node_type),
        themes=sorted(themes),
        metaphors=sorted(metaphors),
        topics=topics,
        channel=meta.get("channel"),
        date_published=meta.get("date_published") or meta.get("date"),
        risk=meta.get("risk"),
        cta=meta.get("cta"),
        trigger_type=meta.get("trigger_type"),
        source_docs=source_docs,
        summary=short_summary(body),
        meta=meta,
    )


def edge_id(from_id: str, edge_type: str, to_id: str) -> str:
    return f"edge:{from_id}->{edge_type}->{to_id}"


def make_edge(from_id: str, edge_type: str, to_id: str, weight: float, evidence: Dict[str, Any]) -> Edge:
    return Edge(
        id=edge_id(from_id, edge_type, to_id),
        from_id=from_id,
        to_id=to_id,
        edge_type=edge_type,
        weight=weight,
        evidence=evidence,
    )


def add_edge(edges: Dict[str, Edge], edge: Edge) -> None:
    edges.setdefault(edge.id, edge)


def find_path_mentions(text: str, candidate_paths: Iterable[str]) -> List[str]:
    found = []
    for path in candidate_paths:
        if path in text:
            found.append(path)
    return found


def extract_bullet_paths_under_heading(body: str, heading: str) -> List[str]:
    lines = body.splitlines()
    results: List[str] = []
    in_section = False

    for line in lines:
        stripped = line.strip()

        if stripped.startswith("#"):
            heading_text = stripped.lstrip("#").strip().lower()
            if heading_text == heading.lower():
                in_section = True
                continue
            elif in_section:
                break

        if in_section and stripped.startswith("- "):
            value = stripped[2:].strip()
            if value:
                results.append(value)

    return results


def build_edges(nodes: Dict[str, Node], bodies: Dict[str, str]) -> List[Edge]:
    edges: Dict[str, Edge] = {}
    path_to_id = {node.path: node.id for node in nodes.values()}
    node_list = list(nodes.values())

    # Rule: default desired-state edges to candidate posts
    desired_informs = [
        ("desired-state/launch-goals.md", "informs"),
        ("desired-state/message-house.md", "informs"),
        ("desired-state/channel-strategy.md", "targets"),
        ("desired-state/content-policy.md", "constrains"),
        ("desired-state/cadence.md", "constrains"),
    ]

    candidate_posts = [n for n in node_list if n.node_type == "candidate_post"]
    for candidate in candidate_posts:
        for relpath, edge_type in desired_informs:
            if relpath in path_to_id:
                add_edge(
                    edges,
                    make_edge(
                        path_to_id[relpath],
                        edge_type,
                        candidate.id,
                        0.95,
                        {"method": "default_control_plane_rule"},
                    ),
                )

    # Rule: source_docs -> grounds
    for node in node_list:
        for source_path in node.source_docs:
            if source_path in path_to_id:
                add_edge(
                    edges,
                    make_edge(
                        path_to_id[source_path],
                        "grounds",
                        node.id,
                        1.0,
                        {"method": "frontmatter_source_docs", "field": "source_docs"},
                    ),
                )
                if node.node_type == "candidate_post" and source_path.startswith("observed/posts/"):
                    add_edge(
                        edges,
                        make_edge(
                            node.id,
                            "follow_on_from",
                            path_to_id[source_path],
                            0.98,
                            {"method": "frontmatter_source_docs", "reason": "observed post used as source"},
                        ),
                    )

    # Rule: chapter summaries -> full manuscript
    full_ms = path_to_id.get("source/book/full-manuscript.md")
    if full_ms:
        for node in node_list:
            if node.node_type == "source_chapter_summary":
                add_edge(
                    edges,
                    make_edge(
                        node.id,
                        "summarises",
                        full_ms,
                        0.9,
                        {"method": "path_rule"},
                    ),
                )

    # Rule: bibliography references -> indexes
    ref_path = "source/bibliography/references.md"
    if ref_path in path_to_id:
        ref_id = path_to_id[ref_path]
        for node in node_list:
            if node.path.startswith("source/bibliography/") and node.path != ref_path:
                add_edge(
                    edges,
                    make_edge(
                        ref_id,
                        "indexes",
                        node.id,
                        0.85,
                        {"method": "path_rule"},
                    ),
                )

    # Rule: approval/rejection/published/logged/reviewed path mentions
    all_paths = list(path_to_id.keys())

    for node in node_list:
        body = bodies.get(node.path, "")

        if node.node_type in {"decision_approved", "decision_rejected"}:
            mentioned = find_path_mentions(body, [p for p in all_paths if p.startswith("queue/post-candidates/")])
            edge_type = "approved_from" if node.node_type == "decision_approved" else "rejected_from"
            for relpath in mentioned:
                add_edge(
                    edges,
                    make_edge(
                        node.id,
                        edge_type,
                        path_to_id[relpath],
                        0.95,
                        {"method": "body_path_mention"},
                    ),
                )

        if node.node_type == "observed_post":
            mentioned = find_path_mentions(body, [p for p in all_paths if p.startswith("queue/post-candidates/")])
            for relpath in mentioned:
                add_edge(
                    edges,
                    make_edge(
                        node.id,
                        "published_as",
                        path_to_id[relpath],
                        0.95,
                        {"method": "body_path_mention"},
                    ),
                )

        if node.node_type.startswith("log_"):
            for heading in PATH_HEADING_PATTERNS:
                mentioned_items = extract_bullet_paths_under_heading(body, heading)
                for item in mentioned_items:
                    item = item.replace("\\", "/")
                    if item in path_to_id:
                        edge_type = "reviewed_in" if "review" in heading.lower() else "logged_by"
                        add_edge(
                            edges,
                            make_edge(
                                path_to_id[item],
                                edge_type,
                                node.id,
                                0.9,
                                {"method": "log_heading_bullets", "heading": heading},
                            ),
                        )

            # fallback: if log mentions candidate paths anywhere
            mentioned = find_path_mentions(body, [p for p in all_paths if p.startswith("queue/")])
            for relpath in mentioned:
                add_edge(
                    edges,
                    make_edge(
                        path_to_id[relpath],
                        "logged_by",
                        node.id,
                        0.6,
                        {"method": "body_path_mention_fallback"},
                    ),
                )

    # Inferred semantic edges
    for i, a in enumerate(node_list):
        for b in node_list[i + 1 :]:
            # same_theme_as
            shared_themes = sorted(set(a.themes) & set(b.themes))
            if shared_themes:
                add_edge(
                    edges,
                    make_edge(
                        a.id,
                        "same_theme_as",
                        b.id,
                        0.5,
                        {"method": "theme_overlap", "shared_values": shared_themes},
                    ),
                )

            # same_metaphor_as
            shared_metaphors = sorted(set(a.metaphors) & set(b.metaphors))
            if shared_metaphors:
                add_edge(
                    edges,
                    make_edge(
                        a.id,
                        "same_metaphor_as",
                        b.id,
                        0.55,
                        {"method": "metaphor_overlap", "shared_values": shared_metaphors},
                    ),
                )

            # same_channel_as
            if a.channel and b.channel and a.channel == b.channel:
                add_edge(
                    edges,
                    make_edge(
                        a.id,
                        "same_channel_as",
                        b.id,
                        0.45,
                        {"method": "channel_match", "shared_values": [a.channel]},
                    ),
                )

    return list(edges.values())


def node_to_dict(node: Node) -> Dict[str, Any]:
    return {
        "id": node.id,
        "path": node.path,
        "file_name": node.file_name,
        "node_type": node.node_type,
        "title": node.title,
        "status": node.status,
        "tags": node.tags,
        "themes": node.themes,
        "metaphors": node.metaphors,
        "topics": node.topics,
        "channel": node.channel,
        "date_published": node.date_published,
        "risk": node.risk,
        "cta": node.cta,
        "trigger_type": node.trigger_type,
        "source_docs": node.source_docs,
        "summary": node.summary,
    }


def edge_to_dict(edge: Edge) -> Dict[str, Any]:
    return {
        "id": edge.id,
        "from": edge.from_id,
        "to": edge.to_id,
        "type": edge.edge_type,
        "weight": edge.weight,
        "evidence": edge.evidence,
    }


def main() -> int:
    args = parse_args()
    repo_root = Path(args.repo_root).resolve()
    out_dir = (repo_root / args.out_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    md_files = collect_markdown_files(repo_root)
    nodes: Dict[str, Node] = {}
    bodies: Dict[str, str] = {}

    for path in md_files:
        raw = path.read_text(encoding="utf-8", errors="replace")
        meta, body = parse_frontmatter(raw)
        relpath = normalize_path(path, repo_root)
        bodies[relpath] = body
        node = build_node(path, repo_root)
        nodes[node.id] = node

    edges = build_edges(nodes, bodies)

    nodes_path = out_dir / "nodes.ndjson"
    edges_path = out_dir / "edges.ndjson"

    with nodes_path.open("w", encoding="utf-8") as f:
        for node in sorted(nodes.values(), key=lambda n: n.path):
            f.write(json.dumps(node_to_dict(node), ensure_ascii=False) + "\n")

    with edges_path.open("w", encoding="utf-8") as f:
        for edge in sorted(edges, key=lambda e: (e.edge_type, e.from_id, e.to_id)):
            f.write(json.dumps(edge_to_dict(edge), ensure_ascii=False) + "\n")

    print(f"Wrote {nodes_path}")
    print(f"Wrote {edges_path}")
    print(f"Nodes: {len(nodes)}")
    print(f"Edges: {len(edges)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
