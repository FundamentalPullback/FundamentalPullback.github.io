from pathlib import Path
import json,copy
from model import run,I
P=Path(__file__).parent
out={}
def val(o):return run('base',o)['economicResidualPerShareProxy']
for name,key,vals in [('marginRecoveryFunding','marginRecoveryFunding',[0,.5,1]),('tax','tax',[.35,.45,.50]),('workingCapital','incrementalWcRatio',[.06,.12,.18]),('physicalCapex','capexDaFloor',[1,1.25,1.5,2]),('matchedPlanProxy','matchedPlanAnnualAdd',[0,23.3]),('shares','sharesProxy',[46.505570,48.1,50]),('recurringWorkingCapitalLeakage','recurringWcLeakage',[0,50,164.5]),('otherInvestment','otherInvestmentAnnual',[0,10,25]),('roic','roic',[.08,.12,.16])]:
 out[name]=[{'input':v,'economicResidualPerShareProxy':val({key:v})} for v in vals]
for name,key,vals in [('operatingCash','selectedOperatingCash',[100,233.1,350]),('taxReserve','selectedTaxReserve',[0,15.6,41.6]),('pensionReserve','grossPensionAndRetireeReserve',[80.2,122.4,150]),('otherClaims','selectedOtherClaims',[0,19,50]),('debtCarryingError','debtCarryingProxy',[1103.4,1113.4,1153.4])]:
 out[name]=[]
 for v in vals:
  b=copy.deepcopy(I['bridge']);b[key]=v;out[name].append({'input':v,'economicResidualPerShareProxy':val({'bridge':b})})
out['discountGrowth']=[{'discount':d,'growth':g,'economicResidualPerShareProxy':val({'discount':d,'terminalGrowth':g})} for d in [.085,.10,.12] for g in [0,.015,.02]]
target=46.94;lo=0;hi=.10
assert val({'marginUplift':lo})<target<val({'marginUplift':hi})
for _ in range(100):
 m=(lo+hi)/2
 if val({'marginUplift':m})<target:lo=m
 else:hi=m
m=(lo+hi)/2;r=run('base',{'marginUplift':m});err=r['economicResidualPerShareProxy']-target
assert abs(err)<1e-8
ys=[val({'marginUplift':x/10000}) for x in range(0,1001,5)];assert all(b>=a for a,b in zip(ys,ys[1:]))
out['inverse']={'target':target,'marginUplift':m,'firstMargin':r['rows'][0]['margin'],'terminalMargin':r['rows'][-1]['margin'],'firstFcff':r['rows'][0]['fcff'],'year10Revenue':r['rows'][-1]['revenue'],'residualError':err,'monotonicGridPoints':len(ys),'fundingCertified':False,'note':'Selected capital and operating assumptions fixed. Extra first-year funding/dilution not certified; not an executable financing plan.'}
lo=0;hi=.10
assert val({'marginUplift':lo,'marginRecoveryFunding':0})<target<val({'marginUplift':hi,'marginRecoveryFunding':0})
for _ in range(100):
 m=(lo+hi)/2
 if val({'marginUplift':m,'marginRecoveryFunding':0})<target:lo=m
 else:hi=m
m=(lo+hi)/2;r=run('base',{'marginUplift':m,'marginRecoveryFunding':0});err=r['economicResidualPerShareProxy']-target;assert abs(err)<1e-8
ys=[val({'marginUplift':x/10000,'marginRecoveryFunding':0}) for x in range(0,1001,5)];assert all(b>=a for a,b in zip(ys,ys[1:]))
out['inverseEfficiencyAlternative']={'marginUplift':m,'firstMargin':r['rows'][0]['margin'],'terminalMargin':r['rows'][-1]['margin'],'firstFcff':r['rows'][0]['fcff'],'residualError':err,'fundingCertified':False,'note':'Only revenue-driven incremental profit financed at selected ROIC; margin recovery assumed efficiency without extra capital. Physical and working-capital floors still apply. Not central.'}
(P/'sensitivities.json').write_text(json.dumps(out,indent=2)+'\n');print(out['inverse'])
