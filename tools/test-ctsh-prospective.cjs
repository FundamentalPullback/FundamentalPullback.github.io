const fs=require('fs'),path=require('path'),assert=require('assert/strict');
const root=path.resolve(__dirname,'..'),baseline=process.env.CTSH_BASELINE||path.resolve(root,'../../close_correction_release/verified_site');
const load=require('./load-stock-profiles.cjs'),now=require("./current-price-contract.cjs").legacy(root,load(root)),before=load(baseline),clone=x=>JSON.parse(JSON.stringify(x));
const find=(a,t)=>a.profiles.find(p=>p.ticker===t),p=find(now,'CTSH'),old=find(before,'CTSH'),r=now.reports.find(r=>r.id==='A278'),m=r.profiles[0];
assert.equal(p.latestCompleted.id,'A268');assert.equal(p.latestAnalysis.id,'A268');
for(const key of ['latestCompleted','latestAnalysis','latestReview','latestManagement','completed','analyses','decisions','management','scans'])assert.deepEqual(clone(p[key]),clone(old[key]),key);
assert.deepEqual(clone(now.engine.researchBalance(p)),clone(before.engine.researchBalance(old)));
const a268=p.latestCompleted.report.profiles.find(m=>m.ticker==='CTSH');
assert.equal(a268.fundamentalEligibility,'conditional');assert.equal(a268.fundamentalMaximumConditional,66.5);assert.equal(a268.close.price,65.78);assert.deepEqual(clone([a268.valuation.bear,a268.valuation.base,a268.valuation.bull]),[51.76,79.34,109.12]);
for(const key of ['entryPrice','signal','quantity','maximumConditioned','operativeStop'])assert.equal(m[key],null,key);
assert.equal(m.entryApproved,false);assert.equal(m.approvedQuantity,0);assert.equal(m.stage35Complete,false);assert.equal(m.valuation,undefined);
assert(now.engine.isProspectiveStudy(r,m));
for(const edit of [x=>delete x.schema,x=>x.schema='unknown',x=>x.type='fundamental-analysis',x=>x.profiles[0].kind='partial',x=>x.profiles[0].entryApproved=true,x=>x.profiles[0].stage3Complete=true,x=>x.profiles[0].latestCompletedEligible=true,x=>x.profiles[0].stage35Complete=true,x=>x.profiles[0].signal='present',x=>x.profiles[0].approvedQuantity=1,x=>delete x.profiles[0].operativeStop,x=>x.profiles[0].valuation={base:79.34},x=>x.profiles[0].maximumConditioned=65.25]){
 let bad=clone(r);edit(bad);assert(!now.engine.isProspectiveStudy(bad,bad.profiles[0]));
 let synthetic=now.engine.build({reports:[bad]})[0];assert.equal(synthetic.latestAnalysis.id,'A278','Malformed records are not exempted from analysis review');
}
let other=clone(r);other.id='A999';other.profiles[0].ticker='FUTURE';other.profiles[0].historicalModelReference='A998';let base={id:'A998',date:'2026-11-04',profiles:[{ticker:'FUTURE',kind:'complete',completedAt:'2026-11-04'}]};let future=now.engine.build({reports:[base,other]})[0];assert.equal(future.latestCompleted.id,'A998');assert.equal(future.latestAnalysis.id,'A998');assert.equal(future.reports.length,2);
for(const lang of ['es','en']){
 now.t.setLang(lang);before.t.setLang(lang);
 let out=now.t.profileSummaryCard(p),prior=before.t.profileSummaryCard(old);assert(out.includes('A278'));assert(out.includes(lang==='es'?'Estudio prospectivo separado':'Separate prospective study'));assert(out.includes(lang==='es'?'S propuesto 61,20':'proposed S $61.20'));assert(out.includes(lang==='es'?'ejecución suspendida':'execution suspended'));
 assert.equal(out.replace(/<aside class="stock-note prospective-study">[\s\S]*?<\/aside>/,''),prior,'Only the separate study panel changes the CTSH summary');
 for(const tk of ['BZ','LNG','TRMD','GAP'])assert.equal(now.t.profileSummaryCard(find(now,tk)),before.t.profileSummaryCard(find(before,tk)),tk+' card preserved');
}
// Exact append-only publication history: the prospective study plus the three
// independently audited earnings supplements. No arbitrary future ID is allowed.
function assertPublishedReportHistory(reports){
 assert.equal(reports.length,before.reports.length+4,'Exact report count preserves duplicate protection');
 assert.equal(new Set(reports.map(r=>r.id)).size,reports.length,'Report IDs must be unique');
 const priorIds=new Set(before.reports.map(r=>r.id));
 assert.deepEqual(clone(reports.filter(r=>!priorIds.has(r.id)).map(r=>r.id).sort()),['A278','A280','A281','A282']);
 for(const original of before.reports)assert.deepEqual(clone(reports.find(r=>r.id===original.id)),clone(original),original.id);
 assert.equal(require('crypto').createHash('sha256').update(JSON.stringify(reports.find(r=>r.id==='A278'))).digest('hex'),'1650049107734958ddd28c717c2bfdef454479d13393e568ed442ccf7a65ec3f','Exact preserved original A278');
}
assertPublishedReportHistory(now.reports);
for(const change of [
 reports=>reports.push({id:'A279',title:'Unexpected paused candidate'}),
 reports=>reports.push({id:'A283',title:'Unexpected new report'}),
 reports=>reports.push(clone(reports.find(r=>r.id==='A268'))),
 reports=>{reports.find(r=>r.id==='A268').title+=' MUTATION';},
 reports=>{reports.find(r=>r.id==='A278').text+=' MUTATION';}
]){const bad=clone(now.reports);change(bad);assert.throws(()=>assertPublishedReportHistory(bad),'Unexpected additions and changes to A268/A278 must fail');}

const publicDir=root+'/research/2026-11-05/CTSH-stage35-B-V2';for(const filename of ['report.md','report.html','results.json','publication_metadata.json','independent_audit.json','independent_audit.md','manifest.sha256','market_data_revision_vs_A268.json','ohlcv_indicators.csv','public_calculations.py','public_release_certificate.json','public_replay.json','source_register.json','README.md'])assert(fs.existsSync(publicDir+'/'+filename));
assert(fs.readFileSync(publicDir+'/index.html','utf8').includes('6.891.179'));
console.log('PASS A278 schema-gated study; malformed/unknown/future-ticker cases; ES/EN panel rendering; A268 completion, conditional status, valuation, close, balance, decisions and all old reports unchanged; no operational approval.');

assert.equal(require('crypto').createHash('sha256').update(fs.readFileSync(publicDir+'/CTSH_Stage35_B_20261105_PUBLIC_FINAL_V2.zip')).digest('hex'),'e46c290a53863b24cb058303fa1b9c42bc46578cde13e3e94e76edd62c744773');
for(const lang of ['es','en']){now.t.setLang(lang);const h=now.t.profileSummaryCard(p);assert(h.includes('#entradas/CTSH-20261105-B-V2'));}
console.log('PASS original full public-support ZIP hash and labeled ES/EN panel download.');
const result=JSON.parse(fs.readFileSync(publicDir+'/results.json','utf8')),proposal=result.proposal;
assert.equal(m.prospectiveTechnicalCap,65.78);assert.equal(m.prospectiveManualStop,61.2);assert.equal(m.prospectiveM,61.55);
assert.equal(proposal.route,'B');assert.equal(proposal.timeframe,'complete 15-minute regular-session bar');assert.equal(proposal.regular_signal_date,'2026-11-05');assert.equal(proposal.confirmation_close_gt,65.26);assert.equal(proposal.confirmation_close_lte,65.78);assert.equal(proposal.last_signal,'2026-11-05T15:45:00-05:00');assert.equal(proposal.expiry,'2026-11-05T16:00:00-05:00');assert.equal(proposal.A_route_active,false);assert.equal(proposal.automatic_rearming,false);assert.equal(proposal.special_volume_filter_required,false);assert.equal(proposal.support_zone_visit_required,false);assert.equal(proposal.close_gt_open_required,false);assert.equal(proposal.regular_price_gt_fundamental_cap_requires_new_review_before_reactivation,66.5);
assert.equal(proposal.signal_exists,false);assert.equal(proposal.order_sent,false);assert.equal(proposal.fill_confirmed,false);assert.equal(proposal.current_approved_quantity,0);
for(const lang of ['es','en']){now.t.setLang(lang);const h=now.t.profileSummaryCard(p).match(/<aside class="stock-note prospective-study">([\s\S]*?)<\/aside>/)[1];assert(h.includes('09:45–15:45 EST'));assert(h.includes(lang==='es'?'caduca el 5 noviembre':'expires November 5'));assert(h.includes(lang==='es'?'cancelación manual confirmada':'confirmed manual cancellation'));assert(h.includes(lang==='es'?'no reglas universales':'not universal rules'));assert(!/Nov(?:ember)? (?:9|10)|9 noviembre|10 noviembre/.test(h));}
for(const filename of ['evaluate_signal.py','signal_tests.json','signal_boundary_tests.json'])assert(fs.existsSync(publicDir+'/'+filename));
console.log('PASS B 15-minute first-window semantics, November 5 expiry, exact inequalities, no special volume/green/zone filter, inactive A and no operative approvals.');
