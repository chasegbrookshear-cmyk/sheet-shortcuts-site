(function(){
document.querySelectorAll('[data-copy]').forEach(function(b){b.addEventListener('click',function(){var t=document.getElementById(b.dataset.copy).textContent;
 if(navigator.clipboard)navigator.clipboard.writeText(t).then(function(){b.textContent='Copied';setTimeout(function(){b.textContent='Copy'},1500)})})});
var q=document.getElementById('q');if(!q)return;var rows=[].slice.call(document.querySelectorAll('.rows li')),f='all';
function apply(){var t=q.value.trim().toLowerCase().split(/\s+/).filter(Boolean);
 rows.forEach(function(li){var d=li.dataset,h=(d.s||'').toLowerCase();
  var okf=f==='all'||d.type===f||d.avail===f||d.cat===f;var okq=t.every(function(w){return h.indexOf(w)>=0});li.classList.toggle('hidden',!(okf&&okq))});
 document.querySelectorAll('.group').forEach(function(g){g.classList.toggle('hidden',!g.querySelector('li:not(.hidden)'))})}
q.addEventListener('input',apply);
document.querySelectorAll('.filters button').forEach(function(b){b.addEventListener('click',function(){f=b.dataset.f;
 document.querySelectorAll('.filters button').forEach(function(x){x.setAttribute('aria-pressed',x===b)});apply()})});
})();
