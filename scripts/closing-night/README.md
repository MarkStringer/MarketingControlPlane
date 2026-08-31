# Closing-night pipeline — 29 August 2026

Cuts 17 passages out of the two recordings from the last night of the Fringe 2026 run and
renders each one in two aspect ratios, with and without burned-in captions.

    .venv/bin/python scripts/closing-night/make_clips.py            # everything
    .venv/bin/python scripts/closing-night/make_clips.py the-empty-room   # one clip

Safe to re-run. Every stage checks its output against the expected duration and skips
anything already done, so a second run with nothing to do is a no-op. To redo a clip, delete
its files and run again.

## Source

Two portrait phone recordings, in `~/Downloads/` and not in the repo:

| Key | File | Length | What |
|---|---|---|---|
| A | `20260829_182537.mp4` | 48m 37s | The show, performed to an empty room |
| B | `20260829_191832.mp4` | 1m 43s | Piece to camera on the street afterwards |

Both carry `rotation=90` side data, so ffmpeg decodes them as 1080x1920 portrait. That makes
9:16 the native frame.

## Stages

| Stage | Does |
|---|---|
| cut | Denoises and cuts each passage to 1080x1920 |
| captions | Transcribes each clip with word-level timing, corrects it, writes `source/show/clip-captions-2026-08-29/` |
| ass | Builds `.ass` caption files at 9:16 and 4:5 |
| renders | Burns captions in, and builds the 4:5 versions |

## Output

`source/show/assets/clips-2026-08-29/`, gitignored:

    clip-NN-slug.mp4                 1080x1920, no captions
    clip-NN-slug-subtitled.mp4       1080x1920, captions raised clear of the Shorts UI
    4x5/clip-NN-slug.mp4             1080x1350, no captions
    4x5/clip-NN-slug-subtitled.mp4   1080x1350, captions

## Why the 4:5 is not a crop

The source is a phone held close and the face fills the frame top to bottom. A centre crop to
1080x1350 loses either the top of the head or the chin. The 4:5 renders therefore fit the
whole portrait frame inside the 4:5 canvas over a blurred, zoomed copy of itself, so nothing
is lost and the sides are filled.

## Denoising

The venue was dark and the phone was at high ISO, so the raw footage is grainy enough that
h264 spends most of its bitrate encoding noise. `hqdn3d=6:4:8:6` at the cut stage cuts the
file sizes by roughly two thirds and looks cleaner. It is applied once, to the master, so
every derived render inherits it.

The stage lighting is strongly magenta and has been left alone. Grading it out is a
judgement call rather than a fix, and it is what the room looked like.

## Captions

`corrections.py` holds the correction table, shared with `fix_transcript.py`. Corrections are
applied to a whole clip at once and then mapped back onto the cue boundaries, so a phrase that
straddles two captions still matches. Add to `CORRECTIONS` there rather than editing the
`.srt` files by hand, or the next run will overwrite the edit.

## Clip list

The `CLIPS` table in `make_clips.py` is the only copy of the in and out points. The prose
about what each clip is and why it was picked lives in
`source/show/clip-candidates-2026-08-29.md`.
