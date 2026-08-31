---
description: Restart the unfinished closing-night clip renders and report progress
---

Pick up the 29 August 2026 clip pipeline where it stopped.

1. Run `scripts/closing-night/make_clips.py --status` to see what is already done.
2. If anything is missing, start `scripts/closing-night/resume.sh` **in the background**
   (`run_in_background: true`) and tell the user what is outstanding and roughly how long it
   will take. Three renders take about four and a half minutes between them.
3. If nothing is missing, say so and stop. Do not re-render finished work.

Notes:

- The script sweeps any half-written file before it starts, so a render interrupted by the
  machine shutting down is thrown away and redone rather than trusted.
- It needs `~/Downloads/20260829_182537.mp4` and `~/Downloads/20260829_191832.mp4`. Neither is
  in the repo. If they are gone the script says so and exits, and the clips cannot be rebuilt.
- Outputs land in `source/show/assets/clips-2026-08-29/` (gitignored). Captions land in
  `source/show/clip-captions-2026-08-29/` (committed).
- Only one instance runs at a time; a second one exits immediately rather than fighting over
  the same files.

Context for what the clips are: `source/show/clip-candidates-2026-08-29.md`.
How the pipeline works: `scripts/closing-night/README.md`.
