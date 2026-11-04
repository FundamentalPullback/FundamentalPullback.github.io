from pathlib import Path
import json
p=Path(__file__).parent;f=json.loads((p/'inputs.json').read_text());o={}
for t in ['ETN','HUBB']:
 x=f[t]
 if t=='HUBB':
  ps=x['periods'];rev=ps['FY2025']['revenue']-ps['9M2025']['revenue']+ps['9M2026']['revenue'];ebit=ps['FY2025']['operating_income']-ps['9M2025']['operating_income']+ps['9M2026']['operating_income']
 else:rev=x['ttm_revenue'];ebit=x['ttm_operating_income']
 ev=x['price']*x['actual_shares']+x['debt_current']+x['debt_noncurrent']-x['cash']-x['short_investments']+x['nci_book']
 o[t]={'price_date':'2026-11-03','price':x['price'],'ttm_revenue':rev,'ttm_operating_income':ebit,'ttm_operating_margin':ebit/rev,'ev_to_operating_income_proxy':ev/ebit,'q3_gaap_margin':x['q3_operating_income']/x['q3_revenue']}
o['ABB']={'q3_revenue':f['ABB']['q3_revenue'],'q3_gaap_margin':f['ABB']['q3_income_from_operations']/f['ABB']['q3_revenue'],'q3_comparable_growth_pct':f['ABB']['q3_comparable_revenue_growth_pct'],'market_multiple':None}
(p/'results.json').write_text(json.dumps(o,indent=2)+'\n');print(o)
