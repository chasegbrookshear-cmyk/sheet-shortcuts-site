# Entry schema: `data/entries.json` (Growth v0.1 format is the source of truth)

Top level: `version`, `owner`, `built`, `ranking_note`, `example_grid` (shared by every formula: `{"A1:E7": [[...]], "G1:G5": [[...]]}`; ISO date strings become real dates for recalc), `entries` (ordered by Growth's rank).

## Entry fields
| field | used for | rule enforced by `scripts/gate.py` |
|---|---|---|
| `slug` | URL `/<slug>/` | required, unique |
| `type` | `shortcut` \| `formula` | required |
| `category` | index group, category chip, Related | required |
| `name` | H1 (Designer "task in plain words") | required |
| `seo_title` | `<title>` | ≤60 chars |
| `meta` | meta description | ≤160 chars |
| `use` | lede under H1 (formulas) | optional |
| `note` | Gotchas bullet / single-app note | required when any key cell is a dash |
| `keys.excel_windows`, `keys.excel_mac`, `keys.sheets_windows`, `keys.sheets_mac` | shortcut answer table | each combo must appear verbatim (after normalisation: Spacebar=Space, ⌘=Cmd, "Semicolon (;)"=";", etc.) in the matching **platform section** of the saved official page (`sources/ms-win.txt`, `ms-mac.txt`, `g-pc.txt`, `g-mac.txt`), next to an action line sharing a word with `name` (small documented synonym list `SYN` in gate.py). `—` = no shortcut (shown as "—"). Alternatives: `A / B` (both checked). Annotations allowed: `(…)`, `, then …`, ` opens …` |
| `excel_formula`, `sheets_formula` | formula bars | start with `=`; `null` = app lacks it (shown "—"); every function used must be cited by a saved official page for that app |
| `availability` | `both` \| `sheets-only` \| `excel-only` \| `different-names` | single-app pages get the ochre note |
| `expected_result_for_recalc_check` | compared with LibreOffice | text; `a; b; c (spills)` = vertical spill, `a \| b (spills across)`, `x…` = prefix match, `(format as date)` |
| `sources[]` | `{name, url, cache}` | url host must be support.microsoft.com / learn.microsoft.com / support.google.com; `cache` file must exist in repo |
| `checked` | "Checked on" date | required |

## Statuses (data/gate-report.json)
PASS (built) · HOLD (unverifiable source/evidence, or LibreOffice lacks the function) · MISMATCH (LibreOffice result ≠ Growth expected → Growth fixes the entry; never auto-corrected) · FLAGGED (Sheets-only function LO can't compute; built only with `--include-flagged`, with a visible "Not machine-verified" note) · FAIL (schema/banned content).
Fixed holds: `regexextract` (HOLD_LIST in gate.py). Parked entries are simply not in the file.

## Designer template field mapping (design/bet-c-template.md)
| Designer slot | schema |
|---|---|
| H1 task | `name` |
| category chip / type chip | `category` / `type` |
| Answer card (shortcut) | `keys.*`; identical Win/Mac in both apps → one "Windows & Mac" row |
| Formula bar + mini grid | `excel_formula`/`sheets_formula`, `example_grid` columns referenced by the formula, result in J2 from the gate's recalc |
| Only-in-one-app flag | `availability` (+ `note`) |
| Steps | not in schema yet (Growth may add `steps: [..]`, ≤4) |
| Gotchas | `note` |
| Sources / check date | `sources[]`, `checked`; formula pages add "Recalculated with LibreOffice on <gate date>" |
| Related | same `category`, built pages only |
| Newsletter | Kit slot from config (see README) |
