from pathlib import Path
import json
p=Path(__file__).parent;f=json.loads((p/'inputs.json').read_text());v=f['DRI'];o={'DRI':{'revenue_growth':v['revenue']/v['revenue_prior']-1,'ebit_growth':v['ebit']/v['ebit_prior']-1,'margin':v['ebit']/v['revenue'],'cash_less_ppe':v['cfo_continuing']-v['capex'],'prior_cash_less_ppe':v['cfo_prior']-v['capex_prior'],'target_multiple':None},'TXRH':{'q3':None,'next_earnings':f['TXRH']['next_earnings']}}
(p/'outputs.json').write_text(json.dumps(o,indent=2)+'\n')
