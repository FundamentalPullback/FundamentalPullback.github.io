import json,pathlib,copy
from model import *
E=PRICE*SHARES;D=DEBT;rf=.0495;erp=.0441;kd=.065;beta_observed=1.04;beta_normalized=1.2
w=lambda b:(rf+b*erp)*E/(E+D)+kd*.75*D/(E+D)
cal=dict(risk_free=rf,erp=erp,erp_source_riskfree=.0529,beta_provider=beta_observed,beta_normalized_assumption=beta_normalized,debt_cost_assumption=kd,equity_weight=E/(E+D),wacc_provider_beta=w(beta_observed),wacc_normalized_beta=w(beta_normalized),wacc_chosen=.09)
cal['same_inputs_preserve_NYU_market_return']=((.097+(.2*.0441))*E+kd*.75*D)/(E+D)
cal['same_operating_cashflows_provider_wacc_value']=model({**BASE,'wacc':w(beta_observed)})['value']
cal['same_operating_cashflows_normalized_wacc_value']=model({**BASE,'wacc':w(beta_normalized)})['value']
# Same information/prices: accounting/assumptions decomposed, not new results news.
steps=[('A119 exact reconstruction',old_model()),('WACC10 to9 only',old_model(wacc=.09)),('Reserve operatingcash150 + prior taxes99.4 + pension22.6',old_model(wacc=.09,claims=7027.1+272)),('Growth path4/4.5/4.5/4/3.5 only',old_model(wacc=.09,claims=7299.1,growth=BASE['growth'])),('Before acquired amort margin32–32.5; retain ordinaryDA3.5 and oldinvestment9.1',old_model(wacc=.09,claims=7299.1,growth=BASE['growth'],margins=BASE['margin'],da=.035)),('Explicit investment funding + terminalmargin32',model(BASE)['value'])]
bridge=[];prev=None
for label,v in steps:bridge.append(dict(step=label,value=v,delta=None if prev is None else v-prev));prev=v
# Reverse one-variable and joint pairs. Same model, not independent evidence.
def reverse(margin=None,growth=None):
 lo,hi=(0,.20)if margin is not None else(.15,.60)
 for _ in range(100):
  x=(lo+hi)/2;s=copy.deepcopy(BASE)
  if margin is not None:s.update(growth=[x]*5,margin=[margin]*5,terminal_margin=margin)
  else:s.update(growth=[growth]*5,margin=[x]*5,terminal_margin=x)
  if model(s)['value']<PRICE:lo=x
  else:hi=x
 return dict(required=(lo+hi)/2,value=model(s)['value'])
reverse_cases=dict(margin_at_growth4pct=reverse(growth=.04),growth_at_margin32pct=reverse(margin=.32),joint=[dict(margin=m,**reverse(margin=m))for m in [.30,.32,.34,.36]])
robust={f'ROIC_{roic}':model({**BASE,'roic':roic,'terminal_roic':roic})['value']for roic in [.1068,.13,.18,.23]}
base=model(BASE);off=57/365
robust['calendar57days_no_stub']=(base['ev']/1.09**off+CASH-RESERVE-base['claims'])/SHARES
robust['calendar57days_proxy_stub']=(base['ev']/1.09**off+base['rows'][0]['fcff']*off/1.09**off+CASH-RESERVE-base['claims'])/SHARES
robust['full_investments_affiliates_book_credit']=base['value']+(171.3+247.3)/SHARES
robust['extra_claim150_above_base']=model({**BASE,'additional_claims':272})['value']
robust['extra_shares1pct_no_free_cash']=base['equity']/(SHARES*1.01)
robust['extra_shares3pct_no_free_cash']=base['equity']/(SHARES*1.03)
# Sensitivities only, not guessed convertible terms or permanent recurring dilution.
out=dict(capital_cost=cal,migration=bridge,reverse=reverse_cases,robustness=robust)
(P/'valuation_checks.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
