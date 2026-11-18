from pathlib import Path
import json,base64
p=Path('dist')
h=(p/'index.html').read_text(encoding='utf-8')
h=h.replace('<div class="brand"><b>✳</b> The Gen Academy</div>','<div class="brand"><img src="tga-logo.png" alt="The Gen Academy" width="190" height="53"></div>')
h=h.replace('<script src="app.js"></script>','<script id="partner-data" type="application/json">'+(p/'data.json').read_text(encoding='utf-8')+'</script><script src="app.js"></script>')
h=h.replace('Confirmed partners − subsequent churn','Active confirmed partners; churn excluded')
h=h.replace('<div class="filters">','<div class="filters"><label class="sr-only" for="search">Search partners, contacts or notes</label>')
h=h.replace('<span id="count"></span>','<span id="count" aria-live="polite"></span>')
h=h.replace('<div class="table-wrap">','<div id="search-feedback" aria-live="polite"></div><div class="table-wrap">')
h=h.replace('<button id="clear">Clear filters</button>','<button id="clear">Clear filters</button><button id="sort" aria-label="Sort partners alphabetically">Name A–Z ↕</button>')
(p/'index.html').write_text(h,encoding='utf-8')
j=(p/'app.js').read_text(encoding='utf-8')
domain={'OpenAI':'openai.com','Replit':'replit.com','Fireworks AI':'fireworks.ai','LlamaIndex':'llamaindex.ai','ElevenLabs':'elevenlabs.io','Nebius':'nebius.com','Pinecone':'pinecone.io','Mem0':'mem0.ai','Langfuse':'langfuse.com','Keenable':'keenable.ai','NVIDIA / Brev':'nvidia.com','Arize':'arize.com','Composio':'composio.dev','Granola':'granola.ai','OpenRouter':'openrouter.ai','Emergent':'emergent.sh','Context':'context.dev','Gamma':'gamma.app','Exa':'exa.ai','Agora':'agora.io','Gemini':'gemini.google.com','CodeRabbit':'coderabbit.ai','Sarvam':'sarvam.ai'}
j=j.replace("const key='tga-partners-v1';let partners=[],view='overview';", "const key='tga-partners-v1';let partners=[],view='overview',sortAsc=false;")
j=j.replace("const actionable=",'const domains='+json.dumps(domain)+';\nconst companyLogo=p=>`<span class="logo company-logo">${domains[p.name]?`<img src="https://www.google.com/s2/favicons?domain=${encodeURIComponent(domains[p.name])}&sz=64" alt="${esc(p.name)} logo" loading="lazy" referrerpolicy="no-referrer" onerror="this.hidden=true;this.nextElementSibling.hidden=false"><span hidden>${esc(p.name.slice(0,2).toUpperCase())}</span>`:esc(p.name.slice(0,2).toUpperCase())}</span>`;\nconst actionable=')
j=j.replace('<span class="logo">${esc(p.name.slice(0,2).toUpperCase())}</span>','${companyLogo(p)}')
j=j.replace("$('count').textContent=list.length+' partners';", "if(sortAsc)list.sort((a,b)=>a.name.localeCompare(b.name));$('search-feedback').textContent=q?`Found ${list.length} partner${list.length===1?'':'s'} matching “${$('search').value}”`:'';$('count').textContent=list.length+' partners';")
j=j.replace("$('add').onclick=()=>edit(null);", "$('add').onclick=()=>edit(null);$('sort').onclick=()=>{sortAsc=!sortAsc;$('sort').textContent=sortAsc?'Sheet order ↕':'Name A–Z ↕';render();};")
j=j.replace("const source=await fetch('data.json');if(!source.ok)throw Error();const seed=await source.json();", "const seed=JSON.parse($('partner-data').textContent);")
j=j.replace("partners=Array.isArray(saved)?saved:seed;", "partners=Array.isArray(saved)&&saved.every(p=>p&&typeof p.name==='string'&&typeof p.id==='number'&&statuses.includes(p.status))?saved:seed;")
j=j.replace("$('save-status').textContent='Could not load partner data. Reload to try again.';", "$('save-status').textContent='Could not load partner data. Please reopen the dashboard.';console.error('Dashboard initialization failed');")
j=j.replace("document.querySelectorAll('[data-view]').forEach", "document.querySelectorAll('[data-view]').forEach",1)
(p/'app.js').write_text(j,encoding='utf-8')
css=(p/'style.css').read_text(encoding='utf-8')
css=css[css.index('\n')+1:]
css="@import url('https://fonts.googleapis.com/css2?family=Geist:wght@400;500;600;700;800&display=swap');\n"+css
css+='''
/* TGA Phase 1: off-white, purple and periwinkle; light surfaces throughout. */
:root{font-family:Geist,Arial,sans-serif;background:#fafaf1;color:#343443;--purple:#6170ff;--muted:#737383}
body{background:#fafaf1}h1,h2,.metrics strong{font-family:Geist,Arial,sans-serif}aside{background:#fafaf1;border-color:#e6e6e6}.brand img{width:190px;height:auto;display:block;mix-blend-mode:multiply}.workspace{margin-top:36px;color:#737383}nav button{color:#68687b}nav .selected{background:#eceeff;color:#4c58b9}.avatar{background:#f0f1ff;color:#5963ac}
main{background:linear-gradient(135deg,#fafaf1 0%,#fff 65%,#f5f5ff 100%);min-height:100vh}.sourcebar{background:#f3f4ff;border-color:#e6e8ff;color:#656579}.sourcebar span:first-child{color:#59596b}.metrics .hero{background:#eff0ff;border:1px solid #dfe2ff;color:#4a50a0;position:relative;overflow:hidden}.hero>div>span{background:#fff;color:#5962bb}.metrics .hero strong{color:#6170ff}.hero p{color:#65688b}.hero-footer{border-color:#dce0fc;color:#6a6e99}.hero-footer span{color:#7d83ff}.metrics article:nth-child(2){background:#fffdf0;border-color:#f0eddb}.metrics article:nth-child(3){background:#f5f5ff;border-color:#e9e8fc}.metrics article:nth-child(4){background:#fff7f3;border-color:#f5e7df}.metrics article{box-shadow:0 4px 16px #6b70a004}.metrics article>div:first-child{color:#646477}.metrics article p{color:#717182}.mini{color:#777787;border-color:#e5e6ef}.panel{border-color:#e8e8ee;box-shadow:0 3px 14px #77779903}.primary{background:#e6e9ff;color:#4d56b3;border:1px solid #d5dafe}.primary:hover{background:#dce1ff;color:#414a9f}.bar-fill{background:#cdd1ff}.bar-row:first-child .bar-fill{background:#a9afff}th{background:#f6f7ff;color:#676779}.logo{background:#fff;border:1px solid #eeeef2;color:#777c9f}.company-logo{width:38px;height:38px;border-radius:10px;padding:7px}.company-logo img{width:24px;height:24px;object-fit:contain}.badge{background:#f1f1ff;color:#655ca1}.badge.confirmed{background:#edf8f1;color:#387653}.badge.churned{background:#fff0ee;color:#a9554f}td:nth-child(4),td:nth-child(5),td:nth-child(6){color:#686878}td button{font-size:12px}.footnote{color:#727282}.subtext{color:#737382}.table-footer{color:#777787}footer{color:#7a7b89}input:focus,select:focus,textarea:focus,button:focus-visible{outline:3px solid #cdd1ff;outline-offset:2px}input,select,textarea{color:#4b4b60}#search{font-size:13px;padding:12px;background:#fff;border-color:#dcdff5}#search-feedback{font-size:12px;padding:0 23px 14px;color:#6570bd}#search-feedback:empty{display:none}.sr-only{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0,0,0,0)}#toast{background:#f0f2ff;color:#4b53a2;border:1px solid #d5dafb;box-shadow:0 8px 35px #737ca333}dialog::backdrop{background:#cacfe777;backdrop-filter:blur(3px)}
@media(max-width:1100px){.brand img{width:160px}}@media(max-width:700px){.brand img{width:170px}.sourcebar{font-size:10px}.metrics article>div:first-child{font-size:9px}.metrics .hero strong{font-size:44px}}
'''
(p/'style.css').write_text(css,encoding='utf-8')
