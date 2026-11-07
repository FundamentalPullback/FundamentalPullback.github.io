import json,pathlib
P=pathlib.Path(__file__).parent
price=309.10;shares=237.199353 # 234.199353m actual Oct26 basic +3m reported dilution proxy
# USD millions: no sale/dividend proceeds double counted; Freight operations excluded.
bridge={'cash':7961,'customer_tariff_cash':-2700,'operating_cash_reserve':-3000,'freight_stake':3254,'inpost_equity_investment':2501,'other_equity_securities':576,'debt_securities':266,'supply_chain_sale_net_tax_assumption':1050,'debt_ex_finance_leases':-17600,'finance_leases':-1718,'unfunded_pension_and_healthcare':-1661}
net=sum(bridge.values())
beta=1.31;rf=.0486;erp=.0441;kd=.0586;tax=.225;debt=19318
wacc=(rf+beta*erp)*(price*shares)/(price*shares+debt)+kd*(1-tax)*debt/(price*shares+debt)
def model(g=.04,m0=.062,m5=.08,mt=.075,w=wacc,roic=.15,gt=.025,base=90000,capex=.043,lease=.01,da=.043):
 rev=base;prevnopat=base*m0*(1-tax); rows=[];pv=0
 for t in range(1,11):
  growth=g if t<=5 else g+(gt-g)*(t-5)/5
  margin=m0+(m5-m0)*t/5 if t<=5 else m5+(mt-m5)*(t-5)/5
  nr=rev*(1+growth);nopat=nr*margin*(1-tax)
  physical=nr*(capex+lease-da)+.05*(nr-rev)
  economic=max(0,nopat-prevnopat)/roic
  reinv=max(physical,economic)
  if t>5:reinv=(1-(t-5)/5)*reinv+((t-5)/5)*(nopat*growth/roic)
  fcf=nopat-reinv;pv+=fcf/(1+w)**t;rows.append({'year':2026+t,'sales':nr,'margin':margin,'nopat':nopat,'reinvestment':reinv,'fcff':fcf});rev=nr;prevnopat=nopat
 terminal=prevnopat*(1+gt)*(1-gt/roic)/(w-gt);pvt=terminal/(1+w)**10;ev=pv+pvt
 return {'value':(ev+net)/shares,'ev':ev,'terminal_weight':pvt/ev,'rows':rows}
cases={'adverse':model(.015,.055,.06,.06,wacc+.01,.10,.02),'central':model(),'favorable':model(.06,.065,.09,.085,wacc-.005,.18)}
lo=.03;hi=.16
for _ in range(100):
 mid=(lo+hi)/2
 if model(m5=mid,mt=mid-.005)['value']<price:lo=mid
 else:hi=mid
out={'price_reference':price,'shares_proxy':shares,'wacc':wacc,'capital_cost_inputs':{'beta':beta,'rf':rf,'erp':erp,'kd_assumed':kd,'tax':tax},'bridge':bridge,'bridge_net':net,'cases':cases,'inverse_margin_year5':(lo+hi)/2,'wacc_sensitivity':{str(w):model(w=w)['value'] for w in [.08,.09,.10,.11]},'sensitivity':{'no_inpost_or_other_equities':cases['central']['value']-(2501+576)/shares,'no_supply_chain_proceeds':cases['central']['value']-1050/shares,'zero_operating_cash_reserve':cases['central']['value']+3000/shares,'lease_additions_2pct':model(lease=.02)['value'],'base_sales_plus2pct':model(base=91800)['value']},'checks':{'ten_years':len(cases['central']['rows'])==10,'wacc_above_g':wacc>.025,'no_freight_operating_profit':True,'excludes_customer_tariff_cash':bridge['customer_tariff_cash']==-2700}}
P.joinpath('calculations.json').write_text(json.dumps(out,indent=2));print({k:round(v['value'],2) for k,v in cases.items()});print('wacc',wacc,'inverse_margin',out['inverse_margin_year5'],'bridge',net);print(out['sensitivity'])
