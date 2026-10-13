import re,json
def pairs(f):
    L=[l.strip() for l in open(f).read().split('\n')]
    out=[]
    for i,l in enumerate(L[:-1]):
        if l.endswith('|') and i+1<len(L):
            k=L[i+1].rstrip('| ').strip()
            if k and len(k)<60 and re.search(r'(Ctrl|Cmd|⌘|Shift|Alt|Option|F\d|Enter|Home|End|Esc|Tab|Space|Page|Fn|Control|\+)',k): out.append((l.rstrip('| ').strip(),k))
    return out
P={f:pairs(f'sources/{f}.txt') for f in ['ms-win','ms-mac','g-pc','g-mac']}
json.dump(P,open('pairs.json','w'),indent=0,ensure_ascii=False)
for f,v in P.items(): print(f,len(v))
