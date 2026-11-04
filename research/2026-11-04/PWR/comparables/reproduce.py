from pathlib import Path
import json
p=Path(__file__).parent;f=json.loads((p/'inputs.json').read_text());o={'q3_margin_reported':f['q3_ebit']/f['q3_revenue'],'q3_margin_ex_impairment':(f['q3_ebit']+f['q3_impairment'])/f['q3_revenue'],'ytd_cfo_less_ppe':f['ytd_cfo']-f['ytd_capex'],'ytd_after_sbc_proxy':f['ytd_cfo']-f['ytd_capex']-f['ytd_sbc'],'owner_fcf':None,'target_multiple':None,'limits':f['limits']};(p/'outputs.json').write_text(json.dumps(o,indent=2)+'\n')
