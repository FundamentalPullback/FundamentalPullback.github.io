from pathlib import Path
import json,math,importlib.util,csv,hashlib
P=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('prior',P/'model_core.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
price=238.;shares=45.348589;debt=750;rf=.0498;erp=.0441;kd=.06;tax=.28
E=45.034789*price;wE=E/(E+debt)
def wacc(beta):return wE*(rf+beta*erp)+(1-wE)*kd*(1-tax)
wa={label:wacc(beta)for label,beta in [('observed_beta',.73),('base_beta',1),('bear_beta',1.3)]}
# Existing controlled Python DCF preserved. Only evidence-supported rate/time updates and explicitly selected rate sensitivities below.
cases={k:m.model(k,discount=wa[{'bear':'bear_beta','base':'base_beta','bull':'observed_beta'}[k]],stubYears=51/365)for k in ['bear','base','bull']}
def root_price(key,lo,hi,discount):
 f=lambda x:m.model('base',discount=discount,stubYears=51/365,**{key:x})['illustrativePerShare']
 vals=[f(lo+(hi-lo)*i/1000)for i in range(1001)]
 assert min(b-a for a,b in zip(vals,vals[1:]))>=-1e-8
 assert vals[0]<=price<=vals[-1]
 for _ in range(100):
  x=(lo+hi)/2
  if f(x)<price:lo=x
  else:hi=x
 x=(lo+hi)/2
 return {'parameter':key,'value':x,'discount':discount,'price':price,'residual':f(x)-price}
rev=[root_price('growthStart',0,.4,d)for d in [wa['observed_beta'],wa['base_beta'],.10]]
# Favorable bridge sensitivity within the central operating case; not a company value ceiling.
bound=m.model('base',discount=wa['observed_beta'],stubYears=51/365,bridgeDelta=122,shareFactor=45.034789/shares)
checks={
 'client_assets_minus_obligations':3891.3-3891.3,
 'net_debt_ex_client_cash':750-193.9,
 'cash_split_reconciles':3710.6-193.9-3516.7,
 'bank_assets_excluded_from_corporate_cash':True,
 'contract_asset_rollforward':1016.9+154.2-125.7-1045.4,
 'time_awards_rollforward':1133.3+125.8-287.3-352.5-619.3,
 'market_awards_rollforward':166.4+6.8-6.8-50.9-115.5,
 'rsu_rollforward_rounded':76.5+135.1-26.5-6.1-179.1,
 'psu_rollforward_rounded':80.2+134.7-80.1-.2-134.7,
 'cfo_growth_vs_tax_timing':(613.9-482.8)-(65.6+65.4),
 'all_case_fcff_arithmetic':all(abs(z['nopat']-z['selectedNetInvestment']-z['fcff'])<1e-8 for v in cases.values()for z in v['years']),
 'no_claim_current_dilution_certified':True,
 'no_claim_comps_normalized':True
}
inputs={'research_date':'2026-11-11','market_date':'2026-11-10','scanner':{'opportunity':95,'QP':90,'Last':237.96,'source':'delegated current Nov10 scanner; not regular close'},'price_observations':[{'price':238,'session':'regular','time':'2026-11-10 16:00 EST','source':'https://stockanalysis.com/stocks/payc/history/'},{'price':237.96,'session':'extended','time':'2026-11-10 19:30 EST','source':'https://stockanalysis.com/stocks/payc/history/'},{'price':237.95,'session':'reported daily close; conflict unresolved','source':'https://chartexchange.com/symbol/nyse-payc/historical/'}],
'wacc':{'riskfree_treasury_proxy':rf,'rf_source':'https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?field_tdr_date_value=2026&type=daily_treasury_yield_curve','rf_date':'2026-11-10','erp':erp,'erp_source':'https://pages.stern.nyu.edu/~adamodar/New_Home_Page/home.htm?lfrom=202213444','erp_date':'2026-11-01','beta_observed':.73,'beta_source':'https://finance.yahoo.com/quote/PAYC/','beta_method':'5Y monthly; provider beta not independently estimated','beta_base_selected':1,'beta_bear_selected':1.3,'debt_cost_selected':kd,'debt_cost_basis':'Analyst normalized 6%, bracketed against Treasury3M4.30% plus disclosed SOFR margins1.25-2%; 3M Treasury is NOT SOFR and this is NOT an observed borrowing rate. Sensitivity5.55-6.30%.','debt_market_value_proxy':750,'equity_market_cap':E,'tax_selected':tax,'equity_weight':wE,'outputs':wa},
'bank_capital':{'source':'https://www.occ.gov/topics/charters-and-licensing/interpretations-and-decisions/2024/ca1317.pdf','published_condition_date':'2024-02-01','tier1_min':7,'eligible_liquid_min':5.25,'additional_liquidity':'180 days operating expenses','period':'first three years; subsequent amendments/current bank balance not confirmed','not_a_current_distributable_cash_calculation':True},
'guidance':{'source':'https://investors.paycom.com/news/news-details/2026/Paycom-Software-Inc--Reports-Third-Quarter-2026-Results/default.aspx','FY2026_revenue_low':2213,'FY2026_revenue_high':2218,'recurring_growth_approx':.09,'float_interest':107,'adj_EBITDA_low':1069,'adj_EBITDA_high':1079,'GAAP_reconciliation_provided':False},
'normalization':{'software_cap_9M26':58.4,'software_cap_9M25':114.2,'software_SBC_cap_9M26':2.6,'software_cash_resource_proxy_9M26':55.8,'PPE_accrued_unpaid_9M26':8.6,'software_resource_caveat':'58.4 less2.6 is cash-like labor proxy, not certified cash capex due accruals/disposals/other software purchases','SBC_CFO_9M26':52,'SBC_equity_9M26':48.1,'SBC_unexplained_bridge':52+2.6-48.1,'RND_expense_9M26':151.1,'RND_expense_9M25':211.2,'contract_capitalized_9M26':154.2,'contract_amort_9M26':125.7,'contract_end':1045.4}}
peer={'status':'secondary_provider_screen_NOT_normalized_comps','date':'2026-11-10 regular close','PAYX':{'price':116.19,'EV':45050,'EV_EBIT':17.10,'FCF':2020,'source':'https://stockanalysis.com/stocks/payx/statistics/'},'ADP':{'price':305.63,'EV':122720,'EV_EBIT':20.60,'FCF':5250,'source':'https://stockanalysis.com/stocks/adp/statistics/'},'PAYC':{'price':238,'EV_provider':11170,'EV_EBIT_provider':15.05,'source':'https://stockanalysis.com/stocks/payc/statistics/'},'warnings':['PAYC provider EBIT742.6 differs from SEC-derived731.6; not substituted.','PAYC provider debt823.5 includes73.5 operating leases; our unlevered model retains rent and uses750 debt.','PAYC provider44.31m shares excludes/does not match45.034789m Oct27 cover incl restricted shares.','ADP provider debt5.59bn minuscash3.33bn does not equal displayed2.07bn net debt; normalized holdings/leases/investments not resolved.','Peer PEO/gross-v-net pass-through, Paycor acquisition/intangibles and float financing require primary normalization; no median target inferred.']}
results={'status':'screen-grade','stage3_complete':False,'total_fair_value':None,'method':'controlled_deterministic_support_delta_to_existing_partial_model_not_banker_formula_workbook','canonical_fields':{'fairValue':None,'maxEntryPrice':None,'entry':None,'scenarioTotalValues':None},'audit_scope':'independent arithmetic review, partial-only','model_limitations':['2027 starts from Sep2026TTM, not full-year2026 guidance','Remaining2026 stub omitted','Bridge deducts selected dividend reserve but entitlement to dividend at cum-date not modeled','Operating cash reserve and distributable bank cash uncertain'],'wacc':wa,'cases':cases,'reverse_growth':rev,'base_observed_beta':m.model('base',discount=wa['observed_beta'],stubYears=51/365),'favorable_cash_and_share_bound':bound,'wacc_sensitivity':[{ 'beta':b,'kd':d,'wacc':wE*(rf+b*erp)+(1-wE)*d*(1-tax),'value':m.model('base',discount=wE*(rf+b*erp)+(1-wE)*d*(1-tax),stubYears=51/365)['illustrativePerShare']}for b in [.73,1,1.3]for d in [.0555,.06,.063]],'qa':checks,'remaining':['Current bank eligible cash/180-day expense plus post-Sep cash/debt movements','PSU settlement/payout and October awards bridge; $6.5m economic SBC-to-APIC difference','Normalized primary-source peers and consistent EV/earnings denominators','Actual software maintenance/growth investment and capitalized labor reconciliation','Exact regular closing price conflict and future earnings date','Independent arithmetic audit passed for partial research only; audit clarifications applied; not certified total valuation']}
for n,d in [('inputs_delta.json',inputs),('results_delta.json',results),('peers_screen.json',peer)]: (P/n).write_text(json.dumps(d,indent=2)+'\n')
with (P/'forecast_delta.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=['case']+list(cases['base']['years'][0]));w.writeheader();w.writerows({'case':k,**z}for k,v in cases.items()for z in v['years'])
print('WACC',wa);print('VALUES',{k:v['illustrativePerShare']for k,v in cases.items()});print('OBSERVED_BETA_BASE',results['base_observed_beta']['illustrativePerShare']);print('FAVORABLE_BOUND',bound['illustrativePerShare']);print('REVERSE',rev);print('CHECKS',checks)
