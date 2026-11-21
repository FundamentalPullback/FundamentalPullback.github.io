const assert=require('node:assert/strict'), fs=require('node:fs'), cp=require('node:child_process'), path=require('node:path');
const root=path.resolve(__dirname,'..'),base='f4fd7640984c1813171ba6a8ecc2c61b1f2e5bc6';
const {reports,profiles}=require('./load-stock-profiles.cjs')();
const dir=path.join(root,'research/2026-11-21/full-valuations');
const calc=(k)=>JSON.parse(cp.execFileSync(process.execPath,[path.join(dir,'fp-'+k+'-full.cjs')],{encoding:'utf8'}));
const br=calc('br'),axs=calc('axs');
const round=x=>Math.round(x*100)/100;
assert.equal(br.results.base.years.length,10);
assert(axs.every(x=>x.path.length===5&&Math.abs(x.fv-x.riFV)<1e-9));
assert(br.results.base.value<181.41);assert(axs.find(x=>x.key==='base').fv<106.40);
for (const [tk,id,price,values] of [['BR','A783',181.41,['bear','base','bull'].map(k=>br.results[k].value)],['AXS','A784',106.40,axs.map(x=>x.fv)]]) {
 const r=reports.find(r=>r.id===id), m=r.profiles[0];
 assert.equal(m.ticker,tk);assert.equal(m.close.price,price);
 assert.equal(m.valuation.status,'conditional');
 assert.deepEqual([m.valuation.bear,m.valuation.base,m.valuation.bull],values.map(round));
 assert.equal(r.entryEnabled,false);assert.equal(m.entryApproved,false);assert.equal(m.stage35Approved,false);
 assert.equal(profiles.find(p=>p.ticker===tk).latestCompleted.id,id);
 assert(r.text.includes('Reproducibility'));
}
for(const f of ['data/dec.js','data/ges.js','data/ops.js','data/acct.js','data/hist.js','data/stage35-assessments.json','data/lib-stage4-nov20.js','data/scan-5359.js']){
 const old=cp.execFileSync('git',['show',base+':'+f],{cwd:root,maxBuffer:50e6});
 assert(old.equals(fs.readFileSync(root+'/'+f)),f+' preserved');
}
console.log('PASS sourced valuations reproduce exactly, profile links to complete reviews; no approval, ledger, quote or scan-record mutation.');
