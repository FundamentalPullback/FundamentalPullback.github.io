import json,subprocess,sys
from pathlib import Path
p=Path(__file__).resolve().parent
subprocess.run([sys.executable,str(p/'model.py')],check=True,stdout=subprocess.DEVNULL)
r=json.loads((p/'results.json').read_text());checks={}
h=r['historical'];qs=['Q32025','Q42025','Q12026','Q22026']
for k in ['sales','ebit','net_income','cfo','capex','da','sbc']:
 checks['four_quarters_equal_ttm_'+k]=abs(sum(h[q][k] for q in qs)-h['TTM2026'][k])<1e-8
checks['refund_operating']=abs(h['TTM2026']['normalized_ebit']-314.237)<1e-8
for name,v in r['scenarios'].items():
 checks[name+'_ten_years']=len(v['rows'])==10
 checks[name+'_fcff_tie']=all(abs(x['fcff']-(x['nopat']+x['da']-x['capex']-x['dNWC']-x['dOperatingCash']))<1e-8 for x in v['rows'])
 checks[name+'_nonnegative_growth_capex']=all(x['growth_capex']>=0 for x in v['rows'])
 t=v['terminal_physical'];checks[name+'_terminal_physical']=abs(v['terminal_fcff']-(v['terminal_nopat']+t['da']-t['capex']-t['dNWC']-t['dOperatingCash']))<1e-8
 checks[name+'_bridge']=abs(v['value_per_share']-(v['ev']+v['net_bridge'])/v['shares'])<1e-8
 checks[name+'_valid_wacc_g']=v['assumptions']['wacc']>v['assumptions']['g']
checks['case_order']=r['scenarios']['adverso']['value_per_share']<r['scenarios']['central']['value_per_share']<r['scenarios']['favorable']['value_per_share']
checks['no_operating_lease_double_deduction']=abs(r['scenarios']['central']['net_bridge']-416.830)<1e-8
checks['research_no_entry']=json.loads((p/'status.json').read_text())['entryApproved']==False
checks['cash_policy_5pct_below_opening_only']=r['bounded_proxies']['cash_buffer_5pct']<r['bounded_proxies']['opening_cash_buffer_5pct_only']
checks['capm_tie']=abs(r['capital_cost']['capm']+r['capital_cost']['execution_premium']-r['capital_cost']['central_wacc'])<1e-10
checks['calibration_gate_not_approved']=r['canonical_valuation_approved']==False and json.loads((p/'status.json').read_text())['stage3Complete']==False
checks['ttm_eps_quarter_rounding_tolerance']=abs(sum(h[q]['eps'] for q in qs)-h['TTM2026']['eps'])<=.01000001
for n,v in r['scenarios'].items():
 checks[n+'_terminal_positive_capex']=v['terminal_physical']['capex']>v['terminal_physical']['da']
 checks[n+'_terminal_reinvestment']=abs(v['terminal_reinvestment']-v['terminal_nopat']*v['assumptions']['g']/v['assumptions']['roic'])<1e-8
 checks[n+'_pv_tie']=abs(v['ev']-sum(x['pv_fcff'] for x in v['rows'])-v['pv_terminal'])<1e-8
out={'mechanical_only_not_independent_audit':True,'passed':all(checks.values()),'checks':checks}
(p/'audit_checks.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2));assert all(checks.values())
