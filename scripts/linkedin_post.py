#!/usr/bin/env python3
"""
linkedin_post.py

Post a post candidate to LinkedIn.

Usage:
    python3 scripts/linkedin_post.py <path-to-post-candidate.md>

What it does:
    1. Extracts the Draft section from the post candidate
    2. Shows it for confirmation
    3. Posts to LinkedIn
    4. Updates the post candidate status to 'published'
    5. Creates an observed/posts entry
"""

import json
import re
import sys
import urllib.parse
import urllib.request
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
DOTENV = REPO_ROOT / ".env"
OBSERVED_POSTS = REPO_ROOT / "observed" / "posts"
LINKEDIN_POSTS_URL = "https://api.linkedin.com/rest/posts"


def load_env():
    env = {}
    if DOTENV.exists():
        for line in DOTENV.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                env[k.strip()] = v.strip()
    return env


def parse_frontmatter(text):
    """Return (frontmatter_dict, body) from a markdown file with --- frontmatter."""
    if not text.startswith("---"):
        return {}, text
    end = text.index("---", 3)
    fm_text = text[3:end].strip()
    body = text[end + 3:].strip()
    # Simple key: value parser (handles lists with - items)
    fm = {}
    current_key = None
    for line in fm_text.splitlines():
        if re.match(r"^\w[\w_-]*\s*:", line):
            current_key, _, val = line.partition(":")
            current_key = current_key.strip()
            val = val.strip()
            if val:
                fm[current_key] = val.strip('"').strip("'")
            else:
                fm[current_key] = []
        elif line.strip().startswith("- ") and isinstance(fm.get(current_key), list):
            fm[current_key].append(line.strip()[2:].strip())
    return fm, body


def extract_draft(body):
    """Extract the text between # Draft and the next # heading."""
    match = re.search(r"^# Draft\s*\n(.*?)(?=^# |\Z)", body, re.MULTILINE | re.DOTALL)
    if not match:
        return None
    draft_block = match.group(1).strip()
    # Strip surrounding --- fences if present
    draft_block = re.sub(r"^---\s*\n", "", draft_block)
    draft_block = re.sub(r"\n---\s*$", "", draft_block)
    return draft_block.strip()


def update_frontmatter_status(path, new_status):
    text = path.read_text()
    updated = re.sub(
        r"^(status:\s*).*$",
        lambda m: m.group(1) + new_status,
        text,
        count=1,
        flags=re.MULTILINE,
    )
    path.write_text(updated)


def slug_from_path(path):
    """e.g. post-candidate-2026-03-28-001-you-are-not-paul-mccartney -> you-are-not-paul-mccartney"""
    name = path.stem
    # Strip leading post-candidate-YYYY-MM-DD-NNN- prefix
    name = re.sub(r"^post-candidate-\d{4}-\d{2}-\d{2}-\d+-", "", name)
    return name


def create_observed_post(candidate_path, fm, draft_text, linkedin_post_id):
    today = date.today().isoformat()
    slug = slug_from_path(candidate_path)
    filename = f"{today}-{slug}.md"
    out_path = OBSERVED_POSTS / filename

    # Build title from slug
    title = slug.replace("-", " ").title()

    source_docs = fm.get("source_docs", [])
    if isinstance(source_docs, str):
        source_docs = [source_docs]
    source_docs_yaml = "\n".join(f"  - {s}" for s in source_docs) if source_docs else ""

    content = f"""---
id: "{today}-{slug}"
type: "source_post"
title: "{title}"
date_published: "{today}"
channel: "linkedin"
linkedin_post_id: "{linkedin_post_id}"
status: "published"
source_docs:
{source_docs_yaml}
metrics:
  date_checked: null
  impressions: null
  likes: null
  comments: null
  shares: null
  clicks: null
  notes: ""
---

{draft_text}
"""
    out_path.write_text(content)
    return out_path


def post_to_linkedin(token, person_urn, text):
    # Ensure URN is fully qualified
    if not person_urn.startswith("urn:li:person:"):
        person_urn = f"urn:li:person:{person_urn}"

    payload = {
        "author": person_urn,
        "commentary": text,
        "visibility": "PUBLIC",
        "distribution": {
            "feedDistribution": "MAIN_FEED",
            "targetEntities": [],
            "thirdPartyDistributionChannels": [],
        },
        "lifecycleState": "PUBLISHED",
        "isReshareDisabledByAuthor": False,
    }

    data = json.dumps(payload).encode()
    req = urllib.request.Request(LINKEDIN_POSTS_URL, data=data, method="POST")
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Content-Type", "application/json")
    req.add_header("X-Restli-Protocol-Version", "2.0.0")
    req.add_header("LinkedIn-Version", "202501")

    try:
        with urllib.request.urlopen(req) as resp:
            post_id = resp.headers.get("x-restli-id", "")
            return post_id
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        raise RuntimeError(f"LinkedIn API error {e.code}: {body}")


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 scripts/linkedin_post.py <path-to-post-candidate.md>")
        sys.exit(1)

    candidate_path = Path(sys.argv[1])
    if not candidate_path.exists():
        print(f"ERROR: file not found: {candidate_path}")
        sys.exit(1)

    env = load_env()
    token = env.get("LINKEDIN_ACCESS_TOKEN")
    person_urn = env.get("LINKEDIN_PERSON_URN")

    if not token:
        print("ERROR: LINKEDIN_ACCESS_TOKEN not set in .env — run scripts/linkedin_auth.py first")
        sys.exit(1)
    if not person_urn:
        print("ERROR: LINKEDIN_PERSON_URN not set in .env — run scripts/linkedin_auth.py first")
        sys.exit(1)

    text = candidate_path.read_text()
    fm, body = parse_frontmatter(text)

    if fm.get("status") == "published":
        print(f"WARNING: this post candidate is already marked as published.")
        confirm = input("Post again anyway? [y/N] ").strip().lower()
        if confirm != "y":
            sys.exit(0)

    draft = extract_draft(body)
    if not draft:
        print("ERROR: could not find a # Draft section in the post candidate")
        sys.exit(1)

    print("\n" + "=" * 60)
    print("DRAFT TO POST:")
    print("=" * 60)
    print(draft)
    print("=" * 60)
    print(f"\nCharacters: {len(draft)} / 3000")

    if len(draft) > 3000:
        print("ERROR: post exceeds LinkedIn's 3000 character limit")
        sys.exit(1)

    confirm = input("\nPost this to LinkedIn? [y/N] ").strip().lower()
    if confirm != "y":
        print("Aborted.")
        sys.exit(0)

    print("\nPosting to LinkedIn...")
    post_id = post_to_linkedin(token, person_urn, draft)
    print(f"Posted. LinkedIn post ID: {post_id}")

    update_frontmatter_status(candidate_path, "published")
    print(f"Updated {candidate_path.name} status → published")

    observed_path = create_observed_post(candidate_path, fm, draft, post_id)
    print(f"Created observed post: {observed_path.relative_to(REPO_ROOT)}")

    print("\nDone.")


if __name__ == "__main__":
    main()
