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
# The published cover wrap: back | spine | front, one page.
# NOT the "Approved Cover" PDF in ~/projects/DTI/coverStuff - that is an earlier
# design with AI chip, target and money icons. The published book has the skull,
# martini glass and biscuit that the show actually refers to.
WRAP = P + "/assets/BookCover_Full.pdf"

tmp = "/tmp/ycwab_wrap"
subprocess.run(["pdftoppm", "-r", "300", "-png", "-singlefile", WRAP, tmp],
               check=True, capture_output=True)
wrap = Image.open(tmp + ".png").convert("RGB")
wrap.crop((0, 0, 1831, wrap.height)).save(IMG + "/book_back.png")      # spine edges
wrap.crop((2066, 0, wrap.width, wrap.height)).save(IMG + "/book_front.png")
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
