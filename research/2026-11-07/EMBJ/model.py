"""Auditable historical cash model. USD millions; no fair value or trade approval.
Annual audited figures control over release roundings. Both TTM constructions are retained.
"""
from pathlib import Path
import json,csv
P=Path(__file__).parent
cols=['revenue','ebit','net_income_parent','cfo','physical_capex','intangible_capex','da','lease_payments','customer_advances_change','inventory_cash_change']
raw={
'FY2023':[5268.5,314.5,164.0,617.0,238.7,192.1,241.7,13.6,576.8,-287.1],
'FY2024':[6394.7,667.5,352.5,871.2,200.4,265.8,243.6,18.8,748.1,-370.2],
'FY2025':[7577.5,607.6,351.9,870.0,187.2,296.7,259.5,23.8,150.7,-382.2],
'H12024':[2390.8,124.0,128.1,-348.0,100.8,130.9,101.9,7.8,60.1,-665.3],
'H12025':[2922.2,230.7,152.0,-259.9,119.1,132.0,110.2,12.0,32.2,-689.1],
'H12026':[3682.0,367.5,246.0,59.0,139.2,129.5,118.8,12.2,304.9,-452.6],
'Q32025':[2003.5,159.6,116.6,268.9,56.4,82.2,71.5,6.3,-4.3,-68.7],
'Q42025':[2651.8,217.3,83.3,878.4,29.0,82.5,77.8,5.4,122.8,375.6],
'Q12026':[1446.7,81.7,33.4,-388.4,76.0,80.0,53.2,6.2,3.7,-410.1],
'Q22026':[2235.3,285.8,212.6,447.4,63.2,49.5,65.6,6.0,301.2,-42.5]}
a={p:dict(zip(cols,v)) for p,v in raw.items()}
for name,fy,old,new in [('TTM2025Q2','FY2024','H12024','H12025'),('TTM2026Q2','FY2025','H12025','H12026')]:
 a[name]={k:round(a[fy][k]-a[old][k]+a[new][k],4) for k in cols}
a['TTM2026Q2_quarter_sum']={k:round(sum(a[q][k] for q in ['Q32025','Q42025','Q12026','Q22026']),4) for k in cols}
for p,d in a.items():
 d['cash_fcf']=round(d['cfo']-d['physical_capex']-d['intangible_capex'],4)
 d['cash_after_leases']=round(d['cash_fcf']-d['lease_payments'],4)
 d['ebit_margin']=d['ebit']/d['revenue']
 d['cash_fcf_to_parent_income']=d['cash_fcf']/d['net_income_parent']
 d['source']='S1' if p.startswith('FY') else ('S4' if p=='H12024' else ('S3' if p in ['Q32025','Q42025'] else ('derived' if p.startswith('TTM') else 'S2')))
result={'ticker':'EMBJ','as_of':'2026-11-08','units':'USD millions unless stated','status':'material_partial_historical_cash_model','fair_value':None,'price':74.08,'price_date':'2026-11-06','ads_common_ratio':4,'actuals':a,
'paired_ttm_growth':{k:a['TTM2026Q2'][k]/a['TTM2025Q2'][k]-1 for k in ['revenue','ebit','net_income_parent','cash_fcf']},
'quarter_vs_annual_ttm_difference':{k:round(a['TTM2026Q2_quarter_sum'][k]-a['TTM2026Q2'][k],4) for k in cols+['cash_fcf']},
'cash_bridge_q22026':{'cfo':447.4,'financial_investments_adjustment':13.5,'net_ppe':-59.6,'intangibles':-49.5,'consolidated_adjusted_fcf':351.8,'eve_exclusion':49.2,'headline_fcf_ex_eve':401.0,'gross_cash_fcf':334.7},
'normalization':{'q22026_reported_ebit':285.8,'extraordinary_tax_credit':68,'reported_ebit_ex_credit':217.8,'adjusted_ex_eve_ebit':296.9,'adjusted_ex_eve_ex_credit':228.9,'tariffs_not_added_back':8,'fy2024_boeing_recovery':150},
'balance_q22026':{'parent_cash_and_investments':1937.4,'parent_debt':2151.9,'parent_net_debt':214.5,'eve_cash_and_investments':403.2,'eve_debt':312.3,'consolidated_lease_liabilities':121.7,'supplier_finance':53.8,'contract_liabilities':3740.1,'inventories':3702.3,'book_minority_interest':371.8,'balance_sheet_cash':1392.4,'cash_flow_cash':1387.3},
'valuation_gate':{'forecast_funded':False,'current_economic_shares_reconciled':False,'eve_parent_bridge_reconciled':False,'wacc_validated':False,'terminal_reinvestment_calibrated':False,'comps_verified':False,'approved':False}}
(P/'results.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
with (P/'actuals.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=['period']+list(next(iter(a.values())).keys()));w.writeheader();w.writerows(dict(period=p,**d) for p,d in a.items())
assert abs(447.4+13.5-59.6-49.5+49.2-401)<.01
assert abs(a['TTM2026Q2']['revenue']-8337.3)<.01
print(json.dumps({'ttm':a['TTM2026Q2'],'prior':a['TTM2025Q2'],'growth':result['paired_ttm_growth'],'discrepancies':result['quarter_vs_annual_ttm_difference']},indent=2))
