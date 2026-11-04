import json,math
from pathlib import Path
D=Path(__file__).parent
f=json.loads((D/'facts.json').read_text()); checks=[]
def check(name,condition):
 checks.append({'check':name,'passed':bool(condition)})
check('cash components',2514+5392==7906)
check('investment terms',f['cash']['short_term_investments']+f['cash']['long_term_investments']==5392)
src=(D/'selected_balance_excerpt.txt').read_text()
check('short-term balance sheet source', 'Short-term investments557' in src and f['cash']['short_term_investments']==557)
check('long-term balance sheet source','Long-term investments4,835' in src and f['cash']['long_term_investments']==4835)
check('short-term recurring FV gap',557-392==f['cash']['short_term_difference_outside_recurring_fair_value_table_derived'])
check('carrying amount policy explicitly qualified', 'not explicitly disclosed' in f['cash']['difference_nature'])
check('post-July headline bridge',7906-325-500==7081)
check('QRadar rollforward',514-117-191==206)
check('QRadar current/noncurrent',116+90==206)
check('principal derivation',1250-153==1097)
check('net debt and hedge fair value',1774-153==1621)
check('conversion strike formula',abs((1000-88.263)/4.3161-211.24)<.01)
check('nonoperating derivative normalization',620-58==562)
check('deferred liability portions',5+400==405)
check('gross tax exposure arithmetic not net liability',719+113==832)
check('share unit conversion',818771631/1e6==f['shares']['basic_m'])
check('award unit conversion',29821161/1e6==f['shares']['rsu_psu_m'])
check('options unit conversion',232754/1e6==f['shares']['options_m'])
check('reserve unresolved intentionally',f['cash']['operating_reserve'] is None)
check('tax net cash liability unresolved intentionally',f['tax']['verified_incremental_cash_liability'] is None)
check('old warrants no extra dilution',f['old_warrants']['incremental_outstanding_claim']==0)
# Convertible payoff boundaries: hedge negates conversion premium below cap (rounding tolerance).
n=1097/1000*4.3161;c=1097/1000*88.263;k=(1000-88.263)/4.3161
for p in [150,211.24,250,287.21,291.44,350]:
 premium=max(0,n*p+c-1097)
 hlow=n*max(0,min(p,287.21)-k);hhigh=n*max(0,min(p,291.44)-k)
 check('hedge bounded at price '+str(p),premium-hhigh>=-1e-8 and hlow<=hhigh+1e-8)
b=f['deferred_compensation']['named_executive_aggregate_balances_fy26']
check('executive deferred balance sum',math.isclose(b['Arora']+b['Golechha']+b['Jenkins'],b['total'],abs_tol=1e-8))
check('wider deferred balance not mechanically added',b['additional_incremental_deduction'] is None)
result={'all_passed':all(x['passed'] for x in checks),'count':len(checks),'checks':checks,'limitations':'Arithmetic/schema/payoff tests only; not independent source verification or full valuation QA.'}
(D/'offlinechecks.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'all_passed':result['all_passed'],'count':len(checks)}))
assert result['all_passed']
