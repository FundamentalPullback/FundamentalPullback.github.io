from pathlib import Path
import json,math
p=Path(__file__).parent;f=json.loads((p/'facts/inputs.json').read_text());a=json.loads((p/'analysis.json').read_text());h=json.loads((p/'history/history.json').read_text());m=json.loads((p/'publication.json').read_text());s=(p/'report.md').read_text();tests=[]
def check(n,t):tests.append({'name':n,'pass':bool(t)});assert t,n
for k,v in [('q2_ebit_ex_reported_tariff_benefit_approx',50.405),('h1_ebit_ex_reported_tariff_benefit_approx',78.629),('ttm_ebit_ex_reported_tariff_benefit_approx',286.948),('net_cash_before_leases_and_other_obligations',92.954),('operating_lease_total',1865.747),('participation_payment_less_financing_classification_approx',52.197),('h1_prior_ex_impairment_approx',35.022),('h1_prior_ex_impairment_and_inventory_writedown_illustrative',110.022)]:check(k,math.isclose(a[k],v,abs_tol=1e-5))
check('refund recognized once',math.isclose(f['refund_cogs']+f['refund_sga'],f['refund_including_interest']))
check('H1 negative FCF',math.isclose(h['H12026']['fcf_reported_proxy'],-11.312))
check('H1 SBC precise cashflow',math.isclose(h['H12026']['sbc'],28.851))
for k in ['bear','base','bull','buy_ceiling','owner_fcf','equity_bridge','certified_close']:check(k+' unknown',m[k] is None)
for k in ['approved_entry','stage35_approved','latestCompleted','bridge_certified']:check(k+' not approved',m[k] is False)
for name,r in h.items():check(name+' owner unknown',r['owner_fcf'] is None)
for k in ['pros_es','cons_es','pros_en','cons_en']:
 for line in m[k]:check(k+' exact passage',line in s)
check('no unresolved placeholders','{HISTORY_TABLE}' not in s)
(p/'qa.json').write_text(json.dumps({'all_pass':True,'count':len(tests),'tests':tests},indent=2)+'\n');print(len(tests),'QA passed')
