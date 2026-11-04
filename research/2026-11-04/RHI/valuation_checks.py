import json,copy
from model import *
rf=.0495;erp=.0441;observed_beta=.75;normalized_beta=1.2
w=lambda beta:rf+erp*beta
cal={'risk_free':rf,'risk_free_date':'2026-11-03','erp':erp,'erp_date':'2026-11-01','observed_beta_provider':observed_beta,'beta_source':'https://stockanalysis.com/stocks/rhi/statistics/','beta_observed_on':'2026-11-04','normalized_beta_assumption':normalized_beta,'provider_beta_cost_equity':w(observed_beta),'normalized_beta_cost_equity':w(normalized_beta),'chosen_wacc_no_financial_debt':.105,'provider_beta_same_cashflows_value':calculate(dict(BASE,wacc=w(observed_beta)))['value'],'normalized_beta_value':calculate(dict(BASE,wacc=w(normalized_beta)))['value']}
robust={}
for roic in [.12,.1294,.15,.18,.23]:robust['initial_terminal_roic_'+str(roic)]=calculate(dict(BASE,roic=roic,terminal_roic=roic))['value']
for reserve in [0,100,150,200]:robust['cash_reserve_'+str(reserve)]=calculate(BASE,reserve=reserve)['value']
for tax in [.30,.33,.37]:robust['tax_'+str(tax)]=calculate(dict(BASE,tax=tax))['value']
for claim in [50,100,200]:robust['illustrative_legal_cash_loss_NOT_FORECAST_'+str(claim)]=calculate(BASE,claims=claim)['value']
for cost in [.0025,.005,.01]:robust['ongoing_margin_cost_NOT_FORECAST_'+str(cost)]=calculate(BASE,margin_cost=cost)['value']
for sh in [100.94,102.350326,102.351225,103.351225]:robust['share_proxy_'+str(sh)]=calculate(BASE,shares=sh)['value']
robust['charge_all_positive_nopat_growth_margin_recovery']=calculate(BASE,charge_margin_growth=True)['value']
robust['no_stub_same_calendar']=calculate(BASE,include_stub=False)['value']
robust['no_stub_one_year_discount_NOT_BASE']=calculate(BASE,include_stub=False,time_offset=0)['value']
robust['trust_surplus_not_base']=calculate(BASE,claims=-16.409)['value']
# Revenue-only investment proxy is not literal incremental-return attribution when margins change.
b=calculate(BASE);rows=b['rows'];first=rows[0];prev=NORMAL_EBIT*(1-BASE['tax']);actual_delta=first['nopat']-prev
investment_diagnostic={'first_year_positive_nopat_change':actual_delta,'base_reinvestment':first['reinvestment'],'implied_delta_nopat_over_reinvestment':actual_delta/first['reinvestment'],'stated_roic_is_revenue_growth_proxy_not_implied_margin_return':True,'all_positive_nopat_reinvestment_first_year':max(first['net_reinvestment_floor'],actual_delta/BASE['roic'])}
def reverse(margin=None,growth=None):
 lo,hi=(0,.3)if margin is not None else(.02,.25)
 for _ in range(100):
  x=(lo+hi)/2;s=copy.deepcopy(BASE)
  if margin is not None:s.update(growth=[x]*5,margin=[margin]*5,terminal_margin=margin)
  else:s.update(growth=[growth]*5,margin=[x]*5,terminal_margin=x)
  value=calculate(s)['value']
  if value<PRICE:lo=x
  else:hi=x
 return {'required':(lo+hi)/2,'value':value}
reverse_cases={'constant_margin_at_growth5pct':reverse(growth=.05),'constant_growth_at_margin7pct':reverse(margin=.07),'joint':[dict(margin=m,**reverse(margin=m))for m in [.065,.075,.085,.095]]}
# No old DCF existed in A109. The legacy cash-before-financing diagnostic included acquisitions.
legacy={'A109_had_valuation':False,'old_9m_before_financing_cash2026':47.147,'old_9m_before_financing_cash2025':74.811,'current_9m_after_capex_trust_before_acquisitions2025':85.533,'prior_acquisition_cash':10.722,'identity':85.533-10.722,'no_change_to_original_conclusion':'Operating recovery incomplete; newly modeled scenarios do not certify a normalized current run rate.'}
out={'wacc_calibration':cal,'robustness':robust,'reinvestment_diagnostic':investment_diagnostic,'reverse':reverse_cases,'legacy_bridge':legacy,'base_terminal_weight':b['terminal_share_of_ev']}
(P/'valuation_checks.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
