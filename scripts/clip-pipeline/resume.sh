#!/bin/bash
# Resume the You Can Write a Book clip pipeline.
# Idempotent: verifies what exists, then only does the work still missing.
set -u
P=/home/mark/projects/MarketingControlPlane/scripts/clip-pipeline
V=/home/mark/projects/MarketingControlPlane/.venv/bin/python
L=$P/logs; mkdir -p "$L"
mkdir -p /home/mark/projects/MarketingControlPlane/source/show/assets/clips/shorts

echo "== verifying existing output =="
python3 $P/verify.py

echo "== captions =="
$V $P/make_srt.py   >> "$L/srt.log" 2>&1
python3 $P/fix_srt.py > "$L/fix.log" 2>&1
python3 $P/make_ass.py > "$L/ass.log" 2>&1

echo "== 4:5 renders ==";        $V $P/render_clips.py  >> "$L/render.log" 2>&1
echo "== 4:5 subtitle burns =="; $V $P/burn_subs.py     >> "$L/burn.log" 2>&1
echo "== shorts renders ==";     $V $P/render_shorts.py >> "$L/render_shorts.log" 2>&1
echo "== shorts burns ==";       $V $P/burn_shorts.py   >> "$L/burn_shorts.log" 2>&1

python3 $P/verify.py
echo "== ALL DONE =="
