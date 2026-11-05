from pathlib import Path
import json
p=Path(__file__).parent;f=json.loads((p/'inputs.json').read_text());o={'ticker':'WMB','source':f['source'],'cash_less_all_capex':[f['cfo'][i]-f['capex_paid'][i] for i in range(2)],'cash_less_capex_sbc':[f['cfo'][i]-f['capex_paid'][i]-f['sbc'][i] for i in range(2)],'owner_fcf':None,'multiple_target':None,'homogeneous_comps_complete':False}
(p/'outputs.json').write_text(json.dumps(o,indent=2)+'\n')
