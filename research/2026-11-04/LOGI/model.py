from pathlib import Path
import json
P=Path(__file__).parent
PRICE=92.85;SHARES=143.770;START=4953.074
NET=1507.647-250-97.390-58.151-32-50
# September capital. Deferred compensation assets and liabilities matched, no net addition.
def calc(gd=0,md=0,w=.105,g=.025,roic=.25,tax=.18,net=NET,shares=SHARES,da=.013,capex=.015,funding=True):
 growth=[.03,.05,.05,.04,.04];growth=[max(0,v+gd) for v in growth];growth += [growth[-1]+(g-growth[-1])*i/5 for i in range(1,6)]
 margins=[v+md for v in [.165,.17,.17,.17,.17]+[.17]*5];r=START;rows=[];pv=0
 for i in range(10):
  old=r;r*=1+growth[i];ebit=r*margins[i];nopat=ebit*(1-tax);d=r*da;c=r*capex;nwc=(r-old)*.12;explicit=c-d+nwc;economic=nopat*growth[i]/roic
  raw=max(explicit,economic) if funding else explicit;weight=max(0,(i-4)/5);reinv=raw*(1-weight)+economic*weight;fcff=nopat-reinv;pvf=fcff/(1+w)**(i+1);pv+=pvf
  rows.append(dict(year=i+1,revenue=r,growth=growth[i],ebit_margin=margins[i],ebit=ebit,nopat=nopat,da=d,capex=c,delta_nwc=nwc,explicit_reinvestment=explicit,economic_reinvestment=economic,transition_weight=weight,reinvestment=reinv,additional_reinvestment_reserve=reinv-explicit,fcff=fcff,pv_fcff=pvf))
 tn=r*(1+g)*margins[-1]*(1-tax);tri=tn*g/roic;tcf=tn-tri;pvtv=tcf/(w-g)/(1+w)**10;ev=pv+pvtv
 return dict(value=(ev+net)/shares,ev=ev,equity=ev+net,net_bridge=net,pv_explicit=pv,pv_terminal=pvtv,terminal_weight=pvtv/ev,terminal_nopat=tn,terminal_reinvestment=tri,terminal_fcff=tcf,rows=rows,assumptions=dict(wacc=w,g=g,roic=roic,tax=tax,shares=shares,growth_delta=gd,margin_delta=md,da_ratio=da,capex_ratio=capex,nwc_ratio=.12,funding_guard=funding))
def solve(fn,lo,hi):
 for _ in range(100):
  mid=(lo+hi)/2
  if fn(mid)<PRICE:lo=mid
  else:hi=mid
 return (lo+hi)/2
cases={'bear':calc(-.03,-.03,.12,.015,.18),'base':calc(),'bull':calc(.03,.02,.095,.03,.30)}
def old_fcfe(flow,g,w,t):
 pv=0;current=flow
 for i in range(10):
  rate=g if i<5 else g+(t-g)*(i-4)/5
  current*=1+rate;pv+=current/(1+w)**(i+1)
 tv=current*(1+t)/(w-t)/(1+w)**10
 return dict(value=(pv+tv)/SHARES,terminal_weight=tv/(pv+tv),shares=SHARES)
old={'bear':old_fcfe(650,0,.12,.02),'base':old_fcfe(750,.05,.105,.025),'bull':old_fcfe(825,.08,.095,.03)}
out=dict(asof='2026-11-04',price=PRICE,price_date='2026-11-03 16:00 America/New_York',cases=cases,capital_bridge=dict(cash=1507.647,operating_cash_reserve=250,noncurrent_tax_liability=97.390,employee_benefit_obligations=58.151,unpaid_repurchases=32,unpaid_capex_sensitivity_only=11.159,assumed_repatriation_reserve=50,nominal_debt=0,net=NET),reverse=dict(growth_extra_first5=solve(lambda x:calc(gd=x)['value'],-.03,.3),margin_extra_all_years=solve(lambda x:calc(md=x)['value'],-.05,.3)),sensitivity=[dict(wacc=w,g=g,value=calc(w=w,g=g)['value']) for w in [.095,.10,.105,.11,.12] for g in [.015,.02,.025,.03]],roic_sensitivity=[dict(roic=r,value=calc(roic=r)['value']) for r in [.18,.20,.25,.30,.35]],tax_sensitivity=[dict(tax=t,value=calc(tax=t)['value']) for t in [.15,.18,.21]],explicit_only_sensitivity=calc(funding=False),dilution_sensitivity=calc(shares=SHARES*1.03)['value'],unpaid_capex_sensitivity=calc(net=NET-11.159)['value'],repatriation_reserve_sensitivity=[dict(reserve=x,value=calc(net=NET+50-x)['value']) for x in [0,50,100]],historical_A108=dict(published_rounded=dict(bear=41.54,base=76.60,bull=120.42),reconstruction=old,status='New reconstruction from disclosed assumptions and Q2 diluted143.770m matches rounded publication; original executable unavailable, not a recovered original file'))
json.dump(out,open(P/'model.json','w'),indent=2);print({k:v['value'] for k,v in cases.items()});print(out['reverse']);print('NET',NET,'TV',cases['base']['terminal_weight'])
