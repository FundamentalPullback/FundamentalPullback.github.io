// Current published inputs must remain complete and append-only, independently
// of the dated accounting fixtures used by the execution regression tests.
const fs=require('fs'),path=require('path'),assert=require('assert/strict'),Module=require('module'),crypto=require('crypto');
const root=path.resolve(__dirname,'..'),filename=path.join(__dirname,'load-stock-profiles.cjs'),m=new Module(filename,module);m.filename=filename;m.paths=module.paths;
m._compile(fs.readFileSync(filename,'utf8').replace('profileRoute,renderProfile,','profileRoute,renderProfile,positions,acctCalc,equitySeries,'),filename);
const {t,c}=m.exports(root),contract=require('./reviewed-ledger-contract.json'),sha=s=>crypto.createHash('sha256').update(s).digest('hex');
assert.equal(c.FP.ops.length,contract.opsRowsIncludingHeader);
assert.equal(sha(JSON.stringify(c.FP.ops)),contract.opsSha256,'Current public ledger unchanged');
const old=t.PARTS.hist(require('./load-accounting-nov6-fixture.cjs')().hist);
for(const [ticker,dates] of Object.entries(old))for(const [date,price] of Object.entries(dates))assert.equal(t.S.hist[ticker][date],price,`${ticker} ${date}: historical price is immutable`);
const latest=Object.keys(t.S.hist.SPY).sort().at(-1);assert.equal(latest,t.S.snapshot,'Manifest matches saved SPY history');
assert(t.S.snapshot>='2026-11-06');
assert.equal(t.S.acct.spy,t.S.hist.SPY[t.S.snapshot],'Saved SPY account quote matches snapshot');
for(const [ticker,q] of Object.entries(t.S.acct.prices)){
 assert.equal(q.p,t.S.hist[ticker]?.[t.S.snapshot],ticker+' saved account quote matches dated history');
}
// Check every appended session, not just the final point. A missing intermediate
// held-symbol close must not silently disappear from the equity curve.
for(const date of Object.keys(t.S.hist.SPY).filter(d=>d>'2026-11-06').sort()){
 const held={};for(const op of t.S.ops)if(op.date.slice(0,10)<=date)held[op.ticker]=(held[op.ticker]||0)+op.shares*(op.type==='Venta'?-1:1);
 for(const [ticker,qty] of Object.entries(held))if(qty>1e-6)assert(Number.isFinite(t.S.hist[ticker]?.[date])&&t.S.hist[ticker][date]>0,`${ticker} ${date}: every appended session requires its own close`);
}
const eq=t.equitySeries(null);assert.equal(eq.at(-1).d,t.S.snapshot,'Latest historical session has complete held-symbol coverage');
const tradeDate=t.S.ops.map(x=>x.date.slice(0,10)).sort().at(-1);
if(t.S.snapshot>=tradeDate){
 const X=t.acctCalc();for(const k of ['cash','total','realized','totPL','ret'])assert(Number.isFinite(X[k]),k);
 assert(Math.abs(eq.at(-1).v-X.total)<1e-7,'Saved equity agrees with account total');
 assert.equal(t.S.acct.spy,t.S.hist.SPY[t.S.snapshot]);
 for(const p of X.open){assert(Number.isFinite(t.S.hist[p.ticker][t.S.snapshot]));assert.equal(p.price,t.S.hist[p.ticker][t.S.snapshot]);}
 // Missing any currently held close must truncate history, never use fill or last.
 for(const p of X.open){const h=t.S.hist[p.ticker],v=h[t.S.snapshot];delete h[t.S.snapshot];assert(t.equitySeries(null).at(-1).d<t.S.snapshot,p.ticker+' missing-close guard');h[t.S.snapshot]=v;}
}
console.log('PASS current ledger hash, immutable prior daily history, manifest/equity dates and current held-symbol price completeness.');
