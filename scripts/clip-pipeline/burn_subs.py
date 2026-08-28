import os, subprocess, sys

SP  = "/home/mark/projects/MarketingControlPlane/scripts/clip-pipeline"
OUT = "/home/mark/projects/MarketingControlPlane/source/show/assets/clips"
SRT = "/home/mark/projects/MarketingControlPlane/source/show/clip-captions"

STYLE = ("FontName=DejaVu Sans,FontSize=40,Bold=1,"
         "PrimaryColour=&H00FFFFFF&,BackColour=&HA0000000&,"
         "BorderStyle=3,Outline=8,Shadow=0,"
         "Alignment=2,MarginV=64,MarginL=50,MarginR=50")

names = sorted(f for f in os.listdir(OUT)
               if f.endswith(".mp4") and not f.endswith("-subtitled.mp4"))
only = sys.argv[1:] or None

for name in names:
    slug = name[len("clip-00-"):-len(".mp4")]
    if only and slug not in only:
        continue
    src = os.path.join(OUT, name)
    srt = os.path.join(SRT, slug + ".srt")
    dst = os.path.join(OUT, name[:-4] + "-subtitled.mp4")
    if not os.path.exists(srt):
        print("no srt for", slug); continue
    if os.path.exists(dst):
        print("skip", os.path.basename(dst)); continue
    vf = "subtitles=%s:force_style='%s'" % (srt.replace(":", r"\:"), STYLE)
    r = subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", src,
                        "-vf", vf, "-c:v", "libx264", "-preset", "medium", "-crf", "20",
                        "-pix_fmt", "yuv420p", "-c:a", "copy", "-movflags", "+faststart", dst],
                       capture_output=True, text=True)
    if r.returncode != 0:
        print("FAIL", slug, r.stderr[-900:])
    else:
        print("ok  %-45s %.1f MB" % (os.path.basename(dst), os.path.getsize(dst)/1e6))
