#!/usr/bin/env bash
# Phone-width screenshots (360 and 390 px) of a built site. Usage: bash scripts/shots.sh [outdir]
set -e; cd "$(dirname "$0")/.."; OUTDIR=${1:-out}; mkdir -p shots
CH=$(command -v google-chrome || command -v chromium || command -v chromium-browser)
for w in 360 390; do for p in index.html fill-down/index.html xlookup/index.html importrange/index.html; do
  [ -f "$OUTDIR/$p" ] || continue
  n=$(echo "$p" | sed 's#/index.html##;s#index.html#index#')
  "$CH" --headless=new --no-sandbox --disable-gpu --hide-scrollbars --force-device-scale-factor=2 \
    --window-size=$w,1900 --screenshot="$PWD/shots/$n-$w.png" "file://$PWD/$OUTDIR/$p" 2>/dev/null
done; done; ls -1 shots
