// Presentation-only regression for long bilingual position-status labels.
const fs=require('fs'),path=require('path'),assert=require('assert/strict'),Module=require('module');
const root=path.resolve(__dirname,'..'),html=fs.readFileSync(root+'/index.html','utf8');
for(const rule of ['.pos-card { cursor: default; min-width: 0; }','.pos-card > * { min-width: 0; }','.pos-card .card-top { flex-wrap: wrap; }','.pos-card .card-top > div { min-width: 0; }','.pos-card .card-top .pill { max-width: 100%; white-space: normal; overflow-wrap: anywhere; }'])assert(html.includes(rule),'Scoped shrink/wrapping rule '+rule);
const filename=path.join(__dirname,'load-stock-profiles.cjs'),m=new Module(filename,module);m.filename=filename;m.paths=module.paths;
m._compile(fs.readFileSync(filename,'utf8').replace('profileRoute,renderProfile,','profileRoute,renderProfile,vPosiciones,vCartera,'),filename);
const a=m.exports(root),t=a.t;
// The old HRB-36 / unknown-fee fixture predates the recorded full exit.
// Test current labels, plus a synthetic long label and unknown fee, without
// pretending that the historic position is still open.
const originalGes=JSON.parse(JSON.stringify(t.S.ges)),originalOps=JSON.parse(JSON.stringify(t.S.ops));
for(const lang of ['es','en']){
 t.setLang(lang);let h=t.vPosiciones();assert(h.includes('pos-card'));
 assert(h.includes(lang==='es'?'S manual adoptado; M revalidado ahora':'Manual S adopted; M revalidated now'));
 let p=t.vCartera();assert(!p.includes('+—'));assert(!p.includes('NaN'));
 const long=t.S.ges.find(r=>r.ticker==='ASO'&&r.rep==='A494');
 const prior=[long.state,long.stateEn];long.state='Parcial ejecutada; 36 acciones; sin ampliar';long.stateEn='Partial filled; 36 shares; no add-on';
 h=t.vPosiciones();assert(h.includes(lang==='es'?long.state:long.stateEn));[long.state,long.stateEn]=prior;
 const op=t.S.ops.at(-1),fee=op.fee,notes=op.notes;op.fee=null;op.notes='Comisión no publicada. / Fee not published.';
 p=t.vCartera();assert(p.includes(lang==='es'?'Comisión no publicada':'Fee not published'));assert(!p.includes('+—'));assert(!p.includes('NaN'));op.fee=fee;op.notes=notes;
}
assert.deepEqual(JSON.parse(JSON.stringify(t.S.ges)),originalGes);assert.deepEqual(JSON.parse(JSON.stringify(t.S.ops)),originalOps);
console.log('PASS scoped position-card minimum widths and wrapping; ES/EN source labels retained; unavailable return has no plus prefix. Browser layout QA still required.');
