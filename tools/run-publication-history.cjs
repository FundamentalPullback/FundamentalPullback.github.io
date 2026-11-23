// Keep the existing dated assertions intact. They describe the last published
// tree before the next scan/research batch, not a permanently current profile.
const assert=require('node:assert/strict'),fs=require('node:fs'),os=require('node:os'),path=require('node:path'),cp=require('node:child_process');
const root=path.resolve(__dirname,'..');
const recorded='dd0d359bd640fcf9203f96f4ca3df33a2a60bdcb';
const historicalTests=[
 'test-scanner-nov4.cjs','test-scanner-nov5.cjs','test-scanner-nov9.cjs',
 'test-research-batch90-nov11.cjs','test-research-gnxpi-nov11.cjs','test-research-you-nov11.cjs','test-research-br-nov11.cjs',
 'test-research-chdn-decision-nov11.cjs','test-research-htht-refresh-nov11.cjs','test-research-ryan-decision-nov11.cjs',
 'test-research-bmi-decision-nov11.cjs','test-research-kr-decision-nov11.cjs','test-research-bah-decision-nov11.cjs',
 'test-research-epam-decision-nov11.cjs','test-research-aeo-decision-nov11.cjs'
];
const publicRepo='https://github.com/FundamentalPullback/FundamentalPullback.github.io.git';
// Commits directly referenced by the required publication contracts. Explicit
// public fetches also work in a fresh depth-one checkout, without credentials.
const historyRefs=[recorded,
 '9c3211ed3342af058f1966c383fef570527addd1','36a01fc52c03745d7634ce954e1d224ea36cd4ef','6fd3af3817a2dca0cef876dd4d731b82d4872efb',
 '95473b63181956de842a1e0d37237271480d9138','7f750ca7d66cdb6a486e4e7197b7dbe0579f94b2','09aad1a4434929580e76e5572c6ecffb422b8e6d',
 '7824c2042c85282351344e25c410a5a9ffbd7fdc','2757327e1fa60961a76a5bee0e9f7facf8126d4c','31fc8692fec17deacbef049ddb04ec7d4bad230c',
 '0a82b2d453f498de6dee12d5718f93074b4068e2', '624de566c67fd77bddde9393cd89adcbfabbac63',
 '2824694bbce4c77b9a946cc500605b9694571cff','731ce46cc892ca2cf90cc7c1f72da4717b861f6e','c5e9d9d8f2b6e57de97ac48f00d93713ac093475',
 'd7beca1ecc6ebdd2b17596d0207d64c9541f3373','e5e87a029bd3d86c6010c8967a4dce0541e977d1'
];
const git=(args,options={})=>cp.execFileSync('git',args,{cwd:root,timeout:120000,...options});
function present(ref){return cp.spawnSync('git',['cat-file','-e',ref+'^{commit}'],{cwd:root,stdio:'ignore'}).status===0;}
const missing=historyRefs.filter(ref=>!present(ref));
if(missing.length){
 console.log(`Reading ${missing.length} pinned public Git revisions for the publication tests.`);
 git(['-c','credential.helper=','fetch','--no-tags','--depth=1',publicRepo,...missing],{stdio:'inherit',env:{...process.env,GIT_TERMINAL_PROMPT:'0'}});
}
for(const ref of historyRefs)assert(present(ref),'Required public Git revision unavailable: '+ref);
const staging=fs.mkdtempSync(path.join(os.tmpdir(),'fp-publication-history-')),snapshot=path.join(staging,'tree');
let added=false;
try {
 git(['worktree','add','--detach','--quiet',snapshot,recorded]);added=true;
 assert.equal(git(['rev-parse','HEAD'],{cwd:snapshot,encoding:'utf8'}).trim(),recorded);
 assert.equal(git(['status','--porcelain'],{cwd:snapshot,encoding:'utf8'}).trim(),'');
 for(const test of historicalTests){
  const file='tools/'+test;
  assert(fs.readFileSync(path.join(snapshot,file)).equals(fs.readFileSync(path.join(root,file))),`Preserve exact dated assertions: ${test}`);
  console.log(`Dated replay ${test} at ${recorded.slice(0,7)}`);
  cp.execFileSync(process.execPath,[file],{cwd:snapshot,stdio:'inherit',timeout:120000});
 }
 const load=require('./load-stock-profiles.cjs'),before=load(snapshot),now=load(root);
 const json=x=>JSON.parse(JSON.stringify(x));
 const priorManifest=before.c.window.FP_MANIFEST,currentManifest=now.c.window.FP_MANIFEST;
 assert.equal(currentManifest.scanRows,now.c.FP.scan.length,'Current scanner manifest counts all actual rows');
 assert(currentManifest.scannerAsOf>=priorManifest.scannerAsOf,'Current scanner date does not roll back');
 assert.deepEqual(json(now.c.FP.scan.filter(row=>row[0]<=priorManifest.scannerAsOf)),json(before.c.FP.scan),'Later scanner loads preserve all dated rows and source precision');
 for(const [date,audit] of Object.entries(before.c.window.FP_SCAN_AUDIT))assert.equal(JSON.stringify(now.c.window.FP_SCAN_AUDIT[date]),JSON.stringify(audit),'Historic scanner audit unchanged: '+date);
 const currentById=new Map(now.reports.map(r=>[r.id,r]));
 assert.equal(currentById.size,now.reports.length,'Current library IDs are unique');
 for(const r of before.reports)assert.equal(JSON.stringify(currentById.get(r.id)),JSON.stringify(r),'Preserve original reports in the current archive: '+r.id);
 const profiles=new Map(now.profiles.map(p=>[p.ticker,p]));
 for(const p of before.profiles){
  const next=profiles.get(p.ticker);assert(next,'Preserve historical ticker: '+p.ticker);
  for(const a of p.analyses){
   if(a.report){const old=next.analyses.find(x=>x.id===a.id&&x.date===a.date);assert(old&&old.isComplete===a.isComplete,`${p.ticker} keeps archived ${a.id} and its original depth`);}
   if(a.date)assert(next.latestAnalysis?.date>=a.date,`${p.ticker} does not lose its latest dated assessment`);
  }
 }
 for(const [ticker,id] of [['BR','A783'],['AXS','A784']]){
  const p=profiles.get(ticker),r=currentById.get(id),meta=r?.profiles.find(m=>m.ticker===ticker);
  assert(meta&&meta.stage3Complete&&!meta.entryApproved&&meta.approvedQuantity===0,`${id}: completed research stays separate from entry approval`);
  assert(p.completed.some(a=>a.id===id)&&p.analyses.some(a=>a.id===id),`${ticker}: new completed research linked without losing the record it superseded`);
  if(p.latestCompleted.id===id&&p.latestAnalysis.id===id){const balance=now.engine.researchBalance(p);assert.equal(balance.sourceId,id);assert.equal(balance.status,'ready');}
 }
 console.log(`PASS ${historicalTests.length} byte-identical dated suites; current archive, scanner history, successor linkage and evidence cross-checks.`);
} finally {
 if(added)git(['worktree','remove',snapshot]);
 fs.rmdirSync(staging);
}
