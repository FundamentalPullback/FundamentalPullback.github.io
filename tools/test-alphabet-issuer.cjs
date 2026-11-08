// Read-only source preservation and issuer/security separation contract.
const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const a=require('./load-stock-profiles.cjs')(),S=a.t.S,hash=x=>crypto.createHash('sha256').update(x).digest('hex');
const hashes={'lib.js':'8916b9c9dd1195fd5e035784d538d9f3ad102689447bb2716d863d5bde240c7e','dec.js':'932698d42c0e844907bf01a334817b559b40d7c6e84549cb7b73f99e1a83adc1'};
for(const [f,h]of Object.entries(hashes))assert.equal(hash(fs.readFileSync(path.join(__dirname,'../data',f))),h,'Historical source bytes: '+f);
for(const [id,h]of Object.entries({A036:'4322cceaa31aefca9f0e3206212543c070fb77c5b7281ec17edb07c5235390bf',A037:'f7b5944a0e80c291b91bd10a2081c1712161b0130d51c04c94a03dacb37d4ef5',A057:'093163ab578cd20f835922b0183d4bd422cc113ca82d309c8b306d1814325257'}))assert.equal(hash(JSON.stringify(a.reports.find(r=>r.id===id))),h,'Historical report object: '+id);
// Only the corrected historical sources are constrained; future research may complete.
const historicalIds=['A036','A037','A057'];
for(const ticker of ['GOOG','GOOGL']){
 const p=a.profiles.find(p=>p.ticker===ticker),x=p.issuerResearch;
 assert(!p.completed.some(r=>historicalIds.includes(r.id)));assert.equal(x.issuerKey,'CIK0001652044');assert.equal(x.shareClass,ticker==='GOOG'?'C':'A');
 assert.equal(x.appliedOn,'2026-11-08');assert.equal(x.statusAsOf,'2026-11-08');assert.equal(x.scope,'historical-issuer-research-only');assert.equal(JSON.stringify(x.appliesToReportIds),JSON.stringify(historicalIds));assert.equal(x.historicalWorkDelivered,true);assert.equal(x.currentStage3Certified,false);assert.equal(x.latestCompletedEligible,false);assert.equal(x.approvedValue,null);assert.equal(x.approvedEntry,null);assert.equal(x.entryApproved,false);
 for(const id of ['A036','A037','A057'])assert.equal(p.reports.filter(r=>r.id===id).length,1);
 for(const id of ['A036','A037']){const rows=p.analyses.filter(r=>r.id===id);assert.equal(rows.length,1);assert.equal(rows[0].isComplete,false);}
 assert.equal(p.analyses.some(r=>r.id==='A057'),false);assert.equal(p.analyses.find(r=>r.id==='A037').kind,'Revisión parcial de valoración; sin certificación Stage 3');
 assert.equal(x.reports.find(r=>r.id==='A057').referenceOnly,true);
 assert.deepEqual(JSON.parse(JSON.stringify(p.decisions)).sort((a,b)=>a.date.localeCompare(b.date)),JSON.parse(JSON.stringify(S.dec.filter(r=>r.ticker===ticker))).sort((a,b)=>a.date.localeCompare(b.date)));
 assert.deepEqual(JSON.parse(JSON.stringify(p.scans)),JSON.parse(JSON.stringify(S.scan.filter(r=>r.ticker===ticker))));
 for(const lang of ['es','en']){a.t.setLang(lang);const h=a.t.renderProfile(p);assert(h.includes('issuer-research'));assert(h.includes(lang==='en'?'Historical delivery is not financial certification':'La entrega histórica no equivale a certificación financiera'));assert(!h.includes('NaN'));}
 S.profileQ=ticker;S.profileScans='all';S.profileStatus='all';S.profileView='all';S.profileContextValid=true;S.profileFilter='complete';assert.equal(a.t.profileResults(a.profiles).length,p.latestCompleted?1:0);S.profileFilter='other';assert.equal(a.t.profileResults(a.profiles).length,p.latestCompleted?0:1);
}
const original=JSON.stringify({reports:a.reports,decisions:S.dec});
const isolated=a.engine.build({reports:a.reports.filter(r=>['A036','A037','A057'].includes(r.id)),decisions:S.dec.filter(r=>r.ticker==='GOOG'),scans:[]});
const g=isolated.find(p=>p.ticker==='GOOGL');assert.equal(g.decisions.length,0);assert.equal(g.scans.length,0);assert.equal(g.latestReview,null);assert.equal(g.latestAnalysis.id,'A037');assert.equal(g.latestCompleted,null);
assert.equal(JSON.stringify({reports:a.reports,decisions:S.dec}),original);
const futureReport={id:'A999',date:'2026-11-09',cat:'Selección y valoración',title:'Future valid fundamental research',text:'Future reviewed source',profiles:['GOOG','GOOGL'].map(ticker=>({ticker,kind:'complete',completedAt:'2026-11-09'}))};
const future=a.engine.build({reports:a.reports.concat([futureReport]),decisions:S.dec,scans:S.scan});
for(const ticker of ['GOOG','GOOGL']){const p=future.find(p=>p.ticker===ticker);assert.equal(p.latestCompleted.id,'A999');assert.equal(p.latestAnalysis.id,'A999');assert.equal(p.completed.filter(r=>r.id==='A999').length,1);assert(!p.completed.some(r=>historicalIds.includes(r.id)));for(const lang of ['es','en']){a.t.setLang(lang);const h=a.t.renderProfile(p);assert(h.includes('A999'));assert(h.includes(lang==='en'?'not later research':'no las investigaciones posteriores'));}}
console.log('PASS Alphabet issuer-only links, historical-only completion exclusion and future valid completion, delivery/certification distinction, source hashes, class isolation, deduplication, bilingual rendering and filters.');
