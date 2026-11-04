from pathlib import Path
from copy import deepcopy
import json,math
from model import X,calculate
P=Path(__file__).parent
R=calculate(X);checks=[]
def ck(s,b):
 assert b,s
 checks.append(s)
def value(x):return calculate(x)['base']['hybridConditionalPerShare']
out={'central':{n:r['hybridConditionalPerShare'] for n,r in R.items()},'sensitivity':{}}
s=out['sensitivity']
def one(group,key,vals):
 a=[]
 for v in vals:
  x=deepcopy(X);x[group][key]=v;a.append({'input':v,'conditionalHybridValue':value(x)})
 return a
for label,group,key,vs in [('cashReserve','capital','operatingCashReserve',[150,250,500,800]),('nciClaim','capital','nciSelectedEconomicClaim',[49.065,100,250,500]),('historicalTax','capital','historicalTaxReserve',[100,188.105,250]),('netAwardDilution','capital','selectedNetAwardDilution',[0,1.24,3]),('stakePriceEur','capital','technoprobePriceEur',[12.17,18.255,24.34,30.425,36.51]),('stakeExitTaxRate','capital','stakeSelectedExitTaxRate',[0,.20,.30]),('stakeLiquidityHaircut','capital','stakeLiquidityHaircut',[0,.10,.25]),('unobservedCapital','capital','postBalanceCashAdjustment',[-450,-225,0,225]),('incrementalWC','common','incrementalWorkingCapitalRatio',[.15,.27,.40]),('annualTaxShield','common','annualAcquisitionTaxShield',[0,3,6]),('taxBefore2036','common','taxBefore2036',[.16,.20,.24]),('terminalTax','common','tax2036AndTerminal',[.20,.22,.26])]:s[label]=one(group,key,vs)
s['formfactorClosing']=one('capital','formfactorClosingAssumed',[False,True])
s['formfactorLiquidityHaircut']=one('capital','formfactorLiquidityHaircut',[0,.25,.50,1])
s['formfactorPrice']=one('capital','formfactorPrice',[48.395,96.79,134.23497259])
s['wacc_g']=[]
for w in [.10,.11,.12,.1275,.14,.15]:
 for g in [.02,.025,.03,.035,.04]:
  x=deepcopy(X);x['scenarios']['base'].update(wacc=w,g=g);s['wacc_g'].append({'wacc':w,'g':g,'value':value(x)})
s['marginShift']=[];s['growthShift']=[];s['roic']=[];s['capexFloor']=[]
for d in [-.05,-.025,0,.025,.05,.10]:
 x=deepcopy(X);x['scenarios']['base']['margins']=[m+d for m in X['scenarios']['base']['margins']];s['marginShift'].append({'shift':d,'value':value(x)})
for d in [-.04,0,.04,.08,.12,.20]:
 x=deepcopy(X);x['scenarios']['base']['growthAfterYear1']=[g+d for g in X['scenarios']['base']['growthAfterYear1']];s['growthShift'].append({'shift':d,'value':value(x)})
for ro in [.15,.20,.30,.40,.60]:
 x=deepcopy(X);x['scenarios']['base']['roic']=ro;s['roic'].append({'roic':ro,'value':value(x)})
for d in [-.01,0,.01,.025]:
 x=deepcopy(X)
 for k in ['capexRatioYear1','capexRatioYear10']:x['scenarios']['base'][k]+=d
 s['capexFloor'].append({'shift':d,'value':value(x)})
x=deepcopy(X);x['common']['releaseWorkingCapitalOnDecline']=True;s['wcReleaseOnDecline']={'value':value(x),'note':'Allows assumed working capital recovery on falling revenue; not an observed receivable/inventory recovery.'}
s['jointHighDemandStress']=[]
for d in [0,.03,.05]:
 x=deepcopy(X);p=x['scenarios']['bull'];p['margins']=[.40]*10;p['growthAfterYear1']=[g+d for g in p['growthAfterYear1']];p['wacc']=.10
 a=calculate(x)['bull'];s['jointHighDemandStress'].append({'margin':.40,'growthShiftOverBull':d,'wacc':.10,'value':a['hybridConditionalPerShare'],'terminalShare':a['terminalShareOfIndustrialEV'],'interpretation':'Joint optimistic assumptions, not a probability or certified target.'})
# A pure illustrative industrial residual excludes the quoted investee mark entirely.
x=deepcopy(X);x['capital']['technoprobePriceEur']=0;s['stakeZero']={'value':value(x)}
def solve(kind,lo,hi):
 def f(z):
  x=deepcopy(X)
  if kind=='margin':x['scenarios']['base']['margins']=[m+z for m in X['scenarios']['base']['margins']]
  else:x['scenarios']['base']['growthAfterYear1']=[g+z for g in X['scenarios']['base']['growthAfterYear1']]
  return value(x)
 grid=[f(lo+(hi-lo)*i/100) for i in range(101)];mono=all(b>=a-1e-8 for a,b in zip(grid,grid[1:]));ck(kind+' inverse monotonic',mono)
 if not(grid[0]<=X['price']<=grid[-1]):return {'root':None,'range':[lo,hi],'valueAtUpperBound':grid[-1]}
 a,b=lo,hi
 for _ in range(80):
  m=(a+b)/2
  if f(m)<X['price']:a=m
  else:b=m
 z=(a+b)/2;return {'root':z,'value':f(z),'target':X['price'],'range':[lo,hi]}
out['inverse']={'uniformMarginShift':solve('margin',0,.60),'uniformGrowthShiftYears2to10':solve('growth',0,.50)}
for n,r in R.items():
 p=X['scenarios'][n];prev=X['ebitPreAcqAmortAnchor']*(1-X['initialTax'])
 for a in r['rows']:
  pre=n+str(a['year']);ck(pre+' nopat',math.isclose(a['nopat'],a['revenue']*a['marginAfterSbcBeforeAcquiredAmort']*(1-a['taxRate']),rel_tol=1e-11));ck(pre+' funded',a['netReinvestment']+1e-8>=max(0,a['nopat']-prev)/p['roic']);ck(pre+' physical',a['netReinvestment']+1e-8>=a['grossCapexFloor']-a['physicalOtherDa']+a['workingCapitalInvestment']);ck(pre+' no WC windfall',a['workingCapitalInvestment']>=0);ck(pre+' fcff',math.isclose(a['fcff'],a['nopat']-a['netReinvestment'],abs_tol=1e-8));ck(pre+' PV',math.isclose(a['pv'],a['fcff']/(1+p['wacc'])**(a['year']-2026),rel_tol=1e-11));prev=a['nopat']
 ck(n+' terminal physical floor',r['terminalReinvestment']+1e-8 >= r['rows'][-1]['revenue']*(1+p['g'])*(p['capexRatioYear10']-X['common']['depreciationRatio'])+r['rows'][-1]['revenue']*p['g']*X['common']['incrementalWorkingCapitalRatio']);ck(n+' terminal funded',r['terminalReinvestment']+1e-8>=r['terminalNopat']*p['g']/p['roic']);ck(n+' EV',math.isclose(r['enterpriseValueIndustrial'],sum(a['pv'] for a in r['rows'])+r['pvTerminal'],rel_tol=1e-12));ck(n+' SOTP',math.isclose(r['hybridConditionalEquity'],r['enterpriseValueIndustrial']+r['industrialCapitalBridge']+r['technoprobeNetSelectedMark']+r['formfactorConditionalMarkedAsset'],rel_tol=1e-12));ck(n+' per share',math.isclose(r['hybridConditionalPerShare']*r['sharesMillions'],r['hybridConditionalEquity'],rel_tol=1e-12));ck(n+' tax holiday ends',r['rows'][-1]['taxRate']==.22);ck(n+' no total certified',r['certifiedTotalFairValue'] is None)
ck('FORM closing pays cash',R['base']['formfactorConditionalCashOutflow']==300);ck('FORM mark financed',math.isclose(R['base']['formfactorConditionalMarkedAsset'],2.234887*96.79,rel_tol=1e-12));ck('FORM loss no tax credit',R['base']['formfactorConditionalMarkedAsset']<300);ck('FORM no-close reconciliation',math.isclose(s['formfactorClosing'][0]['conditionalHybridValue']-s['formfactorClosing'][1]['conditionalHybridValue'],(300-2.234887*96.79)/R['base']['sharesMillions'],rel_tol=1e-10));
ck('ordered',out['central']['bear']<out['central']['base']<out['central']['bull']);out['checks']={'passed':len(checks),'labels':checks};(P/'checks.json').write_text(json.dumps(out,indent=2)+'\n');print(len(checks),'valuation PASS')
