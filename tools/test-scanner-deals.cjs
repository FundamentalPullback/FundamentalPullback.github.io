const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict'),Module=require('node:module');
const filename=path.join(__dirname,'load-stock-profiles.cjs'),m=new Module(filename,module);m.filename=filename;m.paths=module.paths;
m._compile(fs.readFileSync(filename,'utf8').replace('profileRoute,renderProfile,','profileRoute,renderProfile,vEscaner,'),filename);
const {t,c}=m.exports(path.resolve(__dirname,'..'));const day='2026-11-20',keys=Object.keys(c.window.FP_SCAN_DEALS[day].targets);
assert.deepEqual(keys.sort(),['LCII','LNTH','MKTX','QGEN','RRC']);
t.S.scanDate=day;
for(const lang of ['es','en']){
 t.setLang(lang);
 t.S.onlyS2=false;t.S.dealTargetsOnly=false;
 let h=t.vEscaner();
 assert(h.includes('id="scan-deal-toggle"'));
 assert(h.includes('<span class="status">173</span>'));
 for(const k of keys)assert(!h.includes('>'+k+'</td>'),k);
 for(const k of ['PATK','KMB','CPAY','G'])assert(h.includes('>'+k+'</td>'),k);
 t.S.onlyS2=true;t.S.dealTargetsOnly=true;
 h=t.vEscaner();
 assert(h.includes('<span class="status">5</span>'));
 for(const k of keys)assert(h.includes('>'+k+'</td>'),k);
 for(const k of ['PATK','KMB','CPAY','G'])assert(!h.includes('>'+k+'</td>'),k);
 assert(h.includes('role="')||h.includes('aria-label='));
 assert(!h.includes('id="only-s2"'));
}
assert(c.FP.scan.filter(r=>r[0]===day).length===178);
t.S.scanDate='2026-11-10';t.S.dealTargetsOnly=true;
assert(!t.vEscaner().includes('id="scan-deal-toggle"'));
console.log('PASS dated takeover routing: all five names diverted before ranking, originals archived, acquirers retained, older cohorts unchanged.');
