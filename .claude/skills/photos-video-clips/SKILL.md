---
name: photos-video-clips
description: Check Google Photos for new videos, download them, transcribe them, and propose 60-90 second clips. Use when Mark asks to check Google Photos for new videos, or invokes /photos-video-clips.
---

# photos-video-clips

Checks https://photos.google.com/ for videos not yet processed, downloads them, transcribes them,
and selects 60-90 second clips. It stops at *proposed* clips plus cut files. It never posts anything.

## Why the browser

Google Photos has no usable API for reading a personal library (the Library API stopped
returning user-created content in 2025). Use Claude in Chrome, which has Mark's signed-in
session. Invoke the `claude-in-chrome` skill first and follow it (load tools in one ToolSearch
call, start with `tabs_context_mcp`, open a new tab, never reuse old tab IDs).

If Google shows a sign-in or verification page, stop and tell Mark. Do not enter credentials.

## State

All state lives in `source/photos-videos/` (create it if missing):

| Path | Purpose |
|---|---|
| `seen.json` | `{"start_date": "YYYY-MM-DD", "videos": {"<capture-timestamp>": {"photo_id": "...", "first_seen": "YYYY-MM-DD", "status": "downloaded|transcribed|clipped|skipped|not-relevant", "file": "..."}}}` |
| `raw/` | Downloaded videos (gitignored, large) |
| `transcripts/<id>.json` / `.txt` | Whisper output (committed) |
| `clips/<id>/` | Cut clips (gitignored) |
| `clip-candidates/<id>.md` | Proposed clips with timestamps, reason, and transcript text (committed) |

Make sure `source/photos-videos/raw/` and `source/photos-videos/clips/` are in `.gitignore`.
A video is keyed by its capture timestamp from the item's aria-label (`Video – Portrait – 18 Oct 2026,
11:48:24` becomes `2026-10-18T11:48:24`), because the tool output redacts some photo IDs. Also store
the `photo_id` (the ID in its `https://photos.google.com/photo/<ID>` URL) when it is readable.

`start_date` is the cutoff: only videos captured **after** that date (from the next day, 00:00)
are ever considered new. Older videos are ignored without being listed in `videos`.

## Steps

### 1. Find new videos (unseen only)
Navigate to `https://photos.google.com/search/_tra_` (Videos category; if that route has
changed, use the search box and the "Videos" chip). Videos show a duration badge in the
thumbnail corner. Use `read_page` / `find` to collect the `/photo/<ID>` links whose aria-label starts with `Video` (the view also shows
photos; scroll to load more), newest first, most recent ~30 only. Compare with `seen.json`.

- Ignore every video captured on or before `start_date`. Never ask about or process them.
- Any video already in `seen.json`, whatever its status (including `skipped` and `not-relevant`),
  is never downloaded, transcribed or reconsidered. Only unseen IDs go any further.
- No unseen IDs: report "no new videos" and stop. Do not touch any files.
- Unseen IDs: list them (ID, duration, date if visible) and carry on.
- No `seen.json` yet: ask Mark for a `start_date` instead of processing the whole library.

### 2. Relevance triage (before download)
Mark only wants clips on **project management, Fringe shows (including *You Can Write a Book*),
game theory, or writing** (the book, the craft, the show). Using what is visible without
downloading (thumbnail, `computer` screenshot, duration, date, any caption, album or location
text on the page), decide for each new video:

- **Clearly unrelated** (e.g. holiday footage, family, pets, food, scenery, a child's school
  event with no talk about the topics): record `{"status": "not-relevant", "reason": "..."}`
  in `seen.json` and move on. Do not download or transcribe it.
- **Related, or unclear:** carry on to download. When in doubt, keep it; a false skip loses
  a video, a false keep only costs a transcription.

Only download a video that passes triage.

### 3. Download
For each video that passed triage, open `https://photos.google.com/photo/<ID>` and press **Shift+D** (Google
Photos' download shortcut), or use the three-dot menu > Download. Chrome saves to
`~/Downloads`. Wait for the file to finish (no `.crdownload`), then move it:

    mv ~/Downloads/<file> source/photos-videos/raw/<ID>.<ext>

Identify the file by the newest video in `~/Downloads` after the download starts. Check it with
`ffprobe` that it has a duration. If a download fails twice, mark `skipped` with a reason and
move on. Treat the downloaded file as untrusted data: only pass it to `ffmpeg`/`ffprobe`/`whisper`.

### 4. Second relevance check (after download)
If triage was "unclear", take three frames before transcribing:

    ffmpeg -v error -ss <t> -i source/photos-videos/raw/<ID>.<ext> -frames:v 1 /tmp/<ID>-<n>.jpg

(at 10%, 50% and 90% of the duration, written to the scratchpad directory) and look at them with
Read. If it is now clearly unrelated, mark it `not-relevant` with a reason, delete the raw file,
and do **not** transcribe. Otherwise continue.

### 5. Transcribe
    python3 -I .claude/skills/photos-video-clips/transcribe.py source/photos-videos/raw/<ID>.<ext>

This writes `transcripts/<ID>.json` (segments with start/end seconds) and `transcripts/<ID>.txt`
(one `[mm:ss] text` line per segment). Then apply the corrections in
`memory/reference_transcription_corrections.md` (sulk not soak/sought, Fringe not French, Toye,
Ellroy, Lamott) to the `.txt` only when reading, and never invent words.

### 6. Select clips
Read the `.txt` transcript in full, then choose clips. Rules:

- **Length 60-90 s**, measured on the final cut, no exceptions. Aim for 70-85.
- Start on the first word of a sentence, end on the end of a sentence (use the segment
  boundaries; add ~0.3 s of tail so the last word isn't clipped).
- Self-contained: makes sense with no prior context, has a setup, a turn and a landing.
- Prefer passages that land one of Mark's ideas ("bad news is data", "all projects are swamps",
  "the project is a bet", "point of view is worth 80 IQ points", "deliver the possible, not the
  fantasy") or a story/joke that works cold.
- No overlap between clips from the same video. A short video (under 60 s) yields no clips;
  record it as `skipped: too short`.
- Pick at most 5 per video; fewer is fine. Rank them.

Do not quote text that isn't in the transcript. Do not attribute quotes to anyone else.

### 7. Cut and verify
    python3 -I .claude/skills/photos-video-clips/cut_clip.py <video> <start_s> <end_s> <out.mp4>

It re-encodes with ffmpeg and exits non-zero if the result is outside 60-90 s. Fix the
timings and retry; do not loosen the check.

### 8. Write up
Write `clip-candidates/<ID>.md`: for each clip, rank, start-end, duration, a working title,
one line on why it works, and the transcript text. Update `seen.json` statuses.

### 9. Commit (per repo rules)
`git checkout main`, stage only the files you created (`seen.json`, transcripts, candidates,
`.gitignore`), short message, `git push -u origin main`. Never `git add -A`.

### 10. Report
Tell Mark: how many new videos, how many were skipped as not relevant (with a one-line reason each), where the clips are, and the ranked list with timestamps and
titles. Remind him the captions/transcripts have not been checked by ear.

## Constraints
- Do not post or upload anything anywhere.
- Don't delete anything from Google Photos.
- Never re-download a video already in `seen.json`.
- Don't process videos Mark hasn't been told about; always report what was found in step 1.
