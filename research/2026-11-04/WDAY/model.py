import json,math
from pathlib import Path
P=Path(__file__).parent
price=197.94; shares=246.307
# all USD millions; fixed existing diluted proxy; no assumed free buybacks.
def calc(gdelta=0,mdelta=0,w=.095,g=.03,roic=.25,net=-377,margins=None,reserve=0,fade_da=True,transition_reinvestment=False):
 growth=[11400/10155-1,.10,.09,.08,.07]
 growth=[x+gdelta for x in growth]+[.07+gdelta+((g-(.07+gdelta))*i/5) for i in range(1,6)]
 mar=(margins or [.15,.17,.19,.21,.22])+[.22+(.24-.22)*i/5 for i in range(1,6)]
 mar=[x+mdelta for x in mar]
 r=10155;rows=[];pv=0
 for i in range(10):
  prev=r;r*=1+growth[i];ebit=r*mar[i];tax=ebit*.22;nopat=ebit-tax;da=r*(.035 if i<5 or not fade_da else .035-.01*(i-4)/5);capex=r*.025
  # customer funding and deferred commission change combined; fade financing benefit to zero
  wc_ratio=-.10 if i<5 else -.10*(10-(i+1))/5
  nwc=(r-prev)*wc_ratio
  transition_charge=nopat*g/roic*(i-4)/5 if transition_reinvestment and i>=5 else 0
  fcff=nopat+da-capex-nwc-transition_charge
  disc=(1+w)**(i+1);pv+=fcff/disc
  rows.append(dict(year=i+1,revenue=r,growth=growth[i],ebit_margin=mar[i],ebit=ebit,tax=tax,nopat=nopat,da=da,capex=capex,delta_nwc=nwc,transition_charge=transition_charge,fcff=fcff,pv_fcff=fcff/disc))
 term_nopat=r*(1+g)*mar[-1]*.78;reinv=term_nopat*g/roic;termfcff=term_nopat-reinv;tv=termfcff/(w-g);pvtv=tv/(1+w)**10;ev=pv+pvtv;eq=ev+net
 return dict(assumptions=dict(wacc=w,terminal_g=g,terminal_roic=roic,tax=.22,shares=shares,net_cash_bridge=net,margin_delta=mdelta,growth_delta_first5=gdelta),rows=rows,pv_explicit=pv,pv_terminal=pvtv,terminal_reinvestment=reinv,terminal_fcff=termfcff,terminal_share=pvtv/ev,ev=ev,equity_value=eq,value_per_share=eq/shares,versus_price=eq/shares/price-1)
cases={'adverse':calc(-.03,-.03,.105,.025,.20),'central':calc(),'favorable':calc(.02,.03,.085,.035,.30)}
# historical reconstruction only, same published A058 visible parameters; original code unavailable.
old=calc(w=.096,net=414,margins=[.16,.18,.20,.21,.22],fade_da=False)
bridge=[('A058 visible-assumption reconstruction, no exact-replication claim',old['value_per_share'])]
bridge.append(('Current net financial cash bridge before operating reserve (373)',calc(w=.096,net=373,margins=[.16,.18,.20,.21,.22],fade_da=False)['value_per_share']))
bridge.append(('Less explicitly estimated operating cash reserve750',calc(w=.096,net=-377,margins=[.16,.18,.20,.21,.22],fade_da=False)['value_per_share']))
bridge.append(('Near-term margins15/17/19 vs16/18/20',calc(w=.096,fade_da=False)['value_per_share']))
bridge.append(('WACC9.5 vs9.6 before D&A fade',calc(fade_da=False)['value_per_share']))
bridge.append(('D&A fades to capex through years6–10; current central',cases['central']['value_per_share']))
def solve(fun,lo,hi):
 for _ in range(100):
  mid=(lo+hi)/2
  if fun(mid)<price:lo=mid
  else:hi=mid
 return (lo+hi)/2
reverse_margin=solve(lambda v:calc(mdelta=v)['value_per_share'],-.1,.5)
reverse_growth=solve(lambda v:calc(gdelta=v)['value_per_share'],-.1,.3)
sensitivity=[dict(wacc=w,g=g,value=calc(w=w,g=g)['value_per_share']) for w in [.085,.09,.095,.10,.105] for g in [.025,.03,.035]]
result=dict(asof='2026-11-04',price=price,price_date='2026-11-03 regular close 16:00 EST',status='screen-grade; full post-acquisition value not certified',cases=cases,reverse=dict(constant_margin_extra=reverse_margin,first5_growth_extra=reverse_growth,margin_solution_year1=.15+reverse_margin,margin_solution_terminal=.24+reverse_margin),sensitivity=sensitivity,bridge=bridge,acquisition_sensitivity=[dict(hypothetical_net_cost=n,value=calc(net=-377-n)['value_per_share']) for n in [0,500,1000,2000]],terminal_roic_sensitivity=[dict(roic=r,value=calc(roic=r)['value_per_share']) for r in [.15,.2,.25,.3]],reserve_sensitivity=[dict(reserve=r,value=calc(net=373-r)['value_per_share']) for r in [0,750,1500]])
result['transition_reinvestment_sensitivity']={k:calc(transition_reinvestment=True,**kw) for k,kw in [('adverse',dict(gdelta=-.03,mdelta=-.03,w=.105,g=.025,roic=.20)),('central',{}),('favorable',dict(gdelta=.02,mdelta=.03,w=.085,g=.035,roic=.30))]}
assert all(len(v['rows'])==10 and v['assumptions']['wacc']>v['assumptions']['terminal_g'] for v in cases.values())
json.dump(result,open(P/'model.json','w'),indent=2)
for k,v in cases.items():print(k,v['value_per_share'],v['terminal_share'],v['rows'][0]['fcff'])
print('reverse',result['reverse']);print('bridge',bridge);print('sensitivity',sensitivity)
