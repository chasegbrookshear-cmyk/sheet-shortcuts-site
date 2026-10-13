(function(){
// Newsletter: progressive enhancement. No JS = plain POST to Kit. With JS = fetch + inline aria-live result;
// on network/CORS failure fall back to a normal form submit.
document.querySelectorAll('form.nl-form').forEach(function(f){f.addEventListener('submit',function(ev){
 if(!window.fetch||f.dataset.fallback)return; ev.preventDefault();
 var out=f.parentNode.querySelector('.nl-result'),btn=f.querySelector('button');btn.disabled=true;out.className='nl-result';out.textContent='Sending…';
 fetch(f.action,{method:'POST',body:new FormData(f),headers:{'Accept':'application/json'}}).then(function(r){
  return r.json().catch(function(){return{}}).then(function(j){btn.disabled=false;
   if(r.ok){out.textContent='Thanks! Check your inbox to confirm your subscription.';f.reset()}
   else{out.className='nl-result err';out.textContent=(j&&(j.error&&j.error.message||j.message))||'Sorry, that didn’t work. Please check the address and try again.'}})
 }).catch(function(){f.dataset.fallback='1';f.submit()});
})});

// Copy buttons (hidden without JS; the formula text stays readable either way).
document.querySelectorAll('[data-copy]').forEach(function(b){b.addEventListener('click',function(){
 var t=document.getElementById(b.dataset.copy).textContent,st=document.getElementById('copy-status');t=t.charAt(0)==='='?t:'='+t;
 function done(ok){b.textContent=ok?'Copied':'Copy failed';if(st){st.textContent='';setTimeout(function(){st.textContent=ok?'Copied':'Copy failed'},50)}setTimeout(function(){b.textContent='Copy'},1800)}
 function legacy(){var a=document.createElement('textarea');a.value=t;a.setAttribute('readonly','');a.style.position='fixed';a.style.opacity='0';document.body.appendChild(a);a.select();var ok=false;try{ok=document.execCommand('copy')}catch(e){}document.body.removeChild(a);done(ok)}
 if(navigator.clipboard&&window.isSecureContext)navigator.clipboard.writeText(t).then(function(){done(true)},legacy);else legacy()})});
var rows=[].slice.call(document.querySelectorAll('.group .rows li')),f='all';
function apply(){rows.forEach(function(li){var d=li.dataset;li.classList.toggle('hidden',!(f==='all'||d.type===f||d.avail===f||d.cat===f))});
 document.querySelectorAll('.group').forEach(function(g){g.classList.toggle('hidden',!g.querySelector('li:not(.hidden)'))})}
document.querySelectorAll('.filters button').forEach(function(b){b.addEventListener('click',function(){f=b.dataset.f;
 document.querySelectorAll('.filters button').forEach(function(x){x.setAttribute('aria-pressed',x===b)});apply()})});

// App/platform preferences (localStorage). No JS: controls hidden, everything shown.
var H=document.documentElement,P={app:H.getAttribute('data-app')||'',os:H.getAttribute('data-os')||''},listeners=[];
function syncPrefs(){document.querySelectorAll('[data-pref]').forEach(function(b){b.setAttribute('aria-pressed',P[b.dataset.pref]===b.dataset.val)})}
document.querySelectorAll('[data-pref]').forEach(function(b){b.addEventListener('click',function(){var k=b.dataset.pref;P[k]=P[k]===b.dataset.val?'':b.dataset.val;
 if(P[k])H.setAttribute('data-'+k,P[k]);else H.removeAttribute('data-'+k);try{if(P[k])localStorage.setItem('cs.'+k,P[k]);else localStorage.removeItem('cs.'+k)}catch(e){}
 syncPrefs();listeners.forEach(function(fn){fn()})})});syncPrefs();

// Instant fuzzy search over search-index.json (combobox + listbox, aria-live count).
var ROOT=window.CS_ROOT||'.',IDX=null,loading=null;
function load(){if(IDX)return Promise.resolve(IDX);if(!loading)loading=fetch(ROOT+'/search-index.json').then(function(r){return r.json()}).then(function(j){
 IDX=j.map(function(e){var hay=(e.t+' '+e.s+' '+e.c+' '+(e.d||'')+' '+(e.f?e.f.join(' '):'')).toLowerCase();e._w=hay.split(/[^a-z0-9]+/).filter(Boolean);e._t=e.t.toLowerCase();e._n=e._t.split(/[^a-z0-9]+/).filter(Boolean);e._s=e.s.toLowerCase().split(' | ');return e});return IDX});return loading}
var MOD={ctrl:'ctrl',control:'ctrl',ctl:'ctrl',cmd:'cmd',command:'cmd','⌘':'cmd',meta:'cmd',win:'cmd',shift:'shift','⇧':'shift',alt:'alt',option:'alt',opt:'alt','⌥':'alt',fn:'fn'},
 KN={'return':'enter',pgdn:'pgdn',pagedown:'pgdn',esc:'escape',del:'delete',spacebar:'space'},STOP={a:1,an:1,the:1,to:1,of:1,'in':1,how:1,i:1,do:1,on:1,with:1,for:1,my:1,excel:1,sheets:1,google:1,sheet:1,shortcut:1,formula:1,key:1,keys:1};
function parseCombo(q){var t=q.toLowerCase().replace(/\s*\+\s*/g,' + ').split(/\s+/).filter(function(x){return x&&x!=='+'}),m=[],k=[];
 t.forEach(function(x){if(MOD[x])m.push(MOD[x]);else k.push(KN[x]||x)});if(!m.length)return null;
 if(q.slice(-1)==='+'&&/\+\s*\+$/.test(q))k.push('+');m=m.filter(function(x,i){return m.indexOf(x)===i}).sort();return{m:m,k:k.join(' ')}}
function lev(a,b){if(Math.abs(a.length-b.length)>2)return 9;var p=[],i,j;for(j=0;j<=b.length;j++)p[j]=j;
 for(i=1;i<=a.length;i++){var c=[i];for(j=1;j<=b.length;j++)c[j]=Math.min(p[j]+1,c[j-1]+1,p[j-1]+(a[i-1]===b[j-1]?0:1));p=c}return p[b.length]}
function tokScore(w,words){var best=0;for(var i=0;i<words.length;i++){var x=words[i],s=0;
 if(x===w)s=3;else if(x.indexOf(w)===0)s=w.length>1?2.2:0;else if(w.length>3&&x.indexOf(w)>0)s=1.2;
 else if(w.length>=4&&x.length>=3){var d=lev(w,x.slice(0,w.length+1)),d2=lev(w,x);d=Math.min(d,d2);if(d===1)s=1.4;else if(d===2&&w.length>=7)s=0.9}
 if(s>best)best=s}return best}
// which of ew,em,sw,sm slots are visible under prefs
function slots(){var o=[];[['excel','win'],['excel','mac'],['sheets','win'],['sheets','mac']].forEach(function(s,i){if((!P.app||P.app===s[0])&&(!P.os||P.os===s[1]))o.push(i)});return o}
function isDash(v){return !v||v==='—'||v==='-'}
function visible(e){var sl=slots();if(e.y==='s')return sl.some(function(i){return !isDash(e.k[i])});
 if(P.app==='excel')return !isDash(e.f[0]);if(P.app==='sheets')return !isDash(e.f[1]);return true}
function scoreCombo(e,c){var best=0,sl=slots();sl.forEach(function(i){(e.m[i]||[]).forEach(function(x){var p=x.split(' '),mods=p.filter(function(y){return/^(alt|cmd|ctrl|fn|shift)$/.test(y)}),key=p.slice(mods.length).join(' '),s=0;
 var cm=c.m.map(function(y){return y}),em=mods.slice();
 function same(a,b){return a.length===b.length&&a.every(function(y){return b.indexOf(y)>=0})}
 var swap=function(a){return a.map(function(y){return y==='cmd'?'ctrl':y})};
 if(c.k===key||(!c.k&&false)){if(same(cm,em))s=100;else if(same(swap(cm),swap(em)))s=85;else if(c.m.every(function(y){return em.indexOf(y)>=0||swap(em).indexOf(y==='cmd'?'ctrl':y)>=0}))s=45;else s=30}
 else if(!c.k&&same(cm,em))s=20;
 if(s>best)best=s})});return best}
function search(q){var c=parseCombo(q),res=[];
 var toks=q.toLowerCase().replace(/[+]/g,' ').split(/[^a-z0-9$%#@!^&;=`~\-]+/).filter(function(w){return w&&!STOP[w]&&!MOD[w]}),ql=q.toLowerCase().trim();
 IDX.forEach(function(e){if(!visible(e))return;var s=0;
  if(c&&e.y==='s')s+=scoreCombo(e,c);
  if(!c||!c.k){var tot=0,hit=0;toks.forEach(function(w){var t=Math.max(tokScore(w,e._w),1.6*tokScore(w,e._n));if(t>0)hit++;tot+=t});
   if(toks.length&&hit>=Math.ceil(toks.length*0.5)){s+=tot*(hit/toks.length);
    if(e._t===ql)s+=30;else if(e._t.indexOf(ql)===0)s+=15;else if(e._t.indexOf(ql)>=0)s+=8;
    if(e._s.indexOf(ql)>=0)s+=14;else if(e._s.some(function(x){return x.indexOf(ql)>=0}))s+=7}}
  if(s>0)res.push([s,e])});
 res.sort(function(a,b){return b[0]-a[0]||a[1].t.localeCompare(b[1].t)});return {r:res.slice(0,8),c:c}}
function esc(s){return String(s).replace(/[&<>"]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
function kb(v){if(isDash(v))return'—';return esc(v).split(/\s*\/\s*/).map(function(p){return p.replace(/^([^ (,]+)/,function(c){return c.split(/\+(?!$)/).map(function(k){return'<kbd>'+k+'</kbd>'}).join('+')})}).join(' / ')}
var LAB=['Excel Win','Excel Mac','Sheets Win','Sheets Mac'];
function preview(e){if(e.y==='s'){var sl=slots(),seen={},out=[];sl.forEach(function(i){if(!isDash(e.k[i])&&!seen[e.k[i]]&&out.length<2){seen[e.k[i]]=1;out.push('<span class="sr-only">'+LAB[i]+': </span>'+kb(e.k[i]))}});return out.join(' · ')}
 var f=P.app==='sheets'?e.f[1]:(e.f[0]||e.f[1]);return esc(f.length>38?f.slice(0,36)+'…':f)}
document.querySelectorAll('[data-search]').forEach(function(box){var inp=box.querySelector('input'),ul=box.querySelector('[role=listbox]'),st=box.querySelector('[role=status]'),act=-1,last=[],tm;
 function setAct(i){var o=ul.querySelectorAll('[role=option]');act=i;o.forEach(function(x,j){x.setAttribute('aria-selected',j===i)});
  if(i>=0&&o[i]){inp.setAttribute('aria-activedescendant',o[i].id);o[i].scrollIntoView({block:'nearest'})}else inp.removeAttribute('aria-activedescendant')}
 function close(){ul.hidden=true;inp.setAttribute('aria-expanded','false');setAct(-1)}
 function run(){var q=inp.value.trim();if(!q){ul.innerHTML='';close();st.textContent='';return}
  load().then(function(){var o=search(q);last=o.r;act=-1;
   if(!last.length){ul.innerHTML='<li class="none" role="option" aria-disabled="true" id="'+inp.id+'-none">No match for “'+esc(q)+'”'+(P.app||P.os?'. Try turning off the Excel/Sheets or Win/Mac filter.':'. Try other words, e.g. “copy down”.')+'</li>'}
   else ul.innerHTML=last.map(function(x,i){var e=x[1],note=(o.c&&o.c.k&&x[0]<85&&e.y==='s')?' · closest key match':'';
    return '<li role="option" id="'+inp.id+'-o'+i+'" aria-selected="false"><div class="ro" data-u="'+e.u+'"><span class="rt">'+esc(e.t)+'</span><span class="rk">'+preview(e)+'</span><span class="rc">'+esc(e.c)+(e.y==='s'?' · shortcut':' · formula')+note+'</span></div></li>'}).join('');
   ul.hidden=false;inp.setAttribute('aria-expanded','true');
   clearTimeout(tm);tm=setTimeout(function(){st.textContent=last.length?last.length+' result'+(last.length>1?'s':'')+'. Top: '+last[0][1].t+'. Use up and down arrows to choose.':'No results.'},350)})}
 inp.addEventListener('focus',load,{once:true});inp.addEventListener('input',run);
 inp.addEventListener('keydown',function(ev){var n=last.length;
  if(ev.key==='ArrowDown'){ev.preventDefault();if(ul.hidden)run();else if(n)setAct((act+1)%n)}
  else if(ev.key==='ArrowUp'){ev.preventDefault();if(n)setAct(act<=0?n-1:act-1)}
  else if(ev.key==='Enter'){var i=act>=0?act:(n?0:-1);if(i>=0&&!ul.hidden){ev.preventDefault();location.href=ROOT+'/'+last[i][1].u+'/index.html'}}
  else if(ev.key==='Escape'){if(!ul.hidden){ev.preventDefault();close()}else inp.value=''}});
 ul.addEventListener('mousedown',function(ev){ev.preventDefault()});ul.addEventListener('click',function(ev){var d=ev.target.closest('.ro');if(d)location.href=ROOT+'/'+d.dataset.u+'/index.html'});
 inp.addEventListener('blur',function(){setTimeout(close,150)});
 listeners.push(function(){if(inp.value.trim())run()})});
})();
