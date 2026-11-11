from pathlib import Path
import json,hashlib
B=Path(__file__).resolve().parent
p=B/'legacy_scenario_extract.json';x=json.loads(p.read_text());quote=50.65
out={'method':'Frozen November4 scenario outputs, not a new valuation. Comparison only; no updated FX, capital, discount rates or Q3 actuals.','quote':{'date':'2026-11-10','time':'16:00 EST','regular_close':quote,'source':'https://stockanalysis.com/stocks/htht/history/'},'price_change_since_prior':quote/48.91-1,'scenarios':{}}
for name,v in x.items():
 assert abs(v['equity']/(v['parameters']['share']*v['fx'])-v['price'])<1e-9
 assert abs(v['enterprise']+v['net_nonoperating_assets']-v['equity'])<1e-9
 out['scenarios'][name]={'dated_value':v['price'],'value_to_current_price':v['price']/quote-1,'date':'2026-11-04','fresh_valuation':False}
out['checks_passed']=10
(B/'comparisons.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
