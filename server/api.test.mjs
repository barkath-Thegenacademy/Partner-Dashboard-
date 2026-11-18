import assert from 'node:assert/strict';
import {DatabaseSync} from 'node:sqlite';
import {readFileSync} from 'node:fs';
import {api} from './api.mjs';
const sqlite=new DatabaseSync(':memory:');sqlite.exec(readFileSync('drizzle/0000_shared_board.sql','utf8'));
const env={DB:{prepare(sql){
 let values=[];
 return {
  bind(...v){values=v;return this},
  async first(){return sqlite.prepare(sql).get(...values)},
  async run(){const r=sqlite.prepare(sql).run(...values);return {meta:{changes:Number(r.changes)}}}
 };
}}};
const seed=JSON.parse(readFileSync('web/data.json','utf8')).map(p=>({...p,cohorts:[]}));
const req=(email,revision,partners=seed,origin='https://tga.test')=>new Request('https://tga.test/api/partners',{method:'PUT',headers:{'content-type':'application/json',origin,...(email?{'oai-authenticated-user-email':email,'oai-authenticated-user-id':'test-user'}:{})},body:JSON.stringify({revision,partners})});
assert.equal((await api(req(null,0),env,seed)).status,403);
assert.equal((await api(req('stranger@example.com',0),env,seed)).status,403);
assert.equal((await api(req('sumukh@thegenacademy.com',0,seed,'https://evil.test'),env,seed)).status,403);
assert.equal((await api(req('SUMUKH@THEGENACADEMY.COM',0),env,seed)).status,200);
assert.equal((await api(req('barkath@thegenacademy.com',0),env,seed)).status,409);
const changed=structuredClone(seed);changed[0].cohorts=['dec-jan'];
assert.equal((await api(req('barkath@thegenacademy.com',1,changed),env,seed)).status,200);
const shared=await (await api(new Request('https://tga.test/api/partners'),env,seed)).json();
assert.equal(shared.revision,2);assert.deepEqual(shared.partners[0].cohorts,['dec-jan']);
assert.equal((await api(req('sumukh@thegenacademy.com',2,[...seed,seed[0]]),env,seed)).status,400);
assert.equal((await api(req('sumukh@thegenacademy.com',2,[]),env,seed)).status,400);
console.log('Passed: authorization, origin protection, shared persistence, stale-write conflicts, validation.');
