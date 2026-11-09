const fs=require('fs'),vm=require('vm'),assert=require('assert/strict');
const root=require('path').resolve(__dirname,'..'),c={window:{}};c.FP=c.window.FP={};vm.createContext(c);
for(const f of ['data/manifest.js','data/ops.js','data/acct.js','data/hist.js'])vm.runInContext(fs.readFileSync(root+'/'+f,'utf8'),c);
const html=fs.readFileSync(root+'/index.html','utf8');let app=[...html.matchAll(/<script[^>]*>([\s\S]*?)<\/script>/g)].map(x=>x[1]).find(x=>x.includes('var DEC_MAP'));
app=app.slice(0,app.indexOf('  var hash ='))+app.slice(app.indexOf('  var PARTS ='),app.indexOf('  var DENY ='))+'\nwindow.TEST={S,PARTS,positions,acctCalc,equitySeries,currentDayPL,accountQuotes,vInicio,vCartera,vOperaciones,vPosiciones,livePanel,priceStatus,calPanel,setLang:function(l){lang=l;}};render=function(){};})();';
const noop=()=>{},el={addEventListener:noop,setAttribute:noop,querySelectorAll:()=>[],style:{}};
Object.assign(c,{document:{getElementById:()=>el,addEventListener:noop,querySelectorAll:()=>[],querySelector:()=>el,hidden:false},localStorage:{getItem:()=>null},console,Date,Intl,setTimeout,clearTimeout,AbortController,location:{hash:'#cartera'},URL,URLSearchParams});c.window.addEventListener=noop;vm.runInContext(app,c);
const t=c.window.TEST,F=c.FP;for(const k of ['ops','acct','hist'])t.S[k]=t.PARTS[k](F[k]);t.S.scan=[];t.S.dec=[];t.S.ges=[];t.S.lib=[];t.S.libState='ok';t.S.snapshot=c.window.FP_MANIFEST.asOf;
const near=(a,b)=>assert(Math.abs(a-b)<1e-7,`${a} !== ${b}`);
assert.equal(require('crypto').createHash('sha256').update(JSON.stringify(F.ops.slice(0,27))).digest('hex'),'cc6dc5fc6ab15f0d5e26cb71e2c414f96746aa550deef256a11df732502e0c05','All 26 prior operations preserved');
assert.equal(F.ops.length,29);assert.equal(t.S.ops.filter(x=>x.date.startsWith('2026-11-09')).length,2);assert.equal(t.S.ops.filter(x=>x.ticker==='HRB'&&x.type==='Venta').length,2);
const newRows=JSON.stringify(F.ops.slice(27));assert(!/DEV\w+|account[_ -]?id|Sentinel_|libfile_|data:image/.test(newRows));
let P=t.positions();assert.equal(P.list.filter(x=>x.shares>0).length,5);assert.equal(P.list.find(x=>x.ticker==='HRB').shares,0);assert.equal(P.list.find(x=>x.ticker==='ANF').shares,0);assert.equal(P.warn.length,0);
let X=t.acctCalc();near(X.cash,68115.621075);near(X.realized,2392.500455);near(P.sales.find(x=>x.date==='2026-11-09 09:31:32').pnl,485.958625);near(P.sales.find(x=>x.date==='2026-11-09 12:35:29').pnl,145.03);assert.equal(X.day,null);assert.equal(X.dayPct,null);
const originalOps=t.S.ops;const history=JSON.stringify(t.equitySeries(null));t.S.ops=t.S.ops.filter(x=>x.date<'2026-11-09');assert.equal(JSON.stringify(t.equitySeries(null)),history);t.S.ops=originalOps;assert.equal(X.eq.at(-1).d,'2026-11-06');
// Feed fixture with all open positions unchanged from Nov6; only sale execution contribution remains.
const prices={SPY:{p:735.29,prev:735.29}};for(const p of P.list){const q=t.S.acct.prices[p.ticker];if(q)prices[p.ticker]={p:q.p,prev:q.p};}
t.S.live={prices,at:Date.parse('2026-11-09T18:00:00Z'),readAt:Date.parse('2026-11-09T18:00:00Z')};X=t.acctCalc();const expected=30.8615*(152.03-149.54)-.11+36*(52.44-52.69)-.05;near(X.day,expected);near(X.day,67.685135);near(X.total-X.day,X.eq.at(-1).v);near(X.dayBase,X.eq.at(-1).v);assert.equal(JSON.stringify(X.eq),history);
for(const lang of ['en','es']){t.setLang(lang);for(const render of [t.vInicio,t.vCartera,t.vOperaciones,t.vPosiciones]){const h=render();assert(!h.includes('NaN'));assert(!h.includes('undefined'));}assert(t.vOperaciones().includes('152'));assert(t.priceStatus().includes(lang==='en'?'Recorded trades through':'Operaciones registradas hasta'));}
// Missing a sold ticker prior-close must not fabricate day P&L.
const saved=prices.ANF;delete prices.ANF;assert.equal(t.acctCalc().day,null);assert.equal(t.acctCalc().dayPct,null);prices.ANF=saved;
// Old quote date cannot be applied to newer trades.
t.S.live.at=Date.parse('2026-11-06T22:00:00Z');assert.equal(t.acctCalc().day,null);t.S.live.at=Date.parse('2026-11-09T18:00:00Z');
// Buy and same-day partial: benchmark exposure is beginning holdings, not ending inventory.
t.S.ops.push({date:'2026-11-09 13:00:00',ticker:'ASO',shares:2,exec:66,fee:.2,type:'Compra',notes:''});near(t.acctCalc().day,expected+2*(67.28-66)-.2);t.S.ops.pop();
// Unknown fee keeps all net totals unavailable.
const sale=t.S.ops.at(-1),fee=sale.fee,notes=sale.notes;sale.fee=null;sale.notes='Fee not published.';assert.equal(t.acctCalc().cash,null);assert.equal(t.acctCalc().day,null);sale.fee=fee;sale.notes=notes;
for(const s of [...html.matchAll(/<script[^>]*>([\s\S]*?)<\/script>/g)].map(x=>x[1]).filter(Boolean))new vm.Script(s);
console.log('PASS: two unique full exits, prior ledger preserved, five holdings, exact cash/P&L, no identifiers, current/stale/missing-prior-close/buy/unknown-fee cases, history unchanged, ES/EN views, inline syntax.');console.log(JSON.stringify({cash:X.cash,realized:X.realized,dayFixture:X.day,historyLast:X.eq.at(-1),open:X.open.map(p=>({ticker:p.ticker,shares:p.shares}))}));
