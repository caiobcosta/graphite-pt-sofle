#!/bin/sh
# Renders cheatsheet/*.html to PDF and PNG with headless Chrome and pdftoppm (poppler).
set -e
cd "$(dirname "$0")/.."
python3 scripts/gen_cheatsheet.py
python3 scripts/gen_cheatsheet.py --combo
CHROME="${CHROME:-/Applications/Google Chrome.app/Contents/MacOS/Google Chrome}"
for n in cheatsheet cheatsheet-combined; do
  "$CHROME" --headless=new --disable-gpu --no-pdf-header-footer --print-to-pdf="cheatsheet/$n.pdf" "cheatsheet/$n.html"
  pdftoppm -r 150 -png -singlefile "cheatsheet/$n.pdf" "cheatsheet/$n"
done
