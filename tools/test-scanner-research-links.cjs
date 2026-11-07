// Run: node tools/test-research-workspace.cjs. Uses Node built-ins only.
const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict'),path=require('node:path');
const root=path.resolve(__dirname,'..'),c={window:{}},events={},replaced=[];c.FP=c.window.FP={};vm.createContext(c);
vm.runInContext(fs.readFileSync(root+'/data/manifest.js','utf8'),c);
for(const file of [...c.window.FP_MANIFEST.files,'data/names.js',...c.window.FP_MANIFEST.libraryFiles,'data/stock-profiles.js'])vm.runInContext(fs.readFileSync(root+'/'+file,'utf8'),c);
const html=fs.readFileSync(root+'/index.html','utf8');let app=[...html.matchAll(/<script[^>]*>([\s\S]*?)<\/script>/g)].map(x=>x[1]).find(x=>x.includes('var DEC_MAP'));new vm.Script(app);
app=app.slice(0,app.indexOf('  var hash ='))+app.slice(app.indexOf('  var PARTS ='),app.indexOf('  var DENY ='))+'\nwindow.TEST={latestScannerNotice,GROUPS,RENDER,vRevision,vResumen,vEscaner,vRetro,dailyHash,profileDecisionRows,profileDecisionArchive,decisionArchiveTable,profileSavedViews,DEC_ORDER,decLabel,profileStatus,profileStatusLabel,profileStatusBadge,profileStatusCaution,profileStatusOptions,profileStatusSelect,profileState,renderUI:render,S,PARTS,profiles,vFichas,renderProfile,profileRoute,profileResults,profileContext,profileHref,profileSearchHash,profileNavigation,profileSummaryCard,mountProfileQuotes,setLang:function(l){lang=l;}};render=function(){};})();';
const noop=()=>{},el={addEventListener:noop,setAttribute:noop,querySelectorAll:()=>[],style:{}};
Object.assign(c,{document:{getElementById:()=>el,addEventListener:(name,fn)=>(events[name]||(events[name]=[])).push(fn),querySelectorAll:()=>[],querySelector:()=>el,hidden:false},localStorage:{getItem:()=>null},history:{state:{unrelated:'preserved'},replaceState:(state,title,href)=>replaced.push({state,href})},console,Date,Intl,setTimeout:()=>1,clearTimeout:noop,AbortController,location:{hash:'#fichas'},URL,URLSearchParams});c.window.addEventListener=noop;vm.runInContext(app,c);
const t=c.window.TEST,F=c.FP;t.S.scan=t.PARTS.scan([F.scanHead].concat(F.scan));for(const k of ['dec','ges','ops','acct','hist'])t.S[k]=t.PARTS[k](F[k]);t.S.lib=c.window.FP_LIB.reports;t.S.libState='ok';t.S.snapshot=c.window.FP_MANIFEST.asOf;


const saved={scan:t.S.scan,dec:t.S.dec,lib:t.S.lib};
for(const lang of ['es','en']){
 t.setLang(lang);
 let h=t.latestScannerNotice();
 assert(h.includes('data-scan-date="2026-11-06"'));
 assert(h.includes(lang==='es'?'12 empresas con registros':'12 companies with research'));
 // Multiple reports and a legacy decision for the same ticker do not double count.
 const report=t.S.lib.find(r=>r.id==='A296');
 t.S.lib=saved.lib.concat([report]);t.S.dec=saved.dec.concat([{ticker:'LMT',date:'2026-11-06'}]);
 h=t.latestScannerNotice();assert(h.includes(lang==='es'?'12 empresas con registros':'12 companies with research'));
 // Future scan must not inherit old research, even if report publication is on its date.
 t.S.scan=saved.scan.concat([{ticker:'LMT',date:'2026-11-07',opp:100}]);
 h=t.latestScannerNotice();assert(h.includes('data-scan-date="2026-11-07"'));assert(h.includes(lang==='es'?'Todavía no hay registros':'No research records'));
 // Explicit profile scanner metadata can link a future review without same-day decisions.
 t.S.lib=saved.lib.concat([{date:'2026-11-08',profiles:[{ticker:'LMT',scanner:{date:'2026-11-07'},kind:'review'}]}]);
 h=t.latestScannerNotice();assert(h.includes(lang==='es'?'1 empresas con registros':'1 companies with research'));
 t.S.scan=saved.scan;t.S.lib=saved.lib;t.S.dec=saved.dec;
}
console.log('PASS latest scanner research: 12 linked profiles, later publication dates, deduplication, future rollover, explicit association, ES/EN.');
