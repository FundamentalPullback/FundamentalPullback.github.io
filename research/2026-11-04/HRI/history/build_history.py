"""Offline reconstruction from selected observations; no network or full filings needed."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parent
obs=json.loads((ROOT/'observations.json').read_text());index={o['id']:o for o in obs}
metrics=['sales','net_income','eps_diluted','cfo','rental_gross_capex','rental_disposal_proceeds','nonrental_capex','nonrental_disposal_proceeds','rental_da','other_da','sbc','transaction_expenses','pretax_income','interest_nonoperating_signed','other_nonoperating_signed']
def direct(source,metric,start,end):
 o=index.get(f'{source}:{metric}:{start}:{end}')
 if o:return {'value':o['value'],'status':'direct','observation_ids':[o['id']]}
 return None
def combine(a,b,sign,formula):
 assert a is not None and b is not None,(formula,a,b)
 return {'value':round(a['value']+sign*b['value'],6),'status':'derived','formula':formula,'observation_ids':list(dict.fromkeys(a['observation_ids']+b['observation_ids']))}
def base(source,start,end):return {m:direct(source,m,start,end) for m in metrics}
annual={f'FY{y}':base('annual',f'{y}-01-01',f'{y}-12-31') for y in (2023,2024,2025)}
ytd25=base('q3','2025-01-01','2025-09-30');ytd26=base('q3','2026-01-01','2026-09-30');h126=base('q2','2026-01-01','2026-06-30')
q1=base('q1','2026-01-01','2026-03-31');q2=base('q2','2026-04-01','2026-06-30');q3=base('q3','2026-07-01','2026-09-30')
q4={m:combine(annual['FY2025'][m],ytd25[m],-1,'FY2025 - 9M2025') for m in metrics if m!='eps_diluted'}
q4['eps_diluted']=direct('q4_release','eps_diluted','2025-10-01','2025-12-31')
for m in metrics:
 if q2[m] is None:q2[m]=combine(h126[m],q1[m],-1,'6M2026 - Q1 2026')
 if q3[m] is None:q3[m]=combine(ytd26[m],h126[m],-1,'9M2026 - 6M2026')
ttm={m:combine(q4[m],ytd26[m],1,'Q4 2025 + 9M2026') for m in metrics if m!='eps_diluted'}
# EPS is nonadditive under changing shares and antidilution. A sum of reported quarter EPS is disclosed, never labelled reported GAAP TTM EPS.
ttm['eps_diluted']={'value':None,'status':'not_reported','reason':'A trailing-twelve-month GAAP diluted EPS is not directly reported; do not subtract FY and 9M EPS.'}
ttm['eps_diluted_sum_of_quarters']={'value':round(sum(q['eps_diluted']['value'] for q in (q4,q1,q2,q3)),2),'status':'derived','formula':'Sum of four reported quarterly diluted EPS; not a recalculated GAAP TTM diluted EPS','observation_ids':sum([q['eps_diluted']['observation_ids'] for q in (q4,q1,q2,q3)],[])}
ytd24=base('q3_prior','2024-01-01','2024-09-30')
prior_ttm={m:combine(combine(annual['FY2024'][m],ytd24[m],-1,'FY2024 - 9M2024'),ytd25[m],1,'FY2024 - 9M2024 + 9M2025') for m in metrics if m!='eps_diluted'}
prior_ttm['eps_diluted']={'value':None,'status':'not_reported','reason':'No valid directly reported TTM diluted EPS; annual and YTD EPS are not additive.'}
periods={**annual,'TTM2025Q3':prior_ttm,'2025Q4':q4,'2026Q1':q1,'2026Q2':q2,'2026Q3':q3,'TTM2026Q3':ttm}
for name,p in periods.items():
 p['operating_ebit']=combine(combine(p['pretax_income'],p['interest_nonoperating_signed'],-1,'Pretax - signed nonoperating interest'),p['other_nonoperating_signed'],-1,'Pretax - signed nonoperating interest - signed other nonoperating')
 p['net_rental_capex']=combine(p['rental_gross_capex'],p['rental_disposal_proceeds'],-1,'Rental gross capex - rental disposal proceeds')
 p['fcf_after_gross_capex']=combine(combine(p['cfo'],p['rental_gross_capex'],-1,'CFO - gross rental capex'),p['nonrental_capex'],-1,'CFO - gross rental capex - nonrental capex')
 p['fcf_after_net_capex']=combine(combine(p['fcf_after_gross_capex'],p['rental_disposal_proceeds'],1,'Gross-capex FCF + rental disposal proceeds'),p['nonrental_disposal_proceeds'],1,'CFO - rental and nonrental capex + rental and nonrental disposal proceeds')
 for metric,value in p.items():
  assert value is not None,(name,metric)
  assert all(i in index for i in value.get('observation_ids',[]))
out={'company':'Herc Holdings Inc.','ticker':'HRI','as_of':'2026-11-04','units':'USD millions except EPS in USD/share','periods':periods,'notes':['Operating EBIT is analytically derived, not a reported operating-income subtotal. Transaction costs and loss on assets held for sale remain in EBIT. Interest and Other nonoperating income/expense are excluded.','Cash capex and proceeds follow the cash-flow statement, not accrual-basis equipment sales revenue. Capex is expressed as a positive outflow.','H&E results consolidated from June 2, 2025. FY2025 contains a partial period; current TTM Oct 1 2025-Sep 30 2026 contains 12 months of acquired operations. Growth across FY2024/FY2025 is acquisition-distorted.','Comparable TTM2025Q3 spans October 1 2024-September 30 2025 and includes only about four months of H&E from June 2, 2025. Current TTM includes twelve months, so TTM growth and cash conversion are not like-for-like.', 'FY2024 includes $194m assets-held-for-sale loss; FY2025 includes $48m. No normalization applied.','Quarter cash flow observations derive from cumulative YTD differences; Q4 uses full year less nine months. Rounded reported amounts create rounding limits.']}
(ROOT/'history.json').write_text(json.dumps(out,indent=2)+'\n')
# Independent statement-level control totals, checked against extracted/derived values.
checks=[]
for period,metric,expected in [('FY2023','sales',3282),('FY2024','sales',3568),('FY2025','sales',4376),('FY2023','operating_ebit',663),('FY2024','operating_ebit',549),('FY2025','operating_ebit',423),('TTM2026Q3','sales',4916),('TTM2026Q3','net_income',123),('TTM2026Q3','operating_ebit',653),('TTM2026Q3','cfo',1266),('TTM2026Q3','rental_gross_capex',1318),('TTM2026Q3','rental_disposal_proceeds',461),('TTM2026Q3','nonrental_capex',141),('FY2025','fcf_after_net_capex',299),('2025Q4','eps_diluted',.72)]:
 actual=periods[period][metric]['value'];checks.append(dict(period=period,metric=metric,expected=expected,actual=actual,pass_=actual==expected))
for m in metrics:
 if m=='eps_diluted':continue
 actual=sum(q[m]['value'] for q in (q4,q1,q2,q3));expected=ttm[m]['value'];checks.append(dict(test='Four quarters equal TTM',metric=m,actual=actual,expected=expected,pass_=abs(actual-expected)<1e-6))
for m in metrics:
 a=direct('q3_prior',m,'2025-01-01','2025-09-30');b=ytd25[m]
 checks.append(dict(test='9M2025 agrees across 2025 and 2026 Q3 filings',metric=m,actual=a['value'],expected=b['value'],pass_=a['value']==b['value']))
for m,expected in [('sales',4118),('operating_ebit',286),('net_income',-69),('cfo',1101),('rental_gross_capex',1130),('rental_disposal_proceeds',396),('nonrental_capex',157)]:
 actual=prior_ttm[m]['value'];checks.append(dict(test='Prior TTM selected controls',metric=m,actual=actual,expected=expected,pass_=actual==expected))
qa={'checks':checks,'all_passed':all(c['pass_'] for c in checks),'observation_count':len(obs)}
(ROOT/'QA.json').write_text(json.dumps(qa,indent=2)+'\n')
assert qa['all_passed'],[c for c in checks if not c['pass_']]
print('PASS',len(checks),'checks; history.json built offline')
for name,p in periods.items():print(name, {m:p[m]['value'] for m in ['sales','operating_ebit','net_income','eps_diluted','cfo','rental_gross_capex','rental_disposal_proceeds','nonrental_capex','sbc']})
import csv
columns=list(periods['TTM2026Q3'])
with (ROOT/'history.csv').open('w',newline='') as f:
 writer=csv.writer(f);writer.writerow(['period']+columns)
 for period,values in periods.items():writer.writerow([period]+[values.get(m,{}).get('value','') for m in columns])
