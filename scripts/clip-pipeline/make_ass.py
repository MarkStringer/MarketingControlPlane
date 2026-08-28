"""Build .ass caption files from the corrected .srt files.

ffmpeg's `subtitles` filter converts SRT using a default 384x288 script
resolution, so a force_style FontSize is multiplied by (video height / 288) -
about 4.7x at 1350 tall. Writing real .ass files with PlayResX/PlayResY set to
the video size means the sizes below are true pixels.
"""
import os, re

P   = "/home/mark/projects/MarketingControlPlane/scripts/clip-pipeline"
SRT = "/home/mark/projects/MarketingControlPlane/source/show/clip-captions"

# name -> (width, height, font size, bottom margin)
PROFILES = {
    "4x5":  (1080, 1350, 42, 72),
    "9x16": (1080, 1920, 42, 300),   # lifted clear of the YouTube Shorts UI
}

HEADER = """[Script Info]
ScriptType: v4.00+
PlayResX: %d
PlayResY: %d
WrapStyle: 0
ScaledBorderAndShadow: yes
YCbCr Matrix: TV.601

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,DejaVu Sans,%d,&H00FFFFFF,&H00FFFFFF,&H33000000,&H33000000,-1,0,0,0,100,100,0,0,3,14,0,2,40,40,%d,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

def to_ass_time(t):
    h, m, rest = t.split(":")
    s, ms = rest.split(",")
    return "%d:%02d:%02d.%02d" % (int(h), int(m), int(s), int(ms) // 10)

def parse(path):
    out = []
    for b in open(path).read().strip().split("\n\n"):
        lines = b.split("\n")
        if len(lines) < 3:
            continue
        a, e = lines[1].split(" --> ")
        out.append((a.strip(), e.strip(), lines[2:]))
    return out

made = 0
for prof, (w, h, size, marginv) in PROFILES.items():
    outdir = os.path.join(P, "ass", prof)
    os.makedirs(outdir, exist_ok=True)
    for f in sorted(os.listdir(SRT)):
        if not f.endswith(".srt"):
            continue
        cues = parse(os.path.join(SRT, f))
        with open(os.path.join(outdir, f[:-4] + ".ass"), "w") as fh:
            fh.write(HEADER % (w, h, size, marginv))
            for a, e, text in cues:
                body = "\\N".join(l.strip() for l in text)
                fh.write("Dialogue: 0,%s,%s,Cap,,0,0,0,,%s\n"
                         % (to_ass_time(a), to_ass_time(e), body))
        made += 1
print("wrote %d .ass files across %d profiles" % (made, len(PROFILES)))
