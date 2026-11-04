// Run: node tools/test-research-workspace.cjs. Uses Node built-ins only.
const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict'),path=require('node:path');
const root=path.resolve(__dirname,'..'),c={window:{}},events={},replaced=[];c.FP=c.window.FP={};vm.createContext(c);
vm.runInContext(fs.readFileSync(root+'/data/manifest.js','utf8'),c);
for(const file of [...c.window.FP_MANIFEST.files,'data/names.js',...c.window.FP_MANIFEST.libraryFiles,'data/stock-profiles.js'])vm.runInContext(fs.readFileSync(root+'/'+file,'utf8'),c);
const html=fs.readFileSync(root+'/index.html','utf8');let app=[...html.matchAll(/<script[^>]*>([\s\S]*?)<\/script>/g)].map(x=>x[1]).find(x=>x.includes('var DEC_MAP'));new vm.Script(app);
app=app.slice(0,app.indexOf('  var hash ='))+app.slice(app.indexOf('  var PARTS ='),app.indexOf('  var DENY ='))+'\nwindow.TEST={GROUPS,RENDER,vRevision,vResumen,vEscaner,vRetro,dailyHash,profileDecisionRows,profileDecisionArchive,decisionArchiveTable,profileSavedViews,DEC_ORDER,decLabel,profileStatus,profileStatusLabel,profileStatusBadge,profileStatusCaution,profileStatusOptions,profileStatusSelect,profileState,renderUI:render,S,PARTS,profiles,vFichas,renderProfile,profileRoute,profileResults,profileContext,profileHref,profileSearchHash,profileNavigation,profileSummaryCard,mountProfileQuotes,setLang:function(l){lang=l;}};render=function(){};})();';
const noop=()=>{},el={addEventListener:noop,setAttribute:noop,querySelectorAll:()=>[],style:{}};
Object.assign(c,{document:{getElementById:()=>el,addEventListener:(name,fn)=>(events[name]||(events[name]=[])).push(fn),querySelectorAll:()=>[],querySelector:()=>el,hidden:false},localStorage:{getItem:()=>null},history:{state:{unrelated:'preserved'},replaceState:(state,title,href)=>replaced.push({state,href})},console,Date,Intl,setTimeout:()=>1,clearTimeout:noop,AbortController,location:{hash:'#fichas'},URL,URLSearchParams});c.window.addEventListener=noop;vm.runInContext(app,c);
const t=c.window.TEST,F=c.FP;t.S.scan=t.PARTS.scan([F.scanHead].concat(F.scan));for(const k of ['dec','ges','ops','acct','hist'])t.S[k]=t.PARTS[k](F[k]);t.S.lib=c.window.FP_LIB.reports;t.S.libState='ok';t.S.snapshot=c.window.FP_MANIFEST.asOf;

const counts={},before=JSON.stringify([t.S.dec,t.S.ops,t.S.ges]),all=t.profiles();
// Derive the expected latest rows from source dates, not a fixed publication count.
// Sort independently so the runtime's latestPerTicker implementation is still tested.
const sourceLatest = new Map();
Array.from(t.S.dec).map((r,i)=>({r,i})).sort((a,b)=>
 String(a.r.adate||'').localeCompare(String(b.r.adate||'')) ||
 String(a.r.date||'').localeCompare(String(b.r.date||'')) || a.i-b.i
).forEach(({r})=>sourceLatest.set(r.ticker,r));
const sourceApproved = r => ['Apta para Stage 3.5','Aprobada Stage 3, bloqueada'].includes(r.decision);
const expectedCounts = {
 approvals: Array.from(sourceLatest.values()).filter(sourceApproved).length,
 waiting: Array.from(sourceLatest.values()).filter(r=>!sourceApproved(r)&&r.decision!=='En cartera').length
};
assert.deepEqual(Array.from(t.GROUPS.find(g=>g.id==='invest').views),['fichas','revision','analisis','retro']);
for(const lang of ['en','es']){
 t.setLang(lang);
 for(const [old,view] of [['aprobadas','approvals'],['descartadas','waiting']]){
  assert.equal(t.profileRoute(old),'fichas');assert.equal(t.S.profileView,view);assert.equal(t.S.profileHistory,'latest');
  const rows=t.profileDecisionRows(),shown=t.profileResults(all),h=t.vFichas();counts[view]=rows.length;
  assert(h.includes('id="profile-history"'));assert(h.includes('data-sort="archive|next"'));assert(h.includes('data-sort="archive|expiry"'));assert(h.includes('data-sort="archive|r3"'));assert(h.includes('data-sort="archive|x3"'));assert(h.includes('href="#posiciones"'));
  assert(h.includes(lang==='en'?'not current purchase authorization':'no es autorización actual de compra'));
  for(const r of rows){assert(h.includes(r.ticker));assert(shown.some(p=>p.ticker===r.ticker));}
  const newest=rows.length;t.profileRoute('fichas?view='+view+'&history=all');assert(t.profileDecisionRows().length>=newest);assert(t.profileSearchHash().includes('history=all'));
  for(const p of t.profileResults(all)) {const href=t.profileHref(p.ticker,t.profileContext());t.profileRoute(href.slice(1));assert.equal(t.S.profileView,view);assert.equal(t.S.profileHistory,'all');assert(t.profileSearchHash().includes('view='+view));}
 }
 assert.equal(t.profileRoute('fichas?view=history'),'fichas');assert.equal(t.profileDecisionRows().length,sourceLatest.size);assert.deepEqual(Array.from(t.profileDecisionRows(),r=>r.ticker).sort(),Array.from(sourceLatest.keys()).sort());for(const r of t.profileDecisionRows())assert.equal(r,sourceLatest.get(r.ticker),'Latest row identity must follow source dates: '+r.ticker);
 t.profileRoute('fichas?view=history&history=all');assert.equal(t.profileDecisionRows().length,t.S.dec.length);
 t.profileRoute('fichas?view=approvals&q=notfound');assert(t.vFichas().includes('id="profile-history"'));assert(t.vFichas().includes(lang==='en'?'No matching decisions':'Sin decisiones coincidentes'));
 t.S.scanDate='2026-11-02';t.S.scanQ='EL';t.S.onlyS2=false;assert.equal(t.profileRoute('escaner'),'revision');assert.equal(t.S.reviewDate,'2026-11-02');assert.equal(t.S.reviewPanel,'scanner');assert.equal(t.S.scanQ,'EL');assert.equal(t.S.onlyS2,false);
 let h=t.vRevision();assert(h.includes('id="review-date"'));assert(!h.includes('id="scan-date"'));assert(h.includes('id="scan-q"'));assert(h.includes('data-sort="scan|opp"'));
 t.profileRoute('revision?date=2026-11-03&panel=scanner&q=EL&stage2=0&scanSort=pe&scanDir=asc');h=t.vRevision();assert.equal(t.S.resDate,t.S.scanDate);assert(h.includes(lang==='en'?'Exported margin (unverified)':'Margen exportado (sin validar)'));assert(h.includes(lang==='en'?'Verified GAAP operating margin':'Margen operativo GAAP verificado'));
 assert.equal(t.S.sort.scan.key,'pe');assert.equal(t.S.sort.scan.dir,'asc');const href=t.dailyHash('overview');t.profileRoute(href.slice(1));assert.equal(t.S.reviewDate,'2026-11-03');assert.equal(t.S.scanQ,'EL');assert.equal(t.S.onlyS2,false);h=t.vRevision();assert(!h.includes('id="res-date"'));assert(h.includes('data-resdate'));assert(h.includes('data-sort="res|streak"'));
 t.profileRoute('revision?panel=scanner');assert.equal(t.S.sort.scan.key,'opp');assert.equal(t.S.sort.scan.dir,'desc');assert.equal(t.S.sort.res.key,'opp');
 t.S.resDate='2026-10-23';assert.equal(t.profileRoute('resumen'),'revision');assert.equal(t.S.reviewDate,'2026-10-23');assert.equal(t.S.reviewPanel,'overview');
 t.S.retro=t.PARTS.retro(F.retro);h=t.vRetro();assert(h.includes('outcome-cutoff'));assert(h.includes(lang==='en'?'Published outcomes through:':'Resultados publicados hasta:'));
}
assert.deepEqual(counts,expectedCounts);
// A future company must add one latest decision; a newer review replaces, not duplicates it.
const savedDec=t.S.dec;
try {
 assert(!sourceLatest.has('ZZFUTURE'));
 const first={ticker:'ZZFUTURE',company:'Future research fixture',date:'2040-01-01',adate:'2040-01-02',decision:'En observación',rep:'TEST1'};
 const later={...first,adate:'2040-01-03',rep:'TEST2'};
 t.S.dec=savedDec.concat([first]);
 t.profileRoute('fichas?view=history');assert.equal(t.profileDecisionRows().length,sourceLatest.size+1);
 t.profileRoute('fichas?view=waiting');assert.equal(t.profileDecisionRows().length,expectedCounts.waiting+1);
 t.profileRoute('fichas?view=approvals');assert.equal(t.profileDecisionRows().length,expectedCounts.approvals);
 t.S.dec=savedDec.concat([first,later]);
 t.profileRoute('fichas?view=history');assert.equal(t.profileDecisionRows().length,sourceLatest.size+1);
 assert.equal(t.profileDecisionRows().find(r=>r.ticker==='ZZFUTURE').rep,'TEST2');
 t.S.dec=savedDec.concat([later,first]);
 assert.equal(t.profileDecisionRows().length,sourceLatest.size+1);
 assert.equal(t.profileDecisionRows().find(r=>r.ticker==='ZZFUTURE').rep,'TEST2','Input order must not override a newer analysis date');
 t.profileRoute('fichas?view=history&history=all');assert.equal(t.profileDecisionRows().length,savedDec.length+2);
} finally {t.S.dec=savedDec;}
assert.equal(JSON.stringify([t.S.dec,t.S.ops,t.S.ges]),before,'Consolidation must not mutate decisions, trades or management rows');
console.log('PASS research workspaces: four research menu items; legacy aliases; shared dated overview/scanner; audit/source labels and sorting; saved approval/waiting/all history, latest/all switching, search, profile context, execution/expiry/valuation/reason/returns; source-derived counts and future company/review fixtures, unchanged source data, EN/ES and distinct Hindsight cutoff.');

