import json,csv
from pathlib import Path
from model import run,INPUT
P=Path(__file__).resolve().parent
out={}
out['wacc_g']=[{'wacc':w,'g':g,'value':run(changes={'scenario.wacc':w,'scenario.g':g})['valuePerShare']} for w in [.085,.095,.105,.115] for g in [0,.01,.015,.02]]
out['midcycle_margin']=[{'terminalRealMargin':v,'value':run(changes={'scenario.margin2031Real2027':v})['valuePerShare']} for v in [8.84,10.88,12,15,17.26,20,25,30,38]]
out['capital']=[{'name':k,'assumption':v,'value':run(changes={k:v})['valuePerShare']} for k,vals in {'capital.additionalHistoricalTaxWcReserve':[0,1325,2687],'capital.operatingCashReserve':[0,3000,5000],'capital.nciEconomicProxy':[880,1200,2000],'capital.aroEnvironmentalCurrentStaleProxy':[0,205,400],'capital.propelAccrued':[947,1500,2000],'capital.unknownPostSeptemberNetCapital':[-2000,0,2000],'capital.receivableRemittancePrudence':[0,269],'capital.employeeNoncurrentReserve':[276,484,739]}.items() for v in vals]
out['operations']=[{'name':k,'assumption':v,'value':run(changes={k:v})['valuePerShare']} for k,vals in {'common.capitalSpendingFloor2027':[3000,4000,5000],'common.netReplacementFloorDaFraction':[.1,.25,.5],'scenario.refiningCashCost2027':[5000,5500,6000,6500],'scenario.midstreamEbit2027':[2200,2550,2900],'scenario.marketingEbit2027':[300,650,1000],'scenario.renewableEbit2031Real2027':[-250,0,250],'common.tax':[.21,.24,.27],'common.priorOperatingNopatAnchor':[10000,15000,20470.3]}.items() for v in vals]
out['jv']=[{'name':k,'assumption':v,'value':run(changes={k:v})['valuePerShare']} for k,vals in {'scenario.jvParentTax':[0,.15,.20,.24,.30],'scenario.jvRoe':[.08,.10,.125],'scenario.jvEarnings2031Real2027':[1000,1500,2000],'scenario.jvKe':[.09,.11,.13]}.items() for v in vals]
out['calendar']={'withEstimatedStub':run()['valuePerShare'],'withoutStub':run(changes={'common.stubEnabled':False})['valuePerShare'],'incorrectOneYearDiscountIllustration':run(changes={'common.year1DiscountDays':365})['valuePerShare']}
out['shares']={'currentPlusProxies':run()['sharesMillions'],'weightedQ3Sensitivity':run()['equityValue']/398.953}
# Scan rather than assume monotonic behavior when reinvestment floors change.
grid=[(v/20,run(changes={'scenario.margin2031Real2027':v/20})['valuePerShare']) for v in range(0,1201)]
roots=[];target=INPUT['price']
for (a,fa),(b,fb) in zip(grid,grid[1:]):
 if (fa-target)*(fb-target)<0:
  lo,hi=a,b
  for _ in range(60):
   mid=(lo+hi)/2;fm=run(changes={'scenario.margin2031Real2027':mid})['valuePerShare']
   if (fa-target)*(fm-target)<=0: hi=mid
   else:lo=mid;fa=fm
  root=(lo+hi)/2;roots.append({'margin2031Real2027':root,'value':run(changes={'scenario.margin2031Real2027':root})['valuePerShare']})
out['reverse']={'targetPrice':target,'searchedRealMarginRange':[0,60],'roots':roots,'monotonicIncreasingOnGrid':all(b[1]>=a[1] for a,b in zip(grid,grid[1:])),'holdsOtherBaseAssumptionsConstant':True,'notMarketConsensus':True}
(P/'sensitivities.json').write_text(json.dumps(out,indent=2)+'\n')
print(out['reverse'])
