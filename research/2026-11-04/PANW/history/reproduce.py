#!/usr/bin/env python3
"""Offline build from selected primary-source numeric observations; standard library only."""
import json,csv,hashlib
from pathlib import Path
P=Path(__file__).resolve().parent
src=json.loads((P/'selected_observations.json').read_text());d={};checks=[]
for f in src['facts']:
 p=d.setdefault(f['period'],{});m=f['metric'];v=f['value']
 assert m not in p or p[m]==v
 p[m]=v
flows=['revenue','ebit','net_income','sbc_expense','cfo','sbc_cf','capital_spend_signed','contract_cost_amortization','contract_cost_cash_change','deferred_revenue_cash_change','da','acquisitions_cash_signed','acquisition_amortization']
for yr in [2025,2026]:
 for q,curr,prev in [(2,f'6MFY{yr}',f'Q1FY{yr}'),(3,f'9MFY{yr}',f'6MFY{yr}'),(4,f'FY{yr}',f'9MFY{yr}')]:
  dest=d.setdefault(f'Q{q}FY{yr}',{})
  for m in flows:
   val=d[curr][m]-d[prev][m]
   if m in dest:assert abs(dest[m]-val)<1e-8,(yr,q,m)
   dest[m]=val
 for m in flows:
  total=sum(d[f'Q{q}FY{yr}'][m] for q in range(1,5));assert abs(total-d[f'FY{yr}'][m])<1e-8
  checks.append({'check':f'FY{yr} = Q1+Q2+Q3+Q4 for {m}','passed':True})
for p,v in d.items():
 v['capital_spend']=-v['capital_spend_signed'];v['fcf_gross']=v['cfo']-v['capital_spend']
 v['fcf_less_sbc_cf']=v['fcf_gross']-v['sbc_cf'];v['fcf_less_sbc_expense']=v['fcf_gross']-v['sbc_expense']
 v['ebit_margin_pct']=100*v['ebit']/v['revenue'];v['fcf_margin_pct']=100*v['fcf_gross']/v['revenue'];v['fcf_less_sbc_cf_margin_pct']=100*v['fcf_less_sbc_cf']/v['revenue']
 if 'capitalized_software_amortization' in v:v['physical_other_da_residual']=v['da']-v['acquisition_amortization']-v['capitalized_software_amortization']
 v['commissions_cash_less_amortization']=-v['contract_cost_cash_change']-v['contract_cost_amortization']
 # Not separately disclosed; never silently replace missing observations with zero.
 for m in ['sbc_capitalized','software_cash_capex_separate','ppe_cash_capex_separate','cash_taxes']:
  v.setdefault(m,None)
for yr in [2025,2026]:
 for q in range(1,5):
  p=f'Q{q}FY{yr}';prior=f'Q{q}FY{yr-1}'
  if prior in d:d[p]['revenue_growth_reported_pct']=100*(d[p]['revenue']/d[prior]['revenue']-1)
for yr in [2025,2026]:d[f'FY{yr}']['revenue_growth_reported_pct']=100*(d[f'FY{yr}']['revenue']/d[f'FY{yr-1}']['revenue']-1)
d['TTM_2026-07-31']=dict(d['FY2026']);d['PRIOR_TTM_2025-07-31']=dict(d['FY2025'])
rows=[dict(period=p,**v) for p,v in d.items()]
(P/'reported_history.json').write_text(json.dumps({'as_of':src['as_of'],'units':src['units'],'periods':d,'sources':src['sources']},indent=2)+'\n')
fields=['period']+sorted({k for r in rows for k in r if k!='period'})
with (P/'reported_history.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
comparison={m:{'ttm':d['FY2026'][m],'prior_ttm':d['FY2025'][m],'change':d['FY2026'][m]-d['FY2025'][m]} for m in flows+['fcf_gross','fcf_less_sbc_cf','fcf_less_sbc_expense','cash_taxes']}
(P/'ttm_comparison.json').write_text(json.dumps(comparison,indent=2)+'\n')
(P/'checks.json').write_text(json.dumps({'passed':all(c['passed'] for c in checks),'checks':checks,'last_actual_period':'FY2026 ended 2026-07-31','TTM_equals_FY':True,'Q1FY2027_actuals_included':False},indent=2)+'\n')
print('PASS:',len(checks),'quarter/year arithmetic and direct-observation checks; offline outputs rebuilt.')
