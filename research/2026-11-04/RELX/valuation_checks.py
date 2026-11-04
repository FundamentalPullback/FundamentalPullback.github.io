import json,copy
from model import *
PRICE=39.40; equity=PRICE/FX*CAPITAL['diluted_shares']; debt=8906; we=equity/(equity+debt);rf=.053087;erp=.0441;kd=.058
w=lambda beta:we*(rf+beta*erp)+(1-we)*kd*.77
cal={'risk_free_gbp_par_10y':rf,'risk_free_date':'2026-10-28 latest accessible BOE primary series, not Nov3','erp_mature_market_proxy':erp,'beta_provider_search_only':.28,'beta_normalized_assumption':.85,'debt_cost_assumption_not_current_bond_yield':kd,'equity_weight':we,'normalized_wacc':w(.85),'provider_beta_wacc':w(.28),'chosen_wacc':.085,'provider_beta_value':calculate(dict(SCENARIOS['base'],wacc=w(.28)))['usd_per_adr'],'normalized_value':calculate(dict(SCENARIOS['base'],wacc=w(.85)))['usd_per_adr']}
def legacy(wacc=.08,fx=1.332807,growth=None,margins=None,da=.074,investment=.081,terminal_roic=.15,roic_floor=None):
 r=9720;prev=3122*.77;ev=0;growth=growth or[.06,.06,.055,.05,.045];margins=margins or[.323,.328,.333,.338,.34]
 for y in range(1,11):
  g=growth[y-1]if y<=5 else growth[-1]+(.025-growth[-1])*(y-5)/5;m=margins[y-1]if y<=5 else margins[-1];old=r;r*=1+g;n=r*m*.77;reinvest=r*(investment-da)+(r-old)*.08
  if roic_floor:reinvest=max(reinvest,max(0,n-prev)/roic_floor)
  fc=n-reinvest;ev+=fc/(1+wacc)**y;prev=n
 terminal_n=n*1.025;ri=terminal_n*.025/terminal_roic
 if roic_floor:ri=max(ri,r*1.025*(investment-da)+r*.025*.08)
 ev+=((terminal_n-ri)/(wacc-.025))/(1+wacc)**10
 return(ev-8899)/1794.1*fx
steps=[('A111 narrative reconstruction',legacy()),('FX updated only',legacy(fx=FX)),('GBP WACC8 to8.5 only',legacy(fx=FX,wacc=.085)),('Growth path5.5/5.5/5/4.5/4',legacy(fx=FX,wacc=.085,growth=SCENARIOS['base']['growth'])),('Before-acquired margins35–36.5; ordinaryDA5.3; old investment8.1',legacy(fx=FX,wacc=.085,growth=SCENARIOS['base']['growth'],margins=SCENARIOS['base']['margin'],da=.053)),('Fund prepublication/renewal/M&A total9.3; terminal18',legacy(fx=FX,wacc=.085,growth=SCENARIOS['base']['growth'],margins=SCENARIOS['base']['margin'],da=.053,investment=.093,terminal_roic=.18)),('Fund positive incremental NOPAT and terminal investment floor',calculate(SCENARIOS['base'])['usd_per_adr'])]
bridge=[];prior=None
for label,v in steps:bridge.append({'step':label,'value':v,'change':None if prior is None else v-prior});prior=v

def reverse(growth=None,margin=None):
 lo,hi=(0,.25)if margin is not None else(.15,.70)
 for _ in range(100):
  x=(lo+hi)/2;s=copy.deepcopy(SCENARIOS['base']);s['growth']=[x if margin is not None else growth]*5;s['margin']=[margin if margin is not None else x]*5;v=calculate(s)['usd_per_adr']
  if v<PRICE:lo=x
  else:hi=x
 return {'required':(lo+hi)/2,'value':v}
robust={}
for roic in [.13,.154,.18,.23]:robust['ROIC_'+str(roic)]=calculate(dict(SCENARIOS['base'],roic=roic,terminal_roic=roic))['usd_per_adr']
for extra in [.005,.01]:robust['extra_replacement_'+str(extra)]=calculate(SCENARIOS['base'],extra_replacement=extra)['usd_per_adr']
for tax in [.225,.25]:robust['tax_'+str(tax)]=calculate(dict(SCENARIOS['base'],tax=tax))['usd_per_adr']
for fx in [1.2,1.3,1.4]:robust['fx_'+str(fx)]=calculate(SCENARIOS['base'],fx=fx)['usd_per_adr']
# No assertion these cash expenditures equal post-June net-debt changes. Gross-outflow stress excludes subsequent cash generation.
for outflow in [366,766,866]:robust['latest_shares_plus_gross_cash_outflow_'+str(outflow)]=calculate(SCENARIOS['base'],shares=1740.716354+7.6,extra_claims=outflow)['usd_per_adr']
robust['June_capital_at_latest_shares_free_buyback_NOT_BASE']=calculate(SCENARIOS['base'],shares=1740.716354+7.6)['usd_per_adr']
robust['pension_fully_netted_NOT_BASE']=calculate(SCENARIOS['base'],extra_claims=-236)['usd_per_adr']
# Rolling TTM anniversary horizon: first full forecast year ends30June2027. Nov3 is126days beyond June30.
offset=-126/365;remainder=239/365
b=calculate(SCENARIOS['base']);r=calculate(SCENARIOS['base'],time_offset=offset)
# Approximate already elapsed portion must not be counted again; no new balance exists to certify its disposition.
elapsed_pv=b['rows'][0]['fcff']*(126/365)/(1.085)**remainder
calendar={'original_convention':'10 rolling full years discounted from June30 anchor, treated as valuation reference, not measured Nov3 balance','asof_Nov3_full_first_year_NOT_BASE':r['usd_per_adr'],'first_year_remaining_fraction':remainder,'asof_Nov3_proportional_remaining_year_and_old_capital':r['usd_per_adr']-elapsed_pv/CAPITAL['diluted_shares']*FX,'note':'Timing sensitivity only: no observed post-June cash/debt statement; proportional intra-year cash ignores seasonality and is not current NAV.'}
out={'wacc_calibration':cal,'migration':bridge,'migration_caveat':'Original executable not located. Narrative reconstruction rounds exactly to published29.59; new accounting/method changes are explicit, not new earnings.','reverse':{'margin_at_growth5_5':reverse(growth=.055),'growth_at_margin36_5':reverse(margin=.365),'joint':[dict(margin=m,**reverse(margin=m))for m in [.35,.365,.39,.42]]},'robustness':robust,'calendar':calendar}
(P/'valuation_checks.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
