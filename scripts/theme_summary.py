#!/usr/bin/env python3
"""
theme_summary.py — answers "which themes land?"

Reads all observed posts with metrics and produces a ranked summary
of themes and metaphors by engagement score.

Usage:
    python scripts/theme_summary.py
    python scripts/theme_summary.py --sort likes
    python scripts/theme_summary.py --min-data  # only posts with actual metrics
"""

import argparse
import os
import sys
from pathlib import Path
from collections import defaultdict

import yaml


ENGAGEMENT_WEIGHTS = {
    "likes": 1,
    "comments": 3,   # comments signal stronger resonance than likes
    "shares": 2,
    "clicks": 1,
    "impressions": 0.01,  # scale down — impressions are much larger numbers
}


def parse_frontmatter(path: Path) -> dict | None:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return None
    end = text.index("---", 3)
    try:
        return yaml.safe_load(text[3:end])
    except yaml.YAMLError:
        return None


def engagement_score(metrics: dict) -> float | None:
    """Weighted engagement score. Returns None if no data at all."""
    if not metrics or all(v is None for k, v in metrics.items() if k in ENGAGEMENT_WEIGHTS):
        return None
    score = 0.0
    for field, weight in ENGAGEMENT_WEIGHTS.items():
        val = metrics.get(field)
        if val is not None:
            score += val * weight
    return score


def load_posts(posts_dir: Path) -> list[dict]:
    posts = []
    for md in sorted(posts_dir.glob("*.md")):
        fm = parse_frontmatter(md)
        if not fm:
            continue
        score = engagement_score(fm.get("metrics", {}))
        posts.append({
            "id": fm.get("id", md.stem),
            "title": fm.get("title", md.stem),
            "date": fm.get("date_published", ""),
            "channel": fm.get("channel", "unknown"),
            "themes": fm.get("themes") or [],
            "metaphors": fm.get("metaphors") or [],
            "metrics": fm.get("metrics") or {},
            "score": score,
        })
    return posts


def rank_by_theme(posts: list[dict], metric: str) -> dict[str, list]:
    """Group posts by theme, sorted by chosen metric within each theme."""
    by_theme = defaultdict(list)
    for post in posts:
        for theme in post["themes"]:
            by_theme[theme].append(post)
    # Sort posts within each theme
    for theme in by_theme:
        by_theme[theme].sort(
            key=lambda p: p["metrics"].get(metric) or 0,
            reverse=True
        )
    return by_theme


def theme_aggregate(posts: list[dict]) -> dict[str, dict]:
    """For each theme, aggregate metrics across all posts that use it."""
    agg = defaultdict(lambda: defaultdict(lambda: None))
    counts = defaultdict(int)
    scored = defaultdict(list)

    for post in posts:
        for theme in post["themes"]:
            counts[theme] += 1
            if post["score"] is not None:
                scored[theme].append(post["score"])
            for field in ["likes", "comments", "shares", "impressions", "clicks"]:
                val = post["metrics"].get(field)
                if val is not None:
                    current = agg[theme][field] or 0
                    agg[theme][field] = current + val

    result = {}
    for theme in counts:
        avg_score = (sum(scored[theme]) / len(scored[theme])) if scored[theme] else None
        result[theme] = {
            "post_count": counts[theme],
            "posts_with_data": len(scored[theme]),
            "avg_score": avg_score,
            **{k: v for k, v in agg[theme].items()},
        }
    return result


def metaphor_aggregate(posts: list[dict]) -> dict[str, dict]:
    """Same aggregation for metaphors."""
    agg = defaultdict(lambda: defaultdict(lambda: None))
    counts = defaultdict(int)
    scored = defaultdict(list)

    for post in posts:
        for metaphor in post["metaphors"]:
            counts[metaphor] += 1
            if post["score"] is not None:
                scored[metaphor].append(post["score"])
            for field in ["likes", "comments", "shares"]:
                val = post["metrics"].get(field)
                if val is not None:
                    current = agg[metaphor][field] or 0
                    agg[metaphor][field] = current + val

    result = {}
    for metaphor in counts:
        avg_score = (sum(scored[metaphor]) / len(scored[metaphor])) if scored[metaphor] else None
        result[metaphor] = {
            "post_count": counts[metaphor],
            "posts_with_data": len(scored[metaphor]),
            "avg_score": avg_score,
            **{k: v for k, v in agg[metaphor].items()},
        }
    return result


def fmt_val(v) -> str:
    if v is None:
        return "—"
    if isinstance(v, float):
        return f"{v:.1f}"
    return str(v)


def print_table(rows: list[tuple], headers: list[str], title: str):
    print(f"\n{'═' * 60}")
    print(f"  {title}")
    print(f"{'═' * 60}")
    col_widths = [len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            col_widths[i] = max(col_widths[i], len(str(cell)))
    fmt = "  " + "  ".join(f"{{:<{w}}}" for w in col_widths)
    print(fmt.format(*headers))
    print("  " + "  ".join("-" * w for w in col_widths))
    for row in rows:
        print(fmt.format(*row))


def main():
    parser = argparse.ArgumentParser(description="Summarise which themes and metaphors land")
    parser.add_argument("--repo-root", default=".", help="Path to repo root")
    parser.add_argument("--sort", default="score", choices=["score", "likes", "comments", "shares"],
                        help="Metric to sort by (default: score)")
    parser.add_argument("--min-data", action="store_true",
                        help="Only include posts that have at least one metric value")
    args = parser.parse_args()

    posts_dir = Path(args.repo_root) / "observed" / "posts"
    if not posts_dir.exists():
        print(f"Error: {posts_dir} not found", file=sys.stderr)
        sys.exit(1)

    posts = load_posts(posts_dir)
    if not posts:
        print("No posts found.")
        return

    if args.min_data:
        posts = [p for p in posts if p["score"] is not None]
        if not posts:
            print("No posts with metric data yet. Run metrics collection first.")
            return

    has_data = any(p["score"] is not None for p in posts)

    # ── Per-post summary ──────────────────────────────────────────────────────
    sort_key = args.sort if args.sort != "score" else None
    post_rows = []
    for p in sorted(posts, key=lambda x: (
        x["score"] if sort_key is None else (x["metrics"].get(sort_key) or 0)
    ) or 0, reverse=True):
        m = p["metrics"]
        post_rows.append((
            p["date"],
            p["title"][:35] + ("…" if len(p["title"]) > 35 else ""),
            fmt_val(m.get("likes")),
            fmt_val(m.get("comments")),
            fmt_val(m.get("shares")),
            fmt_val(m.get("impressions")),
            fmt_val(p["score"]),
        ))
    print_table(post_rows,
                ["Date", "Title", "Likes", "Cmts", "Shares", "Impr", "Score"],
                "Posts ranked by engagement")

    # ── Themes ────────────────────────────────────────────────────────────────
    theme_agg = theme_aggregate(posts)
    theme_rows = []
    for theme, data in sorted(theme_agg.items(),
                               key=lambda x: x[1]["avg_score"] or 0,
                               reverse=True):
        theme_rows.append((
            theme,
            data["post_count"],
            fmt_val(data.get("likes")),
            fmt_val(data.get("comments")),
            fmt_val(data.get("shares")),
            fmt_val(data["avg_score"]),
        ))
    print_table(theme_rows,
                ["Theme", "Posts", "Likes", "Cmts", "Shares", "Avg Score"],
                "Themes ranked by avg engagement score")

    # ── Metaphors ─────────────────────────────────────────────────────────────
    metaphor_agg = metaphor_aggregate(posts)
    metaphor_rows = []
    for metaphor, data in sorted(metaphor_agg.items(),
                                  key=lambda x: x[1]["avg_score"] or 0,
                                  reverse=True):
        metaphor_rows.append((
            metaphor,
            data["post_count"],
            fmt_val(data.get("likes")),
            fmt_val(data.get("comments")),
            fmt_val(data.get("shares")),
            fmt_val(data["avg_score"]),
        ))
    print_table(metaphor_rows,
                ["Metaphor", "Posts", "Likes", "Cmts", "Shares", "Avg Score"],
                "Metaphors ranked by avg engagement score")

    if not has_data:
        print("\n  (No metric data yet — all scores are zero. Run metrics collection to populate.)")
    print()


if __name__ == "__main__":
    main()
