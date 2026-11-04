from pathlib import Path
import json
P=Path(__file__).parent;C=json.loads((P/'facts.json').read_text());checks={
'cash excludes restricted':C['cash']==7437.384 and C['restrictedCashExcluded']==13.506,
'notes principal':C['notesPrincipal']==3750,
'finance leases selected not exact':C['financeLeaseProxySelected']==15 and C['financeLeaseJuneDerived']==12.502,
'UTB reserve':abs(C['taxReserveSelected']-C['utbJuneGross']-C['utbJuneInterestPenalty'])<1e-7,
'currenttax increase':abs(C['currentIncomeOtherTaxes']-C['currentIncomeOtherTaxesJune']-537.576)<1e-7,
'ASR paid not repeated':C['asrPrepaidSeptember']==1000 and C['asrFutureSharesAssumed']==0,
'dated shares':C['sharesDate']=='2026-10-20' and C['coverShares']==1249.171,
'dividend payable':C['dividendPayable']==412.218,
'buyback payable':C['buybackPayable']==31.512,
'capex accrued':C['additionalCapexReserveSelected']==141.965,
'no transition tax duplicate':C['cashTaxTransitionRemaining']==0,
'no gross EDC asset':C['deferredCompNetAddedSelected']==0,
'all facts have primary source':all(u.startswith('https://') for u in C['sources'].values())}
assert all(checks.values());(P/'checks.json').write_text(json.dumps({'passed':len(checks),'checks':checks},indent=2)+'\n');print(len(checks),'capital checks PASS')
