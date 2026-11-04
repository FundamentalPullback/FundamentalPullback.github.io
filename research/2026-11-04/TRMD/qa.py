from pathlib import Path
import json,math
p=Path(__file__).parent;f=json.loads((p/'facts/inputs.json').read_text());a=json.loads((p/'analysis.json').read_text());h=json.loads((p/'history/normalized_history.json').read_text());m=json.loads((p/'publication.json').read_text());s=(p/'report.md').read_text();tests=[]
def check(name,test):tests.append({'name':name,'pass':bool(test)});assert test,name
check('carrying debt reconciles',math.isclose(f['borrowing_principal']-f['unamortized_borrowing_cost']+f['lease_liability'],f['carrying_borrowings']))
check('cash excludes restricted',math.isclose(a['cash_ex_restricted'],446.2))
check('historical net debt',math.isclose(a['historical_net_debt_ex_restricted'],704.1))
check('capex commitments',math.isclose(a['committed_vessels']+a['committed_other_capex'],615.3))
check('NAV debt same gross convention',math.isclose(a['debt_principal_plus_leases'],f['nav_borrowing_deduction']))
check('liquidity includes facilities',math.isclose(f['cash_total']+f['credit_facilities_undrawn'],f['reported_liquidity']))
for k in ['bear','base','bull','buy_ceiling','owner_fcf','equity_bridge','certified_close']:check(k+' unknown',m[k] is None)
for k in ['approved_entry','stage35_approved','latestCompleted','bridge_certified']:check(k+' not certified',m[k] is False)
for key,r in h.items():check(key+' owner unknown',r['owner_fcf'] is None)
for r in a['nav_sensitivity_not_fair_value']:check('NAV mechanical sensitivity '+str(r['broker_fleet_haircut']),math.isclose(r['after_declared_dividend_nav_proxy'],(f['issuer_nav']-138.7-f['fleet_broker_value']*r['broker_fleet_haircut'])/102.7))
for k in ['pros_es','cons_es','pros_en','cons_en']:
 for line in m[k]:check(k+' exact passage',line in s)
check('no unresolved placeholders','{HISTORY_TABLE}' not in s and '{NAV_TABLE}' not in s)
(p/'qa.json').write_text(json.dumps({'all_pass':True,'tests':tests,'count':len(tests)},indent=2)+'\n');print(len(tests),'QA passed')
