from pathlib import Path
import json
p=Path(__file__).parent
x=json.loads((p/'inputs.json').read_text())
for v in x['comparisons']:
 v['dailyTCEGrowth']=v['dailyTCE']/v['priorDailyTCE']-1
 v['isHomogeneousValuationMultiple']=False
(p/'results.json').write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
print('Peer operational comparison reproduced')
