// Project only the independently validated Nov 12 management successor for dated tests.
const fs=require('fs'),assert=require('assert/strict'),crypto=require('crypto');
const sha=x=>crypto.createHash('sha256').update(x).digest('hex');
function legacy(root,a){
 // Verify the known append-only Nov 13 report, then reconstruct the older fixture.
 const next=a.reports.filter(r=>r.id==='A594');
 if(next.length) {
  assert.equal(next.length,1);
  assert.equal(sha(JSON.stringify(next[0])),'bc05ec43eed320b54639428dc9d5dbd00695f678a003ee8fd0fa2c1a750271db');
  assert(next[0].managementResearchOnly && next[0].profiles.length===6 && next[0].profiles.every(p=>p.kind==='management'&&!p.valuation&&!p.entryApproved&&!p.completedAt));
  a.reports=a.reports.filter(r=>r.id!=='A594');a.t.S.lib=a.reports;a.c.window.FP_LIB.reports=a.reports;
  a.c.window.FP_MANIFEST.libraryFiles=a.c.window.FP_MANIFEST.libraryFiles.filter(f=>f!=='data/lib-stage4-nov13.js');a.profiles=a.t.profiles();
 }
 const rec=a.reports.find(r=>r.id==='A593');if(!rec)return a;
 const p=JSON.parse(fs.readFileSync(root+'/tools/stage4-nov12-prior.json')),rows=a.c.FP.ges;
 assert.equal(a.reports.filter(r=>r.id==='A593').length,1);assert.equal(sha(JSON.stringify(rec)),p.reportHash);
 assert(rec.managementResearchOnly&&rec.profiles.length===6&&rec.profiles.every(p=>p.kind==='management'&&!p.valuation&&!p.entryApproved&&!p.completedAt));
 assert.equal(rows.length,p.priorGesRows+6);assert.equal(sha(JSON.stringify(rows.slice(0,p.priorGesRows))),p.priorGesHash);assert.equal(sha(JSON.stringify(rows.slice(p.priorGesRows))),p.newGesHash);
 a.reports=a.reports.filter(r=>r.id!=='A593');a.t.S.lib=a.reports;a.c.window.FP_LIB.reports=a.reports;a.c.FP.ges=rows.slice(0,p.priorGesRows);a.t.S.ges=a.t.PARTS.ges(a.c.FP.ges);a.c.window.FP_MANIFEST.libraryFiles=a.c.window.FP_MANIFEST.libraryFiles.filter(f=>f!=='data/lib-stage4-nov12.js');a.profiles=a.t.profiles();return a;
}
module.exports={legacy};
