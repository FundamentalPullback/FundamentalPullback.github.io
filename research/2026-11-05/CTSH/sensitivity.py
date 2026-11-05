from value import *
from scipy.optimize import brentq
base=value();price=I['price'];out={}
def v(**kwargs):return value(overrides=kwargs)['per_share']
out['wacc_terminal_g']=[dict(wacc=w,g=g,value=v(wacc=w,terminal_g=g))for w in [.075,.08,wacc,.09,.095,.10]for g in [.02,.025,.03]]
out['same_wacc_tests']={
 'organic_2pct':v(organic_growth=.02),
 'margins_minus_50bp':v(margins=[m-.005 for m in I['cases']['base']['margins']],terminal_margin=.155),
 'acquisition_multiple_3_5':v(acquisition_multiple=3.5),
 'capex_1_8pct':v(capex_pct=.018),
 'terminal_roic_10pct':v(terminal_roic=.10),
 'tax_27pct':v(tax=.27),
 'further_5_DSO_days':v(dso_cash_stress_2027=308),
 'moderate_combined':v(organic_growth=.02,margins=[m-.005 for m in I['cases']['base']['margins']],terminal_margin=.155,acquisition_multiple=3.5,tax=.27,capex_pct=.018),
 'moderate_combined_with_5_DSO_days':v(organic_growth=.02,margins=[m-.005 for m in I['cases']['base']['margins']],terminal_margin=.155,acquisition_multiple=3.5,tax=.27,capex_pct=.018,dso_cash_stress_2027=308),
 'operating_bear_at_base_wacc':value('bear',overrides={'wacc':wacc})['per_share'],
 'owned_business_only_committed_dyflex':value(owned=True)['per_share'],
 'new_deals_opening_day':v(recognition_fraction=1),
 'new_deals_year_end':v(recognition_fraction=0),
 'zero_inherited_growth':v(inherited_growth_2027=0),
 'beta_raw_no_shrink':v(wacc=(I['risk_free']+B['beta']*I['erp'])*(1-dw)+I['cost_debt']*(1-I['capital_tax'])*dw),
 'beta_one':v(wacc=(I['risk_free']+I['erp'])*(1-dw)+I['cost_debt']*(1-I['capital_tax'])*dw)
}
out['bridge_tests']={label:value(bridge_overrides=pars)['per_share']for label,pars in {
 'cash_reserve_800':{'operating_cash':800},'postsept_buybacks_150':{'post_september_buyback_cash':150},'postsept_buybacks_0':{'post_september_buyback_cash':0},'pension_0':{'pension_deficit':0},'pension_400':{'pension_deficit':400},'no_incremental_dilution':{'incremental_dilution':0},'diluted_450':{'incremental_dilution':450-I['shares_actual_oct23']}}.items()}
out['stub_tests']={str(x):v(stub_issuer_fcf=x)for x in [0,730,880,1030]}
out['reverse']={
 'wacc_at_price':brentq(lambda x:v(wacc=x)-price,.03,.2),
 'organic_growth_at_price':brentq(lambda x:v(organic_growth=x)-price,-.08,.15),
 'parallel_margin_change_at_price':brentq(lambda x:v(margins=[m+x for m in I['cases']['base']['margins']],terminal_margin=.16+x)-price,-.10,.10),
 'acquisition_multiple_at_price':brentq(lambda x:v(acquisition_multiple=x)-price,.1,15),
 'terminal_roic_at_price':brentq(lambda x:v(terminal_roic=x)-price,.0251,.50)
}
out['legacy_approx_reconstruction']={}
R=22095;pv=0
for t in range(1,11):
 prev=R;g=[.045,.045,.04,.035,.03][t-1]if t<=5 else .03+(.025-.03)*(t-5)/5;m=[.154,.157,.16,.16,.16][t-1]if t<=5 else .16;R*=1+g;nopat=R*m*.75;reinv=R*(.055-.026)+(R-prev)*.15
 if t>5:f=(t-5)/5;reinv=(1-f)*reinv+f*nopat*.025/.15
 pv+=(nopat-reinv)/1.1**t
pv_tv=R*1.025*.16*.75*(1-.025/.15)/(.1-.025)/1.1**10
out['legacy_approx_reconstruction']=dict(per_share=(pv+pv_tv-500)/450,published=66.47,warning='Reconstruction from preserved narrative, not the unavailable original executable; small rounding/convention difference.')
out['new_model_at_10pct']=v(wacc=.10)
(P/'sensitivity.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
