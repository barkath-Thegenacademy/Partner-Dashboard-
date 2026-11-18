from pathlib import Path
import re
p=Path('web/app.js');s=p.read_text(encoding='utf-8')
start=s.index('function persist()');end=s.index('function render()',start)
s=s[:start]+'''let revision=0,canEdit=false,saving=false,dirty=false;
async function request(path,options={}){const res=await fetch(path,{cache:'no-store',...options});const body=await res.json();if(!res.ok)throw Error(body.error||'Request failed');return body;}
async function persist(){
 if(!canEdit||saving)return false;
 saving=true;dirty=true;$('save-status').textContent='Saving shared changes...';
 try{localStorage.setItem('tga-shared-draft',JSON.stringify(partners));}catch{}
 try{const result=await request('/api/partners',{method:'PUT',headers:{'Content-Type':'application/json'},body:JSON.stringify({revision,partners:partners.map(p=>({...p,cohorts:memberships(p)}))})});revision=result.revision;dirty=false;$('save-status').textContent='Saved for everyone';try{localStorage.removeItem('tga-shared-draft');}catch{}return true;}
 catch(e){$('save-status').textContent='Not saved: '+e.message;toast(e.message);return false;}
 finally{saving=false;}
}
async function refreshBoard(){const data=await request('/api/partners');partners=data.partners;revision=data.revision;dirty=false;render();$('save-status').textContent='Shared board loaded';}
''' +s[end:]
s=s.replace("function edit(id){", "function edit(id){if(saving){toast('Please wait for the save to finish.');return;}")
s=s.replace("$('editor').showModal();", "$('form').querySelectorAll('input,select,textarea,button[type=submit]').forEach(el=>el.disabled=!canEdit);$('editor').showModal();")
s=s.replace("$('form').onsubmit=e=>{e.preventDefault();", "$('form').onsubmit=async e=>{e.preventDefault();if(!canEdit||saving)return;")
s=s.replace("persist();render();$('editor').close();toast('Partner saved');", "if(await persist()){render();$('editor').close();toast('Partner saved for everyone');}")
s=s.replace("let f=e.target.files[0];if(!f)return;", "let f=e.target.files[0];if(!f||!canEdit||saving)return;")
s=s.replace("persist();render();toast(incoming.length+' partners imported; matched by name.');", "if(await persist()){render();toast(incoming.length+' partners imported for everyone.');}")
s=s[:s.index('async function init()')]+'''
async function init(){
 $('add').disabled=true;$('import').disabled=true;
 try{const user=await request('/api/me');canEdit=user.canEdit;
 $('auth-status').textContent=user.email?(canEdit?'Editor: ':'Viewing as ')+user.email:'Sign in to edit shared partners';
 $('signin').textContent=user.email?'Switch account':'Sign in to edit';
 $('signin').href=user.email?'/signout-with-chatgpt?return_to=%2F':'/signin-with-chatgpt?return_to=%2F';
 await refreshBoard();$('add').disabled=!canEdit;$('import').disabled=!canEdit;
 let old;try{old=JSON.parse(localStorage.getItem(key));}catch{}
 $('local-backup').hidden=!Array.isArray(old);
 $('local-backup').onclick=()=>{const current=partners;partners=old;try{$('export').click();}finally{partners=current;}};
 $('refresh-board').onclick=async()=>{if(dirty&&!confirm('Discard the unsaved draft and load the latest shared board? Export CSV first if you want to keep it.'))return;try{await refreshBoard();}catch(e){toast(e.message);}};
 $('open-editor').onclick=()=>{if(!canEdit){location.href=$('signin').href;return;}setView('directory');$('search').focus();toast('Choose a partner to edit, or select Add partner.');};
 setInterval(async()=>{if(saving||dirty||$('editor').open||document.hidden)return;try{await refreshBoard();}catch{$('save-status').textContent='Connection interrupted. Refresh to retry.';}},20000);
 }catch(e){$('save-status').textContent='Could not load shared board. Reload to retry.';toast(e.message);}
}init();
'''
p.write_text(s,encoding='utf-8')
p=Path('web/index.html');s=p.read_text(encoding='utf-8')
s=s.replace('<section class="heading">','<div class="shared-access"><span id="auth-status">Loading access...</span><a id="signin" target="_top" href="/signin-with-chatgpt?return_to=%2F">Sign in to edit</a><button id="open-editor">Open partner editor</button><button id="refresh-board">Refresh board</button><button id="local-backup" hidden>Export old browser records</button></div><section class="heading">')
s=re.sub(r'<span id="save-status">.*?</span>','<span id="save-status">Loading shared records...</span>',s)
s=s.replace('Saved in this browser. Export a CSV to keep or share your updates.','Changes save to the shared board for Barkath and Sumukh. Sign in with your authorized TGA account to edit.')
s=s.replace('Sheet snapshot','Original sheet snapshot')
p.write_text(s,encoding='utf-8')
p=Path('web/style.css');p.write_text(p.read_text(encoding='utf-8')+'\n.shared-access{display:flex;align-items:center;gap:12px;flex-wrap:wrap;padding:14px 18px;background:#f0f0ff;border:1px solid #dedfff;border-radius:12px;margin-top:20px;font-size:13px}.shared-access a{color:#4f56b8}.shared-access button{background:white;border:1px solid #d9daf5;border-radius:8px;padding:8px 12px;cursor:pointer}button:disabled{opacity:.5;cursor:not-allowed}#save-status{max-width:560px}input:disabled,textarea:disabled,select:disabled{opacity:1;color:#555}\n',encoding='utf-8')
