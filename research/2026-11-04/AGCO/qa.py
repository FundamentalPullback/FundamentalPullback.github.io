from pathlib import Path
import json
p=Path(__file__).parent;a=json.loads((p/'analysis.json').read_text());f=json.loads((p/'facts/inputs.json').read_text());m=json.loads((p/'publication.json').read_text());h=json.loads((p/'history/history.json').read_text())['rows'];cs=[]
def ck(n,b):cs.append({'check':n,'pass':bool(b)});assert b,n
for k,v in {'q3_ebit_ex_identified_na_ieepa':103.1,'q3_na_ebit_ex_identified_ieepa':.8,'nine_month_cfo_less_ppe':-380.6,'prior_nine_month_cfo_less_ppe':65.2,'nominal_debt_diagnostic':2684.5,'nominal_net_debt_diagnostic':2269.4,'finance_jv_sale_gain_tie':20,'identified_buyback_cash':401.9}.items():ck(k,abs(a[k]-v)<1e-7)
for k in ['bear','base','bull','owner_fcf','equity_bridge']:ck(k+' null',a[k] is None and m[k] is None)
for k in ['latestCompleted','stage35_approved','approved_entry']:ck(k+' false',m[k] is False)
ck('calendar unknown',a['next_earnings_date'] is None)
for r in h:
 ck(r['period']+' FCF identity',abs(r['fcf_ppe_proxy']-(r['cfo']-r['capex_ppe']))<.001)
 ck(r['period']+' software unknown',r['software_capex_separate'] is None)
for k in ['pros_es','cons_es','pros_en','cons_en']:
 for s in m[k]:ck('exact '+s[:25],s in (p/'report.md').read_text())
ck('no placeholder','{HISTORY_TABLE}' not in (p/'report.md').read_text());ck('history QA','PASS' in (p/'history/qa.txt').read_text())
(p/'qa.json').write_text(json.dumps({'passed':len(cs),'failed':0,'checks':cs},indent=2)+'\n');print(len(cs),'PASS')
