import os, subprocess, sys

SP  = "/home/mark/projects/MarketingControlPlane/scripts/clip-pipeline"
OUT = "/home/mark/projects/MarketingControlPlane/source/show/assets/clips/shorts"
ASS = "/home/mark/projects/MarketingControlPlane/scripts/clip-pipeline/ass/9x16"


names = sorted(f for f in os.listdir(OUT)
               if f.endswith(".mp4") and not f.endswith("-subtitled.mp4"))
only = sys.argv[1:] or None

for name in names:
    slug = name[len("clip-00-"):-len(".mp4")]
    if only and slug not in only:
        continue
    src = os.path.join(OUT, name)
    srt = os.path.join(ASS, slug + ".ass")
    dst = os.path.join(OUT, name[:-4] + "-subtitled.mp4")
    if not os.path.exists(srt):
        print("no ass for", slug); continue
    if os.path.exists(dst):
        print("skip", os.path.basename(dst)); continue
    vf = "ass=%s" % srt.replace(":", r"\:")
    r = subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", src,
                        "-vf", vf, "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
                        "-pix_fmt", "yuv420p", "-c:a", "copy", "-movflags", "+faststart", dst],
                       capture_output=True, text=True)
    if r.returncode != 0:
        print("FAIL", slug, r.stderr[-900:])
    else:
        print("ok  %-45s %.1f MB" % (os.path.basename(dst), os.path.getsize(dst)/1e6))
