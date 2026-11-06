// Exact partial research successor. Offline tests only; no account, refresh or remote writes.
const fs=require('fs'),path=require('path'),assert=require('assert/strict'),crypto=require('crypto'),Module=require('module'),vm=require('vm');
const root=path.resolve(__dirname,'..'),clone=x=>JSON.parse(JSON.stringify(x)),sha=b=>crypto.createHash('sha256').update(b).digest('hex');
const filename=path.join(__dirname,'load-stock-profiles.cjs'),m=new Module(filename,module);m.filename=filename;m.paths=module.paths;m._compile(fs.readFileSync(filename,'utf8').replace('profileRoute,renderProfile,','profileRoute,renderProfile,profileCardData,'),filename);
const a=m.exports(root),contract=require('./trp-bsy-contract.cjs'),c=contract.validate(root,a);
for(const [f,h] of Object.entries(c.priorDataHashes))assert.equal(sha(require('./trailing-contract.cjs').priorBytes(root,'data/'+f)),h,'Every prior data file unchanged '+f);
for(const [f,h] of Object.entries(c.priorResearchHashes))assert.equal(sha(fs.readFileSync(root+'/'+f)),h,'Every prior research file unchanged '+f);
const rows=JSON.parse(fs.readFileSync(root+'/data/dec.js','utf8').slice('window.FP=window.FP||{};FP.dec='.length,-2)),pending=JSON.parse(fs.readFileSync(root+'/tools/pending-web-commentary.json'));
const before=JSON.stringify({reports:a.reports,dec:a.t.S.dec,ops:a.t.S.ops,ges:a.t.S.ges,acct:a.t.S.acct,hist:a.t.S.hist});
const walk=dir=>fs.readdirSync(dir).flatMap(n=>fs.statSync(path.join(dir,n)).isDirectory()?walk(path.join(dir,n)):[path.join(dir,n)]);
for(const [i,tk] of ['TRP','BSY'].entries()){
 const id=c.ids[i],report=a.reports.find(r=>r.id===id),meta=report.profiles[0],p=a.profiles.find(x=>x.ticker===tk),d=a.t.profileCardData(p),folder=root+'/research/2026-11-05/'+tk+'-post-earnings/',v=c.sourceVerification[tk],ed=JSON.parse(fs.readFileSync(folder+'editorial_metadata.json')),body=fs.readFileSync(folder+(tk==='TRP'?'dossier_es.md':'BSY_resultados_20261105.html'),'utf8'),full=fs.readFileSync(folder+'website_report.md','utf8'),page=fs.readFileSync(folder+'index.html','utf8');
 assert.equal(report.schema,'fp.post-earnings-supplement.v1');assert.equal(report.type,'post-earnings-supplement');assert.equal(meta.kind,'partial');assert.equal(meta.earningsUpdateComplete,true);
 for(const k of ['stage3Complete','latestCompletedEligible','fundamentalApproved','stage35Complete','stage35Approved','entryApproved','postResultsDailyTrendVerified'])assert.equal(meta[k],false,tk+' '+k);
 for(const k of ['currentPrice','fairValue','maxPrice','approvedQuantity','signal','entryPrice','quantity','maximumConditioned','fundamentalMaximum','technicalMaximum','operativeStop','currentQP','currentOpportunity'])assert.equal(meta[k],null,tk+' '+k);
 assert.equal(meta.valuation.status,'unavailable');for(const k of ['bear','base','bull'])assert.equal(meta.valuation[k],null);assert(!meta.close);assert(!report.entryPlan);
 assert.equal(p.latestAnalysis.id,id);assert.equal(p.latestAnalysis.isComplete,false);assert.equal(p.latestReview.rep,id);assert.equal(p.latestReview.decision,'En observación');assert.equal(p.latestCompleted,null);assert.equal(d.model,null);
 assert.equal(d.scan.price,tk==='TRP'?62.71:43.64);assert.equal(d.scan.date,'2026-11-04');assert(!d.close||d.close.price!==(tk==='TRP'?64.38:47.09));
 if(tk==='BSY'){assert(p.reports.some(r=>r.id==='A119'));assert(p.reports.some(r=>r.id==='A128')||p.decisions.some(r=>r.rep==='A128'));}
 assert.equal(rows[c.priorDecision.rows+i].length,40);for(let j=8;j<=13;j++)assert.equal(rows[c.priorDecision.rows+i][j],null);
 assert.equal(full,report.text);if(tk==='TRP')assert(full.includes(body));else{assert(!full.includes('<!DOCTYPE'));assert(full.includes('BSY_resultados_20261105.html'));assert(full.length<body.length/2,'Summary links to full original HTML rather than conversion');}
 assert.equal(sha(fs.readFileSync(folder+'editorial_metadata.json')),v.editorialSha256);
 for(const x of [ed.summary,...ed.pros,...ed.risks]){assert(body.includes(x.evidence_quote),'Exact original evidence');assert(full.includes(x.evidence_quote));assert(full.includes(x.es));assert(full.includes(x.en));assert(full.includes(x.source_url));}
 for(const [file,h] of Object.entries(v.publicFileSha256))assert.equal(sha(fs.readFileSync(folder+file)),h,'Audited original source '+tk+'/'+file);
 assert.equal(sha(fs.readFileSync(folder+'PUBLIC_FINAL.zip')),v.archiveSha256);
 assert.equal(meta.prosCons.sourceFingerprint,a.engine.balanceFingerprint(full));assert(a.engine.balanceStructured({...meta.prosCons,ticker:tk,reportId:id},report,tk,'2026-11-05','test'),'Evidence-bound reviewed balance');
 assert(page.includes('name="viewport"'));assert(page.includes('href="../../../#ficha/'+tk+'"'));assert(page.includes('Sin entrada / No entry'));assert(page.includes('Stage 3 pendiente / pending'));assert(page.includes('table-wrap')||!page.includes('<table'));
 assert(full.includes(tk==='TRP'?'15:34:29 UTC':'16:14:40 UTC'));assert(full.includes('Not live, a regular close or an executable quote'));assert(full.includes(tk==='TRP'?'not certified value':'neither issuer value nor stock-price downside'));
 for(const lang of ['es','en'])for(const inline of [true,false]){a.t.setLang(lang);const out=a.t.profileSummaryCard(p,inline),metrics=out.match(/<dl class="stock-summary-values">([\s\S]*?)<\/dl>/)[1];assert(out.includes(lang==='es'?meta.summary:meta.summaryEn));assert(out.includes('#biblioteca/'+id));assert(metrics.includes('<dd class="stock-estimate">—</dd>'));assert(!metrics.includes(tk==='TRP'?'64.38':'47.09'));assert(!/NaN|undefined|Infinity/.test(out));}
 for(const file of walk(folder)){if(file.endsWith('.zip'))continue;const text=fs.readFileSync(file,'utf8');assert(!/\/workspace\/|\/agent_notes\/|\/user_notes\/|\/home\/agent\/|file:\/\/|BEGIN PRI[V]ATE KEY|Bea[r]er /i.test(text),'No private data '+file);assert(!/\.(?:pdf|png|jpg|jpeg)$/i.test(file),'No full third-party source dumps');}
 const marker=pending.pending.find(x=>x.reportId===id);assert.equal(marker.sourceFingerprint,meta.prosCons.sourceFingerprint);assert.equal(marker.supplement,'research/2026-11-05/'+tk+'-post-earnings/website_report.md');
}
assert.equal(JSON.stringify({reports:a.reports,dec:a.t.S.dec,ops:a.t.S.ops,ges:a.t.S.ges,acct:a.t.S.acct,hist:a.t.S.hist}),before,'Rendering never mutates data');
for(const mutate of [r=>r.push({id:'A290'}),r=>r.push(clone(r.find(x=>x.id==='A286'))),r=>r.find(x=>x.id==='A119').title+='edited',r=>r.find(x=>x.id==='A287').profiles[0].valuation.base=23.91]){const bad={...a,reports:clone(a.reports)};mutate(bad.reports);assert.throws(()=>contract.validate(root,bad),'Any unpinned successor must fail closed');}
const count=a.reports.length;vm.runInContext(fs.readFileSync(root+'/'+c.library,'utf8'),a.c);assert.equal(a.c.window.FP_LIB.reports.length,count,'Idempotent dedicated chunk');
console.log('PASS A286 TRP and A287 BSY: partial only, no current valuation/price/ceiling/entry approval; prior scanner and report history preserved; exact original public bytes and ZIPs, evidence-bound ES/EN summary, safe HTML linking, pending reconciliation and fail-closed pinned successor.');
