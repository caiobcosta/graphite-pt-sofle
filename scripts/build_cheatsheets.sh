#!/bin/sh
# Renders the cheat sheets to HTML, PDF and PNG with headless Chrome and pdftoppm (poppler).
# Extra arguments go to gen_cheatsheet.py (--angle=N, --scale=F, --overrides=FILE); OUTDIR picks the folder.
set -e
cd "$(dirname "$0")/.."
OUTDIR="${OUTDIR:-cheatsheet}"
python3 scripts/gen_cheatsheet.py --outdir="$OUTDIR" "$@"
python3 scripts/gen_cheatsheet.py --combo --outdir="$OUTDIR" "$@"
CHROME="${CHROME:-/Applications/Google Chrome.app/Contents/MacOS/Google Chrome}"
for n in cheatsheet cheatsheet-combined; do
  "$CHROME" --headless=new --disable-gpu --no-pdf-header-footer --print-to-pdf="$OUTDIR/$n.pdf" "$OUTDIR/$n.html" 2>/dev/null
  pdftoppm -r 150 -png -singlefile "$OUTDIR/$n.pdf" "$OUTDIR/$n"
done
