// Presentation-only contracts for the entry-plan archive. No browser or network required.
const fs=require('fs'),vm=require('vm'),assert=require('assert/strict'),path=require('path');
const root=path.resolve(__dirname,'..'),loaded=require('./load-stock-profiles.cjs')(root),html=loaded.html;
const r=loaded.reports.find(x=>x.id==='A278'),clone=x=>JSON.parse(JSON.stringify(x));
assert(r&&r.entryPlan,'Published prospective fixture exists');
const original=JSON.stringify(loaded.reports);
let language='en',clock='2026-11-05T12:45:00Z';
class ArchiveClock extends Date { constructor(...args){super(...(args.length?args:[clock]));} static now(){return Date.parse(clock);} }
const escape=s=>String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/"/g,'&quot;');
const c={window:{FP_PROFILE_ENGINE:loaded.engine},S:{lib:loaded.reports,libState:'ok'},document:{addEventListener:()=>{}},location:{hash:''},URLSearchParams,Date:ArchiveClock,encodeURIComponent,decodeURIComponent,isFinite,pt:(a,b)=>language==='es'?a:b,esc:escape,head:(a,b)=>a+b,ensureLib:()=>{},loadingBlock:()=>'<p>Loading fixture</p>',notice:(a,b,action)=>'<p>'+a+' '+b+'</p>'+(action||''),t:()=>({all:'All',retry:'Retry'}),reportLink:(id,label)=>'<a class="btn" href="#biblioteca/'+id+'">'+label+'</a>'};
vm.createContext(c);vm.runInContext(html.slice(html.indexOf('  function isEntryPlan'),html.indexOf('  /* ---------- library ---------- */')),c);
function render(route,lang='en'){language=lang;c.entryPlanRoute(route);return c.vEntradas();}
function decoded(s){return s.replace(/&quot;/g,'"').replace(/&lt;/g,'<').replace(/&amp;/g,'&');}
function proseText(s){return [...s.matchAll(/<p>([\s\S]*?)<\/p>/g)].map(x=>decoded(x[1])).join(' ');}
function semanticChecks(out){
 const ids=[...out.matchAll(/\bid="([^"]+)"/g)].map(x=>x[1]);assert.equal(new Set(ids).size,ids.length,'No duplicate IDs');
 for(const match of out.matchAll(/\b(?:aria-labelledby|for)="([^"]+)"/g))for(const id of match[1].split(' '))assert(ids.includes(id),'Accessible label target '+id);
 for(const svg of out.matchAll(/<svg\b[^>]*>/g)){assert(svg[0].includes('aria-hidden="true"'));assert(svg[0].includes('focusable="false"'));}
 assert(out.includes('alt="" aria-hidden="true"'),'Decorative emblem has empty alternative text');
 const stack=[],voids=new Set(['input','img','br','path','rect','circle']);
 for(const match of out.matchAll(/<(\/)?([a-z][a-z0-9]*)\b([^>]*)>/gi)){
  const [,close,tag,attrs]=match;if(voids.has(tag)||/\/$/.test(attrs))continue;
  if(close)assert.equal(stack.pop(),tag,'Balanced markup at '+tag);else stack.push(tag);
 }
 assert.equal(stack.length,0,'All rendered elements close');
}
for(const lang of ['es','en']){
 let list=render('entradas?q=ctsh&state=pending',lang);semanticChecks(list);
 assert(list.includes('entry-hero'));assert(list.includes('entry-card'));assert(list.includes('entry-state--pending'));
 assert(list.includes('PUBLIC_FINAL_V2'));assert(list.includes('CTSH'));assert(list.includes('entry-primary'));
 assert(list.includes(escape(c.entryPlanHash(r.entryPlan.id,'ctsh','pending'))));
 for(const value of [r.entryPlan.signal.closeGt,r.entryPlan.signal.closeLte,r.entryPlan.levels.cap,r.entryPlan.levels.M,r.entryPlan.levels.S,r.entryPlan.expiresAt])assert(list.includes(String(value)),'Existing published value '+value);
 assert(list.includes(lang==='es'?'Niveles propuestos e inactivos':'Proposed inactive levels'));
 assert(list.includes(lang==='es'?'No hay ejecución ni orden registrada':'No execution or order is recorded'));
 const detail=render('entradas/'+r.entryPlan.id+'?q=ctsh&state=pending',lang);semanticChecks(detail);
 for(const cls of ['entry-hero--detail','entry-detail-head','entry-levels','entry-facts','entry-prose','entry-events','entry-source-links'])assert(detail.includes(cls));
 assert(detail.includes(escape('#entradas?q=ctsh&state=pending')),'Return to archive retains exact filters');
 for(const id of [r.id,r.entryPlan.predecessorReportId])assert(detail.includes('#biblioteca/'+id));
 for(const url of [r.profiles[0].studyUrl,r.profiles[0].publicSupportUrl,r.entryPlan.events[0].source])assert(detail.includes(escape(url)));
 const prose=detail.match(/<div class="entry-prose">([\s\S]*?)<\/div>/)[1];
 assert.equal(proseText(prose),lang==='es'?r.profiles[0].summary:r.profiles[0].summaryEn,'Paragraph breaks preserve every word and number of the original summary');
 assert((prose.match(/<p>/g)||[]).length>1,'Long source prose is broken into readable paragraphs');
 assert.equal((detail.match(/<li>/g)||[]).length,r.entryPlan.events.length,'Timeline shows only actual recorded events');
 for(const e of r.entryPlan.events){assert(detail.includes(escape(e.at)));assert(detail.includes(escape(lang==='es'?e.evidenceEs:e.evidenceEn)));}
 render('entradas?q=none',lang);assert(!c.vEntradas().includes('entry-card'));
 render('entradas/missing',lang);assert(!c.vEntradas().includes('class="panel entry-detail"'));
}
clock='2026-11-05T21:00:00Z';
let expired=render('entradas/'+r.entryPlan.id);assert(expired.includes('entry-state--expired'));assert(expired.includes('from declared deadline'));assert(expired.includes('The original record remains pending'));
assert.equal(r.entryPlan.events[0].state,'pending');
for(const state of ['activated','cancelled']){
 const fixture=clone(r);fixture.entryPlan.events.push({state,at:'2026-11-05T15:00:00Z',source:'research/test.json',evidenceEs:'Evidencia de prueba.',evidenceEn:'Test evidence.'});
 if(state==='activated')fixture.entryPlan.events[1].verifiedSignal={kind:'regular-15m-signal',verified:true,at:'2026-11-05T14:45:00Z',source:'research/test-signal.json'};
 c.S.lib=[fixture];assert(c.isEntryPlan(fixture));const out=render('entradas/'+fixture.entryPlan.id);assert(out.includes('entry-state--'+state));assert(out.includes('never a purchase or an order'));semanticChecks(out);
}
c.S.lib=loaded.reports;clock='2026-11-05T12:45:00Z';
for(const state of ['idle','loading','fail']){c.S.libState=state;const out=render('entradas');assert(out.includes('entry-hero'));assert(out.includes('No execution or order'));assert(!out.includes('entry-grid'));if(state==='fail')assert(out.includes('data-libretry="1"'));}
c.S.libState='ok';render('entradas?q=%22%3E%3Cimg%20src=x%3E');assert(!c.vEntradas().includes('<img src=x>'));
assert.equal(JSON.stringify(loaded.reports),original,'Rendering never mutates source data');
const css=html.slice(html.indexOf('/* Entry-plan presentation only.'),html.indexOf('</style>'));
// Every ordinary selector in this isolated block must be scoped to the archive.
for(const match of css.replace(/\/\*[\s\S]*?\*\//g,'').matchAll(/([^{}]+)\{/g)){
 const selector=match[1].trim();if(selector.startsWith('@'))continue;
 // Split only top-level commas: commas inside :is() are selector arguments.
 let depth=0,start=0;const selectors=[];for(let i=0;i<selector.length;i++){if(selector[i]==='(')depth++;if(selector[i]===')')depth--;if(selector[i]===','&&!depth){selectors.push(selector.slice(start,i));start=i+1;}}selectors.push(selector.slice(start));
 for(const part of selectors)assert(part.includes('#v-entradas'),'Unscoped selector: '+part);
}
assert(css.includes('@media(max-width:640px)'));assert(css.includes('minmax(0,1fr)'));assert(css.includes(':focus-visible'));assert(css.includes('outline:3px'));
assert(css.includes('@media(prefers-reduced-motion:no-preference)'));assert(!/animation\s*:/.test(css));assert.equal((css.match(/transition\s*:/g)||[]).length,1);
assert(css.includes(':root[data-theme="dark"] #v-entradas'));assert(css.includes(':root:not([data-theme="light"]) #v-entradas'));
assert(css.includes('.entry-card-title a:visited'));assert(css.includes('@media(forced-colors:active)'));
function luminance(hex){const c=hex.match(/../g).map(x=>parseInt(x,16)/255).map(x=>x<=.04045?x/12.92:((x+.055)/1.055)**2.4);return c[0]*.2126+c[1]*.7152+c[2]*.0722;}
function contrast(a,b){const x=luminance(a),y=luminance(b);return (Math.max(x,y)+.05)/(Math.min(x,y)+.05);}
for(const [fg,bg] of [['9A4F09','FFFFFF'],['9A4F09','F2F4F3'],['9A4F09','F6E7D6'],['E39A4C','151F27'],['E39A4C','0E151B'],['E39A4C','3A2814'],['13202B','FBEFCB'],['E3E9EC','3A2E0E'],['192630','F0B266'],['F0B266','13232F'],['C5D0D6','3C392A'],['4A5A66','F6E7D6'],['9AA9B3','3A2814']])assert(contrast(fg,bg)>=4.5,fg+' / '+bg+' normal-text contrast');
console.log('PASS scoped archive styling, light/dark text contrast, keyboard focus, reduced-motion/forced-colors contracts, responsive rules and decorative SVG accessibility.');
console.log('PASS ES/EN list/detail structure, unchanged source prose/economics/evidence, four status presentations, immutable pending-to-deadline display, preserved filters/links, loading/empty/error states and render purity.');
console.log('NOTE: These are source/render-contract checks, not a browser visual or pixel-layout pass.');
