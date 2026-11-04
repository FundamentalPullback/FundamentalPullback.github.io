from pathlib import Path
import json
P=Path(__file__).parent
PRICE=332.59;SHARES=35.572;START=2476.256
NET=233.339+31.993-100-1375-10.201-25.502-40.901-.650
# August capital only: subsequent90 revolver/BCC price and cash uses are not reconstructed.
def calc(gd=0,md=0,w=.091,g=.03,roic=.20,tax=.20,net=NET,shares=SHARES,da=.04,capex=.045,funding=True):
 growth=[2612.5/START-1,.05,.05,.04,.04];growth=[max(0,v+gd) for v in growth];growth += [growth[-1]+(g-growth[-1])*i/5 for i in range(1,6)]
 margins=[v+md for v in [.315,.318,.32,.323,.325]+[.325]*5];r=START;rows=[];pv=0
 for i in range(10):
  old=r;r*=1+growth[i];ebit=r*margins[i];nopat=ebit*(1-tax);d=r*da;c=r*capex;nwc=(r-old)*.08;explicit=c-d+nwc;economic=nopat*growth[i]/roic
  raw=max(explicit,economic) if funding else explicit;weight=max(0,(i-4)/5);reinv=raw*(1-weight)+economic*weight;fcff=nopat-reinv;pvf=fcff/(1+w)**(i+1);pv+=pvf
  rows.append(dict(year=i+1,revenue=r,growth=growth[i],ebit_margin=margins[i],ebit=ebit,nopat=nopat,da=d,capex=c,delta_nwc=nwc,explicit_reinvestment=explicit,economic_reinvestment=economic,transition_weight=weight,reinvestment=reinv,fcff=fcff,pv_fcff=pvf))
 tn=r*(1+g)*margins[-1]*(1-tax);tri=tn*g/roic;tcf=tn-tri;pvtv=tcf/(w-g)/(1+w)**10;ev=pv+pvtv
 return dict(value=(ev+net)/shares,ev=ev,equity=ev+net,net_bridge=net,pv_explicit=pv,pv_terminal=pvtv,terminal_weight=pvtv/ev,terminal_nopat=tn,terminal_reinvestment=tri,terminal_fcff=tcf,rows=rows,assumptions=dict(wacc=w,g=g,roic=roic,tax=tax,shares=shares,growth_delta=gd,margin_delta=md,da_ratio=da,capex_ratio=capex,nwc_ratio=.08,funding_guard=funding))
def solve(fn,lo,hi):
 for _ in range(100):
  mid=(lo+hi)/2
  if fn(mid)<PRICE:lo=mid
  else:hi=mid
 return (lo+hi)/2
cases={'bear':calc(-.025,-.025,.101,.02,.16),'base':calc(),'bull':calc(.025,.02,.081,.035,.25)}
out=dict(asof='2026-11-04',price=PRICE,price_date='2026-11-03 16:00 America/New_York',scope='August capital / legacy operating perimeter. BCC undisclosed purchase economics not certified; subsequent90m revolver treated only through paired cash/use scenarios.',cases=cases,capital_bridge=dict(cash=233.339,liquid_investments=31.993,operating_cash_reserve=100,nominal_debt=1375,contingent_liabilities=10.201,noncurrent_tax_liability=25.502,declared_dividend_payable=40.901,litigation_reserve=.650,net=NET),historical_A022=dict(bear=198,base=248,bull=295,status='Published rounded exploratory values; original support not recovered, not exact reproduction'),historical_A003=dict(bear=15.5*18/1.1,base=17.25*20/1.1,bull=19*23/1.1,method='EPS multiple discounted one year; not current rule'),reverse=dict(growth_extra_first5=solve(lambda x:calc(gd=x)['value'],-.03,.3),margin_extra_all_years=solve(lambda x:calc(md=x)['value'],-.05,.3)),sensitivity=[dict(wacc=w,g=g,value=calc(w=w,g=g)['value']) for w in [.081,.086,.091,.096,.101] for g in [.02,.025,.03,.035]],roic_sensitivity=[dict(roic=r,value=calc(roic=r)['value']) for r in [.15,.18,.20,.25,.30]],tax_sensitivity=[dict(tax=t,value=calc(tax=t)['value']) for t in [.18,.20,.23]],post_balance_net_cash_use_sensitivity=[dict(net_cash_use=x,value=calc(net=NET-x)['value']) for x in [0,90,150,300]],explicit_only_sensitivity=calc(funding=False),dilution_sensitivity=calc(shares=SHARES*1.03)['value'],cash_accrual_sensitivity=dict(owner_cash_reported=623.381,without_full_accrued_comp_inflow=623.381-62.553),timing_sensitivity=(cases['base']['ev']*(1.091**(2/12))+NET)/SHARES)
json.dump(out,open(P/'model.json','w'),indent=2);print({k:v['value'] for k,v in cases.items()});print(out['reverse']);print('bridge',NET,'TV',cases['base']['terminal_weight'],'explicitonly',out['explicit_only_sensitivity']['value'])
