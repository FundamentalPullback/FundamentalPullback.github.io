import json,pathlib
p=pathlib.Path(__file__).parent;x=json.loads((p/'inputs.json').read_text());o={}
for k in ['WDC','NTAP']:
 a=x[k];o[k]={'ebit_margin':a['ebit']/a['revenue'],'fcf':a['cfo']-a['capex'],'fcf_less_sbc_sensitivity':a['cfo']-a['capex']-a['sbc']}
o['WDC']['revenue_growth']=x['WDC']['revenue']/x['WDC']['prior_revenue']-1
(p/'outputs.json').write_text(json.dumps(o,indent=2)+'\n')
