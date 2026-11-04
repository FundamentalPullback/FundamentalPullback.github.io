import json
from pathlib import Path
from model import run,INPUT
P=Path(__file__).resolve().parent
def values(change):
 r=run('base',change);return {'failure':r['conditionalFailureValuePerShare'],'close':r['conditionalImmediateCloseValuePerShare'],'standaloneBeforeFailure':r['standaloneBeforeFailureCosts']}
x={}
x['discount_growth']=[dict(syyWacc=w,jrdWacc=w+.005,g=g,**values({'scenarios.base.syy.wacc':w,'scenarios.base.jrd.wacc':w+.005,'scenarios.base.syy.g':g,'scenarios.base.jrd.g':g})) for w in [.075,.085,.095,.105] for g in [.015,.02,.025,.03]]
for key,vals in {'capital.bookToPrincipalAndHedgeReserve':[0,200,400],'capital.operatingCashReserve':[500,1500,2500],'capital.historicalTaxTimingReserve':[0,126,186],'capital.postSeptemberOtherNetCapital':[-1000,-500,0,500],'capital.octoberFinancingCostReserve':[0,150,300],'transaction.buyerCostReserve':[0,100,240],'transaction.closingAdjustmentReserve':[0,300,600,1000],'transaction.conditionalRegulatoryFailureFee':[0,1164],'transaction.failureOtherCostReserve':[0,200,500],'sharesStandalone':[492.270756,493.874171,494,500],'businesses.syy.tax':[.225,.25,.275],'businesses.jrd.additionalAnnualCompPreTax':[0,45,90],'businesses.jrd.tax':[.25,.275,.30],'businesses.syy.grossCapexRatio':[.01,.012,.015,.018],'businesses.jrd.grossCapexRatio':[.01,.012,.018,.025],'scenarios.base.syy.roic':[.08,.10,.12,.16],'scenarios.base.jrd.roic':[.10,.15,.20,.25]}.items():
 x[key]=[dict(input=v,**values({key:v})) for v in vals]
x['marginEfficiencyNoExtraCapitalSensitivity']={'assumption':'Revenue-growth NOPAT investment only; margin uplift funded from already-expensed efficiency effort with no extra capital. Alternative, not central.',**values({'businesses.syy.growthFundingMode':'revenueOnly','businesses.jrd.growthFundingMode':'revenueOnly'})}
x['margin_parallel']=[dict(change=m,**values({f'scenarios.base.{who}.{k}':INPUT['scenarios']['base'][who][k]+m for who in ['syy','jrd'] for k in ['margin1','margin5','margin10']})) for m in [-.01,-.005,0,.005,.01,.02]]
x['synergy_target']=[dict(annualTarget=v,**values({'scenarios.base.synergyAnnual':[0,.6*v,v,v,v,v,v,v,v,v]})) for v in [0,125,250]]
# Closing-case reverse: equal parallel margins, cash/debt and funded reinvestment unchanged.
def inverse_metric(v):return values({f'scenarios.base.{who}.{k}':INPUT['scenarios']['base'][who][k]+v for who in ['syy','jrd'] for k in ['margin1','margin5','margin10']})['close']
grid=[(-.02+i*.001,inverse_metric(-.02+i*.001)) for i in range(101)]
monotonic=all(grid[i+1][1]>=grid[i][1]-1e-9 for i in range(len(grid)-1));roots=[]
for (a,fa),(b,fb) in zip(grid,grid[1:]):
 if (fa-INPUT['price'])*(fb-INPUT['price'])<0:
  for _ in range(70):
   mid=(a+b)/2;fm=inverse_metric(mid)
   if (fa-INPUT['price'])*(fm-INPUT['price'])<=0:b=mid
   else:a=mid;fa=fm
  roots.append({'parallelMarginIncrease':(a+b)/2,'closeValue':inverse_metric((a+b)/2)})
x['conditionalCloseReverse']={'targetPrice':INPUT['price'],'marginGrid':[-.02,.08],'monotonic':monotonic,'roots':roots,'meaning':'Conditional closing case only. Not market-implied deal probability or a recommendation.'}
r=run('base');t=INPUT['transaction'];dealgain=r['jrd']['enterpriseValue']+r['synergyValue']-t['economicCashFreeDebtFreeBase']-t['buyerCostReserve']-t['closingAdjustmentReserve'];x['staticDealTimingSensitivity']=[]
for months in [0,3,6,12]:
 for carry in [0,100,250]:
  value=(r['syy']['enterpriseValue']+r['capitalBridgeProxy']+dealgain/(1+INPUT['scenarios']['base']['jrd']['wacc'])**(months/12)-carry)/(INPUT['sharesStandalone']+INPUT['conditionalSellerShares'])
  x['staticDealTimingSensitivity'].append({'monthsAssumedDelay':months,'additionalNetCarryCost':carry,'conditionalCloseValue':value,'meaning':'Static net-deal-value timing stress, not a dated closing forecast or complete preclose financing projection.'})
(P/'sensitivities.json').write_text(json.dumps(x,indent=2)+'\n');print(x['conditionalCloseReverse'])
