import json
MSU="https://support.microsoft.com/en-us/office/keyboard-shortcuts-in-excel-1798d9d5-842a-42b8-9c99-9b7213f0040f"
GSU="https://support.google.com/docs/answer/181110"
SRC_S=[{"name":"Microsoft Support: Keyboard shortcuts in Excel (Windows and macOS tabs)","url":MSU,"cache":"sources/ms-excel-shortcuts.html"},
       {"name":"Google Docs Editors Help: Keyboard shortcuts for Google Sheets","url":GSU,"cache":"sources/g-sheets-shortcuts.html"}]
# slug, action, category, excel_win, excel_mac, sheets_win, sheets_mac, note
S=[
("select-entire-column","Select an entire column","Selecting","Ctrl+Space","Ctrl+Space","Ctrl+Space","Ctrl+Space",""),
("select-entire-row","Select an entire row","Selecting","Shift+Space","Shift+Space","Shift+Space","Shift+Space",""),
("select-all","Select all","Selecting","Ctrl+A (or Ctrl+Shift+Space)","Cmd+A","Ctrl+A","Cmd+A","In Excel, pressing it again expands from the current region to the whole sheet."),
("fill-down","Fill down","Editing","Ctrl+D","Cmd+D (Ctrl+D also listed)","Ctrl+D","Cmd+D",""),
("fill-selected-range","Fill a selected range with the same entry","Editing","Ctrl+Enter","Cmd+Return","Ctrl+Enter","Cmd+Enter",""),
("paste-values-only","Paste values only","Editing","Ctrl+Alt+V, then V, then Enter","Cmd+Ctrl+V opens Paste Special","Ctrl+Shift+V","Cmd+Shift+V","Excel has no one-step values paste on Microsoft's page; it opens Paste Special. Don't invent a Mac key for the Values option."),
("edit-active-cell","Edit the active cell","Editing","F2","F2 (or Ctrl+U)","F2","F2",""),
("undo-redo","Undo and redo","Editing","Ctrl+Z / Ctrl+Y","Cmd+Z / Cmd+Y","Ctrl+Z / Ctrl+Y","Cmd+Z / Cmd+Y",""),
("insert-todays-date","Insert today's date","Dates and times","Ctrl+;","Ctrl+;","Ctrl+;","Cmd+;",""),
("insert-current-time","Insert the current time","Dates and times","Ctrl+Shift+:","Cmd+;","Ctrl+Shift+;","Cmd+Shift+;","Excel for Mac's date and time keys differ from Sheets on Mac."),
("format-as-currency","Format as currency","Number formats","Ctrl+Shift+$","Ctrl+Shift+$","Ctrl+Shift+4","Ctrl+Shift+4","Same physical keys on a US keyboard ($ is Shift+4)."),
("format-as-percentage","Format as percentage","Number formats","Ctrl+Shift+%","Ctrl+Shift+%","Ctrl+Shift+5","Ctrl+Shift+5",""),
("format-as-date","Format as date","Number formats","Ctrl+Shift+#","Ctrl+Shift+#","Ctrl+Shift+3","Ctrl+Shift+3",""),
("format-as-time","Format as time","Number formats","Ctrl+Shift+@","Ctrl+Shift+@","Ctrl+Shift+2","Ctrl+Shift+2",""),
("format-as-number","Format as a number with two decimals","Number formats","Ctrl+Shift+!","Ctrl+Shift+!","Ctrl+Shift+1","Ctrl+Shift+1",""),
("format-as-scientific","Format as scientific notation","Number formats","Ctrl+Shift+^","Ctrl+Shift+^","Ctrl+Shift+6","Ctrl+Shift+6",""),
("strikethrough","Strikethrough","Text formatting","Ctrl+5","Shift+Cmd+X","Alt+Shift+5","Cmd+Shift+X",""),
("center-align","Center align","Text formatting","Alt+H, A, C","Cmd+E","Ctrl+Shift+E","Cmd+Shift+E","Excel for Windows uses a ribbon key sequence, not a chord."),
("outline-border","Add an outline border","Text formatting","Ctrl+Shift+&","Cmd+Option+0","Alt+Shift+7","Option+Shift+7",""),
("remove-borders","Remove borders","Text formatting","Ctrl+Shift+_","Cmd+Option+Hyphen","Alt+Shift+6","Option+Shift+6",""),
("insert-hyperlink","Insert a link","Inserting","Ctrl+K","Cmd+K","Ctrl+K","Cmd+K",""),
("insert-note","Add or edit a note","Inserting","Shift+F2","Shift+F2","Shift+F2","Shift+F2",""),
("insert-comment","Add a comment","Inserting","Ctrl+Shift+F2","Cmd+Shift+F2","Ctrl+Alt+M","Cmd+Option+M",""),
("insert-new-sheet","Insert a new sheet","Sheets and tabs","Shift+F11","Shift+F11","Shift+F11","Shift+Fn+F11",""),
("next-sheet","Move to the next sheet","Sheets and tabs","Ctrl+Page Down","Ctrl+Page Down","Alt+Down Arrow","Option+Down Arrow","Previous sheet is parked: Microsoft's Mac table lists Ctrl+Page Down for both directions."),
("insert-cells-rows-columns","Insert cells, rows or columns","Rows and columns","Ctrl+Shift++","Ctrl+Shift+=","Ctrl+Alt+=","Cmd+Option+=","Sheets opens an insert menu; select whole rows or columns first."),
("delete-cells-rows-columns","Delete cells, rows or columns","Rows and columns","Ctrl+-","Cmd+-","Ctrl+Alt+-","Cmd+Option+-","Select whole rows or columns first to delete them directly."),
("hide-rows","Hide rows","Rows and columns","Ctrl+9","Ctrl+9","Ctrl+Alt+9","Cmd+Option+9",""),
("hide-columns","Hide columns","Rows and columns","Ctrl+0","Ctrl+0","Ctrl+Alt+0","Cmd+Option+0",""),
("go-to-top-of-sheet","Jump to the top of the sheet","Navigation","Ctrl+Home","Ctrl+Home","Ctrl+Home","Cmd+Fn+Left Arrow",""),
("go-to-last-cell","Jump to the last used cell","Navigation","Ctrl+End","Ctrl+End","Ctrl+End","Cmd+Fn+Right Arrow",""),
("show-all-formulas","Show all formulas","Formulas","Ctrl+`","Ctrl+`","Ctrl+~","Ctrl+~",""),
("absolute-reference-f4","Switch absolute and relative references","Formulas","F4","Cmd+T","F4","Fn+F4","Use while editing a formula with a reference selected."),
("autosum","AutoSum","Formulas","Alt+=","Shift+Cmd+T","—","—","Google's shortcut page lists no AutoSum shortcut, so Sheets shows a dash."),
("convert-to-table","Turn a range into a table","Data","Ctrl+T (or Ctrl+L)","Cmd+T","Ctrl+Alt+T","Cmd+Option+T",""),
("open-filter-menu","Open a filter drop-down","Data","Alt+Down Arrow","Option+Down Arrow","Ctrl+Alt+R","Ctrl+Cmd+R","The cell must have a filter on it."),
]
ents=[]
for slug,act,cat,xw,xm,gw,gm,note in S:
    t=f"{act} shortcut in Excel and Google Sheets"
    ents.append(dict(slug=slug,type="shortcut",category=cat,name=act,
      seo_title=(t if len(t)<=60 else f"{act}: Excel & Sheets shortcut")[:60],
      meta=f"{act} with one key combo. Excel and Google Sheets keys for Windows and Mac, checked against Microsoft's and Google's official shortcut pages."[:155],
      keys={"excel_windows":xw,"excel_mac":xm,"sheets_windows":gw,"sheets_mac":gm},
      note=note,sources=SRC_S,checked="2026-10-13"))
fs=json.load(open('func-sources.json'))
GRID={"A1:E7":[["Order","Region","Rep","Amount","Date"],[1001,"East","Ana",120,"2026-01-05"],[1002,"West","Ben",80,"2026-01-12"],[1003,"East","Cy",200,"2026-02-03"],[1004,"North","Ana",50,"2026-02-20"],[1005,"West","Ana",150,"2026-03-08"],[1006,"East","Ben",90,"2026-03-15"]],
      "G1:G5":[["Text"],["  hello   world "],["jane doe"],["SKU-1042-BLU"],["a,b,c"]]}
# fn, slug, category, use, excel_formula, sheets_formula(None=same), availability, expected(for Builder to confirm by recalc), recalc
F=[
("VLOOKUP","vlookup","Lookup","Find a value in the first column and return a value from the same row.",'=VLOOKUP(1003,A2:E7,4,FALSE)',None,"both","200","libreoffice"),
("XLOOKUP","xlookup","Lookup","Look up a value in one range and return the match from another, without column numbers.",'=XLOOKUP(1003,A2:A7,D2:D7)',None,"both","200","libreoffice-24.8+"),
("INDEX","index","Lookup","Return the value at a given position in a range.",'=INDEX(D2:D7,3)',None,"both","200","libreoffice"),
("MATCH","match","Lookup","Return the position of a value in a range.",'=MATCH(1004,A2:A7,0)',None,"both","4","libreoffice"),
("INDEX + MATCH","index-match","Lookup","Combine INDEX and MATCH to look up in any direction.",'=INDEX(C2:C7,MATCH(1005,A2:A7,0))',None,"both","Ana","libreoffice"),
("SUMIF","sumif","Math","Add numbers that meet one condition.",'=SUMIF(B2:B7,"East",D2:D7)',None,"both","410","libreoffice"),
("SUMIFS","sumifs","Math","Add numbers that meet several conditions.",'=SUMIFS(D2:D7,B2:B7,"East",C2:C7,"Ana")',None,"both","120","libreoffice"),
("COUNTIF","countif","Math","Count cells that meet one condition.",'=COUNTIF(C2:C7,"Ana")',None,"both","3","libreoffice"),
("COUNTIFS","countifs","Math","Count rows that meet several conditions.",'=COUNTIFS(B2:B7,"West",D2:D7,">100")',None,"both","1","libreoffice"),
("AVERAGEIFS","averageifs","Math","Average numbers that meet one or more conditions.",'=AVERAGEIFS(D2:D7,B2:B7,"East")',None,"both","136.666…","libreoffice"),
("SUMPRODUCT","sumproduct","Math","Multiply ranges together and add the results; handy for conditional totals.",'=SUMPRODUCT((B2:B7="East")*D2:D7)',None,"both","410","libreoffice"),
("ROUND","round","Math","Round a number to a set number of digits.",'=ROUND(AVERAGE(D2:D7),1)',None,"both","115","libreoffice"),
("COUNTA","counta","Math","Count cells that aren't empty.",'=COUNTA(A2:A7)',None,"both","6","libreoffice"),
("IF","if","Logic","Return one value if a test is true and another if it's false.",'=IF(D2>100,"Big","Small")',None,"both","Big","libreoffice"),
("IFS","ifs","Logic","Check several conditions in order and return the first match.",'=IFS(D2>=150,"High",D2>=100,"Mid",TRUE,"Low")',None,"both","Mid","libreoffice"),
("IFERROR","iferror","Logic","Show your own value instead of an error.",'=IFERROR(VLOOKUP(9999,A2:E7,4,FALSE),"Not found")',None,"both","Not found","libreoffice"),
("LET","let","Logic","Name a calculation once and reuse it inside a formula.",'=LET(t,SUM(D2:D7),t*0.1)',None,"both","69","libreoffice-24.8+"),
("FILTER","filter","Dynamic arrays","Return only the rows that meet a condition.",'=FILTER(A2:A7,B2:B7="East")',None,"both","1001; 1003; 1006 (spills)","libreoffice-24.8+"),
("UNIQUE","unique","Dynamic arrays","List each value once.",'=UNIQUE(B2:B7)',None,"both","East; West; North (spills)","libreoffice-24.8+"),
("SORT","sort","Dynamic arrays","Sort a range with a formula.",'=SORT(D2:D7,1,FALSE)',None,"both","200; 150; 120; 90; 80; 50 (spills)","libreoffice-24.8+"),
("TEXTJOIN","textjoin","Text","Join text from a range with a separator.",'=TEXTJOIN(", ",TRUE,UNIQUE(C2:C7))',None,"both","Ana, Ben, Cy","libreoffice-24.8+"),
("CONCATENATE","concatenate","Text","Join pieces of text into one cell.",'=CONCATENATE(C2," - ",B2)',None,"both","Ana - East","libreoffice"),
("TRIM","trim","Text","Remove extra spaces from text.",'=TRIM(G2)',None,"both","hello world","libreoffice"),
("PROPER","proper","Text","Capitalize the first letter of each word.",'=PROPER(G3)',None,"both","Jane Doe","libreoffice"),
("LEFT","left","Text","Take characters from the start of text.",'=LEFT(G4,3)',None,"both","SKU","libreoffice"),
("MID","mid","Text","Take characters from the middle of text.",'=MID(G4,5,4)',None,"both","1042","libreoffice"),
("LEN","len","Text","Count the characters in text.",'=LEN(G4)',None,"both","12","libreoffice"),
("SUBSTITUTE","substitute","Text","Replace specific text inside a string.",'=SUBSTITUTE(G4,"-"," ")',None,"both","SKU 1042 BLU","libreoffice"),
("TEXT","text","Text","Format a number or date as text in a pattern you choose.",'=TEXT(E2,"mmm d, yyyy")',None,"both","Jan 5, 2026","libreoffice"),
("REGEXEXTRACT","regexextract","Text","Pull the part of text that matches a pattern.",'=REGEXEXTRACT(G4,"[0-9]+")',None,"both","1042","not-in-libreoffice: flag, do not publish until checked another way"),
("DATEDIF","datedif","Dates","Count days, months or years between two dates.",'=DATEDIF(E2,E7,"d")',None,"both","69","libreoffice"),
("NETWORKDAYS","networkdays","Dates","Count working days between two dates.",'=NETWORKDAYS(E2,E3)',None,"both","6","libreoffice"),
("EOMONTH","eomonth","Dates","Get the last day of a month.",'=EOMONTH(E2,0)',None,"both","2026-01-31 (format as date)","libreoffice"),
("TEXTSPLIT / SPLIT","split-text","Text","Split text into cells by a separator. Excel calls it TEXTSPLIT; Sheets calls it SPLIT.",'=TEXTSPLIT(G5,",")','=SPLIT(G5,",")',"different-names","a | b | c (spills across)","check LibreOffice version for TEXTSPLIT; SPLIT is Sheets-only"),
("QUERY","query","Sheets-only","Run a SQL-like query over a range.",None,'=QUERY(A1:E7,"select C, sum(D) group by C",1)',"sheets-only","Rep/sum table","sheets-only: not checkable in LibreOffice; flag"),
("ARRAYFORMULA","arrayformula","Sheets-only","Apply one formula down a whole column.",None,'=ARRAYFORMULA(D2:D7*2)',"sheets-only","240; 160; 400; 100; 300; 180","sheets-only: not checkable in LibreOffice; flag"),
("IMPORTRANGE","importrange","Sheets-only","Pull a range from another Google Sheets file.",None,'=IMPORTRANGE("spreadsheet_url","Sheet1!A1:E7")',"sheets-only","(needs a second file; show syntax only, no result cell)","sheets-only: no result shown"),
]
key={"TEXTSPLIT / SPLIT":("TEXTSPLIT","SPLIT"),"INDEX + MATCH":("INDEX","MATCH")}
for fn,slug,cat,use,xf,gf,av,exp,rc in F:
    src=[]
    a,b=key.get(fn,(fn,fn))
    for k in dict.fromkeys([a,b]):
        d=fs.get(k,{})
        if d.get('excel') and av!="sheets-only": src.append({"name":f"Microsoft Support: {k} function","url":d['excel'],"cache":f"sources/functions/excel-{k.lower()}.txt"})
        if d.get('sheets') and not (av=="different-names" and k=="TEXTSPLIT"): src.append({"name":f"Google Docs Editors Help: {k}","url":d['sheets'],"cache":f"sources/functions/sheets-{k.lower()}.txt"})
    t=f"{fn} in Excel and Google Sheets, with an example"
    if len(t)>60: t=f"{fn} in Excel and Google Sheets"
    if av=="sheets-only": t=f"{fn} in Google Sheets (and the Excel workaround)"[:60] if False else f"{fn} in Google Sheets, with an example"
    ents.append(dict(slug=slug,type="formula",category=cat,name=fn,seo_title=t[:60],
      meta=f"{use} How {fn} works in Excel and Google Sheets, with a worked example recalculated before publishing."[:155] if av!="sheets-only" else f"{use} {fn} is a Google Sheets function with no Excel equivalent of the same name. Worked example inside."[:155],
      use=use,excel_formula=xf,sheets_formula=gf if gf else xf if av!="sheets-only" else gf,availability=av,
      expected_result_for_recalc_check=exp,recalc=rc,example_grid="GRID",sources=src,checked="2026-10-13"))
bad=[e['slug'] for e in ents if len(e['sources'])<(1 if e.get('availability') in('sheets-only',) else 2)]
json.dump({"version":"0.1","owner":"Growth","built":"2026-10-13","example_grid":GRID,
  "ranking_note":"Order is Growth's judgment of common desk-worker searches, not measured search volume (no keyword tool on a $0 budget).",
  "entries":ents},open('bet-c-entries.json','w'),indent=1,ensure_ascii=False)
print(len(ents),'entries; short on sources:',bad)
print(max(len(e['seo_title']) for e in ents), max(len(e['meta']) for e in ents))
