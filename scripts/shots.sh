#!/usr/bin/env bash
# Phone-width (390px) screenshots of the built site using headless Chrome. Requires `make build` first.
set -e; cd "$(dirname "$0")/.."; mkdir -p shots
CH=$(command -v google-chrome || command -v chromium || command -v chromium-browser)
for p in index.html xlookup/index.html paste-values-only/index.html; do
  n=$(echo "$p" | sed 's#/index.html##;s#index.html#index#')
  "$CH" --headless=new --no-sandbox --disable-gpu --hide-scrollbars --force-device-scale-factor=2 \
    --window-size=390,1700 --screenshot="$PWD/shots/$n-390.png" "file://$PWD/out/$p" 2>/dev/null
done; ls -1 shots
