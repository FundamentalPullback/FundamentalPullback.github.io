import json
from pathlib import Path
P=Path(__file__).resolve().parent
a={2023:dict(sales=14889,ebit=560,ni=502,cfo=1532,capex=420,da=522,sbc=80),2024:dict(sales=15086,ebit=1112,ni=844,cfo=1486,capex=447,da=500,sbc=126),2025:dict(sales=15366,ebit=1115,ni=816,cfo=1293,capex=470,da=496,sbc=162)}
h={2024:dict(sales=7108,ebit=498,ni=364,cfo=579,capex=182,da=247),2025:dict(sales=7188,ebit=552,ni=409,cfo=308,capex=181,da=243,sbc=71),2026:dict(sales=7148,ebit=1121,ni=840,cfo=550,capex=289,da=259,sbc=85)}
q3=dict(sales=3942,ebit=334,ni=236,cfo=607-308,capex=327-181)
q4={k:a[2025][k]-h[2025][k]-q3[k] for k in q3}
q1=dict(sales=3497,ebit=445,ebit_normalized=182,ni=339,ni_adjusted=145,cfo=213,capex=135)
q2={k:h[2026][k]-q1[k] for k in ['sales','ebit','ni','cfo','capex']};q2.update(ebit_normalized=259,ni_adjusted=190)
h[2026]['ebit_normalized']=1121-313+50-417
h[2026]['ni_adjusted']=840-232+38-311
for o in [*a.values(),*h.values(),q3,q4,q1,q2]:
 o['fcf_reported']=o['cfo']-o['capex'];o['operating_margin_reported']=o['ebit']/o['sales']
 if 'ebit_normalized' in o:o['operating_margin_normalized']=o['ebit_normalized']/o['sales']
ttm={k:a[2025][k]+h[2026][k]-h[2025][k] for k in ['sales','ebit','ni','cfo','capex','da','sbc','fcf_reported']}
prior={k:a[2024][k]+h[2025][k]-h[2024][k] for k in ['sales','ebit','ni','cfo','capex','da','fcf_reported']}
ttm['ebit_normalized']=1115+441-552
ttm['ni_adjusted']=816+335-409
ratios={'q1_ebit_normalized_yoy':182/(552-292)-1,'q2_ebit_normalized_yoy':259/292-1,'h1_ebit_normalized_yoy':441/552-1,'ttm_ebit_normalized_yoy':1004/prior['ebit']-1,'h1_ni_adjusted_yoy':335/409-1,'ttm_ni_adjusted_yoy':742/prior['ni']-1,'ttm_sales_yoy':ttm['sales']/prior['sales']-1,'ttm_reported_fcf_yoy':ttm['fcf_reported']/prior['fcf_reported']-1}
cash_bridge={'h1_reported_fcf':261,'less_net_settlement_and_concurrent_donation_pretax':263,'less_cash_tariff_refund_and_interest_received':100,'h1_fcf_after_removing_identified_pretax_cash_inflows_before_cash_tax_normalization':261-263-100,'ttm_fcf_after_removing_identified_pretax_cash_inflows_before_cash_tax_normalization':ttm['fcf_reported']-263-100,'warning':'These residuals are diagnostic cash bridges, NOT certified normalized FCF or FCFF. Cash tax allocation, seasonal working capital, SBC, lease and reinvestment reconciliation remain necessary for valuation. Do not subtract the $417m accrued EBIT gain from CFO; only $95m cash refund plus $5m interest was received. $417m refund receivable and $95m vendor liability remain at August 1.'}
guide={'sales_low':15366*1.01,'sales_high':15366*1.015,'ebit_low':15366*1.01*.074,'ebit_high':15366*1.015*.076,'eps_low':2.35,'eps_high':2.45,'diluted_shares':367,'capex':650}
guide['ebit_growth_low']=guide['ebit_low']/1115-1;guide['ebit_growth_high']=guide['ebit_high']/1115-1
guide['implied_h2_ebit_low']=guide['ebit_low']-441;guide['implied_h2_ebit_high']=guide['ebit_high']-441
guide['implied_h2_ebit_growth_low']=guide['implied_h2_ebit_low']/(1115-552)-1;guide['implied_h2_ebit_growth_high']=guide['implied_h2_ebit_high']/(1115-552)-1
guide['forward_pe_low']=23.75/2.45;guide['forward_pe_high']=23.75/2.35
annual_ebit_reconciliation={
 2023:dict(reported=560,restructuring_costs=93,building_sale_gain=47,company_adjusted=560+93-47,scope='Company non-GAAP reconciliation, not automatic economic exclusion of restructuring. FY2023 is outside both TTM windows.'),
 2024:dict(reported=1112,additional_ebit_adjustments_identified=0,retained=1112,scope='Reported EBIT retained. FY2024 H1, including Q2 credit-card-related income, is removed when constructing prior TTM.'),
 2025:dict(reported=1115,additional_ebit_adjustments_identified=0,retained=1115,scope='Reported EBIT retained; company reported no adjusted fiscal 2025 metrics.')
}
out=dict(units='USD million except per-share, ratios and dates',annual_reported=a,annual_ebit_reconciliation=annual_ebit_reconciliation,half_year=h,last_four_quarters={'Q3_FY2025':q3,'Q4_FY2025_derived':q4,'Q1_FY2026':q1,'Q2_FY2026':q2},ttm_ended_20260801=ttm,prior_ttm_ended_20250802=prior,growth=ratios,cash_bridge=cash_bridge,fy2026_company_guidance_and_derived=guide)
assert sum(q['ebit_normalized'] if 'ebit_normalized' in q else q['ebit'] for q in out['last_four_quarters'].values())==1004
assert sum(q['fcf_reported'] for q in out['last_four_quarters'].values())==957
assert h[2026]['ebit_normalized']==441 and ttm['ebit_normalized']==1004 and prior['ebit']==1166
(P/'calculations.json').write_text(json.dumps(out,ensure_ascii=False,indent=2))
print(json.dumps(out,ensure_ascii=False,indent=2))
