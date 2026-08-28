# -*- coding: utf-8 -*-
"""Correct the machine-generated captions before they are burned in."""
import os, re, sys

SP  = "/home/mark/projects/MarketingControlPlane/scripts/clip-pipeline"
SRC = SP + "/srt-raw"
DST = "/home/mark/projects/MarketingControlPlane/source/show/clip-captions"
os.makedirs(DST, exist_ok=True)

MAXLINE, MAXLINES = 42, 2

# applied to every file, in order
GLOBAL = [
    (r"(\d) ,(\d)", r"\1,\2"),           # 20 ,000 -> 20,000
    (r"(\w) -(\w)", r"\1-\2"),           # duty -free -> duty-free, non -fiction
    (r"\s+([,.?!])", r"\1"),
    (r"\bemotional labor\b", "emotional labour"),
    (r"\blabor\b", "labour"),
    (r"\brealize\b", "realise"),
    (r"\brealized\b", "realised"),
    (r"\brecognize\b", "recognise"),
    (r"\bapologize\b", "apologise"),
    (r"\bDeliving the Impossible\b", "Delivering the Impossible"),
    (r"\bDeliberately Impossible\b", "Delivering the Impossible"),
    (r"\bA Press\b", "Apress"),
    (r"\bEllen Mott\b", "Anne Lamott"),
    (r"\bA(?:m|)lamot\b", "Anne Lamott"),
    (r"\bJames [AE]lroy\b", "James Ellroy"),
    (r"\bP\.?G\.? Wood ?[Hh]ouse\b", "P.G. Wodehouse"),
    (r"\bHuntress Thompson\b", "Hunter S. Thompson"),
    (r"\bArleigh Russell\b", "Arlie Russell"),
    (r"\bAli Russell\b", "Arlie Russell"),
    (r"\bAudemars\b", "Audubon"),
    (r"\bhalf ?-?assed\b", "half-arsed"),
    (r"\bseven[- ]eighths?[- ](?:assed|asked)\b", "seven-eighths-arsed"),
    (r"\btenth of an ass\b", "tenth of an arse"),
    (r"\bthe meadows\b", "the Meadows"),
    (r"\bstand up\b", "stand-up"),
    (r"\bfringe theatre\b", "Fringe theatre"),
    (r"\bFrench show\b", "Fringe show"),
]

# per-clip corrections: (pattern, replacement)
PER_FILE = {
    "paul-mccartney": [
        (r"and he's\s*\n?lined with CDs", "and it's lined with CDs"),
        (r"\bhe's lined with CDs\b", "it's lined with CDs"),
        (r"by a bunch of different majors", "by a bunch of different measures"),
    ],
    "six-year-sulk": [
        (r"But I need new book stems and mine with both hands\.",
         "But I need to put this down, because I mime with both hands."),
        (r"\bI salt for six years\b", "I sulked for six years"),
        (r"\bI sought for six years\b", "I sulked for six years"),
    ],
    "victoria-line": [
        (r"I left them somewhere on the London\. The London Underground",
         "I left them somewhere on the London Underground. The London Underground"),
        (r"the subconscious, I probably quite closely related",
         "the subconscious are probably quite closely related"),
    ],
    "slush-pile": [
        (r"^and One of the good things", "One of the good things"),
        (r"\bThat's what it's called\b", "is what it's called"),
        (r"\bThey had somebody hadn't put\b", "Somebody hadn't put"),
    ],
    "john-mills-bathroom": [
        (r"either to the article or the Antarctic", "either to the Arctic or the Antarctic"),
        (r"\ba poll unaided\b", "a pole unaided"),
        (r"and now I'm look at me I'm in trouble", "and now, look at me, I'm in trouble"),
        (r"when you write your letters", "when you get letters like that"),
        (r"no I can't I've talked to the banks I can't", "no, I've talked to the banks"),
        (r"John Mills house of tea", "John Mills' house for tea"),
        (r"John Mills said what are you gonna have to talk you out of it",
         "John Mills said, well, you're going to have to talk your way out of it"),
        (r"talk to people about walking to the Antarctic where it was",
         "talk to people about walking to the Antarctic, wherever it was"),
        (r"\bI saw your film Scott of the Antarctic\b",
         "I saw your film, Scott of the Antarctic"),
    ],
    "tell-me-a-story": [],
    "talking-in-a-field": [],
    "emotional-labour": [
        (r"people who sell you soft drinks", "people who sell soft drinks"),
    ],
    "skull-not-crossbones": [
        (r"if ever you never want to be alone and just start to mix a martini",
         "if you never want to be alone, just start to mix a martini"),
        (r"\bchapter ship\b", "Chapter Ship"),
    ],
    "englished-our-way": [],
    "nearest-and-dearest": [],
    "opening-the-box": [
        (r"I mentioned that I mentioned as a subconscious thing",
         "I mentioned the subconscious thing"),
    ],
    "audience-of-one": [
        (r"this is\.\.\. You can write a book\. I'm Mark Stringer\.",
         "this is You Can Write a Book, by Mark Stringer."),
    ],
    "split-infinitive": [
        (r"\bSplit Infinity\b", "split infinitive"),
        (r"\bthe infinity is just one word\b", "the infinitive is just one word"),
        (r"\bWord processes\b", "Word processors"),
    ],
    "tech-rehearsal": [
        (r"So like when I first when I first came here", "So when I first came here"),
        (r"I got no idea what fucking tech rehearsal was",
         "I had no idea what a fucking tech rehearsal was"),
        (r"about the lighting doesn't mean I'm not really gonna know I'm like an idiot",
         "about the lighting or something I'm not really going to know. I'm not, like, an idiot"),
        (r"there was like part me was thinking", "there was like part of me was thinking"),
        (r"I won't just I just won't do this show", "I just won't do this show"),
        (r"do you want to play some music cuz like yeah",
         "do you want to play some music? I was like, yeah"),
        (r"\bfringe show\b", "Fringe show"),
    ],
}

def wrap(text):
    """Re-wrap to at most MAXLINES balanced lines."""
    words = text.split()
    if not words:
        return text
    full = " ".join(words)
    if len(full) <= MAXLINE:
        return full
    # balance across two lines
    best, bestcost = None, None
    for i in range(1, len(words)):
        a, b = " ".join(words[:i]), " ".join(words[i:])
        if len(a) > MAXLINE or len(b) > MAXLINE:
            continue
        cost = abs(len(a) - len(b))
        if bestcost is None or cost < bestcost:
            best, bestcost = (a, b), cost
    if best:
        return best[0] + "\n" + best[1]
    # too long for two lines: greedy fill, keep everything
    lines, cur = [], ""
    for w in words:
        if cur and len(cur) + 1 + len(w) > MAXLINE:
            lines.append(cur); cur = w
        else:
            cur = (cur + " " + w).strip()
    if cur:
        lines.append(cur)
    return "\n".join(lines)


def parse(path):
    blocks = open(path).read().strip().split("\n\n")
    out = []
    for b in blocks:
        lines = b.split("\n")
        if len(lines) < 3:
            continue
        out.append((lines[0], lines[1], " ".join(lines[2:])))
    return out

def split_time(ts):
    a, b = ts.split(" --> ")
    def sec(t):
        h, m, rest = t.split(":")
        s, ms = rest.split(",")
        return int(h)*3600 + int(m)*60 + int(s) + int(ms)/1000.0
    return sec(a), sec(b)

def fmt(s):
    h = int(s//3600); m = int(s%3600//60); x = s%60
    return "%02d:%02d:%02d,%03d" % (h, m, int(x), round((x-int(x))*1000))

MAXCUE = MAXLINE * MAXLINES - 10

report = []
for f in sorted(os.listdir(SRC)):
    if not f.endswith(".srt"):
        continue
    slug = f[:-4]
    cues = parse(os.path.join(SRC, f))

    # --- correct at document level so cross-cue phrases match ---
    words = []
    bounds = [0]
    for _, _, text in cues:
        words += text.split()
        bounds.append(len(words))
    doc = " ".join(words)
    before = doc
    for pat, rep in GLOBAL + PER_FILE.get(slug, []):
        doc = re.sub(pat, rep, doc)
    doc = re.sub(r"\s{2,}", " ", doc).strip()
    new_words = doc.split()

    # map old word boundaries onto the corrected word list
    import difflib
    sm = difflib.SequenceMatcher(a=words, b=new_words, autojunk=False)
    mapping = {}
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        for i in range(i1, i2 + 1):
            if i not in mapping:
                span_a = max(i2 - i1, 1)
                frac = (i - i1) / span_a
                mapping[i] = min(len(new_words), j1 + int(round(frac * (j2 - j1))))
    mapping[len(words)] = len(new_words)
    nb = [mapping.get(b, b) for b in bounds]
    nb = sorted(set(nb))
    while len(nb) < len(bounds):
        nb.append(len(new_words))

    out = []
    for k in range(len(cues)):
        s0, e0 = split_time(cues[k][1])
        lo = nb[k] if k < len(nb) else len(new_words)
        hi = nb[k+1] if k+1 < len(nb) else len(new_words)
        text = " ".join(new_words[lo:hi]).strip()
        if not text:
            continue
        # split a cue that is too long for two lines, sharing its time slot
        if len(text) > MAXCUE:
            ws = text.split()
            half = len(ws)//2
            for w in range(half, len(ws)):
                if ws[w-1].endswith((",", ".", "?", "!")):
                    half = w; break
            a, b = " ".join(ws[:half]), " ".join(ws[half:])
            mid = s0 + (e0-s0) * len(a)/max(len(text), 1)
            out.append((s0, mid-0.02, a))
            out.append((mid, e0, b))
        else:
            out.append((s0, e0, text))

    with open(os.path.join(DST, f), "w") as fh:
        for i, (s0, e0, text) in enumerate(out, 1):
            fh.write("%d\n%s --> %s\n%s\n\n" % (i, fmt(s0), fmt(e0), wrap(text)))

    over = sum(1 for _, _, t in out if len(wrap(t).split("\n")) > MAXLINES)
    report.append((slug, len(cues), len(out), 0 if doc == before else 1, over))

print("%-24s %6s %6s %7s %9s" % ("clip", "in", "out", "edited", ">2 lines"))
for r in report:
    print("%-24s %6d %6d %7d %9d" % r)
