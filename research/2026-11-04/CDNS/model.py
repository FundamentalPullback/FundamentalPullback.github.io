"""USD millions. Deterministic FCFF migration, not a trade authorization."""
from pathlib import Path
import json
P=Path(__file__).parent
SHARES=275.278;PRICE=323.75;R0=6402;NET=1452.020-500-2650

def old_fcfe(growth=.15,target=.25,ke=.105,g=.03):
 r=R0;pv=0;rows=[]
 for y in range(1,11):
  gr=growth if y<=5 else growth+(g-growth)*(y-5)/5;r*=1+gr;m=.20+(target-.20)*min(y/5,1);cf=r*m;pv+=cf/(1+ke)**y;rows.append(dict(year=y,revenue=r,cash_margin=m,fcfe=cf))
 tv=cf*(1+g)/(ke-g)/(1+ke)**10
 return dict(value=(pv+tv)/SHARES,rows=rows,terminal_weight=tv/(pv+tv))

def calc(growth=.15,margin_end=.33,w=.101,g=.03,roic=.25,net=NET,terminal_reinvestment=True,trans=True,tax=.24,capex_ratio=.035,nwc_increment=.05):
 r=R0;pv=0;rows=[]
 for y in range(1,11):
  gr=growth if y<=5 else growth+(g-growth)*(y-5)/5;prev=r;r*=1+gr
  m=.287+(margin_end-.287)*min(y/5,1)
  if y>5:m=margin_end+.01*(y-5)/5
  ebit=r*m;nopat=ebit*(1-tax);da=r*.02;capex=r*capex_ratio;nwc=(r-prev)*nwc_increment
  # Replace the explicit investment profile progressively with sustainable ROIC-linked reinvestment, not an abrupt terminal cliff.
  explicit_reinv=capex-da+nwc;weight=(y-5)/5 if trans and y>5 else 0
  sustainable_reinv=nopat*g/roic;reinv=explicit_reinv*(1-weight)+sustainable_reinv*weight
  fcff=nopat-reinv;pv+=fcff/(1+w)**y
  rows.append(dict(year=y,growth=gr,revenue=r,ebit_margin=m,ebit=ebit,tax=ebit*tax,nopat=nopat,maintenance_da=da,capex=capex,delta_nwc=nwc,explicit_reinvestment=explicit_reinv,transition_weight=weight,reinvestment=reinv,fcff=fcff,pv_fcff=fcff/(1+w)**y))
 tn=r*(1+g)*m*(1-tax);tri=tn*g/roic if terminal_reinvestment else (capex-da+nwc)*(1+g);tcf=tn-tri;pvtv=tcf/(w-g)/(1+w)**10;ev=pv+pvtv;eq=ev+net
 return dict(value=eq/SHARES,ev=ev,equity=eq,net_bridge=net,pv_explicit=pv,pv_terminal=pvtv,terminal_weight=pvtv/ev,terminal_fcff=tcf,terminal_nopat=tn,terminal_reinvestment=tri,assumptions=dict(growth=growth,margin_year5=margin_end,margin_terminal=m,wacc=w,g=g,roic=roic,tax=tax,shares=SHARES,capex_ratio=capex_ratio,nwc_increment=nwc_increment),rows=rows)
cases={'bear':calc(.10,.305,.111,.025,.20),'base':calc(),'bull':calc(.20,.355,.091,.035,.30)}
old={'bear':old_fcfe(.10,.225,.115,.025),'base':old_fcfe(),'bull':old_fcfe(.20,.275,.095,.035)}
def solve(fn,lo,hi):
 for _ in range(100):
  x=(lo+hi)/2
  if fn(x)<PRICE:lo=x
  else:hi=x
 return (lo+hi)/2
# Pure financing/method comparison: preserve old FCFE cash path; add normalized net interest then discount at WACC and bridge financial claims.
# $130m interest minus $40m cash interest, taxed24%, fixed annual normalized cost.
def migration(w=.105,unlever=False,net=0,terminal_charge=False):
 rows=old['base']['rows'];pv=0
 for row in rows:
  fc=row['fcfe']+(90*.76 if unlever else 0);pv+=fc/(1+w)**row['year']
 terminal=fc*1.03
 if terminal_charge:terminal*=1-.03/.25
 tv=terminal/(w-.03)/(1+w)**10
 return (pv+tv+net)/SHARES
bridge=[['Exact A106 FCFE reproduction',old['base']['value']],['Add normalized net interest after tax; same10.5% discount, no bridge',migration(unlever=True)],['Discount same unlevered cash at10.1%',migration(.101,True)],['Add excess cash952.020 minus nominal debt2650',migration(.101,True,NET)],['Apply terminal reinvestment12% to legacy terminal cash (diagnostic only)',migration(.101,True,NET,True)],['Full operating FCFF forecast and smooth sustainable reinvestment',cases['base']['value']]]
out=dict(asof='2026-11-04',price=PRICE,price_date='2026-11-03 regular close16:00EST',status='research only; no entry',historical_A106=old,cases=cases,bridge=bridge,reverse=dict(first5_growth=solve(lambda x:calc(growth=x)['value'],.01,.6),year5_margin=solve(lambda x:calc(margin_end=x)['value'],.20,.90)),sensitivity=[dict(wacc=w,g=g,value=calc(w=w,g=g)['value']) for w in [.091,.096,.101,.106,.111] for g in [.025,.03,.035]],reserve_sensitivity=[dict(reserve=v,value=calc(net=1452.02-v-2650)['value']) for v in [0,500,1000]],terminal_roic_sensitivity=[dict(roic=v,value=calc(roic=v)['value']) for v in [.15,.20,.25,.30]],tax_sensitivity=[dict(tax=v,value=calc(tax=v)['value']) for v in [.24,.27,.29]],timing_sensitivity=(cases['base']['ev']/(1.101**(2/12))+NET)/SHARES)
assert abs(old['base']['value']-150.68)<.005
assert all(len(v['rows'])==10 and v['assumptions']['wacc']>v['assumptions']['g'] for v in cases.values())
json.dump(out,open(P/'model.json','w'),indent=2)
print({k:v['value'] for k,v in cases.items()});print(out['reverse']);print(bridge)
