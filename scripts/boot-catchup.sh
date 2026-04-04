#!/usr/bin/env bash
# boot-catchup.sh — run agents that missed their scheduled slot because the laptop was off.
#
# Called by cron @reboot (with a short sleep to let networking settle).
# For each agent: if today is a scheduled day, the scheduled time has passed,
# and the agent hasn't run today → run it now in the background.

REPO="$(cd "$(dirname "$0")/.." && pwd)"
TODAY=$(date +%Y-%m-%d)
DOW=$(date +%u)          # 1=Mon … 7=Sun
NOW_MINS=$(( 10#$(date +%H) * 60 + 10#$(date +%M) ))

CATCHUP_LOG="$REPO/scripts/logs/boot-catchup-$TODAY.log"
mkdir -p "$(dirname "$CATCHUP_LOG")"

log() { echo "[boot-catchup $(date +%H:%M)] $*" | tee -a "$CATCHUP_LOG"; }

log "Boot catchup starting. DOW=$DOW NOW=${NOW_MINS}min"

# run_if_needed NAME SCRIPT SCHED_MINS SCHED_DAYS
#   SCHED_MINS  — scheduled time in minutes since midnight (e.g. 540 = 09:00)
#   SCHED_DAYS  — space-separated list of dow values (1=Mon … 5=Fri)
run_if_needed() {
  local name=$1
  local script=$2
  local sched_mins=$3
  local sched_days=$4

  local state="$REPO/.agent-state/${name}.last-run"
  local last
  last=$(cat "$state" 2>/dev/null || echo "")

  if [ "$last" = "$TODAY" ]; then
    log "$name: already ran today — skipping"
    return 0
  fi

  # Is today a scheduled day?
  if ! echo "$sched_days" | grep -qw "$DOW"; then
    log "$name: not scheduled today (DOW=$DOW, scheduled on: $sched_days) — skipping"
    return 0
  fi

  # Has the scheduled time passed?
  local sched_h=$(( sched_mins / 60 ))
  local sched_m=$(( sched_mins % 60 ))
  if [ "$NOW_MINS" -lt "$sched_mins" ]; then
    log "$name: scheduled at $(printf '%02d:%02d' $sched_h $sched_m) but it's only $(date +%H:%M) — skipping (cron will handle it)"
    return 0
  fi

  log "$name: missed slot at $(printf '%02d:%02d' $sched_h $sched_m) — starting now"
  bash "$script" >> "$CATCHUP_LOG" 2>&1 &
}

# ── Schedule ──────────────────────────────────────────────────────────────────
# content-scout: Mon(1) and Thu(4) at 09:00
run_if_needed "content-scout" "$REPO/scripts/run-content-scout.sh" 540 "1 4"

# reply-scout: Mon–Fri at 09:00
run_if_needed "reply-scout" "$REPO/scripts/run-reply-scout.sh" 540 "1 2 3 4 5"

log "Boot catchup: all checks done. Background jobs may still be running."
