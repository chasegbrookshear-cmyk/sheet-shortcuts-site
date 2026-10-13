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
