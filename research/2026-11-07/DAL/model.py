"""Historical bridge only. No DCF or approved valuation while capital gates remain open."""
import json,csv
from pathlib import Path
P=Path(__file__).parent
# USD millions. GAAP; CFO-capex is not FCFF. Input sources archived releases/2025 10-K.
cols=['period','revenue','passenger','cargo','other','ebit','net_income','da','cfo','capex','source']
rows=[
['FY2023',58048,48909,723,8416,5521,4609,2341,6464,5323,'10K2025 pp56,58'],
['FY2024',61643,50894,822,9927,5995,3457,2513,8025,5140,'10K2025 pp56,58'],
['FY2025',63364,51768,900,10696,5822,5005,2443,8342,4499,'10K2025 pp56,58'],
['Q4_2025',16003,12916,246,2841,1467,1219,620,2260,908,'Q4_2025 release statements'],
['Q1_2026',15854,12302,226,3326,501,-289,635,2432,1200,'March_2026 release statements'],
['Q2_2026',19757,15607,294,3856,1864,1604,656,1596,1458,'June_2026 release statements'],
['Q3_2026',20186,15534,301,4351,1454,756,673,1713,1413,'Q3_2026 release statements'],
['9M_2026',55797,43443,821,11533,3819,2070,1964,5740,4071,'Q3_2026 statements/reconciliation; capex=sum reported quarters'],
['9M_2025',47361,38852,654,7855,4355,3786,1823,6082,3592,'Q3_2026 comparison; CFO and capex Q3_2026 10-Q p5 (replaces rounded release subtraction)'],
['9M_2024',46084,38079,574,7431,4278,2614,1878,6131,3830,'Q3_2025 comparison; DA/CFO/capex=FY2024-Q4_2024'],
]
d={r[0]:dict(zip(cols,r)) for r in rows}
for name,fy,cur,old in [('TTM_2026_09','FY2025','9M_2026','9M_2025'),('TTM_2025_09','FY2024','9M_2025','9M_2024')]:
 d[name]={'period':name,**{k:d[fy][k]+d[cur][k]-d[old][k] for k in cols[1:-1]},'source':f'{fy}+{cur}-{old}'}
for r in d.values():r['ebit_margin']=r['ebit']/r['revenue'];r['cfo_less_capex']=r['cfo']-r['capex']
with (P/'financial_history.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=cols+['ebit_margin','cfo_less_capex']);w.writeheader();w.writerows(d.values())
a,b=d['TTM_2026_09'],d['TTM_2025_09']
out={'ticker':'DAL','status':'bounded_partial','valuation_approved':False,'entry_approved':False,'conservative':None,'base':None,'favorable':None,'maximum':None,'current_ttm':a,'prior_ttm':b,'growth':{k:a[k]/b[k]-1 for k in ['revenue','ebit','net_income','cfo','capex','cfo_less_capex']},'price':{'date':'2026-11-06','regular_close':87.20,'scanner_last':87.26,'difference':0.06,'source':'MarketWatch November 6 close report'},'quarter_rounding':{'Q1_Q2_Q3_CFO_sum':5741,'reported_9M_CFO':5740,'Q1_Q2_Q3_NI_sum':2071,'reported_9M_NI':2070},'fcff':None,'wacc':None,'terminal_value':None}
(P/'results.json').write_text(json.dumps(out,indent=2))
assert a['revenue']==71800 and a['ebit']==5286
assert a['cfo']==8000 and a['capex']==4978
print(json.dumps(out,indent=2))
