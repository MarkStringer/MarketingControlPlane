#!/bin/bash
# Resume the closing-night clip pipeline (29 August 2026 recordings).
#
# Safe to run at any time, as often as you like. It throws away anything that
# was half written when the machine went down, then does only the work still
# missing. A run with nothing left to do prints the totals and exits.
set -u
R=/home/mark/projects/MarketingControlPlane
P=$R/scripts/closing-night
V=$R/.venv/bin/python

if [ ! -f "$HOME/Downloads/20260829_182537.mp4" ]; then
  echo "Source recording missing: ~/Downloads/20260829_182537.mp4"
  echo "The clips cannot be rebuilt without it."
  exit 1
fi

echo "== before =="
$V $P/make_clips.py --status

$V $P/make_clips.py "$@" 2>&1 | tee -a $P/run.log

echo "== after =="
$V $P/make_clips.py --status
