from pathlib import Path
import json,math
P=Path(__file__).parent;f=json.loads((P/'facts.json').read_text());x=json.loads((P.parent/'model/inputs.json').read_text());c=x['capital'];tests={}
def ck(n,a):assert a,n;tests[n]=True
ck('cash excludes restricted',math.isclose(f['cash']+f['marketableSecurities'],c['cashAndShortInvestments']))
ck('debt nominal',c['debtPrincipal']==f['debtPrincipal'])
ck('tax reserve selected gross plus prior interest',math.isclose(c['historicTaxReserve'],f['grossUTB']+f['interestPenaltiesFY25']))
ck('awards selected weighted gap',math.isclose(c['selectedNetAwards'],f['q3WeightedDiluted']-f['q3WeightedBasic']))
ck('shares actual date',c['actualShares']==f['actualShares'])
ck('pending capital not booked',not f['capitalRaiseClosingVerified'] and not f['capitalRaiseCashAlreadyInBalance'])
ck('conditional issue exact',c['financingShares']==f['capitalRaiseShares'] and c['financingCash']==f['capitalRaiseCash'])
ck('FICT not independently valued',c['fictStakeSelectedValue']==0 and f['FICTIndependentValuationUnverified'])
ck('restricted not netted debt',f['restrictedCashExcluded']==3.59)
ck('grant reserve',c['grantRepaymentReserve']==f['deferredGrantPotentialRepayment'])
ck('historical severance',c['restructuringPayable']==f['restructuringPayable'])
ck('future earnings unknown',f['nextEarningsDate'] is None and not f['nextEarningsConfirmed'])
(P/'checks.json').write_text(json.dumps({'passed':len(tests),'checks':tests},indent=2)+'\n');print('PASS',len(tests))
