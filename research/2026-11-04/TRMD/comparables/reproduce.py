from pathlib import Path
import json
p=Path(__file__).parent;f=json.loads((p/'inputs.json').read_text())
a={'tce_growth_pct':100*(f['tce_revenue']/f['tce_revenue_prior']-1),'daily_tce_growth_pct':100*(f['daily_tce']/f['daily_tce_prior']-1),'adjusted_ni_recalculated':f['net_income']-f['vessel_sale_gains']+f['fair_value_loss_financial_liabilities'],'ev_ebit':None,'target_multiple':None,'limitation':'Different fleet composition and vessel sales. Operational context only, not a homogeneous multiple or permanent earning-power comparison.'}
assert abs(a['adjusted_ni_recalculated']-f['issuer_adjusted_net_income'])<.11
(p/'outputs.json').write_text(json.dumps(a,indent=2)+'\n')
