const fs=require('fs'),vm=require('vm'),a=require('assert/strict'),path=require('path');
const root=path.resolve(__dirname,'..'),dir=root+'/data/';const c={window:{}};c.FP=c.window.FP={};vm.createContext(c);vm.runInContext(fs.readFileSync(dir+'manifest.js','utf8'),c);for(const f of [...c.window.FP_MANIFEST.files,'data/names.js',...c.window.FP_MANIFEST.libraryFiles,'data/stock-profiles.js'])vm.runInContext(fs.readFileSync(root+'/'+f,'utf8'),c);
const html=fs.readFileSync(root+'/index.html','utf8');let app=[...html.matchAll(/<script[^>]*>([\s\S]*?)<\/script>/g)].map(x=>x[1]).find(x=>x.includes('var DEC_MAP'));new vm.Script(app);app=app.slice(0,app.indexOf('  var hash ='))+app.slice(app.indexOf('  var PARTS ='),app.indexOf('  var DENY ='))+'\nwindow.TEST={S,PARTS,profiles,vFichas,renderProfile,profileRoute,acctCalc,profileCardData,profileSummaryCard,profileJsonRecords,latestScannerNotice,scannerNoticeArchive,vInicio,setLang:function(l){lang=l;}};render=function(){};})();';const noop=()=>{},el={addEventListener:noop,setAttribute:noop,querySelectorAll:()=>[],style:{}};Object.assign(c,{document:{getElementById:()=>el,addEventListener:noop,querySelectorAll:()=>[],querySelector:()=>el,hidden:false},localStorage:{getItem:()=>null},console,Date,Intl,setTimeout,clearTimeout,AbortController,location:{hash:'#fichas'},URL,URLSearchParams});c.window.addEventListener=noop;vm.runInContext(app,c);const t=c.window.TEST,e=c.window.FP_PROFILE_ENGINE,F=c.FP;
t.S.scan=t.PARTS.scan([F.scanHead].concat(F.scan));for(const k of ['dec','ges','ops','acct','hist'])t.S[k]=t.PARTS[k](F[k]);t.S.lib=c.window.FP_LIB.reports;t.S.libState='ok';t.S.snapshot=c.window.FP_MANIFEST.asOf;const data={scans:t.S.scan,decisions:t.S.dec,management:t.S.ges,operations:t.S.ops,reports:t.S.lib,names:c.window.FP_NAMES};let ps=e.build(data), by=Object.fromEntries(ps.map(p=>[p.ticker,p]));
let full=0,closing=0;for(const p of ps){let d=t.profileCardData(p);if(d.model)full++;if(d.close)closing++;for(let lang of ['es','en']){t.setLang(lang);let h=t.profileSummaryCard(p,true);a(h.includes(p.ticker));a(!h.includes('NaN'));a(!h.includes('undefined'));a(!h.includes('Infinity'));a(h.includes('stock-summary-values'));let all=t.renderProfile(p);a(all.indexOf('stock-summary')<all.indexOf('profile-metrics'));}}
t.S.profileQ=ps[0].ticker;t.S.profileTicker=null;t.S.profileFilter='all';a(t.vFichas().includes('stock-summary'));a(!t.vFichas().includes('class="profile-results"'));
// Quotes from live feed/account and scanner Last are never a regular close.
t.S.live={prices:{NOCLOSE:{p:123}},at:Date.now()};t.S.acct.prices.NOCLOSE={p:456};let p=e.build({scans:[{ticker:'NOCLOSE',date:'2026-11-04',price:789}]})[0];a.equal(t.profileCardData(p).close,null);a.equal(t.profileCardData(p).model,null);a.equal(t.profileCardData(p).scan.price,789);
// Future structured standalone report creates a current card without an index rebuild.
t.S.lib=t.S.lib.concat([{id:'FUTURE',date:'2026-11-05',title:'NEWX review',text:'',profiles:[{ticker:'NEWX',company:'New example',kind:'complete',completedAt:'2026-11-05',valuation:{base:30,bear:20,bull:40,asOf:'2026-11-05',labelEn:'Conditional'},close:{price:25,sessionDate:'2026-11-04',priceType:'regular-close'}}]}]);t.S.scan=t.S.scan.concat([{ticker:'NEWX',date:'2026-11-04',price:26}]);let newp=t.profiles().find(p=>p.ticker==='NEWX');a(newp);let fresh=t.profileCardData(newp);a.equal(fresh.model.base,30);a.equal(fresh.close.price,25);a.equal(fresh.scan.date,'2026-11-04');
// Newer withdrawals suppress older estimates, no-new-valuation preserves them.
let old={ticker:'TEST',adate:'2026-11-01',date:'2026-10-30',price:20,base:30,cons:10,fav:50,rep:'',vdate:'2026-11-01'};let no={...old,base:null,cons:null,fav:null,adate:'2026-11-05',vlab:'Sin valor justo certificado',vdate:''};p=e.build({decisions:[old,no]})[0];a.equal(t.profileCardData(p).model,null);no.vlab='Sin valoración nueva';p=e.build({decisions:[old,no]})[0];a.equal(t.profileCardData(p).model.base,30);
// Unstructured prose and non-matching JSON never produce numeric facts.
a.equal(t.profileJsonRecords('A price of $999 on 2026-11-05.').length,0);a.equal(t.profileJsonRecords('{"ticker":"TEST","regular_close":999}').length,0);
console.log('PASS',ps.length,'profiles in ES/EN;',full,'documented models;',closing,'documented closes; card-first exact search, provenance, source date separation, withheld values, all legacy fixtures and future automatic updates.');
// Conflicting same-session closes are withheld, rather than picked arbitrarily.
const oldSnapshot=t.S.snapshot;t.S.snapshot='2026-11-04';t.S.hist.NEWX={'2026-11-04':24};a.equal(t.profileCardData(newp).close,null);a.equal(t.profileCardData(newp).closeConflict,'2026-11-04');delete t.S.hist.NEWX;t.S.snapshot=oldSnapshot;
// Explicit unsupported currencies do not get formatted as USD.
t.S.lib=t.S.lib.concat([{id:'EURTEST',date:'2026-11-06',profiles:[{ticker:'EUROX',kind:'partial',valuation:{base:20,currency:'EUR',asOf:'2026-11-06'},close:{price:21,currency:'EUR',sessionDate:'2026-11-05',priceType:'regular-close'}}]}]);let ep=t.profiles().find(p=>p.ticker==='EUROX');a.equal(t.profileCardData(ep).model,null);a.equal(t.profileCardData(ep).close,null);
// A new source updates an existing ticker without changing the profile code.
t.S.lib=t.S.lib.concat([{id:'HPENEW',date:'2098-11-07',profiles:[{ticker:'HPE',kind:'complete',completedAt:'2098-11-07',valuation:{base:45,bear:25,bull:70,asOf:'2098-11-07'},close:{price:44,sessionDate:'2098-11-06',priceType:'regular-close'}}]}]);let hp=t.profiles().find(p=>p.ticker==='HPE');a.equal(t.profileCardData(hp).model.base,45);a.equal(t.profileCardData(hp).close.price,44);a.equal(hp.latestCompleted.id,'HPENEW');
console.log('PASS conflict withholding, unsupported currency guard, and existing-ticker automatic valuation/close update.');

// Today shows one current scanner notice, while old notices remain in the dated archive.
const originalScans=t.S.scan;for(const lang of ['es','en']){t.setLang(lang);const h=t.latestScannerNotice();a.equal((h.match(/latest-scanner-notice/g)||[]).length,1);require('./scanner-nov5-contract.cjs').validate(root);a(h.includes('data-scan-date="2026-11-05"')||h.includes('data-scan-date="2026-11-04"')||h.includes('data-scan-date="2026-11-03"'));a(!t.vInicio().includes('2 November close · research extended 3 November UTC'));a(!t.vInicio().includes('Cierre 2 noviembre · análisis ampliado 3 noviembre UTC'));a(t.scannerNoticeArchive('2026-11-02').includes('research/2026-11-02/index.html'));}
t.S.scan=originalScans.concat([{ticker:'FUTUREDAY',date:'2099-01-05',price:10,opp:90}]);for(const lang of ['es','en']){t.setLang(lang);let h=t.latestScannerNotice();a(h.includes('data-scan-date="2099-01-05"'));a(!h.includes('2026-11-03'));a(!h.includes('A149'));a(h.includes(lang==='en'?'No research records':'Todavía no hay registros'));}t.S.scan=originalScans;a(t.scannerNoticeArchive('2099-01-05')==='');console.log('PASS Today latest-only scanner notice, ES/EN future rollover, retained dated archives and no stale report link.');

// The summary card has three metrics; old documented-close records stay preserved.
for(const p of ps)for(const lang of ['es','en'])for(const inline of [true,false]){t.setLang(lang);const h=t.profileSummaryCard(p,inline);const metrics=h.match(/<dl class="stock-summary-values">([\s\S]*?)<\/dl>/)[1];a.equal((metrics.match(/<dt>/g)||[]).length,3);a(!metrics.includes('Último cierre documentado'));a(!metrics.includes('Latest documented close'));a(metrics.includes(lang==='en'?'Scanner price':'Precio del escáner'));a(metrics.includes(lang==='en'?'Estimated value':'Valor estimado'));a(metrics.includes(lang==='en'?'Bear–bull scenarios':'Escenarios bajista–alcista'));a(h.includes('profile-quote'));}
a.equal(fresh.close.price,25);a.equal(t.profileCardData(hp).close.price,44);
console.log('PASS three-metric summary layout in ES/EN, inline and direct cards; TradingView and historical close records preserved.');

// Zero is a valid valuation result, not absent data. Prices still must be positive.
const priorSourceSnapshot=JSON.stringify({dec:t.S.dec,lib:t.S.lib,scan:t.S.scan});
for(const tk of ['VFC','SSL']){
 const stock=by[tk];a(stock,'expected zero-residual fixture '+tk);const d=t.profileCardData(stock);a.equal(d.model.cons,0);a(d.model.fav>0);
 for(const language of ['es','en'])for(const inline of [true,false]){t.setLang(language);const h=t.profileSummaryCard(stock,inline),metrics=h.match(/<dl class="stock-summary-values">([\s\S]*?)<\/dl>/)[1];a(metrics.includes(language==='es'?'0,00':'0.00'));a(h.includes('stock-summary-band'));a(!/NaN|Infinity/.test(h));}
}
a.equal(JSON.stringify({dec:t.S.dec,lib:t.S.lib,scan:t.S.scan}),priorSourceSnapshot);
let zeroRow={ticker:'ZEROROW',adate:'2099-01-05',date:'2099-01-04',price:10,base:0,cons:0,fav:0,rep:'',vdate:'2099-01-05'};
let zeroProfile=e.build({decisions:[zeroRow]})[0];a.equal(t.profileCardData(zeroProfile).model.base,0);a.equal(t.profileCardData(zeroProfile).model.cons,0);a.equal(t.profileCardData(zeroProfile).model.fav,0);
for(const language of ['es','en']){t.setLang(language);const h=t.profileSummaryCard(zeroProfile);a(h.includes('stock-summary-band'));a(!/NaN|Infinity/.test(h));}
// A later explicit zero is not a withdrawal; a later null still withholds the model.
let positiveRow={...zeroRow,adate:'2099-01-03',vdate:'2099-01-03',base:20,cons:10,fav:30};a.equal(t.profileCardData(e.build({decisions:[positiveRow,zeroRow]})[0]).model.base,0);
a.equal(t.profileCardData(e.build({decisions:[positiveRow,{...zeroRow,base:null,cons:null,fav:null}]})[0]).model,null);
// Validate both Decisions and structured report pathways without coercing blank/false/string/negative/nonfinite input.
for(const bad of [null,undefined,'',false,'0',NaN,Infinity,-1]){
 const r={...zeroRow,ticker:'MISSINGROW',base:20,cons:bad,fav:30};const p=e.build({decisions:[r]})[0];a.equal(t.profileCardData(p).model.cons,null);
 for(const language of ['es','en']){t.setLang(language);const h=t.profileSummaryCard(p);a(h.includes('<dd class="">—</dd>'));a(!h.includes('stock-summary-band'));a(!/NaN|Infinity/.test(h));}
 a.equal(t.profileCardData(e.build({decisions:[{...r,base:bad}]})[0]).model,null);
}
for(const [i,bear] of [0,null,undefined,'',false,'0',NaN,Infinity,-1].entries()){
 const tk='ZEROF'+i,report={id:'ZEROFACT'+i,date:'2099-02-01',profiles:[{ticker:tk,kind:'complete',completedAt:'2099-02-01',valuation:{base:bear===0?0:20,bear:bear,bull:30,asOf:'2099-02-01'},close:{price:0,sessionDate:'2099-01-31',priceType:'regular-close'}}]};
 t.S.lib=t.S.lib.concat([report]);const p=t.profiles().find(x=>x.ticker===tk),d=t.profileCardData(p);a.equal(d.model.cons,bear===0?0:null);a.equal(d.model.base,bear===0?0:20);a.equal(d.close,null);
 const noPrice=e.build({scans:[{ticker:'ZEROPRICE'+i,date:'2099-01-31',price:bear}]})[0];a.equal(t.profileCardData(noPrice).scan,null);
}
console.log('PASS zero valuation scenarios in VFC/SSL and future row/report fixtures, all-zero range, zero-base update, absent/invalid withholding, positive-only prices, immutable research, ES/EN inline/direct cards.');

// Standalone fundamental updates may pair a verified stored scanner without changing decisions or management.
const beforeFundamental=JSON.stringify({dec:t.S.dec,ges:t.S.ges,ops:t.S.ops});
const fundFact={ticker:'FUNDFUTURE',kind:'complete',completedAt:'2099-03-01',valuation:{base:20,bear:10,bull:30,asOf:'2099-03-01'},scanner:{date:'2099-02-27',price:15,source:'published-scanner'}};
t.S.lib=t.S.lib.concat([{id:'FUNDFUTUREREPORT',date:'2099-03-01',profiles:[fundFact]}]);
t.S.scan=t.S.scan.concat([{ticker:'FUNDFUTURE',date:'2099-02-27',price:15},{ticker:'FUNDFUTURE',date:'2099-02-28',price:16}]);
const legacyFund={ticker:'FUNDFUTURE',adate:'2099-02-01',date:'2099-01-31',price:12,base:13,cons:10,fav:17,rep:'',vdate:'2099-02-01',decision:'En observación'};
let fp=e.build({scans:t.S.scan,decisions:[legacyFund],reports:t.S.lib}).find(p=>p.ticker==='FUNDFUTURE');
a.equal(t.profileCardData(fp).scan.price,15);a.equal(t.profileCardData(fp).scan.date,'2099-02-27');a.equal(t.profileCardData(fp).model.base,20);a.equal(fp.latestReview.price,12);a.equal(fp.latestReview.decision,'En observación');
for(const sc of [{date:'2099-02-27',price:99},{date:'2099-02-26',price:15},{date:'2099-02-27',price:0},null]){fundFact.scanner=sc;fp=e.build({scans:t.S.scan,decisions:[legacyFund],reports:t.S.lib}).find(p=>p.ticker==='FUNDFUTURE');a.equal(t.profileCardData(fp).scan.price,12);}
fundFact.scanner={date:'2099-02-27',price:0.0000001,source:'published-scanner'};
for(const bad of [null,undefined,'',false,true,'0.0000001',NaN,Infinity,-1,0,0.0000002]){fp=e.build({scans:t.S.scan,decisions:[legacyFund],reports:t.S.lib}).find(p=>p.ticker==='FUNDFUTURE');fp.scans=[{date:'2099-02-27',price:bad}];a.equal(t.profileCardData(fp).scan.price,12);}
a.equal(JSON.stringify({dec:t.S.dec,ges:t.S.ges,ops:t.S.ops}),beforeFundamental);
console.log('PASS optional standalone scanner metadata: exact stored date/price, rejected unknown/invalid pair, historical decision and management unchanged.');
