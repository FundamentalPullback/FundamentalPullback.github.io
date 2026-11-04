import json
from pathlib import Path
p=Path(__file__).parent;i=json.loads((p/'inputs.json').read_text());ev=i['price']*i['quarterWeightedDilutedShares']+i['debtCarrying']-i['cashCorporate'];ebit=i['fy25Pretax']+i['fy25Interest']+i['nine26Pretax']+i['nine26Interest']-i['nine25Pretax']-i['nine25Interest'];o={'broEvProxy':ev,'broTtmPretaxPlusInterest':ebit,'broProxyMultiple':ev/ebit,'ryanEquivalentMultiple':None,'reason':'Class A and LLC unit economics differ by parent-only TRA/assets; no mechanically identical unit price assumed.'};(p/'outputs.json').write_text(json.dumps(o,indent=2)+'\n')
