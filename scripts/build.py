"""Build the static site from data/entries.json. Runs the gate first and refuses to build on failure.
Usage: python3 scripts/build.py [--out out] [--site-url https://example.invalid] [--templates templates]"""
import json, shutil, sys, html, re, datetime
from string import Template
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import gate

ROOT = Path(__file__).resolve().parent.parent
def arg(n, d): return sys.argv[sys.argv.index(n) + 1] if n in sys.argv else d
OUT = Path(arg("--out", str(ROOT / "out")))
SITE_URL = arg("--site-url", "https://example.invalid").rstrip("/")  # no domain yet
TPL = Path(arg("--templates", str(ROOT / "templates")))
SITE = "Sheet Shortcuts"
e_ = lambda s: html.escape(str(s), quote=True)
APP = {"excel": "Excel", "sheets": "Google Sheets"}

def slugify(s): return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")

def page(title, desc, body, root):
    return Template((TPL / "base.html").read_text()).substitute(title=e_(title), description=e_(desc), body=body, root=root, site_name=SITE)

def keys(k): return " ".join(f"<kbd>{e_(p.strip())}</kbd>" if p.strip() not in ("+",) else "+" for p in re.split(r"(\+)", k)) if k else ""

def app_card(e, prod, avail):
    blk = e[prod]
    if prod not in avail:
        return f'<div class="card"><h3>{APP[prod]}</h3><span class="flag only-flag">Not available in {APP[prod]}</span><p>{e_(blk.get("unavailable_note",""))}</p></div>'
    if e["kind"] == "shortcut":
        rows = "".join(f"<tr><td>{os_}</td><td>{keys(blk[k])}</td></tr>" for os_, k in (("Windows", "windows"), ("Mac", "mac")))
        same = '<p class="lede" style="font-size:.85rem">Same keys on Windows and Mac.</p>' if blk["windows"] == blk["mac"] else ""
        return f'<div class="card"><h3>{APP[prod]}</h3><table class="keys">{rows}</table>{same}</div>'
    return f'<div class="card"><h3>{APP[prod]} <small>(Windows &amp; Mac)</small></h3><pre>{e_(blk["formula"])}</pre></div>'

def example_html(e, rep):
    ex = e["example"]; cells = ex["cells"]
    cols = sorted({re.match(r"[A-Z]+", a).group() for a in cells}); rows = sorted({int(re.search(r"\d+", a).group()) for a in cells})
    t = "<tr><th></th>" + "".join(f"<th>{c}</th>" for c in cols) + "</tr>"
    for r in rows: t += f"<tr><th>{r}</th>" + "".join(f"<td>{e_(cells.get(f'{c}{r}', ''))}</td>" for c in cols) + "</tr>"
    st = rep.get("recalc_status", "")
    flag = (f'<span class="flag ok">✓ Recalculated by code: {e_(ex["formula_cell"])} = {e_(ex["expected"])}</span>' if st == "VERIFIED"
            else '<span class="flag unverified-flag">⚠ Not machine-verified — LibreOffice cannot compute this function</span>')
    return (f'<h2>Example</h2><p>Put this in <code>{e_(ex["formula_cell"])}</code>:</p><pre>{e_(e["excel"]["formula"])}</pre>'
            f'<table class="cells">{t}</table><p>Expected result: <code>{e_(ex["expected"])}</code>. {e_(ex.get("explain",""))}</p>{flag}')

def entry_html(e, rep):
    avail = gate.apps(e)
    flags = ""
    if e["availability"] != "both":
        only = "Excel only" if e["availability"] == "excel_only" else "Google Sheets only"
        flags = f'<span class="flag only-flag">{only}</span>'
    if e.get("unverified_flag"): flags += '<span class="flag unverified-flag">Unverified result</span>'
    srcs = "".join(f'<li><a href="{e_(s["url"])}" rel="nofollow noopener">{APP[s["product"]]}: official help page</a><blockquote>“{e_(s["quote"])}”</blockquote></li>' for s in e["sources"])
    body = (f'<p><a href="../category/{slugify(e["category"])}/index.html">{e_(e["category"])}</a> · {"Keyboard shortcut" if e["kind"]=="shortcut" else "Formula"}</p>'
            f'<h1>{e_(e["title"])}</h1><p class="lede">{e_(e["meta_description"])}</p>{flags}'
            f'<div class="grid">{app_card(e,"excel",avail)}{app_card(e,"sheets",avail)}</div>'
            + (example_html(e, rep) if e["kind"] == "formula" else "")
            + f'<h2>Notes</h2><p>{e_(e["notes"])}</p><h2>Sources</h2><ul class="sources">{srcs}</ul>')
    return page(e["title"], e["meta_description"], body, "..")

def listing(es, root):
    return '<ul class="list">' + "".join(f'<li><a href="{root}/{x["slug"]}/index.html">{e_(x["title"])}</a><span class="k">{x["kind"]}</span></li>' for x in es) + "</ul>"

def main():
    ok, rep = gate.run(verbose=True)
    if not ok: print("BUILD ABORTED: gate failed"); sys.exit(1)
    entries = gate.load()
    if OUT.exists(): shutil.rmtree(OUT)
    shutil.copytree(ROOT / "static", OUT / "static")
    urls = ["/"]; cats = {}
    for e in entries:
        d = OUT / e["slug"]; d.mkdir(parents=True)
        (d / "index.html").write_text(entry_html(e, rep[e["slug"]])); urls.append(f"/{e['slug']}/")
        cats.setdefault(e["category"], []).append(e)
    for c, es in cats.items():
        d = OUT / "category" / slugify(c); d.mkdir(parents=True)
        (d / "index.html").write_text(page(c, f"{c} shortcuts and formulas for Excel and Google Sheets.", f"<h1>{e_(c)}</h1>{listing(es,'../..')}", "../..").replace('href="../../../', 'href="../../'))
        urls.append(f"/category/{slugify(c)}/")
    catlinks = '<div class="cats">' + "".join(f'<a href="category/{slugify(c)}/index.html">{e_(c)} ({len(v)})</a>' for c, v in sorted(cats.items())) + "</div>"
    body = (f'<h1>Spreadsheet shortcuts &amp; formulas, Excel and Google Sheets side by side</h1>'
            f'<p class="lede">Every page shows both apps, Windows and Mac keys, cites the official help page, and formulas are recalculated by code.</p>'
            f'{catlinks}<h2>Shortcuts</h2>{listing([x for x in entries if x["kind"]=="shortcut"],".")}<h2>Formulas</h2>{listing([x for x in entries if x["kind"]=="formula"],".")}')
    (OUT / "index.html").write_text(page("Excel & Google Sheets shortcuts and formulas", "Side-by-side keyboard shortcuts and formulas for Excel and Google Sheets.", body, "."))
    today = datetime.date.today().isoformat()
    (OUT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
        "".join(f"  <url><loc>{SITE_URL}{u}</loc><lastmod>{today}</lastmod></url>\n" for u in urls) + "</urlset>\n")
    (OUT / "robots.txt").write_text("User-agent: *\nDisallow: /\n")  # private preview; flip at launch
    idx = [{"s": x["slug"], "t": x["title"], "c": x["category"], "k": x["kind"],
            "x": " ".join(str(v) for p in ("excel", "sheets") for v in x[p].values())} for x in entries]
    (OUT / "search.json").write_text(json.dumps(idx, ensure_ascii=False))
    ok2, _ = gate.run(out_dir=OUT, verbose=False)
    if not ok2: print("BUILD FAILED: rendered-output gate failed, see gate-report.json"); sys.exit(1)
    print(f"Built {len(entries)} pages + {len(cats)} categories -> {OUT}")

if __name__ == "__main__": main()
