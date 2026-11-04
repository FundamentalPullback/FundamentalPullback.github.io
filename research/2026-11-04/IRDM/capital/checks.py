from pathlib import Path
import json,math
P=Path(__file__).parent;f=json.loads((P/'facts.json').read_text());x=json.loads((P.parent/'model/inputs.json').read_text());k=x['capital'];t=[]
def ck(n,b):assert b,n;t.append(n)
ck('principal not book plus repeated revolver',k['debtPrincipal']==2159.458)
ck('carrying to principal',math.isclose(f['debtCarrying']+f['deferredDebtCostsAndDiscount'],f['debtPrincipal']))
ck('cash',k['cash']==f['cash'])
ck('actual shares not weighted',k['actualShares']==f['sharesActual'])
ck('tax historical reserve',k['taxReserve']==f['UTBFY25'])
ck('net cap',math.isclose(k['hedgeAssetSelected'],f['capAssetSept']-f['capPremiumLiabilitySept']))
ck('RSU dividend obligation',k['dividendPayable']==f['rsuDividendsPayable'])
ck('no automatic fee',k['terminationFee']==0)
ck('no phantom buyback',f['no2026Buybacks'] and f['buybackProgramTerminated']=='2026-06-28')
ck('prior Aireon stake not added',f['priorStakeNoLongerSeparateAsset'])
ck('no preferred',f['noPreferredOutstanding'])
ck('selected award proxy not certified count',k['selectedAwards']==2.5 and f['awardOverlapNotFullyReconciled'])
(P/'checks.json').write_text(json.dumps({'passed':len(t),'tests':t},indent=2)+'\n');print('PASS',len(t))
