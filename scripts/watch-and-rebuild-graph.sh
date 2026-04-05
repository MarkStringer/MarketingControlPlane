#!/usr/bin/env bash
# watch-and-rebuild-graph.sh
#
# Watches all .md files in the repo. When a change is detected, waits 30
# minutes (debounced — resets on each new change) then rebuilds the graph.
#
# Requires: inotify-tools (sudo apt-get install -y inotify-tools)
#
# Add to crontab:
#   @reboot sleep 120 && /home/mark/projects/MarketingControlPlane/scripts/watch-and-rebuild-graph.sh

set -euo pipefail

REPO="$(cd "$(dirname "$0")/.." && pwd)"
SCRIPT="$REPO/scripts/build_markdown_graph.py"
LOG="$REPO/agent-logs/graph-watcher.log"
PIDFILE="/tmp/mcp-graph-rebuild-timer.pid"
DELAY=1800  # 30 minutes

mkdir -p "$(dirname "$LOG")"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" >> "$LOG"
}

run_build() {
    log "Rebuilding graph..."
    cd "$REPO" && python3 "$SCRIPT" --repo-root . >> "$LOG" 2>&1
    log "Graph rebuild complete."
    rm -f "$PIDFILE"
}

cancel_timer() {
    if [ -f "$PIDFILE" ]; then
        old_pid=$(cat "$PIDFILE")
        # Kill the sleep subprocess group
        kill -- -"$old_pid" 2>/dev/null || kill "$old_pid" 2>/dev/null || true
        rm -f "$PIDFILE"
    fi
}

log "Graph watcher started. Watching $REPO for .md changes."

inotifywait -m -r \
    -e modify,create,delete,move \
    --include '\.md$' \
    --exclude '(\.git|graph/)' \
    "$REPO" 2>/dev/null \
| while read -r _dir _event _file; do
    cancel_timer

    # Start new 30-min debounce timer in its own process group
    (
        set -m
        sleep $DELAY
        run_build
    ) &
    timer_pid=$!
    echo "$timer_pid" > "$PIDFILE"
    log "Change detected ($_dir$_file) — will rebuild in 30 min (timer pid $timer_pid)"
done
