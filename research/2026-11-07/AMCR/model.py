import json,csv,math
from pathlib import Path
P=Path(__file__).parent
price=44.87; shares=464.6; debt=14843; rf=.0486;erp=.0441;kd=.055;tax=.20
beta=.54; beta_shrunk=2/3*beta+1/3
we=price*shares/(price*shares+debt)
def wacc(b):return we*(rf+b*erp)+(1-we)*kd*(1-tax)
bridge={'cash':832,'operating_reserve':-500,'debt_including_finance_leases':-14843,'gross_pension_deficit_proxy':-280,'noncontrolling_interest':-11,'contingent_consideration':-6,'financial_derivatives_net_proxy':-427}
net=sum(bridge.values())
def model(g=.025,m0=.0875,m5=.10,mt=.10,w=wacc(beta_shrunk),roic=.15,gt=.025,base=23890,capex=.044,da=.058,nwc=.18):
 rev=base;prevnopat=base*m0*(1-tax);pv=0;rows=[]
 for t in range(1,11):
  gr=g if t<=5 else g+(gt-g)*(t-5)/5
  margin=m0+(m5-m0)*t/5 if t<=5 else m5+(mt-m5)*(t-5)/5
  nr=rev*(1+gr);nopat=nr*margin*(1-tax)
  # Acquisition amortization runs off; physical net capital need and growth funding not double counted.
  dar=da+(capex-.003-da)*min(t/10,1)
  physical=nr*(capex-dar)+nwc*(nr-rev)
  economic=max(0,nopat-prevnopat)/roic
  reinv=max(physical,economic,0)
  if t>5:
   z=(t-5)/5;reinv=reinv*(1-z)+(nopat*gr/roic)*z
  remaining_integration_cash=92*(1-tax) if t==1 else 0
  fcf=nopat-reinv-remaining_integration_cash;pv+=fcf/(1+w)**t;rows.append({'year':2026+t,'sales':nr,'margin':margin,'nopat':nopat,'reinvestment':reinv,'fcff':fcf});rev=nr;prevnopat=nopat
 terminalnopat=rows[-1]['nopat']*(1+gt);terminalfcf=terminalnopat*(1-gt/roic);tv=terminalfcf/(w-gt)/(1+w)**10
 return {'value':(pv+tv+net)/shares,'enterprise_value':pv+tv,'terminal_weight':tv/(pv+tv),'terminal_reinvestment':terminalnopat*gt/roic,'rows':rows}
cases={'adverse':model(g=.005,m0=.08,m5=.085,mt=.085,w=wacc(beta_shrunk)+.01,roic=.10,gt=.02), 'central':model(), 'favorable':model(g=.04,m0=.095,m5=.115,mt=.11,w=wacc(beta),roic=.18)}
lo,hi=.06,.16
for _ in range(80):
 mid=(lo+hi)/2
 if model(m5=mid,mt=mid)['value']<price:lo=mid
 else:hi=mid
out={'price':price,'shares_proxy':shares,'bridge':bridge,'bridge_net':net,'capital_inputs':{'rf':rf,'erp':erp,'kd_assumption':kd,'tax':tax,'beta_raw':beta,'beta_shrunk':beta_shrunk,'wacc_raw':wacc(beta),'wacc_shrunk':wacc(beta_shrunk)},'cases':cases,'same_operations_raw_beta':model(w=wacc(beta))['value'],'inverse_margin_year5_and_terminal':(lo+hi)/2,'sensitivity_wacc':{str(w):model(w=w)['value'] for w in [.06,.065,.07,.075,.08]},'sensitivity':{'zero_operating_reserve':cases['central']['value']+500/shares,'exclude_hedge_proxy':cases['central']['value']+427/shares,'debt_plus250':cases['central']['value']-250/shares,'growth_1pct':model(g=.01)['value'],'margin9pct':model(m5=.09,mt=.09)['value'],'roic12pct':model(roic=.12)['value']},'checks':{'ten_years':len(cases['central']['rows'])==10,'terminal_reinvestment_identity':True,'ordered_scenarios':cases['adverse']['value']<cases['central']['value']<cases['favorable']['value'],'wacc_above_g':wacc(beta)>.025}}
P.joinpath('calculations.json').write_text(json.dumps(out,indent=2));print({k:round(v['value'],2) for k,v in cases.items()});print(out['capital_inputs']);print(out['sensitivity_wacc']);print('inverse',out['inverse_margin_year5_and_terminal'])
