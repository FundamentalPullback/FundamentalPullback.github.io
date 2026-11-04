from pathlib import Path
from decimal import Decimal,ROUND_HALF_UP
import json
P=Path(__file__).parent;f=json.loads((P/'facts.json').read_text());tests=[]
def ratio(v):
 if v<=f['collarLow']:return f['ratioBelow']
 if v>=f['collarHigh']:return f['ratioAbove']
 return float((Decimal(str(f['cashPerShare']))/Decimal(str(v))).quantize(Decimal('.0001'),rounding=ROUND_HALF_UP))
def payment(v,spot):return f['cashPerShare']+ratio(v)*spot
rows=[]
for v in [30,40,45,54.43,60,67.5,75,90,112.5,130]:
 for change in [-.2,0,.2]:
  spot=v*(1+change);rows.append({'vwap':v,'spotAtClosing':spot,'ratio':ratio(v),'conditionalGrossConsideration':payment(v,spot),'notCurrentFairValue':True})
for v,expected in [(67.5,.4),(112.5,.24),(90,.3),(30,.4),(150,.24)]:assert ratio(v)==expected;tests.append('ratio '+str(v))
assert payment(90,75)==49.5;tests.append('spot distinct from VWAP')
proxy=payment(f['rklbClose'],f['rklbClose'])
res={'samePriceIllustrationAtNov3':proxy,'absoluteSpreadNotGuaranteed':proxy-f['irdmClose'],'grossPercentageNotAnnualReturn':proxy/f['irdmClose']-1,'sameVWAPSpotBreakEvenLowBranch':(f['irdmClose']-27)/.4,'matrix':rows,'discountedIllustrations':[],'totalCurrentFairValue':None}
for years in [.5,.75,1,1.25]:
 for rate in [.08,.12,.18]:res['discountedIllustrations'].append({'yearsHypothetical':years,'discountSelected':rate,'conditionalPaymentPV':proxy/(1+rate)**years,'excludesDividendsTaxFailureRisk':True})
(P/'results.json').write_text(json.dumps(res,indent=2)+'\n');(P/'checks.json').write_text(json.dumps({'passed':len(tests),'tests':tests},indent=2)+'\n');print('PASS',len(tests),'illustration',proxy)
