// Project the independently validated A494 successor only for dated historical tests.
const fs=require('fs'),assert=require('assert/strict'),crypto=require('crypto'),cp=require('child_process');
const sha=x=>crypto.createHash('sha256').update(x).digest('hex');
function contract(root){return JSON.parse(fs.readFileSync(root+'/tools/stage4-nov9-prior.json'));}
function priorBytes(root,f){
 const c=contract(root),ref=c.historicalSources[f];
 if(!ref)return fs.readFileSync(root+'/'+f);
 if(f==='index.html')assert.equal(sha(fs.readFileSync(root+'/'+f)),c.currentIndexHash,'Reviewed current UI');
 // Resolve immutable, already public source bytes without embedding portfolio history.
 const b=cp.execFileSync('git',['show',ref.revision+':'+f],{cwd:root,maxBuffer:10e6});
 assert.equal(sha(b),ref.sha256,'Exact historical public source '+f);return b;
}
function legacy(root,a){const report=a.reports.find(r=>r.id==='A494');if(!report)return a;const c=contract(root),rows=a.c.FP.ges;assert.equal(a.reports.filter(r=>r.id==='A494').length,1);assert.equal(sha(JSON.stringify(report)),c.reportHash);assert.equal(report.managementResearchOnly,true);assert(report.profiles.every(p=>p.kind==='management'));assert.equal(sha(JSON.stringify(rows.slice(0,c.priorGesRows))),c.priorGesHash);assert.equal(sha(JSON.stringify(rows.filter(r=>r[2]==='A494'))),c.newGesHash);a.reports=a.reports.filter(r=>r.id!=='A494');a.t.S.lib=a.reports;a.c.window.FP_LIB.reports=a.reports;a.c.FP.ges=rows.filter(r=>r[2]!=='A494');a.t.S.ges=a.t.PARTS.ges(a.c.FP.ges);a.c.window.FP_MANIFEST.libraryFiles=a.c.window.FP_MANIFEST.libraryFiles.filter(f=>f!=='data/lib-stage4-nov9.js');a.profiles=a.t.profiles();return a;}
module.exports={legacy,priorBytes};
