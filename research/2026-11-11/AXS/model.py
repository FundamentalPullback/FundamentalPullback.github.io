"""AXS research model. USD millions except per share. Python standard library only.
Source actuals: q3supp.htm pp3,5,16-17 and FY2025 10-K pp63,64,78-79,115.
Analyst assumptions are explicitly segregated; no price is certified executable.
"""
import json,csv,pathlib
P=pathlib.Path(__file__).parent
B=5749.455;shares=72.727;price=107.96
fy={
'2023':dict(npe=5083.781,nii=611.742,gaap_common=346.042,op_common=486.133,combined=99.9,ay_excat_loss=55.9,cat_points=2.7,reserve_points=8.1,op_roe=11.0,bvps=54.06),
'2024':dict(npe=5306.235,nii=759.229,gaap_common=1051.536,op_common=952.035,combined=92.3,ay_excat_loss=55.7,cat_points=4.3,reserve_points=-.5,op_roe=18.6,bvps=65.27),
'2025':dict(npe=5714.609,nii=766.903,gaap_common=978.648,op_common=1024.212,combined=89.8,ay_excat_loss=56.3,cat_points=2.8,reserve_points=-1.6,op_roe=18.1,bvps=77.20)}
qs=[dict(period='Q4 2025',npe=1528.475,nii=186.992,gaap_common=282.044,op_common=249.547,cat=29.855,reserve_release=29.852,combined=90.4,eps=3.67,op_eps=3.25,interest=16.844,amort=2.396,other_insurance=4.383),dict(period='Q1 2026',npe=1480.466,nii=184.740,gaap_common=247.204,op_common=256.887,cat=47.800,reserve_release=18.062,combined=89.8,eps=3.29,op_eps=3.42,interest=16.426,amort=2.396,other_insurance=5.649),dict(period='Q2 2026',npe=1518.984,nii=181.594,gaap_common=250.532,op_common=210.649,cat=80.334,reserve_release=14.836,combined=93.1,eps=3.38,op_eps=2.84,interest=16.838,amort=2.396,other_insurance=5.601),dict(period='Q3 2026',npe=1619.334,nii=211.367,gaap_common=201.515,op_common=229.203,cat=74.508,reserve_release=14.843,combined=94.0,eps=2.75,op_eps=3.12,interest=16.680,amort=5.726,other_insurance=5.738)]
# Q2 op income from Q2 supplement p17; Q1 = H1 467.536 minus Q2 210.649.
ttm={k:sum(q[k] for q in qs) for k in ['npe','nii','gaap_common','op_common','cat','reserve_release','interest','amort','other_insurance','eps','op_eps']}
assumptions={
'bear':dict(underlying_cr=.92,cat_ratio=.06,nii=730,tax=.21,restructure=20,ke=.13,g=.02,terminal_roe=.105,initial_reserve_shock=300),
'base':dict(underlying_cr=.90,cat_ratio=.045,nii=800,tax=.20,restructure=15,ke=.12,g=.03,terminal_roe=.13,initial_reserve_shock=0),
'bull':dict(underlying_cr=.885,cat_ratio=.035,nii=840,tax=.19,restructure=10,ke=.11,g=.04,terminal_roe=.155,initial_reserve_shock=0)}
# Reserve releases normalized to zero. Group combined ratio includes corporate G&A:
# do NOT subtract corporate expense again. Fee economics already in expense ratio / other insurance income.
def run(a):
 income=(ttm['npe']*(1-a['underlying_cr']-a['cat_ratio'])+a['nii']+ttm['other_insurance']-ttm['interest']-ttm['amort']-a['restructure'])*(1-a['tax'])-30.25
 roe=income/B;book=B;pvri=0;pvd=0;rows=[]
 for year in range(1,11):
  r=roe if year<=5 else roe+(a['terminal_roe']-roe)*(year-5)/5
  earning=book*r-(a['initial_reserve_shock']*(1-a['tax']) if year==1 else 0)
  retention=book*a['g'];dist=earning-retention;end=book+retention
  residual=earning-book*a['ke'];df=(1+a['ke'])**year
  pvri+=residual/df;pvd+=dist/df
  rows.append(dict(year=year,book_open=book,roe=r,income=earning,retention=retention,distribution=dist,book_close=end,residual_income=residual,discount_factor=df))
  book=end
 terminal_ri=book*(a['terminal_roe']-a['ke'])/(a['ke']-a['g']);terminal_equity=book*(a['terminal_roe']-a['g'])/(a['ke']-a['g'])
 value=(B+pvri+terminal_ri/(1+a['ke'])**10)/shares
 ddm=(pvd+terminal_equity/(1+a['ke'])**10)/shares
 assert abs(value-ddm)<1e-9
 assert all(x['distribution']>=0 for x in rows)
 return dict(normalized_income=income,normalized_eps=income/shares,starting_roe=roe,fair_value=value,ddm_crosscheck=ddm,price_upside=value/price-1,margin_of_safety=1-price/value,exploratory_price_at_25pct_discount=value*.75,year1_distribution=rows[0]['distribution'],terminal_pv_fraction=(terminal_equity/(1+a['ke'])**10/shares)/value,rows=rows)
results={k:run(v) for k,v in assumptions.items()}
sensitivity=[]
for ke in [.10,.11,.12,.13,.14]:
 for terminal in [.11,.12,.13,.14,.15,.16]:
  a=assumptions['base']|dict(ke=ke,terminal_roe=terminal);sensitivity.append(dict(ke=ke,terminal_roe=terminal,value=run(a)['fair_value']))
# Reverse model: constant operating ROE all ten years and terminal, g3%.
required=.03+(price/(B/shares))*(.12-.03)
# Reverse base earnings normalization holding underlying ratio perpetual and all other assumptions fixed.
# To qualify for 25% margin of safety required intrinsic value is price/.75.
reverse_roe_mos=.03+((price/.75)/(B/shares))*(.12-.03)
output=dict(status='partial_research_model_not_approved',canonical_fair_value=None,canonical_target=None,canonical_entry_price=None,canonical_max_price=None,entry_approved=False,discount_25pct_status='exploratory analyst sensitivity; not user plan rule or necessary rejection criterion',as_of='2026-11-11',price=dict(value=price,date='2026-11-10',basis='user scanner Last; not certified close'),book=B,shares=shares,book_per_share=B/shares,actual_fy=fy,actual_quarters=qs,ttm=ttm,assumptions=assumptions,results=results,sensitivity=sensitivity,reverse=dict(perpetual_roe_for_price=required,exploratory_perpetual_roe_at_25pct_discount=reverse_roe_mos),rate_sensitivity=dict(afs_assets=13691.574,duration=3.2,plus100bp_pretax=-13691.574*.032,plus100bp_aftertax_per_share=-13691.574*.032*.8/shares,full_portfolio_100bp_reinvestment_increment=14139.802*.01,credit_and_rate_2025_pretax=668.241))
(P/'model_results.json').write_text(json.dumps(output,indent=2))
for k,r in results.items():
 with (P/('forecast_'+k+'.csv')).open('w') as f:
  w=csv.DictWriter(f,fieldnames=r['rows'][0]);w.writeheader();w.writerows(r['rows'])
print(json.dumps({k:{x:v for x,v in r.items() if x!='rows'} for k,r in results.items()},indent=2));print('TTM',ttm,'reverse',output['reverse'])
