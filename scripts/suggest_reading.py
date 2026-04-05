#!/usr/bin/env python3
"""
suggest_reading.py

Checks whether the graph has materially changed (using git history),
and if so, suggests books to read that explore the direction of change.

Usage:
    python scripts/suggest_reading.py --repo-root .
    python scripts/suggest_reading.py --repo-root . --since HEAD~3
    python scripts/suggest_reading.py --repo-root . --force

Outputs:
    queue/reading-candidates/reading-candidate-YYYY-MM-DD-NNN.md

Requires (at least one of):
    ANTHROPIC_API_KEY
    OPENAI_API_KEY
"""

from __future__ import annotations

import argparse
import json
import os
import random
import subprocess
import sys
from collections import Counter
from datetime import date
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


# ---------------------------------------------------------------------------
# Git helpers
# ---------------------------------------------------------------------------

def run_git(args: List[str], cwd: Path) -> str:
    result = subprocess.run(
        ["git"] + args,
        capture_output=True,
        text=True,
        cwd=cwd,
    )
    if result.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} failed: {result.stderr.strip()}")
    return result.stdout


def last_commit_touching_graph(repo_root: Path) -> Optional[str]:
    """Return the SHA of the most recent commit that changed graph/ files."""
    out = run_git(
        ["log", "--oneline", "--follow", "-1", "--", "graph/nodes.ndjson", "graph/edges.ndjson"],
        cwd=repo_root,
    ).strip()
    if not out:
        return None
    return out.split()[0]


def read_ndjson_at_commit(repo_root: Path, commit: str, rel_path: str) -> List[Dict[str, Any]]:
    """Read an ndjson file as it existed at a given git commit."""
    try:
        content = run_git(["show", f"{commit}:{rel_path}"], cwd=repo_root)
    except RuntimeError:
        return []
    return [json.loads(l) for l in content.splitlines() if l.strip()]


def read_ndjson(path: Path) -> List[Dict[str, Any]]:
    if not path.exists():
        return []
    return [json.loads(l) for l in path.read_text().splitlines() if l.strip()]


# ---------------------------------------------------------------------------
# Graph summarisation
# ---------------------------------------------------------------------------

def summarise(nodes: List[Dict[str, Any]], edges: List[Dict[str, Any]]) -> Dict[str, Any]:
    theme_counts: Counter = Counter()
    type_counts: Counter = Counter()
    metaphor_counts: Counter = Counter()
    edge_type_counts: Counter = Counter()

    for n in nodes:
        type_counts[n.get("node_type", "unknown")] += 1
        for t in n.get("themes") or []:
            theme_counts[t] += 1
        for m in n.get("metaphors") or []:
            metaphor_counts[m] += 1

    for e in edges:
        edge_type_counts[e.get("type", "unknown")] += 1

    return {
        "node_count": len(nodes),
        "edge_count": len(edges),
        "type_counts": dict(type_counts),
        "theme_counts": dict(theme_counts),
        "metaphor_counts": dict(metaphor_counts),
        "edge_type_counts": dict(edge_type_counts),
    }


def compute_delta(before: Dict[str, Any], after: Dict[str, Any]) -> Dict[str, Any]:
    """Return what changed between two graph summaries."""

    def counter_delta(a: Dict[str, int], b: Dict[str, int]) -> Dict[str, int]:
        keys = set(a) | set(b)
        return {k: b.get(k, 0) - a.get(k, 0) for k in keys if b.get(k, 0) != a.get(k, 0)}

    theme_delta = counter_delta(before["theme_counts"], after["theme_counts"])
    new_themes = [t for t, d in theme_delta.items() if d > 0 and t not in before["theme_counts"]]
    grown_themes = [t for t, d in theme_delta.items() if d > 0 and t in before["theme_counts"]]
    removed_themes = [t for t, d in theme_delta.items() if d < 0]

    metaphor_delta = counter_delta(before["metaphor_counts"], after["metaphor_counts"])
    new_metaphors = [m for m, d in metaphor_delta.items() if d > 0 and m not in before["metaphor_counts"]]

    type_delta = counter_delta(before["type_counts"], after["type_counts"])

    node_change = after["node_count"] - before["node_count"]
    edge_change = after["edge_count"] - before["edge_count"]

    return {
        "node_change": node_change,
        "edge_change": edge_change,
        "new_themes": sorted(new_themes),
        "grown_themes": sorted(grown_themes),
        "removed_themes": sorted(removed_themes),
        "new_metaphors": sorted(new_metaphors),
        "type_delta": {k: v for k, v in type_delta.items() if v != 0},
        "theme_delta": {k: v for k, v in theme_delta.items() if v != 0},
    }


def is_material(delta: Dict[str, Any]) -> bool:
    """Return True if the delta is substantial enough to warrant suggestions."""
    if delta["new_themes"]:
        return True
    if abs(delta["node_change"]) >= 3:
        return True
    if abs(delta["edge_change"]) >= 10:
        return True
    if len(delta["grown_themes"]) >= 3:
        return True
    if delta["new_metaphors"]:
        return True
    return False


# ---------------------------------------------------------------------------
# Prompt construction
# ---------------------------------------------------------------------------

SYSTEM_PROMPT = """\
You are a well-read advisor helping a nonfiction author figure out what books to read next.
The author is Mark Stringer, who writes and speaks about project management, software delivery,
creativity, and writing. His book is *Delivering the Impossible* (Springer).
He is also developing an Edinburgh Fringe show called *You Can Write a Book*.

You will be given a description of how a knowledge graph has changed recently.
Your job is to suggest 4–6 real books that would be interesting and useful to read,
given the direction of that change.

Rules:
- Suggest only real books that exist. Do not invent titles or authors.
- Each suggestion should include: title, author, one sentence on why it's relevant to the delta.
- Favour lateral connections over obvious ones.
- Prefer books that bridge the themes in unexpected ways.
- Be specific about *why* the graph change makes this book relevant now.
- Do not suggest books already in the repo's source material.
"""


def build_prompt(delta: Dict[str, Any], before: Dict[str, Any], after: Dict[str, Any]) -> str:
    lines = ["The knowledge graph has changed as follows:\n"]

    if delta["node_change"] != 0:
        lines.append(f"- Node count changed by {delta['node_change']:+d} (now {after['node_count']})")
    if delta["edge_change"] != 0:
        lines.append(f"- Edge count changed by {delta['edge_change']:+d} (now {after['edge_count']})")

    if delta["new_themes"]:
        lines.append(f"\nNew themes that appeared:\n  " + "\n  ".join(delta["new_themes"]))

    if delta["grown_themes"]:
        top_grown = sorted(delta["grown_themes"], key=lambda t: -delta["theme_delta"].get(t, 0))[:8]
        lines.append(f"\nThemes that grew most:\n  " + "\n  ".join(
            f"{t} (+{delta['theme_delta'][t]})" for t in top_grown
        ))

    if delta["removed_themes"]:
        lines.append(f"\nThemes that shrank or disappeared:\n  " + "\n  ".join(delta["removed_themes"][:5]))

    if delta["new_metaphors"]:
        lines.append(f"\nNew metaphors that appeared:\n  " + "\n  ".join(delta["new_metaphors"]))

    if delta["type_delta"]:
        lines.append("\nNode type changes:")
        for t, d in sorted(delta["type_delta"].items(), key=lambda x: -abs(x[1])):
            lines.append(f"  {t}: {d:+d}")

    top_after = sorted(after["theme_counts"].items(), key=lambda x: -x[1])[:10]
    lines.append("\nCurrent top themes in the graph:")
    for t, c in top_after:
        lines.append(f"  {t}: {c}")

    lines.append("\nBased on this, suggest 4–6 books Mark should read next.")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Model calls
# ---------------------------------------------------------------------------

def ask_openai(prompt: str) -> str:
    from openai import OpenAI
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY not set")
    client = OpenAI(api_key=api_key)
    model = os.getenv("OPENAI_MODEL", "gpt-4o")
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        max_tokens=1200,
    )
    return response.choices[0].message.content.strip()


def ask_claude(prompt: str) -> str:
    import anthropic
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("ANTHROPIC_API_KEY not set")
    client = anthropic.Anthropic(api_key=api_key)
    model = os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-6")
    message = client.messages.create(
        model=model,
        max_tokens=1200,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": prompt}],
    )
    return message.content[0].text.strip()


def ask_model(prompt: str) -> Tuple[str, str]:
    """Ask a randomly selected available model. Returns (provider, response)."""
    available = []
    if os.environ.get("OPENAI_API_KEY"):
        available.append("openai")
    if os.environ.get("ANTHROPIC_API_KEY"):
        available.append("claude")
    if not available:
        raise RuntimeError("Neither OPENAI_API_KEY nor ANTHROPIC_API_KEY is set.")

    provider = random.choice(available)
    if provider == "openai":
        return "openai", ask_openai(prompt)
    else:
        return "claude", ask_claude(prompt)


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------

def next_output_path(repo_root: Path) -> Path:
    out_dir = repo_root / "queue" / "reading-candidates"
    out_dir.mkdir(parents=True, exist_ok=True)
    today = date.today().isoformat()
    n = 1
    while True:
        path = out_dir / f"reading-candidate-{today}-{n:03d}.md"
        if not path.exists():
            return path
        n += 1


def write_output(
    repo_root: Path,
    delta: Dict[str, Any],
    suggestions: str,
    provider: str,
    since_commit: str,
) -> Path:
    path = next_output_path(repo_root)
    new_themes_line = ", ".join(delta["new_themes"]) if delta["new_themes"] else "none"
    grown_themes_line = ", ".join(delta["grown_themes"][:6]) if delta["grown_themes"] else "none"

    content = f"""---
date: {date.today().isoformat()}
type: reading-candidate
status: unread
model: {provider}
since_commit: {since_commit}
---

# Reading suggestions — {date.today().isoformat()}

## Graph change summary

- Nodes changed: {delta['node_change']:+d}
- Edges changed: {delta['edge_change']:+d}
- New themes: {new_themes_line}
- Grown themes: {grown_themes_line}
- New metaphors: {', '.join(delta['new_metaphors']) if delta['new_metaphors'] else 'none'}

## Suggested reading

{suggestions}
"""
    path.write_text(content, encoding="utf-8")
    return path


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".", help="Path to repo root")
    parser.add_argument(
        "--since",
        default=None,
        help="Compare against this git ref (default: last commit touching graph/)",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Generate suggestions even if the change is not material",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo_root = Path(args.repo_root).resolve()

    nodes_path = repo_root / "graph" / "nodes.ndjson"
    edges_path = repo_root / "graph" / "edges.ndjson"

    if not nodes_path.exists() or not edges_path.exists():
        print("Missing graph files. Run build_markdown_graph.py first.", file=sys.stderr)
        return 2

    # Determine the comparison commit
    since = args.since
    if since is None:
        # Find the commit before the most recent graph change
        log = run_git(
            ["log", "--oneline", "--", "graph/nodes.ndjson", "graph/edges.ndjson"],
            cwd=repo_root,
        ).strip().splitlines()
        if len(log) < 2:
            print("Not enough graph history to compare. Use --force to generate anyway.", file=sys.stderr)
            if not args.force:
                return 1
            since = log[0].split()[0] if log else "HEAD"
        else:
            # Compare HEAD against the commit before the most recent graph change
            since = log[1].split()[0]

    print(f"Comparing current graph against commit {since} ...", file=sys.stderr)

    before_nodes = read_ndjson_at_commit(repo_root, since, "graph/nodes.ndjson")
    before_edges = read_ndjson_at_commit(repo_root, since, "graph/edges.ndjson")
    after_nodes = read_ndjson(nodes_path)
    after_edges = read_ndjson(edges_path)

    before_summary = summarise(before_nodes, before_edges)
    after_summary = summarise(after_nodes, after_edges)
    delta = compute_delta(before_summary, after_summary)

    print(
        f"Delta: {delta['node_change']:+d} nodes, {delta['edge_change']:+d} edges, "
        f"{len(delta['new_themes'])} new themes, {len(delta['grown_themes'])} grown themes.",
        file=sys.stderr,
    )

    if not is_material(delta) and not args.force:
        print("No material change detected. Use --force to generate suggestions anyway.", file=sys.stderr)
        return 0

    prompt = build_prompt(delta, before_summary, after_summary)
    print("Asking model for book suggestions ...", file=sys.stderr)
    provider, suggestions = ask_model(prompt)

    out_path = write_output(repo_root, delta, suggestions, provider, since)
    print(f"Written to {out_path.relative_to(repo_root)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
