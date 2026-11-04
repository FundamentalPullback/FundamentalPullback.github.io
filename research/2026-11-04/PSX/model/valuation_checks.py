import json,math
from pathlib import Path
P=Path(__file__).resolve().parent
m=json.loads((P/'results.json').read_text());i=json.loads((P/'inputs.json').read_text());checks=[]
def ck(label,a,b=None):
 ok=bool(a) if b is None else math.isclose(a,b,rel_tol=1e-9,abs_tol=1e-7)
 checks.append({'check':label,'pass':ok});assert ok,(label,a,b)
for name,x in m.items():
 s=x['assumptions'];rows=x['rows'];prev=None
 for r in rows:
  y=r['year'];seg=[r[k] for k in ['refiningEbit','midstreamEbit','marketingEbit','renewableEbit','corporateEbit']]
  ck(f'{name}{y}ebit',sum(seg),r['operatingEbitExJv']);ck(f'{name}{y}fcff',r['nopat']+r['da']-r['capex']-r['workingCapitalInvestment'],r['fcff'])
  ck(f'{name}{y}jvcash',r['jvEquityIncome']-r['jvIncrementalParentTax']-r['jvRetainedCapital'],r['jvEquityCashFlow'])
  ck(f'{name}{y}replacement',r['capex']>=1.25*r['da']-1e-6)
  ck(f'{name}{y}pv',r['fcff']/(1+s['wacc'])**r['discountYears'],r['fcffPv'])
  ck(f'{name}{y}jvpv',r['jvEquityCashFlow']/(1+s['jvKe'])**r['discountYears'],r['jvPv'])
  ck(f'{name}{y}growthfunded',r['netReinvestment']>=r['growthInvestmentFloor']-1e-6)
  if prev:
   after=lambda a:a*.76 if a>=0 else a
   growth=sum(max(after(a)-after(b),0) for a,b in zip(seg,prev)) /s['roic']
   ck(f'{name}{y}segmentgrowth',growth,r['growthInvestmentFloor'])
  prev=seg
 ck(name+'tenyears',len(rows)==10)
 ck(name+'operatingvalue',sum(r['fcffPv'] for r in rows)+x['operatingTerminalPv']+x['operatingStubPv'],x['operationsValue'])
 ck(name+'jvvalue',sum(r['jvPv'] for r in rows)+x['jvTerminalPv']+x['jvStubPv'],x['jvEquityValue'])
 ck(name+'bridge',x['operationsValue']+x['jvEquityValue']+x['capitalBridge'],x['equityValue'])
 ck(name+'shares',x['equityValue']/x['sharesMillions'],x['valuePerShare'])
 ck(name+'terminalcash',x['terminalOperatingNopat']-x['terminalOperatingReinvestment'],x['terminalOperatingFcff'])
 ck(name+'fundedterminal',x['terminalOperatingReinvestment']>=x['terminalOperatingNopat']*s['g']/s['roic']-1e-6)
 ck(name+'jvterminal',x['terminalJvAfterParentTax']-x['terminalJvReinvestment'],x['terminalJvCash'])
 ck(name+'waccg',s['wacc']>s['g'] and s['jvKe']>s['g'])
 ck(name+'calendar',rows[0]['discountYears'],423/365)
ck('ordered',m['bear']['valuePerShare']<m['base']['valuePerShare']<m['bull']['valuePerShare'])
from model import run
for floor in [3000,4000,5000]:
 a=run(changes={'common.capitalSpendingFloor2027':floor});last=a['rows'][-1];g=a['assumptions']['g']; wc=last['revenueProxy']*g*i['common']['workingCapitalIncrementalRevenueFraction'];terminal_capex=a['terminalOperatingReinvestment']+last['da']*(1+g)-wc
 ck('stressTerminalCapexFloor'+str(floor),terminal_capex>=floor*1.02**9*(1+g)-1e-6)
(P/'valuation_checks.json').write_text(json.dumps({'passed':len(checks),'failed':0,'checks':checks},indent=2)+'\n');print(len(checks),'valuation checks PASS')
