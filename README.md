# sheet-shortcuts-site
Static directory of Excel + Google Sheets shortcuts and formulas. Private preview; not deployed, host-agnostic (plain files).

Needs: Python 3 + `openpyxl`, LibreOffice (`soffice`, 24.8+; box has 25.2.3), Google Chrome for screenshots.

    python3 scripts/gate.py                              # gate all 73; exit 1 if a milestone page isn't PASS
    python3 scripts/build.py --set milestone --out out-milestone   # 10-page milestone
    python3 scripts/build.py --set all --out out         # every PASS page (add --include-flagged for Sheets-only unverified)
    cd out && python3 -m http.server 8765 --bind 127.0.0.1  # local preview
    bash scripts/shots.sh out                            # 360/390px screenshots -> shots/
    python3 -m zipfile -c site-preview.zip out/          # offline zip

Data: `data/entries.json` (Growth), `data/publish.json` (milestone list), report `data/gate-report.json`. Schema + template mapping: `SCHEMA.md`. Design spec: `design/bet-c-template.md`. Growth's tooling/README: `growth/`.
Template: `templates/base.html`, `static/style.css`, `static/site.js`; fonts self-hosted in `static/fonts` (OFL).

Config (`site.config.json`, gitignored; defaults in `site.config.example.json`; env vars override): `SITE_URL` (sitemap base, default https://example.invalid), `KIT_FORM_ACTION` (Kit form POST URL) and `KIT_FORM_ID`. With none set, a disabled newsletter placeholder renders. `KIT_API_KEY` is a secret and is never written into the site. YouTube link: youtube.com/@cellshortcut. `robots.txt` disallows all and pages carry `noindex` during preview.
