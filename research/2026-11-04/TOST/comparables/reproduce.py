import json
from pathlib import Path
p=Path(__file__).parent;x=json.loads((p/'inputs.json').read_text());out={}
for n in ['TOST','SHOP']:
 a=x[n];ev=a['close']*a['basicShares']+a['debt']-a['cashSecurities'];out[n]={'indicativeEv':ev,'evGaapEbit':ev/a['gaapEbit'],'gaapOperatingMargin':a['gaapEbit']/a['revenue'],'cashAfterLoanIntangibleAndSbc':a['reportedFcf']-a['loanFunding']-a.get('otherIntangibleCash',0)-a['noncashSbc']}
 if 'partialNormalizedEbit' in a:out[n]['evPartialNormalizedEbit']=ev/a['partialNormalizedEbit']
out['limits']=x['limits'];(p/'results.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(out)
