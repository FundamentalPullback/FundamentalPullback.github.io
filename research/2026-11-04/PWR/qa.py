from pathlib import Path
import json
p=Path(__file__).parent;f=json.loads((p/'facts/inputs.json').read_text());a=json.loads((p/'analysis.json').read_text());m=json.loads((p/'publication.json').read_text());h=json.loads((p/'history/history.json').read_text());checks=[]
def ck(n,b):checks.append({'check':n,'pass':bool(b)});assert b,n
for k,v in {'cash_ex_jv_and_captive':2136.253,'separate_restricted_cash':6.018,'gross_debt_before_discount':7046.870,'contingent_consideration':837.380,'contract_liabilities_balance_change':2277.344,'contract_assets_balance_change':191.031,'price_difference':0.09,'scanner_vs_same_date_close_difference':18.32}.items():ck(k,abs(a[k]-v)<1e-7)
ck('debt carrying reconciliation',abs(a['gross_debt_before_discount']-f['debt_discount_costs']-f['debt_carrying'])<1e-7)
ck('acquisition price reconciliation',abs(sum(f[k] for k in ['acquisition_cash_consideration','acquisition_stock_consideration','acquisition_contingent_consideration'])-f['acquisition_total_consideration'])<1e-7)
ck('segment versus consolidated EBIT',abs(f['segment_ebit_9m26']-f['corporate_cost_9m26']-f['ebit_9m26'])<1e-7)
for k in ['bear','base','bull','buy_ceiling','owner_fcf','equity_bridge']:ck(k+' deliberately null',a[k] is None and m[k] is None)
for k in ['approved_entry','stage35_approved','latestCompleted']:ck(k+' false',m[k] is False)
ck('calendar unknown',a['next_earnings_date'] is None)
ck('redeemable unknown',f['redeemable_nci'] is None)
ck('price not certified',f['price_certified'] is None)
for k in ['pros_es','cons_es','pros_en','cons_en']:
 ck(k+' nonempty',len(m[k])==3)
 for s in m[k]:ck('exact '+s[:25],s in (p/'report.md').read_text())
ck('no placeholder','{HISTORY_TABLE}' not in (p/'report.md').read_text())
for r in h['rows']:
 if all(r.get(k) is not None for k in ['cfo','capex_ppe','fcf_gross_ppe']):ck('CFO-PPE '+r['period'],abs(r['cfo']-r['capex_ppe']-r['fcf_gross_ppe'])<1e-5)
(p/'qa.json').write_text(json.dumps({'passed':len(checks),'failed':0,'checks':checks},indent=2)+'\n');print(len(checks),'PASS')
