#!/usr/bin/env python3
"""
run_content_scout.py

First-pass content scout for the MarketingControlPlane repo.

What it does:
- Reads a bounded set of markdown files from the repo
- Builds a compact context pack
- Prioritises recently changed markdown files under source/ as inspiration
- Prioritises recently changed markdown files under observed/posts/ as follow-on inspiration
- Calls the OpenAI Responses API for grounded post candidates
- Writes candidates into queue/post-candidates/
- Writes a run log into agent-logs/content-scout/

Usage:
    python scripts/run_content_scout.py --repo-root .
    python scripts/run_content_scout.py --repo-root . --count 3 --model gpt-5.4
    python scripts/run_content_scout.py --repo-root . --dry-run
    python scripts/run_content_scout.py --repo-root . --ignore-recent-source-changes
    python scripts/run_content_scout.py --repo-root . --ignore-recent-observed-post-changes

Environment:
    OPENAI_API_KEY must be set.
    OPENAI_MODEL is optional and overrides the default model.

Notes:
- This script is intentionally conservative: it only writes candidate files and logs.
- It does not publish anything.
- It prefers local repo reads over hosted retrieval for this first pass.
- It treats recent changes under source/ as higher-priority inspiration.
- It treats recent changes under observed/posts/ as prompts for follow-on or adjacent posts.
"""

from __future__ import annotations

import argparse
import json
import os
import random
import re
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None  # type: ignore

try:
    from anthropic import Anthropic
except ImportError:
    Anthropic = None  # type: ignore


DEFAULT_OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o")
DEFAULT_ANTHROPIC_MODEL = os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-6")

ALLOWED_CHANNELS = ["linkedin", "x", "blog_newsletter"]
ALLOWED_RISK = ["low", "medium", "high"]
ALLOWED_CTA = ["none", "soft", "direct"]
ALLOWED_TRIGGER_TYPES = [
    "evergreen",
    "transcript_led",
    "show_led",
    "book_led",
    "promotional",
    "follow_on",
]

PRIORITY_PATTERNS = [
    "desired-state/**/*.md",
    "source/book/metaphors.md",
    "source/book/key-quotes.md",
    "source/book/chapter-summaries/**/*.md",
    "source/book/**/*.md",
    "source/youtube-transcripts/**/*.md",
    "source/**/*.md",
    "observed/posts/**/*.md",
]

SKIP_PARTS = {
    ".git",
    ".github",
    ".venv",
    "venv",
    "__pycache__",
    "node_modules",
    "queue",          # do not feed existing queue back in
    "agent-logs",     # avoid log echo
    "decisions",      # keep v1 simple
}

SYSTEM_PROMPT = """
You are Content Scout for a markdown-based marketing control plane for a book launch.

Your job:
- Read the supplied repo documents.
- Produce grounded candidate social posts.
- Prefer distinctive ideas from the book/transcripts/show over generic project-management commentary.
- Do not invent quotes.
- Do not claim you read files that were not supplied.
- Use plain, vivid language.
- Each candidate should feel like it comes from the author's actual ideas.
- One candidate should be wild and crazy.
- One candidate should be grounded in transcript/show material.
- If recently changed observed/posts documents are supplied, treat them as evidence of what has just been posted and use them to suggest at least one sensible follow-on, sequel, adjacent angle, or next-step post when relevant.
- One candidate can be a softer promotional/book-aware post, but keep the CTA restrained unless the context clearly supports it.
- Novelty matters. If observed posts are present, avoid repeating them too closely.
- Every candidate must explain why it exists and which source files support it.
- If recently changed source documents are supplied, treat them as fresh inspiration for at least one candidate when relevant.
"""

JSON_SCHEMA: Dict[str, Any] = {
    "type": "object",
    "additionalProperties": False,
    "required": ["run_summary", "documents_used", "candidates"],
    "properties": {
        "run_summary": {
            "type": "string",
            "description": "Short summary of what this run chose to focus on."
        },
        "documents_used": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Repo-relative paths of the documents actually used."
        },
        "candidates": {
            "type": "array",
            "minItems": 1,
            "maxItems": 6,
            "items": {
                "type": "object",
                "additionalProperties": False,
                "required": [
                    "working_title",
                    "channel",
                    "theme",
                    "metaphors",
                    "trigger_type",
                    "risk",
                    "cta",
                    "hook",
                    "draft",
                    "rationale",
                    "why_now",
                    "source_docs",
                    "source_ideas",
                    "novelty_note",
                    "risk_note",
                ],
                "properties": {
                    "working_title": {"type": "string"},
                    "channel": {"type": "string", "enum": ALLOWED_CHANNELS},
                    "theme": {"type": "string"},
                    "metaphors": {
                        "type": "array",
                        "items": {"type": "string"},
                    },
                    "trigger_type": {"type": "string", "enum": ALLOWED_TRIGGER_TYPES},
                    "risk": {"type": "string", "enum": ALLOWED_RISK},
                    "cta": {"type": "string", "enum": ALLOWED_CTA},
                    "hook": {"type": "string"},
                    "draft": {"type": "string"},
                    "rationale": {"type": "string"},
                    "why_now": {"type": "string"},
                    "source_docs": {
                        "type": "array",
                        "items": {"type": "string"},
                    },
                    "source_ideas": {
                        "type": "array",
                        "items": {"type": "string"},
                    },
                    "novelty_note": {"type": "string"},
                    "risk_note": {"type": "string"},
                },
            },
        },
    },
}


@dataclass
class RepoDoc:
    path: Path
    relpath: str
    meta: Dict[str, Any]
    body: str
    excerpt: str
    score: float


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def slugify(text: str, max_len: int = 48) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = text.strip("-")
    return text[:max_len] or "untitled"


def compact_whitespace(text: str) -> str:
    return re.sub(r"[ \t]+", " ", text).strip()


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
    """
    Very small frontmatter parser.
    Supports:
    ---
    key: value
    list_key:
      - item
      - item
    ---
    """
    if not text.startswith("---\n"):
        return {}, text

    end = text.find("\n---\n", 4)
    if end == -1:
        return {}, text

    fm_text = text[4:end]
    body = text[end + 5 :]

    meta: Dict[str, Any] = {}
    current_list_key: str | None = None

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


def yaml_quote(value: Any) -> str:
    if value is None:
        return '""'
    text = str(value)
    text = text.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{text}"'


def yaml_list(key: str, values: List[Any]) -> str:
    lines = [f"{key}:"]
    if not values:
        lines.append('  - ""')
        return "\n".join(lines)
    for v in values:
        lines.append(f"  - {yaml_quote(v)}")
    return "\n".join(lines)


def dump_frontmatter(data: Dict[str, Any]) -> str:
    lines = ["---"]
    for key, value in data.items():
        if isinstance(value, list):
            lines.append(yaml_list(key, value))
        else:
            lines.append(f"{key}: {yaml_quote(value)}")
    lines.append("---")
    return "\n".join(lines)


def should_skip(path: Path) -> bool:
    return any(part in SKIP_PARTS for part in path.parts)


def collect_markdown_files(repo_root: Path) -> List[Path]:
    seen: set[Path] = set()
    files: List[Path] = []

    for pattern in PRIORITY_PATTERNS:
        for path in repo_root.glob(pattern):
            if path.is_file() and path.suffix.lower() == ".md" and not should_skip(path):
                if path not in seen:
                    seen.add(path)
                    files.append(path)

    return files


def run_git_command(repo_root: Path, args: List[str]) -> str | None:
    try:
        result = subprocess.run(
            ["git", *args],
            cwd=repo_root,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None
    return result.stdout.strip()


def get_changed_markdown_files(repo_root: Path, prefix: str) -> List[str]:
    """
    Return repo-relative markdown files under a prefix that changed recently.

    Preference order:
    1. Diff between HEAD~1 and HEAD (good for push-triggered workflow runs)
    2. Uncommitted/new files under that prefix (good for local runs)
    """
    candidates: List[str] = []

    diff_output = run_git_command(repo_root, ["diff", "--name-only", "HEAD~1", "HEAD", "--", prefix])
    if diff_output:
        for line in diff_output.splitlines():
            relpath = line.strip().replace("\\", "/")
            if relpath.startswith(prefix) and relpath.endswith(".md"):
                full_path = repo_root / relpath
                if full_path.is_file() and not should_skip(full_path):
                    candidates.append(relpath)

    status_output = run_git_command(repo_root, ["status", "--porcelain", "--untracked-files=all", "--", prefix])
    if status_output:
        for line in status_output.splitlines():
            if len(line) < 4:
                continue
            relpath = line[3:].strip().replace("\\", "/")
            if relpath.startswith(prefix) and relpath.endswith(".md"):
                full_path = repo_root / relpath
                if full_path.is_file() and not should_skip(full_path):
                    candidates.append(relpath)

    deduped: List[str] = []
    seen: set[str] = set()
    for relpath in candidates:
        if relpath not in seen:
            seen.add(relpath)
            deduped.append(relpath)
    return deduped


def compute_score(relpath: str, meta: Dict[str, Any], body: str, path: Path) -> float:
    score = 0.0

    if relpath.startswith("desired-state/"):
        score += 1000
    elif relpath == "source/book/metaphors.md":
        score += 940
    elif relpath == "source/book/key-quotes.md":
        score += 930
    elif relpath.startswith("source/book/chapter-summaries/"):
        score += 850
    elif relpath.startswith("source/book/"):
        score += 800
    elif relpath.startswith("source/youtube-transcripts/"):
        score += 740
    elif relpath.startswith("source/"):
        score += 700
    elif relpath.startswith("observed/posts/"):
        score += 500

    # Prefer files with more obviously useful metadata.
    for useful_key in ("title", "date_published", "themes", "book_themes", "topics"):
        if useful_key in meta:
            score += 10

    # Mild bonus for substantive content.
    score += min(len(body), 8000) / 8000 * 20

    # Mild bonus for newer files.
    try:
        mtime = path.stat().st_mtime
        age_days = max((utc_now().timestamp() - mtime) / 86400, 0)
        score += max(30 - min(age_days, 30), 0) / 3
    except OSError:
        pass

    return score


def make_excerpt(body: str, max_chars: int = 2600) -> str:
    text = body.strip()
    text = re.sub(r"\n{3,}", "\n\n", text)
    if len(text) <= max_chars:
        return text
    return text[:max_chars].rsplit(" ", 1)[0] + " …"


def load_repo_docs(repo_root: Path) -> List[RepoDoc]:
    docs: List[RepoDoc] = []

    for path in collect_markdown_files(repo_root):
        raw = path.read_text(encoding="utf-8", errors="replace")
        meta, body = parse_frontmatter(raw)
        relpath = str(path.relative_to(repo_root)).replace("\\", "/")
        docs.append(
            RepoDoc(
                path=path,
                relpath=relpath,
                meta=meta,
                body=body,
                excerpt=make_excerpt(body),
                score=compute_score(relpath, meta, body, path),
            )
        )

    docs.sort(key=lambda d: (-d.score, d.relpath))
    return docs


def choose_context_docs(
    docs: List[RepoDoc],
    max_docs: int,
    max_chars: int,
    changed_source_relpaths: List[str] | None = None,
    changed_observed_post_relpaths: List[str] | None = None,
) -> List[RepoDoc]:
    chosen: List[RepoDoc] = []
    total_chars = 0
    changed_source_relpaths = changed_source_relpaths or []
    changed_observed_post_relpaths = changed_observed_post_relpaths or []

    def try_add(doc: RepoDoc) -> bool:
        nonlocal total_chars
        if doc in chosen:
            return False
        if len(chosen) >= max_docs:
            return False
        if total_chars + len(doc.excerpt) > max_chars:
            return False
        chosen.append(doc)
        total_chars += len(doc.excerpt)
        return True

    # Always include desired-state docs first.
    desired = [d for d in docs if d.relpath.startswith("desired-state/")]
    desired.sort(key=lambda d: d.relpath)
    for doc in desired:
        if len(chosen) >= max_docs:
            break
        if not try_add(doc):
            break

    # Force in recently changed source docs so the model can use them as inspiration.
    if changed_source_relpaths:
        lookup = {d.relpath: d for d in docs}
        changed_docs = [lookup[p] for p in changed_source_relpaths if p in lookup]
        changed_docs.sort(key=lambda d: (-d.score, d.relpath))
        for doc in changed_docs:
            if len(chosen) >= max_docs:
                break
            try_add(doc)

    # Force in recently changed observed posts so the model can propose follow-on ideas.
    if changed_observed_post_relpaths:
        lookup = {d.relpath: d for d in docs}
        changed_docs = [lookup[p] for p in changed_observed_post_relpaths if p in lookup]
        changed_docs.sort(key=lambda d: (-d.score, d.relpath))
        for doc in changed_docs:
            if len(chosen) >= max_docs:
                break
            try_add(doc)

    # Then fill with best-scoring remaining docs.
    for doc in docs:
        if len(chosen) >= max_docs:
            break
        try_add(doc)

    return chosen


def render_context(docs: List[RepoDoc]) -> str:
    chunks = []
    for doc in docs:
        chunks.append(
            "\n".join(
                [
                    f"## DOCUMENT: {doc.relpath}",
                    f"META: {json.dumps(doc.meta, ensure_ascii=False)}",
                    "EXCERPT:",
                    doc.excerpt,
                ]
            )
        )
    return "\n\n".join(chunks)


def build_user_prompt(
    repo_root: Path,
    docs: List[RepoDoc],
    count: int,
    changed_source_docs: List[RepoDoc],
    changed_observed_post_docs: List[RepoDoc],
) -> str:
    context = render_context(docs)

    changed_source_section = ""
    if changed_source_docs:
        changed_lines = "\n".join(f"- {doc.relpath}" for doc in changed_source_docs)
        changed_source_section = f"""
Recently changed source docs (treat these as especially strong inspiration if they are relevant):
{changed_lines}

Extra rule for this run:
- At least one candidate should be directly inspired by one or more of the recently changed source docs.
- Mention those changed source docs in source_docs for the relevant candidate(s).
"""

    changed_observed_posts_section = ""
    if changed_observed_post_docs:
        changed_lines = "\n".join(f"- {doc.relpath}" for doc in changed_observed_post_docs)
        changed_observed_posts_section = f"""
Recently changed observed posts (treat these as things that have just gone out or have just been updated):
{changed_lines}

Extra rule for this run:
- At least one candidate should be a sensible follow-on, sequel, adjacent angle, counterpoint, expansion, or next-step post based on one or more of the recently changed observed posts.
- Do not simply repeat those posts.
- Mention the relevant observed post files in source_docs for the follow-on candidate(s).
"""

    return f"""
Repository root: {repo_root}

You are generating candidate posts for a markdown-based marketing control plane.

Requirements:
- Produce exactly {count} candidates.
- Ground them in the supplied documents only.
- Prefer the author's distinctive metaphors, language, and arguments.
- Keep them useful and specific.
- Avoid generic "project management thought leadership".
- Do not fabricate direct quotations unless the wording clearly appears in the supplied excerpts.
- Use source_docs that actually appear in the supplied context.
- Keep at least one candidate clearly transcript- or show-led if transcript/show material appears in the context.
- Keep at least one candidate evergreen.
- Keep any promotional candidate restrained.

Write for these goals if present in the repo:
- increase awareness of the book
- discuss issues from the book in relation to project management, seeing things in different ways, and delivering software

{changed_source_section}
{changed_observed_posts_section}
Output only structured JSON matching the schema.

Here is the repo context:

{context}
""".strip()


def call_openai(user_prompt: str) -> Dict[str, Any]:
    if OpenAI is None:
        raise RuntimeError("openai package is not installed.")
    client = OpenAI()
    response = client.responses.create(
        model=DEFAULT_OPENAI_MODEL,
        input=[
            {
                "role": "system",
                "content": [{"type": "input_text", "text": SYSTEM_PROMPT}],
            },
            {
                "role": "user",
                "content": [{"type": "input_text", "text": user_prompt}],
            },
        ],
        text={
            "format": {
                "type": "json_schema",
                "name": "content_scout_output",
                "schema": JSON_SCHEMA,
                "strict": True,
            },
        },
    )
    if not getattr(response, "output_text", None):
        raise RuntimeError(
            "OpenAI returned no output_text. Check the raw response for refusals or incomplete output."
        )
    try:
        return json.loads(response.output_text)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"OpenAI output was not valid JSON:\n{response.output_text}") from exc


def call_anthropic(user_prompt: str) -> Dict[str, Any]:
    if Anthropic is None:
        raise RuntimeError("anthropic package is not installed.")
    client = Anthropic()
    response = client.messages.create(
        model=DEFAULT_ANTHROPIC_MODEL,
        max_tokens=4096,
        system=SYSTEM_PROMPT,
        tools=[
            {
                "name": "content_scout_output",
                "description": "Output structured post candidates.",
                "input_schema": JSON_SCHEMA,
            }
        ],
        tool_choice={"type": "tool", "name": "content_scout_output"},
        messages=[{"role": "user", "content": user_prompt}],
    )
    tool_use = next((b for b in response.content if b.type == "tool_use"), None)
    if tool_use is None:
        raise RuntimeError("Anthropic returned no tool_use block. Check the raw response.")
    return tool_use.input


def call_model(user_prompt: str) -> tuple[Dict[str, Any], str]:
    has_openai = bool(os.getenv("OPENAI_API_KEY")) and OpenAI is not None
    has_anthropic = bool(os.getenv("ANTHROPIC_API_KEY")) and Anthropic is not None

    if has_openai and has_anthropic:
        provider = random.choice(["openai", "anthropic"])
    elif has_openai:
        provider = "openai"
    elif has_anthropic:
        provider = "anthropic"
    else:
        raise RuntimeError("Neither OPENAI_API_KEY nor ANTHROPIC_API_KEY is set.")

    print(f"  provider selected: {provider}")
    if provider == "openai":
        return call_openai(user_prompt), provider
    else:
        return call_anthropic(user_prompt), provider


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def normalise_candidate(candidate: Dict[str, Any]) -> Dict[str, Any]:
    cleaned = dict(candidate)

    cleaned["working_title"] = compact_whitespace(cleaned["working_title"])
    cleaned["hook"] = cleaned["hook"].strip()
    cleaned["draft"] = cleaned["draft"].strip()
    cleaned["rationale"] = cleaned["rationale"].strip()
    cleaned["why_now"] = cleaned["why_now"].strip()
    cleaned["novelty_note"] = cleaned["novelty_note"].strip()
    cleaned["risk_note"] = cleaned["risk_note"].strip()

    cleaned["metaphors"] = [compact_whitespace(m) for m in cleaned.get("metaphors", []) if str(m).strip()]
    cleaned["source_docs"] = [compact_whitespace(p) for p in cleaned.get("source_docs", []) if str(p).strip()]
    cleaned["source_ideas"] = [compact_whitespace(i) for i in cleaned.get("source_ideas", []) if str(i).strip()]

    if cleaned["channel"] not in ALLOWED_CHANNELS:
        cleaned["channel"] = "linkedin"
    if cleaned["risk"] not in ALLOWED_RISK:
        cleaned["risk"] = "medium"
    if cleaned["cta"] not in ALLOWED_CTA:
        cleaned["cta"] = "soft"
    if cleaned["trigger_type"] not in ALLOWED_TRIGGER_TYPES:
        cleaned["trigger_type"] = "evergreen"

    return cleaned


def write_candidate_markdown(
    repo_root: Path,
    candidate: Dict[str, Any],
    index: int,
    run_ts: str,
) -> Path:
    queue_dir = repo_root / "queue" / "post-candidates"
    ensure_dir(queue_dir)

    date_part = utc_now().strftime("%Y-%m-%d")
    file_slug = slugify(candidate["working_title"])
    filename = f"post-candidate-{date_part}-{index:03d}-{file_slug}.md"
    out_path = queue_dir / filename

    frontmatter = {
        "id": f"post-candidate-{date_part}-{index:03d}",
        "type": "post_candidate",
        "status": "awaiting_approval",
        "channel": candidate["channel"],
        "theme": candidate["theme"],
        "metaphors": candidate["metaphors"],
        "source_docs": candidate["source_docs"],
        "trigger_type": candidate["trigger_type"],
        "risk": candidate["risk"],
        "cta": candidate["cta"],
        "generated_by": "scripts/run_content_scout.py",
        "generated_at": run_ts,
    }

    body = "\n\n".join(
        [
            f"# {candidate['working_title']}",
            "## Hook",
            candidate["hook"],
            "## Rationale",
            candidate["rationale"],
            "## Draft",
            candidate["draft"],
            "## Why now",
            candidate["why_now"],
            "## Supporting ideas",
            "\n".join(f"- {item}" for item in candidate["source_ideas"]) or "-",
            "## Source docs",
            "\n".join(f"- {item}" for item in candidate["source_docs"]) or "-",
            "## Novelty note",
            candidate["novelty_note"],
            "## Risk note",
            candidate["risk_note"],
            "## Reviewer notes",
            "- ",
        ]
    )

    out_path.write_text(
        dump_frontmatter(frontmatter) + "\n\n" + body + "\n",
        encoding="utf-8",
    )
    return out_path


def write_log_markdown(
    repo_root: Path,
    provider: str,
    chosen_docs: List[RepoDoc],
    changed_source_docs: List[RepoDoc],
    changed_observed_post_docs: List[RepoDoc],
    result: Dict[str, Any],
    written_files: List[Path],
    run_ts: str,
) -> Path:
    log_dir = repo_root / "agent-logs" / "content-scout"
    ensure_dir(log_dir)

    filename = f"content-scout-{run_ts.replace(':', '').replace('-', '')}.md"
    out_path = log_dir / filename

    frontmatter = {
        "id": f"content-scout-{run_ts}",
        "type": "agent_log",
        "agent": "content_scout",
        "status": "completed",
        "provider": provider,
        "generated_at": run_ts,
    }

    body_parts = [
        "# Summary",
        result.get("run_summary", "").strip() or "No summary provided.",
        "## Changed source docs used as inspiration",
        "\n".join(f"- {doc.relpath}" for doc in changed_source_docs) or "-",
        "## Changed observed posts used for follow-on suggestions",
        "\n".join(f"- {doc.relpath}" for doc in changed_observed_post_docs) or "-",
        "## Documents chosen for context",
        "\n".join(f"- {doc.relpath}" for doc in chosen_docs) or "-",
        "## Documents reported as used by model",
        "\n".join(f"- {path}" for path in result.get("documents_used", [])) or "-",
        "## Candidate files written",
        "\n".join(f"- {str(path.relative_to(repo_root)).replace(chr(92), '/')}" for path in written_files) or "-",
        "## Candidate working titles",
        "\n".join(f"- {c.get('working_title', '').strip()}" for c in result.get("candidates", [])) or "-",
    ]

    out_path.write_text(
        dump_frontmatter(frontmatter) + "\n\n" + "\n\n".join(body_parts) + "\n",
        encoding="utf-8",
    )
    return out_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate grounded post candidates from repo markdown.")
    parser.add_argument("--repo-root", default=".", help="Path to the repo root.")
    parser.add_argument("--count", type=int, default=3, help="Number of candidates to ask for.")
    parser.add_argument("--max-docs", type=int, default=14, help="Maximum number of repo docs to include in context.")
    parser.add_argument("--max-context-chars", type=int, default=28000, help="Approximate character budget for context excerpts.")
    parser.add_argument("--dry-run", action="store_true", help="Print results instead of writing files.")
    parser.add_argument(
        "--ignore-recent-source-changes",
        action="store_true",
        help="Do not prioritize recently changed markdown files under source/.",
    )
    parser.add_argument(
        "--ignore-recent-observed-post-changes",
        action="store_true",
        help="Do not prioritize recently changed markdown files under observed/posts/.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    if not os.getenv("OPENAI_API_KEY") and not os.getenv("ANTHROPIC_API_KEY"):
        print("Neither OPENAI_API_KEY nor ANTHROPIC_API_KEY is set.", file=sys.stderr)
        return 2

    repo_root = Path(args.repo_root).resolve()
    if not repo_root.exists():
        print(f"Repo root does not exist: {repo_root}", file=sys.stderr)
        return 2

    docs = load_repo_docs(repo_root)
    if not docs:
        print("No markdown files found to build context.", file=sys.stderr)
        return 1

    changed_source_relpaths: List[str] = []
    if not args.ignore_recent_source_changes:
        changed_source_relpaths = get_changed_markdown_files(repo_root, "source/")

    changed_observed_post_relpaths: List[str] = []
    if not args.ignore_recent_observed_post_changes:
        changed_observed_post_relpaths = get_changed_markdown_files(repo_root, "observed/posts/")

    doc_lookup = {doc.relpath: doc for doc in docs}
    changed_source_docs = [doc_lookup[p] for p in changed_source_relpaths if p in doc_lookup]
    changed_observed_post_docs = [doc_lookup[p] for p in changed_observed_post_relpaths if p in doc_lookup]

    chosen_docs = choose_context_docs(
        docs=docs,
        max_docs=args.max_docs,
        max_chars=args.max_context_chars,
        changed_source_relpaths=changed_source_relpaths,
        changed_observed_post_relpaths=changed_observed_post_relpaths,
    )

    user_prompt = build_user_prompt(
        repo_root,
        chosen_docs,
        args.count,
        changed_source_docs,
        changed_observed_post_docs,
    )
    result, provider = call_model(user_prompt)

    candidates = [normalise_candidate(c) for c in result.get("candidates", [])]
    if not candidates:
        print("Model returned no candidates.", file=sys.stderr)
        return 1

    run_ts = utc_now().replace(microsecond=0).isoformat().replace("+00:00", "Z")

    if args.dry_run:
        dry_run_output = {
            "recently_changed_source_docs": changed_source_relpaths,
            "recently_changed_observed_posts": changed_observed_post_relpaths,
            "model_output": result,
        }
        print(json.dumps(dry_run_output, indent=2, ensure_ascii=False))
        return 0

    written_files: List[Path] = []
    for idx, candidate in enumerate(candidates, start=1):
        written = write_candidate_markdown(repo_root, candidate, idx, run_ts)
        written_files.append(written)

    log_path = write_log_markdown(
        repo_root=repo_root,
        provider=provider,
        chosen_docs=chosen_docs,
        changed_source_docs=changed_source_docs,
        changed_observed_post_docs=changed_observed_post_docs,
        result=result,
        written_files=written_files,
        run_ts=run_ts,
    )

    print("Content scout completed.")
    if changed_source_relpaths:
        print("  recently changed source docs:")
        for relpath in changed_source_relpaths:
            print(f"    - {relpath}")
    if changed_observed_post_relpaths:
        print("  recently changed observed posts:")
        for relpath in changed_observed_post_relpaths:
            print(f"    - {relpath}")
    for path in written_files:
        print(f"  wrote candidate: {path}")
    print(f"  wrote log:       {log_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
