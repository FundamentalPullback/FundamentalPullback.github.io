// Exact append-only post-earnings supplements; no network, account or spreadsheet writes.
const fs=require('fs'),path=require('path'),assert=require('assert/strict'),crypto=require('crypto'),vm=require('vm'),Module=require('module');
const root=path.resolve(__dirname,'..'),contract=JSON.parse(fs.readFileSync(path.join(__dirname,'morning-earnings-contract.json'),'utf8'));
const sha=b=>crypto.createHash('sha256').update(b).digest('hex'),clone=x=>JSON.parse(JSON.stringify(x));
const filename=path.join(__dirname,'load-stock-profiles.cjs'),m=new Module(filename,module);m.filename=filename;m.paths=module.paths;
m._compile(fs.readFileSync(filename,'utf8').replace('profileRoute,renderProfile,','profileRoute,renderProfile,profileCardData,'),filename);
const a=m.exports(root),ids=['A280','A281','A282'],tickers=['FA','ROK','IMAX'];
const successor=require('./current-price-contract.cjs').validate(root,a);
assert.equal(sha(fs.readFileSync(root+'/index.html')),successor.indexSha256,'Exact audited current-price UI successor');
for(const [f,h] of Object.entries(contract.dataHashes))assert.equal(sha(fs.readFileSync(root+'/data/'+f)),f==='stock-profiles.js'?successor.engineSha256:h,'All prior data preserved, exact separately tested engine successor: '+f);
const actualManifest=clone(a.c.window.FP_MANIFEST),expectedManifest=clone(contract.priorManifest);expectedManifest.libraryFiles.push('data/lib-morning-earnings.js','data/lib-current-price-reviews.js');expectedManifest.generated=actualManifest.generated;
assert.deepEqual(actualManifest,expectedManifest,'Only version and dedicated library addition in manifest');assert(Date.parse(actualManifest.generated)>Date.parse(contract.priorManifest.generated));
assert.equal(sha(fs.readFileSync(root+'/data/lib-morning-earnings.js')),contract.librarySha256);
const originalDec=fs.readFileSync(root+'/data/dec.js'),prefix='window.FP=window.FP||{};FP.dec=';
assert(originalDec.toString().startsWith(prefix)&&originalDec.toString().endsWith('];\n'));
const rows=JSON.parse(originalDec.toString().slice(prefix.length,-2));assert.equal(rows.length,contract.rows+3);
assert.equal(sha(Buffer.concat([originalDec.subarray(0,contract.bytes-3),Buffer.from('];\n')])),contract.sha256,'Exact old decision byte prefix');assert.equal(sha(JSON.stringify(rows.slice(contract.rows))),contract.appendSha256,'Only exact new append');
const pending=JSON.parse(fs.readFileSync(root+'/tools/pending-web-commentary.json','utf8'));
assert.equal(pending.pending.length,contract.priorPending.pending.length+6,'Only exact six research markers after this old baseline');assert.deepEqual(pending.pending.slice(-3).map(x=>x.reportId),successor.ids);assert.deepEqual(pending.pending.slice(0,contract.priorPending.pending.length),contract.priorPending.pending,'All previous pending reconciliation records preserved');assert.deepEqual(pending.pending.slice(contract.priorPending.pending.length,contract.priorPending.pending.length+3).map(x=>x.reportId),ids);
for(const [id,h] of Object.entries(contract.historicalReportHashes))assert.equal(sha(JSON.stringify(a.reports.find(r=>r.id===id))),h,'Original report preserved '+id);
assert(!a.reports.some(r=>r.id==='A279'),'Paused candidate remains absent');
const before=JSON.stringify({lib:a.reports,dec:a.t.S.dec,ops:a.t.S.ops,ges:a.t.S.ges,acct:a.t.S.acct,hist:a.t.S.hist});
const priceBy={FA:23,ROK:445,IMAX:51.76},contextBy={FA:23.91,ROK:393.43,IMAX:50.51};
for(let i=0;i<3;i++){
 const tk=tickers[i],id=ids[i],report=a.reports.find(r=>r.id===id),p=a.profiles.find(x=>x.ticker===tk),meta=report.profiles[0],d=a.t.profileCardData(p),row=rows[contract.rows+i],folder=root+'/research/2026-11-05/'+tk+'-post-earnings/',verification=contract.sourceVerification[tk];
 assert.equal(a.reports.filter(r=>r.id===id).length,1);assert.equal(report.schema,'fp.post-earnings-supplement.v1');assert.equal(report.type,'post-earnings-supplement');assert.equal(meta.kind,'partial');assert.equal(meta.earningsUpdateComplete,true);
 for(const key of ['stage3Complete','latestCompletedEligible','fundamentalApproved','stage35Complete','stage35Approved','entryApproved','postResultsDailyTrendVerified'])assert.equal(meta[key],false,tk+' '+key);
 for(const key of ['approvedQuantity','signal','entryPrice','quantity','maximumConditioned','fundamentalMaximum','technicalMaximum','operativeStop','currentQP','currentOpportunity'])assert.equal(meta[key],null,tk+' '+key);
 assert.equal(meta.valuation.status,'unavailable');for(const key of ['bear','base','bull'])assert.equal(meta.valuation[key],null);assert(!('close' in meta),'No intraday observation in close facts');assert(!('entryPlan' in report));
 assert.equal(d.model,null);assert.equal(d.scan.price,priceBy[tk]);assert.equal(d.scan.date,'2026-11-04');assert(!d.close||d.close.price!==contextBy[tk],'Intraday context never becomes regular close');
 assert.equal(p.latestAnalysis.id,id);assert.equal(p.latestAnalysis.isComplete,false);assert.equal(p.latestReview.rep,id);assert.equal(p.latestReview.decision,'En observación');
 if(tk==='FA'){assert.equal(p.latestCompleted.id,'A122');assert.equal(p.latestCompleted.date,'2026-10-30');assert(p.reports.some(x=>x.id==='A113'));assert(p.reports.some(x=>x.id==='A122'));assert.equal(a.engine.researchBalance(p).status,'newer-analysis');}
 else {assert.equal(p.latestCompleted,null);assert.equal(a.engine.researchBalance(p).status,'no-analysis');}
 assert.equal(row.length,40);assert.equal(row[3],priceBy[tk]);assert.equal(row[0],'2026-11-04');assert.equal(row[4],'2026-11-05');for(let j=8;j<=13;j++)assert.equal(row[j],null,'No numerical valuation or ceiling in decision');
 assert.equal(meta.prosCons.sourceFingerprint,a.engine.balanceFingerprint(report.text));assert(a.engine.balanceStructured({...meta.prosCons,ticker:tk,reportId:id},report,tk,'2026-11-05','test'));
 const editorial=JSON.parse(fs.readFileSync(folder+'editorial_metadata.json','utf8')),original=fs.readFileSync(folder+'report.md','utf8'),full=fs.readFileSync(folder+'website_report.md','utf8'),page=fs.readFileSync(folder+'index.html','utf8');assert.equal(full,report.text);assert(full.includes(original));
 for(const x of [editorial.summary,...editorial.pros,...editorial.risks]){assert(original.includes(x.evidence_quote));if(x.additional_evidence_quote)assert(original.includes(x.additional_evidence_quote));assert(full.includes(x.source_url));assert(full.includes(x.es));assert(full.includes(x.en));}
 for(const [name,h] of Object.entries(verification.publicFileSha256))assert.equal(sha(fs.readFileSync(folder+name)),h,'Audited source byte preservation '+tk+'/'+name);
 assert.equal(sha(fs.readFileSync(folder+tk+'_post_results_20261105.zip')),verification.archiveSha256);
 const pub=JSON.parse(fs.readFileSync(folder+'publication_record.json','utf8'));assert.equal(pub.public_readiness,'ready_partial_only');assert.equal(pub.independent_audit_status,'pass_partial_supplement');assert.equal(pub.context_quote.type,'intraday_not_executable');assert.equal(pub.context_quote.price,contextBy[tk]);
 assert(page.includes('name="viewport"'));assert(page.includes('Stage 3 pendiente / pending'));assert(page.includes('Sin entrada / No entry'));assert(page.includes('table-wrap')||!page.includes('<table'));assert(page.includes('href="../../../#ficha/'+tk+'"'));
 for(const lang of ['es','en'])for(const inline of [true,false]){a.t.setLang(lang);const out=a.t.profileSummaryCard(p,inline),metrics=out.match(/<dl class="stock-summary-values">([\s\S]*?)<\/dl>/)[1];assert(out.includes(lang==='es'?meta.summary:meta.summaryEn));assert(out.includes('#biblioteca/'+id));assert(metrics.includes('<dd class="stock-estimate">—</dd>'));assert(!metrics.includes(String(contextBy[tk])));assert(!/NaN|undefined|Infinity/.test(out));}
 for(const name of fs.readdirSync(folder)){if(name.endsWith('.zip'))continue;const text=fs.readFileSync(folder+name,'utf8');assert(!/\/workspace\/|\/agent_notes\/|\/user_notes\/|\/home\/agent\/|file:\/\/|BEGIN PRI[V]ATE KEY|Bea[r]er /i.test(text),'No internal/secret data '+name);assert(!/\.(?:pdf|png|jpg|jpeg)$/i.test(name),'No third-party raw source dumps');}
 const marker=pending.pending.find(x=>x.reportId===id);assert.equal(marker.sourceFingerprint,meta.prosCons.sourceFingerprint);assert.equal(marker.supplement,'research/2026-11-05/'+tk+'-post-earnings/website_report.md');
}
assert.equal(JSON.stringify({lib:a.reports,dec:a.t.S.dec,ops:a.t.S.ops,ges:a.t.S.ges,acct:a.t.S.acct,hist:a.t.S.hist}),before,'Rendering never mutates data');
// Duplicate library loading is idempotent, like all append-only chunks.
const count=a.reports.length;vm.runInContext(fs.readFileSync(root+'/data/lib-morning-earnings.js','utf8'),a.c);assert.equal(a.c.window.FP_LIB.reports.length,count);
console.log('PASS A280 FA / A281 ROK / A282 IMAX: partial earnings only; all current value, ceiling, signal, stop and quantity fields unavailable; no approvals; no new close facts.');
console.log('PASS old source/data/report bytes and exact decision prefix; paused A279 absent; audited public artifacts and exact bilingual evidence; historical FA completion; ES/EN cards; no internal paths; pending Sheet sync and idempotence.');
