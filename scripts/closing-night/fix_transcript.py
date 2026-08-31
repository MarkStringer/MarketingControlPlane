# -*- coding: utf-8 -*-
"""Rewrite the two 2026-08-29 transcripts from the raw JSON, corrected."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from corrections import fix_segments, FACTUAL_NOTES

WORK = ("/tmp/claude-1000/-home-mark-projects-MarketingControlPlane/"
        "2508c676-726b-41c9-a22b-f40cbf8f44a2/scratchpad")
DST  = "/home/mark/projects/MarketingControlPlane/source/show"

def paragraphs(segs, width):
    out, buf, start = [], [], None
    for r in segs:
        if start is None:
            start = r["s"]
        buf.append(r["t"])
        if sum(len(x) for x in buf) > width:
            out.append((start, " ".join(buf))); buf, start = [], None
    if buf:
        out.append((start, " ".join(buf)))
    return out

SHOW_HEAD = """---
title: You Can Write a Book — live transcript, 2026-08-29 (no audience)
source: ~/Downloads/20260829_182537.mp4 (48m 37s, 1080x1920 portrait, Edinburgh Fringe 2026)
transcribed_by: faster-whisper distil-large-v3, 2026-08-31
corrected_by: scripts/closing-night/fix_transcript.py, 2026-08-31
accuracy_note: Mishearings corrected against scripts/closing-night/corrections.py. Speech is
  otherwise as spoken, including the repetitions and the filler. Safe to quote, but listen
  back before putting a sentence in someone else's mouth.
---

> Twelfth and final show of the run. Nobody came. Mark performed the whole show to an empty
> room and recorded it on a phone held close, skipping the audience writing breaks and taking
> the S cards in the order they came out rather than having the audience pick them. He heckles
> himself at the end, reading out the heckle cards he normally hands to the audience.
>
> Left as spoken, because they are his errors rather than the transcriber's:
>
%s

"""

PTC_HEAD = """---
title: Piece to camera after the final show, 2026-08-29
source: ~/Downloads/20260829_191832.mp4 (1m 43s, 1080x1920 portrait, shot outdoors)
transcribed_by: faster-whisper distil-large-v3, 2026-08-31
corrected_by: scripts/closing-night/fix_transcript.py, 2026-08-31
accuracy_note: Mishearings corrected against scripts/closing-night/corrections.py.
---

> Recorded at 19:18, four minutes after the final show of the run came down. Nobody had come,
> and Mark performed the whole show to the empty room anyway. This is him talking about that
> straight to camera on the street. He says at the end that he wants it to be a short, so it
> can go out close to as-is.
>
> The aside about where the word theatre comes from is indistinct on the recording and the
> transcription of it is a guess.

"""

for src, dst, head, width in [
    ("show.json",  "show-transcript-2026-08-29.md", SHOW_HEAD, 320),
    ("short.json", "show-transcript-2026-08-29-piece-to-camera.md", PTC_HEAD, 260),
]:
    segs = fix_segments(json.load(open(os.path.join(WORK, src))))
    body = "\n".join("[%02d:%02d] %s" % (s // 60, s % 60, t)
                     for s, t in paragraphs(segs, width))
    notes = "\n".join("> - " + n for n in FACTUAL_NOTES)
    with open(os.path.join(DST, dst), "w") as f:
        f.write((head % notes if "%s" in head else head) + body + "\n")
    print("wrote", dst, len(segs), "segments")
