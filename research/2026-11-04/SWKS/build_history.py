from pathlib import Path
import json,csv
P=Path(__file__).parent; F=json.load(open(P/'history/source_inputs.json'))['facts']['us-gaap']; OUT=P/'history';OUT.mkdir(exist_ok=True)
TAGS={'revenue':'RevenueFromContractWithCustomerExcludingAssessedTax','grossProfit':'GrossProfit','ebitGAAP':'OperatingIncomeLoss','netIncome':'NetIncomeLoss','epsDiluted':'EarningsPerShareDiluted','dilutedShares':'WeightedAverageNumberOfDilutedSharesOutstanding','cfo':'NetCashProvidedByUsedInOperatingActivities','capexPPE':'PaymentsToAcquirePropertyPlantAndEquipment','purchasedIntangibles':'PaymentsToAcquireIntangibleAssets','sbc':'ShareBasedCompensation','depreciation':'Depreciation','amortizationAll':'AmortizationOfIntangibleAssets'}
def get(k,start,end):
 rows=[x for u in F[TAGS[k]]['units'].values() for x in u if x.get('start')==start and x['end']==end and x['filed']<='2026-11-04']
 if not rows:return None
 x=sorted(rows,key=lambda x:x['filed'])[-1];return x['val']/(1 if k=='epsDiluted' else 1e6)
periods=[('FY2023','2022-10-01','2023-09-29'),('FY2024','2023-09-30','2024-09-27'),('FY2025','2024-09-28','2025-10-03'),('Q1FY2026','2025-10-04','2026-01-02'),('Q2FY2026','2026-01-03','2026-04-03'),('Q3FY2026','2026-04-04','2026-07-03')]
rows=[]
for name,start,end in periods:
 d={'period':name,'start':start,'end':end,'perimeter':'Skyworks standalone'}
 for k in TAGS:
  v=get(k,start,end)
  if v is None and name in ['Q2FY2026','Q3FY2026']:
   prev={'Q2FY2026':'2026-01-02','Q3FY2026':'2026-04-03'}[name];ytd=get(k,'2025-10-04',end);prior=get(k,'2025-10-04',prev)
   if ytd is not None and prior is not None:v=round(ytd-prior,6)
  d[k]=v
 rows.append(d)
for name,vals in [('Q4FY2026',[1045.7,427.4,22.3,23.4,.15,151.5,33.7,94.7,10.8,49.5,73,43]),('FY2026',[3959.6,1614.9,216.7,172.1,1.14,151,549.9,320.6,30.5,218.4,289.1,173.4])]:
 d={'period':name,'start':'2026-07-04' if name.startswith('Q4') else '2025-10-04','end':'2026-10-02','perimeter':'Skyworks standalone'};d.update(dict(zip(TAGS,vals)));rows.append(d)
for d in rows:
 d['fcfPPE']=round(d['cfo']-d['capexPPE'],6);d['fcfAfterPurchasedIntangibles']=round(d['fcfPPE']-d['purchasedIntangibles'],6);d['fcfLessSBCDiagnostic']=round(d['fcfAfterPurchasedIntangibles']-d['sbc'],6);d['operatingMargin']=d['ebitGAAP']/d['revenue'];d['grossMargin']=d['grossProfit']/d['revenue'];d['fcfPerDilutedShare']=d['fcfAfterPurchasedIntangibles']/d['dilutedShares']
(OUT/'history.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
with open(OUT/'history.csv','w') as f:w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
checks={}
for k in TAGS:
 if k not in ['epsDiluted','dilutedShares']:
  diff=sum(x[k] for x in rows if x['period'].startswith('Q'))-rows[-1][k];checks[k]={'quarterSumMinusFY':round(diff,6),'withinPublishedRounding':abs(diff)<=.300001}
checks['note']='Quarter cash and investment disclosures rounded to 0.1m. PPE quarters sum 320.7 vs FY320.6; intangibles30.6 vs FY30.5. Preserve published amounts, do not invent a reconciliation.'
(OUT/'checks.json').write_text(json.dumps(checks,indent=2)+'\n');print(json.dumps(rows,indent=2));print(checks)
