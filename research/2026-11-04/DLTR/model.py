from pathlib import Path
import json
P=Path(__file__).parent
PRICE=134.07;SHARES=190.9;START=20068.7
NET=1058.1-500-2950-23.4-.5-5.3
# New reconstruction. The first projected year is a normalized forward twelve-month period, not fiscal2026 guidance.
def calc(case='base',gd=0,md=0,w=None,g=None,roic=.12,tax=.25,net=NET,shares=SHARES,funding=True,transition=True,oneoff=40):
 initial,gs,ms,rate,tg={'bear':(20370,[.03,.025,.02,.015],[.072,.075,.077,.08,.08],.11,.02),'base':(21000,[.05,.045,.04,.035],[.092,.095,.097,.10,.10],.10,.025),'bull':(21630,[.07,.065,.06,.055],[.112,.115,.117,.12,.12],.09,.03)}[case]
 w=rate if w is None else w;g=tg if g is None else g
 growth=[initial/START-1]+[v+gd for v in gs];growth += [growth[-1]+(g-growth[-1])*i/5 for i in range(1,6)]
 margins=[v+md for v in ms]+[ms[-1]+md]*5;r=START;rows=[];pv=0
 for i in range(10):
  old=r;r*=1+growth[i];cr=.055-(.01*max(0,i-4)/5 if transition else 0)
  ebit=r*margins[i]-(oneoff if i==0 else 0);nopat=ebit*(1-tax);da=r*.034;capex=r*cr;nwc=(r-old)*.10;explicit=capex-da+nwc;economic=max(0,r*margins[i]*(1-tax)*growth[i]/roic);reinv=max(explicit,economic) if funding else explicit;fcff=nopat-reinv;pvf=fcff/(1+w)**(i+1);pv+=pvf
  rows.append(dict(year=i+1,revenue=r,growth=growth[i],core_ebit_margin=margins[i],incremental_reinvestment_expense=oneoff if i==0 else 0,ebit=ebit,nopat=nopat,core_nopat=r*margins[i]*(1-tax),da=da,capex=capex,capex_ratio=cr,delta_nwc=nwc,explicit_reinvestment=explicit,economic_reinvestment=economic,additional_reinvestment_reserve=reinv-explicit,reinvestment=reinv,fcff=fcff,pv_fcff=pvf))
 tr=r*(1+g);tn=tr*margins[-1]*(1-tax);te=tr*(.045-.034)+(tr-r)*.10;tri=max(te,tn*g/roic);tcf=tn-tri;pvtv=tcf/(w-g)/(1+w)**10;ev=pv+pvtv
 return dict(value=(ev+net)/shares,ev=ev,equity=ev+net,net_bridge=net,pv_explicit=pv,pv_terminal=pvtv,terminal_weight=pvtv/ev,terminal_nopat=tn,terminal_explicit_reinvestment=te,terminal_reinvestment=tri,terminal_fcff=tcf,rows=rows,assumptions=dict(case=case,wacc=w,g=g,roic=roic,tax=tax,shares=shares,growth_delta_years2to5=gd,margin_delta_all10_and_terminal=md,initial_revenue=initial,da_ratio=.034,terminal_capex_ratio=.045,nwc_ratio=.10,funding_guard=funding,capex_transition=transition,first_year_incremental_expense=oneoff))
def solve(fn,lo,hi):
 assert fn(lo)<PRICE<fn(hi),(fn(lo),fn(hi))
 for _ in range(100):
  mid=(lo+hi)/2
  if fn(mid)<PRICE:lo=mid
  else:hi=mid
 return (lo+hi)/2
old={k:calc(k,funding=False,transition=False,oneoff=0,net=1058.1-500-2950) for k in ['bear','base','bull']}
out=dict(asof='2026-11-04',price=PRICE,price_date='2026-11-03 16:00 America/New_York',cases={k:calc(k) for k in ['bear','base','bull']},capital_bridge=dict(cash=1058.1,operating_reserve=500,nominal_debt=2950,longterm_tax_payable=23.4,unsettled_repurchases=.5,subsequent_repurchases=5.3,net=NET,restricted_cash_excluded=43.7),historical_A113=dict(published={'bear':35.55,'base':72.78,'bull':130.27},reconstruction=old,status='New reconstruction from disclosed FCFF table; original executable not recovered. Not a migration from FCFE.'),reverse=dict(growth_extra_years2to5=None,growth_scan=[dict(delta=x/1000,value=calc(gd=x/1000)['value']) for x in range(401)],margin_extra_all_years=solve(lambda x:calc(md=x)['value'],0,.2)),sensitivity=[dict(wacc=w,g=g,value=calc(w=w,g=g)['value']) for w in [.09,.095,.10,.105,.11] for g in [.02,.025,.03]],roic_sensitivity=[dict(roic=x,value=calc(roic=x)['value']) for x in [.10,.12,.15,.18,.20]],tax_sensitivity=[dict(tax=x,value=calc(tax=x)['value']) for x in [.23,.25,.28]],capital_sensitivity=dict(reserve250=calc(net=NET+250)['value'],reserve750=calc(net=NET-250)['value'],lease_guarantee_full30=calc(net=NET-30)['value'],retroactive_duties26=calc(net=NET-26)['value'],remove_postbalance_buybacks=calc(net=NET+5.3)['value']),expense_sensitivity=[dict(first_year_expense=x,value=calc(oneoff=x)['value']) for x in [0,40,100,200]],dilution_sensitivity=calc(shares=SHARES*1.03)['value'],no_growth_funding_floor=calc(funding=False)['value'],no_capex_transition=calc(transition=False)['value'])
json.dump(out,open(P/'model.json','w'),indent=2)
if __name__=='__main__':print({k:round(v['value'],4) for k,v in out['cases'].items()},'old',{k:round(v['value'],5) for k,v in old.items()})
