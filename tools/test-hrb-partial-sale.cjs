// Authorized accounting reconciliation; retains unknown-fee safety regression.
const fs=require('fs'),path=require('path'),assert=require('assert/strict'),Module=require('module'),crypto=require('crypto');
const root=path.resolve(__dirname,'..'),clone=x=>JSON.parse(JSON.stringify(x));
const filename=path.join(__dirname,'load-stock-profiles.cjs'),m=new Module(filename,module);m.filename=filename;m.paths=module.paths;
m._compile(fs.readFileSync(filename,'utf8').replace('profileRoute,renderProfile,','profileRoute,renderProfile,vPosiciones,vOperaciones,vInicio,vCartera,calPanel,positions,acctCalc,equitySeries,calSeries,livePanel,'),filename);
const a=m.exports(root),t=a.t,ops=clone(a.c.FP.ops),sha=s=>crypto.createHash('sha256').update(s).digest('hex');
assert.equal(ops.length,27);assert.equal(sha(JSON.stringify(ops.slice(0,25))),'20729a2578b1495b1c864ffee7f181abc240f2062a9af8980636cf06f4ae6785','all previous operations preserved');
assert.equal(t.S.ops.filter(x=>x.ticker==='CTSH').length,1);const c=t.S.ops.find(x=>x.ticker==='CTSH');assert.equal(c.shares,41);assert.equal(c.exec,66.69);assert.equal(c.fee,0);assert.match(c.notes,/estimated/i);
const hrb=t.S.ops.filter(x=>x.ticker==='HRB'&&x.type==='Venta');assert.equal(hrb.length,1);assert.equal(hrb[0].shares,18);assert.equal(hrb[0].fee,.04);assert.match(hrb[0].notes,/estimada/);
assert(!JSON.stringify(ops.slice(25)).match(/DEV\w+|account[_ -]?id|data:image|libfile_|Sentinel_|\d{2}:\d{2}:\d{2}/));
const p=t.positions();assert.equal(p.list.filter(x=>x.shares>1e-6).length,7);assert.equal(p.list.find(x=>x.ticker==='HRB').shares,36);assert.equal(p.list.find(x=>x.ticker==='CTSH').shares,41);assert(!p.incompleteFees);
const archived=JSON.parse(fs.readFileSync(root+'/tools/accounting-prior.json'));const vm=require('vm'),cc={window:{FP:{}}};cc.FP=cc.window.FP;vm.createContext(cc);vm.runInContext(archived['data/hist.js'],cc);const oldHist=t.PARTS.hist(cc.FP.hist);for(const [tk,ds] of Object.entries(oldHist))for(const [d,p] of Object.entries(ds))assert.equal(t.S.hist[tk][d],p,'historical prefix unchanged');
const X=t.acctCalc();for(const key of ['cash','total','realized','totPL','ret','day','dayPct'])assert(Number.isFinite(X[key]),key);assert(t.S.snapshot>='2026-11-06');assert.equal(t.S.hist.CTSH['2026-11-05'],66.54);assert.equal(t.S.hist.CTSH['2026-11-06'],64.72);assert.equal(t.S.hist.ANF['2026-11-06'],149.54);assert.equal(t.S.hist.EXLS['2026-11-06'],43.15);
assert.equal(t.equitySeries(null).at(-1).d,t.S.snapshot);assert(Math.abs(t.equitySeries(null).at(-1).v-X.total)<.000001);
for(const lang of ['es','en']){t.setLang(lang);for(const render of [t.vInicio,t.vCartera,t.vOperaciones,t.calPanel]){const h=render();assert(h.includes(lang==='es'?'Contabilidad PAPER provisional':'Provisional PAPER accounting'));assert(!h.includes('NaN'));}const h=t.vInicio();assert(h.includes(lang==='es'?'Posiciones abiertas registradas':'Recorded open positions'));assert(h.includes(lang==='es'?'no una actualización diaria automática':'not an automatic daily feed'));}
// Unknown fee still blanks net/account totals and excludes affected historical dates.
const old=hrb[0].notes;hrb[0].fee=null;hrb[0].notes='Comisión no publicada. / Fee not published.';
assert(t.positions().incompleteFees);for(const key of ['cash','total','realized','totPL','ret','day','dayPct'])assert.equal(t.acctCalc()[key],null,key);assert(t.equitySeries(null).every(x=>x.d<'2026-11-05'));hrb[0].fee=.04;hrb[0].notes=old;
// A missing held-symbol close must never become the fill or previous close.
const d=t.S.snapshot,close=t.S.hist.CTSH[d];delete t.S.hist.CTSH[d];assert(t.equitySeries(null).at(-1).d<d);t.S.hist.CTSH[d]=close;
console.log('PASS authorized PAPER ledger, 7 positions, provisional totals, complete Nov6 history, estimated and unknown fee safety, missing-close guard, ES/EN disclosure, no identifiers.');console.log(JSON.stringify({cash:X.cash,total:X.total,realized:X.realized,day:X.day,open:X.open.map(x=>({ticker:x.ticker,shares:x.shares,price:x.price,value:x.value}))}));
