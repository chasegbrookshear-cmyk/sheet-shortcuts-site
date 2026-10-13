gate:    ; python3 scripts/gate.py
build:   ; python3 scripts/build.py --out out
preview: build ; cd out && python3 -m http.server 8765 --bind 127.0.0.1
zip:     build ; rm -f dist.zip && cd out && zip -qr ../site-preview.zip .
shots:   ; bash scripts/shots.sh
