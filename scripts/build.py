"""Gate + build. Usage:
  python3 scripts/build.py [--set milestone|all] [--out out] [--include-flagged]
Config: site.config.json (gitignored; copy site.config.example.json) and env vars override it:
  SITE_URL, KIT_FORM_ACTION (Kit form POST URL), KIT_FORM_ID. KIT_API_KEY is never written into output."""
import json, os, re, sys, shutil, html, datetime
from string import Template
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent)); import gate

ROOT = Path(__file__).resolve().parent.parent
def arg(n, d): return sys.argv[sys.argv.index(n) + 1] if n in sys.argv else d
OUT = Path(arg("--out", str(ROOT / "out"))); SET = arg("--set", "all"); TPL = Path(arg("--templates", str(ROOT / "templates")))
cfg = json.loads((ROOT / "site.config.example.json").read_text())
if (ROOT / "site.config.json").exists(): cfg.update(json.loads((ROOT / "site.config.json").read_text()))
for k in ("site_url", "kit_form_action", "kit_form_id"):
    if os.environ.get(k.upper()): cfg[k] = os.environ[k.upper()]
if os.environ.get("KIT_API_KEY") or cfg.get("kit_api_key"):
    print("note: KIT_API_KEY is set but is a secret; it is NOT rendered into the static site (embed forms need only the form action/id).")
E = lambda s: html.escape(str(s), quote=True)
ACCENTS = ["#C2410C", "#1D6FA3", "#7A4FA0", "#B83250"]
def slugify(s): return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")

def page(title, desc, body, root, footer_extra=""):
    return Template((TPL / "base.html").read_text()).substitute(title=E(title), description=E(desc), body=body, root=root,
        site_name=E(cfg["site_name"]), youtube_url=E(cfg["youtube_url"]), footer_extra=footer_extra)

NL = [0]
def newsletter():
    NL[0] += 1; i = "" if NL[0] == 1 else f"-{NL[0]}"; nid, did = f"nl-email{i}", f"nl-status{i}"
    act = cfg.get("kit_form_action", "").strip()
    if act.startswith("https://"):
        fid = E(cfg.get("kit_form_id", ""))
        return (f'<section class="nl" data-newsletter="kit" data-kit-form-id="{fid}"><h2>One new shortcut a week</h2>'
                f'<form class="nl-form" method="post" action="{E(act)}"><label for="{nid}">Email address</label>'
                f'<input id="{nid}" type="email" name="email_address" required autocomplete="email" placeholder="you@example.com">'
                f'<button type="submit">Subscribe</button></form>'
                f'<p class="nl-result" role="status" aria-live="polite"></p><p class="small">Free. Unsubscribe anytime.</p></section>')
    return ('<section class="nl" data-newsletter="kit-placeholder"><h2>One new shortcut a week</h2>'
            '<!-- Kit Free form slot: set KIT_FORM_ACTION (+ KIT_FORM_ID) at build time to enable. -->'
            f'<form onsubmit="return false"><label for="{nid}">Email address</label><input id="{nid}" type="email" placeholder="you@example.com" aria-describedby="{did}" disabled>'
            f'<button type="submit" disabled aria-describedby="{did}">Coming soon</button></form><p class="small" id="{did}">Newsletter not live yet.</p></section>')

def keys_html(v):
    if gate.is_dash(v): return '<span class="dash" aria-label="none">—</span>'
    out = []
    for part in re.split(r"\s+/\s+", v):
        m = re.match(r"^(.*?)((?:\s+\(|,\s*then\b|\s+opens\b).*)?$", part); combo, rest = m.group(1), m.group(2) or ""
        if re.search(r",\s", combo):  # ribbon sequence: Alt+H, A, C
            chips = '<span class="plus">,</span> '.join(chip(c) for c in combo.split(", "))
        else: chips = chip(combo)
        out.append(chips + (f' <span class="ann">{E(rest.strip())}</span>' if rest else ""))
    return ' <span class="plus">/</span> '.join(out)
def chip(c):
    toks = re.findall(r"\+\+$|[^+]+|\+(?=$)", c)
    toks = [t if t != "++" else "+" for t in toks]
    if c.endswith("++"): toks = c[:-2].split("+") + ["+"]
    return '<span class="plus">+</span>'.join(f"<kbd>{E(t.strip())}</kbd>" for t in toks if t.strip())

def shortcut_card(e):
    k = e["keys"]; rows = []
    same = k["excel_windows"] == k["excel_mac"] and k["sheets_windows"] == k["sheets_mac"]
    plats = [("Windows &amp; Mac", "windows")] if same else [("Windows", "windows"), ("Mac", "mac")]
    t = "".join(f'<tr><th scope="row">{lab}</th><td>{keys_html(k["excel_"+p])}</td><td>{keys_html(k["sheets_"+p])}</td></tr>' for lab, p in plats)
    table = f'<table class="keys"><thead><tr><th></th><th scope="col">Excel</th><th scope="col">Google Sheets</th></tr></thead><tbody>{t}</tbody></table>'
    stack = '<div class="stack">' + "".join(f'<h2>{app}</h2>' + "".join(f'<div class="row"><span class="os">{lab}</span><span>{keys_html(k[pre+p])}</span></div>' for lab, p in plats)
                                         for app, pre in (("Excel", "excel_"), ("Google Sheets", "sheets_"))) + "</div>"
    return f'<div class="card">{table}{stack}</div>'

def refs(f):
    cols = set()
    for a, b, c, d in re.findall(r"\b([A-G])(\d)(?::([A-G])(\d))?", f or ""):
        c = c or a; cols |= {chr(x) for x in range(ord(a), ord(c) + 1)}
    return sorted(cols)

def formula_card(e, rep, meta):
    parts = []; avail = e["availability"]
    for app, lab in (("excel", "Excel"), ("sheets", "Google Sheets")):
        f = e.get(f"{app}_formula"); fid = f"f-{app}"
        parts.append(f'<div class="app-label">{lab}</div>')
        if gate.is_dash(f): parts.append('<div class="fbar"><span class="dash">—</span></div>'); continue
        parts.append(f'<div class="fbar"><span class="eq">=</span><code id="{fid}">{E(f[1:])}</code><button class="copy" data-copy="{fid}" type="button">Copy</button></div>')
    rc = rep.get("recalc", {}); app = "excel" if rc.get("excel", {}).get("computed") else "sheets"
    res = rc.get(app, {}); verified = res.get("computed") and res.get("matches_expected")
    cells = gate.grid_cells(meta); cols = refs(e.get("excel_formula") or e.get("sheets_formula"))[:3] or ["A"]
    vals = [x.strip() for x in str(res.get("result", "")).split(";")] if verified else []
    head = "<tr><th></th>" + "".join(f"<th>{c}</th>" for c in cols) + "<th>J</th></tr>"
    body = ""
    nrows = 7 if any(c in "ABCDE" for c in cols) else 5
    for r in range(1, nrows + 1):
        def cv(c):
            v = cells.get(f"{c}{r}", ""); return v.date().isoformat() if isinstance(v, datetime.datetime) else v
        rv = "Result" if r == 1 else (vals[r - 2] if 0 <= r - 2 < len(vals) else "")
        cls = ' class="result"' if (r >= 2 and rv != "" and verified) else ""
        body += f"<tr><th>{r}</th>" + "".join(f"<td>{E(cv(c))}</td>" for c in cols) + f"<td{cls}>{E(rv)}</td></tr>"
    tag = (f'<span class="rtag">RESULT ✓ recalculated</span>' if verified else
           '<span class="only"><strong>Not machine-verified.</strong> LibreOffice cannot compute this function, so no result is shown.</span>')
    return (f'<div class="card">{"".join(parts)}<div class="gridbox"><table class="mini"><thead>{head}</thead><tbody>{body}</tbody></table></div>'
            f'<p style="margin:6px 0 0;font-size:14px">Formula in <code>J2</code>.</p>{tag}</div>')

def only_note(e):
    a = e.get("availability")
    if e["type"] == "formula" and a == "sheets-only":
        return f'<div class="only"><strong>Google Sheets only.</strong> Excel has no equivalent function of the same name, so the Excel cell shows “—”.</div>'
    if e["type"] == "formula" and a == "excel-only":
        return f'<div class="only"><strong>Excel only.</strong> Google Sheets has no equivalent function, so the Sheets cell shows “—”.</div>'
    if e["type"] == "shortcut":
        for app, lab in (("excel", "Excel"), ("sheets", "Google Sheets")):
            if all(gate.is_dash(e["keys"][f"{app}_{p}"]) for p in ("windows", "mac")):
                return f'<div class="only"><strong>No {lab} shortcut.</strong> {E(e.get("note",""))}</div>'
    return ""

def entry_page(e, rep, meta, published, accent):
    chips = (f'<div class="chips"><a class="chip" style="color:{accent}" href="../index.html#{slugify(e["category"])}">{E(e["category"])}</a>'
             f'<span class="chip type">{e["type"].upper()}</span></div>')
    card = shortcut_card(e) if e["type"] == "shortcut" else formula_card(e, rep, meta)
    got = f'<h2>Gotchas</h2><ul class="gotchas"><li>{E(e["note"])}</li></ul>' if e.get("note") and not only_note(e).count(E(e["note"])) else ""
    srcs = "".join(f'<li><a href="{E(s["url"])}" rel="noopener nofollow">{E(s["name"])}</a></li>' for s in e["sources"])
    if e["type"] == "shortcut":
        ev = "".join(f'<li>“{E(x["quote"][:160])}”</li>' for v in (rep.get("evidence") or {}).values() for x in (v or []))
        extra = f'<details><summary>Quoted lines from the saved official pages</summary><ul>{ev}</ul></details>'
        when = f'Checked on {E(e["checked"])}.'
    else:
        extra = ""; when = f'Checked on {E(e["checked"])}. Recalculated with LibreOffice on {E(rep["_date"])}.'
    sib = [x for x in published if x["category"] == e["category"] and x["slug"] != e["slug"]][:5]
    rel = ('<h2>Related</h2><div class="related">' + "".join(f'<a href="../{x["slug"]}/index.html">{E(x["name"])}</a>' for x in sib) + "</div>") if sib else ""
    use = f'<p class="lede">{E(e["use"])}</p>' if e.get("use") else ""
    body = (f'<p class="ai-strip">AI-made: written with AI. Shortcuts checked against official pages; formulas recalculated in code.</p>'
            f'<h1>{E(e["name"])}</h1>{chips}{use}{card}{only_note(e)}{got}'
            f'<section class="sources"><h2>Sources</h2><p>Checked against:</p><ul>{srcs}</ul><p class="date">{when}</p>{extra}</section>'
            f'{rel}{newsletter()}')
    return page(e["seo_title"], e["meta"], body, "..")

def preview(e):
    if e["type"] == "shortcut": return f'{e["keys"]["excel_windows"]} · {e["keys"]["sheets_windows"]}'
    return e.get("excel_formula") or e.get("sheets_formula") or ""

def main():
    ok, rep, stamp = gate.run(verbose=False)
    meta = gate.load(); entries = meta["entries"]
    allowed = {"PASS"} | ({"FLAGGED"} if "--include-flagged" in sys.argv else set())
    eligible = [e for e in entries if rep[e["slug"]]["status"] in allowed and e.get("status", "v1") == "v1"]
    if SET == "milestone":
        want = json.loads((ROOT / "data/publish.json").read_text())["milestone"]
        if not ok: print("BUILD ABORTED: milestone set has non-PASS entries:", stamp["publish_blocked"]); sys.exit(1)
        eligible = [e for e in eligible if e["slug"] in want]
    held = [(e["slug"], rep[e["slug"]]["status"]) for e in entries if e not in eligible]
    if OUT.exists(): shutil.rmtree(OUT)
    shutil.copytree(ROOT / "static", OUT / "static")
    cats = list(dict.fromkeys(e["category"] for e in eligible)); acc = {c: ("#9A6700" if c == "Sheets-only" else ACCENTS[i % 4]) for i, c in enumerate(cats)}
    for e in eligible:
        NL[0] = 0
        r = dict(rep[e["slug"]]); r["_date"] = stamp["date"]
        d = OUT / e["slug"]; d.mkdir(parents=True); (d / "index.html").write_text(entry_page(e, r, meta, eligible, acc[e["category"]]))
    # index
    av = lambda e: ("sheets-only" if e.get("availability") == "sheets-only" else "excel-only" if e.get("availability") == "excel-only" else "both")
    filt = [("all", "All"), ("shortcut", "Shortcuts"), ("formula", "Formulas"), ("excel-only", "Excel only"), ("sheets-only", "Sheets only")] + [(slugify(c), c) for c in cats]
    chips = '<div class="filters" role="toolbar" aria-label="Filter">' + "".join(f'<button type="button" data-f="{f}" aria-pressed="{str(f=="all").lower()}">{E(l)}</button>' for f, l in filt) + "</div>"
    NL[0] = 0; groups = ""; n = 0
    for gi, c in enumerate(cats):
        rows = ""
        for e in [x for x in eligible if x["category"] == c]:
            n += 1
            s = " ".join([e["name"], c, e["type"], preview(e)])
            rows += (f'<li data-type="{e["type"]}" data-avail="{av(e)}" data-cat="{slugify(c)}" data-s="{E(s)}"><a href="{e["slug"]}/index.html">'
                     f'<span class="n">{n}</span><span class="t">{E(e["name"])}</span><span class="kp">{E(preview(e))}</span>'
                     f'<span class="chip type">{e["type"][:4].upper() if e["type"]=="formula" else "KEYS"}</span></a></li>')
        groups += f'<section class="group" id="{slugify(c)}"><h2 style="border-left-color:{acc[c]}">{E(c)}</h2><ul class="rows">{rows}</ul></section>'
        if gi == 0: groups += newsletter()
    body = (f'<p class="ai-strip">AI-made: written with AI. Shortcuts checked against official pages; formulas recalculated in code.</p>'
            f'<h1>Excel &amp; Google Sheets, side by side</h1><p class="promise">Every shortcut for Windows and Mac, every formula recalculated before it’s published.</p>'
            f'<input id="q" type="search" placeholder="Search {len(eligible)} shortcuts &amp; formulas" aria-label="Search">{chips}{groups}')
    (OUT / "index.html").write_text(page(f'{cfg["site_name"]}: Excel and Google Sheets shortcuts and formulas', "Excel and Google Sheets keyboard shortcuts and formulas side by side, Windows and Mac.", body, ".", newsletter()))
    base = cfg["site_url"].rstrip("/")
    (OUT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
        "".join(f"  <url><loc>{base}/{u}</loc><lastmod>{stamp['date']}</lastmod></url>\n" for u in [""] + [f'{e["slug"]}/' for e in eligible]) + "</urlset>\n")
    (OUT / "robots.txt").write_text("User-agent: *\nDisallow: /\n")
    (OUT / "search.json").write_text(json.dumps([{"s": e["slug"], "t": e["name"], "c": e["category"], "k": e["type"], "x": preview(e)} for e in eligible], ensure_ascii=False))
    # rendered-output gate
    bad = []
    for e in eligible:
        h = (OUT / e["slug"] / "index.html").read_text()
        for need in ("AI-made", "Excel", "Google Sheets", "Checked against"):
            if need not in h: bad.append(f'{e["slug"]}: missing {need}')
        if h.count("AI-made") < 2: bad.append(f'{e["slug"]}: AI label must appear above title and in footer')
        if re.search(r"<img|logo|screenshot", h, re.I): bad.append(f'{e["slug"]}: image/logo')
        if e["type"] == "formula" and rep[e["slug"]]["status"] == "PASS" and "RESULT ✓ recalculated" not in h: bad.append(f'{e["slug"]}: no recalculated result')
    if bad: print("BUILD FAILED (render gate):", *bad, sep="\n  "); sys.exit(1)
    print(f"Built {len(eligible)} pages ({SET}) -> {OUT}. Gate counts: {stamp['counts']}. Not built: {len(held)}")
    for s, st in held: print(f"  {st:8} {s}")

if __name__ == "__main__": main()
