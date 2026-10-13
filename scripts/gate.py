"""Build gate. Exits non-zero if any entry breaks a publishing rule.
Usage: python3 scripts/gate.py [--out out]   (with --out also checks rendered HTML)"""
import json, re, sys, shutil, subprocess, tempfile
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent
OFFICIAL = {"excel": ("support.microsoft.com", "learn.microsoft.com"), "sheets": ("support.google.com",)}
BANNED = [r"renewal by andersen", r"\bandersen\b", r"ship ?lab", r"window replacement", r"home improvement",
          r"\btax (advice|return|deduction)", r"\binvest(ing|ment) advice", r"\bHR advice"]
NEEDS_PREFIX = {"XLOOKUP": "_xlfn.XLOOKUP", "TEXTJOIN": "_xlfn.TEXTJOIN", "XMATCH": "_xlfn.XMATCH",
                "IFS": "_xlfn.IFS", "CONCAT": "_xlfn.CONCAT", "FILTER": "_xlfn._xlws.FILTER",
                "UNIQUE": "_xlfn.UNIQUE", "SORT": "_xlfn._xlws.SORT", "LET": "_xlfn.LET"}
REQ = ["id", "slug", "kind", "title", "meta_description", "category", "excel", "sheets", "notes", "availability", "sources"]

def norm(s): return re.sub(r"\s+", " ", s).strip()

def load():
    return json.loads((ROOT / "data/entries.json").read_text())["entries"]

def check_schema(e, errs):
    for k in REQ:
        if k not in e or e[k] in (None, "", []): errs.append(f"missing field {k}")
    if e.get("kind") not in ("shortcut", "formula"): errs.append("kind must be shortcut|formula")
    if e.get("availability") not in ("both", "excel_only", "sheets_only"): errs.append("bad availability")
    if not re.fullmatch(r"[a-z0-9-]+", e.get("slug", "")): errs.append("slug must be [a-z0-9-]")
    if len(e.get("meta_description", "")) > 160: errs.append("meta_description > 160 chars")

def apps(e):
    a = e.get("availability")
    return [p for p in ("excel", "sheets") if not (a == "excel_only" and p == "sheets") and not (a == "sheets_only" and p == "excel")]

def check_sources(e, errs):
    quotes = {"excel": [], "sheets": []}
    for s in e.get("sources", []):
        host = urlparse(s.get("url", "")).hostname or ""
        prod = s.get("product")
        if prod not in OFFICIAL or host not in OFFICIAL[prod]:
            errs.append(f"non-official source for {prod}: {host}"); continue
        p = ROOT / s.get("saved_copy", "")
        if not s.get("saved_copy") or not p.is_file():
            errs.append(f"saved copy missing: {s.get('saved_copy')}"); continue
        if not s.get("quote") or norm(s["quote"]) not in norm(p.read_text(errors="ignore")):
            errs.append(f"quote not found in saved copy {s['saved_copy']}: {s.get('quote')!r}"); continue
        quotes[prod].append(norm(s["quote"]))
    for prod in apps(e):
        if not quotes[prod]: errs.append(f"no verified official {prod} source")
    return quotes

def check_both(e, errs):
    a = e.get("availability")
    for prod in ("excel", "sheets"):
        blk = e.get(prod) or {}
        unavailable = prod not in apps(e)
        if unavailable:
            if not blk.get("unavailable_note"): errs.append(f"{prod}: excluded by availability={a} but no unavailable_note")
            continue
        if e["kind"] == "shortcut":
            for os_ in ("windows", "mac"):
                if not blk.get(os_): errs.append(f"{prod}.{os_} keys missing")
        elif not blk.get("formula", "").startswith("="): errs.append(f"{prod}.formula missing/does not start with =")

def check_shortcut_keys(e, quotes, errs):
    for prod in apps(e):
        for os_ in ("windows", "mac"):
            k = norm(e[prod].get(os_, ""))
            if k and not any(k in q for q in quotes[prod]):
                errs.append(f"{prod}.{os_} key '{k}' not shown in any quoted official line")

def check_formula_fn(e, quotes, errs):
    for prod in apps(e):
        fns = set(re.findall(r"([A-Z][A-Z0-9.]+)\(", e[prod]["formula"]))
        for fn in fns:
            if not any(fn + "(" in q for q in quotes[prod]):
                errs.append(f"{prod}: function {fn} not cited in an official {prod} quote")

def to_xlsx_formula(f):
    for fn, pre in NEEDS_PREFIX.items():
        f = re.sub(rf"(?<![A-Z_.]){fn}\(", pre + "(", f)
    return f

def recalc(formulas):
    """formulas: list of (key, cells, formula_cell, formula). Returns {key: value} via LibreOffice headless."""
    import openpyxl
    soffice = shutil.which("soffice") or shutil.which("libreoffice")
    if not soffice: raise RuntimeError("LibreOffice (soffice) not on PATH; cannot verify formulas")
    tmp = Path(tempfile.mkdtemp(prefix="sss-recalc-"))
    wb = openpyxl.Workbook(); wb.remove(wb.active)
    for i, (key, cells, fc, f) in enumerate(formulas):
        ws = wb.create_sheet(f"t{i}")
        for addr, v in cells.items(): ws[addr] = v if v != "" else None
        ws[fc] = to_xlsx_formula(f)
    src = tmp / "in" / "check.xlsx"; src.parent.mkdir(); wb.save(src)
    out = tmp / "out"; out.mkdir()
    prof = tmp / "profile"
    r = subprocess.run([soffice, f"-env:UserInstallation=file://{prof}", "--headless", "--norestore", "--nolockcheck",
                        "--calc", "--convert-to", "xlsx:Calc MS Excel 2007 XML", "--outdir", str(out), str(src)],
                       capture_output=True, text=True, timeout=180)
    res = out / "check.xlsx"
    if r.returncode or not res.exists(): raise RuntimeError(f"LibreOffice recalc failed: {r.stderr or r.stdout}")
    wb2 = openpyxl.load_workbook(res, data_only=True)
    vals = {key: wb2[f"t{i}"][fc].value for i, (key, cells, fc, f) in enumerate(formulas)}
    shutil.rmtree(tmp, ignore_errors=True)
    return vals

def same(a, b):
    if isinstance(b, (int, float)) and not isinstance(b, bool):
        try: return abs(float(a) - float(b)) < 1e-9
        except (TypeError, ValueError): return False
    return a == b

def run(out_dir=None, verbose=True):
    entries = load(); report = {}; jobs = []
    slugs = [e.get("slug") for e in entries]
    for e in entries:
        errs = []; check_schema(e, errs)
        if errs: report[e.get("slug", "?")] = {"errors": errs, "status": "FAIL"}; continue
        check_both(e, errs); q = check_sources(e, errs)
        blob = json.dumps(e).lower()
        for b in BANNED:
            if re.search(b, blob, re.I): errs.append(f"banned content: {b}")
        if e["kind"] == "shortcut":
            check_shortcut_keys(e, q, errs)
        else:
            check_formula_fn(e, q, errs)
            ex = e.get("example") or {}
            if not ex.get("cells") or "expected" not in ex or not ex.get("formula_cell"):
                errs.append("formula needs example.cells, example.formula_cell, example.expected")
            else:
                for prod in apps(e): jobs.append(((e["slug"], prod), ex["cells"], ex["formula_cell"], e[prod]["formula"]))
        report[e["slug"]] = {"errors": errs, "kind": e["kind"]}
    if len(set(slugs)) != len(slugs): report["_global"] = {"errors": ["duplicate slugs"]}
    if jobs:
        vals = recalc(jobs)
        byslug = {e["slug"]: e for e in entries}
        for (slug, prod), *_ in jobs:
            e = byslug[slug]; got = vals[(slug, prod)]; exp = e["example"]["expected"]
            r = report[slug]; r.setdefault("recalc", {})[prod] = got
            if got is None or (isinstance(got, str) and got.startswith("#")) or "_xlfn" in str(got):
                if e.get("unverified_flag"): r["recalc_status"] = "UNVERIFIED (flagged)"
                else: r["recalc_status"] = "FAILED"; r["errors"].append(f"{prod}: LibreOffice could not compute (got {got!r}); set unverified_flag to publish with a visible flag")
            elif not same(got, exp):
                r["recalc_status"] = "FAILED"; r["errors"].append(f"{prod}: recalc {got!r} != expected {exp!r}")
            else: r.setdefault("recalc_status", "VERIFIED")
    if out_dir:
        out = Path(out_dir)
        for e in entries:
            p = out / e["slug"] / "index.html"
            r = report.setdefault(e["slug"], {"errors": []})
            if not p.exists(): r["errors"].append("page not rendered"); continue
            h = p.read_text()
            for need in ("AI-made", "Excel", "Google Sheets"):
                if need not in h: r["errors"].append(f"rendered page lacks '{need}'")
            if re.search(r"<img|<svg[^>]*logo|screenshot", h, re.I): r["errors"].append("rendered page has image/logo/screenshot")
            if e["kind"] == "shortcut" and not ("Windows" in h and "Mac" in h): r["errors"].append("rendered page lacks Windows/Mac")
            if e["availability"] != "both" and "only-flag" not in h: r["errors"].append("availability flag not visible")
            if e.get("unverified_flag") and "unverified-flag" not in h: r["errors"].append("unverified flag not visible")
    ok = True
    for slug, r in report.items():
        r["status"] = "PASS" if not r["errors"] else "FAIL"; ok &= not r["errors"]
        if verbose:
            extra = f" [{r.get('recalc_status')} {r.get('recalc')}]" if r.get("recalc") else ""
            print(f"{r['status']}  {slug}{extra}")
            for x in r["errors"]: print(f"      - {x}")
    (ROOT / "gate-report.json").write_text(json.dumps(report, indent=2, default=str, ensure_ascii=False))
    return ok, report

if __name__ == "__main__":
    out = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else None
    ok, _ = run(out)
    print("GATE PASS" if ok else "GATE FAIL"); sys.exit(0 if ok else 1)
