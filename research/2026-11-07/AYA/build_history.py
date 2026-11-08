from pathlib import Path
import json,csv
p=Path(__file__).parent
# USD millions. FY2023 CF uses recast comparative in FY2024, not originally presented FY2023 CF.
keys=['revenue','operating_income','net_income','parent_income','cfo','ppe_cash','exploration_cash','supplier_deposits','sbc_expense','da']
data={'FY2023':[42.849,4.931,5.332,5.504,3.377,79.353,21.860,7.556,3.201,5.004],'FY2024':[39.117,-38.747,-26.027,-21.617,-8.615,62.881,29.891,2.569,8.231,3.370],'FY2025':[202.102,62.517,46.280,45.557,71.948,33.425,42.053,3.137,15.176,20.525],'H1_2024':[18.756,-1.216,4.222,4.300,-4.928,36.935,13.999,1.169,2.197,.840],'H1_2025':[72.446,10.995,15.571,15.754,15.706,15.002,11.319,2.335,8.763,8.978],'9M_2025':[126.783,26.167,27.994,28.159,38.099,25.468,25.445,2.475,12.371,13.712],'H1_2026':[214.068,130.742,83.567,82.914,118.573,12.365,24.621,2.790,6.326,14.762],'Q2_2026':[96.794,53.155,35.038,34.588,48.402,9.678,10.556,1.438,2.992,7.757]}
h={k:dict(zip(keys,v)) for k,v in data.items()}
def bridge(n,a,b,c=None):h[n]={k:h[a][k]-h[b][k]+(h[c][k] if c else 0) for k in keys}
bridge('Q3_2025','9M_2025','H1_2025');bridge('Q4_2025','FY2025','9M_2025');bridge('Q1_2026','H1_2026','Q2_2026');bridge('TTM_Jun2026','FY2025','H1_2025','H1_2026');bridge('TTM_Jun2025','FY2024','H1_2024','H1_2025')
for v in h.values():v['cash_after_ppe_exploration_deposits']=v['cfo']-v['ppe_cash']-v['exploration_cash']-v['supplier_deposits'];v['operating_margin']=v['operating_income']/v['revenue']
(p/'financial_history.json').write_text(json.dumps(h,indent=2))
with open(p/'financial_history.csv','w') as f:
 w=csv.DictWriter(f,fieldnames=['period']+list(next(iter(h.values()))));w.writeheader();w.writerows(dict(period=k,**v) for k,v in h.items())
print(json.dumps({k:v for k,v in h.items() if k.startswith('TTM')},indent=2))
