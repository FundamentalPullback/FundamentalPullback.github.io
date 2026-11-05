const assert=require('assert/strict'),path=require('path');
const {t,profiles}=require('./load-stock-profiles.cjs')(path.resolve(__dirname,'..'));
const currentHrb=profiles.find(p=>p.ticker==='HRB'),aso=profiles.find(p=>p.ticker==='ASO');
// Calendar supersession at the November 4 review remains a historical fixture.
const datedHrb=t.S.ges.filter(r=>r.ticker==='HRB'&&r.date==='2026-11-04'&&r.rep==='A247');assert.equal(datedHrb.length,1);
const hrb={...currentHrb,latestManagement:datedHrb[0]};
const before=JSON.stringify({dec:t.S.dec,ges:t.S.ges,ops:t.S.ops,acct:t.S.acct,hist:t.S.hist});
for(const lang of ['es','en']){
 t.setLang(lang);const h=t.renderProfile(hrb),a=t.renderProfile(aso);
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
assert(html.includes("if (S.onlyS2 && !(r.opp !== null && r.opp >= 85)) return false;"));
assert(html.includes("S.onlyS2=params.get('stage2')!=='0'"));
assert(html.includes('no certifica Stage 1, Stage 2'));assert(html.includes('does not certify Stage 1, Stage 2'));
console.log('PASS score-only filter labels, preserved Opportunity threshold and legacy route, bilingual no-Stage1/Stage2-certification notice.');
