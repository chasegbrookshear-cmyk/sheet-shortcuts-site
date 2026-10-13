# Bet C entry list (Growth, 2026-10-13)

- `bet-c-entries.json` v0.1: 73 entries (36 shortcuts, 37 formulas). Each has a slug, category, SEO title (60 characters or fewer), meta description (155 or fewer), keys or formulas, and sources with a local cache path.
- Shortcut keys were copied from Microsoft's Excel shortcut page (Windows and macOS tabs) and Google's Sheets shortcut page (PC and Mac sections). Both pages are cached in `sources/`. The parsed pairs are in `pairs.json`, built by `pairs.py`.
- Formula sources are the official Microsoft and Google function pages. They're cached in `sources/functions/`, with URLs in `func-sources.json`, built by `fetchfn.py`.
- `expected_result_for_recalc_check` is Growth's hand calculation. Builder's recalc check is the real gate, so any mismatch is a bug in the entry.
- Every formula uses one shared example grid, `example_grid` (A1:E7 orders and G1:G5 text).

Flags:
- REGEXEXTRACT: LibreOffice can't recalc it. Hold that page until it's checked another way.
- QUERY, ARRAYFORMULA and IMPORTRANGE are Sheets-only. Show a dash in the Excel cell, and IMPORTRANGE gets a syntax line only, with no result.
- TEXTSPLIT and SPLIT are one page because the two apps use different names. Check LibreOffice's TEXTSPLIT support.
- XLOOKUP, LET, FILTER, UNIQUE, SORT and TEXTJOIN-with-UNIQUE need LibreOffice 24.8 or later.
- Paste values: Excel opens the Paste Special dialog, so there's no made-up Mac key for the Values option.
- AutoSum has no Sheets shortcut on Google's page, so that cell is a dash.

Parked (missing an official source, or the source looks wrong):
- previous sheet: Microsoft's Mac table lists Ctrl+Page Down for both directions.
- fill right, find and replace, unhide rows and columns, group and ungroup, clear formatting: the Excel Windows tab doesn't list these.
- XMATCH: it isn't in Google's function index.
- TODAY: the result changes every day.

Ranking: the order is Growth's judgment of what desk workers commonly search for. It is not measured search volume, since there's no keyword tool on a $0 budget.

Newsletter: Kit Free. Kit's own help pages say it allows up to 10,000 subscribers, unlimited forms and landing pages, unlimited broadcasts, API access and selling digital products; emails carry Kit branding. The fallback is beehiiv Free, which allows up to 2,500 subscribers and has embed forms. It needs a free signup that Chase does himself.
