from pathlib import Path
import re
p=Path('dist/app.js');s=p.read_text(encoding='utf-8')
start=s.index('function showCurrentCohort()');end=s.index("const key=",start)
s=s[:start]+'''const COHORTS=[{id:'apr-may',label:'April–May'},{id:'aug-sep',label:'August–September'},{id:'oct-nov',label:'October–November'},{id:'dec-jan',label:'December–January'}];
const memberships=p=>Array.isArray(p.cohorts)?p.cohorts.filter(c=>COHORTS.some(x=>x.id===c)):[];
const inCohort=(p,id)=>!id||(id==='unassigned'?memberships(p).length===0:memberships(p).includes(id));
const cohortLabel=id=>COHORTS.find(c=>c.id===id)?.label||'Unassigned';
function chooseCohort(id){$('cohort-filter').value=id;['search','status'].forEach(k=>$(k).value='');render();}
function showCurrentCohort(){setView('directory');$('cohort-filter').focus();}
const cohortCard=$('cohort').closest('article');cohortCard.setAttribute('role','button');cohortCard.setAttribute('tabindex','0');cohortCard.setAttribute('aria-label','View cohort partners');cohortCard.style.cursor='pointer';cohortCard.addEventListener('click',showCurrentCohort);cohortCard.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();showCurrentCohort();}});
''' + s[end:]
s=s.replace("p.cohort?'current cohort':'not marked current'", "memberships(p).map(cohortLabel).join(' ')||'unassigned'")
start=s.index('function render(){');end=s.index("$('bars').innerHTML",start)
s=s[:start]+'''function render(){const selected=$('cohort-filter').value;const scoped=partners.filter(p=>inCohort(p,selected));const confirmed=scoped.filter(p=>p.status==='Confirmed').length,current=scoped.filter(p=>memberships(p).length>0).length,pipeline=scoped.filter(p=>p.status!=='Confirmed'&&p.status!=='Churned').length;
$('net').textContent=confirmed;$('cohort').textContent=selected?scoped.length:current;$('cohort-kpi-title').textContent=selected?'PARTNERS IN VIEW':'ASSIGNED TO COHORTS';$('cohort-kpi-caption').textContent=selected?cohortLabel(selected):'Unique partners with cohort assignments';$('pipeline').textContent=pipeline;$('attention').textContent=scoped.filter(actionable).length;$('coverage').textContent=selected?'Click to view partner details':`${partners.length-current} partners still unassigned`;$('total').textContent=scoped.length+' organizations';$('scope-label').textContent=selected?cohortLabel(selected):'All cohorts';
$('cohort-tabs').innerHTML=[{id:'',label:'All partners'},...COHORTS,{id:'unassigned',label:'Unassigned'}].map(c=>`<button type="button" class="cohort-tab ${selected===c.id?'active':''}" data-cohort="${c.id}" aria-pressed="${selected===c.id}"><span>${esc(c.label)}</span><b>${partners.filter(p=>inCohort(p,c.id)).length}</b></button>`).join('');
$('assignment-note').hidden=!partners.some(p=>p.cohort&&memberships(p).length===0);
''' + s[end:]
s=s.replace("partners.some(p=>p.status===s)","scoped.some(p=>p.status===s)")
s=s.replace("let n=partners.filter(p=>p.status===s).length", "let n=scoped.filter(p=>p.status===s).length")
s=s.replace('partners.length?n/partners.length*100:0','scoped.length?n/scoped.length*100:0')
s=s.replace('const actions=partners.filter(actionable)','const actions=scoped.filter(actionable)')
s=s.replace("(!c||(c==='current'?p.cohort===true:p.cohort!==true))",'inCohort(p,c)')
s=re.sub(r'<span class="cohort">\$\{p\.cohort\?.*?</span>', '<span class="cohort">${memberships(p).length?memberships(p).map(id=>`<span class="cohort-tag">${esc(cohortLabel(id))}</span>`).join(\'\'):\'Unassigned\'}</span>',s)
s=s.replace("$('edit-cohort').checked=p.cohort;", "$('edit-cohort').checked=!!p.cohort;$('edit-cohorts').innerHTML=COHORTS.map(c=>`<label class=\"check\"><input type=\"checkbox\" name=\"partner-cohort\" value=\"${c.id}\" ${memberships(p).includes(c.id)?'checked':''}> ${esc(c.label)}</label>`).join('');")
s=s.replace("cohort:$('edit-cohort').checked};", "cohort:$('edit-cohort').checked,cohorts:[...document.querySelectorAll('input[name=\"partner-cohort\"]:checked')].map(el=>el.value)};")
s=s.replace("document.addEventListener('click',e=>{let b=", "document.addEventListener('click',e=>{let tab=e.target.closest('[data-cohort]');if(tab){chooseCohort(tab.dataset.cohort);return;}let b=")
s=s.replace("'Follow-up date'],...partners", "'Follow-up date','Cohorts'],...partners")
s=s.replace("p.offer,p.lecture,p.followup])", "p.offer,p.lecture,p.followup,memberships(p).map(cohortLabel).join(' | ')])")
s=s.replace("followup:v('Follow-up date')};", "followup:v('Follow-up date'),...(headers.includes('Cohorts')?{cohorts:v('Cohorts').split('|').map(x=>{if(!x.trim())return null;let c=COHORTS.find(c=>normalize(c.label).replace(/[–—]/g,'-')===normalize(x).replace(/[–—]/g,'-')||c.id===normalize(x));if(!c)throw Error('Unknown cohort: '+x);return c.id;}).filter(Boolean)}:{})};")
s=s.replace("partners[i]={...p,id:partners[i].id}", "partners[i]={...partners[i],...p,id:partners[i].id}")
s=s.replace("let index=h=>headers.indexOf(h)","let index=h=>headers.indexOf(h)")
s=s.replace("}catch{partners=seed;}render();", "}catch{partners=seed;}partners=partners.map(p=>({...p,cohorts:memberships(p)}));render();")
p.write_text(s,encoding='utf-8')
p=Path('dist/index.html');h=p.read_text(encoding='utf-8')
h=h.replace('<div id="overview">','''<section class="cohort-section" aria-label="Cohort boards"><div class="cohort-heading"><div><h2>Cohort boards</h2><p>Select a cohort to see its partners, pipeline, and next steps.</p></div><span id="scope-label">All cohorts</span></div><div id="cohort-tabs" class="cohort-tabs"></div><p id="assignment-note" class="assignment-note">The sheet marks 11 partners as “current” without a date range. They remain Unassigned until you select their cohorts in partner details.</p></section><div id="overview">''')
h=h.replace('<div>CURRENT COHORT</div>','<div id="cohort-kpi-title">ASSIGNED TO COHORTS</div>').replace('<p>Partners supporting this cohort</p>','<p id="cohort-kpi-caption">Unique partners with cohort assignments</p>')
h=h.replace('<option value="current">Current cohort</option><option value="other">Not in current cohort</option>','<option value="apr-may">April–May</option><option value="aug-sep">August–September</option><option value="oct-nov">October–November</option><option value="dec-jan">December–January</option><option value="unassigned">Unassigned</option>')
h=h.replace('<th>CURRENT COHORT</th>','<th>COHORTS</th>')
h=h.replace('<label class="check"><input id="edit-cohort" type="checkbox"> Current cohort partner</label>','<input id="edit-cohort" type="checkbox" hidden><fieldset class="cohort-fieldset"><legend>Cohorts</legend><p>Select every cohort this partner supports.</p><div id="edit-cohorts"></div></fieldset>')
p.write_text(h,encoding='utf-8')
p=Path('dist/style.css');css=p.read_text(encoding='utf-8');css+='''
.cohort-section{margin:0 0 26px}.cohort-heading{display:flex;justify-content:space-between;gap:20px;align-items:center;margin-bottom:15px}.cohort-heading p{font-size:12px}.cohort-heading>span{font-size:11px;color:#6170bb;background:#eff0ff;padding:7px 11px;border-radius:6px}.cohort-tabs{display:grid;grid-template-columns:repeat(3,1fr);gap:10px}.cohort-tab{display:flex;justify-content:space-between;align-items:center;background:#fff;border:1px solid #e5e6ee;padding:15px;text-align:left;font-size:12px}.cohort-tab b{background:#f5f5fc;padding:4px 9px;border-radius:5px;font-size:15px;color:#7376a4}.cohort-tab.active{background:#edf0ff;border-color:#a9afff;color:#4f5cb1}.cohort-tab.active b{background:#fff;color:#6170ff}.assignment-note{font-size:11px;background:#fffcee;border:1px solid #f0ecd5;padding:11px 14px;border-radius:7px;color:#7c7564;margin-top:12px}.cohort-fieldset{border:1px solid #e5e6f1;border-radius:8px;padding:13px;margin:0 0 16px}.cohort-fieldset legend{font-weight:600;font-size:12px}.cohort-fieldset p{font-size:11px;margin:0 0 12px}#edit-cohorts{display:grid;grid-template-columns:1fr 1fr;gap:8px}#edit-cohorts label{margin:0;padding:8px;background:#f7f8ff;border-radius:6px;font-size:11px}.cohort-tag{display:inline-block;padding:4px 7px;background:#f1f2ff;color:#626ba8;border-radius:5px;margin:2px;font-size:10px}.metrics article[role=button]:hover{outline:2px solid #cdd1ff}.metrics article[role=button]:focus-visible{outline:3px solid #a9afff}@media(max-width:700px){.cohort-tabs{grid-template-columns:1fr 1fr}.cohort-heading{align-items:flex-start}.cohort-tab{font-size:11px;padding:12px}}
''';p.write_text(css,encoding='utf-8')
