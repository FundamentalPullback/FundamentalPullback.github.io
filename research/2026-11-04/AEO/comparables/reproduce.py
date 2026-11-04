from pathlib import Path
import json
p=Path(__file__).parent;a=[]
for f in json.loads((p/'inputs.json').read_text()):
 r={'ticker':f['ticker'],'ebit_ex_refund':f['ebit']-f['refund_ebit'],'prior_ebit_ex_identified_gain':f['prior_ebit']-f['prior_nonrecurring_operating_gain'],'source':f['source'],'target_multiple':None,'limitation':'Limited Q2 operating bridge; brand mix, lease accounting, scope and other normalization remain different.'};r['limited_change_pct']=100*(r['ebit_ex_refund']/r['prior_ebit_ex_identified_gain']-1);a.append(r)
(p/'outputs.json').write_text(json.dumps(a,indent=2)+'\n')
