"""POOL: USD millions, except per-share USD. Valuation as of 2026-11-06."""
import json
from pathlib import Path
P=Path(__file__).parent
price=211.70; shares=35.923+.216; debt=1166.882; cash=105.657; reserve=100
rf=.0486; erp=.0441; beta=.94; kd=.0586; tax=.25
wacc=(rf+beta*erp)*(price*shares)/(price*shares+debt)+kd*(1-tax)*debt/(price*shares+debt)
scenarios={'adverse':dict(g=.015,margin=.10,wacc=wacc+.01,terminal=.02,roic=.15), 'base':dict(g=.04,margin=.115,wacc=wacc,terminal=.025,roic=.18),'favorable':dict(g=.06,margin=.125,wacc=wacc-.005,terminal=.03,roic=.22)}
def value(g=.04,margin=.115,wacc=wacc,terminal=.025,roic=.18):
 sales=5448.118; rows=[]; pv=0; startmargin=(574.495+2)/sales
 for y in range(1,11):
  growth=g if y<=5 else g+(terminal-g)*(y-5)/5
  old=sales;sales*=1+growth
  m=startmargin+(margin-startmargin)*min(y,5)/5
  nopat=sales*m*(1-tax)
  # Explicit capex includes IT/software allowance; M&A paid separately.
  capex=sales*.013; da=sales*.0095; nwc=(sales-old)*.20; acq=sales*.002
  explicit=capex-da+nwc+acq
  reinvest=explicit if y<=5 else explicit*(1-(y-5)/5)+(nopat*growth/roic)*((y-5)/5)
  fcff=nopat-reinvest; pv+=fcff/(1+wacc)**y
  rows.append(dict(year=y,sales=sales,growth=growth,ebit_margin=m,nopat=nopat,capex=capex,da=da,nwc=nwc,acquisitions=acq,reinvestment=reinvest,fcff=fcff))
 tv=rows[-1]['nopat']*(1+terminal)*(1-terminal/roic)/(wacc-terminal);tvpv=tv/(1+wacc)**10
 ev=pv+tvpv;return dict(value=(ev-debt+max(cash-reserve,0))/shares,enterprise=ev,terminal_fraction=tvpv/ev,rows=rows)
results={k:value(**v) for k,v in scenarios.items()}
lo,hi=-.03,.20
for _ in range(100):
 mid=(lo+hi)/2
 if value(g=mid)['value']<price:lo=mid
 else:hi=mid
output=dict(asof='2026-11-06',price=price,shares=shares,debt=debt,cash=cash,operating_cash_reserve=reserve,riskfree=rf,erp=erp,beta=beta,cost_debt=kd,tax=tax,wacc=wacc,assumptions=scenarios,results=results,reverse_initial_growth=(lo+hi)/2,sensitivity_wacc={str(round(wacc+d,5)):value(wacc=wacc+d)['value'] for d in [-.01,-.005,0,.005,.01]})
(P/'valuation.json').write_text(json.dumps(output,indent=2))
print(json.dumps({k:{'value':v['value'],'tv':v['terminal_fraction']} for k,v in results.items()},indent=2));print('wacc',wacc,'reverse',output['reverse_initial_growth'])
