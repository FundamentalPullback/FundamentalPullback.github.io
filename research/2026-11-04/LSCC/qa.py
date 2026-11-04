from pathlib import Path
import json
p=Path(__file__).parent;a=json.loads((p/'analysis.json').read_text());f=json.loads((p/'facts/inputs.json').read_text());m=json.loads((p/'publication.json').read_text());h=json.loads((p/'history/normalized_history.json').read_text());cs=[]
def ck(n,b):cs.append({'check':n,'pass':bool(b)});assert b,n
for k,v in {'purchase_price_tie':1589.664,'acquisition_cash_net':971.346,'q3_unallocated_segment_cost':89.559,'nominal_net_debt_oct3':746.723,'nine_month_after_software':163.479,'nine_month_after_software_sbc':40.715}.items():ck(k,abs(a[k]-v)<1e-8)
ck('debt principal reconciliation',abs(f['debt_carrying']+f['debt_costs']-f['debt_principal'])<1e-8)
ck('term paydown',f['term_draw']-f['term_prepayment']==f['debt_principal'])
for k in ['bear','base','bull','owner_fcf','equity_bridge']:ck(k+' null',a[k] is None and m[k] is None)
for k in ['latestCompleted','stage35_approved','approved_entry']:ck(k+' false',m[k] is False)
ck('calendar unknown',a['next_earnings_date'] is None)
ck('53 week TTM',h['periods']['TTMQ3FY2026']['weeks']==53)
ck('TTM software cash',abs(h['periods']['TTMQ3FY2026']['metrics']['software_ip_cash']['value']/1e6-42.716)<1e-8)
ck('history controls',all(x['passed'] for x in json.loads((p/'history/qa.json').read_text())))
for k in ['pros_es','cons_es','pros_en','cons_en']:
 for s in m[k]:ck('exact '+s[:25],s in (p/'report.md').read_text())
ck('no placeholder','{HISTORY_TABLE}' not in (p/'report.md').read_text())
ck('scanner kept',m['scanner_price']==126.05 and m['price']==107.25)
(p/'qa.json').write_text(json.dumps({'passed':len(cs),'failed':0,'checks':cs},indent=2)+'\n');print(len(cs),'PASS')
