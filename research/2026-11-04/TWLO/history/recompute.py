#!/usr/bin/env python3
"""Offline, deterministic, Python stdlib only. Source amounts USD thousands.
Run from any cwd; rebuild history.json/history.csv/qa.json from numeric extracts.
No network; full filings deliberately excluded from delivery.
"""
import json,csv,pathlib
from collections import defaultdict
P=pathlib.Path(__file__).resolve().parent
s=json.loads((P/'source_numeric_extracts.json').read_text()); d=defaultdict(dict); provenance=defaultdict(dict);checks=[]
for r in s['observations']:
 p,m,v=r['period'],r['metric'],r['value']
 if p in d and m in d[p]:
  assert d[p][m]==v,(p,m,d[p][m],v)
 d[p][m]=v;provenance[p][m]=r['source']+':table'+str(r['table'])
# CFO SBC and P&L SBC differ; do not combine them.
for y in [2025,2026]:
 for m in ['da_cfo','sbc_cfo','commission_amortization']:
  d[f'Q2{y}'][m]=d[f'6M{y}'][m]-d[f'Q1{y}'][m];provenance[f'Q2{y}'][m]=f'6M{y}-Q1{y}'
  d[f'Q3{y}'][m]=d[f'9M{y}'][m]-d[f'6M{y}'][m];provenance[f'Q3{y}'][m]=f'9M{y}-6M{y}'
for y in [2024,2025]:
 for m in ['da_cfo','sbc_cfo','commission_amortization']:
  d[f'Q4{y}'][m]=d[f'FY{y}'][m]-d[f'9M{y}'][m];provenance[f'Q4{y}'][m]=f'FY{y}-9M{y}'
for p,row in d.items():
 for m in ['software_cash','capex_cash']: 
  if m in row:row[m]=abs(row[m])
for y in [2025,2026]:
 p=f'TTM_Q3{y}'; a=f'FY{y-1}'; b=f'9M{y}';c=f'9M{y-1}'
 for m in ['revenue','ebit','ni_common','gross_profit','cfo','software_cash','capex_cash','da_cfo','sbc_cfo','commission_amortization']:
  d[p][m]=d[a][m]+d[b][m]-d[c][m];provenance[p][m]=f'{a}+{b}-{c}'
 qs=[f'Q4{y-1}',f'Q1{y}',f'Q2{y}',f'Q3{y}']
 d[p]['eps_diluted_sum_reported_quarters']=round(sum(d[q]['eps_diluted'] for q in qs),2)
 provenance[p]['eps_diluted_sum_reported_quarters']='Sum of four directly reported quarter EPS, not company-reported TTM EPS or NI/share reconstruction.'
 d[p]['amort_acquired']=sum(d[q]['amort_acquired'] for q in qs)
 d[p]['sbc_pl']=sum(d[q]['sbc_pl'] for q in qs)
 for m in ['revenue','ebit','ni_common','cfo','software_cash','capex_cash']:
  assert abs(d[p][m]-sum(d[q][m] for q in qs))<0.001,(p,m)
 checks.append(f'{p}: annual + current nine months - previous nine months equals sum of four quarters for revenue, EBIT, NI, CFO, capex and software.')
for p,row in d.items():
 if all(m in row for m in ['cfo','software_cash','capex_cash']):row['fcf_cfo_less_cash_capex_and_software']=row['cfo']-row['software_cash']-row['capex_cash']
 if 'revenue' in row:
  row['ebit_margin_pct']=round(100*row['ebit']/row['revenue'],6)
  if 'gross_profit' in row:row['gross_margin_pct']=round(100*row['gross_profit']/row['revenue'],6)
order=['FY2023','FY2024','FY2025','Q42024','Q12025','Q22025','Q32025','Q42025','Q12026','Q22026','Q32026','TTM_Q32025','TTM_Q32026','9M2024','9M2025','9M2026','6M2025','6M2026']
result={'as_of':s['as_of'],'units':'USD thousands, except EPS USD/share and percentages','notes':['EBIT is GAAP income from operations. Cash capex includes purchased long-lived/intangible assets, not solely physical PPE.','TTM EPS is only the sum of directly reported quarterly diluted EPS. It is not an official TTM figure; no division of TTM NI by shares.','CFO SBC is distinct from P&L SBC. D&A includes amortization; do not add acquired amortization to CFO D&A.','Null/missing is not zero.'], 'periods':{p:d[p] for p in order},'provenance':dict(provenance),'sources':s['sources']}
(P/'history.json').write_text(json.dumps(result,indent=2)+'\n')
cols=['period']+sorted(set().union(*(r.keys() for r in d.values())))
with (P/'history.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=cols);w.writeheader();w.writerows(dict(period=p,**d[p]) for p in order)
for p in ['FY2023','FY2024','FY2025']+[f'Q{q}{y}' for y,qs in [(2024,[4]),(2025,[1,2,3,4]),(2026,[1,2,3])] for q in qs]:
 for m in ['revenue','ebit','ni_common','eps_diluted','cfo','capex_cash','software_cash']:assert m in d[p],(p,m)
checks+=['All FY23-25 and last four quarters plus prior-year quarter comparatives have revenue, EBIT, common NI, directly reported EPS, CFO and both capex components.','Duplicate observations from different sources agree exactly.','No next earnings date assumed. No valuation performed.']
(P/'qa.json').write_text(json.dumps({'status':'PASS','checks':checks,'limitations':['Capitalized commission cash additions not separately disclosed in inspected sources; do not infer from asset movement alone.','Software book capitalization and cash investment differ due to noncash elements/timing.','Zipwhip detailed shutdown history not verified from an accessible primary excerpt; do not create organic perimeter adjustment.']},indent=2)+'\n')
print(json.dumps({p:d[p] for p in ['TTM_Q32025','TTM_Q32026']},indent=2))
