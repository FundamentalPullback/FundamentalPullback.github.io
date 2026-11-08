import json, subprocess,sys
from pathlib import Path
p=Path(__file__).parent
subprocess.run([sys.executable,str(p/'model.py')],check=True,stdout=subprocess.DEVNULL)
r=json.loads((p/'results.json').read_text());h=r['history'];checks={}
for k in ['sales','ebit','net','da','cfo','capex','sbc','interest','fcf']:
 checks['quarter_sum_'+k]=abs(sum(h[q][k] for q in ['Q3_2025','Q4_2025','Q1_2026','Q2_2026'])-h['TTM'][k])<1e-8
for k,v in r['scenarios'].items():
 checks[k+'_ten_years']=len(v['forecast'])==10
 checks[k+'_fcff']=all(abs(x['fcff']-(x['nopat']+x['da']-x['capex']-x['delta_wc']))<1e-7 for x in v['forecast'])
 checks[k+'_terminal_physical']=abs(v['terminal_fcff']-(v['terminal_nopat']+v['terminal_da']-v['terminal_capex']-v['terminal_delta_wc']))<1e-7
 checks[k+'_bridge']=abs(v['equity']-(v['ev']-52896+85))<1e-7
 checks[k+'_wacc_gt_g']=v['assumptions']['wacc']>v['assumptions']['g']
 checks[k+'_positive_capex']=all(x['capex']>0 for x in v['forecast'])
checks['scenario_order']=r['scenarios']['adverso']['per_share']<r['scenarios']['central']['per_share']<r['scenarios']['favorable']['per_share']
checks['price_distinct_from_scanner']=r['regular_close']['price']!=r['regular_close']['scanner_last']
checks['debt_includes_finance_leases_once']=r['bridge']['debt']==52896
checks['normalized_refund_once']=r['normalized_ttm_ebit']==h['TTM']['ebit']-685
checks['prior_ttm_week_difference_disclosed']=r['matched_history']['prior_ttm_weeks']==53 and r['matched_history']['current_ttm_weeks']==52
checks['cash_refund_inventory_timing']=abs(r['cfo_reconciliation']['fcff_proxy_after_refund_inventory_timing']-(r['cfo_reconciliation']['fcff_cfo_proxy']-45))<1e-8
checks['erp_snapshot_date']=r['cost_of_capital']['erp_date']=='2026-11-01'
for k,v in r['scenarios'].items():
 checks[k+'_terminal_reinvestment']=abs(v['terminal_reinvestment']-v['terminal_nopat']*v['assumptions']['g']/v['assumptions']['terminal_roic'])<1e-7
 checks[k+'_pv_ev']=abs(v['ev']-sum(x['pv'] for x in v['forecast'])-v['pv_terminal'])<1e-7
out=dict(passed=all(checks.values()),checks=checks,external_audit='completed: see audit.json; mechanical checks do not certify assumptions');(p/'validation.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2));assert out['passed']
