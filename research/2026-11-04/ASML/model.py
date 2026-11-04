from pathlib import Path
import json
P=Path(__file__).parent;C=json.load(open(P/'capital.json'));PRICE=1552.14;FX=1.1179;SHARES=383.5;START=39473.5;NET=C['net_bridge']
def calc(gd=0,md=0,w=.095,g=.03,roic=.25,tax=.18,net=NET,shares=SHARES,fx=FX,first=53000,start=START):
 # First year estimates next twelve months, not FY2027 official guidance.
 gs=[first/start-1]+[.14+gd]*4;gs += [gs[-1]+(g-gs[-1])*i/5 for i in range(1,6)]
 margins=[.38+md,.39+md,.40+md,.40+md,.40+md]+[.40+md]*5
 r=start;rows=[];pv=0
 for i,gr in enumerate(gs):
  prev=r;r=first if i==0 else r*(1+gr);ebit=r*margins[i];nopat=ebit*(1-tax);da=r*.028;capex=r*.045;nwc=(r-prev)*.10;explicit=capex-da+nwc;economic=nopat*gr/roic;reinv=max(explicit,economic);fcff=nopat-reinv;p=fcff/(1+w)**(i+1);pv+=p
  rows.append(dict(year=i+1,revenue=r,growth=gr,ebit_margin=margins[i],ebit=ebit,nopat=nopat,da=da,capex=capex,delta_nwc=nwc,explicit_reinvestment=explicit,economic_reinvestment=economic,additional_reinvestment_reserve=reinv-explicit,reinvestment=reinv,fcff=fcff,pv_fcff=p))
 tr=r*(1+g);tn=tr*margins[-1]*(1-tax);te=tr*(.045-.028)+(tr-r)*.10;re=max(te,tn*g/roic);fc=tn-re;tv=fc/(w-g)/(1+w)**10;ev=pv+tv;eur=(ev+net)/shares
 return dict(value=eur*fx,value_eur=eur,ev_eur_m=ev,equity_eur_m=ev+net,pv_explicit=pv,pv_terminal=tv,terminal_weight=tv/ev,terminal_nopat=tn,terminal_reinvestment=re,terminal_fcff=fc,rows=rows,assumptions=dict(first_revenue=first,start_reference=start,growth_years2to5=.14+gd,margin_delta_all10andterminal=md,wacc=w,g=g,roic=roic,tax=tax,fx=fx,shares=shares,net_bridge=net))
def old(first=53000,gr=.14,margin=.38,w=.095):
 r=44000;pv=0;rows=[];gs=[first/r-1]+[gr]*4+[gr+(.03-gr)*i/5 for i in range(1,6)]
 for i,g in enumerate(gs):
  prev=r;r*=1+g;n=r*margin*.82;fc=n-r*.012-(r-prev)*.10;p=fc/(1+w)**(i+1);pv+=p;rows.append(dict(year=i+1,revenue=r,fcff=fc))
 tv=n*1.03*(1-.03/.25)/(w-.03)/(1+w)**10
 return dict(value=(pv+tv+5208.5)/385.3*1.1181,terminal_weight=tv/(pv+tv),rows=rows)
cases=dict(bear=calc(first=50000,gd=-.06,md=-.04,w=.105,g=.025,roic=.20,tax=.20),base=calc(),bull=calc(first=56000,gd=.06,md=.02,w=.085,g=.035,roic=.30,tax=.17))
def roots(fn,lo,hi,n=400):
 scan=[dict(x=lo+(hi-lo)*i/n,value=fn(lo+(hi-lo)*i/n)) for i in range(n+1)];roots=[]
 for a,b in zip(scan,scan[1:]):
  if (a['value']-PRICE)*(b['value']-PRICE)<0:
   l=a['x'];h=b['x'];fl=a['value']-PRICE
   for _ in range(70):
    m=(l+h)/2
    if (fn(m)-PRICE)*fl>0:l=m
    else:h=m
   roots.append((l+h)/2)
 return dict(scan=scan,roots=roots,maximum=max(scan,key=lambda a:a['value']))
out=dict(asof='2026-11-04',price=PRICE,price_date='2026-11-03',fx_date='2026-11-03',currency='EUR financials, USD per listed registered ordinary share; ratio1:1',classification='Conditional research valuation, not integral completion or entry approval',cases=cases,capital_bridge=C,historical_A033=dict(method='New reconstruction from disclosed inputs; original executable unavailable.',bear=old(50000,.08,.34,.105),base=old(),bull=old(56000,.20,.40,.09)),reverse_growth=roots(lambda x:calc(gd=x)['value'],0,.60),reverse_margin=roots(lambda x:calc(md=x)['value'],0,.25),sensitivity=[dict(wacc=w,g=g,value=calc(w=w,g=g)['value']) for w in [.085,.09,.095,.10,.105] for g in [.02,.025,.03,.035]],roic_sensitivity=[dict(roic=r,value=calc(roic=r)['value']) for r in [.15,.20,.25,.30,.40]],capital_sensitivity={k:calc(net=NET+v)['value'] for k,v in dict(add_all_strategic_book_assets=5454.1,remove_prior_tax_proxy=174.5,additional_debt500=-500,operating_cash3000=1000,operating_cash5000=-1000,no_post_period_distributions=C['post_period_buybacks']+C['dividend_proxy']).items()},guidance_baseline_sensitivity=dict(value=calc(start=44500)['value'],explanation='Replace historical TTM starting revenue with midpoint FY2026 revenue guidance; changes initial reinvestment, not actual cash or date. Not base.'),dilution_sensitivity=calc(shares=SHARES*1.03)['value'],fx_sensitivity={str(f):calc(fx=f)['value'] for f in [1.05,1.10,1.1179,1.15,1.20]})
json.dump(out,open(P/'model.json','w'),indent=2);print({k:round(v['value'],4) for k,v in cases.items()});print('old',{k:out['historical_A033'][k]['value'] for k in cases});print('reverse',out['reverse_growth']['roots'],out['reverse_margin']['roots'])
