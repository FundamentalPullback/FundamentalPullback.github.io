const assert=require('node:assert/strict'),fs=require('node:fs'),cp=require('node:child_process'),path=require('node:path');
const {c,t,reports,profiles}=require('./load-stock-profiles.cjs')();
const d='2026-11-20', by=new Map(profiles.map(x=>[x.ticker,x]));
const rows=c.FP.scan.filter(x=>x[0]===d);
assert.equal(rows.length,178);
assert.equal(new Set(rows.map(x=>x[1])).size,178);
assert.equal(rows.filter(x=>x[10]>=85).length,98);
assert.equal(rows.filter(x=>x[7]===null&&x[8]===null).length,77);
assert(rows.every(x=>x.length===13&&x[12]===null));
assert.equal(c.window.FP_MANIFEST.scanRows,c.FP.scan.length);
assert.equal(c.window.FP_MANIFEST.scannerAsOf,d);
assert.equal(c.window.FP_SCAN_AUDIT[d].certifiedClose,false);
assert.equal(new Set(reports.map(r=>r.id)).size,reports.length);
const ix=reports.find(x=>x.id==='A604');
assert(ix.text.includes('178 of 178'));
rows.forEach((row,i)=>{
 const id='A'+(605+i), report=reports.find(x=>x.id===id),m=report.profiles[0],p=by.get(row[1]);
 assert.equal(report.scannerDate,d);
 assert.equal(report.entryEnabled,false);
 assert.equal(m.ticker,row[1]);
 assert.equal(m.scanner.price,row[3]);
 assert.equal(m.entryApproved,false);
 assert.equal(m.operativeStop,null);
 assert.equal(m.latestCompletedEligible,false);
 assert(ix.text.includes('#biblioteca/'+id+')'));
 assert(report.text.includes('## Valuation'));
 assert(report.text.includes('## Revisit condition'));
 assert(/\]\(https:\/\//.test(report.text));
 assert(p.scanDates.includes(d));
 assert(p.analyses.some(x=>x.id===id));
 assert.notEqual(p.latestCompleted?.id,id);
});
for(const sym of ['G','MKTX','FTDR','RRC']){
 const p=by.get(sym); for(const lang of ['es','en']){t.setLang(lang);const h=t.renderProfile(p);assert(h.includes(sym));assert(!h.includes('NaN'));}
}
t.profileRoute('fichas?filter=all&sort=ticker&scans=1');
assert.deepEqual(Array.from(t.profileResults(t.profiles()),x=>x.ticker).sort(),Array.from(rows,x=>x[1]).sort());
const root=path.resolve(__dirname,'..');
for(const f of ['dec.js','ges.js','ops.js','acct.js','hist.js','stage35-assessments.json','lib-stage4-nov20.js']){
 const old=cp.execFileSync('git',['show','dd0d359bd640fcf9203f96f4ca3df33a2a60bdcb:data/'+f],{cwd:root,maxBuffer:50e6});
 assert(old.equals(fs.readFileSync(root+'/data/'+f)),f+' preserved');
}
console.log('PASS November 21 upload: 178 unique and individually linked reports, 98 high-opportunity, missing metrics retained, no completion or execution claims.');
