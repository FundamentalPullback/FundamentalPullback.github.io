import json
from pathlib import Path
from model import run,INPUT
P=Path(__file__).resolve().parent
out={}
out['wacc_g']=[{'wacc':w,'g':g,'value':run(changes={'scenario.wacc':w,'scenario.g':g})['valuePerShare']} for w in [.085,.095,.105,.115] for g in [.02,.025,.03,.035]]
out['roic']=[{'roic':r,'value':run(changes={'scenario.roic':r})['valuePerShare']} for r in [.15,.20,.25,.35,.50,.75,1.0]]
out['capital']=[{'name':k,'assumption':v,'value':run(changes={k:v})['valuePerShare']} for k,vals in {'capital.strategicRecoveryAfterTaxLiquidityFraction':[0,.5,1],'capital.operatingCashReserve':[0,1500,2500],'capital.unknownPostSeptemberNetCapital':[-500,0,500],'capital.additionalContingencyReserve':[0,250,500],'root.sharesMillions':[1037.917,1043.011,1050,1070,1090]}.items() for v in vals]
out['operating']=[{'name':k,'assumption':v,'value':run(changes={k:v})['valuePerShare']} for k,vals in {'common.cashTaxRate':[.20,.25,.30],'common.cashCapexRevenueRatio':[.035,.045,.06],'common.netCommissionPerIncrementalRevenue':[.05,.10,.15],'common.otherWcPerIncrementalRevenue':[0,.02,.05],'common.newLeadershipTargetChargeTotal':[0,126.55,250]}.items() for v in vals]
out['marginShift']=[{'percentagePointShift':shift*100,'value':run(changes={f'scenario.margin{y}':INPUT['scenarios']['base'][f'margin{y}']+shift for y in [2027,2031,2036]})['valuePerShare']} for shift in [-.03,-.01,0,.01,.03,.05]]
out['calendar']={'withStub':run()['valuePerShare'],'withoutStub':run(changes={'common.stubEnabled':False})['valuePerShare'],'incorrectOneYearDiscountIllustration':run(changes={'common.firstDiscountDays':365})['valuePerShare']}
# Tax neutrality of acquired book amortization when tax deductions are not established.
out['acquiredAmortZeroValuationCheck']=run(changes={'common.acquiredAmortMemo':[0]*10})['valuePerShare']
# Find all roots over a stated grid. Margin shifts also fund their incremental NOPAT.
target=INPUT['price'];grid=[]
for step in range(-100,501):
 shift=step/1000;changes={f'scenario.margin{y}':INPUT['scenarios']['base'][f'margin{y}']+shift for y in [2027,2031,2036]};grid.append((shift,run(changes=changes)['valuePerShare']))
roots=[]
for (a,fa),(b,fb) in zip(grid,grid[1:]):
 if (fa-target)*(fb-target)<0:
  lo,hi=a,b
  for _ in range(60):
   mid=(lo+hi)/2;v=run(changes={f'scenario.margin{y}':INPUT['scenarios']['base'][f'margin{y}']+mid for y in [2027,2031,2036]})['valuePerShare']
   if (fa-target)*(v-target)<=0:hi=mid
   else:lo=mid;fa=v
  root=(lo+hi)/2;roots.append({'parallelMarginIncrease':root,'margin2027':.15+root,'margin2036':.23+root,'value':run(changes={f'scenario.margin{y}':INPUT['scenarios']['base'][f'margin{y}']+root for y in [2027,2031,2036]})['valuePerShare']})
out['reverse']={'targetPrice':target,'searchedMarginShift':[-.1,.5],'monotonicOnGrid':all(b[1]>=a[1] for a,b in zip(grid,grid[1:])),'roots':roots,'notConsensus':True}
growth_grid=[(z/1000,run(changes={'scenario.growth':[v+z/1000 for v in INPUT['scenarios']['base']['growth']]})['valuePerShare']) for z in range(0,151)]
growth_roots=[]
for (a,fa),(b,fb) in zip(growth_grid,growth_grid[1:]):
 if (fa-target)*(fb-target)<0:
  lo,hi=a,b
  for _ in range(60):
   mid=(lo+hi)/2;v=run(changes={'scenario.growth':[g+mid for g in INPUT['scenarios']['base']['growth']]})['valuePerShare']
   if (fa-target)*(v-target)<=0:hi=mid
   else:lo=mid;fa=v
  shift=(lo+hi)/2;growth_roots.append({'annualGrowthShift':shift,'growth2027':.18+shift,'growth2036':.03+shift,'value':run(changes={'scenario.growth':[g+shift for g in INPUT['scenarios']['base']['growth']]})['valuePerShare']})
out['reverseGrowth']={'range':[0,.15],'roots':growth_roots,'monotonicOnGrid':all(b[1]>=a[1] for a,b in zip(growth_grid,growth_grid[1:])),'terminalGStill':.03,'notConsensus':True}
(P/'sensitivities.json').write_text(json.dumps(out,indent=2)+'\n');print(out['reverse'])
