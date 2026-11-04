from pathlib import Path
import json
P=Path(__file__).parent
PRICE=189.35;SHARES=85.2;START=4067.3*1.10
# Sep cash/debt, known subsequent Overly cash88.7 and matching revolver40; both financing legs included once.
CASH=388.1+40-88.7;DEBT=2041.2+40;RESERVE=200;PENSION=31.8;EARNOUT=30.3;DEFERRED_NET=.2
NET=CASH-DEBT-RESERVE-PENSION-EARNOUT-DEFERRED_NET

def calc(gd=0,md=0,w=.092,g=.03,roic=.20,net=NET,tax=.20,da_ratio=.032,capex_ratio=.025,nwc_ratio=.15,start=START,shares=SHARES,margin_path=None,growth_funded=False):
 growth=[.06,.05,.05,.04,.04];growth=[max(0,x+gd) for x in growth];growth += [growth[-1]+(g-growth[-1])*i/5 for i in range(1,6)]
 margins=margin_path or ([.215,.22,.225,.23,.23]+[.23+.005*i/5 for i in range(1,6)]);margins=[x+md for x in margins]
 r=start;rows=[];pv=0
 for i in range(10):
  prev=r;r*=1+growth[i];ebit=r*margins[i];nopat=ebit*(1-tax);da=r*da_ratio;capex=r*capex_ratio;nwc=(r-prev)*nwc_ratio
  reinv0=capex-da+nwc;weight=max(0,(i-4)/5);reinv=reinv0*(1-weight)+nopat*g/roic*weight;reinv=nopat*growth[i]/roic if growth_funded else reinv;cf=nopat-reinv;pv+=cf/(1+w)**(i+1)
  rows.append(dict(year=i+1,revenue=r,growth=growth[i],ebit_margin=margins[i],ebit=ebit,nopat=nopat,da=da,capex=capex,delta_nwc=nwc,unblended_reinvestment=reinv0,transition_weight=weight,reinvestment=reinv,fcff=cf,pv_fcff=cf/(1+w)**(i+1)))
 tn=r*(1+g)*margins[-1]*(1-tax);tri=tn*g/roic;tcf=tn-tri;pvtv=tcf/(w-g)/(1+w)**10;ev=pv+pvtv
 return dict(value=(ev+net)/shares,ev=ev,equity=ev+net,net_bridge=net,pv_explicit=pv,pv_terminal=pvtv,terminal_weight=pvtv/ev,terminal_nopat=tn,terminal_reinvestment=tri,terminal_fcff=tcf,rows=rows,assumptions=dict(wacc=w,g=g,roic=roic,tax=tax,shares=shares,growth_delta=gd,margin_delta=md,da_ratio=da_ratio,capex_ratio=capex_ratio,delta_nwc_ratio=nwc_ratio,growth_funded=growth_funded))

def old(gd=0,md=0,w=.095,g=.03,roic=.18):
 r=4289;pv=0
 for y,(gr,ma) in enumerate(zip([.06,.05,.05,.04,.04],[.215,.218,.22,.22,.22]),1):
  prev=r;r*=1+max(0,gr+gd);nopat=r*(ma+md)*.8;cf=nopat+r*.033-r*.025-(r-prev)*.15;pv+=cf/(1+w)**y
 tv=r*(1+g)*(ma+md)*.8*(1-g/roic)/(w-g)/(1+w)**5
 return (pv+tv-1710.5)/85.9
cases={'bear':calc(-.03,-.02,.102,.025,.17),'base':calc(),'bull':calc(.03,.02,.082,.035,.23)}
def solve(fn,lo,hi):
 for _ in range(100):
  x=(lo+hi)/2
  if fn(x)<PRICE:lo=x
  else:hi=x
 return (lo+hi)/2
out=dict(asof='2026-11-04',price=PRICE,price_date='2026-11-03 16:00 EST regular close',cases=cases,historical_A064={'bear':old(-.03,-.02,.105,.025,.15),'base':old(),'bull':old(.03,.02,.085,.035,.21)},capital_bridge=dict(cash_september=388.1,nominal_debt_september=2041.2,new_revolver=40,overly_consideration=88.7,proforma_cash=CASH,proforma_debt=DEBT,operating_reserve=RESERVE,pension_gross_deficit_proxy=PENSION,earnout_reserve_assumption=EARNOUT,deferred_comp_net_claim=DEFERRED_NET,net=NET),reverse=dict(growth_extra_first5=solve(lambda x:calc(gd=x)['value'],-.02,.3),margin_extra_all_years=solve(lambda x:calc(md=x)['value'],-.02,.3)),sensitivity=[dict(wacc=w,g=g,value=calc(w=w,g=g)['value']) for w in [.082,.087,.092,.097,.102] for g in [.025,.03,.035]],claims_sensitivity=[dict(extra_claims=v,value=calc(net=NET-v)['value']) for v in [-30.3,0,10.5,50]],roic_sensitivity=[dict(roic=v,value=calc(roic=v)['value']) for v in [.15,.18,.20,.25]],da_sensitivity=[dict(da_ratio=v,value=calc(da_ratio=v)['value']) for v in [.025,.03,.032]],timing_sensitivity=(cases['base']['ev']/(1.092**(2/12))+NET)/SHARES)
bridge=[['A064 exact five-year base reconstruction',old()]]
a=dict(start=4289,shares=85.9,net=-1710.5,w=.095,roic=.18,da_ratio=.033,margin_path=[.215,.218,.22,.22,.22]+[.22]*5)
bridge.append(['Ten-year horizon and years6-10 transition, same old drivers',calc(**a)['value']])
a['start']=START;bridge.append(['Current FY2026 revenue guidance midpoint as starting base',calc(**a)['value']])
a['shares']=SHARES;bridge.append(['Latest Q3 diluted share proxy',calc(**a)['value']])
a['net']=NET;bridge.append(['Known Overly/debt bridge, operating cash and claim reserves',calc(**a)['value']])
a['margin_path']=None;bridge.append(['Current normalized margin path',calc(**a)['value']])
a['da_ratio']=.032;bridge.append(['D&A3.2% instead3.3%',calc(**a)['value']])
a['roic']=.20;bridge.append(['Terminal ROIC20% instead18%',calc(**a)['value']])
a['w']=.092;bridge.append(['WACC9.2% instead9.5%; final central',calc(**a)['value']])
out['bridge']=bridge
out['growth_funding_stress']=calc(growth_funded=True)
out['first5_growth_reinvestment']={'revenue_growth':cases['base']['rows'][4]['revenue']/START-1,'cumulative_reinvestment':sum(x['reinvestment'] for x in cases['base']['rows'][:5])}
out['noncore_recovery_sensitivity']=[dict(recovery_fraction=f,recovery=130.6*f,value=calc(net=NET+130.6*f)['value']) for f in [0,.5,1]]
assert all(len(v['rows'])==10 and v['assumptions']['wacc']>v['assumptions']['g'] for v in cases.values())
json.dump(out,open(P/'model.json','w'),indent=2);print({k:v['value'] for k,v in cases.items()});print(out['historical_A064']);print(out['reverse']);print(out['capital_bridge'])
