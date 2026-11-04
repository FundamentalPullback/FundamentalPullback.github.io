from pathlib import Path
import json
p=Path(__file__).parent;f=json.loads((p/'inputs.json').read_text());o={k:{'reported_margin':v['ebit']/v['revenue'],'target_multiple':None,'owner_fcf':None,'limits':v['limits']} for k,v in f.items()};o['PLUG']['ebit_ex_recovery_limited']=f['PLUG']['ebit']-f['PLUG']['recoveries_of_previously_impaired_assets_rounded'];(p/'outputs.json').write_text(json.dumps(o,indent=2)+'\n')
