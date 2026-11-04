from pathlib import Path
import json
p=Path(__file__).parent
x=json.loads((p/'inputs.json').read_text());o=[]
for r in x:
 a=dict(r);a['margin_pct']=r['ebit']/r['revenue']*100;a['sales_yoy_pct']=(r['revenue']/r['prior_revenue']-1)*100;a['cfo_less_capex']=r['cfo']-r['capex'];o.append(a)
(p/'outputs.json').write_text(json.dumps(o,indent=2)+'\n')
