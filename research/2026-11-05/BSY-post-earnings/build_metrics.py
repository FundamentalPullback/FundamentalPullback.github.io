import json,csv
from pathlib import Path
p=Path(__file__).parent
annual=[{'period':'2023','revenue':1228.413,'gross_profit':962.330,'ebit':230.542,'net_income_group':326.787,'cfo':416.696,'capex_software':25.002,'sbc':72.972,'dcp_mtm':13.580,'diluted_eps':1.0,'acquisitions_cash':26.023}, {'period':'2024','revenue':1353.095,'gross_profit':1095.328,'ebit':302.150,'net_income_group':234.433,'cfo':435.292,'capex_software':14.046,'sbc':74.417,'dcp_mtm':12.382,'diluted_eps':.72,'acquisitions_cash':130.407},{'period':'2025','revenue':1501.779,'gross_profit':1224.249,'ebit':362.621,'net_income_group':277.794,'cfo':538.464,'capex_software':18.255,'sbc':72.576,'dcp_mtm':14.409,'diluted_eps':.85,'acquisitions_cash':93.252}]
# 2023 group net income is shown, not parent attributable; flag explicitly rather than disguise.
annual[0]['net_income_scope']='group income consistently for annual periods'
annual_shares={'2023':(312.358823,332.503633),'2024':(314.886615,333.774167),'2025':(314.690707,333.089213)} # S3 10-K, annual statement/EPS note, source_notes.json
for a in annual:
 a['weighted_average_basic_shares_m'],a['weighted_average_diluted_shares_m']=annual_shares[a['period']]
 a['fcf']=a['cfo']-a['capex_software'];a['fcf_less_total_sbc']=a['fcf']-a['sbc'];a['ebit_margin']=a['ebit']/a['revenue'];a['ebit_ex_dcp_mtm']=a['ebit']+a['dcp_mtm'];a['normalized_nopat_21pct']=a['ebit_ex_dcp_mtm']*.79
 a['fcf_per_basic_share']=a['fcf']/a['weighted_average_basic_shares_m'];a['fcf_less_total_sbc_per_basic_share']=a['fcf_less_total_sbc']/a['weighted_average_basic_shares_m']
quarter=[{'period':'Q4 2025','revenue':391.582,'gross_profit':320.682,'ebit':78.510,'net_income_parent':58.638,'cfo':141.588,'capex_software':5.419,'dcp_mtm':2.038,'diluted_eps':.18}, {'period':'Q1 2026','revenue':424.181,'gross_profit':350.407,'ebit':126.260,'net_income_parent':95.386,'cfo':193.408,'capex_software':5.551,'dcp_mtm':-1.074,'diluted_eps':.30},{'period':'Q2 2026','revenue':410.727,'gross_profit':336.740,'ebit':88.608,'net_income_parent':78.573,'cfo':71.513,'capex_software':7.715,'dcp_mtm':11.661,'diluted_eps':.25},{'period':'Q3 2026','revenue':421.507,'gross_profit':349.551,'ebit':122.623,'net_income_parent':89.933,'cfo':109.434,'capex_software':7.994,'dcp_mtm':-.786,'diluted_eps':.29}]
for q in quarter:
 q['fcf']=q['cfo']-q['capex_software'];q['ebit_margin']=q['ebit']/q['revenue'];q['ebit_ex_dcp_mtm']=q['ebit']+q['dcp_mtm']
ttm=[]
for label,rev,gross,ebit,ni,cfo,capex,sbc,dcp in [('TTM Sep2025',1460.019,1185.477,345.523,269.316,478.508,18.383,71.598,11.088),('TTM Sep2026',1647.997,1357.38,416.001,322.53,515.943,26.679,82.339,11.839)]:
 ttm.append(dict(period=label,revenue=rev,gross_profit=gross,ebit=ebit,net_income_parent=ni,cfo=cfo,capex_software=capex,sbc=sbc,dcp_mtm=dcp,fcf=cfo-capex,fcf_less_total_sbc=cfo-capex-sbc,ebit_ex_dcp_mtm=ebit+dcp,normalized_nopat_21pct=(ebit+dcp)*.79,ebit_margin=ebit/rev))
bridge=[('Net income',263.861-219.127),('D&A',46.399-50.125),('Deferred taxes',27.244-23.339),('SBC',64.8-55.037),('DCP MTM',9.801-12.371),('Debt issuance cost amortization',3.266-5.682),('Derivative fair value',-4.752-9.293),('FX remeasurement',-.047-1.194),('Other noncash',-11.381-(-1.154)),('Receivables',3.326-40.813),('Prepaids',-7.33-2.128),('Payables and accruals',-18.241-(-36.984)),('Deposits',23.586-42.359),('Deferred revenues',-28.109-(-24.369)),('Tax payables',1.932-(-2.085))]
checks={'cfo_delta':374.355-396.876,'bridge_sum':sum(v for k,v in bridge),'fcf_delta':353.095-384.04,'ttm_revenue_change':1647.997/1460.019-1,'ttm_normalized_nopat_change':427.84/356.611-1,'ttm_fcf_less_sbc_change':406.925/388.527-1,'ttm_fcf_change':489.264/460.125-1,'nine_month_fcf_change':353.095/384.04-1,'nine_month_fcf_less_sbc_change':288.295/329.003-1,'snapshot_pullback':1-47.09/50.52,'required_q4_fcf_low':500-353.095,'required_q4_fcf_high':570-353.095,'cash_settlement_shares_approx':317.691424-6.908797,'bridge':1165-(150.874-50)+(111.985+4.687)+.048}
assert abs(checks['cfo_delta']-checks['bridge_sum'])<1e-8
assert abs(sum(q['revenue'] for q in quarter)-1647.997)<1e-8
assert abs(sum(q['fcf'] for q in quarter)-489.264)<1e-8
assert abs(checks['bridge']-1180.846)<1e-8
# Historical FCF/share uses reported basic shares, not the valuation cash-settlement denominator.
# FY2024 is leap year; TTM and derived quarters are reconstructed by calendar-day weights.
basic9_2024=314.820679;basic9_2025=314.826779;basic9_2026=311.671484
sharettm25=(366*314.886615+273*basic9_2025-274*basic9_2024)/365
sharettm26=(365*314.690707+273*basic9_2026-273*basic9_2025)/365
quarter_basic=[(365*314.690707-273*basic9_2025)/92,(181*312.227764-91*311.784740)/90,311.784740,310.474561]
for q,b in zip(quarter,quarter_basic):
 q['weighted_average_basic_shares_m']=b;q['fcf_per_basic_share']=q['fcf']/b
for a,b in zip(ttm,[sharettm25,sharettm26]):
 a['weighted_average_basic_shares_m']=b;a['fcf_per_basic_share']=a['fcf']/b;a['fcf_less_total_sbc_per_basic_share']=a['fcf_less_total_sbc']/b
metrics=dict(annual=annual,quarters=quarter,ttm=ttm,cfo_bridge=bridge,checks=checks,per_share_method={'numerator':'CFO minus property/equipment and capitalized software; historical levered cash flow, not FCFF', 'denominator':'Published weighted-average basic shares including phantom shares under issuer accounting; annual reported, TTM and Q4 2025/Q1 2026 derived using calendar-day weights', 'not_equivalent_to':'Diluted FCF/share or 311m model cash-settlement shares', 'sources':['S1','S3','S4','S7'], 'basic_9m_2024':basic9_2024,'basic_9m_2025':basic9_2025,'basic_9m_2026':basic9_2026})
(p/'metrics.json').write_text(json.dumps(metrics,indent=2))
for name,rows in [('annual',annual),('quarters',quarter),('ttm',ttm)]:
 fields=list(dict.fromkeys(k for row in rows for k in row))
 with (p/f'{name}.csv').open('w') as f:
  w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
print(json.dumps(checks,indent=2))
