import json,csv,pathlib
p=pathlib.Path(__file__).parent
fields=['revenue','ebit','net_income','eps_diluted','cfo','capex','da','sbc']
rows={
'FY2023':[7429,1285,878,3.84,954,298,269,43],
'FY2024':[7307,1266,798,3.61,886,226,282,40],
'FY2025':[7291,1126,649,3.11,1102,237,254,31],
'H1_2024':[2910,370,239,1.06,30,101,142,22],
'H1_2025':[2974,367,169,.79,145,93,128,18],
'H1_2026':[2892,447,301,1.49,316,98,120,10],
'9M_2025':[4567,527,246,1.17,225,174,191,25],
'Q3_2025':[1594,161,77,.37,80,81,63,7],
'Q1_2026':[1378,231,183,.90,244,49,61,8],
'Q2_2026':[1514,216,118,.58,72,49,59,2],
}
r={k:dict(zip(fields,v)) for k,v in rows.items()}
r['Q4_2025_derived']={f:r['FY2025'][f]-r['9M_2025'][f] for f in fields}
for label,year,cur,prior in [('TTM_20260801','FY2025','H1_2026','H1_2025'),('TTM_20250802','FY2024','H1_2025','H1_2024')]:
 r[label]={f:round(r[year][f]+r[cur][f]-r[prior][f],4) for f in fields}
for k,v in r.items():
 v['fcf_cfo_less_capex']=v['cfo']-v['capex'];v['ebit_margin']=v['ebit']/v['revenue'];v['core_ebit_retaining_costs']=v['ebit']
for k,removal in [('H1_2026',168),('Q1_2026',88),('Q2_2026',80),('TTM_20260801',168)]:r[k]['core_ebit_retaining_costs']-=removal
json.dump(r,open(p/'history.json','w'),indent=2)
with open(p/'history.csv','w') as f:
 w=csv.DictWriter(f,fieldnames=['period']+list(next(iter(r.values())).keys()));w.writeheader();w.writerows(dict(period=k,**v) for k,v in r.items())
checks={'ttm_sales':r['TTM_20260801']['revenue'],'ttm_core_ebit_growth':r['TTM_20260801']['core_ebit_retaining_costs']/r['TTM_20250802']['core_ebit_retaining_costs']-1,'ttm_fcf':r['TTM_20260801']['fcf_cfo_less_capex'],'ttm_prior_fcf':r['TTM_20250802']['fcf_cfo_less_capex'],'h1_cash_ex_receipts_before_cash_tax_reconciliation':316-98-88-85,'ttm_cash_ex_receipts_before_cash_tax_reconciliation':1031-88-85,'h1_reported_fcf_improvement':218-52,'h1_core_ebit_growth':279/367-1,'pullback':(24.94-21.36)/24.94,'four_quarter_ebit_rounding_difference':sum(r[x]['ebit'] for x in ['Q3_2025','Q4_2025_derived','Q1_2026','Q2_2026'])-r['TTM_20260801']['ebit']}
json.dump(checks,open(p/'validation_checks.json','w'),indent=2)
print(json.dumps(checks,indent=2))
# Executable review tests. Published statements are rounded to USD millions.
assert r['FY2023']['fcf_cfo_less_capex']==656
assert r['FY2024']['fcf_cfo_less_capex']==660
assert r['FY2025']['fcf_cfo_less_capex']==865
assert r['TTM_20260801']['revenue']==7209
assert r['TTM_20260801']['ebit']==1206
assert r['TTM_20260801']['core_ebit_retaining_costs']==1038
assert r['TTM_20250802']['core_ebit_retaining_costs']==1263
assert r['TTM_20260801']['fcf_cfo_less_capex']==1031
assert r['TTM_20250802']['fcf_cfo_less_capex']==783
assert r['Q2_2026']['core_ebit_retaining_costs']==136
assert 216+9-80==145 # Management-adjusted ex-refund, NOT cost-retaining core.
assert 447-88-80==279
assert 316-98-88-85==45 # Pre cash-tax reconciliation, not final normalized FCF.
assert abs(checks['four_quarter_ebit_rounding_difference'])<=1
assert abs(sum(r[x]['revenue'] for x in ['Q3_2025','Q4_2025_derived','Q1_2026','Q2_2026'])-7209)<=1
assert abs(sum(r[x]['net_income'] for x in ['Q3_2025','Q4_2025_derived','Q1_2026','Q2_2026'])-781)<=1
assert r['Q1_2026']['cfo']+r['Q2_2026']['cfo']==316
assert r['Q1_2026']['capex']+r['Q2_2026']['capex']==98
checks['assertions_passed']=18
checks['rounding_tolerance_usd_m']=1
checks['source_map']={'FY2023/FY2024/FY2025':'fy2025: consolidated income and cash-flow statements','H1_2024/H1_2025':'q2_2025: consolidated income and cash-flow statements','H1_2026':'q2_2026: consolidated income and cash-flow statements','9M_2025/Q3_2025':'q3_2025: consolidated income and cash-flow statements','Q1_2026':'q1_2026: consolidated income and cash-flow statements','Q2_2026':'q2_2026 income, cash derived H1 minus Q1','Q4_2025_derived':'fy2025 minus q3_2025 YTD','core_adjustments':'q2_2026 note 1 tariff refunds; MD&A non-GAAP reconciliation and footnotes'}
json.dump(checks,open(p/'validation_checks.json','w'),indent=2)
