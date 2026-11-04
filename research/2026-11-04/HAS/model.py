from pathlib import Path
import json
P=Path(__file__).parent
PRICE=117.97;SHARES=142.5;START=5181.0
# September cash/debt. Prior-year tax and pension proxies explicitly not September actuarial amounts.
NET=850.7+576.2-350-3527.8-24.6-52.6-52.1-30
BRIDGE=dict(cash=850.7,treasuries=576.2,operating_cash_reserve=350,nominal_debt=3527.8,nci=24.6,pension_prior_year_proxy=52.6,tax_prior_year_proxy=52.1,legacy_environmental=30,net=NET)
def calc(gd=0,md=0,w=.10,g=.025,roic=.20,tax=.24,net=NET,shares=SHARES,da=.029,capex=.04,start=START):
 growth=[max(0,v+gd) for v in [.08,.07,.06,.05,.04]];growth += [growth[-1]+(g-growth[-1])*i/5 for i in range(1,6)]
 margins=[v+md for v in [.23,.24,.25,.255,.26]+[.26]*5];r=start;rows=[];pv=0
 for i in range(10):
  old=r;r*=1+growth[i];ebit=r*margins[i];nopat=ebit*(1-tax);d=r*da;c=r*capex;nwc=(r-old)*.10;explicit=c-d+nwc;economic=nopat*growth[i]/roic;reinv=max(explicit,economic);fcff=nopat-reinv;pvf=fcff/(1+w)**(i+1);pv+=pvf
  rows.append(dict(year=i+1,revenue=r,growth=growth[i],ebit_margin=margins[i],ebit=ebit,nopat=nopat,da=d,capex=c,delta_nwc=nwc,explicit_reinvestment=explicit,economic_reinvestment=economic,reinvestment=reinv,additional_reinvestment_reserve=reinv-explicit,fcff=fcff,pv_fcff=pvf))
 tr=r*(1+g);tn=tr*margins[-1]*(1-tax);te=tr*(capex-da)+(tr-r)*.10;tri=max(te,tn*g/roic);tcf=tn-tri;pvtv=tcf/(w-g)/(1+w)**10;ev=pv+pvtv
 return dict(value=(ev+net)/shares,ev=ev,equity=ev+net,net_bridge=net,pv_explicit=pv,pv_terminal=pvtv,terminal_weight=pvtv/ev,terminal_nopat=tn,terminal_reinvestment=tri,terminal_fcff=tcf,rows=rows,assumptions=dict(wacc=w,g=g,roic=roic,tax=tax,shares=shares,growth_delta=gd,margin_delta=md,da_ratio=da,capex_ratio=capex,nwc_ratio=.10))
def solve(fn,lo,hi):
 assert fn(lo)<=PRICE<=fn(hi)
 for _ in range(90):
  m=(lo+hi)/2
  if fn(m)<PRICE:lo=m
  else:hi=m
 return (lo+hi)/2
cases={'bear':calc(-.04,-.04,.11,.015,.15,.26),'base':calc(),'bull':calc(.04,.035,.09,.03,.25,.23)}
def old(flow,g):
 pv=sum(flow*(1+g)**i/(1.10)**i for i in range(1,6));tv=flow*(1+g)**5*1.025/(.10-.025)/(1.10)**5
 return dict(value=(pv+tv)/143.2,terminal_weight=tv/(pv+tv))
scan=[dict(extra_growth=x/1000,value=calc(gd=x/1000)['value']) for x in range(0,401)]
roots=[]
for a,b in zip(scan,scan[1:]):
 if (a['value']-PRICE)*(b['value']-PRICE)<0:roots.append([a['extra_growth'],b['extra_growth']])
out=dict(asof='2026-11-04',price=PRICE,price_date='2026-11-03 16:00 America/New_York',cases=cases,capital_bridge=BRIDGE,reverse=dict(margin_extra_all_years=solve(lambda x:calc(md=x)['value'],-.10,.30),growth_scan=scan,growth_root_brackets=roots,growth_roots=[solve(lambda x:calc(gd=x)['value'],a,b) for a,b in roots if calc(gd=a)['value']<PRICE],growth_scan_max=max(scan,key=lambda x:x['value'])),sensitivity=[dict(wacc=w,g=g,value=calc(w=w,g=g)['value']) for w in [.09,.095,.10,.105,.11] for g in [.015,.02,.025,.03]],roic_sensitivity=[dict(roic=r,value=calc(roic=r)['value']) for r in [.12,.15,.20,.25,.30]],capital_sensitivity={k:calc(net=NET+v)['value'] for k,v in {'remove_prior_tax_proxy':52.1,'remove_prior_pension_proxy':52.6,'cash_reserve250':100,'cash_reserve450':-100,'refund_receivable_recovery13':13}.items()},pullforward_sensitivity=calc(start=START-40)['value'],amortization_sensitivity=calc(md=-80/START)['value'],dilution_sensitivity=calc(shares=SHARES*1.03)['value'],historical_A026=dict(method='Five-year FCFE plus perpetuity; reconstructed from disclosed assumptions, not recovered original executable. No net-debt deduction.',cases={k:old(*v) for k,v in {'bear':(800,.03),'base':(900,.07),'bull':(1000,.10)}.items()}))
json.dump(out,open(P/'model.json','w'),indent=2);print({k:v['value'] for k,v in cases.items()});print(NET,out['reverse']['margin_extra_all_years'],out['reverse']['growth_root_brackets'])
