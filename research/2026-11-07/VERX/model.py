"""Reproducible historical tie-out, USD millions. No certified DCF while input gates remain open."""
import json
from pathlib import Path
P=Path(__file__).parent
keys=['revenue','ebit_gaap','net_income','cfo','ppe_additions','software_additions','sbc','da']
data={
'FY2023':[572.387,-17.510,-13.093,74.332,49.261,18.972,33.919,71.891],
'FY2024':[666.776,-2.228,-52.729,164.821,65.769,21.344,47.425,82.733],
'FY2025':[748.444,2.331,7.211,165.543,96.236,21.718,57.763,96.931],
'9M2024':[488.320,10.876,15.069,123.688,47.520,16.357,36.459,61.448],
'9M2025':[553.733,4.942,14.214,123.275,69.342,16.444,46.249,70.797],
'9M2026':[613.891,-14.735,-40.100,122.165,70.607,15.969,47.651,87.317],
'Q1_2026':[196.646,-10.606,-2.510,37.975,24.660,5.656,18.508,27.053],
'H1_2026':[400.616,-15.049,6.533,68.871,47.831,10.648,32.270,56.177]}
data={p:dict(zip(keys,v)) for p,v in data.items()}
def combine(name,*terms):data[name]={k:round(sum(c*data[p][k] for c,p in terms),6) for k in keys}
combine('Q4_2025',(1,'FY2025'),(-1,'9M2025'))
combine('Q2_2026',(1,'H1_2026'),(-1,'Q1_2026'))
combine('Q3_2026',(1,'9M2026'),(-1,'H1_2026'))
combine('TTM_2025_09',(1,'FY2024'),(1,'9M2025'),(-1,'9M2024'))
combine('TTM_2026_09',(1,'FY2025'),(1,'9M2026'),(-1,'9M2025'))
for p,d in data.items():
 d['fcf_cfo_less_all_capex']=round(d['cfo']-d['ppe_additions']-d['software_additions'],6)
 d['fcf_less_sbc_diagnostic_only']=round(d['fcf_cfo_less_all_capex']-d['sbc'],6)
 d['op_margin']=d['ebit_gaap']/d['revenue'];d['net_margin']=d['net_income']/d['revenue']
checks={k:abs(sum(data[p][k] for p in ['Q4_2025','Q1_2026','Q2_2026','Q3_2026'])-data['TTM_2026_09'][k])<1e-8 for k in keys}
assert all(checks.values())
results={'units':'USD million','source_map':{'FY2023_FY2025':'FY2025 Form 10-K consolidated statements','9M2024':'Q3 2025 official results, comparative cash flow and income statement','9M2025_9M2026':'Q3 2026 Form 10-Q consolidated statements','Q1_2026':'Q1 2026 earnings release','H1_2026':'Q2 2026 earnings release'},'historical':data,'checks_four_quarters_equal_ttm':checks,'valuation':{'status':'not_certified','fcff_method':'10 years: 5 explicit plus 5 transition; EBIT*(1-tax)+DA-all necessary investment-dNWC; SBC retained in EBIT; terminal net reinvestment NOPAT*g/ROIC','fair_values':None,'buy_ceiling':None,'margin_of_safety':None,'reverse_dcf':None,'reason':'No completed forecast, current WACC evidence, normalized sustainable margin/reinvestment bridge, or equity dilution/excess cash reconciliation. No placeholders promoted to valuation.'}}
(P/'model_results.json').write_text(json.dumps(results,indent=2)+'\n');(P/'history.json').write_text(json.dumps(data,indent=2)+'\n')
print(json.dumps({k:data[k] for k in ['TTM_2025_09','TTM_2026_09']},indent=2))
