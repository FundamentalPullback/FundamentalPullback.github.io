from pathlib import Path
import json
P=Path(__file__).parent
PRICE=42.13;SHARES=152.570075;START=2435
CASH=154.066+178.612;DEBT=512.5;RESERVE=100;EARNOUT=61.1;DEFERRED=15;RETIREMENT=35.213+.430;UNCERTAIN_TAX=2.556;FINLEASE=2.432;REPATTAX=293*.05
NET=CASH-DEBT-RESERVE-EARNOUT-DEFERRED-RETIREMENT-FINLEASE-REPATTAX-UNCERTAIN_TAX
# Operating lease expense remains in EBIT; operating lease liability is not subtracted again.
def calc(gd=0,md=0,w=.102,g=.03,roic=.25,tax=.24,net=NET,shares=SHARES,funding=True):
 growth=[max(0,x+gd) for x in [.14,.12,.10,.09,.08]];growth += [growth[-1]+(g-growth[-1])*i/5 for i in range(1,6)]
 margins=[x+md for x in [.15,.155,.16,.165,.17]+[.17]*5];r=START;rows=[];pv=0
 for i in range(10):
  old=r;r*=1+growth[i];ebit=r*margins[i];nopat=ebit*(1-tax);da=r*.018;capex=r*.025;nwc=(r-old)*.18
  explicit=capex-da+nwc;economic=nopat*growth[i]/roic
  # Fund the greater of explicit incremental cash requirements and assumed capital productivity in years1-5.
  raw=max(explicit,economic) if funding else explicit;weight=max(0,(i-4)/5);reinv=raw*(1-weight)+economic*weight;fcff=nopat-reinv;pvfcff=fcff/(1+w)**(i+1);pv+=pvfcff
  rows.append(dict(year=i+1,revenue=r,growth=growth[i],ebit_margin=margins[i],ebit=ebit,nopat=nopat,da=da,capex=capex,delta_nwc=nwc,explicit_reinvestment=explicit,economic_reinvestment=economic,transition_weight=weight,reinvestment=reinv,fcff=fcff,pv_fcff=pvfcff))
 tn=r*(1+g)*margins[-1]*(1-tax);tri=tn*g/roic;tv=(tn-tri)/(w-g);pvtv=tv/(1+w)**10;ev=pv+pvtv
 return dict(value=(ev+net)/shares,ev=ev,equity=ev+net,net_bridge=net,pv_explicit=pv,pv_terminal=pvtv,terminal_weight=pvtv/ev,terminal_nopat=tn,terminal_reinvestment=tri,terminal_fcff=tn-tri,rows=rows,assumptions=dict(wacc=w,g=g,roic=roic,tax=tax,shares=shares,growth_delta=gd,margin_delta=md,funding_guard=funding,maintenance_da=.018,capex=.025,nwc_ratio=.18))
def solve(fn,lo,hi):
 for _ in range(100):
  mid=(lo+hi)/2
  if fn(mid)<PRICE:lo=mid
  else:hi=mid
 return (lo+hi)/2
cases={'bear':calc(-.05,-.02,.112,.025,.20),'base':calc(),'bull':calc(.04,.02,.092,.035,.30)}
out=dict(asof='2026-11-04',price=PRICE,price_date='2026-11-03 16:00 America/New_York',cases=cases,capital_bridge=dict(unrestricted_cash=154.066,short_term_investments=178.612,nominal_debt=DEBT,operating_cash_reserve=RESERVE,contingent_consideration=EARNOUT,deferred_consideration=DEFERRED,retirement_reserve=RETIREMENT,finance_leases=FINLEASE,uncertain_tax_liability=UNCERTAIN_TAX,foreign_distribution_tax_assumption=REPATTAX,net=NET),historical_A003={'bear':1.65*18/1.1,'base':1.90*22/1.1,'bull':2.15*25/1.1,'method':'Normalized EPS times exit multiple discounted one year, not FCFF; old15% discount not current rule'},reverse=dict(growth_extra_first5=solve(lambda x:calc(gd=x)['value'],-.05,.3),margin_extra_all_years=solve(lambda x:calc(md=x)['value'],-.05,.3)),sensitivity=[dict(wacc=w,g=g,value=calc(w=w,g=g)['value']) for w in [.092,.097,.102,.107,.112] for g in [.025,.03,.035]],roic_sensitivity=[dict(roic=r,value=calc(roic=r)['value']) for r in [.18,.20,.25,.30,.35]],tax_sensitivity=[dict(tax=t,value=calc(tax=t)['value']) for t in [.21,.24,.27]],claims_sensitivity=[dict(extra_claims=x,value=calc(net=NET-x)['value']) for x in [-14.65,0,71.9,100]],explicit_only_stress=calc(funding=False),dilution_sensitivity=calc(shares=SHARES*1.03)['value'])
json.dump(out,open(P/'model.json','w'),indent=2);print({k:v['value'] for k,v in cases.items()});print(out['reverse']);print('NET',NET,'TV',cases['base']['terminal_weight'],'explicit-only',out['explicit_only_stress']['value'])
