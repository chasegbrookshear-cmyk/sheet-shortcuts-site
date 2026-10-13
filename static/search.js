(function(){var q=document.getElementById('q'),ul=document.getElementById('results');if(!q)return;var root=q.dataset.root,idx=null;
function load(cb){if(idx)return cb();fetch(root+'/search.json').then(function(r){return r.json()}).then(function(d){idx=d;cb()})}
function esc(s){return s.replace(/[&<>"]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
q.addEventListener('input',function(){var t=q.value.trim().toLowerCase();if(!t){ul.innerHTML='';return}
load(function(){var terms=t.split(/\s+/);var hits=idx.filter(function(e){var h=(e.t+' '+e.c+' '+e.k+' '+e.x).toLowerCase();return terms.every(function(w){return h.indexOf(w)>=0})}).slice(0,8);
ul.innerHTML=hits.map(function(e){return'<li><a href="'+root+'/'+e.s+'/index.html">'+esc(e.t)+' <small>· '+esc(e.c)+'</small></a></li>'}).join('')||'<li><a>No matches</a></li>'})})})();
