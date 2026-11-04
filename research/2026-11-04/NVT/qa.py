from pathlib import Path
import json,math
p=Path(__file__).parent;a=json.loads((p/'analysis.json').read_text());f=json.loads((p/'facts/capital_events.json').read_text());m=json.loads((p/'publication.json').read_text());h=json.loads((p/'history/history.json').read_text())['rows'];cs=[]
def check(n,b):cs.append({'check':n,'pass':bool(b)});assert b,n
check('Debt nominal vs carrying',abs(f['debt_carrying']+f['debt_costs_discount']-f['debt_nominal'])<1e-8)
check('September prefunding not duplicated',abs(a['post_draw_debt_before_other_movements']-3046.6)<1e-8)
check('Mechanical cash only',abs(a['mechanical_cash_after_draw_and_price_before_other_movements']-221.8)<1e-8)
check('Mechanical net debt',abs(a['mechanical_net_debt_before_other_movements']-2824.8)<1e-8)
check('IEEPA net excluded once',abs(a['nine_month_ebit_without_net_ieepa_benefit']-756.5)<1e-8)
for k in ['bear','base','bull','owner_fcf','equity_bridge']:check(k+' unknown',a[k] is None and m[k] is None)
for k in ['latestCompleted','stage35_approved','approved_entry']:check(k+' false',m[k] is False)
check('calendar unknown',a['next_earnings_date'] is None)
check('Reported price distinct from scanner',m['price']!=m['scanner_price'])
for r in h:
 if r.get('cfo_continuing') is not None and r.get('capex_ppe_continuing') is not None:check(r['period']+' FCF identity',abs(r['fcf_continuing_strict']-(r['cfo_continuing']-r['capex_ppe_continuing']))<0.001)
for k in ['pros_es','cons_es','pros_en','cons_en']:
 for s in m[k]:check('Exact evidence '+s[:25],s in (p/'report.md').read_text())
check('No unexpanded templates','{HISTORY_TABLE}' not in (p/'report.md').read_text())
check('History audit passes',json.loads((p/'history/qa.json').read_text())['status']=='PASS')
(p/'qa.json').write_text(json.dumps({'passed':len(cs),'failed':0,'checks':cs},indent=2)+'\n');print(len(cs),'PASS')
