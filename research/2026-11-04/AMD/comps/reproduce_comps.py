"""Portable stdlib-only operating comparisons, not valuations or forecasts."""
import json,csv
from pathlib import Path
p=Path(__file__).resolve().parent
s=json.loads((p/'source_numeric_subset.json').read_text());r=s['records']
for v in r:
 v['fcf']=v['cfo']-v['capex_cash']-v['principal_ppe_intangibles']
 assert v['fcf']==v['reported_fcf']
 v['fcf_less_sbc']=v['fcf']-v['sbc']
 for k in ['gaap_ebit','cfo','fcf','fcf_less_sbc','sbc']:
  v[k+'_pct_revenue']=100*v[k]/v['revenue']
(p/'operating_comps.json').write_text(json.dumps({'units':s['units'],'as_of':s['as_of'],'records':r,'segment_context':s['segment_context']},indent=2)+'\n')
with (p/'operating_comps.csv').open('w') as f:
 fields=list(dict.fromkeys(k for v in r for k in v));w=csv.DictWriter(f,fields);w.writeheader();w.writerows(r)
for v in r:
 if v['months']==3: print(v['issuer'],v['period'],v['gaap_ebit_pct_revenue'],v['fcf_pct_revenue'],v['fcf_less_sbc'])
