from pathlib import Path
import json
p=Path(__file__).parent;f=json.loads((p/'inputs.json').read_text());s=f['SCCO'];b=f['BHP_Copper'];o={'scco_gaap_operating_margin':s['ebit']/s['revenue'],'scco_cfo_less_capital_investment':s['cfo']-s['capital_investment'],'bhp_underlying_ebitda_to_revenue_not_gaap_margin':b['underlying_ebitda']/b['revenue']};(p/'outputs.json').write_text(json.dumps(o,indent=2)+'\n')
