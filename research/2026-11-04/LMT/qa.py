from pathlib import Path
import json,math
p=Path(__file__).parent;f=json.loads((p/'facts/inputs.json').read_text());a=json.loads((p/'analysis.json').read_text());h=json.loads((p/'history/normalized_history.json').read_text())['periods'];m=json.loads((p/'publication.json').read_text());s=(p/'report.md').read_text();tests=[]
def check(name,test):tests.append({'name':name,'pass':bool(test)});assert test,name
check('operating FAS CAS',f['cas_cost_9m']-f['pension_service_cost_9m']==f['fas_cas_operating_9m'])
check('total pension expense',f['pension_service_cost_9m']+f['pension_nonservice_cost_9m']==f['pension_expense_9m'])
for key,val in [('reported_fcf_9m',5625),('reported_fcf_9m_prior',4152),('cash_after_capex_and_sbc_proxy_9m',5356),('cash_after_capex_and_sbc_proxy_prior',3937),('cashflow_assets_liabilities_net',-1159),('net_contract_assets',4255),('net_contract_assets_prior',1561),('ebit_ex_profit_booking_9m_limited',6020),('ebit_ex_profit_booking_prior_limited',5600),('ebit_ex_booking_and_fas_cas_9m_limited',4756),('ebit_ex_booking_and_fas_cas_prior_limited',4462),('carrying_net_debt_subtotal',14538),('historical_gross_debt_rollforward_unverified',21746),('environmental_net_accounting_exposure',53),('program_loss_reserves_total',1754)]:check(key,math.isclose(a[key],val))
for k in ['bear','base','bull','buy_ceiling','owner_fcf','equity_bridge','certified_close']:check(k+' unknown',m[k] is None)
for k in ['approved_entry','stage35_approved','latestCompleted','bridge_certified']:check(k+' not certified',m[k] is False)
for key,r in h.items():check(key+' owner unknown',r['owner_fcf'] is None)
for k in ['pros_es','cons_es','pros_en','cons_en']:
 for line in m[k]:check(k+' exact passage',line in s)
check('no unresolved placeholders','{HISTORY_TABLE}' not in s and '{SOURCE_LIST}' not in s)
(p/'qa.json').write_text(json.dumps({'all_pass':True,'tests':tests,'count':len(tests)},indent=2)+'\n');print(len(tests),'QA passed')
