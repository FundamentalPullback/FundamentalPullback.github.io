import json
from pathlib import Path
p=Path(__file__).resolve().parent
x=json.loads((p/'inputs.json').read_text())
ebit=x['sales']-sum(x['operatingCosts'].values())
assert ebit==3163
assert sum(x['salesComponents'].values())==x['sales']
rows={k:x['soldUnitsMillions'][k]*v for k,v in x['priceStepUsdPerUnit'].items()}
scenarios={name:{'grossRevenueChange':sum(x['soldUnitsMillions'][k]*v for k,v in delta.items()),'fairValue':None,'cashFlow':None} for name,delta in x['selectedPriceOnlyScenarios'].items()}
out={'period':x['period'],'ebitReconstructed':ebit,'grossPriceStepExposure':rows,'priceOnlyScenarios':scenarios,'aroTotal':x['aroCurrent']+x['aroNoncurrent'],'redChrisRealNEMShareRange':[x['redChrisRealCapex100pctLow']*x['redChrisOwnership'],x['redChrisRealCapex100pctHigh']*x['redChrisOwnership']],'fairValue':None,'tenYearDcf':None,'inverseDcf':None,'caveats':x['caveats']}
assert out['aroTotal']==6773
assert scenarios['higher']['grossRevenueChange']==-scenarios['lower']['grossRevenueChange']
assert out['redChrisRealNEMShareRange']==[2940.,3360.]
(p/'results.json').write_text(json.dumps(out,indent=2)+'\n')
print('Analysis arithmetic: 5 checks PASS; no valuation produced')
