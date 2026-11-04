from pathlib import Path
import json,math
P=Path(__file__).parent;c=json.loads((P/'facts.json').read_text());x=json.loads((P.parent/'model/inputs.json').read_text());checks=[]
def ck(n,b):
 assert b,n
 checks.append(n)
ck('Debt aggregation',c['shortDebt']+c['longDebtCurrent']+c['longDebtNoncurrent']==20106)
ck('Cash aggregation',c['cash']+c['shortInvestments']==818)
ck('Pensions aggregation',c['pensionLiabilities']+c['otherPostRetirementLiabilities']==780)
ck('Selected tax historical',c['historicUnrecognizedTaxBenefitsFY25']+c['historicInterestPenaltyFY25']==1518)
ck('No automatic notice double count',x['capital']['historicTaxReserve']==1518 and c['noticeOverlapWithExistingReservesUnreconciled'])
ck('No revolver cash',x['capital']['cashAndShortInvestments']==818 and c['revolverUndrawn']==4000)
ck('Dated shares',c['actualSharesDate']=='2026-09-30' and x['capital']['actualShares']==388.5)
ck('Weighted dilution proxy',math.isclose(c['q3WeightedDiluted']-c['q3WeightedBasic'],1))
ck('Dividend still cum',not c['dividendPaidAtPriceDate'])
ck('No old Stage2 inheritance',c['currentStage2'] is None)
t=json.loads((P.parent/'transaction/verified.json').read_text())
ck('No final exchange ratio',t['exchange']['finalExchangeRatio'] is None)
ck('No Mobility cash in model',x['capital']['postBalanceNetAdjustment']==0)
(P/'checks.json').write_text(json.dumps({'passed':len(checks),'labels':checks},indent=2)+'\n');print(len(checks),'capital PASS')
