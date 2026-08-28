import subprocess, os, sys

SP  = "/home/mark/projects/MarketingControlPlane/scripts/clip-pipeline"
IMG = SP + "/assets/img9x16"
OUT = "/home/mark/projects/MarketingControlPlane/source/show/assets/clips/shorts"
DL  = "/home/mark/Downloads"

W, H = 1080, 1920

AUDIO = {
    "22": DL + "/Voice 260822_181740.m4a",
    "24": DL + "/Voice 260824_181409.m4a",
    "25": DL + "/Voice 260825_182031.m4a",
}

# alternating print material and photographs
IMAGES = [
    (IMG + "/flyer_front.png",          "black"),
    (IMG + "/photo_on_stage.png",       "0x090F03"),
    (IMG + "/flyer_back.png",           "0xF9DBBD"),
    (IMG + "/photo_headshot_colour.png","white"),
    (IMG + "/book_front.png",           "0x84CEE4"),
    (IMG + "/photo_headshot_bw.png",    "white"),
    (IMG + "/book_back.png",            "0x84CEE4"),
]

def t(mmss):
    m, s = mmss.split(":")
    return int(m) * 60 + int(s)

# (order, slug, source date, in, out)
CLIPS = [
    (1,  "paul-mccartney",        "22", "44:00", "45:31"),
    (2,  "six-year-sulk",         "22", "11:00", "11:58"),
    (3,  "victoria-line",         "24", "42:26", "43:23"),
    (4,  "slush-pile",            "22", "08:00", "09:02"),
    (5,  "john-mills-bathroom",   "24", "27:53", "29:41"),
    (6,  "talking-in-a-field",    "24", "30:17", "31:23"),
    (7,  "tell-me-a-story",       "22", "33:46", "34:53"),
    (8,  "emotional-labour",      "22", "40:31", "41:47"),
    (9,  "skull-not-crossbones",  "22", "49:07", "50:06"),
    (10, "englished-our-way",     "24", "51:05", "51:51"),
    (11, "nearest-and-dearest",   "24", "51:53", "52:41"),
    (12, "opening-the-box",       "24", "59:27", "60:20"),
    (13, "audience-of-one",       "25", "00:03", "01:07"),
    (14, "split-infinitive",      "22", "20:53", "22:01"),
    (15, "tech-rehearsal",        "24", "56:32", "57:28"),
]

only = sys.argv[1:] or None
os.makedirs(OUT, exist_ok=True)

for order, slug, date, tin, tout in CLIPS:
    if only and slug not in only:
        continue
    dur = t(tout) - t(tin)
    n = len(IMAGES)
    # split duration across images, remainder onto the last
    each = round(dur / n, 3)
    spans = [each] * (n - 1) + [round(dur - each * (n - 1), 3)]

    name = "clip-%02d-%s.mp4" % (order, slug)
    dest = os.path.join(OUT, name)
    if os.path.exists(dest):
        print("skip", name); continue

    cmd = ["ffmpeg", "-y", "-loglevel", "error"]
    for (path, _), span in zip(IMAGES, spans):
        cmd += ["-loop", "1", "-t", str(span), "-i", path]
    cmd += ["-ss", str(t(tin)), "-to", str(t(tout)), "-i", AUDIO[date]]

    parts = []
    for i, (path, bg) in enumerate(IMAGES):
        parts.append(
            "[%d:v]setsar=1,fps=25[v%d]" % (i, i)
        )
    parts.append("".join("[v%d]" % i for i in range(n)) + "concat=n=%d:v=1:a=0[v]" % n)

    cmd += [
        "-filter_complex", ";".join(parts),
        "-map", "[v]", "-map", "%d:a" % n,
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart",
        "-shortest", dest,
    ]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print("FAIL %s\n%s" % (name, r.stderr[-1500:]))
    else:
        print("ok  %-40s %3ds  %.1f MB" % (name, dur, os.path.getsize(dest) / 1e6))
