from pathlib import Path
import json
p=Path(__file__).parent;f=json.loads((p/'inputs.json').read_text());d=f['DE'];c=f['CNH'];o={'de_precision_sales_growth':d['sales_production_precision']/d['prior_sales']-1,'de_precision_segment_margin':d['segment_operating_profit']/d['sales_production_precision'],'cnh_industrial_adjusted_margin_not_gaap':c['industrial_adjusted_ebit']/c['industrial_sales']};(p/'outputs.json').write_text(json.dumps(o,indent=2)+'\n')
