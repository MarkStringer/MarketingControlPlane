#!/usr/bin/env bash
# run-reply-scout.sh — run the reply scout as a local Claude Code agent
# Searches LinkedIn for posts Mark can reply to, drafts candidates, commits and pushes.
# Records last-run date in .agent-state/reply-scout.last-run

set -euo pipefail

REPO="$(cd "$(dirname "$0")/.." && pwd)"
STATE_FILE="$REPO/.agent-state/reply-scout.last-run"
TODAY=$(date +%Y-%m-%d)

# ── Environment ──────────────────────────────────────────────────────────────
export PATH="/home/mark/.local/bin:/usr/local/bin:/usr/bin:/bin:$PATH"

if [ -f "$HOME/.env.secrets" ]; then
  set -a
  # shellcheck disable=SC1090
  source "$HOME/.env.secrets"
  set +a
fi

mkdir -p "$REPO/agent-logs/reply-scout" "$(dirname "$STATE_FILE")" "$REPO/scripts/logs"
LOG="$REPO/scripts/logs/reply-scout-$TODAY.log"

# ── Prompt ────────────────────────────────────────────────────────────────────
PROMPT="Today is $TODAY. You are the Reply Scout agent for this MarketingControlPlane repo.

Your task — work through these steps in order:

1. Search the web for recent LinkedIn posts about project management.
   Use the query: site:linkedin.com/posts \"project management\"
   Try both WebSearch and fetching the URL:
   https://www.google.com/search?q=site%3Alinkedin.com%2Fposts+%22project+management%22&tbs=qdr:d

2. Read observed/replies/ to see what Mark has replied to recently — do not repeat those themes.

3. Evaluate each post you find. Select 2–4 where Mark has something genuinely
   non-obvious to add, grounded in his book themes.
   REJECT: list posts, glossary posts, corporate promotional content, posts where
   the only reply would be agreement or generic commentary.
   SELECT: posts with a specific claim or argument where Mark can add a structural
   observation, a reframe, or a counterpoint from the book.

4. For each selected post, draft a reply in Mark's voice.
   Voice rules: direct, sometimes dry, no hashtags, no em-dashes, no bullet points
   unless genuinely needed, ends with a point not a question.
   Signature phrases (use when natural, not forced):
   \"bad news is data\", \"all projects are swamps\", \"the project is a bet\",
   \"point of view is worth 80 IQ points\", \"deliver the possible not the fantasy\"

5. Write each reply candidate to queue/reply-candidates/ using the template at
   queue/reply-candidates/template-reply-candidate.md.
   Name files: reply-candidate-$TODAY-NNN-<slug>.md

6. Write a run log to agent-logs/reply-scout/reply-scout-log-$TODAY.md
   using the template at agent-logs/reply-scout/template-reply-scout-log.md.
   The log must list every post considered, with SELECTED or REJECTED and a one-line reason.

7. Follow the CLAUDE.md git workflow exactly:
   - git checkout main
   - Stage only the files you created
   - Commit with a short message
   - git push -u origin main"

# ── Run ───────────────────────────────────────────────────────────────────────
echo "[reply-scout] Starting at $(date)" | tee "$LOG"
cd "$REPO"

claude --dangerously-skip-permissions -p "$PROMPT" 2>&1 | tee -a "$LOG"

echo "$TODAY" > "$STATE_FILE"
echo "[reply-scout] Done at $(date)" | tee -a "$LOG"
