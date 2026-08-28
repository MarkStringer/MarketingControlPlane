"""Delete any rendered file whose duration does not match its expected length."""
import os, subprocess, sys

D = "/home/mark/projects/MarketingControlPlane/source/show/assets/clips"

def t(m):
    a, b = m.split(":"); return int(a)*60 + int(b)

CLIPS = [
    (1,  "paul-mccartney",       "44:00", "45:31"), (2,  "six-year-sulk",      "11:00", "11:58"),
    (3,  "victoria-line",        "42:26", "43:23"), (4,  "slush-pile",         "08:00", "09:02"),
    (5,  "john-mills-bathroom",  "27:53", "29:41"), (6,  "talking-in-a-field", "30:17", "31:23"),
    (7,  "tell-me-a-story",      "33:46", "34:53"), (8,  "emotional-labour",   "40:31", "41:47"),
    (9,  "skull-not-crossbones", "49:07", "50:06"), (10, "englished-our-way",  "51:05", "51:51"),
    (11, "nearest-and-dearest",  "51:53", "52:41"), (12, "opening-the-box",    "59:27", "60:20"),
    (13, "audience-of-one",      "00:03", "01:07"), (14, "split-infinitive",   "20:53", "22:01"),
    (15, "tech-rehearsal",       "56:32", "57:28"),
]

def dur(p):
    try:
        out = subprocess.run(["ffprobe","-v","error","-show_entries","format=duration",
                              "-of","csv=p=0",p], capture_output=True, text=True).stdout.strip()
        return float(out)
    except Exception:
        return None

removed = kept = 0
for order, slug, tin, tout in CLIPS:
    want = t(tout) - t(tin)
    for d in (D, os.path.join(D, "shorts")):
        for suffix in ("", "-subtitled"):
            p = os.path.join(d, "clip-%02d-%s%s.mp4" % (order, slug, suffix))
            if not os.path.exists(p):
                continue
            got = dur(p)
            if got is None or abs(got - want) > 0.6:
                print("removing %-46s want %5.1fs got %s" %
                      (os.path.relpath(p, D), want, ("%.1fs" % got) if got else "unreadable"))
                os.remove(p); removed += 1
            else:
                kept += 1
print("verified: %d good, %d removed" % (kept, removed))
