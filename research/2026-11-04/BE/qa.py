from pathlib import Path
import json
p=Path(__file__).parent;f=json.loads((p/'facts/inputs.json').read_text());a=json.loads((p/'analysis.json').read_text());m=json.loads((p/'publication.json').read_text());h=json.loads((p/'history/history.json').read_text());checks=[]
def ck(n,b):checks.append({'check':n,'pass':bool(b)});assert b,n
for k,v in {'cfo_less_ppe_9m':41.585,'after_sbc_proxy_9m':-116.056,'limited_ebit_ex_tariff_9m':442.676,'oracle_issued_shares':2.154231,'oracle_asset_rounded':306.5,'debt_carrying_discount_cost_difference':49.272,'nominal_debt_less_cash_ex_financing':39.019,'financing_obligation_balance_vs_pv_difference_rounded':149.306,'vendor_advance_balance_change':309.640,'cash_contract_assets_and_deposits_net':-7.437,'customer_concentration_share_9m':.66,'price_difference':.01}.items():ck(k,abs(a[k]-v)<1e-7)
ck('principal reconciliation',abs(f['recourse_principal']+f['nonrecourse_principal']-f['total_debt_principal'])<1e-7)
ck('warranty balance',abs(f['warranty_performance_prior']+f['warranty_performance_accrual']-f['warranty_performance_payments']-f['warranty_performance_balance'])<1e-7)
ck('finance payment PV',abs(f['financing_obligations_nominal_payments']-f['financing_obligations_imputed_interest']-f['financing_obligations_payment_pv'])<1e-7)
ck('available revolver',f['revolver_limit']-f['revolver_letters_of_credit']==f['available_revolver'])
ck('shares already include notes/awards',abs(f['shares_q3_basic']+f['convertible_shares_in_diluted_q3']+f['awards_in_diluted_q3']-f['shares_q3_diluted'])<1e-7)
ck('ifconverted numerator',abs(f['q3_attributable_ni']+f['q3_ifconverted_interest_adjustment']-f['q3_diluted_ni'])<1e-7)
ck('purchase commitments sum',sum(f[k] for k in ['purchases_2026_remaining_rounded','purchases_2027_rounded','purchases_2028_rounded','purchases_2029_rounded'])==f['purchases_commitments_rounded'])
for k in ['bear','base','bull','buy_ceiling','owner_fcf','equity_bridge']:ck(k+' deliberately null',a[k] is None and m[k] is None)
for k in ['approved_entry','stage35_approved','latestCompleted']:ck(k+' false',m[k] is False)
ck('calendar unknown',a['next_earnings_date'] is None)
ck('price not certified',f['price_certified'] is None)
for k in ['pros_es','cons_es','pros_en','cons_en']:
 ck(k+' nonempty',len(m[k])==3)
 for s in m[k]:ck('exact '+s[:25],s in (p/'report.md').read_text())
ck('no placeholder','{HISTORY_TABLE}' not in (p/'report.md').read_text())
for r in h['rows']:
 if all(r.get(k) is not None for k in ['cfo','capex_ppe','fcf_ppe']):ck('CFO-PPE '+r['period'],abs(r['cfo']-r['capex_ppe']-r['fcf_ppe'])<1e-5)
(p/'qa.json').write_text(json.dumps({'passed':len(checks),'failed':0,'checks':checks},indent=2)+'\n');print(len(checks),'PASS')
