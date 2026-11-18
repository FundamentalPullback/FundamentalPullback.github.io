// Project only the exact reviewed Nov17 scanner append before comparing frozen historical fixtures.
const fs=require('node:fs'),assert=require('node:assert/strict'),crypto=require('node:crypto');
const sha=x=>crypto.createHash('sha256').update(JSON.stringify(x)).digest('hex');
function legacy(root,a){
 const p=JSON.parse(fs.readFileSync(root+'/tools/scanner-nov17-prior.json'));
 const manifest=a.c.window.FP_MANIFEST;if(!manifest.files.includes(p.scanFile))return a;
 const ids=new Set(Object.keys(p.reportHashes)),added=a.reports.filter(r=>ids.has(r.id));
 assert.equal(added.length,3);assert.equal(new Set(added.map(r=>r.id)).size,3);
 for(const r of added)assert.equal(sha(r),p.reportHashes[r.id]);
 const rows=a.c.FP.scan.filter(x=>x[0]===p.date);
 assert.equal(rows.length,29);assert.equal(sha(rows),p.rowsHash);
 assert.equal(sha(a.c.window.FP_SCAN_AUDIT[p.date]),p.auditHash);
 a.reports=a.reports.filter(r=>!ids.has(r.id));a.t.S.lib=a.reports;a.c.window.FP_LIB.reports=a.reports;
 a.c.FP.scan=a.c.FP.scan.filter(x=>x[0]!==p.date);a.t.S.scan=a.t.PARTS.scan([a.c.FP.scanHead].concat(a.c.FP.scan));
 delete a.c.window.FP_SCAN_AUDIT[p.date];
 manifest.files=manifest.files.filter(x=>x!==p.scanFile);
 manifest.libraryFiles=manifest.libraryFiles.filter(x=>x!==p.libraryFile);
 manifest.scanRows-=rows.length;assert.equal(manifest.scanRows,p.priorRows);
 manifest.scannerAsOf='2026-11-10';
 a.profiles=a.t.profiles();
 return a;
}
module.exports={legacy};
