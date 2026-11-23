const assert=require('assert/strict'),path=require('path');
const {t,profiles}=require('./load-stock-profiles.cjs')(path.resolve(__dirname,'..'));
const currentHrb=profiles.find(p=>p.ticker==='HRB'),aso=profiles.find(p=>p.ticker==='ASO');
// Calendar supersession at the November 4 review remains a historical fixture.
const datedHrb=t.S.ges.filter(r=>r.ticker==='HRB'&&r.date==='2026-11-04'&&r.rep==='A247');assert.equal(datedHrb.length,1);
const historicalAnalysis=currentHrb.analyses.find(a=>a.id==='A082');assert(historicalAnalysis);
const hrb={...currentHrb,latestAnalysis:historicalAnalysis,latestManagement:datedHrb[0]};
const before=JSON.stringify({dec:t.S.dec,ges:t.S.ges,ops:t.S.ops,acct:t.S.acct,hist:t.S.hist});
for(const lang of ['es','en']){
 t.setLang(lang);const h=t.renderProfile(hrb),a=t.renderProfile(aso);
 if(currentHrb.latestAnalysis.date>'2026-11-04'){const current=t.renderProfile({...currentHrb,latestManagement:datedHrb[0]});assert(!current.includes(lang==='es'?'Próximo paso del informe histórico':'Historical report next step'));}
 assert(h.includes(lang==='es'?'Próximo paso del informe histórico (puede estar superado): ':'Historical report next step (may be superseded): '));
 assert(h.includes(lang==='es'?'Resultados ~5 nov':'Results ~Nov 5'));
 assert(h.includes(lang==='es'?'Próximo paso de la revisión histórica':'Historical review next step'));
 const cal=h.match(/<p class="profile-management-calendar">([\s\S]*?)<\/p>/)[1];
 assert(cal.includes(lang==='es'?'4 nov 2026':'Nov 4, 2026'));
 assert(cal.includes(lang==='es'?'Resultados 9 nov':'Results Nov 9'));
 assert(!cal.includes('~5 nov')&&!cal.includes('~Nov 5'));
 assert(a.includes(lang==='es'?'Próximos resultados sin fecha primaria exacta confirmada.':'Next exact earnings date unconfirmed in primary sources.'));
 // Generic future ticker: dates, not ticker/report IDs, govern supersession.
 const future=JSON.parse(JSON.stringify(hrb));future.ticker='FUTURECAL';future.latestManagement={...future.latestManagement,ticker:'FUTURECAL',date:'2099-01-05',rep:'FUTURE',next:'Evento futuro por confirmar',nextEn:'Future event unconfirmed'};
 const f=t.renderProfile(future);assert(f.includes('2099'));assert(f.includes(lang==='es'?'Evento futuro por confirmar':'Future event unconfirmed'));assert(f.includes(lang==='es'?'informe histórico':'Historical report next step'));
 // Older, same-date, undated and absent management never supersede newer research.
 for(const date of ['2020-01-01',hrb.latestAnalysis.date,'']) {const q={...hrb,latestManagement:{...hrb.latestManagement,date}}; const out=t.renderProfile(q);assert(!out.includes(lang==='es'?'Próximo paso del informe histórico':'Historical report next step'));}
 const q={...hrb,latestManagement:null};assert(!t.renderProfile(q).includes('profile-management-calendar'));
}
assert.equal(JSON.stringify({dec:t.S.dec,ges:t.S.ges,ops:t.S.ops,acct:t.S.acct,hist:t.S.hist}),before);
console.log('PASS management calendar ES/EN: HRB historical Nov5 versus dated Nov9, ASO unknown, generic future ticker, strict newer-date guards and immutable records.');
const fs=require('fs');const html=fs.readFileSync(path.resolve(__dirname,'../index.html'),'utf8');
assert.equal((html.match(/onlyS2: "Opportunity ≥85"/g)||[]).length,2);
// Verify the same ≥85 rule through the actual scanner, including the explicit
// takeover lane. Do not pin the exact source string of either implementation.
const Module=require('node:module'),filename=path.join(__dirname,'load-stock-profiles.cjs'),m=new Module(filename,module);
m.filename=filename;m.paths=m.constructor._nodeModulePaths(__dirname);
const source=fs.readFileSync(filename,'utf8'),exportAnchor='profileRoute,renderProfile,';
assert.equal(source.split(exportAnchor).length,2);
m._compile(source.replace(exportAnchor,exportAnchor+'vEscaner,'),filename);
const {t:scan,c}=m.exports(path.resolve(__dirname,'..'));
const day='2026-11-20',targets=Object.keys(c.window.FP_SCAN_DEALS[day].targets),rows=Array.from(scan.S.scan).filter(r=>r.date===day);
assert(targets.length>0&&rows.some(r=>targets.includes(r.ticker)&&r.opp<85),'Fixture distinguishes takeover routing from the ordinary threshold');
const boundary=[{ticker:'FP84TEST',opp:84},{ticker:'FP85TEST',opp:85},{ticker:'FPNATEST',opp:null}].map(r=>({...rows[0],...r}));
scan.S.scan=Array.from(scan.S.scan).concat(boundary);scan.S.scanDate=day;
const admitted=h=>Array.from(h.matchAll(/<td class="t">([^<]+)<\/td>/g),x=>x[1]).sort();
const ordinary=rows.filter(r=>!targets.includes(r.ticker)).concat(boundary);
for(const lang of ['es','en']){
 scan.setLang(lang);scan.S.dealTargetsOnly=false;scan.S.onlyS2=true;
 assert.deepEqual(admitted(scan.vEscaner()),ordinary.filter(r=>r.opp!==null&&r.opp>=85).map(r=>r.ticker).sort(),'Ordinary scanner includes exactly the non-targets with scores ≥85, not null/84');
 scan.S.onlyS2=false;
 assert.deepEqual(admitted(scan.vEscaner()),ordinary.map(r=>r.ticker).sort(),'Turning the score filter off retains non-targets across all scores');
 scan.S.onlyS2=true;scan.S.dealTargetsOnly=true;
 assert.deepEqual(admitted(scan.vEscaner()),targets.slice().sort(),'Takeover lane is exact and does not drop lower-score targets');
 scan.S.scanDate='2026-11-10';
 assert.deepEqual(admitted(scan.vEscaner()),Array.from(scan.S.scan).filter(r=>r.date==='2026-11-10'&&r.opp!==null&&r.opp>=85).map(r=>r.ticker).sort(),'Prior session keeps the ordinary threshold even after takeover view');
 scan.S.scanDate=day;
}
assert(html.includes("S.onlyS2=params.get('stage2')!=='0'"));
assert(html.includes('no certifica Stage 1, Stage 2'));assert(html.includes('does not certify Stage 1, Stage 2'));
console.log('PASS score-only filter labels, preserved Opportunity threshold and legacy route, bilingual no-Stage1/Stage2-certification notice.');
