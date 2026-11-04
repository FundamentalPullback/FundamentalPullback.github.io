from pathlib import Path
import json
P=Path(__file__).parent
r=json.load(open(P/'sources/peer_inputs.json'))
for name,v in r.items():
 v['market_cap_diluted_proxy']=v['price']*v['shares'];v['ev_ex_operating_leases']=v['market_cap_diluted_proxy']+v['debt_carrying']-v['cash_investments'];v['ttm_sales']=v['annual_sales']+v['h1_sales']-v['prior_h1_sales'];v['ttm_ebit']=v['annual_ebit']+v['h1_ebit']-v['prior_h1_ebit'];v['ttm_ebit_normalized']=v['ttm_ebit']-v['refund_removed']-v['tsa_removed'];v['ev_ebit_normalized']=v['ev_ex_operating_leases']/v['ttm_ebit_normalized'];v['ttm_margin_normalized']=v['ttm_ebit_normalized']/v['ttm_sales'];v['guidance_pe_ex_refund']=v['price']/(v['guide_eps_mid']-v['guide_eps_benefit'])
json.dump(dict(price_date='2026-11-03',period='TTM to 2026-08-01, DG to 2026-07-31',companies=r,limitations=['DLTR uses nominal debt; DG uses disclosed carrying debt, not exactly identical capital measures.','DLTR/FIVE gross operating refunds removed; DG adjustment is NET 66bp estimate after reinvestment, not equivalent gross-only normalization.','Guidance EPS are adjusted, tax and TSA normalization incomplete; not GAAP P/E.','No peer-implied value or group median. Different traffic, product mix, growth, import exposure and leases.']),open(P/'peers.json','w'),indent=2)
print({k:round(v['ev_ebit_normalized'],2) for k,v in r.items()})
