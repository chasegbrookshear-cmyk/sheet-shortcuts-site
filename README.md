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

Config (`site.config.json`, gitignored; defaults in `site.config.example.json`; env vars override): `SITE_URL` (sitemap base, default https://example.invalid), `KIT_FORM_ACTION` (Kit form POST URL) and `KIT_FORM_ID`. With `kit_form_action` empty, a disabled placeholder renders. `KIT_API_KEY` is a secret and is never written into the site. YouTube link: youtube.com/@cellshortcut. `robots.txt` disallows all and pages carry `noindex` during preview.

## Newsletter (Kit Free)
Live form posts to Kit form 10040110: `https://app.kit.com/forms/10040110/subscriptions`, field `email_address`. It's our own HTML form, with no Kit script or styling. The id/action are not secret and are committed in `site.config.example.json`, so a restore keeps them. For a local override, run `cp site.config.example.json site.config.json` (gitignored), or set the env vars `KIT_FORM_ACTION` and `KIT_FORM_ID`. Never store `KIT_API_KEY` in either file; the build doesn't render it.
Behaviour: without JS, it's a normal POST. With JS, it uses fetch (`Accept: application/json`) and shows the result inline (`aria-live="polite"`); on a network/CORS error it falls back to a normal submit. A CORS preflight returned `Access-Control-Allow-Origin: *`; the real POST response format is untested (no test signup was made).

## Lookup features (search, filters, categories)
- `data/synonyms.json`: plain-language task phrases per slug + task labels per category. `build.py` writes `out/search-index.json` (~4.5 KB gzipped) with names, synonyms, raw keys and canonical key combos (`ctrl shift v`, Mac Option = alt) per Excel/Sheets x Win/Mac.
- Header search on every page + big search on home: vanilla JS combobox/listbox, fuzzy (prefix + edit distance), key-combo aware (`ctrl+shift+l`, `cmd shift L`). Hidden without JS; the full list and category pages still work.
- Excel/Sheets and Win/Mac toggles persist in localStorage (`cs.app`, `cs.os`), filter search and hide keys on entry pages via `html[data-app|data-os]`. Default and no-JS: show all.
- Category pages at `out/c/<category>/` (noindex). Big keys at the top of shortcut pages. Copy buttons have aria-labels and an aria-live "Copied" status.
- CSS is inlined into every page at build time (static/style.css is the source).
