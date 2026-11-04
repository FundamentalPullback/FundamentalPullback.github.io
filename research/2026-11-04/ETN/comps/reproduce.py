"""Offline, standard-library-only limited peer comparison. Run from any directory."""
from pathlib import Path
import json,csv
P=Path(__file__).resolve().parent
x=json.loads((P/'inputs.json').read_text());out={}
for ticker in ('ETN','HUBB'):
 d=x[ticker]
 if ticker=='HUBB':
  periods=d['periods'];t={k:periods['FY2025'][k]+periods['9M2026'][k]-periods['9M2025'][k] for k in ('revenue','operating_income','pretax_income','net_interest_expense')}
  revenue=t['revenue'];oi=t['operating_income'];ebit=t['pretax_income']+t['net_interest_expense']
 else:revenue=d['ttm_revenue'];oi=d['ttm_operating_income'];ebit=d['ttm_ebit_pretax_plus_net_interest']
 equity=d['price']*d['actual_shares'];debt=d['debt_current']+d['debt_noncurrent'];ev=equity+debt-d['cash']-d['short_investments']+d['nci_book']
 out[ticker]={'price':d['price'],'actual_shares':d['actual_shares'],'market_cap':equity,'debt_carrying':debt,'cash_plus_short_investments':d['cash']+d['short_investments'],'nci_book':d['nci_book'],'enterprise_value':ev,'ttm_revenue':revenue,'ttm_operating_income':oi,'ttm_ebit_pretax_plus_net_interest':ebit,'ev_to_revenue':ev/revenue,'ev_to_operating_income':ev/oi,'ev_to_ebit_pretax_plus_net_interest':ev/ebit,'ttm_operating_margin':oi/revenue,'ttm_ebit_margin':ebit/revenue,'q3_operating_margin':d['q3_operating_income']/d['q3_revenue']}
 assert ev>equity and revenue>0 and ebit>0
out['ABB']={'q3_revenue':x['ABB']['q3_revenue'],'q3_operating_margin':x['ABB']['q3_income_from_operations']/x['ABB']['q3_revenue'],'q3_operational_ebita_margin':x['ABB']['q3_operational_ebita_margin_pct']/100,'market_multiple':None}
(P/'results.json').write_text(json.dumps(out,indent=2)+'\n')
with (P/'results.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=['ticker']+list(out['ETN']));w.writeheader();w.writerows({'ticker':k,**out[k]} for k in ('ETN','HUBB'))
print(json.dumps(out,indent=2))
