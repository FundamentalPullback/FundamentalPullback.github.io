from pathlib import Path
import json,math,sys
from model import I,C,value,capital
P=Path(__file__).parent;R=json.loads((P/'results.json').read_text());tests=[]
def check(name,condition):
 tests.append({'name':name,'pass':bool(condition)});assert condition,name
for case,d in R.items():
 v=value(case);check(case+' frozen value',abs(v['perShareConditional']-d['perShareConditional'])<1e-10)
 for n,r in enumerate(d['rows']):
  check(f'{case} year{n+1} cash identity',abs(r['gaapEbitIllustrative']-r['cashTax']+r['totalDa']-r['fundedTotalCapexEquivalent']-r['workingCapitalInvestment']-r['additionalCapitalizedSbcCost']-r['fcff'])<1e-7)
  check(f'{case} year{n+1} physical funding',r['fundedTotalCapexEquivalent']>=r['physicalCapexFloor']-1e-8)
  check(f'{case} year{n+1} economic funding',r['selectedNetInvestment']>=r['economicNetInvestmentFloor']-1e-8)
  check(f'{case} year{n+1} positive tax',r['cashTax']>=0)
  check(f'{case} year{n+1} discount',abs(r['pv']-r['fcff']/(1+d['assumptions']['discount'])**(n+1))<1e-8)
 t=d['terminal'];check(case+' terminal physical',t['netInvestment']>=t['physicalNetFloor']-1e-8);check(case+' terminal economic',t['netInvestment']>=t['economicNetFloor']-1e-8)
 check(case+' terminal cash',abs(t['fcff']-(t['nopat']-t['netInvestment']-t['additionalCapitalizedSbcCost']))<1e-8)
 check(case+' no amort tax shield',abs(value(case,{'acquiredAmortAnnual':0})['perShareConditional']-d['perShareConditional'])<1e-9)
 check(case+' bridge',abs(d['equityValueConditional']-(d['enterpriseValue']+capital()['netBridge']))<1e-8)
 for extra in [.01,.025]:
  u=value(case,{'extraCapexRatio':extra});q=u['terminal'];check(f'{case} recurrent floor{extra}',q['netInvestment']>=q['capexFloor']-q['physicalSoftwareDa']+q['workingCapitalInvestment']-1e-8)
check('scenarios order',R['bear']['perShareConditional']<R['base']['perShareConditional']<R['bull']['perShareConditional'])
for k in ['marginShift','growthShift']:
 v=json.loads((P/'inverse.json').read_text())[k];check(k+' monotonic grid',v['monotone'])
 if v['solution'] is not None:
  overrides={'marginShift':v['solution']} if k=='marginShift' else {'growth':[g+v['solution'] for g in I['scenarios']['base']['growth']]}
  check(k+' inverse price',abs(value(overrides=overrides)['perShareConditional']-I['price'])<1e-6)
check('normalization anchor',abs(I['anchorEbit']-13142.948)<1e-8)
(P/'checks.json').write_text(json.dumps({'passed':len(tests),'checks':tests},indent=2)+'\n');print(len(tests),'valuation checks PASS')
