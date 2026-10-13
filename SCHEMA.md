# Entry schema (`data/entries.json`)

One file, `{"entries": [ ... ]}`. Each entry becomes one page at `/<slug>/`. The gate (`python3 scripts/gate.py`) rejects any entry that breaks a rule below, and `scripts/build.py` will not build while any entry fails.

| field | type | rules |
|---|---|---|
| `id` | string | unique, e.g. `s006` (shortcut) / `f006` (formula) |
| `slug` | string | `[a-z0-9-]`, unique, becomes the URL |
| `kind` | `shortcut` \| `formula` | |
| `title` | string | page H1 |
| `meta_description` | string | ≤160 chars |
| `category` | string | free text; one category page per distinct value |
| `excel` | object | shortcut: `{"windows": "Ctrl+D", "mac": "Cmd+D"}` · formula: `{"formula": "=SUMIFS(...)"}` |
| `sheets` | object | same shape as `excel` |
| `notes` | string | plain text; no tax, HR or investing advice |
| `example` | object | **formulas only**: `{"cells": {"A1": "Fruit", "B2": 1.2, ...}, "formula_cell": "D2", "expected": 0.5, "explain": "..."}`. Empty string = blank cell. `expected` is a number or exact string |
| `availability` | `both` \| `excel_only` \| `sheets_only` | when not `both`, the missing app's block must have `"unavailable_note"`; the page shows a visible “… only” flag |
| `sources` | list | each: `{"url", "product": "excel"\|"sheets", "saved_copy": "sources/<slug>/<file>.txt", "quote"}` |
| `unverified_flag` | bool, optional | only for formulas LibreOffice cannot compute; publishes with a visible “Not machine-verified” flag. Without it, an uncomputable formula fails |

## What the gate enforces
- Both apps on every page; shortcuts need Windows **and** Mac keys for each available app (repeat the same value if they're identical).
- Sources: Excel sources must be on `support.microsoft.com` / `learn.microsoft.com`; Sheets on `support.google.com`. The `saved_copy` file must exist in the repo and contain the `quote` (whitespace-insensitive).
- Shortcuts: every key string (e.g. `Ctrl + Shift + v`) must appear **exactly as written** inside one of that app's quotes. So copy key text from the official page verbatim (Google uses `Ctrl + d`, `⌘ + d`; Microsoft uses `Ctrl+D`, `Cmd+D`).
- Formulas: each function name used must appear as `NAME(` in an official quote for that app; the example is written to an xlsx, recalculated with LibreOffice headless, and must equal `expected`. New Excel functions get `_xlfn.` prefixes automatically (see `NEEDS_PREFIX` in `scripts/gate.py`; add any new ones there).
- Banned content patterns (brand/home-improvement/advice terms), and on rendered output: an “AI-made” label, both app names, no `<img>`/logos/screenshots.

## Adding an entry
1. Save the official page as text: `curl -sL <url>`, strip tags (see how `sources/*/` files look), save to `sources/<slug>/<name>.txt`.
2. Copy a quote line from that file containing the keys / syntax.
3. Add the JSON entry, run `python3 scripts/gate.py`, fix anything listed.
