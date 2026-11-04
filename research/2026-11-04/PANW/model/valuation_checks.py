from pathlib import Path
from copy import deepcopy
import json,math
from model import X,calculate
P=Path(__file__).parent
r=calculate(X);checks=[]
def ck(label,condition):
 assert condition,label
 checks.append(label)
def val(x):return calculate(x)['base']['conditionalValuePerShare']
def change(group,key,v):
 x=deepcopy(X);x[group][key]=v;return val(x)
out={'central':{k:v['conditionalValuePerShare'] for k,v in r.items()},'sensitivities':{}}
s=out['sensitivities']
s['wacc_g']=[{'wacc':w,'g':g,'value':val({**deepcopy(X),'scenarios':{**deepcopy(X['scenarios']),'base':{**X['scenarios']['base'],'wacc':w,'g':g}}})} for w in [.075,.08,.09,.10,.11,.12] for g in [.02,.025,.03,.035,.04] if w>g]
for name,group,key,values in [('taxRisk','capital','selectedHistoricalTaxRiskReserve',[0,500,719,832]),('netExistingDilution','capital','selectedExistingAwardNetDilution',[0,15,30]),('cashReserve','capital','operatingCashReserve',[1000,2000,3000]),('unknownCapital','capital','unknownPostJulyCapital',[-2000,-1000,0,1000]),('convertibleFairValue','capital','convertibleFairValueProxy',[1250,1774,2250]),('deferredComp','capital','deferredCompensationEconomicLiability',[0,405]),('taxShieldAnnual10y','common','annualSelectedAcquisitionTaxShield',[0,100,250,400]),('commission','common','netCommissionPerIncrementalRevenue',[0,.09,.15]),('tax','common','tax',[.20,.24,.28])]:
 s[name]=[{'input':v,'value':change(group,key,v)} for v in values]
s['priorNopatAnchor']=[]
for e in [500,1218,2000,3000]:
 x=deepcopy(X);x['normalizedOperatingEbitAnchor']=e;s['priorNopatAnchor'].append({'priorEbit':e,'value':val(x)})
s['marginShift']=[];s['growthShift']=[];s['roic']=[];s['capexFloor']=[]
for d in [-.05,-.025,0,.025,.05,.10]:
 x=deepcopy(X)
 for k in ['marginYear1','marginYear5','marginYear10']:x['scenarios']['base'][k]+=d
 s['marginShift'].append({'shift':d,'value':val(x)})
for d in [-.05,-.025,0,.025,.05,.10,.20]:
 x=deepcopy(X);x['scenarios']['base']['growthAfterYear1']=[g+d for g in X['scenarios']['base']['growthAfterYear1']];s['growthShift'].append({'shift':d,'value':val(x)})
for k in [.15,.20,.30,.40,.60]:
 x=deepcopy(X);x['scenarios']['base']['roic']=k;s['roic'].append({'roic':k,'value':val(x)})
for d in [0,.01,.02,.04]:
 x=deepcopy(X)
 for k in ['grossCapexRatioYear1','grossCapexRatioYear10']:x['scenarios']['base'][k]+=d
 s['capexFloor'].append({'additionalRevenueRatio':d,'value':val(x)})
x=deepcopy(X);x['common']['fundAllPositiveNopatGrowth']=False;s['revenueGrowthOnlyInvestment']={'value':val(x),'note':'Alternative margin-efficiency assumption, not base; cannot assert same marginal ROIC for unfunded margin gains.'}
# A bounded monotonic root search, explicitly returning null outside test domain.
def solve(kind,lo,hi):
 def f(z):
  x=deepcopy(X)
  if kind=='margin':
   for k in ['marginYear1','marginYear5','marginYear10']:x['scenarios']['base'][k]+=z
  else:x['scenarios']['base']['growthAfterYear1']=[g+z for g in X['scenarios']['base']['growthAfterYear1']]
  return val(x)
 grid=[f(lo+(hi-lo)*i/100) for i in range(101)];ck(kind+' inverse monotonic',all(b>=a-1e-8 for a,b in zip(grid,grid[1:])))
 target=X['price'];a,b=lo,hi
 if not(grid[0]<=target<=grid[-1]):return {'root':None,'range':[lo,hi],'valueAtUpperBound':grid[-1],'target':target}
 for _ in range(80):
  m=(a+b)/2
  if f(m)<target:a=m
  else:b=m
 root=(a+b)/2;return {'root':root,'value':f(root),'target':target,'range':[lo,hi]}
out['inverse']={'uniformMarginShift':solve('margin',0,.60),'growthShiftYears2to10':solve('growth',0,.50)}
for n,v in r.items():
 p=X['scenarios'][n];c=X['common'];prev=X['normalizedOperatingEbitAnchor']*(1-c['tax'])
 for row in v['rows']:
  ck(n+str(row['year'])+' tax',math.isclose(row['nopat'],row['ebitAfterSbcBeforeAcquiredAmort']*(1-c['tax']),rel_tol=1e-10))
  ck(n+str(row['year'])+' investment',row['netReinvestment']+1e-7>=max(0,row['nopat']-prev)/p['roic'])
  ck(n+str(row['year'])+' physical',row['netReinvestment']+1e-7>=row['grossCapitalInvestmentFloor']-row['physicalAndInternalSoftwareDa']+row['netCommissionInvestment']+row['otherWorkingCapitalInvestment'])
  ck(n+str(row['year'])+' fcff',math.isclose(row['fcff'],row['nopat']-row['netReinvestment'],abs_tol=1e-8))
  ck(n+str(row['year'])+' pv',math.isclose(row['pv'],row['fcff']/(1+p['wacc'])**(row['year']-2026),rel_tol=1e-10))
  prev=row['nopat']
 ck(n+' terminal financed',v['terminalReinvestment']+1e-7>=v['terminalNopat']*p['g']/p['roic'])
 ck(n+' ev',math.isclose(v['enterpriseValue'],sum(z['pv'] for z in v['rows'])+v['pvTerminal'],rel_tol=1e-12))
 ck(n+' equity',math.isclose(v['conditionalValuePerShare']*v['sharesMillions'],v['enterpriseValue']+v['capitalBridge'],rel_tol=1e-12))
ck('ordered',out['central']['bear']<out['central']['base']<out['central']['bull'])
out['checks']={'passed':len(checks),'labels':checks};(P/'valuation_checks.json').write_text(json.dumps(out,indent=2)+'\n');print('valuation',len(checks),'PASS')
