#!/bin/bash
# Generates a Work in Progress show poster sized for Instagram (1080x1350, 4:5).
#
# WIP shows:
#   Cavendish Arms, Stockwell
#   128 Hartington Rd, London SW8 2HJ
#   Tuesday 16th June 2026
#   Tuesday 30th June 2026
#
# Source image: ~/Downloads/vectorstock_43267619.jpg (3000x1660)
# Fonts required:
#   - Pirata One: ~/.local/share/fonts/adventure/PirataOne-Regular.ttf
#   - Helvetica Bold: system font

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SOURCE_IMAGE=~/Downloads/vectorstock_43267619.jpg
WIP_TAG=/tmp/wip_tag_text.png
POSTER_BASE=/tmp/wip_poster_insta_base.png
OUTPUT="$SCRIPT_DIR/wip-poster-insta.png"

# Step 1: Main poster (1080x1350)
convert -size 1080x1350 xc:'#4169E1' \
  \( "$SOURCE_IMAGE" \
     -fuzz 20% -fill '#4169E1' -opaque white \
     -resize x1350 -gravity center -extent 1080x1350 \) \
  -composite \
  -font Helvetica-Bold -fill white \
  -gravity North -pointsize 110 -annotate +0+20 "Mark Stringer" \
  -gravity North -pointsize 260 \
  -fill '#001a4d' -stroke none -font Pirata-One \
  -annotate +5+185 "You can" \
  -annotate +5+445 "write" \
  -annotate +5+705 "a book!" \
  -fill '#FFD700' -stroke '#1a237e' -strokewidth 4 \
  -annotate +0+180 "You can" \
  -annotate +0+440 "write" \
  -annotate +0+700 "a book!" \
  -stroke none \
  -fill white -font Helvetica -pointsize 32 \
  -gravity South \
  -annotate +0+320 "Work in Progress Shows" \
  -annotate +0+270 "Tuesday 16th & 30th June 2026" \
  -annotate +0+220 "9:00pm" \
  -annotate +0+170 "Cavendish Arms, Stockwell" \
  -annotate +0+120 "128 Hartington Rd, London SW8 2HJ" \
  -fill '#FFD700' -draw "polygon 700,1350 1080,1350 1080,1010" \
  "$POSTER_BASE"

# Step 2: WORK / IN / PROGRESS tag
convert -size 240x135 xc:none \
  -alpha on \
  -font Helvetica-Bold -fill '#1a237e' -pointsize 36 \
  -gravity center \
  -annotate +0-38 "WORK" \
  -annotate +0+0 "IN" \
  -annotate +0+38 "PROGRESS" \
  -background none -rotate -45 +repage \
  "$WIP_TAG"

# Step 3: QR code (navy on yellow, links to Eventbrite)
QR_IMG=/tmp/wip_qr.png
qrencode -o "$QR_IMG" -s 5 -m 2 \
  --foreground=1a237e --background=FFD700 \
  "https://www.eventbrite.com/e/you-can-write-a-book-tickets-1986985842142?aff=erellivmlt"

# Step 4: Composite WIP tag (bottom right) and QR code (bottom left)
convert "$POSTER_BASE" \
  "$WIP_TAG" -gravity NorthWest -geometry +810+1100 -composite \
  "$QR_IMG"  -gravity SouthWest -geometry +20+20   -composite \
  "$OUTPUT"

echo "Written: $OUTPUT"
