// Finite exact successor: two audited partial earnings supplements, never arbitrary additions.
const fs=require('fs'),assert=require('assert/strict'),crypto=require('crypto');
const sha=b=>crypto.createHash('sha256').update(b).digest('hex'),clone=x=>JSON.parse(JSON.stringify(x));
function contract(root){return JSON.parse(fs.readFileSync(root+'/tools/trp-bsy-contract.json'));}
function priorDecisionBytes(root){
 const c=contract(root),b=fs.readFileSync(root+'/data/dec.js'),prefix='window.FP=window.FP||{};FP.dec=';
 assert(b.toString().startsWith(prefix)&&b.toString().endsWith('];\n'));
 const rows=JSON.parse(b.toString().slice(prefix.length,-2));assert.equal(rows.length,c.priorDecision.rows+2,'Only two exact decision additions');
 assert.equal(sha(JSON.stringify(rows.slice(c.priorDecision.rows))),c.appendRowsSha256,'Exact two decision rows');
 const old=Buffer.concat([b.subarray(0,c.priorDecision.bytes-3),Buffer.from('];\n')]);assert.equal(sha(old),c.priorDecision.sha256,'Exact complete prior decision bytes');return old;
}
function priorPending(root){
 const c=contract(root),p=JSON.parse(fs.readFileSync(root+'/tools/pending-web-commentary.json'));
 assert.deepEqual({...p,pending:p.pending.slice(0,-2)},c.priorPending,'All prior reconciliation state preserved');
 assert.deepEqual(p.pending.slice(-2).map(x=>x.reportId),c.ids,'Only exact new reconciliation markers');return clone(c.priorPending);
}
function priorResearchIndexBytes(root){const c=contract(root),s=fs.readFileSync(root+'/research/2026-11-05/index.html','utf8');assert.equal(s.split(c.researchIndexAppend).length,2);const old=Buffer.from(s.replace(c.researchIndexAppend,''));assert.equal(sha(old),c.priorResearchIndexSha256,'Exact prior research index');return old;}
function validate(root,loaded){
 const c=contract(root);assert.deepEqual(c.ids,['A286','A287']);assert.equal(sha(fs.readFileSync(root+'/'+c.library)),c.librarySha256);
 assert.equal(sha(fs.readFileSync(root+'/index.html')),c.indexSha256,'UI and trading controls unchanged');
 assert.equal(loaded.reports.length,Object.keys(c.priorReportHashes).length+2);assert.equal(new Set(loaded.reports.map(x=>x.id)).size,loaded.reports.length);
 for(const [id,h] of Object.entries({...c.priorReportHashes,...c.reportHashes})){const r=loaded.reports.find(x=>x.id===id);assert(r,'Required report '+id);assert.equal(sha(JSON.stringify(r)),h,'Exact report '+id);}
 priorDecisionBytes(root);priorPending(root);priorResearchIndexBytes(root);
 const actual=clone(loaded.c.window.FP_MANIFEST),expected=clone(c.priorManifest);expected.libraryFiles.push(c.library);expected.generated=actual.generated;assert.deepEqual(actual,expected,'Only exact library and generated manifest changes');assert(Date.parse(actual.generated)>=Date.parse(c.priorManifest.generated));
 return c;
}
function legacy(root,loaded){
 const c=validate(root,loaded),old=priorDecisionBytes(root).toString(),prefix='window.FP=window.FP||{};FP.dec=';
 loaded.reports=loaded.reports.filter(r=>!c.ids.includes(r.id));loaded.t.S.lib=loaded.reports;loaded.t.S.dec=loaded.t.PARTS.dec(JSON.parse(old.slice(prefix.length,-2)));loaded.c.window.FP_MANIFEST.libraryFiles=loaded.c.window.FP_MANIFEST.libraryFiles.filter(f=>f!==c.library);loaded.profiles=loaded.t.profiles();return loaded;
}
module.exports={validate,priorDecisionBytes,priorPending,priorResearchIndexBytes,legacy};
