const assert=require('assert/strict'),fs=require('fs'),cp=require('child_process'),vm=require('vm');
const a=require('./load-stock-profiles.cjs')(),r=a.reports.find(r=>r.id==='A528');
const c={window:{}};vm.runInNewContext(cp.execFileSync('git',['show','2757327e1fa60961a76a5bee0e9f7facf8126d4c:data/lib-research-sono-nxpi.js'],{encoding:'utf8'}),c);const old=c.window.FP_LIB.reports.find(r=>r.id==='A528');
assert(r.text.endsWith(old.text));assert.equal(r.entryEnabled,false);assert.equal(r.profiles[0].entryApproved,false);assert.equal(r.profiles[0].kind,'partial');assert.equal(r.profiles[0].valuation.status,'unavailable');assert.equal(r.date,'2026-11-11');assert.equal(new Set(a.reports.map(r=>r.id)).size,a.reports.length);assert.deepEqual(JSON.parse(JSON.stringify(a.reports.find(r=>r.id==='A529'))),JSON.parse(JSON.stringify(c.window.FP_LIB.reports.find(r=>r.id==='A529'))));
for(const word of ['570–630','36–37','73–111','ritmo de salida','no resuelven la valoración'])assert(r.text.includes(word));
for(const f of ['data/dec.js','data/ops.js','data/lib-research-sono-nxpi.js','tools/pending-web-commentary.json'])assert(fs.readFileSync(f).equals(cp.execFileSync('git',['show','2757327e1fa60961a76a5bee0e9f7facf8126d4c:'+f],{maxBuffer:200e6})));
console.log('PASS SONO official guidance supplement, prior report and NXPI intact, no approval/valuation/account mutation');

require('./test-history-nov11.cjs'); // Authorized later market-only history append; ledger and prior closes remain protected.
