const editors = new Set(['barkath@thegenacademy.com','sumukh@thegenacademy.com']);
const statuses = ['Confirmed','In discussion','Call Scheduled','Got intro','In Pipeline','Churned'];
const cohorts = ['apr-may','aug-sep','oct-nov','dec-jan'];
const json = (data,status=200) => Response.json(data,{status,headers:{'Cache-Control':'no-store'}});
export function identity(request) {
  const email = (request.headers.get('oai-authenticated-user-email') || '').trim().toLowerCase();
  const authenticated = !!request.headers.get('oai-authenticated-user-id');
  return {email:authenticated?email:null,canEdit:authenticated&&editors.has(email)};
}
export function validate(records) {
  if (!Array.isArray(records)||!records.length||records.length>2000) throw Error('Provide between 1 and 2000 partner records.');
  const ids=new Set(), names=new Set();
  return records.map(p=>{
    if(!p||!Number.isSafeInteger(p.id)||p.id<1||ids.has(p.id))throw Error('Invalid or duplicate partner ID.');
    ids.add(p.id);
    const out={id:p.id,cohort:!!p.cohort};
    for(const k of ['name','poc','status','notes','offer','lecture','followup']) {
      if(typeof p[k]!=='string'||p[k].length>10000)throw Error('Invalid partner field: '+k);
      out[k]=p[k].trim();
    }
    const name=out.name.normalize('NFKC').toLowerCase();
    if(!name||out.name.length>200||names.has(name))throw Error('Partner names must be unique.');
    names.add(name);
    if(!statuses.includes(out.status))throw Error('Invalid status.');
    if(!Array.isArray(p.cohorts)||p.cohorts.some(c=>!cohorts.includes(c)))throw Error('Invalid cohort.');
    out.cohorts=[...new Set(p.cohorts)];return out;
  });
}
export async function api(request,env,seed) {
  const path=new URL(request.url).pathname, user=identity(request);
  if(path==='/api/me')return json(user);
  if(path!=='/api/partners')return json({error:'Not found'},404);
  if(request.method==='GET') {
    const row=await env.DB.prepare('SELECT * FROM shared_board WHERE id = 1').first();
    return json(row?{partners:JSON.parse(row.records),revision:row.revision,updatedAt:row.updated_at}:{partners:seed,revision:0,updatedAt:null});
  }
  if(request.method!=='PUT')return json({error:'Method not allowed'},405);
  if(!user.canEdit)return json({error:'Sign in with an authorized TGA editor account.'},403);
  if(request.headers.get('origin')!==new URL(request.url).origin)return json({error:'Invalid origin'},403);
  if(!request.headers.get('content-type')?.startsWith('application/json'))return json({error:'JSON required'},415);
  let payload,records;
  try {
    const raw=await request.text();if(raw.length>2000000)throw Error('Import is too large.');
    payload=JSON.parse(raw);records=validate(payload.partners);
    if(!Number.isSafeInteger(payload.revision)||payload.revision<0)throw Error('Invalid revision.');
  } catch(e) {return json({error:e.message||'Invalid request'},400);}
  const stamp=new Date().toISOString(), revision=payload.revision+1;
  const result=payload.revision===0
    ?await env.DB.prepare('INSERT OR IGNORE INTO shared_board (id,records,revision,updated_by,updated_at) VALUES (1,?,?,?,?)').bind(JSON.stringify(records),revision,user.email,stamp).run()
    :await env.DB.prepare('UPDATE shared_board SET records = ?, revision = ?, updated_by = ?, updated_at = ? WHERE id = 1 AND revision = ?').bind(JSON.stringify(records),revision,user.email,stamp,payload.revision).run();
  if(!result.meta.changes)return json({error:'Another editor saved changes. Refresh the board, then reapply your changes. Your draft is still available to export.'},409);
  return json({revision,updatedAt:stamp});
}
