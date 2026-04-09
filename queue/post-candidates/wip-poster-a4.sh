#!/bin/bash
# Generates a Work in Progress show poster at A4 print resolution (2480x3508, 300dpi).
#
# WIP shows:
#   Cavendish Arms, Stockwell
#   128 Hartington Rd, London SW8 2HJ
#   Tuesday 16th June 2026
#   Tuesday 30th June 2026
#
# Source image: ~/Downloads/vectorstock_43267619.jpg (3000x1660)
#   - Watermarked; replace with purchased copy when available
#
# Fonts required:
#   - Pirata One: ~/.local/share/fonts/adventure/PirataOne-Regular.ttf
#   - Helvetica Bold: system font
#   - Install Pirata One if missing:
#       mkdir -p ~/.local/share/fonts/adventure
#       wget "https://github.com/google/fonts/raw/main/ofl/pirataone/PirataOne-Regular.ttf" \
#            -O ~/.local/share/fonts/adventure/PirataOne-Regular.ttf
#       fc-cache -f ~/.local/share/fonts

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SOURCE_IMAGE=~/Downloads/vectorstock_43267619.jpg
WIP_TAG=/tmp/wip_tag_a4.png
POSTER_BASE=/tmp/wip_poster_a4_base.png
OUTPUT="$SCRIPT_DIR/wip-poster-a4.png"

# Step 1: Main poster (2480x3508 = A4 at 300dpi)
convert -size 2480x3508 xc:'#4169E1' \
  \( "$SOURCE_IMAGE" \
     -fuzz 20% -fill '#4169E1' -opaque white \
     -resize x3508 -gravity center -extent 2480x3508 \) \
  -composite \
  -font Helvetica-Bold -fill white \
  -gravity North -pointsize 260 -annotate +0+50 "Mark Stringer" \
  -gravity North -pointsize 645 \
  -fill '#001a4d' -stroke none -font Pirata-One \
  -annotate +12+459  "You can" \
  -annotate +12+1116 "write" \
  -annotate +12+1774 "a book!" \
  -fill '#FFD700' -stroke '#1a237e' -strokewidth 10 \
  -annotate +0+447  "You can" \
  -annotate +0+1104 "write" \
  -annotate +0+1762 "a book!" \
  -stroke none \
  -fill white -font Helvetica -pointsize 74 \
  -gravity South \
  -annotate +0+868 "Work in Progress Shows" \
  -annotate +0+744 "Tuesday 16th & 30th June 2026" \
  -annotate +0+620 "9:00pm" \
  -annotate +0+496 "Cavendish Arms, Stockwell" \
  -annotate +0+372 "128 Hartington Rd, London SW8 2HJ" \
  -fill '#FFD700' -draw "polygon 1612,3508 2480,3508 2480,2604" \
  "$POSTER_BASE"

# Step 2: WORK / IN / PROGRESS tag
convert -size 595x335 xc:none \
  -alpha on \
  -font Helvetica-Bold -fill '#1a237e' -pointsize 89 \
  -gravity center \
  -annotate +0-94 "WORK" \
  -annotate +0+0  "IN" \
  -annotate +0+94 "PROGRESS" \
  -background none -rotate -45 +repage \
  "$WIP_TAG"

# Step 3: QR code (navy on yellow, links to Eventbrite)
QR_IMG=/tmp/wip_qr_a4.png
qrencode -o "$QR_IMG" -s 12 -m 4 \
  --foreground=1a237e --background=FFD700 \
  "https://www.eventbrite.com/e/you-can-write-a-book-tickets-1986985842142?aff=erellivmlt"

# Step 4: Composite WIP tag (bottom right) and QR code (bottom left)
convert "$POSTER_BASE" \
  "$WIP_TAG" -gravity NorthWest -geometry +1858+2850 -composite \
  "$QR_IMG"  -gravity SouthWest -geometry +50+50    -composite \
  "$OUTPUT"

echo "Written: $OUTPUT"
