import json,re
P=json.load(open('pairs.json'))
S=[ # slug, title, google action, excel regex
("select-column","Select an entire column","Select column",r"^Select an entire column"),
("select-row","Select an entire row","Select row",r"^Select an entire row"),
("fill-down","Fill down","Fill down",r"Fill Down command"),
("fill-right","Fill right","Fill right",r"Fill Right command"),
("fill-range","Fill a selected range with the same entry","Fill range",r"[Ff]ill the selected cell range with the current entry"),
("paste-values","Paste values only","Paste values only",r"^Paste values"),
("find-replace","Find and replace","Find and replace",r"Find and Replace|^Open the Replace"),
("strikethrough","Strikethrough","Strikethrough",r"strikethrough"),
("insert-date","Insert today's date","Insert date",r"current date"),
("insert-time","Insert the current time","Insert time",r"current time"),
("format-currency","Format as currency","Format as currency",r"Currency format"),
("format-percent","Format as percentage","Format as percentage",r"Percentage format"),
("format-date","Format as date","Format as date",r"Date format"),
("format-time","Format as time","Format as time",r"Time format"),
("format-number","Format as number with two decimals","Format as decimal",r"Number format with two decimal"),
("format-scientific","Format as scientific notation","Format as exponent",r"Scientific number format"),
("insert-link","Insert a hyperlink","Insert link",r"[Hh]yperlink"),
("show-formulas","Show all formulas","Show all formulas",r"display of cell values and formulas|Toggle.*formulas"),
("absolute-reference","Toggle absolute and relative references (F4)","(when entering a formula)#F4",r"absolute and relative|absolute, relative"),
("hide-rows","Hide rows","Hide row",r"^Hide the selected rows"),
("hide-columns","Hide columns","Hide column",r"^Hide the selected columns"),
("unhide-rows","Unhide rows","Unhide row",r"^Unhide"),
("group-rows","Group rows or columns","Group rows or columns",r"^Group"),
("ungroup-rows","Ungroup rows or columns","Ungroup rows or columns",r"^Ungroup"),
("insert-note","Add or edit a note","Insert/edit note",r"[Nn]ote"),
("insert-comment","Add a comment","Insert/edit comment",r"[Cc]omment"),
("insert-sheet","Insert a new sheet","Insert new sheet",r"[Ii]nsert a new worksheet"),
("next-sheet","Move to the next sheet","Move to next sheet",r"next sheet"),
("previous-sheet","Move to the previous sheet","Move to previous sheet",r"previous sheet"),
("go-to-start","Jump to the top of the sheet","Move to beginning of sheet",r"beginning of a worksheet"),
("go-to-end","Jump to the last used cell","Move to end of sheet",r"last cell on a worksheet"),
("clear-formatting","Clear formatting","Clear formatting",r"[Cc]lear.*format|Remove.*format"),
("center-align","Center align","Center align",r"[Cc]enter"),
("outer-border","Add an outline border","Apply outer border",r"outline border"),
("remove-borders","Remove borders","Remove borders",r"[Rr]emove.*border"),
("insert-rows-cols","Insert rows or columns","Insert rows above",r"Insert dialog|Open the Insert"),
("delete-rows-cols","Delete rows or columns","Delete rows",r"Delete dialog|Open the Delete"),
("convert-to-table","Convert a range to a table","Convert range to table",r"Create Table|[Ii]nsert a table|create a table"),
("filter-dropdown","Open a filter drop-down","Open drop-down menu on filtered cell",r"AutoFilter|drop-down list"),
("edit-cell","Edit the active cell (F2)","#F2",r"^Edit the active cell"),
("recalculate-preview","Preview a formula's result (F9)","(when entering a formula)#F9",r"Calculate all|[Cc]alculate"),
("undo-redo","Undo and redo","Undo",r"^Undo|^Redo"),
("select-all","Select all","Select all",r"^Select the entire worksheet"),
("keyboard-help","See every shortcut","Show common keyboard shortcuts",r"Tell me|Search box|Help"),
]
def g(plat,act):
    name,_,key=act.partition('#')
    r=[(a,k) for a,k in P[plat] if a==name and (not key or k==key) or (not name and k==key)]
    return r[:1]
def x(plat,rx): return [(a,k) for a,k in P[plat] if re.search(rx,a)][:3]
out=[]
for s,t,ga,ex in S:
    out.append(dict(slug=s,title=t,g_pc=g('g-pc',ga),g_mac=g('g-mac',ga),x_win=x('ms-win',ex),x_mac=x('ms-mac',ex)))
json.dump(out,open('pick.json','w'),indent=1,ensure_ascii=False)
for o in out: print(o['slug'],'| G',o['g_pc'],o['g_mac'],'\n   XW',o['x_win'],'\n   XM',o['x_mac'])
