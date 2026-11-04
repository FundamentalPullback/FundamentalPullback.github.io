from model import inputs,calc
from pathlib import Path
import json,copy
p=Path(__file__).resolve().parent
specs=[('marginRecoveryCapitalFundingFraction',[0,.5,1]),('physicalCapexToResidualDdaFloor',[.75,1,1.25]),('rentalCashFactor',[.9,1,1.1]),('tax',[.23,.26,.29]),('workingCapitalPerIncrementalRevenue',[.05,.1,.2]),('otherInvestingAnnualStress',[0,22,44]),('capital.operatingCashReserveSelected',[300,500,800]),('capital.unreconciledClaimReserveSelected',[0,100,250]),('capital.sharesProxy',[113.376445,118,124]),('cases.base.wacc',[.095,.11,.125]),('cases.base.terminalGrowth',[0,.01,.02]),('cases.base.marginalRoic',[.08,.12,.16])]
out=[]
for key,vals in specs:
 rows=[]
 for val in vals:
  x=copy.deepcopy(inputs);o=x
  parts=key.split('.')
  for k in parts[:-1]:o=o[k]
  o[parts[-1]]=val;r=calc('base',x);rows.append({'input':val,'equityResidualPerShare':r['equityResidualPerShare'],'operatingEvAfterRent':r['operatingEvAfterFullRent']})
 out.append({'parameter':key,'rows':rows})
(p/'sensitivities.json').write_text(json.dumps(out,indent=2)+'\n')
# Both inverse variants require a valid bracket and a small final target residual.
target=inputs['latestClose']
def solve(x):
 lo,hi=0,.15
 flo=calc('base',x,margin_shift=lo)['equityResidualPerShare']-target
 fhi=calc('base',x,margin_shift=hi)['equityResidualPerShare']-target
 assert flo<=0<=fhi,('inverse target not bracketed',flo,fhi)
 grid=[calc('base',x,margin_shift=j*.0005)['equityResidualPerShare'] for j in range(301)]
 assert all(a<=b+1e-9 for a,b in zip(grid,grid[1:])), 'inverse not monotonic on checked grid'
 for _ in range(100):
  mid=(lo+hi)/2
  if calc('base',x,margin_shift=mid)['equityResidualPerShare']<target:lo=mid
  else:hi=mid
 shift=(lo+hi)/2;r=calc('base',x,margin_shift=shift);error=r['equityResidualPerShare']-target
 assert abs(error)<1e-8,('inverse residual',error)
 return shift,r,{'lowValueMinusTarget':flo,'highValueMinusTarget':fhi,'finalResidual':error,'checkedMonotonicGridPoints':301}
shift,r,diag=solve(inputs)
result={'solved':True,'target':target,'marginUpliftAllYears':shift,'firstMargin':inputs['cases']['base']['margins'][0]+shift,'terminalMargin':inputs['cases']['base']['margins'][-1]+shift,'value':r['equityResidualPerShare'],'rootChecks':diag,'fullyFundedInverseFirstYearFcff':r['rows'][0]['fcff'],'fullyFundedInverseExternalFundingNotModeled':True,'warning':'Conditional reverse requirement, not forecast; positive margin-growth NOPAT funded at selected marginal ROIC. First-year negative FCFF creates a funding need; no financing execution, liquidity availability or dilution is certified.'}
x=copy.deepcopy(inputs);x['marginRecoveryCapitalFundingFraction']=0
shift,r,diag=solve(x)
result['efficiencyAlternative']={'marginFundingFraction':0,'marginUplift':shift,'firstMargin':x['cases']['base']['margins'][0]+shift,'terminalMargin':x['cases']['base']['margins'][-1]+shift,'value':r['equityResidualPerShare'],'rootChecks':diag}
(p/'inverse.json').write_text(json.dumps(result,indent=2)+'\n')
print('Both inverse brackets, residuals and monotonic grids PASS')
