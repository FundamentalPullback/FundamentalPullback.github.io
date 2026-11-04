from pathlib import Path
import json
p=Path(__file__).parent;f=json.loads((p/'inputs.json').read_text())
a={'q3_operating_margin':f['q3_ebit']/f['q3_revenue'],'q3_prior_operating_margin':f['q3_ebit_prior']/f['q3_revenue_prior'],'nine_months_cfo_less_capex':f['nine_months_cfo']-f['nine_months_capex'],'nine_months_prior_cfo_less_capex':f['nine_months_cfo_prior']-f['nine_months_capex_prior'],'valuation_multiple':None,'limitation':'Operating context only; pension treatment, program mix, contract cash and impairments are not normalized to one homogeneous EV/EBIT basis.'}
(p/'outputs.json').write_text(json.dumps(a,indent=2)+'\n')
