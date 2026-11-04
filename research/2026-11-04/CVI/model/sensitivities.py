from pathlib import Path
from copy import deepcopy
import json
from model import calculate,X
P=Path(__file__).resolve().parent

def calc(x):
 r=calculate(x)['base'];return {'failureSignedResidualPerShare':r['failureAfterCommonOffering']['signedResidualPerShare'],'closingSignedResidualPerShare':r['immediateClosing']['signedResidualPerShare'],'parentEV':r['parent']['operatingEV'],'targetEV':r['target']['operatingEV']}
def change(path,val):
 y=deepcopy(X);p=y
 for k in path[:-1]:p=p[k]
 p[path[-1]]=val;return y
s={}
for name,path,values in [
 ('parentNormalizedEbitda',['scenarios','base','parent','ebitdaNormalizedYear5'],[300,450,600,750,900]),
 ('targetNormalizedEbitda',['scenarios','base','target','ebitdaNormalizedYear5'],[300,500,700,900,1100]),
 ('operatingCashReserve',['capital','selectedOperatingCashReserve'],[0,250,500,750]),
 ('historicalIncomeTaxPayable',['capital','historicalIncomeTaxPayable'],[0,132,200]),
 ('uanStakeRecoveryFraction',['capital','uanQuotedEquityStake'],[0,230.83452,461.66904,692.50356]),
 ('uanExitTaxReserve',['capital','selectedUanExitTaxReserve'],[0,50,100]),
 ('failureFee',['transaction','failureTerminationFee'],[0,84,168,252]),
 ('pipePrice',['transaction','pipePriceIllustration'],[53.37,47.55,490/10.515248,45,40]),
 ('workingCapitalPurchaseAdjustment',['transaction','purchasePriceIncludingWorkingCapital'],[4200,4569,4969,5369]),
 ('financingFriction',['transaction','debtFinancingFrictionProxy'],[58,75,100,150]),
 ('parentTurnaroundAnnual',['scenarios','base','parent','turnaroundCapexYear1'],[50,100,150,200]),
 ('targetTurnaroundAnnual',['scenarios','base','target','turnaroundCapexYear1'],[35,70,105,140]),
 ('targetCarveoutReplacementCost',['scenarios','base','target','corporateCashCostYear1'],[0,20,40,60]),
 ('unknownPostSeptemberCapital',['capital','unknownPostSeptemberCapital'],[-500,-250,0,250,500]),
 ('parentRoic',['scenarios','base','parent','roic'],[.08,.12,.16,.20]),
 ('targetRoic',['scenarios','base','target','roic'],[.08,.12,.16,.20])]:
 s[name]=[dict(value=v,**calc(change(path,v))) for v in values]
s['discountGrowthMatrix']=[]
for w in [.09,.10,.11,.12]:
 for g in [0,.01,.015,.02]:
  y=deepcopy(X)
  for unit in ['parent','target']:
   y['scenarios']['base'][unit]['wacc']=w+(0 if unit=='parent' else .005);y['scenarios']['base'][unit]['g']=g
  s['discountGrowthMatrix'].append(dict(parentWacc=w,targetWacc=w+.005,g=g,**calc(y)))
# Simultaneous sustainable EBITDA uplift after year1; end-year5 ramp as modeled.
def shifted(delta):
 y=deepcopy(X)
 for u in ['parent','target']:y['scenarios']['base'][u]['ebitdaNormalizedYear5']+=delta
 return calc(y)
lo,hi=0.,5000.
for _ in range(100):
 mid=(lo+hi)/2
 if shifted(mid)['closingSignedResidualPerShare']<X['price']:lo=mid
 else:hi=mid
s['inverseJointNormalizedEbitdaUplift']={'upliftEachBusiness':(lo+hi)/2,'parentNormalizedEbitda':450+(lo+hi)/2,'targetNormalizedEbitda':500+(lo+hi)/2,'referencePrice':X['price'],'result':shifted((lo+hi)/2),'meaning':'One selected equal-dollar two-business path, not a unique implied forecast or probability; all positive NOPAT growth funded.'}
c=X['capital'];t=X['transaction'];legacy=c['rfsHistoricalLiability']+c['derivativeNetLiabilityAfterCollateralAndAssets']+c['historicalIncomeTaxPayable']+c['historicalCashCompensationLiability']+c['historicalAccruedInterestExUan']+c['environmentalLegacyReserve']+c['utbLegacyReserve']
sources=c['cashExUanRounded']+t['commonNetProceeds']+t['pipeProceeds']+2750-t['debtFinancingFrictionProxy']
uses=t['purchasePriceIncludingWorkingCapital']+183+t['futureAcquisitionCosts']+t['nonrefundableIepFee']+t['targetLegacyEnvironmentalAndAro']+t['additionalClosingAdjustmentReserve']+c['selectedOperatingCashReserve']+legacy
s['illustrativeFundingStress']={'sources':sources,'usesIncludingSelectedReserves':uses,'shortfallBeforeUnverifiedInventoryFinancingOrInterimCash':uses-sources,'legacyPaymentsIncluded':legacy,'notForecast':'Selected operating and closing reserves are prudential, not contractually required amounts. No timing bridge or inventory monetization/debt liability terms certified. New debt2750 is assumed drawn only in this stress, not reported actual.'}
s['cycleRecoveryUsingExistingCapacity']=[]
for case in ['bear','base','bull']:
 y=deepcopy(X)
 for unit in ['parent','target']:y['scenarios'][case][unit]['fundAllPositiveNopatGrowth']=False
 r=calculate(y)[case]
 s['cycleRecoveryUsingExistingCapacity'].append({'case':case,'failureSignedResidualPerShare':r['failureAfterCommonOffering']['signedResidualPerShare'],'closingSignedResidualPerShare':r['immediateClosing']['signedResidualPerShare']})
def relaxed(delta):
 y=deepcopy(X)
 for unit in ['parent','target']:
  y['scenarios']['base'][unit]['ebitdaNormalizedYear5']+=delta
  y['scenarios']['base'][unit]['fundAllPositiveNopatGrowth']=False
 return calc(y)
lo,hi=0.,5000.
for _ in range(100):
 mid=(lo+hi)/2
 if relaxed(mid)['closingSignedResidualPerShare']<X['price']:lo=mid
 else:hi=mid
s['inverseExistingCapacityCycleRecovery']={'upliftEachBusiness':(lo+hi)/2,'parentNormalizedEbitda':450+(lo+hi)/2,'targetNormalizedEbitda':500+(lo+hi)/2,'result':relaxed((lo+hi)/2),'meaning':'Capacity held fixed; cyclical margin recovery does not require separate plant investment, while physical/turnaround floors and nominal-growth/terminal reinvestment remain. Selected sensitivity, not proven capacity or cost forecast.'}
(P/'sensitivities.json').write_text(json.dumps(s,indent=2));print('Built sensitivities')
