// Dated source-bound reviews. No network, trading or account writes.
const fs=require('fs'),path=require('path'),assert=require('assert/strict'),crypto=require('crypto'),vm=require('vm'),Module=require('module');
const root=path.resolve(__dirname,'..'),base=path.resolve(root,'../../morning_earnings_release/verified_site'),clone=x=>JSON.parse(JSON.stringify(x)),sha=b=>crypto.createHash('sha256').update(b).digest('hex');
const filename=path.join(__dirname,'load-stock-profiles.cjs'),mod=new Module(filename,module);mod.filename=filename;mod.paths=module.paths;
mod._compile(fs.readFileSync(filename,'utf8').replace('profileRoute,renderProfile,','profileRoute,renderProfile,isEntryPlan,entryPlanStatus,entryPlanCompose,entryPlanFollowups,vEntradas,entryPlanRoute,'),filename);
const a=mod.exports(root),before=require('./load-stock-profiles.cjs')(base),c=require('./current-price-contract.cjs').validate(root,a),get=(x,t)=>x.profiles.find(p=>p.ticker===t),records=Object.fromEntries(c.ids.map(id=>[id,a.reports.find(r=>r.id===id)]));
for(const [f,h] of Object.entries(c.priorDataHashes))assert.equal(sha(fs.readFileSync(root+'/data/'+f)),h,'All historical data exact: '+f);
assert(!a.reports.some(r=>r.id==='A279'),'Paused TRMD remains unpublished');
const originalReports=JSON.stringify(a.reports),originalState=JSON.stringify({dec:a.t.S.dec,ges:a.t.S.ges,ops:a.t.S.ops,acct:a.t.S.acct,hist:a.t.S.hist});
for(const tk of ['IT','HURN','CTSH']){
 const p=get(a,tk),old=get(before,tk),r=records[tk==='IT'?'A283':tk==='HURN'?'A284':'A285'],m=r.profiles[0];
 for(const k of ['latestCompleted','latestAnalysis','latestReview','latestManagement','completed','analyses','decisions','management','scans'])assert.deepEqual(clone(p[k]),clone(old[k]),tk+' unchanged economics/history '+k);
 assert.deepEqual(clone(a.engine.researchBalance(p)),clone(before.engine.researchBalance(old)),tk+' historical research balance');
 assert.equal(m.historicalModelReference,tk==='IT'?'A185':tk==='HURN'?'A275':'A268');
 for(const key of ['stage3Complete','latestCompletedEligible','stage35Complete','entryApproved','valuationChanged'])assert.equal(m[key],false);
 for(const key of ['signal','entryPrice','quantity','maximumConditioned','operativeStop'])assert.equal(m[key],null);
 assert.equal(m.approvedQuantity,0);assert(!m.valuation);assert(!m.close);assert.equal(m.contextQuote.type,'dated-intraday-not-executable');
 for(const lang of ['es','en']){a.t.setLang(lang);const card=a.t.profileSummaryCard(p);assert(card.includes(r.id));assert(card.includes(lang==='es'?m.summary:m.summaryEn));assert(!/undefined|NaN|Infinity/.test(card));
  if(tk==='HURN'){assert(card.includes('current-price-review'));assert(!card.includes('#entradas/HURN'));assert(card.includes(lang==='es'?'sin entrada':'no entry'));}
  else {assert(card.includes('prospective-study'));assert(card.includes('#entradas/'+r.entryPlan.id));assert(card.includes(lang==='es'?'No activa · sin señal aprobada':'Inactive · no approved signal'));}
 }
 const name=tk==='CTSH'?'CTSH-current-price-B-V3':tk+'-current-price',dir=root+'/research/2026-11-05/'+name+'/',source=c.sourceVerification[tk];
 for(const [file,h] of Object.entries(source.hashes))assert.equal(sha(fs.readFileSync(dir+file)),h,'Audited original '+tk+'/'+file);
 assert.equal(sha(fs.readFileSync(dir+source.archive)),source.sha256,'Exact original ZIP '+tk);
 const body=fs.readFileSync(dir+'report.md','utf8'),full=fs.readFileSync(dir+'website_report.md','utf8'),page=fs.readFileSync(dir+'reader.html','utf8');assert(full.includes(body));assert.equal(full,r.text);assert(page.includes('name="viewport"'));assert(page.includes('Sin entrada / No entry'));assert(page.includes('table-wrap')||!page.includes('<table'));
 for(const file of fs.readdirSync(dir)){if(file.endsWith('.zip')||fs.statSync(dir+file).isDirectory())continue;const txt=fs.readFileSync(dir+file,'utf8');assert(!/\/workspace\/|\/agent_notes\/|\/user_notes\/|\/home\/agent\/|file:\/\/|BEGIN PRI[V]ATE KEY|Bea[r]er /i.test(txt),'No private paths/secrets '+tk+'/'+file);}
}
assert(a.engine.isCurrentPriceReview(records.A284,records.A284.profiles[0]));assert(!a.engine.isProspectiveStudy(records.A284,records.A284.profiles[0]));assert(!a.t.isEntryPlan(records.A284));
for(const change of [r=>r.schema='unknown',r=>r.type='fundamental-analysis',r=>r.profiles[0].kind='review',r=>r.profiles[0].stage3Complete=true,r=>r.profiles[0].valuationChanged=true,r=>r.profiles[0].entryApproved=true,r=>r.profiles[0].approvedQuantity=1,r=>r.profiles[0].maximumConditioned=180,r=>r.profiles[0].contextQuote.type='regular-close',r=>r.profiles[0].valuation={base:164.21}]){const bad=clone(records.A284);change(bad);assert(!a.engine.isCurrentPriceReview(bad,bad.profiles[0]),'Malformed price review must not be exempted from analysis');}
for(const id of ['A283','A285']){
 const r=records[id],p=r.entryPlan,m=r.profiles[0];assert(a.engine.isProspectiveStudy(r,m));assert(a.t.isEntryPlan(r));assert.equal(p.events[0].state,'inactive');assert.equal(a.t.entryPlanStatus(p,'2026-11-05T20:00:00Z').state,'inactive');assert.equal(a.t.entryPlanStatus(p,'2026-11-05T21:00:00Z').state,'expired');assert.equal(p.executionSuspended,true);
 const prop=JSON.parse(fs.readFileSync(root+'/research/2026-11-05/'+(id==='A283'?'IT-current-price':'CTSH-current-price-B-V3')+'/proposal.json'));assert.equal(p.signal.closeGt,prop.lower_price_validity_strict);assert.equal(p.levels.cap,prop.technical_maximum);assert.equal(p.levels.M,prop.M);assert.equal(p.levels.S,prop.S);assert.equal(m.prospectiveFundamentalMaximum,prop.fundamental_maximum);assert.equal(prop[id==='A283'?'first_eligible_bar_start_utc':'first_eligible_bar_start_UTC'],null);
 const forged=clone(r);forged.entryPlan.events.push({state:'activated',at:'2026-11-05T17:15:00Z',source:p.events[0].source,evidenceEs:'Una señal inventada',evidenceEn:'Invented signal',verifiedSignal:{kind:'regular-15m-signal',verified:true,at:'2026-11-05T17:15:00Z',source:p.events[0].source}});assert(!a.t.isEntryPlan(forged,'2026-11-05T20:00:00Z'),'Inactive version cannot transition directly to approved signal');
}
assert.equal(records.A283.entryPlan.events.length,1);assert.equal(records.A285.entryPlan.events.length,2);
const regdir=root+'/research/2026-11-05/CTSH-current-price-B-V3/',reg=JSON.parse(fs.readFileSync(regdir+'observation_registration_public.json'));
assert.equal(sha(fs.readFileSync(regdir+'observation_registration_public.json')),'3ed6ea63a03c0da727f8a70d5e5a2ef6ba43046499e6e23485dc162092f07ade');assert(Date.parse(reg.registered_at_UTC)<Date.parse(reg.bar_start_UTC));assert.equal(reg.bar_start_UTC,'2026-11-05T17:00:00Z');assert.equal(reg.bar_end_UTC,'2026-11-05T17:15:00Z');assert.equal(reg.entryApproved,false);assert.equal(reg.order_sent,false);assert.equal(reg.account_reverified,false);assert.equal(records.A285.entryPlan.events[1].at,reg.registered_at_UTC);assert.equal(records.A285.entryPlan.events[1].state,'inactive');
const v2=a.reports.find(r=>r.id==='A278');assert(a.t.entryPlanFollowups().ok);assert.equal(a.t.entryPlanStatus(a.t.entryPlanCompose(v2,a.t.entryPlanFollowups()).entryPlan).state,'suspended');
for(const lang of ['es','en']){
 a.t.setLang(lang);a.t.entryPlanRoute('entradas?state=inactive');let out=a.t.vEntradas();assert.equal((out.match(/<article class="entry-card">/g)||[]).length,2);assert(!out.includes('entry-state--activated'));assert(!out.includes('TRMD'));
 a.t.entryPlanRoute('entradas?state=activated');out=a.t.vEntradas();assert(!out.includes('<article class="entry-card">'));
 a.t.entryPlanRoute('entradas/CTSH-20261105-B-V3');out=a.t.vEntradas();assert(out.includes('12:00'));assert(out.includes('observation_registration_public.json'));assert(!out.includes('entry-state--activated'));assert(out.includes(lang==='es'?'sin señal aprobada':'no approved signal'));
 a.t.entryPlanRoute('entradas/CTSH-20261105-B-V2');assert(a.t.vEntradas().includes('entry-state--suspended'));
}
const pending=JSON.parse(fs.readFileSync(root+'/tools/pending-web-commentary.json'));assert.deepEqual(pending.pending.slice(0,-3),c.priorPending.pending);assert.deepEqual(pending.pending.slice(-3).map(r=>r.reportId),c.ids);
assert.equal(JSON.stringify(a.reports),originalReports);assert.equal(JSON.stringify({dec:a.t.S.dec,ges:a.t.S.ges,ops:a.t.S.ops,acct:a.t.S.acct,hist:a.t.S.hist}),originalState,'Render cannot change ledgers');
for(const mutate of [r=>r.push({id:'A286'}),r=>r.push(clone(r.find(x=>x.id==='A283'))),r=>r.find(x=>x.id==='A268').title+='edited',r=>r.find(x=>x.id==='A285').profiles[0].entryApproved=true]){const bad={...a,reports:clone(a.reports)};mutate(bad.reports);assert.throws(()=>require('./current-price-contract.cjs').validate(root,bad));}
console.log('PASS exact A283/A284/A285 sources, clean public ZIPs, original models and all historical data; separate dated price context, unchanged completed research and ES/EN summaries.');
console.log('PASS inactive archive state, two observations not signals, source-bound CTSH registration before window, V2 still suspended, no auto-activation or operative approvals, malformed records fail closed.');
