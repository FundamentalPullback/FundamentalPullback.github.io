// Authorized minimized November 5 PAPER execution projection. Offline/read-only.
const fs=require('fs'),path=require('path'),assert=require('assert/strict'),vm=require('vm'),Module=require('module'),crypto=require('crypto');
const root=path.resolve(__dirname,'..'),sha=s=>crypto.createHash('sha256').update(s).digest('hex'),clone=x=>JSON.parse(JSON.stringify(x));
const c={window:{FP:{}}};c.FP=c.window.FP;vm.createContext(c);
for(const key of ['ops','ges'])vm.runInContext(fs.readFileSync(root+'/data/'+key+'.js','utf8'),c);
const ops=clone(c.FP.ops),ges=clone(c.FP.ges),operation=["2026-11-05", "HRB", "", "Venta", "18", "55,29", "", "", "", "Venta parcial PAPER registrada; quedan 36 acciones. Reconciliación A247; no repetir.", "Comisión no publicada. / Fee not published.", ""],management=["HRB", "2026-11-05", "A247", "Parcial ejecutada; 36 acciones; sin ampliar", "Partial filled; 36 shares; no add-on", "45,8", "Activación confirmada; nivel pendiente", "47,33", "Parcial PAPER registrada: 18 acciones vendidas a 55,29 USD; quedan 36. Reconciliación de A247; no repetir la parcial. Revisión previa histórica, no nueva aprobación. Ampliación suspendida.", "PAPER partial recorded: 18 shares sold at $55.29; 36 remain. Reconciles A247; do not repeat the partial. The prior review is historical, not a new approval. Add-on suspended.", "Resultados 9 nov tras cierre; conferencia 16:30 EST. Investor Day 3 dic 08:30 EST.", "Results Nov 9 after close; call 16:30 EST. Investor Day Dec 3 08:30 EST."];
assert.equal(ops.length,26);assert.equal(ges.length,67);
assert.equal(sha(JSON.stringify(ops.slice(0,25))),'20729a2578b1495b1c864ffee7f181abc240f2062a9af8980636cf06f4ae6785','every previous operation preserved');
assert.equal(sha(JSON.stringify(ges.slice(0,66))),'982e7d4e3e9a4fc043df7b80cdf91ac981929b61f4003fa6c0c9dc2dc08a3ae4','every previous management row preserved');
assert.deepEqual(ops[25],operation,'exact minimized public operation');assert.deepEqual(ges[66],management,'exact minimized public management');
assert.equal(ops.filter(r=>r[1]==='HRB'&&/^(venta|sell)$/i.test(r[3])).length,1,'one HRB partial');assert.equal(ges.filter(r=>r[0]==='HRB'&&r[1]==='2026-11-05'&&r[2]==='A247').length,1);
assert.equal(operation[0],'2026-11-05');assert.equal(operation[4],'18');assert.equal(operation[5],'55,29');assert.equal(operation[6],'');assert.equal(operation[11],'');
assert(operation[10].includes('Comisión no publicada'));assert(operation[10].includes('Fee not published'));
const priorManagement=ges.slice(0,66).filter(r=>r[0]==='HRB').at(-1);assert.deepEqual(management.slice(5,8),priorManagement.slice(5,8));assert.deepEqual(management.slice(10),priorManagement.slice(10));
const newExecutionText=JSON.stringify([operation,management.slice(0,5),management.slice(8,10)]);
assert(!/(?:\d{2}:\d{2}|https?:|data:image|account[_ -]?id|cuenta\s*[:#]|DU\d{5,}|U\d{5,}|captura|screenshot|bruto|gross|neto|net proceeds|coste|cost basis|cash|saldo)/i.test(newExecutionText),'no unauthorized execution detail in the public projection');
for(const key of ['ops','ges'])vm.runInContext(fs.readFileSync(root+'/data/'+key+'.js','utf8'),c);assert.deepEqual(clone(c.FP.ops),ops);assert.deepEqual(clone(c.FP.ges),ges);
const filename=path.join(__dirname,'load-stock-profiles.cjs'),m=new Module(filename,module);m.filename=filename;m.paths=module.paths;
m._compile(fs.readFileSync(filename,'utf8').replace('profileRoute,renderProfile,','profileRoute,renderProfile,vPosiciones,vOperaciones,vInicio,vCartera,calPanel,positions,acctCalc,equitySeries,calSeries,livePanel,'),filename);
const a=m.exports(root),t=a.t,currentOps=t.S.ops,currentGes=t.S.ges,originalHist=t.S.hist;
t.S.ops=t.PARTS.ops(ops.slice(0,25));const before=clone(t.positions()),oldEq=clone(t.equitySeries(null)),oldCal=clone(t.calSeries());t.S.ops=currentOps;const after=clone(t.positions());
const oldHrb=before.list.find(p=>p.ticker==='HRB'),newHrb=after.list.find(p=>p.ticker==='HRB');
assert.equal(newHrb.shares,36);assert.equal(oldHrb.shares-newHrb.shares,18);assert.equal(newHrb.avg,oldHrb.avg,'preserved previously public cost basis');
assert.deepEqual(after.list.filter(p=>p.ticker!=='HRB'),before.list.filter(p=>p.ticker!=='HRB'));
assert.equal(after.sales.length,before.sales.length+1);assert.equal(after.sales.filter(r=>r.ticker==='HRB').length,1);assert.equal(newHrb.realized,null);assert.equal(after.sales.at(-1).pnl,null);assert.equal(after.sales.at(-1).ret,null);assert.equal(after.fees,null);assert.equal(after.incompleteFees,true);assert.equal(currentOps.at(-1).fee,null);assert.deepEqual(after.warn,before.warn);
assert.deepEqual(clone(t.equitySeries(null)),oldEq.filter(r=>r.d<operation[0]));assert.deepEqual(clone(t.calSeries()),oldCal.filter(r=>r.d<operation[0]));
// Future prices cannot turn an unpublished fee into an exact net/account result.
t.S.hist=clone(originalHist);for(const prices of Object.values(t.S.hist)){const ds=Object.keys(prices).sort();if(ds.length)for(const day of ['2026-11-05','2026-11-06'])prices[day]=prices[ds.at(-1)];}
assert(t.equitySeries(1).every(r=>r.d<operation[0]));assert(t.calSeries().every(r=>r.d<operation[0]));t.S.hist=originalHist;
const X=t.acctCalc();for(const key of ['cash','total','realized','totPL','ret','excess','day','dayPct'])assert.equal(X[key],null,'unavailable affected aggregate '+key);assert.equal(t.livePanel(X.open,X.cash),'');
const hrbProfile=a.profiles.find(p=>p.ticker==='HRB');assert.equal(hrbProfile.latestManagement.date,'2026-11-05');assert.equal(hrbProfile.latestManagement.rep,'A247');
const immutable=JSON.stringify({ops:t.S.ops,ges:t.S.ges,acct:t.S.acct,hist:t.S.hist});
for(const lang of ['es','en']){
 t.setLang(lang);const html=t.vPosiciones(),banner=html.match(/<section class="panel">[\s\S]*?<\/section>/)[0];
 assert(banner.includes(lang==='es'?'venta parcial PAPER registrada de 18 acciones; quedan 36 acciones':'recorded PAPER partial sale of 18 shares; 36 shares remain'));assert(banner.includes(lang==='es'?'No repetir la parcial de campaña':'Do not repeat the campaign partial'));assert(!banner.includes(lang==='es'?'señal pendiente de parcial':'pending 18-share partial'));
 assert(html.includes(lang==='es'?'Activación confirmada; nivel pendiente':'Activation confirmed; level pending'));assert(html.includes(lang==='es'?'Parcial ejecutada; 36 acciones; sin ampliar':'Partial filled; 36 shares; no add-on'));
 const card=t.renderProfile(hrbProfile);assert(card.includes(lang==='es'?'5 nov 2026':'Nov 5, 2026'));assert(card.includes(lang==='es'?'Resultados 9 nov':'Results Nov 9'));
 for(const render of [t.vOperaciones,t.vInicio,t.vCartera,t.calPanel]){const out=render();assert(out.includes(lang==='es'?'Contabilidad pública incompleta':'Incomplete public accounting'));assert(out.includes(lang==='es'?'Comisión no publicada':'Fee not published'));assert(!out.includes('NaN'));}
 assert(t.vInicio().includes(lang==='es'?'Totales netos actuales no disponibles':'Current net totals unavailable'));
 const portfolio=t.vCartera();assert(!portfolio.includes('<div class="alloc">'),'no apparent account allocation without known cash');
 assert.equal(t.vPosiciones(),html);
}
assert.equal(JSON.stringify({ops:t.S.ops,ges:t.S.ges,acct:t.S.acct,hist:t.S.hist}),immutable);
t.S.ops=clone(currentOps);t.S.ops.at(-1).shares=9;t.setLang('en');assert(t.vPosiciones().includes('recorded PAPER partial sale of 9 shares; 45 shares remain'));t.S.ops=currentOps;t.S.ges=currentGes;
console.log('PASS minimized public HRB partial: 18 at $55.29, 36 remain; exact historical prefixes, no private execution detail, no zero-fee inference, affected net/cash totals unavailable, prior history unchanged, ES/EN notices and idempotence.');
