#!/bin/bash
set -euo pipefail

# SessionStart hook: rebuild the deterministic knowledge graph so graph/nodes.ndjson
# and graph/edges.ndjson reflect the current repository at the start of each session.
# The builder is pure-stdlib Python and runs in well under a second.

# Only run in the remote (Claude Code on the web) environment. Locally, a fresh
# rebuild would show up as an uncommitted change; the repo already has
# scripts/watch-and-rebuild-graph.sh for local use. Remove this guard to also
# rebuild on local session start.
if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

cd "${CLAUDE_PROJECT_DIR:-.}"

python3 scripts/build_markdown_graph.py --repo-root . --out-dir graph
