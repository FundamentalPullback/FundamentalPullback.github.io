import json,csv,math
from pathlib import Path
p=Path(__file__).parent
# USD millions except per-share amounts. Unconsolidated manager basis, including OMG.
cols=['gaap_revenue','management_fees','fee_related_performance_revenues','other_fees','fre','net_realized_performance','realized_investment','net_interest_expense','realized_income','after_tax_ri','class_a_ri_eps','ordinary_sbc','acquisition_sbc']
raw={
'FY2023':[3631.884,2571.513,180.449,92.109,1163.741,133.493,46.185,77.891,1265.528,1185.714,3.65,None,None],
'FY2024':[3884.781,2957.430,231.537,91.879,1361.737,148.878,39.651,83.146,1467.120,1347.823,3.97,348.303,4.548],
'FY2025':[5601.482,3682.922,301.309,272.707,1775.300,169.011,41.443,137.446,1848.308,1704.236,4.76,506.365,234.184],
'9M2024':[2625.784,2176.738,69.553,66.531,965.497,59.545,28.987,62.959,991.070,913.138,2.74,263.096,3.171],
'9M2025':[4096.561,2689.267,130.151,195.493,1247.597,66.779,40.876,96.005,1259.247,1175.111,3.31,383.004,200.079],
'9M2026':[4258.445,3100.897,138.855,252.106,1479.659,138.048,50.218,153.546,1514.379,1369.580,3.79,469.105,98.927],
'Q42025':[1504.921,993.655,171.158,77.214,527.703,102.232,.567,41.441,589.061,529.125,1.45,123.361,34.105],
'Q12026':[1396.436,1001.571,19.556,73.967,464.404,75.336,11.780,48.784,502.736,452.416,1.24,167.333,36.299],
'Q22026':[1428.610,1030.016,40.529,91.962,491.055,50.903,28.683,49.140,521.501,467.569,1.29,151.052,31.727],
'Q32026':[1433.399,1069.310,78.770,86.177,524.200,11.809,9.755,55.622,490.142,449.595,1.26,150.720,30.901]}
h={k:dict(zip(cols,v)) for k,v in raw.items()}
for name,fy,ytd,old in [('TTM202609','FY2025','9M2026','9M2025'),('TTM202509','FY2024','9M2025','9M2024')]:h[name]={c:round(h[fy][c]+h[ytd][c]-h[old][c],6) for c in cols}
for k,v in h.items():
 assert abs(v['management_fees']+v['fee_related_performance_revenues']+v['other_fees'])>0
 assert abs(v['fre']+v['net_realized_performance']+v['realized_investment']-v['net_interest_expense']-v['realized_income'])<.002
v=h['TTM202609'];old=h['TTM202509']
# Pure diagnostic cash conversion / discount grid, NOT approved intrinsic value.
# Start with class-specific RI earnings, haircut ordinary recurring SBC using current ownership and 23.4% statutory tax.
sbc_per_share=v['ordinary_sbc']*.6889*(1-.234)/241.023185
proxy=v['class_a_ri_eps']-sbc_per_share

def factor(g,ke,tg=.03):return sum((1+g)**t/(1+ke)**t for t in range(1,6))+(1+g)**5*(1+tg)/(ke-tg)/(1+ke)**5
rows=[]
for ke in [.10,.115,.13]:
 for g in [.06,.10,.14]:
  for conversion in [.7,.85,1.]:
   f=factor(g,ke);rows.append({'ke_assumption':ke,'growth_assumption':g,'terminal_growth_assumption':.03,'cash_conversion_assumption':conversion,'diagnostic_value_only':proxy*conversion*f,'cash_eps_required_at_133_98':133.98/f})
with (p/'sensitivity_diagnostic.csv').open('w') as f:w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
with (p/'history.csv').open('w') as f:w=csv.DictWriter(f,fieldnames=['period']+cols);w.writeheader();w.writerows(dict(period=k,**v) for k,v in h.items())
out={'ticker':'ARES','status':'material_partial_not_decision_ready','asOf':'2026-11-08','history':h,'ttm_growth':{k:v[k]/old[k]-1 for k in ['management_fees','fre','realized_income','class_a_ri_eps']},'corporate_cash_flow':{'FY2025_cfo':2113.088,'9M2025_cfo':1745.161,'9M2026_cfo':1439.889,'TTM_cfo':2113.088+1439.889-1745.161,'TTM_capex':72.178+83.902-56.385,'warning':'Company-entity CFO remains before AOG allocation, recurring dilution economics and commitments; not distributable cash.'},'current_claims':{'corporate_debt':4778.2,'cash_reported':597.705,'cash_approved_excess':0,'fund_cash_excluded':1164.755,'unfunded_commitments':1873,'gcp_seller_earnout':805.1,'gcp_employee_earnout_fair_value':345.1,'other_employee_earnout_fair_value':116.7,'tra_liability':624.399,'nov2_class_a_m':224.138030,'nov2_nonvoting_m':3.489911,'aog_units_m':102.689992,'mandatory_convertible_shares_min_m':8.151,'mandatory_convertible_shares_max_m':9.78,'q3_ri_total_weighted_shares_m':345.467337,'q3_class_adjusted_weighted_shares_m':241.023185,'corporate_portfolio_unconsolidated':3068.1,'net_accrued_carry_unconsolidated':1191.2},'diagnostic':{'class_a_ri_eps_ttm':v['class_a_ri_eps'],'ordinary_sbc_eps_haircut':sbc_per_share,'earnings_proxy_after_sbc_not_fcfe':proxy,'price_to_ri':133.98/v['class_a_ri_eps'],'required_cash_eps_ke115_growth10':133.98/factor(.10,.115),'low':min(x['diagnostic_value_only'] for x in rows),'high':max(x['diagnostic_value_only'] for x in rows),'warning':'Not fair value. No completed reinvestment, statutory ownership-tax, earnout or capital allocation bridge. No debt subtraction from equity cash stream.'},'approvedFairValue':None,'approvedEntryLow':None,'approvedEntryHigh':None,'maximumFundamentalPrice':None}
(p/'results.json').write_text(json.dumps(out,indent=2));print(json.dumps(out['diagnostic'],indent=2));print(out['ttm_growth'])

exec((p/"extend_model.py").read_text())
