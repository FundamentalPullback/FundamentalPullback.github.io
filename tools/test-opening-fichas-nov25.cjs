const assert=require('node:assert/strict'), fs=require('node:fs'), path=require('node:path'), vm=require('node:vm'), crypto=require('node:crypto');
const root=path.resolve(__dirname,'..'), read=f=>fs.readFileSync(path.join(root,f)), sha=x=>crypto.createHash('sha256').update(x).digest('hex');
function load(f){const c={window:{}};vm.runInNewContext(read(f).toString(),c);return JSON.parse(JSON.stringify(c.window.FP_PLAN));}
const p=load('data/plan.js'), prior=load('data/plan/plan-2026-11-23.js');
assert.equal(p.meta.date,'2026-11-24');assert.equal(p.meta.version,'Versión 2.3');assert.equal(sha(read(p.meta.pdf)),'1fa0c89e5eec2938ce017d0b70f36121e1f183b54adf213ab7588d77face5594');
for(const l of ['es','en']){
 const stable=x=>x[l].sections.filter(s=>!['s35a','s35b'].includes(s.id));
 assert.deepEqual(stable(p),stable(prior),'No rules outside the amended subsections changed');
 const a=p[l].sections.find(x=>x.id==='s35a').blocks[4][1], b=prior[l].sections.find(x=>x.id==='s35a').blocks[4][1];
 assert.deepEqual(a[1],b[1]);assert.deepEqual(a[3],b[3]);
 const s=p[l].sections.find(x=>x.id==='s35b').blocks.flat().filter(x=>typeof x==='string').join(' ');
 assert.match(s,/DAY/);assert.match(s,/EMA50/);assert.match(s,l==='es'?/toca o cae por debajo de M/:/touches or falls below M/);
}
const h=read('index.html').toString(), s=h.slice(h.indexOf('  function openingPlansNov25()'),h.indexOf('  function vEntradas()'));
assert(s.length>500);
for(const lang of ['es','en']){
 const c={pt:(a,b)=>lang==='es'?a:b,esc:String};vm.createContext(c);vm.runInContext(s,c);
 const rendered=c.openingPlansNov25();
 assert.match(rendered,/fichas-apertura-title/);assert.match(rendered,/#ficha\/G/);assert.match(rendered,/#ficha\/EPAM/);assert.match(rendered,/#plan/);
 const cells=[...rendered.matchAll(/<td>([^<]+)<\/td>/g)].map(x=>x[1]);
 const usd=n=>new Intl.NumberFormat(lang==='es'?'es-ES':'en-US',{style:'currency',currency:'USD',currencyDisplay:'narrowSymbol',useGrouping:'always',minimumFractionDigits:2,maximumFractionDigits:2}).format(n);
 for(const [i,close,q,e,m,stop] of [[0,42.92,190,43.15,40.52,40.45],[8,161.48,51,158.95,149.89,149.75]]){
  assert.deepEqual(cells.slice(i,i+7),[usd(close),String(q),usd(e),usd(m),usd(stop),usd(q*e),usd(q*(e-stop))]);
 }
 assert.match(rendered,lang==='es'?/No son aprobaciones, órdenes ni ejecuciones/:/No approvals, orders or fills/);
}
console.log('PASS v2.3 source PDF, isolated ES/EN policy changes, public simulation cards, quantity, nominal risk and not-executed labels.');
