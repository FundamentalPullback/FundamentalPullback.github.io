from pathlib import Path
import json
p=Path(__file__).parent;f=json.loads((p/'facts/inputs.json').read_text());a=json.loads((p/'analysis.json').read_text());m=json.loads((p/'publication.json').read_text());h=json.loads((p/'history/history.json').read_text());checks=[]
def ck(n,b):checks.append({'check':n,'pass':bool(b)});assert b,n
for k,v in {'cfo_less_ppe_software':-13.590,'cash_proxy_after_sbc':-53.617,'debt_increase':304.,'nominal_debt_less_cash_only':789.382,'cash_receivables_unbilled':-90.255,'derivatives_net':4.109,'limited_ebit_ex_earnout_9m':158.251,'limited_ebit_ex_earnout_prior':128.315,'price_difference':.715}.items():ck(k,abs(a[k]-v)<1e-7)
ck('earnout reconciliation',abs(f['earnout_prior']+f['earnout_acquisition']-f['earnout_payments']+f['earnout_remeasurement']+f['earnout_fx']-f['earnout'])<1e-7)
ck('debt reconciliation',abs(f['revolver']+f['termloan']-f['debt_issuance']-f['debt_carrying'])<1e-7)
ck('shorelight reconciliation',abs(f['shorelight_prior']-f['shorelight_oci_loss']-f['shorelight_pnl_loss']-f['shorelight_fv'])<1e-7)
ck('RPO reconciliation',abs(f['rpo2026']+f['rpo2027']+f['rpo_later']-f['rpo'])<1e-7)
for k in ['bear','base','bull','buy_ceiling','owner_fcf','equity_bridge']:ck(k+' null',a[k] is None and m[k] is None)
for k in ['approved_entry','stage35_approved','latestCompleted']:ck(k+' false',m[k] is False)
ck('no certified close',a['certified_close'] is None);ck('next date unknown',a['next_earnings_date'] is None)
for k in ['pros_es','cons_es','pros_en','cons_en']:
 ck(k+' count',len(m[k])==3)
 for s in m[k]:ck('exact '+s[:30],s in (p/'report.md').read_text())
ck('no placeholder','{HISTORY_TABLE}' not in (p/'report.md').read_text())
for r in h['rows']:
 if r.get('revenue_gaap') is not None and r.get('revenue_rbr') is not None and r.get('reimbursable_revenue') is not None:ck('revenue '+r['period'],abs(r['revenue_gaap']-r['revenue_rbr']-r['reimbursable_revenue'])<1e-5)
(p/'qa.json').write_text(json.dumps({'passed':len(checks),'failed':0,'checks':checks},indent=2)+'\n');print(len(checks),'PASS')
