#!/bin/bash
# Generates a Work in Progress show poster for the Cavendish Arms dates.
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
#
# Generates two posters, one per date.

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SOURCE_IMAGE=~/Downloads/vectorstock_43267619.jpg
WIP_TAG=/tmp/wip_tag_text.png
POSTER_BASE=/tmp/wip_poster_base.png

generate_poster() {
  local OUTPUT="$1"

  # Step 1: Main poster
  convert -size 1000x1400 xc:'#4169E1' \
    \( "$SOURCE_IMAGE" \
       -fuzz 20% -fill '#4169E1' -opaque white \
       -resize x1400 -gravity center -extent 1000x1400 \) \
    -composite \
    -font Helvetica-Bold -fill white \
    -gravity North -pointsize 105 -annotate +0+20 "Mark Stringer" \
    -gravity North -pointsize 260 \
    -fill '#001a4d' -stroke none -font Pirata-One \
    -annotate +5+185 "You can" \
    -annotate +5+450 "write" \
    -annotate +5+715 "a book!" \
    -fill '#FFD700' -stroke '#1a237e' -strokewidth 4 \
    -annotate +0+180 "You can" \
    -annotate +0+445 "write" \
    -annotate +0+710 "a book!" \
    -stroke none \
    -fill white -font Helvetica -pointsize 30 \
    -gravity South \
    -annotate +0+350 "Work in Progress Shows" \
    -annotate +0+300 "Tuesday 16th & 30th June 2026" \
    -annotate +0+250 "9:00pm" \
    -annotate +0+200 "Cavendish Arms, Stockwell" \
    -annotate +0+150 "128 Hartington Rd, London SW8 2HJ" \
    -fill '#FFD700' -draw "polygon 650,1400 1000,1400 1000,1050" \
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

  # Step 3: Composite WIP tag
  convert "$POSTER_BASE" \
    "$WIP_TAG" -gravity NorthWest -geometry +749+1149 -composite \
    "$OUTPUT"

  echo "Written: $OUTPUT"
}

generate_poster "$SCRIPT_DIR/wip-poster-cavendish.png"
