"""Rebuild the image assets from their original sources.

Run this if scripts/clip-pipeline/assets/ is missing or you want to refresh it.
Nothing here is authored by the pipeline; it is all derived from files that live
elsewhere on this machine, which is why the assets directory is not committed.
"""
import os, subprocess
from PIL import Image

P    = "/home/mark/projects/MarketingControlPlane/scripts/clip-pipeline"
IMG  = P + "/assets/img"
IMG9 = P + "/assets/img9x16"
os.makedirs(IMG, exist_ok=True)
os.makedirs(IMG9, exist_ok=True)

FLYER = "/home/mark/projects/EdinburghShow"
BLOG  = "/home/mark/projects/MarkStringer.github.io/assets"
WRAP  = ("/home/mark/projects/DTI/coverStuff/"
         "979-8-8688-2204-9_Stringer_Approved Cover.pdf")

# flyers, straight copies
for src, dst in [(FLYER + "/flyer_a5_front.png",   IMG + "/flyer_front.png"),
                 (FLYER + "/flyer_a5_back_v2.png", IMG + "/flyer_back.png")]:
    Image.open(src).convert("RGB").save(dst)

# photographs
for src, dst in [(BLOG + "/mark-headshot-colour.jpg",  IMG + "/photo_headshot_colour.jpg"),
                 (BLOG + "/mark-headshot-bw.jpg",      IMG + "/photo_headshot_bw.jpg"),
                 (BLOG + "/MarkStringerMeOnStage.jpg", IMG + "/photo_on_stage.jpg")]:
    Image.open(src).convert("RGB").save(dst)

# book covers: the approved cover PDF is one page holding back | spine | front
tmp = "/tmp/ycwab_wrap"
subprocess.run(["pdftoppm", "-r", "300", "-png", "-singlefile", WRAP, tmp],
               check=True, capture_output=True)
wrap = Image.open(tmp + ".png").convert("RGB")
sc = wrap.width / 1949.0                      # spine edges measured at 150dpi
wrap.crop((0, 0, int(915 * sc), wrap.height)).save(IMG + "/book_back.png")
wrap.crop((int(1033 * sc), 0, wrap.width, wrap.height)).save(IMG + "/book_front.png")
os.remove(tmp + ".png")

# pre-composite everything onto the 1080x1920 Shorts canvas so ffmpeg never rescales
W, H = 1080, 1920
CANVAS = [("flyer_front.png",           (0, 0, 0)),
          ("photo_on_stage.jpg",        (9, 15, 3)),
          ("flyer_back.png",            (249, 219, 189)),
          ("photo_headshot_colour.jpg", (255, 255, 255)),
          ("book_front.png",            (132, 206, 228)),
          ("photo_headshot_bw.jpg",     (255, 255, 255)),
          ("book_back.png",             (132, 206, 228))]
for name, bg in CANVAS:
    im = Image.open(os.path.join(IMG, name)).convert("RGB")
    r  = min(W / im.width, H / im.height)
    sm = im.resize((int(im.width * r), int(im.height * r)), Image.LANCZOS)
    c  = Image.new("RGB", (W, H), bg)
    c.paste(sm, ((W - sm.width) // 2, (H - sm.height) // 2))
    c.save(os.path.join(IMG9, os.path.splitext(name)[0] + ".png"))

print("rebuilt %d source images and %d Shorts canvases" % (len(os.listdir(IMG)), len(os.listdir(IMG9))))
