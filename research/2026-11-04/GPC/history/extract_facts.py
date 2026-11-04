#!/usr/bin/env python3
"""Optional extraction from downloaded SEC XHTML. Python standard library only.
Usage: python extract_facts.py RAW_DIRECTORY OUTPUT_JSON
Raw filenames: YYYY-MM-DD.html, plus secq326.html. Do not bundle full filings.
"""
import sys,json,xml.etree.ElementTree as ET
from pathlib import Path
TAGS='RevenueFromContractWithCustomerExcludingAssessedTax CostOfGoodsAndServicesSold GrossProfit SellingGeneralAndAdministrativeExpense DepreciationAndAmortization ProvisionForDoubtfulAccounts RestructuringCharges OperatingExpenses InterestExpenseNonoperating PensionSettlementChargeNonoperating OtherNonoperatingIncomeExpense NonoperatingIncomeExpense IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest IncomeTaxExpenseBenefit NetIncomeLoss DepreciationDepletionAndAmortization ShareBasedCompensation NetCashProvidedByUsedInOperatingActivities PaymentsToAcquirePropertyPlantAndEquipment PaymentsToAcquireBusinessesAndInterestInAffiliates AmortizationOfIntangibleAssets WeightedAverageNumberOfDilutedSharesOutstanding EarningsPerShareDiluted AccountsReceivableSale ProceedsFromSaleOfAccountReceivable AccountsReceivableSalesTransactionsFees IncreaseDecreaseInFirstBrandsReserve DefinedBenefitPlanRecognizedNetGainLossDueToSettlementsAndCurtailments1 PaymentsForRestructuring RestructuringReserveNoncashChargesRecoveries'.split()
ACC={'2026-09-30':'000004098726000041','2026-06-30':'000004098726000033','2026-03-31':'000004098726000017','2025-12-31':'000004098726000003','2025-09-30':'000004098725000196','2024-12-31':'000004098725000026'}
records=[]
for date,acc in ACC.items():
 p=Path(sys.argv[1])/(date+'.html')
 if not p.exists() and date=='2026-09-30':p=Path(sys.argv[1])/'secq326.html'
 r=ET.parse(p).getroot();contexts={}
 for e in r.iter():
  if e.tag.endswith('}context'):
   if any(x.tag.endswith(('}explicitMember','}typedMember')) for x in e.iter()):continue
   fields={x.tag.split('}')[-1]:x.text for x in e.iter() if x.tag.endswith(('}startDate','}endDate','}instant'))}
   contexts[e.attrib['id']]=fields
 for e in r.iter():
  a=e.attrib;tag=a.get('name','').split(':')[-1];ctx=contexts.get(a.get('contextRef'))
  if not e.tag.endswith('}nonFraction') or tag not in TAGS or not ctx or 'startDate' not in ctx:continue
  raw=''.join(e.itertext()).replace(',','').replace('\u00a0','').strip()
  try:value=(0 if raw in ['—','–','-'] else float(raw))*10**int(a.get('scale',0))*(-1 if a.get('sign')=='-' else 1)
  except ValueError:continue
  records.append(dict(source_date=date,url=f'https://www.sec.gov/Archives/edgar/data/40987/{acc}/gpc-{date.replace("-", "")}.htm',tag=a['name'],start=ctx['startDate'],end=ctx['endDate'],unit=a['unitRef'],value=value,decimals=a.get('decimals'),fact_id=a.get('id')))
# retain unique facts, highest precision within same filing/tag/period
best={}
for x in records:
 k=(x['source_date'],x['tag'],x['start'],x['end'],x['unit'])
 def precision(z):return 99 if z['decimals']=='INF' else int(z['decimals'] or -99)
 if k not in best or precision(x)>precision(best[k]):best[k]=x
Path(sys.argv[2]).write_text(json.dumps(list(best.values()),indent=2)+'\n')
