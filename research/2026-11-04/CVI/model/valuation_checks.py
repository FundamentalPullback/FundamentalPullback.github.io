from pathlib import Path
from copy import deepcopy
import json,math
from model import X,calculate
P=Path(__file__).resolve().parent;r=calculate(X);checks=[]
def check(name,ok):
 assert ok,name
 checks.append({'check':name,'passed':True})
def close(a,b):return abs(a-b)<1e-7*max(1,abs(a),abs(b))
for case,z in r.items():
 for unit in ['parent','target']:
  q=z[unit];p=X['scenarios'][case][unit];prev=p['priorNopatAnchor']
  check(f'{case}.{unit}.tenyears',len(q['rows'])==10)
  for row in q['rows']:
   pre=f'{case}.{unit}.{row["year"]}'
   check(pre+'.ebit',close(row['ebit'],row['ebitdaBeforeTurnaroundCash']-row['corporateCashCost']-row['daIncludingTurnaround']))
   check(pre+'.tax_no_refund',close(row['nopat'],row['ebit']-max(row['ebit'],0)*X['common']['tax']))
   check(pre+'.funded_growth',row['netReinvestment']+1e-8>=max(0,row['nopat']-prev)/p['roic'])
   check(pre+'.physical_turnaround_funded',row['grossCapitalInvestment']+1e-8>=row['physicalCapexFloor']+row['turnaroundCapexFloor'])
   check(pre+'.fcff_identity',close(row['fcff'],row['nopat']+row['daIncludingTurnaround']-row['grossCapitalInvestment']-row['workingCapitalInvestment']))
   check(pre+'.pv',close(row['pv'],row['fcff']/(1+p['wacc'])**row['year']))
   prev=row['nopat']
  t=q['terminal'];last=q['rows'][-1];g=p['g']
  check(f'{case}.{unit}.wacc_g',p['wacc']>g)
  check(f'{case}.{unit}.terminal_funding',t['netReinvestment']+1e-8>=max(t['nopat'],0)*g/p['roic'])
  check(f'{case}.{unit}.terminal_physical',t['netReinvestment']+1e-8>=max(0,last['physicalCapexFloor']+last['turnaroundCapexFloor']-last['daIncludingTurnaround'])*(1+g)+last['workingCapitalInvestment']*(1+g))
  check(f'{case}.{unit}.terminal_identity',close(t['fcff'],t['nopat']-t['netReinvestment']))
  check(f'{case}.{unit}.ev',close(q['operatingEV'],sum(a['pv'] for a in q['rows'])+t['fcff']/(p['wacc']-g)/(1+p['wacc'])**10))
 check(case+'.pipe_signed_base',close(z['immediateClosing']['pipeSharesIllustration'],800/53.37))
 check(case+'.signed_residual_preserved',close(z['immediateClosing']['signedEquityResidual'],z['immediateClosing']['signedResidualPerShare']*z['immediateClosing']['shares']))
 check(case+'.failure_no_pipe',close(z['failureAfterCommonOffering']['shares'],100.530599+10.515248))
 check(case+'.funding_not_certified',not z['immediateClosing']['financingFeasibleCertified'])
s=json.loads((P/'sensitivities.json').read_text())
check('inverse_matches_price',close(s['inverseJointNormalizedEbitdaUplift']['result']['closingSignedResidualPerShare'],X['price']))
check('inverse_existing_capacity_matches_price',close(s['inverseExistingCapacityCycleRecovery']['result']['closingSignedResidualPerShare'],X['price']))
for k in ['parentNormalizedEbitda','targetNormalizedEbitda']:
 a=[v['closingSignedResidualPerShare'] for v in s[k]];check(k+'.monotone_grid',a==sorted(a))
for k in ['parentTurnaroundAnnual','targetTurnaroundAnnual','financingFriction','workingCapitalPurchaseAdjustment']:
 a=[v['closingSignedResidualPerShare'] for v in s[k]];check(k+'.decreasing_grid',a==sorted(a,reverse=True))
check('uan_no_double_debt',close(X['capital']['nominalDebtAndFinanceLeasesExUan'],1794-570.862))
check('uan_no_double_cash',close(X['capital']['cashExUanRounded'],1278-158.191))
check('uan_no_double_comp',close(X['capital']['historicalCashCompensationLiability'],35-5.428))
check('uan_no_double_interest',close(X['capital']['historicalAccruedInterestExUan'],22-9.897))
check('cycle_average',close(sum([106,1021,903,138,199])/5,473.4))
# Increase both upkeep floors; terminal must preserve higher physical demands.
y=deepcopy(X);y['scenarios']['base']['parent']['physicalCapexYear1']+=100;a=calculate(y)['base']['parent'];check('upkeep_terminal_sensitivity',a['terminal']['maintenanceNetReinvestment']>r['base']['parent']['terminal']['maintenanceNetReinvestment'])
(P/'valuation_checks.json').write_text(json.dumps({'passed':True,'count':len(checks),'checks':checks},indent=2));print(len(checks),'valuation checks PASS')
