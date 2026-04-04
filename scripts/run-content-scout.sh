#!/usr/bin/env bash
# run-content-scout.sh — run the content scout Python agent locally
# Writes candidates to queue/post-candidates/, logs to agent-logs/content-scout/
# Records last-run date in .agent-state/content-scout.last-run
# Commits and pushes all new files.

set -euo pipefail

REPO="$(cd "$(dirname "$0")/.." && pwd)"
STATE_FILE="$REPO/.agent-state/content-scout.last-run"
TODAY=$(date +%Y-%m-%d)

# ── Environment ──────────────────────────────────────────────────────────────
export PATH="/home/mark/.local/bin:/usr/local/bin:/usr/bin:/bin:$PATH"

# Load project .env (LinkedIn keys etc.)
if [ -f "$REPO/.env" ]; then
  set -a
  # shellcheck disable=SC1090
  source "$REPO/.env"
  set +a
fi

# Load API keys from ~/.env.secrets if present
# Create this file with: ANTHROPIC_API_KEY=sk-... and/or OPENAI_API_KEY=sk-...
if [ -f "$HOME/.env.secrets" ]; then
  set -a
  # shellcheck disable=SC1090
  source "$HOME/.env.secrets"
  set +a
fi

if [ -z "${ANTHROPIC_API_KEY:-}" ] && [ -z "${OPENAI_API_KEY:-}" ]; then
  echo "[content-scout] ERROR: Neither ANTHROPIC_API_KEY nor OPENAI_API_KEY is set." >&2
  echo "  Add them to ~/.env.secrets — see scripts/README-local-agents.md" >&2
  exit 1
fi

# ── Run ───────────────────────────────────────────────────────────────────────
mkdir -p "$REPO/agent-logs/content-scout" "$(dirname "$STATE_FILE")"
LOG="$REPO/scripts/logs/content-scout-$TODAY.log"

echo "[content-scout] Starting at $(date)" | tee "$LOG"
cd "$REPO"

python3 scripts/run_content_scout.py --repo-root . 2>&1 | tee -a "$LOG"

# ── Git ───────────────────────────────────────────────────────────────────────
git checkout main
git add agent-logs/content-scout/ queue/post-candidates/

if git diff --cached --quiet; then
  echo "[content-scout] Nothing new to commit." | tee -a "$LOG"
else
  git commit -m "Content scout: $TODAY"
  git push -u origin main
  echo "[content-scout] Committed and pushed." | tee -a "$LOG"
fi

echo "$TODAY" > "$STATE_FILE"
echo "[content-scout] Done at $(date)" | tee -a "$LOG"
