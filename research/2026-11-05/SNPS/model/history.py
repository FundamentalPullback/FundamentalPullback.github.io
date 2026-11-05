from pathlib import Path
import json
P=Path(__file__).resolve().parent
# All USDm. Primary statements and segment reconciliation. No stock-comp addback.
cols=['revenue','ebit','net_income_cont','diluted_shares','cfo_total','capex','sbc_cont','acquired_amort','restructuring','acq_operating','interest']
raw={
'FY2023':[5318.014,1273.239,1227.045,155.195,1703.274,191.822,513.094,54.576,53.091,13.831,2.703],
'FY2024':[6127.436,1355.711,1441.710,155.944,1407.029,139.500,657.935,124.234,0,138.733,36.829],
'FY2025':[7054.178,914.927,1336.120,165.656,1518.608,169.454,893.294,504.383,0,254.755,446.729],
'9M2024':[4491.450,1044.909,1162.429,155.863,844.211,118.772,492.550,53.317,0,91.771,20.547],
'9M2025':[4799.318,793.534,887.424,158.176,878.870,134.908,655.909,99.193,0,218.680,251.977],
'9M2026':[7161.605,680.963,627.863,191.981,2298.603,156.089,712.631,1210.292,236.340,62.091,429.313],
'Q12025':[1455.315,251.839,295.683,156.189,-67.455,40.715,186.463,12.596,0,60.681,11.139],
'Q22025':[1604.266,376.426,349.232,156.088,275.365,55.588,201.723,11.656,0,39.571,94.336],
'Q32025':[1739.737,165.269,242.509,161.682,670.960,38.605,267.723,74.941,0,118.428,146.502],
'Q12026':[2408.798,203.046,64.958,190.762,856.832,35.320,258.724,404.235,118.282,15.592,162.715],
'Q22026':[2275.985,120.426,17.105,192.144,628.934,54.198,222.303,403.631,115.894,23.649,133.364],
'Q32026':[2476.822,357.491,545.800,192.319,812.837,66.571,231.604,402.426,2.164,22.850,133.234]}
D={k:dict(zip(cols,v)) for k,v in raw.items()}
for y in [2024,2025]:
 D['Q4'+str(y)]={c:D['FY'+str(y)][c]-D['9M'+str(y)][c] for c in cols};D['Q4'+str(y)]['diluted_shares']=D['FY'+str(y)]['diluted_shares']*4-D['9M'+str(y)]['diluted_shares']*3
for y in [2025,2026]:
 D['TTM'+str(y)]={c:D['FY'+str(y-1)][c]+D['9M'+str(y)][c]-D['9M'+str(y-1)][c] for c in cols};D['TTM'+str(y)]['diluted_shares']=(D['Q4'+str(y-1)]['diluted_shares']+D['9M'+str(y)]['diluted_shares']*3)/4
for k,r in D.items():
 r['fcf_total']=r['cfo_total']-r['capex'];r['economic_ebit_before_replacement']=r['ebit']+r['acquired_amort']+r['restructuring']+r['acq_operating'];r['normalized_replacement_cost']=r['revenue']*.01;r['normalized_ebit']=r['economic_ebit_before_replacement']-r['normalized_replacement_cost'];r['normalized_income']=(r['normalized_ebit']-r['interest'])*.8;r['normalized_eps']=r['normalized_income']/r['diluted_shares'];r['fcf_after_sbc']=r['fcf_total']-r['sbc_cont'];r['normalized_margin']=r['normalized_ebit']/r['revenue']
# Do not label combined earnings as homogeneous organic earnings.
PF={'FY2024':8450.296,'FY2025':8920.890,'9M2024':6385.630,'9M2025':6666.029,'Q12025':2217.683,'Q22025':2157.992,'Q32025':2290.354}
PF['Q42024']=PF['FY2024']-PF['9M2024'];PF['TTM2025']=PF['FY2024']+PF['9M2025']-PF['9M2024'];PF['TTM2026']=D['TTM2026']['revenue']
O={'history':D,'proforma_revenue':PF,'proforma_ttm_growth':PF['TTM2026']/PF['TTM2025']-1,'normalization':'EBIT + acquired amortization + operating acquisition/divestiture expense + restructuring - 1% revenue replacement cost. SBC and deferred compensation retained. No nonoperating gains or interest income. 20% normalized tax; reported interest retained. This is an economic earnings proxy, not homogeneous organic or acquisition-adjusted proforma EPS.','cash_limitation':'FY23/24 cash flow includes Software Integrity while revenues/EPS are continuing operations. No claim of homogeneous cash growth. FY23 total PPE and software investment191.822 = purchases of PPE, net189.618 + capitalization of software development costs2.204. FY24/25 building-sale proceeds16.339/74.279 are separate cash-flow lines, not reductions of PPE purchases. FY26 channel recognition change $60m and divestitures complicate growth.'}
(P/'history.json').write_text(json.dumps(O,indent=2));print({k:(D[k]['normalized_eps'],D[k]['fcf_total']) for k in ['FY2023','FY2024','FY2025','TTM2025','TTM2026']});print(PF)
