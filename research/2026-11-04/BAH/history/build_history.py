import json,csv
from pathlib import Path
P=Path(__file__).parent;raw=json.loads((P/'xbrl_numeric_subset.json').read_text())
tags={'revenue':'us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax','ebit':'us-gaap:OperatingIncomeLoss','netIncome':'us-gaap:NetIncomeLoss','tax':'us-gaap:IncomeTaxExpenseBenefit','da':'us-gaap:DepreciationAndAmortization','cfo':'us-gaap:NetCashProvidedByUsedInOperatingActivities','capex':'us-gaap:PaymentsToAcquireProductiveAssets','sbc':'us-gaap:ShareBasedCompensation','cashTax':'us-gaap:IncomeTaxesPaidNet','billableExpenses':'bah:BillableExpenses'}
def take(start,end,file):
 d={}
 for k,t in tags.items():
  vals={r['value']/1e6 for r in raw if r['file']==file and r['tag']==t and r.get('startdate')==start and r.get('enddate')==end}
  if not vals and k=='sbc':vals={r['value']/1e6 for r in raw if r['file']==file and r['tag']=='us-gaap:AdjustmentsToAdditionalPaidInCapitalSharebasedCompensationRequisiteServicePeriodRecognitionValue' and r.get('startdate')==start and r.get('enddate')==end}
  assert len(vals)<=1,(k,start,end,vals)
  d[k]=next(iter(vals)) if vals else None
 return d
def combine(items):return {k:sum(m*x[k] for m,x in items) if all(x[k] is not None for _,x in items) else None for k in tags}
r={}
for yr in [2024,2025,2026]:r['FY'+str(yr)]=take(str(yr-1)+'-04-01',str(yr)+'-03-31','fy26')
r['H1FY26']=take('2025-04-01','2025-09-30','q2fy27');r['H1FY27']=take('2026-04-01','2026-09-30','q2fy27');r['H1FY25']=take('2024-04-01','2024-09-30','q2fy26');r['9MFY26']=take('2025-04-01','2025-12-31','q3fy26')
r['Q2FY27']=take('2026-07-01','2026-09-30','q2fy27');r['Q2FY27']['cfo']=294;r['Q2FY27']['capex']=31 # primary issuer Q2 release, supplement to cumulative statement
r['Q1FY27']=combine([(1,r['H1FY27']),(-1,r['Q2FY27'])]);r['Q3FY26']=combine([(1,r['9MFY26']),(-1,r['H1FY26'])]);r['Q4FY26']=combine([(1,r['FY2026']),(-1,r['9MFY26'])]);r['TTM20260930']=combine([(1,r['FY2026']),(1,r['H1FY27']),(-1,r['H1FY26'])]);r['TTM20250930']=combine([(1,r['FY2025']),(1,r['H1FY26']),(-1,r['H1FY25'])])
checks=0
for name,d in r.items():
 d['fcf']=d['cfo']-d['capex'] if None not in [d['cfo'],d['capex']] else None
 d['revenueExBillables']=d['revenue']-d['billableExpenses'] if d['billableExpenses'] is not None else None
 d['ebitMargin']=d['ebit']/d['revenue']
 d['fcfAfterSbcDiagnostic']=d['fcf']-d['sbc'] if None not in [d['fcf'],d['sbc']] else None
 if d['fcf'] is not None:assert abs(d['fcf']-(d['cfo']-d['capex']))<1e-8;checks+=1
for k in tags:
 qs=[r[q][k] for q in ['Q3FY26','Q4FY26','Q1FY27','Q2FY27']]
 if None not in qs:assert abs(sum(qs)-r['TTM20260930'][k])<1e-7;checks+=1
(P/'history.json').write_text(json.dumps(r,indent=2,sort_keys=True)+'\n');(P/'qa.json').write_text(json.dumps({'checks':checks,'allPass':True},indent=2)+'\n')
with (P/'history.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=['period']+list(next(iter(r.values())).keys()));w.writeheader();w.writerows({'period':k,**v} for k,v in r.items())
print(json.dumps({k:r[k] for k in ['TTM20260930','TTM20250930']},indent=2))
