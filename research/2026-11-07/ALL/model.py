"""ALL preliminary insurer residual-income model. USD millions unless per-share.
Run: python model.py. No price targets approved.
Sources and judgments separated in sources.json and report.md.
"""
import json,csv
from pathlib import Path
P=Path(__file__).parent
B=30310.; SH=252.1; PRICE=254.81; RF=.0486; ERP=.0441; BETA=.12
# ROE assumptions are after corporate interest/preferred dividends and economic SBC.
# Fixed diluted share base: no free buyback accretion; distributions are cash equivalents.
def model(roe=.20,terminal_roe=.16,ke=.0927,g1=.05,gt=.03,book=B,shares=SH):
 b=book; rows=[]; pv_ri=0; pv_dist=0
 for t in range(1,11):
  w=max(0,(t-5)/5); r=roe+(terminal_roe-roe)*w; g=g1+(gt-g1)*w
  income=b*r; retain=b*g; distribution=income-retain; ri=(r-ke)*b
  pv_ri+=ri/(1+ke)**t; pv_dist+=distribution/(1+ke)**t
  rows.append(dict(year=t,opening_book=b,roe=r,growth=g,net_income_common=income,retained_capital=retain,payout_ratio=1-g/r,distribution=distribution,residual_income=ri,closing_book=b+retain))
  b+=retain
 tv_ri=b*(terminal_roe-ke)/(ke-gt); pv_tv_ri=tv_ri/(1+ke)**10
 tv_ddm=b*(terminal_roe-gt)/(ke-gt); pv_tv_ddm=tv_ddm/(1+ke)**10
 v=book+pv_ri+pv_tv_ri; ddm=pv_dist+pv_tv_ddm
 assert abs(v-ddm)<1e-6
 return dict(value_per_share=v/shares,upside=v/shares/PRICE-1,terminal_RI_share=pv_tv_ri/v,terminal_DDM_share=pv_tv_ddm/v,initial_book=book,shares=shares,ke=ke,roe=roe,terminal_roe=terminal_roe,g1=g1,gt=gt,year1_distribution=rows[0]['distribution'],rows=rows)
cases={'adverso':model(.13,.12,.105,.03,.025),'central':model(),'favorable':model(.24,.18,.085,.06,.03)}
# Same model inverted: first five years ROE solved, terminal ROE remains16%, not unique inference.
def solve(ke,terminal_roe):
 lo,hi=-.2,.8
 for _ in range(100):
  mid=(lo+hi)/2
  if model(mid,terminal_roe,ke)['value_per_share']<PRICE:lo=mid
  else:hi=mid
 return (lo+hi)/2
sens=[dict(ke=k,terminal_roe=r,value=model(.20,r,k)['value_per_share'],implied_initial_roe=solve(k,r)) for k in [.0827,.0927,.1027,.1127] for r in [.12,.14,.16,.18]]
# Reconcile net equity: starting common+common earnings+APIC-treasury net-common distributions+OCI.
equity_bridge=28609+7719+99-2939+55-830-2403
assert equity_bridge==30310
# GAAP aggregate TTM earnings / sum-of-quarter-weighted shares convention from issuer.
periods=[('2025Q4',17345,3803,3788,892,73,14776,4006,209,14.37,264.7),('2026Q1',16941,2428,2797,938,-405,14802,2658,1240,9.25,262.6),('2026Q2',18596,3241,2330,1009,1055,14918,2006,1722,12.51,259.1),('2026Q3',17348,2050,2493,1177,-545,15086,2022,1650,8.03,255.3)]
with (P/'financials_quarterly.csv').open('w') as f:
 w=csv.writer(f);w.writerow(['period','revenue','common_net_income','adjusted_common_income','investment_income','investment_derivative_gain_loss','PL_earned_premium','PL_underwriting_income','catastrophe_loss','diluted_EPS','weighted_diluted_shares']);w.writerows(periods)
# Normalize from economic drivers, not selected target price. Total investment income and
# pretax services/corporate assumption aggregate all remaining group earnings excluding disposals.
normalized={}
for name,cr,nii,other in [('adverso',.97,3500,-400),('central',.93,3800,-300),('favorable',.90,4200,-200)]:
 uw=59582*(1-cr);ni=(uw+nii+other)*.79-117
 normalized[name]=dict(premiums=59582,combined_ratio=cr,underwriting=uw,investment_income=nii,other_net_pretax=other,tax=.21,preferred_dividends=117,normalized_common_income=ni,normalized_roe=ni/B)
results={'status':'partial_research_illustrative_valuation_not_approved','as_of':'2026-11-08','price':{'regular_close':PRICE,'date':'2026-11-06','time':'16:00:00 America/New_York','scanner_last':254.81},'actual_beta_5Y':BETA,'actual_beta_CAPM':RF+BETA*ERP,'assumed_valuation_beta':1.,'rf':RF,'erp':ERP,'cases':cases,'sensitivity':sens,'normalized_earnings':normalized,'equity_bridge':equity_bridge,'TTM_revenue':sum(x[1] for x in periods),'TTM_common_net_income':sum(x[2] for x in periods),'TTM_adjusted_common_income':sum(x[3] for x in periods),'TTM_PL_premiums':sum(x[6] for x in periods),'TTM_PL_underwriting':sum(x[7] for x in periods),'TTM_cat':sum(x[8] for x in periods),'TTM_combined_ratio':1-sum(x[7] for x in periods)/sum(x[6] for x in periods),'market_cap_basic_oct19':PRICE*247.449496,'fully_diluted_equity_value_sep30':PRICE*SH,'historical_pb':{'2023':139.98/59.39,'2024':192.79/72.35,'2025':208.15/108.45,'2026_Nov6_vs_Sept30':PRICE/(B/SH)},'QA':{'RI_equals_DDM':True,'equity_bridge':True,'no_float_debt_deduction':True,'no_excess_cash_addback':True,'no_free_buybacks':True}}
(P/'results.json').write_text(json.dumps(results,indent=2))
print(json.dumps({k:{a:v[a] for a in ['value_per_share','upside','terminal_RI_share','terminal_DDM_share','year1_distribution']} for k,v in cases.items()},indent=2));print('Inverse base',solve(.0927,.16));print(normalized)
