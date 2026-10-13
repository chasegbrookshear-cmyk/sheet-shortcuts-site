# sheet-shortcuts-site
Static directory of Excel + Google Sheets shortcuts and formulas. Private preview build; not deployed.

Requirements: Python 3 with `openpyxl`, LibreOffice (`soffice`) on PATH, Google Chrome for screenshots.

    python3 scripts/gate.py                 # gate only (recalcs formulas)
    python3 scripts/build.py --out out      # gate + build to out/ (+ post-render gate)
    cd out && python3 -m http.server 8765 --bind 127.0.0.1   # local preview
    bash scripts/shots.sh                   # phone-width screenshots -> shots/
    (cd out && zip -qr ../site-preview.zip .)   # offline zip

Schema: `SCHEMA.md`. Template: `templates/base.html` + `static/style.css` (placeholder; swap via `--templates <dir>`; template vars: `$title $description $body $root $site_name`). Newsletter form is a disabled slot marked `data-newsletter-slot` in the template. Sitemap base URL is `https://example.invalid` until a domain exists (`--site-url`). `robots.txt` disallows all during preview.
