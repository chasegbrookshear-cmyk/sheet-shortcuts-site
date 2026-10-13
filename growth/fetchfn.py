import re,html,json,subprocess
F="VLOOKUP XLOOKUP INDEX MATCH XMATCH SUMIF SUMIFS COUNTIF COUNTIFS AVERAGEIFS IF IFS IFERROR FILTER UNIQUE SORT TEXTJOIN CONCATENATE TRIM LEFT MID LEN SUBSTITUTE TEXT DATEDIF NETWORKDAYS EOMONTH TODAY ROUND SUMPRODUCT LET QUERY ARRAYFORMULA IMPORTRANGE SPLIT TEXTSPLIT REGEXEXTRACT PROPER COUNTA".split()
ms=open('sources/ms-excel-functions.html',errors='ignore').read()
MS={n:s for s,n in re.findall(r'href="functions/([^"]+)"[^>]*>([A-Z0-9.]+)<',ms)}
g=open('sources/g-sheets-functions.html',errors='ignore').read()
G={}
for row in re.findall(r'(?s)<tr data-category="[^"]*">(.*?)</tr>',g):
    c=re.findall(r'(?s)<td class="cc">(.*?)</td>',row)
    if len(c)>=4:
        n=re.sub(r'<[^>]+>','',c[1]).strip(); l=re.search(r'href="([^"]+)"',c[3])
        syn=html.unescape(re.sub(r'<[^>]+>','',c[2])).strip()
        if l: G.setdefault(n,(('https://support.google.com'+html.unescape(l.group(1))) if l.group(1).startswith('/') else html.unescape(l.group(1)),syn))
def txt(s):
    s=re.sub(r'(?s)<(script|style)[^>]*>.*?</\1>',' ',s); s=re.sub(r'<(br|/tr|/li|/p|/h\d)[^>]*>','\n',s)
    s=html.unescape(re.sub(r'<[^>]+>',' ',s)); s=re.sub(r'[ \t]+',' ',s); return re.sub(r'\n\s*\n+','\n',s)
out={}
for f in F:
    r={}
    if f in MS:
        u='https://support.microsoft.com/en-us/excel/functions/'+MS[f]
        h=subprocess.run(['curl','-sL','-A','Mozilla/5.0 Chrome/120',u],capture_output=True).stdout.decode('utf8','ignore')
        ok='Microsoft Support' in h and f.split('.')[0] in h
        open(f'sources/functions/excel-{f.lower()}.txt','w').write(f'URL: {u}\nFetched 2026-10-13\n\n'+txt(h)[:60000]); r['excel']=u if ok else None
    if f in G:
        u=G[f][0]; h=subprocess.run(['curl','-sL','-A','Mozilla/5.0 Chrome/120',u+('&' if '?' in u else '?')+'hl=en'],capture_output=True).stdout.decode('utf8','ignore')
        ok=f in h
        open(f'sources/functions/sheets-{f.lower()}.txt','w').write(f'URL: {u}\nFetched 2026-10-13\n\n'+txt(h)[:60000]); r['sheets']=u if ok else None; r['sheets_syntax']=G[f][1]
    out[f]=r; print(f,'X' if r.get('excel') else '-', 'G' if r.get('sheets') else '-')
json.dump(out,open('func-sources.json','w'),indent=1)
