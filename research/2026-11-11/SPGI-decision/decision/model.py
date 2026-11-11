import json
from pathlib import Path
P=Path(__file__).parent
old=json.loads((P/'legacy.json').read_text())
price=473.38
# Cash-flow and claim preservation: reprice, not reconstruct underlying forecast.
def value(m,r,cost=0,shares=None):
 g=m['parameters']['g']; terminal=m['terminal_value']*(m['parameters']['wacc']-g)
 pv=sum((x['fcff']-cost)/(1+r)**x['year'] for x in m['rows'])
 tv=(terminal-cost*(1+g))/(r-g)/(1+r)**10
 return {'wacc':r,'enterprise_value':pv+tv,'net_claims':m['net_claims'],'price':(pv+tv-m['net_claims'])/(shares or m['shares']),'terminal_share':tv/(pv+tv)}
e=288.8*price;d=13062;ke=.0498+1.03*.0441;kd=.055;tax=.23
wacc=ke*e/(e+d)+kd*(1-tax)*d/(e+d)
base=old['models']['base'];lo=.030001;hi=.2
for _ in range(150):
 mid=(lo+hi)/2
 if value(base,mid)['price']>price:lo=mid
 else:hi=mid
out={'date':'2026-11-11','price':price,'priceDate':'2026-11-10 16:00 EST','rateInputs':{'riskFree':.0498,'ERP':.0441,'beta':1.03,'costDebtAssumed':kd,'tax':tax,'marketEquityProxy':e,'bookDebtProxy':d,'costEquity':ke,'wacc':wacc},'legacyTieouts':{k:value(m,m['parameters']['wacc']) for k,m in old['models'].items()},'rateScenarios':{k:value(base,r) for k,r in [('observedBeta',wacc),('7pct',.07),('8pct',.08),('9pct',.09),('10pct',.10)]},'cashDrag':{str(c):value(base,wacc,c) for c in [0,100,300,500]},'sharesSensitivity':value(base,wacc,shares=289.9),'priceImpliedWacc':(lo+hi)/2}
(P/'results.json').write_text(json.dumps(out,indent=2))
print(json.dumps(out,indent=2))
