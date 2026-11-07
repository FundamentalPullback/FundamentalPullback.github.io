"""Supplemental model and source consistency checks; no third-party original material."""
import model,json
from pathlib import Path
p=Path(__file__).parent
h=model.d;t=h['TTM_20260930']
checks={
'TTM_sales_FY25_plus9M26_less9M25':abs(t['sales']-(916.663+660.536-695.957))<1e-9,
'TTM_ebit_FY25_plus9M26_less9M25':abs(t['ebit']-(183.421+122.290-140.372))<1e-9,
'TTM_netincome_rollforward':abs(t['net_income']-(141.634+92.958-108.059))<1e-9,
'TTM_CFO_rollforward':abs(t['cfo']-(183.698+103.878-128.897))<1e-9,
'TTM_DA_rollforward':abs(t['da']-(34.584+29.101-25.784))<1e-9,
'TTM_SBC_rollforward':abs(t['sbc']-(9.190+7.821-6.445))<1e-9,
'TTM_PPE_rollforward':abs(t['capex']-(14.026+12.258-9.993))<1e-9,
'YTD_cash_bridge':abs(226.016+103.878-12.258+.454-94.375-35.936+.140-119.014-.977-67.928)<1e-9}
assert all(checks.values())
s=[]
orig=model.cases['central'].copy()
for ri in [.15,.20,.25,.30]:
 for terminal in [.15,.18,.25]:
  model.cases['central']['roic']=ri;model.cases['central']['terminal_roic']=terminal
  v,_=model.run('central');s.append(dict(growth_roic=ri,terminal_roic=terminal,price=v['price']))
model.cases['central']=orig
v,_=model.run('central')
bridges={
 'baseline':v['price'],
 'no_employee_claim_reserve':v['price']+9.343/model.shares,
 'no_excess_cash_credit':v['price']-37.928/model.shares,
 'full_50m_earnout':v['price']-38/model.shares,
 'all_cash_excess':v['price']+30/model.shares,
 'q3_weighted_diluted_denominator':(v['ev']+model.netbridge)/28.871187}
res={'checks':checks,'incremental_return_sensitivity':s,'capital_and_share_sensitivity':bridges,'status':'research-ready for independent review; NOT a completed Stage3 approval'}
(p/'verification.json').write_text(json.dumps(res,indent=2));print(json.dumps(res,indent=2))
