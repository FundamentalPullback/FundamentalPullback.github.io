from pathlib import Path
import json
p=Path(__file__).parent
f=json.loads((p/'inputs.json').read_text());o={}
for t,v in f.items():
 o[t]={'quarter_margin':v['quarter_ebit']/v['quarter_revenue'] if v.get('quarter_ebit') is not None else v['quarter_reported_margin'],'cash_proxy':v['cfo']-v['capex'],'cash_period':v['cash_period'],'valuation_multiple':None,'limitation':v['limitation']}
(p/'outputs.json').write_text(json.dumps(o,indent=2)+'\n')
