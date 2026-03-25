#!/usr/bin/env python3
"""
edit_graph.py

Make basic changes to graph/nodes.ndjson and graph/edges.ndjson for the
MarketingControlPlane repo.

IMPORTANT
---------
This script edits the generated graph files directly. If you later rebuild the
graph from markdown with build_markdown_graph.py, your manual changes may be
overwritten.

Use this for:
- quick experiments
- temporary fixes
- manual annotations
- investigating graph behavior

For persistent changes, prefer:
- editing the underlying markdown files, or
- extending build_markdown_graph.py

Usage examples:
    python scripts/edit_graph.py --repo-root . stats
    python scripts/edit_graph.py --repo-root . list-nodes --type candidate_post
    python scripts/edit_graph.py --repo-root . add-edge \
        --from "source/book/metaphors.md" \
        --to "queue/post-candidates/post-candidate-2026-03-22-001.md" \
        --type grounds \
        --weight 0.95
    python scripts/edit_graph.py --repo-root . set-node-field \
        --node "queue/post-candidates/post-candidate-2026-03-22-001.md" \
        --field status \
        --value approved
    python scripts/edit_graph.py --repo-root . add-list-value \
        --node "source/book/metaphors.md" \
        --field themes \
        --value ways_of_seeing
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


NODE_FIELDS = {
    "id",
    "path",
    "file_name",
    "node_type",
    "title",
    "status",
    "tags",
    "themes",
    "metaphors",
    "topics",
    "channel",
    "date_published",
    "risk",
    "cta",
    "trigger_type",
    "source_docs",
    "summary",
}

LIST_FIELDS = {"tags", "themes", "metaphors", "topics", "source_docs"}
EDGE_TYPES_HINT = {
    "informs",
    "constrains",
    "targets",
    "grounds",
    "quotes",
    "cites",
    "summarises",
    "indexes",
    "inspired_by",
    "extracts_from",
    "reframes",
    "follow_on_from",
    "responds_to",
    "reviewed_in",
    "approved_from",
    "rejected_from",
    "published_as",
    "logged_by",
    "tests",
    "same_theme_as",
    "same_metaphor_as",
    "same_channel_as",
    "same_audience_as",
    "contrasts_with",
    "elaborates",
    "compresses",
}


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Edit graph/nodes.ndjson and graph/edges.ndjson")
    parser.add_argument("--repo-root", default=".", help="Path to repo root")
    parser.add_argument("--no-backup", action="store_true", help="Skip backup before writing changes")

    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("stats", help="Show graph counts")

    p = subparsers.add_parser("list-nodes", help="List nodes")
    p.add_argument("--type", dest="node_type", help="Filter by node_type")
    p.add_argument("--path-contains", help="Filter by path substring")
    p.add_argument("--limit", type=int, default=50)

    p = subparsers.add_parser("list-edges", help="List edges")
    p.add_argument("--type", dest="edge_type", help="Filter by edge type")
    p.add_argument("--from", dest="from_ref", help="Filter by from node path or id")
    p.add_argument("--to", dest="to_ref", help="Filter by to node path or id")
    p.add_argument("--limit", type=int, default=50)

    p = subparsers.add_parser("set-node-field", help="Set a scalar or JSON field on a node")
    p.add_argument("--node", required=True, help="Node path or node id")
    p.add_argument("--field", required=True, help="Node field name")
    p.add_argument("--value", required=True, help="Field value")
    p.add_argument("--value-type", choices=["str", "int", "float", "bool", "json", "null"], default="str")

    p = subparsers.add_parser("add-list-value", help="Add a value to a node list field")
    p.add_argument("--node", required=True, help="Node path or node id")
    p.add_argument("--field", required=True, choices=sorted(LIST_FIELDS))
    p.add_argument("--value", required=True)

    p = subparsers.add_parser("remove-list-value", help="Remove a value from a node list field")
    p.add_argument("--node", required=True, help="Node path or node id")
    p.add_argument("--field", required=True, choices=sorted(LIST_FIELDS))
    p.add_argument("--value", required=True)

    p = subparsers.add_parser("add-edge", help="Add an edge")
    p.add_argument("--from", dest="from_ref", required=True, help="From node path or id")
    p.add_argument("--to", dest="to_ref", required=True, help="To node path or id")
    p.add_argument("--type", dest="edge_type", required=True, help="Edge type")
    p.add_argument("--weight", type=float, default=0.5, help="Edge weight")
    p.add_argument("--evidence-json", default="{}", help='JSON object, e.g. \'{"method":"manual"}\'')

    p = subparsers.add_parser("remove-edge", help="Remove an edge by from/to/type")
    p.add_argument("--from", dest="from_ref", required=True, help="From node path or id")
    p.add_argument("--to", dest="to_ref", required=True, help="To node path or id")
    p.add_argument("--type", dest="edge_type", required=True, help="Edge type")

    p = subparsers.add_parser("set-edge-weight", help="Update edge weight by from/to/type")
    p.add_argument("--from", dest="from_ref", required=True, help="From node path or id")
    p.add_argument("--to", dest="to_ref", required=True, help="To node path or id")
    p.add_argument("--type", dest="edge_type", required=True, help="Edge type")
    p.add_argument("--weight", required=True, type=float)

    p = subparsers.add_parser("delete-node", help="Delete a node and optionally its incident edges")
    p.add_argument("--node", required=True, help="Node path or node id")
    p.add_argument("--remove-incidents", action="store_true", help="Also delete touching edges")

    return parser.parse_args()


def read_ndjson(path: Path) -> List[Dict[str, Any]]:
    items: List[Dict[str, Any]] = []
    if not path.exists():
        return items
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                items.append(json.loads(line))
    return items


def write_ndjson(path: Path, items: List[Dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8") as f:
        for item in items:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")


def backup_file(path: Path, backup_dir: Path) -> Optional[Path]:
    if not path.exists():
        return None
    backup_dir.mkdir(parents=True, exist_ok=True)
    stamp = utc_now_iso().replace(":", "").replace("-", "")
    backup_path = backup_dir / f"{path.name}.{stamp}.bak"
    shutil.copy2(path, backup_path)
    return backup_path


def coerce_value(value: str, value_type: str) -> Any:
    if value_type == "str":
        return value
    if value_type == "int":
        return int(value)
    if value_type == "float":
        return float(value)
    if value_type == "bool":
        lowered = value.strip().lower()
        if lowered in {"true", "1", "yes", "y"}:
            return True
        if lowered in {"false", "0", "no", "n"}:
            return False
        raise ValueError(f"Cannot parse bool value: {value}")
    if value_type == "json":
        return json.loads(value)
    if value_type == "null":
        return None
    raise ValueError(f"Unsupported value_type: {value_type}")


def edge_id(from_id: str, edge_type: str, to_id: str) -> str:
    return f"edge:{from_id}->{edge_type}->{to_id}"


def index_nodes(nodes: List[Dict[str, Any]]) -> Tuple[Dict[str, Dict[str, Any]], Dict[str, Dict[str, Any]]]:
    by_id = {node["id"]: node for node in nodes}
    by_path = {node["path"]: node for node in nodes if "path" in node}
    return by_id, by_path


def resolve_node(ref: str, nodes: List[Dict[str, Any]]) -> Dict[str, Any]:
    by_id, by_path = index_nodes(nodes)
    if ref in by_id:
        return by_id[ref]
    if ref in by_path:
        return by_path[ref]
    prefixed = f"node:{ref}"
    if prefixed in by_id:
        return by_id[prefixed]
    raise KeyError(f"Could not find node by id or path: {ref}")


def find_edge(edges: List[Dict[str, Any]], from_id: str, edge_type: str, to_id: str) -> Optional[Dict[str, Any]]:
    wanted_id = edge_id(from_id, edge_type, to_id)
    for edge in edges:
        if edge.get("id") == wanted_id:
            return edge
    return None


def cmd_stats(nodes: List[Dict[str, Any]], edges: List[Dict[str, Any]]) -> int:
    node_types = {}
    edge_types = {}
    for node in nodes:
        node_types[node["node_type"]] = node_types.get(node["node_type"], 0) + 1
    for edge in edges:
        edge_types[edge["type"]] = edge_types.get(edge["type"], 0) + 1

    print(f"Nodes: {len(nodes)}")
    print(f"Edges: {len(edges)}")
    print("\nNode types:")
    for k in sorted(node_types):
        print(f"  {k}: {node_types[k]}")
    print("\nEdge types:")
    for k in sorted(edge_types):
        print(f"  {k}: {edge_types[k]}")
    return 0


def cmd_list_nodes(args: argparse.Namespace, nodes: List[Dict[str, Any]]) -> int:
    rows = nodes
    if args.node_type:
        rows = [n for n in rows if n.get("node_type") == args.node_type]
    if args.path_contains:
        rows = [n for n in rows if args.path_contains in n.get("path", "")]
    for node in rows[: args.limit]:
        print(f'{node["id"]} | {node.get("node_type")} | {node.get("path")} | {node.get("title")}')
    print(f"\nShown {min(len(rows), args.limit)} of {len(rows)} matching nodes.")
    return 0


def cmd_list_edges(args: argparse.Namespace, nodes: List[Dict[str, Any]], edges: List[Dict[str, Any]]) -> int:
    node_by_id = {n["id"]: n for n in nodes}
    rows = edges

    if args.edge_type:
        rows = [e for e in rows if e.get("type") == args.edge_type]
    if args.from_ref:
        from_node = resolve_node(args.from_ref, nodes)
        rows = [e for e in rows if e.get("from") == from_node["id"]]
    if args.to_ref:
        to_node = resolve_node(args.to_ref, nodes)
        rows = [e for e in rows if e.get("to") == to_node["id"]]

    for edge in rows[: args.limit]:
        from_path = node_by_id.get(edge["from"], {}).get("path", edge["from"])
        to_path = node_by_id.get(edge["to"], {}).get("path", edge["to"])
        print(f'{edge["type"]} | {from_path} -> {to_path} | weight={edge.get("weight")}')
    print(f"\nShown {min(len(rows), args.limit)} of {len(rows)} matching edges.")
    return 0


def cmd_set_node_field(args: argparse.Namespace, nodes: List[Dict[str, Any]]) -> int:
    node = resolve_node(args.node, nodes)
    if args.field not in NODE_FIELDS:
        print(f"Warning: {args.field!r} is not in the known node field set.", file=sys.stderr)
    value = coerce_value(args.value, args.value_type)
    node[args.field] = value
    print(f"Updated {node['path']}: set {args.field} = {value!r}")
    return 1


def cmd_add_list_value(args: argparse.Namespace, nodes: List[Dict[str, Any]]) -> int:
    node = resolve_node(args.node, nodes)
    values = node.get(args.field) or []
    if not isinstance(values, list):
        raise TypeError(f"Field {args.field} is not a list on node {node['path']}")
    if args.value not in values:
        values.append(args.value)
        node[args.field] = values
        print(f"Added {args.value!r} to {args.field} on {node['path']}")
        return 1
    print(f"Value already present on {node['path']}: {args.value!r}")
    return 0


def cmd_remove_list_value(args: argparse.Namespace, nodes: List[Dict[str, Any]]) -> int:
    node = resolve_node(args.node, nodes)
    values = node.get(args.field) or []
    if not isinstance(values, list):
        raise TypeError(f"Field {args.field} is not a list on node {node['path']}")
    if args.value in values:
        node[args.field] = [v for v in values if v != args.value]
        print(f"Removed {args.value!r} from {args.field} on {node['path']}")
        return 1
    print(f"Value not present on {node['path']}: {args.value!r}")
    return 0


def cmd_add_edge(args: argparse.Namespace, nodes: List[Dict[str, Any]], edges: List[Dict[str, Any]]) -> int:
    from_node = resolve_node(args.from_ref, nodes)
    to_node = resolve_node(args.to_ref, nodes)

    evidence = json.loads(args.evidence_json)
    existing = find_edge(edges, from_node["id"], args.edge_type, to_node["id"])
    if existing:
        print("Edge already exists:")
        print(json.dumps(existing, ensure_ascii=False, indent=2))
        return 0

    edge = {
        "id": edge_id(from_node["id"], args.edge_type, to_node["id"]),
        "from": from_node["id"],
        "to": to_node["id"],
        "type": args.edge_type,
        "weight": args.weight,
        "evidence": evidence,
    }
    edges.append(edge)

    if args.edge_type not in EDGE_TYPES_HINT:
        print(f"Warning: {args.edge_type!r} is not in the known edge type set.", file=sys.stderr)
    print(f"Added edge: {args.edge_type} | {from_node['path']} -> {to_node['path']}")
    return 1


def cmd_remove_edge(args: argparse.Namespace, nodes: List[Dict[str, Any]], edges: List[Dict[str, Any]]) -> int:
    from_node = resolve_node(args.from_ref, nodes)
    to_node = resolve_node(args.to_ref, nodes)
    target = edge_id(from_node["id"], args.edge_type, to_node["id"])

    before = len(edges)
    edges[:] = [e for e in edges if e.get("id") != target]
    changed = before - len(edges)
    if changed:
        print(f"Removed edge: {args.edge_type} | {from_node['path']} -> {to_node['path']}")
        return 1
    print("No matching edge found.")
    return 0


def cmd_set_edge_weight(args: argparse.Namespace, nodes: List[Dict[str, Any]], edges: List[Dict[str, Any]]) -> int:
    from_node = resolve_node(args.from_ref, nodes)
    to_node = resolve_node(args.to_ref, nodes)
    existing = find_edge(edges, from_node["id"], args.edge_type, to_node["id"])
    if not existing:
        print("No matching edge found.", file=sys.stderr)
        return 0
    existing["weight"] = args.weight
    print(f"Updated weight: {args.edge_type} | {from_node['path']} -> {to_node['path']} = {args.weight}")
    return 1


def cmd_delete_node(args: argparse.Namespace, nodes: List[Dict[str, Any]], edges: List[Dict[str, Any]]) -> int:
    node = resolve_node(args.node, nodes)
    before_nodes = len(nodes)
    nodes[:] = [n for n in nodes if n["id"] != node["id"]]
    node_changed = before_nodes - len(nodes)

    edge_changed = 0
    if args.remove_incidents:
        before_edges = len(edges)
        edges[:] = [e for e in edges if e.get("from") != node["id"] and e.get("to") != node["id"]]
        edge_changed = before_edges - len(edges)

    print(f"Deleted node: {node['path']}")
    if args.remove_incidents:
        print(f"Removed incident edges: {edge_changed}")
    else:
        print("Note: incident edges were left in place. Use --remove-incidents to remove them.")
    return 1 if node_changed else 0


def main() -> int:
    args = parse_args()
    repo_root = Path(args.repo_root).resolve()
    graph_dir = repo_root / "graph"
    nodes_path = graph_dir / "nodes.ndjson"
    edges_path = graph_dir / "edges.ndjson"

    if not nodes_path.exists() or not edges_path.exists():
        print(
            "Missing graph files.\n"
            f"Expected:\n  {nodes_path}\n  {edges_path}\n"
            "Run build_markdown_graph.py first.",
            file=sys.stderr,
        )
        return 2

    nodes = read_ndjson(nodes_path)
    edges = read_ndjson(edges_path)

    changed = 0

    if args.command == "stats":
        return cmd_stats(nodes, edges)

    if args.command == "list-nodes":
        return cmd_list_nodes(args, nodes)

    if args.command == "list-edges":
        return cmd_list_edges(args, nodes, edges)

    if args.command == "set-node-field":
        changed = cmd_set_node_field(args, nodes)

    elif args.command == "add-list-value":
        changed = cmd_add_list_value(args, nodes)

    elif args.command == "remove-list-value":
        changed = cmd_remove_list_value(args, nodes)

    elif args.command == "add-edge":
        changed = cmd_add_edge(args, nodes, edges)

    elif args.command == "remove-edge":
        changed = cmd_remove_edge(args, nodes, edges)

    elif args.command == "set-edge-weight":
        changed = cmd_set_edge_weight(args, nodes, edges)

    elif args.command == "delete-node":
        changed = cmd_delete_node(args, nodes, edges)

    else:
        raise ValueError(f"Unsupported command: {args.command}")

    if changed:
        if not args.no_backup:
            backup_dir = graph_dir / "backups"
            backup_nodes = backup_file(nodes_path, backup_dir)
            backup_edges = backup_file(edges_path, backup_dir)
            if backup_nodes:
                print(f"Backed up nodes to {backup_nodes}")
            if backup_edges:
                print(f"Backed up edges to {backup_edges}")

        write_ndjson(nodes_path, nodes)
        write_ndjson(edges_path, edges)
        print(f"Wrote {nodes_path}")
        print(f"Wrote {edges_path}")
    else:
        print("No changes written.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
