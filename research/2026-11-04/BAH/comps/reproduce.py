import json
from pathlib import Path
p=Path(__file__).parent;i=json.loads((p/'inputs.json').read_text());o={}
for k in ['BAH','CACI']:
 d=i[k];ebit=d.get('ttmEbit',d.get('fyEbit',0)+d.get('currentQuarterEbit',0)-d.get('priorQuarterEbit',0));ev=d['price']*d['quarterWeightedDilutedShares']+d['debtCarrying']-d['cash'];o[k]={'proxyEv':ev,'ttmGaapEbit':ebit,'proxyEvEbit':ev/ebit}
(p/'outputs.json').write_text(json.dumps(o,indent=2,sort_keys=True)+'\n')
