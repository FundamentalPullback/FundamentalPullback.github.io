from pathlib import Path
import json
p=Path(__file__).parent;x=json.loads((p/'inputs.json').read_text());o=[]
for r in x:
 r['margin_reported_pct']=100*r['ebit']/r['revenue'];r['ebit_ex_specific_items']=r['ebit']-r['refund_ebit'];r['margin_ex_specific_items_pct']=100*r['ebit_ex_specific_items']/r['revenue'];r['prior_ebit_ex_specific_items']=r['prior_ebit']-r['prior_nonrecurring_operating_gain'];r['sales_growth_pct']=100*(r['revenue']/r['prior_revenue']-1);o.append(r)
(p/'outputs.json').write_text(json.dumps(o,indent=2)+'\n')
