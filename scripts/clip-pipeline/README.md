# Clip pipeline — You Can Write a Book (Fringe 2026)

Cuts 15 passages out of the live show recordings and renders each one as a slideshow
video with burned-in captions, in two aspect ratios.

## Resume

    scripts/clip-pipeline/resume.sh

Safe to run repeatedly. It verifies every existing file against its expected duration,
deletes anything truncated, and then skips every stage that is already complete. A run
with nothing to do is a no-op.

## Stages

| Script | Does |
|---|---|
| `make_srt.py` | Cuts each clip's audio and transcribes it with word-level timing to `srt-raw/` |
| `fix_srt.py` | Corrects the machine transcript and writes `source/show/clip-captions/` |
| `render_clips.py` | Renders 1080x1350 (4:5, LinkedIn) to `source/show/assets/clips/` |
| `burn_subs.py` | Burns captions into the 4:5 videos |
| `render_shorts.py` | Renders 1080x1920 (9:16, YouTube Shorts) to `clips/shorts/` |
| `burn_shorts.py` | Burns captions into the Shorts, raised clear of the YouTube UI |
| `verify.py` | Deletes any rendered file whose duration is wrong |
| `prepare_images.py` | Rebuilds `assets/` from the flyers, photos and cover PDF |

## Clip list

Clip in/out points live in the `CLIPS` table, repeated in `make_srt.py`,
`render_clips.py`, `render_shorts.py` and `verify.py`. Change a clip's timing in all
four, delete its outputs, and re-run `resume.sh`.

Source audio is in `~/Downloads/` and is not part of the repo:

- `Voice 260822_181740.m4a`
- `Voice 260824_181409.m4a`
- `Voice 260825_182031.m4a`

## Images

`assets/` is not committed — rebuild it with:

    python3 scripts/clip-pipeline/prepare_images.py

`assets/img/` holds the 4:5 source images; `assets/img9x16/` holds the same seven
images pre-composited onto the 1080x1920 canvas, so the Shorts render does no
per-frame scaling. Each clip cycles through all seven in this order:

flyer front, on stage, flyer back, colour headshot, book front, b&w headshot, book back.

The book front and back were split out of `~/projects/DTI/coverStuff/` -
`979-8-8688-2204-9_Stringer_Approved Cover.pdf`, which is a single-page wrap.

## Captions

`fix_srt.py` corrects the raw transcript at document level, not per caption, so that
phrases straddling a caption boundary still match. It then re-aligns the corrected
words onto the original timings, and splits any caption too long for two lines.

The corrections are known Whisper mishearings, and the table will need adding to if
the clip list changes. Captions have not been checked against the audio by ear.

## Dependencies

`faster-whisper` in the repo `.venv`, plus `ffmpeg` and `ffprobe`.
