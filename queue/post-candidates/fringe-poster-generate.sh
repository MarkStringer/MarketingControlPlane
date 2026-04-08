#!/bin/bash
# Generates fringe-poster.png
#
# Source image: ~/Downloads/vectorstock_43267619.jpg (3000x1660)
#   - Watermarked version; replace with purchased copy when available
#   - Scaled to fill 1400px height, clipped at sides (no distortion)
#   - White areas replaced with royal blue (#4169E1)
#
# Fonts required:
#   - Pirata One (title): ~/.local/share/fonts/adventure/PirataOne-Regular.ttf
#   - Helvetica Bold (name + details): system font
#   - Install Pirata One:
#       mkdir -p ~/.local/share/fonts/adventure
#       wget "https://github.com/google/fonts/raw/main/ofl/pirataone/PirataOne-Regular.ttf" \
#            -O ~/.local/share/fonts/adventure/PirataOne-Regular.ttf
#       fc-cache -f ~/.local/share/fonts
#
# Output: queue/post-candidates/fringe-poster.png (1000x1400)

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SOURCE_IMAGE=~/Downloads/vectorstock_43267619.jpg
OUTPUT="$SCRIPT_DIR/fringe-poster.png"
WIP_TAG=/tmp/wip_tag_text.png
POSTER_BASE=/tmp/fringe_poster_base.png

# Step 1: Build main poster with image, name, title, details, and yellow triangle
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
  -annotate +0+300 "Edinburgh Festival Fringe 2026" \
  -annotate +0+250 "17-29 August (not Sundays)" \
  -annotate +0+200 "Greenside @ Riddles Court, Clover Studio" \
  -annotate +0+150 "18:20  |  50 minutes" \
  -annotate +0+100 "Tickets: £10 / £5 concession" \
  -fill '#FFD700' -draw "polygon 650,1400 1000,1400 1000,1050" \
  "$POSTER_BASE"

# Step 2: Build WORK / IN / PROGRESS tag — centred text on transparent bg, rotated -45°
convert -size 240x135 xc:none \
  -alpha on \
  -font Helvetica-Bold -fill '#1a237e' -pointsize 36 \
  -gravity center \
  -annotate +0-38 "WORK" \
  -annotate +0+0 "IN" \
  -annotate +0+38 "PROGRESS" \
  -background none -rotate -45 +repage \
  "$WIP_TAG"

# Step 3: Composite WIP tag onto poster (centred on triangle at ~883,1283)
convert "$POSTER_BASE" \
  "$WIP_TAG" -gravity NorthWest -geometry +749+1149 -composite \
  "$OUTPUT"

echo "Poster written to $OUTPUT"
