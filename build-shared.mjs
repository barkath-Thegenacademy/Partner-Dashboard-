import {readFileSync,writeFileSync,mkdirSync,copyFileSync} from 'node:fs';
const assets={};
for(const [file,type] of [['index.html','text/html; charset=utf-8'],['app.js','text/javascript; charset=utf-8'],['style.css','text/css; charset=utf-8'],['tga-logo.png','image/png']])assets['/'+file]={type,data:readFileSync('web/'+file).toString('base64')};
assets['/']=assets['/index.html'];
const seed=JSON.parse(readFileSync('web/data.json','utf8')).map(p=>({...p,cohorts:p.cohorts||[]}));
const source=readFileSync('server/api.mjs','utf8')+`\nconst assets=${JSON.stringify(assets)};const seed=${JSON.stringify(seed)};\nexport default {async fetch(request,env){try{const path=new URL(request.url).pathname;if(path.startsWith('/api/'))return await api(request,env,seed);const asset=assets[path];if(!asset)return new Response('Not found',{status:404});return new Response(Uint8Array.from(atob(asset.data),c=>c.charCodeAt(0)),{headers:{'Content-Type':asset.type,'Cache-Control':'no-cache','X-Content-Type-Options':'nosniff'}});}catch{return Response.json({error:'Shared storage is temporarily unavailable. Please retry.'},{status:503,headers:{'Cache-Control':'no-store'}});}}};\n`;
mkdirSync('dist/server',{recursive:true});writeFileSync('dist/server/index.js',source);
for(const file of ['index.html','app.js','style.css','tga-logo.png','data.json'])copyFileSync('web/'+file,'dist/'+file);
