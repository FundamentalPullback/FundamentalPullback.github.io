from pathlib import Path
import json
p=Path(__file__).parent;a=json.loads((p/'analysis.json').read_text());m=json.loads((p/'publication.json').read_text());h=json.loads((p/'history/history.json').read_text())['periods'];cs=[]
def ck(n,b):cs.append({'check':n,'pass':bool(b)});assert b,n
for k,v in {'nine_month_cfo_less_capex':2288,'nine_month_less_insurance_cash_diagnostic':1589,'nine_month_less_insurance_nci_leases_sbc_diagnostic':801,'consolidated_net_debt_carrying':5063,'policy_net_debt_ex_downstream':1826,'environmental_aro_total':5983,'bagdad_2027_spend_estimate':900,'bagdad_2028_spend_low':1350,'bagdad_2028_spend_high':1575}.items():ck(k,abs(a[k]-v)<1e-7)
for k in ['bear','base','bull','owner_fcf','equity_bridge']:ck(k+' null',a[k] is None and m[k] is None)
for k in ['latestCompleted','stage35_approved','approved_entry']:ck(k+' false',m[k] is False)
ck('calendar unknown',a['next_earnings_date'] is None)
for r in h:
 if r.get('cfo') is not None and r.get('capex') is not None:ck(r['period']+' cash identity',abs(r['fcf_consolidated']-(r['cfo']-r['capex']))<.001)
 if r.get('net_income_consolidated') is not None and r.get('net_income_attributable') is not None and r.get('nci_income') is not None:ck(r['period']+' NI perimeter',abs(r['net_income_consolidated']-r['net_income_attributable']-r['nci_income'])<.001)
for k in ['pros_es','cons_es','pros_en','cons_en']:
 for s in m[k]:ck('exact '+s[:25],s in (p/'report.md').read_text())
ck('history QA','PASS' in (p/'history/qa.txt').read_text());ck('no placeholder','{HISTORY_TABLE}' not in (p/'report.md').read_text())
(p/'qa.json').write_text(json.dumps({'passed':len(cs),'failed':0,'checks':cs},indent=2)+'\n');print(len(cs),'PASS')
