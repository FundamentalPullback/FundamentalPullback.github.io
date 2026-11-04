const fs=require('fs'),assert=require('assert/strict'),load=require('./load-stock-profiles.cjs');
const {c,t,engine:e,profiles,html,reports}=load();
const before=JSON.stringify({reports,dec:t.S.dec,scan:t.S.scan,ops:t.S.ops});let both=0,one=0,missing=0;
for(const p of profiles){const d=e.researchBalance(p);if(d.status==='ready'){d.pros.length&&d.cons.length?both++:one++;assert.equal(d.sourceId,p.latestCompleted.id);assert.equal(d.date,p.latestCompleted.date);for(const x of [...d.pros,...d.cons]){assert(d.report.text.includes(x.evidence),p.ticker);if(x.sourceUrl)assert(d.report.text.includes(x.sourceUrl),p.ticker);}}else missing++;
 for(const lang of ['es','en'])for(const inline of [true,false]){t.setLang(lang);const h=t.profileSummaryCard(p,inline);assert.equal((h.match(/class="stock-balance"/g)||[]).length,1);assert(h.includes('aria-label="'));assert(h.includes(lang==='en'?'Pros &amp; cons':'Pros y contras'));assert(!/undefined|NaN|Infinity/.test(h));assert(h.indexOf('stock-summary-main')<h.indexOf('stock-balance'));assert(h.includes('profile-chart'));assert(h.includes('profile-quote'));}
}
assert.equal(JSON.stringify({reports,dec:t.S.dec,scan:t.S.scan,ops:t.S.ops}),before);
const report={id:'FUTURE',date:'2099-01-01',text:'Recurring revenue rose 9%. Customer losses remain a concern.',profiles:[{ticker:'NEWX',kind:'complete',completedAt:'2099-01-01'}]};
const record={schema:'fp.research-balance.v1',ticker:'NEWX',reportId:report.id,asOf:report.date,sourceFingerprint:e.balanceFingerprint(report.text),pros:[{text:'Ingresos recurrentes +9%.',textEn:'Recurring revenue +9%.',evidence:'Recurring revenue rose 9%.'}],cons:[{text:'Persisten las bajas de clientes.',textEn:'Customer losses remain a concern.',evidence:'Customer losses remain a concern.'}]};
report.profiles[0].prosCons=record;
let p=e.build({reports:[report]})[0];assert.equal(e.researchBalance(p).status,'ready');assert.equal(e.researchBalance(p).mode,'structured-report');
// Same ID revised without re-authoring the source summary: fail closed despite old quotes surviving.
report.text+=' Correction: growth was overstated.';p=e.build({reports:[report]})[0];assert.equal(e.researchBalance(p).status,'stale');
record.sourceFingerprint=e.balanceFingerprint(report.text);assert.equal(e.researchBalance(e.build({reports:[report]})[0]).status,'ready');
// New analysis is selected; no stale old summary survives when it lacks evidence metadata.
const newer={id:'FUTURE2',date:'2099-01-02',text:'New results without a reviewed concise summary.',profiles:[{ticker:'NEWX',kind:'complete',completedAt:'2099-01-02'}]};p=e.build({reports:[report,newer]})[0];assert.equal(e.researchBalance(p).status,'pending');assert.equal(e.researchBalance(p).sourceId,'FUTURE2');
newer.profiles[0].kind='partial';p=e.build({reports:[report,newer]})[0];assert.equal(e.researchBalance(p).status,'newer-analysis');
// Exact quote, date, URLs, explicit company scope and full report identity are mandatory.
function rejected(changes){const r=JSON.parse(JSON.stringify(record));Object.assign(r,changes);return !e.balanceStructured(r,report,'NEWX',record.asOf,'test');}
assert(rejected({asOf:'2099-02-30'}));assert(rejected({ticker:'OTHER'}));assert(rejected({reportId:'OTHER'}));assert(rejected({sourceFingerprint:'different'}));assert(rejected({pros:[{text:'Unsupported inference',evidence:'invented positive fact'}]}));assert(rejected({pros:[{text:'Link not in source',evidence:record.pros[0].evidence,sourceUrl:'https://example.com/unverified'}]}));assert(rejected({pros:[{text:'Unsafe link',evidence:record.pros[0].evidence,sourceUrl:'javascript:alert(1)'}]}));assert(rejected({pros:[record.pros[0],record.pros[0],record.pros[0],record.pros[0]]}));
const prose={id:'PROSE',date:'2099-01-03',text:'## Pros · NEWX\n- Revenue grew, but cash conversion weakened.\n## Cons · NEWX\n- Debt maturities constrain flexibility.\n## Pros · OTHER\n- Revenue doubled at a different company.\n## Cons · OTHER\n- Other company is at risk.\n',profiles:[{ticker:'NEWX',kind:'complete',completedAt:'2099-01-03'}]};
assert.equal(e.researchBalance(e.build({reports:[prose]})[0]).status,'pending');prose.profiles[0].prosConsSectionsFingerprint=e.balanceFingerprint(prose.text);let d=e.researchBalance(e.build({reports:[prose]})[0]);assert.equal(d.status,'ready');assert.equal(d.mode,'explicit-sections');assert.equal(d.pros.length,1);assert(d.pros[0].text.includes('but cash conversion weakened'));assert(!JSON.stringify(d.pros).includes('doubled'));prose.text+='New correction.';assert.equal(e.researchBalance(e.build({reports:[prose]})[0]).status,'pending');
assert(!e.balanceExplicit({...prose,text:'## Business quality\n- Revenue rose.\n## Risks\n- Debt rose.'},'NEWX',prose.date));
// No source/model or pending-event passage becomes a green fact based on generic polarity.
assert.equal(e.researchBalance({ticker:'NOPE'}).status,'no-analysis');
// Source text is escaped; source link validated before output.
const malicious=JSON.parse(JSON.stringify(record));malicious.pros[0].text='<img src=x onerror=alert(1)> Revenue';report.profiles[0].prosCons=malicious;p=e.build({reports:[report]})[0];t.setLang('es');const escaped=t.profileBalancePanel(p);assert(escaped.includes('&lt;img'));assert(!escaped.includes('<img'));
// Passing time or receiving a live quote never changes the dated source summary.
report.profiles[0].prosCons=record;p=e.build({reports:[report]})[0];const old=e.researchBalance(p);t.S.live={prices:{NEWX:{p:9999}},at:Date.now()};assert.equal(e.researchBalance(p).pros[0].text,old.pros[0].text);
assert(html.includes('@media(min-width:1100px){.stock-summary-layout{grid-template-columns:minmax(0,1fr) 292px}'));assert(html.includes('.stock-balance .balance-pros li{color:var(--ok)}'));assert(html.includes('.stock-balance .balance-cons li{color:var(--neg)}'));assert(html.includes('grid-template-columns:minmax(0,1fr);gap:20px'));assert(!/\.stock-balance[^}]*position:\s*(fixed|absolute)/.test(html));
console.log('PASS',profiles.length,'ES/EN inline/direct panels;',both,'both sides;',one,'one side;',missing,'explicit pending. Evidence/source date and scope, stale same-ID corrections, new complete/partial publications, no quote/event inference, safe URLs/HTML, immutable decisions, responsive flow and color-independent labels.');

// Explicit source-grounded unavailable reasons can authorize publication without invented bullets.
newer.profiles[0].kind='complete';newer.profiles[0].prosConsUnavailable={schema:'fp.research-balance-unavailable.v1',asOf:newer.date,sourceFingerprint:e.balanceFingerprint(newer.text),reason:'Falta evidencia suficiente para resumir ambos lados.',reasonEn:'Insufficient evidence to summarize both sides.'};
p=e.build({reports:[report,newer]})[0];assert.equal(e.researchBalance(p).status,'unavailable');newer.text+='Correction.';assert.equal(e.researchBalance(e.build({reports:[report,newer]})[0]).status,'stale');
const builder=fs.readFileSync(require('path').join(__dirname,'build-stock-balance.cjs'),'utf8');assert(builder.includes('Completed research needs reviewed pros/cons'));
console.log('PASS publication guard requires reviewed summaries or explicit unavailable reason; reason invalidates on source correction.');
// Real compilation integration: a new unstructured completion blocks; an explicit
// unavailable assessment or evidence-backed structured summary can be published.
const os=require('os'),path=require('path'),cp=require('child_process');const tmp=fs.mkdtempSync(path.join(os.tmpdir(),'fp-balance-test-'));
try{
 const source=path.resolve(__dirname,'..');for(const name of ['data','tools'])fs.cpSync(path.join(source,name),path.join(tmp,name),{recursive:true});fs.copyFileSync(path.join(source,'index.html'),path.join(tmp,'index.html'));
 const chunk=path.join(tmp,'data/lib-overnight-nov4.js'),original=fs.readFileSync(chunk,'utf8');
 const newReport={id:'QA-FUTURE',date:'2099-02-01',title:'NEWQA completed research',text:'Recurring revenue grows ten percent. Customer losses remain a concern.',profiles:[{ticker:'NEWQA',kind:'complete',completedAt:'2099-02-01'}]};
 function writeNew(){fs.writeFileSync(chunk,original+'\nwindow.FP_LIB.reports.push('+JSON.stringify(newReport)+');\n');}
 function compile(){return cp.spawnSync(process.execPath,[path.join(tmp,'tools/build-stock-balance.cjs')],{encoding:'utf8'});}
 writeNew();let result=compile();assert.notEqual(result.status,0);assert(result.stderr.includes('Completed research needs reviewed pros/cons'));
 newReport.profiles[0].prosConsUnavailable={schema:'fp.research-balance-unavailable.v1',asOf:newReport.date,sourceFingerprint:e.balanceFingerprint(newReport.text),reason:'Sin evidencia suficiente para una síntesis fiable.'};writeNew();result=compile();assert.equal(result.status,0,result.stderr);
 delete newReport.profiles[0].prosConsUnavailable;newReport.profiles[0].prosCons={schema:'fp.research-balance.v1',asOf:newReport.date,sourceFingerprint:e.balanceFingerprint(newReport.text),pros:[{text:'Ingresos recurrentes +10%.',evidence:'Recurring revenue grows ten percent.'}],cons:[{text:'Persisten las bajas de clientes.',evidence:'Customer losses remain a concern.'}]};writeNew();result=compile();assert.equal(result.status,0,result.stderr);
 newReport.text+=' Correction: new information.';writeNew();result=compile();assert.notEqual(result.status,0);
}finally{fs.rmSync(tmp,{recursive:true,force:true});}
console.log('PASS actual publication compilation: new completed source without evidence blocks, explicit pending permitted, structured summary accepted, correction blocks until re-reviewed.');
