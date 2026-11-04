import json,math
from pathlib import Path
from model import run,INPUT
P=Path(__file__).resolve().parent;m=json.loads((P/'results.json').read_text());checks=[]
def ck(label,a,b=None):
 ok=bool(a) if b is None else math.isclose(a,b,rel_tol=1e-9,abs_tol=1e-7);checks.append({'check':label,'pass':ok});assert ok,(label,a,b)
for n,x in m.items():
 s=x['assumptions'];c=INPUT['common'];prevrev=INPUT['revenueAnchor2026'];prevnop=prevrev*INPUT['normalizedMarginAnchor']*(1-c['cashTaxRate'])
 for r in x['rows']:
  tag=n+str(r['year']);ck(tag+'revenue',prevrev*(1+r['revenueGrowth']),r['revenue']);ck(tag+'nopat',r['ebitBeforeAcquiredAmortAfterSbc']-r['cashTax'],r['nopat']);ck(tag+'memo',r['gaapEbitMemo']+r['acquiredAmortMemo'],r['ebitBeforeAcquiredAmortAfterSbc']);ck(tag+'cash',r['nopat']+r['ppeDepreciation']-r['cashPpeCapexFloor']-r['netCommissionInvestment']-r['otherWcInvestment']-r['additionalGrowthInvestment'],r['fcff']);ck(tag+'growthfunding',max(r['nopat']-prevnop,0)/s['roic'],r['growthInvestmentFloor']);ck(tag+'funded',r['netReinvestment']>=r['growthInvestmentFloor']-1e-7);ck(tag+'noSbcAddback',r['marginBeforeSbcMemo']-r['sbcEconomicCostMemo']/r['revenue'],r['marginBeforeNewLeadership']);ck(tag+'pv',r['fcff']/(1+s['wacc'])**r['discountYears'],r['pv']);prevrev=r['revenue'];prevnop=r['nopat']
 ck(n+'years',len(x['rows'])==10);ck(n+'PV',sum(r['pv'] for r in x['rows'])+x['terminalPv']+x['stubPv'],x['enterpriseValue']);ck(n+'equity',x['enterpriseValue']+x['capitalBridge'],x['equityValue']);ck(n+'perShare',x['equityValue']/x['sharesMillions'],x['valuePerShare']);ck(n+'terminal',x['terminalNopat']-x['terminalReinvestment'],x['terminalFcff']);ck(n+'terminalfunded',x['terminalReinvestment']>=x['terminalNopat']*s['g']/s['roic']-1e-7);ck(n+'rate',s['wacc']>s['g']);ck(n+'noInventedAmortShield',run(n,{'common.acquiredAmortMemo':[0]*10})['valuePerShare'],x['valuePerShare'])
ck('ordered',m['bear']['valuePerShare']<m['base']['valuePerShare']<m['bull']['valuePerShare'])
ck('leadershipCost',sum(r['newLeadershipCost'] for r in m['base']['rows']),126.55)
ck('cashDebt',2393+2214+2354+2050*.5-7600-1500-197-34,m['base']['capitalBridge'])
(P/'valuation_checks.json').write_text(json.dumps({'passed':len(checks),'failed':0,'checks':checks},indent=2)+'\n');print(len(checks),'checks PASS')
