# -*- coding: utf-8 -*-
"""Cut, caption and render the closing-night clips.

Source is two portrait phone recordings from 29 August 2026. Both are
1080x1920 after rotation, so 9:16 is the native frame and needs no crop. The
4:5 version fits the whole frame inside 1080x1350 over a blurred copy of
itself rather than cropping, because the framing is too tight to crop.

Every stage skips work that is already done, so this is safe to re-run.
"""
import os, subprocess, sys, json
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from corrections import fix

REPO = "/home/mark/projects/MarketingControlPlane"
DL   = "/home/mark/Downloads"
OUT  = REPO + "/source/show/assets/clips-2026-08-29"
S916 = OUT
S45  = OUT + "/4x5"
CAPS = REPO + "/source/show/clip-captions-2026-08-29"
WORK = HERE + "/work"
for d in (S916, S45, CAPS, WORK, WORK + "/wav", WORK + "/srt", WORK + "/ass"):
    os.makedirs(d, exist_ok=True)

SRC = {"A": DL + "/20260829_182537.mp4",   # the show, 48m37s
       "B": DL + "/20260829_191832.mp4"}   # piece to camera, 1m43s

def t(x):
    m, s = x.split(":")
    return int(m) * 60 + int(s)

#      n  slug                          src  in       out
CLIPS = [
    ( 1, "it-finally-happened",          "B", "00:00", "01:43"),
    ( 2, "the-empty-room",               "A", "21:33", "23:09"),
    ( 3, "im-stuck-again",               "A", "08:25", "09:14"),
    ( 4, "stay-in-the-pool",             "A", "42:53", "44:24"),
    ( 5, "why-should-i-listen-to-you",   "A", "47:19", "48:37"),
    ( 6, "a-technical-term",             "A", "02:14", "03:26"),
    ( 7, "a-tenth-of-an-arse",           "A", "10:25", "12:14"),
    ( 8, "i-sulked-for-six-years",       "A", "13:31", "15:28"),
    ( 9, "not-at-the-beginning",         "A", "16:11", "17:56"),
    (10, "you-are-in-the-club",          "A", "29:17", "30:16"),
    (11, "skull-not-crossbones",         "A", "33:24", "34:34"),
    (12, "not-paul-mccartney",           "A", "34:43", "36:00"),
    (13, "improve-your-scene",           "A", "36:29", "38:14"),
    (14, "talk-your-way-out-of-it",      "A", "38:44", "40:33"),
    (15, "come-in-the-bathroom",         "A", "41:26", "42:53"),
    (16, "put-it-all-in-one-place",      "A", "26:59", "28:26"),
    (17, "a-body-under-the-patio",       "A", "24:01", "25:14"),
]

if sys.argv[1:]:
    CLIPS = [c for c in CLIPS if c[1] in sys.argv[1:]]

def name(n, slug):
    return "clip-%02d-%s" % (n, slug)

def run(args):
    r = subprocess.run(args, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(" ".join(args[:6]) + "\n" + r.stderr[-1500:])

def dur(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "default=nw=1:nk=1", path], capture_output=True, text=True)
    try:    return float(r.stdout.strip())
    except: return 0.0

# ---------------------------------------------------------------- 1. cut 9:16
def cut(job):
    n, slug, src, tin, tout = job
    dst = "%s/%s.mp4" % (S916, name(n, slug))
    want = t(tout) - t(tin)
    if os.path.exists(dst) and abs(dur(dst) - want) < 1.5:
        return
    print("cut ", name(n, slug), flush=True)
    run(["ffmpeg", "-y", "-loglevel", "error", "-ss", str(t(tin)), "-to", str(t(tout)),
         "-i", SRC[src], "-vf", "hqdn3d=6:4:8:6,scale=1080:1920:force_original_aspect_ratio=decrease,"
                               "pad=1080:1920:(ow-iw)/2:(oh-ih)/2,setsar=1",
         "-c:v", "libx264", "-preset", "medium", "-crf", "24", "-threads", "5", "-pix_fmt", "yuv420p",
         "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", dst])

with ThreadPoolExecutor(max_workers=3) as ex:
    list(ex.map(cut, CLIPS))

# ------------------------------------------------------- 2. word-level captions
todo = [c for c in CLIPS if not os.path.exists("%s/%s.srt" % (CAPS, c[1]))]
if todo:
    from faster_whisper import WhisperModel
    model = WhisperModel("distil-large-v3", device="cpu", compute_type="int8", cpu_threads=16)

MAXCHARS, MAXGAP = 72, 0.7

def srt_time(x):
    h, m, s = int(x // 3600), int(x % 3600 // 60), x % 60
    return "%02d:%02d:%02d,%03d" % (h, m, int(s), round((s - int(s)) * 1000))

def wrap(text, maxline=40):
    w = text.split()
    if len(" ".join(w)) <= maxline:
        return " ".join(w)
    best, cost = None, None
    for i in range(1, len(w)):
        a, b = " ".join(w[:i]), " ".join(w[i:])
        if len(a) > maxline or len(b) > maxline:
            continue
        c = abs(len(a) - len(b))
        if cost is None or c < cost:
            best, cost = (a, b), c
    if best:
        return best[0] + "\n" + best[1]
    lines, cur = [], ""
    for x in w:
        if cur and len(cur) + 1 + len(x) > maxline:
            lines.append(cur); cur = x
        else:
            cur = (cur + " " + x).strip()
    if cur:
        lines.append(cur)
    return "\n".join(lines)

for n, slug, src, tin, tout in todo:
    wav = "%s/wav/%s.wav" % (WORK, slug)
    if not os.path.exists(wav):
        run(["ffmpeg", "-y", "-loglevel", "error", "-i", "%s/%s.mp4" % (S916, name(n, slug)),
             "-ac", "1", "-ar", "16000", "-vn", wav])
    print("srt ", slug, flush=True)
    segs, _ = model.transcribe(wav, language="en", beam_size=5, word_timestamps=True,
                               vad_filter=True, condition_on_previous_text=False)
    words = [w for s in segs for w in (s.words or [])]

    # group words into cues, then correct the whole clip at document level
    cues, cur = [], []
    for w in words:
        if cur and (len(" ".join(x.word.strip() for x in cur)) + 1 + len(w.word.strip()) > MAXCHARS
                    or w.start - cur[-1].end > MAXGAP):
            cues.append(cur); cur = []
        cur.append(w)
    if cur:
        cues.append(cur)

    raw = [" ".join(x.word.strip() for x in c) for c in cues]
    doc = fix(" ".join(raw))
    # put the corrected words back on the cue boundaries
    import difflib
    old = " ".join(raw).split()
    new = doc.split()
    bounds, k = [0], 0
    for c in raw:
        k += len(c.split()); bounds.append(k)
    sm = difflib.SequenceMatcher(a=old, b=new, autojunk=False)
    mp = {}
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        for i in range(i1, i2 + 1):
            if i not in mp:
                span = max(i2 - i1, 1)
                mp[i] = min(len(new), j1 + int(round((i - i1) / span * (j2 - j1))))
    mp[len(old)] = len(new)
    nb = [mp.get(b, b) for b in bounds]
    for i in range(1, len(nb)):
        nb[i] = max(nb[i], nb[i - 1])
    nb[-1] = len(new)

    with open("%s/%s.srt" % (CAPS, slug), "w") as f:
        i = 0
        for k, c in enumerate(cues):
            text = " ".join(new[nb[k]:nb[k + 1]]).strip()
            if not text:
                continue
            i += 1
            f.write("%d\n%s --> %s\n%s\n\n" %
                    (i, srt_time(c[0].start), srt_time(c[-1].end), wrap(text)))

# ------------------------------------------------------------------- 3. .ass
HEADER = """[Script Info]
ScriptType: v4.00+
PlayResX: %d
PlayResY: %d
WrapStyle: 0
ScaledBorderAndShadow: yes
YCbCr Matrix: TV.601

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,DejaVu Sans,%d,&H00FFFFFF,&H00FFFFFF,&H20000000,&H20000000,-1,0,0,0,100,100,0,0,3,16,0,2,40,40,%d,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
PROFILES = {"9x16": (1080, 1920, 46, 320), "4x5": (1080, 1350, 44, 80)}

def ass_time(x):
    h, m, rest = x.split(":")
    s, ms = rest.split(",")
    return "%d:%02d:%02d.%02d" % (int(h), int(m), int(s), int(ms) // 10)

for prof, (w, h, size, mv) in PROFILES.items():
    d = "%s/ass/%s" % (WORK, prof)
    os.makedirs(d, exist_ok=True)
    for f in sorted(os.listdir(CAPS)):
        if not f.endswith(".srt"):
            continue
        blocks = open(os.path.join(CAPS, f)).read().strip().split("\n\n")
        with open(os.path.join(d, f[:-4] + ".ass"), "w") as fh:
            fh.write(HEADER % (w, h, size, mv))
            for b in blocks:
                L = b.split("\n")
                if len(L) < 3:
                    continue
                a, e = L[1].split(" --> ")
                fh.write("Dialogue: 0,%s,%s,Cap,,0,0,0,,%s\n" %
                         (ass_time(a.strip()), ass_time(e.strip()), "\\N".join(L[2:])))

# --------------------------------------------------------------- 4. renders
BLUR = ("split[a][b];"
        "[a]scale=1080:1350:force_original_aspect_ratio=increase,crop=1080:1350,"
        "gblur=sigma=40[bg];"
        "[b]scale=-2:1350[fg];"
        "[bg][fg]overlay=(W-w)/2:0,setsar=1")

render_jobs = []
for n, slug, src, tin, tout in CLIPS:
    base, want = name(n, slug), t(tout) - t(tin)
    jobs = [
        ("%s/%s-subtitled.mp4" % (S916, base),
         "ass=%s/ass/9x16/%s.ass" % (WORK, slug), "%s/%s.mp4" % (S916, base)),
        ("%s/%s.mp4" % (S45, base), BLUR, "%s/%s.mp4" % (S916, base)),
        ("%s/%s-subtitled.mp4" % (S45, base),
         BLUR + ",ass=%s/ass/4x5/%s.ass" % (WORK, slug), "%s/%s.mp4" % (S916, base)),
    ]
    for dst, vf, srcfile in jobs:
        if os.path.exists(dst) and abs(dur(dst) - want) < 1.5:
            continue
        render_jobs.append((dst, vf, srcfile))

def render(job):
    dst, vf, srcfile = job
    print("rend", os.path.relpath(dst, OUT), flush=True)
    run(["ffmpeg", "-y", "-loglevel", "error", "-i", srcfile, "-vf", vf,
             "-c:v", "libx264", "-preset", "medium", "-crf", "22", "-threads", "5",
             "-pix_fmt", "yuv420p", "-c:a", "copy", "-movflags", "+faststart", dst])

with ThreadPoolExecutor(max_workers=3) as ex:
    list(ex.map(render, render_jobs))

print("done")
