"""Reproduce peers.json and peers.csv with the standard library only. No network."""
import json,csv
from pathlib import Path
P=Path(__file__).resolve().parent
x=json.loads((P/'peers_inputs.json').read_text()); rows=[]
for ticker in ['RHI','MAN','EFOR','KFY']:
 a=x[ticker]; rev=a.get('revenue');ebit=a.get('ebit_gaap')
 if rev is None: rev=a['fy_revenue']+a['current_ytd_revenue']-a['prior_ytd_revenue']
 if ebit is None: ebit=a['fy_ebit']+a['current_ytd_ebit']-a['prior_ytd_ebit']
 market=a['price']*a['shares'];ev=market+a['debt']+a['nci']-a['cash'];comparison=a.get('ebit_comparison',ebit)
 r=dict(ticker=ticker,price_date=x['price_date'],price=a['price'],ttm_end=a['ttm_end'],shares=a['shares'],market_cap=market,cash=a['cash'],debt=a['debt'],nci=a['nci'],enterprise_value=ev,revenue=rev,ebit_gaap=ebit,ebit_comparison=comparison,margin_gaap_pct=ebit/rev*100,margin_comparison_pct=comparison/rev*100,ev_sales=ev/rev,ev_ebit_gaap=ev/ebit,ev_ebit_comparison=ev/comparison,status='historical_operating_contrast_not_current_comparable' if ticker=='KFY' else 'current_price_latest_reported_balance_TTM')
 if ticker=='MAN':
  r['ttm_impairment']=a['fy_impairment']+a['current_ytd_impairment']-a['prior_ytd_impairment'];assert abs(r['ttm_impairment'])<1e-6
  r['ttm_restructuring_retained']=a['fy_restructuring']+a['current_ytd_restructuring']-a['prior_ytd_restructuring']
 if ticker=='RHI':r['owner_fcf_yield_pct']=a['owner_fcf']/market*100
 if ticker=='KFY':
  r['fee_revenue']=a['fy_fee_revenue']+a['current_ytd_fee_revenue']-a['prior_ytd_fee_revenue']
  r['gross_plan_assets_excluded']=a['marketable_securities']+a['coli_net']
  r['partial_balance_surplus_not_free_cash']=r['gross_plan_assets_excluded']-a['plan_obligations_noncurrent']
  r['ev_if_partial_surplus_credited_sensitivity_only']=ev-r['partial_balance_surplus_not_free_cash']
  r['ev_if_plan_assets_haircut_10pct_sensitivity_only']=ev+max(0,a['plan_obligations_noncurrent']-.9*r['gross_plan_assets_excluded'])
  r['post_ams_bridge_ev_illustrative_not_current']=a['price']*(a['shares']+a['post_ams_new_shares'])+a['post_ams_principal']+a['nci']-(a['cash']-a['post_ams_cash_use_approx'])
  r['post_ams_ev_ebit']=None # No post-transaction operating denominator: do not manufacture a comp.
 rows.append({k:round(v,6) if isinstance(v,float) else v for k,v in r.items()})
assert round(rows[0]['ebit_gaap'],3)==71.911
assert round(rows[1]['ebit_gaap'],1)==303.2
assert round(rows[2]['revenue'],1)==3986.8
assert round(rows[3]['ebit_gaap'],3)==384.675
out={'as_of':x['as_of'],'units':x['units'],'lease_convention':'Operating leases excluded from EV debt; operating lease expense retained in EBIT. No EBITDA substitution.','rows':rows,'input_file':'peers_inputs.json','price_sources':{t:f'https://stockanalysis.com/stocks/{t.lower()}/history/' for t in ['RHI','MAN','EFOR','KFY']}}
(P/'peers.json').write_text(json.dumps(out,indent=2)+'\n')
keys=list(dict.fromkeys(k for r in rows for k in r))
with (P/'peers.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=keys);w.writeheader();w.writerows(rows)
for r in rows:print(r['ticker'],r['enterprise_value'],r['revenue'],r['ebit_comparison'],r['ev_sales'],r['ev_ebit_comparison'],r['status'])
print('Assertions passed.')
