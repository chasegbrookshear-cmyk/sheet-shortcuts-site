# Bet C: page template + index layout (Designer v0.1, Oct 13 2026)
Sheet Shift paper-and-mono look, mobile first. Field names are placeholders until Builder's schema lands; I'll remap, not redesign.

## Tokens
- Paper `#F7F5F0`, ink `#1F2430`, grid lines `#D6D1C4`, header fill `#2B2F3A` / header text `#F7F5F0`, muted `#6F6A5E`.
- One accent per category (burnt orange `#C2410C`, blue `#1D6FA3`, violet `#7A4FA0`, rose `#B83250`, ochre `#9A6700`). No greens.
- Fonts: Inter (UI, headings), JetBrains Mono (keys, formulas, cells). Self-hosted woff2, OFL, `font-display: swap`.
- Type: body 17px/1.55, H1 28px (mobile) / 36px (≥720px). Mono 15px mobile, 16px desktop.
- Max content width 720px. Side padding 16px mobile, 24px ≥720px. Tap targets ≥44px.
- Banned: brand logos, app UI screenshots, ribbon, "fx" glyph, sheet tabs, green selection colors.

## Page template (one shortcut or formula)
1. **Top bar**: site name (Inter SemiBold), link to index. No hamburger.
2. (Removed 2026-10-13 at owner request: no AI label strip.)
3. **H1** = task in plain words ("Insert today's date"). Under it, category chip in the accent + type chip (`SHORTCUT` or `FORMULA`).
4. **Answer card** (the reason people came): white card, 2px ink border, radius 12.
   - Shortcut: a 2-column table, columns `Excel` and `Google Sheets`; rows `Windows` and `Mac`. Keys drawn as mono `<kbd>` chips (paper fill, 1px `#D6D1C4` border, 2px bottom shadow). Identical cells merge into one row labelled "Windows & Mac".
   - On phones <480px the table stacks: one block per app, two key rows each. No horizontal scroll ever.
   - Formula: mono formula bar look (white, 2px ink border, `=` pill), copy button right. Below it a mini grid (≤7 rows × ≤4 cols (cap 7x4, approved by Designer 2026-10-13), row-number gutter, header row in `#2B2F3A`). Result cell: 3px accent border, 14% tint, tag `RESULT ✓ recalculated`. Mini grid scrolls inside its own box on phone; page body never does.
5. **Only-in-one-app flag** (when it applies): ochre-bordered note, "Google Sheets only. Excel has no equivalent function; closest option: …" or "No equivalent" in plain text. Never a faked formula in the other column; that cell shows "—" with the note.
6. **Steps** (optional, ≤4 short numbered lines), then **Gotchas** (≤3 bullets).
7. **Sources** (required): "Checked against" + link(s) to Microsoft/Google official shortcut pages, and the check date. Formula pages show "Recalculated with LibreOffice on <date>". No source field = build fails (Builder's call how).
8. **Related**: 3–5 links to sibling pages in the same category, as plain text rows.
9. **Newsletter box**: one email field + button, paper fill, 1px rule. Once per page, after Related. No popups.
10. **Footer**: "Not affiliated with Microsoft or Google", no tax/HR/investing advice line.

## Index layout
- Header: site name, one-line promise, search input (client-side filter over titles, no JS framework).
- Filter chips row (scrolls sideways on phone): All, Shortcuts, Formulas, Excel only, Sheets only, then categories.
- List, not tile wall: each entry is a row styled like a sheet row, with muted row number, title in Inter, type chip, and a mono key preview on ≥720px (hidden on phone to keep rows one line).
- Grouped by category with a sticky `#2B2F3A` category header band in the accent left border.
- Newsletter box after the first group and in the footer, nowhere else.

## Mobile checks before I PASS a build
- 360px wide: no horizontal page scroll, key table stacks, answer card in first screen.
- Contrast ≥4.5:1 for all text (accents on white pass, computed earlier for Sheet Shift).
- Lighthouse mobile accessibility ≥95, no layout shift from fonts.
