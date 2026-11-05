// Append-only follow-up contracts. These are source/render checks, not browser screenshots.
const fs=require('fs'),vm=require('vm'),assert=require('assert/strict'),path=require('path'),crypto=require('crypto');
const root=path.resolve(__dirname,'..'),loaded=require('./load-stock-profiles.cjs')(root),clone=x=>JSON.parse(JSON.stringify(x));
const source=loaded.reports.find(r=>r.id==='A278'),registry=clone(loaded.c.window.FP_ENTRY_PLAN_FOLLOWUPS),manifest=clone(loaded.c.window.FP_MANIFEST),html=loaded.html;
assert(registry,'Published follow-up registry is loaded through the manifest');
assert.equal(manifest.entryPlanFollowupFile,'data/entry-plan-followups.js');assert.equal(manifest.libraryFiles.filter(f=>f===manifest.entryPlanFollowupFile).length,1);
const e=registry.records[0],sourceBefore=JSON.stringify(loaded.reports),registryBefore=JSON.stringify(registry);let language='es',clock='2026-11-05T20:00:00Z';
class Clock extends Date{constructor(...a){super(...(a.length?a:[clock]));}static now(){return Date.parse(clock);}}
const esc=s=>String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/"/g,'&quot;');
const c={window:{FP_PROFILE_ENGINE:loaded.engine,FP_MANIFEST:manifest,FP_ENTRY_PLAN_FOLLOWUPS:clone(registry)},S:{lib:loaded.reports,libState:'ok'},document:{addEventListener:()=>{}},location:{hash:''},URLSearchParams,Date:Clock,encodeURIComponent,decodeURIComponent,isFinite,pt:(a,b)=>language==='es'?a:b,esc,ensureLib:()=>{},loadingBlock:()=>'',notice:(a,b)=>a+' '+b,t:()=>({all:'All',retry:'Retry'}),reportLink:(id,label)=>'<a href="#biblioteca/'+id+'">'+label+'</a>'};
vm.createContext(c);vm.runInContext(html.slice(html.indexOf('  function isEntryPlan'),html.indexOf('  /* ---------- library ---------- */')),c);
function render(route,lang='es'){language=lang;c.entryPlanRoute(route);return c.vEntradas();}
function invalid(change){c.window.FP_ENTRY_PLAN_FOLLOWUPS=clone(registry);change(c.window.FP_ENTRY_PLAN_FOLLOWUPS);assert.equal(c.entryPlanFollowups().ok,false);const out=render('entradas/'+source.entryPlan.id);assert(!out.includes('entry-detail-head'));assert(out.includes('No se puede verificar'));}
assert(c.isEntryPlan(source));assert(c.entryPlanFollowups().ok);const composite=c.entryPlanCompose(source,c.entryPlanFollowups());assert.equal(composite.entryPlan.events.length,2);assert.equal(composite.entryPlan.events[0].state,'pending');assert.equal(composite.entryPlan.events[1].state,'suspended');assert.equal(c.entryPlanStatus(composite.entryPlan).state,'suspended');
for(const now of ['2026-11-05T20:00:00Z','2026-11-05T21:00:00Z','2026-11-06T15:00:00Z'])assert.equal(c.entryPlanStatus(composite.entryPlan,now).state,'suspended','Deadline does not silently replace a recorded suspension');
for(const lang of ['es','en']){
 const list=render('entradas?q=ctsh&state=suspended',lang);assert(list.includes('entry-card'));assert(list.includes('entry-state--suspended'));assert(list.includes(esc(e.at.slice(0,10))));assert(list.includes(e.reader.path));assert(!list.includes(e.archive.path));assert(list.includes('entry-followup--compact'));assert(!list.includes(esc(e.requestsStartedAt)));assert(!list.includes(esc(e.observedReviewAt)));assert.equal((list.match(new RegExp(e.reader.path,'g'))||[]).length,1);
 const detail=render('entradas/'+source.entryPlan.id+'?q=ctsh&state=suspended',lang);assert(detail.includes(esc('#entradas?q=ctsh&state=suspended')));assert.equal((detail.match(/<li>/g)||[]).length,2);assert(detail.includes(esc(source.entryPlan.events[0].source)));assert(detail.includes(esc(e.source.path)));assert(detail.includes(e.archive.path));assert(detail.includes(esc(lang==='es'?e.evidenceEs:e.evidenceEn)));assert(!detail.includes('entry-followup--compact'));
 assert(detail.includes(lang==='es'?'Suspendida: requiere nueva evaluación documentada':'Suspended: requires a new documented evaluation'));
 assert(detail.includes(lang==='es'?'contexto histórico':'historical context'));assert(detail.includes(lang==='es'?'no reactiva esta versión':'does not reactivate this version'));
 for(const stamp of [e.at,e.observedReviewAt,e.requestsStartedAt,e.barOpenedAt,e.barClosedAt])assert(detail.includes(esc(stamp)));
 for(const value of ['65.26','65.78','61.55','61.2','A268','PUBLIC_FINAL_V2'])assert(detail.includes(value));
 assert(!/quantity|balance|holdings|cantidad|patrimonio|saldo/i.test(list),'No private execution or account data');
 assert(!render('entradas?state=pending',lang).includes('entry-card'));assert(!render('entradas?state=activated',lang).includes('entry-card'));assert(!render('entradas?state=expired',lang).includes('entry-card'));assert(!render('entradas?state=cancelled',lang).includes('entry-card'));
 loaded.t.setLang(lang);const panel=loaded.t.profileSummaryCard(loaded.profiles.find(p=>p.ticker==='CTSH'));assert(panel.includes(lang==='es'?'Suspendida: requiere nueva evaluación documentada':'Suspended: requires a new documented evaluation'));assert(panel.includes(e.reader.path));assert(panel.includes(e.archive.path));assert(panel.includes(esc(e.requestsStartedAt)));assert(panel.includes(esc(e.observedReviewAt)));assert(!panel.includes('entry-followup--compact'));assert(panel.includes(lang==='es'?'resumen histórico':'historical summary'));
}
for(const change of [
 x=>x.schema='unknown',x=>x.extra=true,x=>x.records=[],x=>x.records={},x=>x.records.push(clone(x.records[0])),x=>x.records.push({...clone(x.records[0]),id:'different'}),
 x=>x.records[0].schema='unknown',x=>x.records[0].id='',x=>x.records[0].id='<img>',x=>x.records[0].planId='FOREIGN',x=>x.records[0].reportId='A268',x=>x.records[0].version='V3',
 x=>x.records[0].state='pending',x=>x.records[0].state='activated',x=>x.records[0].state='expired',x=>x.records[0].state='cancelled',x=>x.records[0].quantity=1,x=>x.records[0].verifiedSignal={},
 x=>x.records[0].sourcePlan.levels.S=60,x=>x.records[0].sourcePlan.events[0].at='2026-11-05T11:00:00Z',x=>x.records[0].predecessor.source='research/fake.json',x=>x.records[0].predecessor.state='activated',
 x=>x.records[0].sourceLibrary.path='data/ops.js',x=>x.records[0].sourceLibrary.sha256='bad',x=>x.records[0].sourcePackage.path='research/foreign.zip',x=>x.records[0].sourcePackage.sha256='bad',
 x=>x.records[0].source.path='https://evil.test/e.json',x=>x.records[0].source.path='research/../secret.json',x=>x.records[0].source.path='research//missing.json',x=>x.records[0].source.path='research/x/e.md',x=>x.records[0].source.sha256='bad',
 x=>x.records[0].reader.path='research/foreign/index.html',x=>x.records[0].archive.path='research/foreign/e.zip',x=>x.records[0].archive.path=x.records[0].archive.path.replace('.zip','.html'),
 x=>x.records[0].evidenceEs='',x=>x.records[0].evidenceEn=' ',x=>x.records[0].at='bad',x=>x.records[0].at='2026-02-30T15:00:00Z',x=>x.records[0].at='2027-01-01T00:00:00Z',x=>x.records[0].at='2026-11-05T14:45:00Z',
 x=>x.records[0].observedReviewAt='2026-11-05T14:45:00Z',x=>x.records[0].requestsStartedAt='2026-11-05T14:44:00Z',x=>x.records[0].barClosedAt='2026-11-05T09:45:01-05:00',x=>x.records[0].barOpenedAt='2026-11-05T09:29:00-05:00',
 x=>{x.records[0].barOpenedAt='2026-11-05T09:15:00-05:00';x.records[0].barClosedAt='2026-11-05T09:30:00-05:00';},x=>{x.records[0].barOpenedAt='2026-11-04T09:30:00-05:00';x.records[0].barClosedAt='2026-11-04T09:45:00-05:00';}
])invalid(change);
c.window.FP_ENTRY_PLAN_FOLLOWUPS=undefined;assert.equal(c.entryPlanFollowups().ok,false,'Manifest-declared missing registry fails closed');c.window.FP_MANIFEST={};assert(c.entryPlanFollowups().ok,'Legacy source-only snapshots remain supported');assert(render('entradas?state=pending').includes('entry-card'));c.window.FP_MANIFEST=manifest;
c.window.FP_ENTRY_PLAN_FOLLOWUPS=clone(registry);c.S.lib=loaded.reports.concat([clone(source)]);assert.equal(c.entryPlanFollowups().ok,false,'Duplicate original plan binding fails closed');c.S.lib=loaded.reports;
const changed=clone(source);changed.entryPlan.signal.closeLte=65.79;changed.entryPlan.levels.cap=65.79;c.S.lib=loaded.reports.map(r=>r.id===source.id?changed:r);assert.equal(c.entryPlanFollowups().ok,false,'Unannounced source changes fail closed');c.S.lib=loaded.reports;
clock='2026-11-05T14:45:00Z';assert.equal(c.entryPlanFollowups().ok,false,'Future follow-up is not applied or silently ignored');clock='2026-11-05T20:00:00Z';
const future=clone(source);future.id='A999';Object.assign(future.entryPlan,{id:'FUTURE-B-V3',ticker:'FUTURE',reportId:'A999',version:'V3',predecessorReportId:'A998'});future.profiles[0].ticker='FUTURE';future.profiles[0].historicalModelReference='A998';const generic=clone(registry);Object.assign(generic.records[0],{id:'FUTURE-REVIEW-1',planId:future.entryPlan.id,reportId:future.id,version:future.entryPlan.version,sourcePlan:clone(future.entryPlan)});c.S.lib=[future];c.window.FP_ENTRY_PLAN_FOLLOWUPS=generic;assert(c.entryPlanFollowups().ok,'No ticker-specific schema or runtime branches');assert(render('entradas/FUTURE-B-V3').includes('entry-state--suspended'));
c.S.lib=loaded.reports;c.window.FP_ENTRY_PLAN_FOLLOWUPS=clone(registry);
assert.equal(JSON.stringify(loaded.reports),sourceBefore,'Original source library untouched');assert.equal(JSON.stringify(registry),registryBefore,'Follow-up data untouched');assert.equal(source.entryPlan.events.length,1);assert.equal(source.entryPlan.events[0].state,'pending');
function sha(file){return crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex');}
for(const file of [e.sourceLibrary,e.sourcePackage,e.source,e.reader,e.archive])assert.equal(sha(path.join(root,file.path)),file.sha256,'Bound public artifact '+file.path);
const libraryContext={window:{}};vm.createContext(libraryContext);vm.runInContext(fs.readFileSync(path.join(root,e.sourceLibrary.path),'utf8'),libraryContext);assert.deepEqual(clone(libraryContext.window.FP_LIB.reports.find(r=>r.id===e.reportId)),clone(source),'Source-library digest refers to the actual bound report');
const record=JSON.parse(fs.readFileSync(path.join(root,e.source.path),'utf8'));assert.equal(e.id,record.id);assert.equal(e.planId,record.relatedProposalId);assert.equal(e.reportId,record.relatedReportId);assert.equal(e.state,record.status);assert.equal(e.at,record.followUpPreparedAt);assert.equal(e.observedReviewAt,record.observedReviewRecordedAt);assert.equal(e.requestsStartedAt,record.sourceRequestsStartedAt);assert.equal(e.barOpenedAt,record.observationWindow.start);assert.equal(e.barClosedAt,record.observationWindow.end);assert.equal(e.evidenceEs,record.note);assert.equal(e.evidenceEn,record.noteEn);assert.equal(e.sourcePackage.sha256,record.originalPublicPackageSha256);assert.equal(record.statusLabel,'Suspendida: requiere nueva evaluación documentada');for(const k of ['terminalCancellation','entryApproved','executionVerified','orderSubmittedByReview','automaticReactivation','originalProposalModified','valuationChanged'])assert.equal(record[k],false);
const dir=path.dirname(path.join(root,e.source.path)),observed=JSON.parse(fs.readFileSync(path.join(dir,record.evidenceRecord),'utf8'));assert.equal(observed.minute_bar_count,15);assert.equal(observed.minute_reaggregation_matches_15m,true);assert.equal(observed.independent_provider_matches_exact_ohlc,false);assert.equal(observed.signal_close_gt_65_26_lte_65_78,false);assert.equal(observed.regular_high_gt_fundamental_cap_66_50,true);assert.equal(observed.actions.automatic_rearm_permitted,false);assert.equal(observed.actions.entry_approved,false);
// Dated economic ledgers from verified suspension commit 848a63e249badf779b4c8343239a5809d1c4bd41.
// Preserve their exact bytes as a prefix while allowing only the minimized public HRB
// execution append independently covered by test-hrb-partial-sale.cjs.
const ledgerSnapshots={
 'ops.js':{key:'ops',rows:25,bytes:3509,sha256:'314025aa2d64b9d0516e95748b15c2b2f764b923ffb77b08c78825b36ff74d5a',appendSha256:'25ab3417b569f7fa31926099c929e686079d5170a27841fa95c948b4abe579af'},
 'ges.js':{key:'ges',rows:66,bytes:53969,sha256:'d6641842ebf1b9d7198d127c665b1517e8de8ae10e11c61dea6355021945c426',appendSha256:'f7f81b667cc99ec241fa09d07ed6308a6822b2290acd629099476eb403f3ea47'}
};
const ledgerAppendCounts=[];
for(const [file,snapshot] of Object.entries(ledgerSnapshots)){
 const bytes=fs.readFileSync(path.join(root,'data',file)),text=bytes.toString('utf8'),prefix='window.FP=window.FP||{};FP.'+snapshot.key+'=';
 assert(text.startsWith(prefix)&&text.endsWith(';\n'),'Expected ledger wrapper '+file);
 const rows=JSON.parse(text.slice(prefix.length,-2));assert(rows.length===snapshot.rows||rows.length===snapshot.rows+1,'Only the sole authorized HRB append may follow the suspension snapshot: '+file);
 const historical=Buffer.concat([bytes.subarray(0,snapshot.bytes-3),Buffer.from('];\n')]);
 assert.equal(crypto.createHash('sha256').update(historical).digest('hex'),snapshot.sha256,'Exact prior suspension ledger byte prefix '+file);
 const appended=rows.length-snapshot.rows;ledgerAppendCounts.push(appended);
 if(appended)assert.equal(crypto.createHash('sha256').update(JSON.stringify(rows[snapshot.rows])).digest('hex'),snapshot.appendSha256,'Exact minimized public HRB append '+file);
}
assert.equal(ledgerAppendCounts[0],ledgerAppendCounts[1],'HRB operation and management append must be reconciled together');
const prior=path.resolve(process.env.CTSH_SUSPENSION_BASELINE||path.join(root,'../../entry_plans_visual_release/verified_site'));if(fs.existsSync(prior)){
 for(const f of fs.readdirSync(path.join(root,'data'))){if(f==='manifest.js'||f==='entry-plan-followups.js'||ledgerSnapshots[f]||fs.statSync(path.join(root,'data',f)).isDirectory())continue;assert.equal(sha(path.join(root,'data',f)),sha(path.join(prior,'data',f)),'Unchanged published data '+f);}
 const originalDir='research/2026-11-05/CTSH-stage35-B-V2';for(const f of fs.readdirSync(path.join(root,originalDir)))assert.equal(sha(path.join(root,originalDir,f)),sha(path.join(prior,originalDir,f)),'Unchanged original source '+f);
}
console.log('PASS source-bound append-only suspension, separate timestamps, original pending event, exact documented state, ES/EN list/detail/panel, filters, no automatic expiry/rearm, immutable source and economic records.');
console.log('PASS malformed/duplicate/foreign/future registries fail closed, strict paths/schemas/predecessor/source-plan binding, generic future plan, artifact SHA-256 and exact event-record linkage.');
