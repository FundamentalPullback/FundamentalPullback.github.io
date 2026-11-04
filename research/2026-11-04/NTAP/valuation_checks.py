import json,pathlib,copy
from model import *
P=pathlib.Path(__file__).parent
b=calculate(BASE)
def val(**kw):return calculate(dict(BASE,**kw))['value']
grid=[{'wacc':w,'g':g,'value':val(wacc=w,g=g)}for w in [.10,.112,.125]for g in [.02,.025,.03]]
sens={'historical_tax_claim0':val(historical_tax_claim_reserve=0),'historical_tax_claim68':val(historical_tax_claim_reserve=68),'historical_tax_claim56_if_interest_extra':val(historical_tax_claim_reserve=56),'no_stub':calculate(BASE,stub_scale=0)['value'],'stub_plus20pct':calculate(BASE,stub_scale=1.2)['value'],'stub_minus20pct':calculate(BASE,stub_scale=.8)['value'],'margin_minus2pt':calculate(BASE,margin_shift=-.02)['value'],'margin_plus2pt':calculate(BASE,margin_shift=.02)['value'],'growth_minus2pt':calculate(BASE,growth_shift=-.02)['value'],'growth_plus2pt':calculate(BASE,growth_shift=.02)['value'],'ROIC18pct':val(roic=.18),'ROIC35pct':val(roic=.35),'ROIC100pct_assetlight_stress':val(roic=1.0),'WACC_monthly_consistent_rf529':val(wacc=(.0529+1.51*.0441)*(1-2500/(PRICE*SHARES+2500))+.058*.76*(2500/(PRICE*SHARES+2500))),'tax22pct':val(tax=.22),'tax26pct':val(tax=.26),'acquisitions0':val(post_July_acquisition_reserve=0),'acquisitions500':val(post_July_acquisition_reserve=500),'acquisitions1000':val(post_July_acquisition_reserve=1000),'unknown_capital_minus500':val(capital_movement=-500),'unknown_capital_plus500':val(capital_movement=500),'cashreserve300':calculate(BASE,reserve=300)['value'],'cashreserve900':calculate(BASE,reserve=900)['value'],'no_extraweek_revenue_adjustment':val(extra_week_revenue=0),'capex_ratio_4pct':val(capex_ratio=.04),'SBC_expense_stress_extra1pt_margin':calculate(BASE,margin_shift=-.01)['value']}
def bisect(fn,target,lo,hi):
 for _ in range(100):
  mid=(lo+hi)/2
  if fn(mid)<target:lo=mid
  else:hi=mid
 return (lo+hi)/2
shift=bisect(lambda x:calculate(BASE,growth_shift=x)['value'],PRICE,-.02,.3)
rev=calculate(BASE,growth_shift=shift)
marginshift=bisect(lambda x:calculate(BASE,margin_shift=x)['value'],PRICE,-.02,.5)
# Calendar cross-check: exact model convention versus all annual flows shifted to 1..10 with stub unchanged.
wrong_calendar=(sum(r['FCFF']/(1+BASE['wacc'])**r['year']for r in b['rows'])+b['terminal_value']/(1+BASE['wacc'])**10+b['stub']['PV']+b['capital_bridge_scenario_not_measured']['net_equity_adjustment'])/SHARES
out={'base':b['value'],'wacc_g_grid':grid,'sensitivities':sens,'reverse_growth_uniform_addition':shift,'reverse_growth_year1':BASE['growth'][0]+shift,'reverse_growth_year10':BASE['growth'][-1]+shift,'reverse_revenue_year10':rev['rows'][-1]['revenue'],'reverse_margin_uniform_addition':marginshift,'reverse_year10_margin':BASE['margins'][-1]+marginshift,'incorrect_one_year_firstfull_calendar_value_for_diagnostic_only':wrong_calendar}
(P/'valuation_checks.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
