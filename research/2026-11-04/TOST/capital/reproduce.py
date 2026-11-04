import json
from pathlib import Path
p=Path(__file__).parent;x=json.loads((p/'facts.json').read_text());price=35.35
out={'cashSecurities':x['cash']+x['marketableSecurities'],'selectedBridge':x['cash']+x['marketableSecurities']-x['selectedOperatingCash']-x['warrantFairValueClaim']-x['historicalGrossUtbSelectedReserve'],'basicShares':x['basicClassA']+x['basicClassB'],'netOptionProxy':x['expectedVestOptions']*(1-x['optionWeightedExercise']/price)}
out['dilutedShareProxy']=out['basicShares']+x['expectedVestRsu']+out['netOptionProxy'];out['creditLegacyCashStress84PerShare']=84/out['dilutedShareProxy'];out['utb7PerShare']=7/out['dilutedShareProxy']
assert out['cashSecurities']==1885;assert out['selectedBridge']==1365;assert out['basicShares']==581
(p/'verified.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(out)
