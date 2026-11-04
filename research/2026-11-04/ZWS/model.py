from pathlib import Path
import json
P=Path(__file__).parent
PRICE=44.12;SHARES=168.105;START=1826.3
NET=269.5-100-503.2-10.4-5.2-.7-13.4-8.3
# September capital. Deferred compensation assets and liabilities matched, no net addition.
def calc(gd=0,md=0,w=.094,g=.025,roic=.15,tax=.25,net=NET,shares=SHARES,da=.014,capex=.02,funding=True):
 growth=[.06,.06,.05,.04,.04];growth=[max(0,v+gd) for v in growth];growth += [growth[-1]+(g-growth[-1])*i/5 for i in range(1,6)]
 margins=[v+md for v in [.20,.205,.21,.21,.21]+[.21]*5];r=START;rows=[];pv=0
 for i in range(10):
  old=r;r*=1+growth[i];ebit=r*margins[i];nopat=ebit*(1-tax);d=r*da;c=r*capex;nwc=(r-old)*.15;explicit=c-d+nwc;economic=nopat*growth[i]/roic
  raw=max(explicit,economic) if funding else explicit;weight=max(0,(i-4)/5);reinv=raw*(1-weight)+economic*weight;fcff=nopat-reinv;pvf=fcff/(1+w)**(i+1);pv+=pvf
  rows.append(dict(year=i+1,revenue=r,growth=growth[i],ebit_margin=margins[i],ebit=ebit,nopat=nopat,da=d,capex=c,delta_nwc=nwc,explicit_reinvestment=explicit,economic_reinvestment=economic,transition_weight=weight,reinvestment=reinv,additional_reinvestment_reserve=reinv-explicit,fcff=fcff,pv_fcff=pvf))
 tn=r*(1+g)*margins[-1]*(1-tax);tri=tn*g/roic;tcf=tn-tri;pvtv=tcf/(w-g)/(1+w)**10;ev=pv+pvtv
 return dict(value=(ev+net)/shares,ev=ev,equity=ev+net,net_bridge=net,pv_explicit=pv,pv_terminal=pvtv,terminal_weight=pvtv/ev,terminal_nopat=tn,terminal_reinvestment=tri,terminal_fcff=tcf,rows=rows,assumptions=dict(wacc=w,g=g,roic=roic,tax=tax,shares=shares,growth_delta=gd,margin_delta=md,da_ratio=da,capex_ratio=capex,nwc_ratio=.15,funding_guard=funding))
def solve(fn,lo,hi):
 for _ in range(100):
  mid=(lo+hi)/2
  if fn(mid)<PRICE:lo=mid
  else:hi=mid
 return (lo+hi)/2
cases={'bear':calc(-.03,-.03,.104,.015,.12),'base':calc(),'bull':calc(.03,.025,.084,.03,.20)}
def old_fcfe(flow,g,w,t):
 pv=0;current=flow
 for i in range(10):
  rate=g if i<5 else g+(t-g)*(i-4)/5
  current*=1+rate;pv+=current/(1+w)**(i+1)
 tv=current*(1+t)/(w-t)/(1+w)**10
 return dict(value=(pv+tv)/SHARES,terminal_weight=tv/(pv+tv),shares=SHARES)
out=dict(asof='2026-11-04',price=PRICE,price_date='2026-11-03 16:00 America/New_York',cases=cases,capital_bridge=dict(reported_cash=307.1,covenant_eligible_cash=269.5,cash_access_haircut=37.6,operating_cash_reserve=100,nominal_debt_including_finance_leases=503.2,pension_obligations=10.4,deferred_comp_net_shortfall=5.2,uncertain_tax=.7,tax_indemnities=8.3,acquired_warranty_reserve=13.4,net=NET),reverse=dict(growth_extra_first5=solve(lambda x:calc(gd=x)['value'],-.03,.3),margin_extra_all_years=solve(lambda x:calc(md=x)['value'],-.05,.3)),sensitivity=[dict(wacc=w,g=g,value=calc(w=w,g=g)['value']) for w in [.084,.089,.094,.099,.104] for g in [.015,.02,.025,.03]],roic_sensitivity=[dict(roic=r,value=calc(roic=r)['value']) for r in [.12,.15,.18,.20,.25]],tax_sensitivity=[dict(tax=t,value=calc(tax=t)['value']) for t in [.22,.25,.28]],explicit_only_sensitivity=calc(funding=False),amortization_release_sensitivity=calc(md=59.2/START),dilution_sensitivity=calc(shares=SHARES*1.03)['value'],historical_roic_proxy=(403-49.1)*.75/((1603.3+500.5-300.5+100+1693.5+503.2-307.1+100)/2),capital_sensitivity=dict(exclude_tax_indemnities=calc(net=NET+8.3)['value'],use_full_reported_cash=calc(net=NET+37.6)['value'],remove_acquired_warranty_reserve=calc(net=NET+13.4)['value'],cash_reserve50=calc(net=NET+50)['value'],cash_reserve150=calc(net=NET-50)['value']),historical_A107=dict(published=dict(bear=20.35,base=34.71,bull=53.15),reconstruction_using_current_shares={k:old_fcfe(*v) for k,v in {'bear':(270,.03,.105,.02),'base':(310,.07,.095,.025),'bull':(350,.10,.09,.03)}.items()},status='Reconstruction from disclosed assumptions, current diluted shares; matches disclosed roundedA107 values with Q3shares168.105; original executable not recovered'))
json.dump(out,open(P/'model.json','w'),indent=2);print({k:v['value'] for k,v in cases.items()});print(out['reverse']);print('NET',NET,'TV',cases['base']['terminal_weight'])
