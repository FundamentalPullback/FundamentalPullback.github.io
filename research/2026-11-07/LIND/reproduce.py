import json, pathlib
p=pathlib.Path(__file__).parent
# USD thousands. Primary 10-K FY2025, Q3 2026 10-Q, issuer earnings releases.
a={
'FY2023':dict(revenue=569543,ebit=10599,net_income=-40876,common_income=-49983,cfo=25441,capex=29963,eps_diluted=-.94),
'FY2024':dict(revenue=644727,ebit=21553,net_income=-28195,common_income=-35820,cfo=92355,capex=33520,eps_diluted=-.67),
'FY2025':dict(revenue=771019,ebit=45487,net_income=-24225,common_income=-34647,cfo=111583,capex=47745,eps_diluted=-.63),
'9M2024':dict(revenue=496118,ebit=29124,net_income=-3005,common_income=-9585,cfo=90675,capex=23647),
'9M2025':dict(revenue=587838,ebit=50993,net_income=-1383,common_income=-9833,cfo=97141,capex=36778),
'9M2026':dict(revenue=676411,ebit=70320,net_income=32795,common_income=28835,cfo=111339,capex=18829),
'Q4_2025':dict(revenue=183181,ebit=-5506,net_income=-22842,common_income=-24814,cfo=111583-97141,capex=47745-36778,eps_diluted=-.45),
'Q1_2026':dict(revenue=208013,ebit=15615,common_income=6003,cfo=49474,capex=6886,eps_diluted=.09),
'Q2_2026':dict(revenue=199247,ebit=11954,common_income=-1406,cfo=108529-49474,capex=14885-6886,eps_diluted=-.02),
'Q3_2026':dict(revenue=269151,ebit=42751,common_income=24239,cfo=111339-108529,capex=18829-14885,eps_diluted=.36)}
for end,fy,new,old in [('TTM2026','FY2025','9M2026','9M2025'),('TTM2025','FY2024','9M2025','9M2024')]:
 a[end]={k:a[fy][k]+a[new][k]-a[old][k] for k in ['revenue','ebit','net_income','common_income','cfo','capex']}
for v in a.values():
 v['fcf']=v['cfo']-v['capex'];v['operating_margin']=v['ebit']/v['revenue'];v['common_margin']=v['common_income']/v['revenue']
wa=(55303371*92+64206682*273)/365
checks={'ttm_basic_selected_input_share_proxy':wa,'ttm_basic_eps_selected_input_proxy_not_reconciled':4021000/wa,'ttm_fcf_per_share_selected_input_proxy_not_reconciled':a['TTM2026']['fcf']*1000/wa,'sum_reported_quarterly_diluted_eps':sum(a[q]['eps_diluted'] for q in ['Q4_2025','Q1_2026','Q2_2026','Q3_2026']),'eps_fy_plus_ytd_less_prior_ytd':-.63+.44-(-.18),'quarter_vs_ytd_common_gap_thousands':sum(a[q]['common_income'] for q in ['Q1_2026','Q2_2026','Q3_2026'])-a['9M2026']['common_income'],'quarter_vs_ytd_ebit_gap_thousands':sum(a[q]['ebit'] for q in ['Q1_2026','Q2_2026','Q3_2026'])-a['9M2026']['ebit'],'status':'PENDING_SOURCE_DENOMINATOR_RECONCILIATION_AND_EPS_DEFINITION_NOT_APPROVED'}
checks['source_denominator_audit'] = {
 'q1_2026_common_income_usd': 6003000,
 'q1_2026_diluted_shares_reported': 61113044,
 'q1_2026_eps_ratio': 6003000/61113044,
 'q1_2026_eps_ratio_rounded_2dp': round(6003000/61113044,2),
 'q1_2026_eps_diluted_reported': .09,
 'six_month_basic_shares_from_quarter_days': (60247385*90+65473335*91)/181,
 'six_month_basic_shares_reported': 63529776,
 'six_month_basic_shares_gap_reported_less_quarter_days': 63529776-(60247385*90+65473335*91)/181,
 'q4_2025_basic_shares_implied_by_fy_and_9m_days': (54970812*365-54859959*273)/92,
 'q4_2025_basic_shares_reported': 55303371,
 'q4_2025_basic_shares_gap_reported_less_implied': 55303371-(54970812*365-54859959*273)/92,
 'nine_month_basic_shares_from_6m_and_q3_days': (63529776*181+65560483*92)/273,
 'nine_month_basic_shares_reported': 64206682,
 'nine_month_gap_proxy_less_reported': (63529776*181+65560483*92)/273-64206682,
 'numerator_review_required': 'Review two-class participating preferred allocations and period-specific dilution before any hypothetical positive TTM GAAP-style EPS.',
 'finding': 'Unexplained source-level denominator and EPS discrepancies. Do not assume rounding or certify a reconstructed TTM denominator. Selected-input proxies are not a gate pass.',
 'qa_status': 'OPEN_BLOCKER'
}
assert a['TTM2026']['fcf']==95985
assert a['TTM2026']['ebit']==64814
assert a['TTM2026']['common_income']==4021
(p/'inputs_calculations.json').write_text(json.dumps({'units':'USD thousands except EPS and share counts','financials':a,'checks':checks},indent=2))
(p/'QA.json').write_text(json.dumps({'checks':checks},indent=2))
print(json.dumps({'TTM2026':a['TTM2026'],'TTM2025':a['TTM2025'],'checks':checks},indent=2))
