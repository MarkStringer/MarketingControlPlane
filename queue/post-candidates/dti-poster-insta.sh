#!/bin/bash
# Generates a "Delivering the Impossible" poster sized for Instagram (1080x1350, 4:5).
#
# Source image: ~/Downloads/vectorstock_43267619.jpg (3000x1660)
# Fonts required:
#   - Pirata One: ~/.local/share/fonts/adventure/PirataOne-Regular.ttf
#   - Helvetica Bold: system font

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SOURCE_IMAGE=~/Downloads/vectorstock_43267619.jpg
POSTER_BASE=/tmp/dti_poster_insta_base.png
OUTPUT="$SCRIPT_DIR/dti-poster-insta.png"

convert -size 1080x1350 xc:'#4169E1' \
  \( "$SOURCE_IMAGE" \
     -fuzz 20% -fill '#4169E1' -opaque white \
     -resize x1350 -gravity center -extent 1080x1350 \) \
  -composite \
  -font Helvetica-Bold -fill white \
  -gravity North -pointsize 110 -annotate +0+20 "Mark Stringer" \
  -gravity North -pointsize 210 \
  -fill '#001a4d' -stroke none -font Pirata-One \
  -annotate +5+185 "Delivering" \
  -annotate +5+445 "the" \
  -annotate +5+660 "Impossible" \
  -fill '#FFD700' -stroke '#1a237e' -strokewidth 4 \
  -annotate +0+180 "Delivering" \
  -annotate +0+440 "the" \
  -annotate +0+655 "Impossible" \
  -stroke none \
  -fill white -font Helvetica -pointsize 38 \
  -gravity South \
  -annotate +0+120 "Delivering the Impossible — published by Springer" \
  "$OUTPUT"

echo "Written: $OUTPUT"
