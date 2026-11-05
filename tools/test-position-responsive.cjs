// Presentation-only regression for long bilingual position-status labels.
const fs=require('fs'),path=require('path'),assert=require('assert/strict'),Module=require('module');
const root=path.resolve(__dirname,'..'),html=fs.readFileSync(root+'/index.html','utf8');
for(const rule of ['.pos-card { cursor: default; min-width: 0; }','.pos-card > * { min-width: 0; }','.pos-card .card-top { flex-wrap: wrap; }','.pos-card .card-top > div { min-width: 0; }','.pos-card .card-top .pill { max-width: 100%; white-space: normal; overflow-wrap: anywhere; }'])assert(html.includes(rule),'Scoped shrink/wrapping rule '+rule);
const filename=path.join(__dirname,'load-stock-profiles.cjs'),m=new Module(filename,module);m.filename=filename;m.paths=module.paths;
m._compile(fs.readFileSync(filename,'utf8').replace('profileRoute,renderProfile,','profileRoute,renderProfile,vPosiciones,vCartera,'),filename);
const a=m.exports(root),t=a.t;
for(const lang of ['es','en']){t.setLang(lang);const h=t.vPosiciones();assert(h.includes('pos-card'));assert(h.includes(lang==='es'?'Parcial ejecutada; 36 acciones; sin ampliar':'Partial filled; 36 shares; no add-on'));const p=t.vCartera();assert(!p.includes('+—'),'No plus sign for unavailable return');assert(!p.includes('NaN'));assert(p.includes(lang==='es'?'Comisión no publicada':'Fee not published'));}
console.log('PASS scoped position-card minimum widths and wrapping; ES/EN source labels retained; unavailable return has no plus prefix. Browser layout QA still required.');
