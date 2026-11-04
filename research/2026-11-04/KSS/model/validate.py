from model import inputs,calc
from pathlib import Path
import json,math,copy
p=Path(__file__).resolve().parent;checks=[]
def check(v,label):
 assert v,label
 checks.append(label)
for name in inputs['cases']:
 r=calc(name);c=inputs['cases'][name]
 for a in r['rows']:
  check(abs(a['fcff']-(a['nopat']-a['reinvestment']))<1e-8,name+' FCFF '+str(a['year']))
  check(a['reinvestment']+1e-8>=a['positiveNopatGrowthCapital'],name+' growth financing')
  check(a['reinvestment']+1e-8>=a['netPhysicalReinvestmentFloor'],name+' physical floor')
  check(a['reinvestment']>=0,name+' no invented release')
  check(abs(a['fcff']-(a['nopat']+a['residualDda']-a['impliedGrossCapex']-a['incrementalWc']-a['otherInvestingStress']))<1e-8,name+' gross capex identity')
  check(a['impliedGrossCapex']+1e-8>=a['physicalCapexFloor'],name+' gross maintenance funded')
 t=r['terminal'];check(t['reinvestment']>=t['economicReinvestment']-1e-8,name+' terminal economic floor');check(t['reinvestment']>=t['physicalReinvestmentFloor']-1e-8,name+' terminal physical floor')
 check(abs(r['operatingEvAfterFullRent']-sum(a['pv'] for a in r['rows'])-t['pv'])<1e-7,name+' PV bridge')
 check(r['fairValueTotal'] is None,name+' total null')
 x=copy.deepcopy(inputs);x['capital']['financeAndFinancingLiabilitiesNotDeductedAgain']=0;x['capital']['operatingLeaseLiabilitiesNotDeductedAgain']=0
 check(abs(calc(name,x)['equityResidual']-r['equityResidual'])<1e-8,name+' no double lease liability')
for floor in [.75,1,1.25]:
 x=copy.deepcopy(inputs);x['physicalCapexToResidualDdaFloor']=floor
 for name in inputs['cases']:
  r=calc(name,x);check(r['terminal']['reinvestment']+1e-8>=r['terminal']['physicalReinvestmentFloor'],name+' stressed terminal floor')
check(calc('bear')['equityResidualPerShare']<0 and calc('bear')['conditionalPriceIfPositive'] is None,'negative residual not stock price')
(p/'checks.json').write_text(json.dumps({'passed':len(checks),'checks':checks},indent=2)+'\n');print(len(checks),'valuation checks PASS')
