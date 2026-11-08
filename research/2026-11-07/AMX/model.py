"""AMX evidence model. MXN millions unless stated. No valuation output while gates are open."""
import json,csv
from pathlib import Path
D=Path(__file__).parent
annual={
 '2023':dict(revenue=816012.844,ebit=167783.515,da=151786.064,net_parent=76110.617,cfo=248092.195,ppe=131101.509,intangibles=25237.297,leases=39498.197,interest_paid=29031.855,cash_tax=49466.056,benefits_paid=13090.945),
 '2024':dict(revenue=869220.584,ebit=180100.090,da=164128.361,net_parent=22902.025,cfo=239341.121,ppe=113083.319,intangibles=17751.708,leases=45285.610,interest_paid=31082.117,cash_tax=48089.000,benefits_paid=27271.158),
 '2025':dict(revenue=943638.406,ebit=191403.888,da=180804.783,net_parent=82819.082,cfo=272399.022,ppe=114431.308,intangibles=16386.132,leases=51585.889,interest_paid=32325.287,cash_tax=53199.386,benefits_paid=21577.637)}
# Quarterly release convention; CFO explicitly IFRS, other bridge lines retain issuer definitions.
ytd={
 '9M24':dict(revenue=632280,ebit=133709,ebitda=253120,net_parent=18828,cfo=158072,capex=86737,leases=33422,net_interest_bridge=25150,mgmt_fcf=36055),
 '9M25':dict(revenue=698741,ebit=142275,ebitda=277280,net_parent=63685,cfo=186665,capex=84870,leases=38710,net_interest_bridge=27488,mgmt_fcf=52992),
 'Q1_26':dict(revenue=236844,ebit=50519,ebitda=94504,net_parent=23401,cfo=44798,capex=21624,leases=13389,net_interest_bridge=10065,mgmt_fcf=3267),
 'H1_26':dict(revenue=477915,ebit=102333,ebitda=190412,net_parent=47733,cfo=122799,capex=48112,leases=26425,net_interest_bridge=15055,mgmt_fcf=43021),
 '9M26':dict(revenue=728549,ebit=159446,ebitda=292568,net_parent=72015,cfo=204793,capex=75915,leases=39639,net_interest_bridge=26145,mgmt_fcf=74960)}
fy={
 'FY24':dict(revenue=869221,ebit=180100,ebitda=344228,net_parent=22902,cfo=239341,capex=130835,leases=45286,net_interest_bridge=31082,mgmt_fcf=58730),
 'FY25':dict(revenue=943638,ebit=191404,ebitda=372209,net_parent=82819,cfo=272399,capex=130817,leases=51586,net_interest_bridge=32325,mgmt_fcf=81884)}
def subtract(a,b):return {k:a[k]-b[k] for k in a}
def ttm(a,b,c):return {k:a[k]+b[k]-c[k] for k in a}
quarters={'Q4_25':subtract(fy['FY25'],ytd['9M25']),'Q1_26':ytd['Q1_26'],'Q2_26':subtract(ytd['H1_26'],ytd['Q1_26']),'Q3_26':subtract(ytd['9M26'],ytd['H1_26'])}
ttms={'TTM_Sep25':ttm(fy['FY24'],ytd['9M25'],ytd['9M24']),'TTM_Sep26':ttm(fy['FY25'],ytd['9M26'],ytd['9M25'])}
for r in [*quarters.values(),*ttms.values()]:
 r['ebit_margin']=r['ebit']/r['revenue'];r['cash_residual_not_fcff']=r['cfo']-r['capex']-r['leases']-r['net_interest_bridge']
bridge={'cfo_9m26':204793,'lease_payments':-39639,'net_interest':-26145,'benefit_addback':13013,'investing_other':-1147,'capex':-75915}
assert sum(bridge.values())==74960
cash_growth=74960-52992
gates=[
 'Reconcile interim IFRS cash components, capex/spectrum and lease interest against management bridge; consolidated CFO alone does not normalize taxes, capital working or pension cash.',
 'Update Desktop post-September purchase consideration, acquired debt/cash and subsequent minority offer; add its operating economics and avoid double-counting minority.',
 'Value current noncontrolling interests (A1 39%, EuroTeleSites 43% and others), investments and pension deficit with consistent claims treatment.',
 'Separate mandatory spectrum/physical reinvestment from timing relief, preserve funded terminal reinvestment and country/currency-consistent discounting.',
 'Resolve current FX, pension cash obligations and material tax/legal exposures before issuing equity value or entry approval.'
]
result=dict(ticker='AMX',as_of='2026-11-08',status='partial_research_no_entry_approval',currency='MXN million',price_usd=25.72,price_session='NYSE regular close 2026-11-06 16:00 EST corroborated by ChartExchange',ads_common_ratio=20,annual=annual,quarterly=quarters,paired_ttm=ttms,management_cash_bridge_9m26=bridge,diagnostics={'fcf_growth_pct':cash_growth/52992*100,'tax_and_capex_contribution_pct':((43992-34287)+(84870-75915))/cash_growth*100,'ebitda_after_leases_adjusted_growth_pct':(241238/238261-1)*100,'ttm_ebit_growth_pct':(ttms['TTM_Sep26']['ebit']/ttms['TTM_Sep25']['ebit']-1)*100},valuation={'fair_value':None,'central_range':None,'entry_price':None,'entry_approved':False,'method_intended':'Normalized FCFF, blocked before valuation execution','blockers':gates})
result['interim_ifrs_9m26']={'source':'https://s22.q4cdn.com/604986553/files/content_files/ReportePrevio.pdf','pages':'37-43, 69-70','cfo':204793.006,'cfo_prior':186665.362,'ppe':73501.055,'ppe_prior':76842.792,'intangibles':2413.975,'intangibles_prior':8027.328,'cash_tax':33538.748,'cash_tax_prior':43989.999,'interest_received_in_cfo':4205.439,'interest_paid_financing':26145.210,'investing_cf':-34971.409,'financing_cf':-129978.633,'fx':-430.600,'opening_cash':34954.355,'closing_cash':74366.719,'other_investing_inflow':37321.877,'employee_benefits_longterm':205459.394,'employee_benefits_shortterm':26206.444,'nci_book':64974.389}
i=result['interim_ifrs_9m26']
assert abs(i['cfo']+i['investing_cf']+i['financing_cf']+i['fx']+i['opening_cash']-i['closing_cash'])<.001
assert abs(i['ppe']+i['intangibles']-75915.03)<.001
result['diagnostics']['intangible_share_capex_reduction_pct']=(i['intangibles_prior']-i['intangibles'])/(i['ppe_prior']+i['intangibles_prior']-i['ppe']-i['intangibles'])*100
result['diagnostics']['tax_share_cfo_increase_pct']=(i['cash_tax_prior']-i['cash_tax'])/(i['cfo']-i['cfo_prior'])*100
(D/'results.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
with (D/'history.csv').open('w') as f:
 w=csv.writer(f);w.writerow(['period',*next(iter(quarters.values())).keys()]);
 for p,r in {**quarters,**ttms}.items():w.writerow([p,*r.values()])
print(json.dumps({'diagnostics':result['diagnostics'],'ttm':ttms,'quarters':quarters},indent=2))
