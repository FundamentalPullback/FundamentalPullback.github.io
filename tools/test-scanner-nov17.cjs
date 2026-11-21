// Scoped publication contract: public reviewed subset, no new approvals or Stage 4 changes.
const assert=require('node:assert/strict'),fs=require('node:fs'),cp=require('node:child_process'),path=require('node:path'),vm=require('node:vm');
const root=path.resolve(__dirname,'..'),a=require('./load-stock-profiles.cjs')(),{c,t}=a;
const d='2026-11-17',pub='2026-11-18',base='327b4b8fdbedbc9fd3abd3e64a966488abe9f382';
const manifest=c.window.FP_MANIFEST,raw=c.FP.scan.filter(x=>x[0]===d);
const audit=c.window.FP_SCAN_AUDIT[d];
assert.deepEqual([audit.rowCount,audit.priorityCount,audit.researchPool,audit.publishedCount,audit.reviewCount,audit.valuationCount],[200,112,92,29,27,2]);
assert.equal(audit.certifiedClose,false);
assert.equal(audit.schema,'fp.scanner-review-subset.v1');
assert.equal(raw.length,29);assert.equal(new Set(raw.map(x=>x[1])).size,29);
assert(raw.every(x=>x.length===13&&x[10]>=85&&x[3]>0&&[4,5,6,7,8,11,12].every(i=>x[i]===null)));
assert.equal(manifest.scanRows,c.FP.scan.length);assert(manifest.scannerAsOf>=d);
const reports=a.reports.filter(x=>['A597','A598','A599'].includes(x.id));
assert.equal(reports.length,3);assert.equal(new Set(a.reports.map(x=>x.id)).size,a.reports.length);
const tk=new Set();
for(const r of reports){
 assert.equal(r.entryEnabled,false);assert.equal(r.date,pub);assert.equal(r.scannerDate,d);
 for(const p of r.profiles){
  assert(!tk.has(p.ticker));tk.add(p.ticker);assert.equal(p.kind,'partial');assert.equal(p.stage3Complete,false);assert.equal(p.entryApproved,false);assert.equal(p.maximumConditioned,null);
  const profile=a.profiles.find(x=>x.ticker===p.ticker);assert(profile.scanDates.includes(d));assert(profile.analyses.some(x=>x.id===r.id&&!x.isComplete));assert.notEqual(profile.latestCompleted?.id,r.id);
 }
}
assert.deepEqual([...tk].sort(),Array.from(raw,x=>x[1]).sort());
const fullScans=t.S.scan, fullLib=t.S.lib;
t.S.scan=fullScans.filter(x=>x.date<=d);
t.S.lib=fullLib.filter(x=>x.date<=pub);
for(const [symbol,id,price] of [['GXO','A598',54.95],['FLS','A599',79.75]]){
 const r=reports.find(x=>x.id===id),p=r.profiles[0];assert.equal(p.ticker,symbol);assert.equal(p.close.price,price);assert.equal(p.close.sessionDate,d);assert.equal(p.valuation.status,'unavailable');
 for(const lang of ['es','en']){t.setLang(lang);const h=t.renderProfile(t.profiles().find(x=>x.ticker===symbol));assert(h.includes(id));assert(h.includes('data-scan-subset="'+d+'"'));assert(h.includes(lang==='es'?'sin entrada':'no entry'));assert(!h.includes('NaN'));}
}
t.profileRoute('fichas?filter=all&sort=ticker&scans=1');
assert.deepEqual(Array.from(t.profileResults(t.profiles()),p=>p.ticker).sort(),[...tk].sort());
t.S.scan=fullScans;t.S.lib=fullLib;
for(const f of ['data/dec.js','data/ges.js','data/ops.js','data/acct.js','data/hist.js','data/lib-stage4-nov17.js','data/stage35-assessments.json','tools/pending-web-commentary.json']){
 const atScan=cp.execFileSync('git',['show','0ca5fa7:'+f],{cwd:root,maxBuffer:50e6});
 const prior=cp.execFileSync('git',['show',base+':'+f],{cwd:root,maxBuffer:50e6});assert(atScan.equals(prior),f+' unchanged by Nov17 scan publication');
}
const index=fs.readFileSync(root+'/index.html','utf8'),reverted=require('./stage4-tab-contract.cjs').priorHtml(root,index);
assert(reverted.length>0);assert(index.includes('dates.filter(function(x){return !scannerReviewSubset(x);}).reverse()'));
console.log('PASS November 17 scoped publication: 29 distinct profiles, 2 valuation updates, 27 screens, 0 approvals, correct scanner slice, preserved Stage 4 and records.');
