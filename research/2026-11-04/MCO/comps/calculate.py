import json,csv
from pathlib import Path
p=Path(__file__).parent
d=json.loads((p/'inputs.json').read_text());out=[];rows=[]
for c in d['companies']:
 r={k:c[k] for k in ['ticker','price','shares','shares_date','share_basis','balance_date','debt_nominal','debt_carrying','cash_reported','restricted_cash','nci','notes']}
 for period in ['FY2025','9M2025','9M2026']:
  for metric,value in c[period].items():rows.append({'ticker':c['ticker'],'period':period,'metric':metric,'value':value,'units':d['units'],'source':d['sources'].get(c['ticker'].lower()+('_fy25' if period=='FY2025' else '_q3')) if not (c['ticker']=='SPGI' and period=='FY2025') else d['sources']['spgi_recast']})
 for metric in ['revenue','ebit','cfo','physical_capex','software_capex','sbc','gain_dispositions']:
  v=[c[t].get(metric) for t in ['FY2025','9M2026','9M2025']];r['ttm_'+metric]=v[0]+v[1]-v[2] if all(x is not None for x in v) else None
 r['equity_value']=c['price']*c['shares'];r['unrestricted_cash']=c['cash_reported']-c['restricted_cash'];r['ev_debt_basis']='nominal' if c['debt_nominal'] is not None else 'carrying proxy, nominal not reconciled';r['net_debt']=(c['debt_nominal'] if c['debt_nominal'] is not None else c['debt_carrying'])-r['unrestricted_cash'];r['ev']=r['equity_value']+r['net_debt']+c['nci']+c['preferred'];r['ev_ebit']=r['ev']/r['ttm_ebit'];r['ev_revenue']=r['ev']/r['ttm_revenue'];r['ebit_margin']=r['ttm_ebit']/r['ttm_revenue']
 r['owner_fcf']=None;r['owner_fcf_yield']=None
 if c['ticker']=='MSCI':
  r['ttm_capex_total']=r['ttm_physical_capex']+r['ttm_software_capex'];r['fcf']=r['ttm_cfo']-r['ttm_capex_total'];r['owner_fcf']=r['fcf']-r['ttm_sbc'];r['owner_fcf_yield']=r['owner_fcf']/r['equity_value']
 else:
  r['ttm_ebit_less_disposition_gains']=r['ttm_ebit']-r['ttm_gain_dispositions'];r['ev_ebit_less_disposition_gains']=r['ev']/r['ttm_ebit_less_disposition_gains'];y=c['9M2026'];r['9m_owner_cash_not_annualized']=y['cfo']-y['capex_total']-y['sbc']-y['nci_cash_distributions']
 for metric in ['price','shares','debt_nominal','debt_carrying','cash_reported','restricted_cash','nci']:
  rows.append({'ticker':c['ticker'],'period':d['price_date'] if metric=='price' else c['shares_date'] if metric=='shares' else c['balance_date'],'metric':metric,'value':c[metric],'units':d['units'],'source':d['sources'][c['ticker'].lower()+('_price' if metric=='price' else '_q3')]})
 out.append(r)
(p/'results.json').write_text(json.dumps({'as_of':d['as_of'],'price_date':d['price_date'],'units':d['units'],'peers':out},indent=2))
with (p/'numeric_rows.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=['ticker','period','metric','value','units','source']);w.writeheader();w.writerows(rows)
print(json.dumps(out,indent=2))
