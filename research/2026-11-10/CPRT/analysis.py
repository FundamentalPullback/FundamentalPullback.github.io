from pathlib import Path
import json,csv
P=Path(__file__).parent
# USD thousands, source statements; capex expressed as positive cash outflow.
cols=['revenue','ebit','net_income_parent','da','cfo','cash_capex','sbc','net_interest_income']
raw={
'FY2024':[4236823,1572023,1363020,190256,1472564,510990,35234,145673],
'FY2025':[4646958,1696714,1552449,217784,1799750,568990,38004,178909],
'FY2026':[4666209,1652590,1484270,238466,1604492,337363,38818,181923],
'9M2025':[3521861,1284123,1156095,163642,1361274,481349,28905,129070],
'9M2026':[3513770,1283686,1156847,168799,1246951,258553,29013,142305],
'H1FY2026':[2276704,819404,754446,109713,662753,177660,19550,103492],
'Q1FY2026':[1155030,430694,403714,54199,535253,108042,9319,53505]}
a={k:dict(zip(cols,v)) for k,v in raw.items()}
def sub(x,y):return {k:a[x][k]-a[y][k] for k in cols}
a['Q2FY2026']=sub('H1FY2026','Q1FY2026');a['Q3FY2026']=sub('9M2026','H1FY2026');a['Q4FY2026']=sub('FY2026','9M2026');a['Q4FY2025']=sub('FY2025','9M2025');a['TTMJuly2026']=a['FY2026'].copy()
for k in cols:assert sum(a[q][k] for q in ['Q1FY2026','Q2FY2026','Q3FY2026','Q4FY2026'])==a['FY2026'][k]
for v in a.values():v['simple_fcf']=v['cfo']-v['cash_capex'];v['fcf_less_sbc_diagnostic']=v['simple_fcf']-v['sbc']
metrics={k+'_growth_pct':100*(a['FY2026'][k]/a['FY2025'][k]-1) for k in ['revenue','ebit','net_income_parent','cfo','cash_capex','simple_fcf']}
metrics.update(q4_revenue_growth_pct=100*(a['Q4FY2026']['revenue']/a['Q4FY2025']['revenue']-1),q4_ebit_growth_pct=100*(a['Q4FY2026']['ebit']/a['Q4FY2025']['ebit']-1),cash_plus_treasuries_july_m=(1907901+2581901)/1000,illustrative_cap_m=926330452*32.41/1e6,illustrative_pe_fy26=32.41/1.55,fcf_delta_thousands=a['FY2026']['simple_fcf']-a['FY2025']['simple_fcf'],cfo_delta_thousands=1604492-1799750,capex_delta_thousands=337363-568990)
out={'units':'USD thousands except metrics explicitly noted','source_map':{'annual':'S1 income table28/cash31','9M':'S2 tables7/11','H1':'S3 tables7/11','Q1':'S7 tables7/11'},'periods':a,'metrics':metrics,'valuation':None,'entryApproved':False,'scope':'Standalone Copart through July2026; ACV closed Oct16, not consolidated here'}
(P/'calculations.json').write_text(json.dumps(out,indent=2)+'\n')
with (P/'financials.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=['period']+list(next(iter(a.values()))));w.writeheader();w.writerows(dict(period=k,**v) for k,v in a.items())
print(json.dumps(metrics,indent=2));print(json.dumps({k:a[k] for k in ['Q2FY2026','Q3FY2026','Q4FY2026']},indent=2))
