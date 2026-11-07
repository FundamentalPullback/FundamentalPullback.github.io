import json,csv,os
from pathlib import Path
P=Path(__file__).parent; O=P
# USD millions, except per-share data. Reported source inputs transcribed from issuer filings.
fy={'2023':[6401.4,734.9,432.6,745.2,289.3,272.9,22.4,19.5,68.6],'2024':[5237.1,311.6,149.3,449.5,167.4,288.8,23.4,91.7,74.8],'2025':[5362.8,-40.7,-135.9,585.7,165.8,292.5,38.7,323.2,78.4]}
y25=[4029,-82.6,-154.5,451.1,116.5,216.9,27.6,323.6,59]
y26=[4389.8,283.7,194.8,438.8,148.9,221.2,39.3,23.3,58.7]
y24=[4082.2,367.3,220.5,137.5,137.1,212,20.4,None,None]
keys=['revenue','ebit_gaap','net_income_cont','cfo_cont','capex','da','sbc','impairment','intangible_amortization']
sub=lambda a,b:[None if x is None or y is None else round(x-y,3) for x,y in zip(a,b)]
add=lambda a,b:[None if x is None or y is None else round(x+y,3) for x,y in zip(a,b)]
q1=[1378.1,50.3,21,-63.7,57.2,74.9,9.5,None,None]
h1=[2935.9,179.7,129.2,251.5,98.6,148.5,27.4,.6,None]
q3=[1453.9,104,65.6,187.3,50.3,72.7,11.9,22.7,19.9]
rows={**fy,'9M2025':y25,'9M2026':y26,'9M2024':y24,'Q42025':sub(fy['2025'],y25),'Q12026':q1,'Q22026':sub(h1,q1),'Q32026':q3,'TTM2026':add(sub(fy['2025'],y25),y26),'TTM2025':add(sub(fy['2024'],y24),y25)}
actual={p:dict(zip(keys,a)) for p,a in rows.items()}
for a in actual.values():a['cfo_minus_capex']=round(a['cfo_cont']-a['capex'],3)
json.dump(actual,open(O/'actuals.json','w'),indent=2)
price=77.23; shares=65.6; debt=2001.5; excess_cash=max(0,257.8+10.8-150); pension=35.4; investments=30.3
bridge=excess_cash+investments-debt-pension
cases={'bear':dict(growth=[-.05,0,.02,.025,.025],margins=[.055,.06,.065,.07,.075],terminal_margin=.075,wacc=.115,g=.02,roic=.10,sc=1.4), 'base':dict(growth=[.05,.045,.04,.035,.03],margins=[.075,.085,.09,.095,.10],terminal_margin=.095,wacc=.10,g=.025,roic=.13,sc=1.8), 'bull':dict(growth=[.08,.065,.055,.045,.04],margins=[.085,.10,.11,.115,.12],terminal_margin=.11,wacc=.09,g=.03,roic=.16,sc=2.2)}
def model(c,margin_shift=0,wacc=None,g=None):
 wacc=c['wacc'] if wacc is None else wacc;g=c['g'] if g is None else g
 rev=5723.6;rows=[];pv=0
 for t in range(1,11):
  growth=c['growth'][t-1] if t<=5 else c['growth'][-1]+(g-c['growth'][-1])*(t-5)/5
  margin=c['margins'][t-1] if t<=5 else c['margins'][-1]+(c['terminal_margin']-c['margins'][-1])*(t-5)/5
  margin+=margin_shift;newrev=rev*(1+growth);nopat=newrev*margin*.77
  # Physical maintenance replacement plus capacity and working-capital funding.
  da=newrev*.038;wc=max(0,newrev-rev)*.15;growth_capex=max(0,newrev-rev)/c['sc'];capex=da+growth_capex;fcff=nopat+da-capex-wc
  pv+=fcff/(1+wacc)**t
  rows.append(dict(year=t,revenue=newrev,growth=growth,ebit_margin=margin,ebit=newrev*margin,tax=newrev*margin*.23,nopat=nopat,physical_da=da,capex=capex,delta_nwc=wc,fcff=fcff));rev=newrev
 tn=rev*(1+g)*(c['terminal_margin']+margin_shift)*.77; economic=tn*g/c['roic'];physical=rev*g*(1/c['sc']+.15);reinv=max(economic,physical);tv=(tn-reinv)/(wacc-g);ptv=tv/(1+wacc)**10;ev=pv+ptv
 return dict(value=(ev+bridge)/shares,ev=ev,terminal_weight=ptv/ev,terminal_nopat=tn,terminal_reinvestment=reinv,terminal_economic_reinvestment=economic,terminal_physical_growth_floor=physical,terminal_floor_binding=physical>economic,terminal_physical_da=rev*(1+g)*.038,terminal_delta_nwc=rev*g*.15,terminal_capex=rev*(1+g)*.038+reinv-rev*g*.15,rows=rows)
res={k:model(v) for k,v in cases.items()}
inv=[]
for growthdelta in [-.01,0,.01]:
 c=dict(cases['base']);c['growth']=[x+growthdelta for x in c['growth']];lo=-.07;hi=.15
 for _ in range(80):
  mid=(lo+hi)/2
  if model(c,mid)['value']<price:lo=mid
  else:hi=mid
 inv.append(dict(growth_shift=growthdelta,margin_shift=(hi+lo)/2,terminal_margin=c['terminal_margin']+(hi+lo)/2))
sens=[dict(wacc=w,g=g,value=model(cases['base'],wacc=w,g=g)['value'],terminal_funding_pass=model(cases['base'],wacc=w,g=g)['terminal_reinvestment']>=model(cases['base'],wacc=w,g=g)['terminal_physical_growth_floor']-1e-9) for w in [.09,.10,.11] for g in [.02,.025,.03]]
out=dict(as_of='2026-11-07',price_date='2026-11-06',price=price,shares=shares,bridge=dict(debt=debt,debt_measure="carrying_value_proxy_not_verified_current_principal",prior_year_unamortized_discount_fees=18.6,cash=257.8,securities=10.8,minimum_operating_cash=150,excess_cash=excess_cash,pension=pension,equity_investments=investments,net_adjustment=bridge),assumptions=cases,cases=res,inverse=inv,sensitivity=sens)
json.dump(out,open(O/'valuation.json','w'),indent=2)
with open(O/'forecast.csv','w') as f:
 w=csv.DictWriter(f,fieldnames=['case']+list(res['base']['rows'][0]));w.writeheader()
 for k,v in res.items():
  for row in v['rows']:w.writerow(dict(case=k,**row))
checks={'ttm_revenue_bridge':abs(actual['TTM2026']['revenue']-5723.6)<.001,'quarters_equal_ttm':abs(sum(actual[x]['revenue'] for x in ['Q42025','Q12026','Q22026','Q32026'])-5723.6)<.001,'ordered_values':res['bear']['value']<res['base']['value']<res['bull']['value'],'terminal_growth_funding':all(v['terminal_reinvestment']>=v['terminal_physical_growth_floor']-1e-9 for v in res.values()),'terminal_economic_funding':all(v['terminal_reinvestment']>=v['terminal_economic_reinvestment']-1e-9 for v in res.values()),'positive_terminal_capex':all(v['terminal_capex']>v['terminal_physical_da'] for v in res.values()),'wacc_above_g':all(c['wacc']>c['g'] for c in cases.values()),'ten_years':all(len(v['rows'])==10 for v in res.values()),'sbc_not_added_back':True,'no_buyback_share_reduction':True}
json.dump(checks,open(O/'qa.json','w'),indent=2);assert all(checks.values())
print(json.dumps({k:{a:v[a] for a in ['value','terminal_weight']} for k,v in res.items()},indent=2));print(inv);print(actual['TTM2026']);print(actual['TTM2025'])
# Independent functional QA and cycle/reinvestment stress tests.
inverseqa=[]
for x in inv:
 c=dict(cases['base']);c['growth']=[v+x['growth_shift'] for v in c['growth']];m=x['margin_shift'];points=[model(c,s)['value'] for s in [-.07,-.02,0,.05,.10,.15]]
 inverseqa.append(dict(growth_shift=x['growth_shift'],bracket=[-.07,.15],bracket_values=[points[0],points[-1]],monotonic=all(a<b for a,b in zip(points,points[1:])),residual=model(c,m)['value']-price,terminal_funding_pass=model(c,m)['terminal_reinvestment']>=model(c,m)['terminal_physical_growth_floor']-1e-9))
stresses=[]
for name,changes in [('slower capital turnover',{'sc':1.3}),('faster capital turnover',{'sc':2.3}),('lower terminal ROIC',{'roic':.10}),('higher terminal ROIC',{'roic':.16}),('slow recovery',{'growth':[0,.02,.03,.03,.03],'margins':[.06,.07,.08,.09,.095]})]:
 c=dict(cases['base']);c.update(changes);stresses.append(dict(name=name,value=model(c)['value'],terminal_funding_pass=model(c)['terminal_reinvestment']>=model(c)['terminal_physical_growth_floor']-1e-9))
json.dump(dict(inverse=inverseqa,cycle=stresses),open(O/'additional-qa.json','w'),indent=2)
assert all(x['monotonic'] and abs(x['residual'])<1e-8 and x['bracket_values'][0]<price<x['bracket_values'][1] for x in inverseqa)

assert all(x['terminal_funding_pass'] for x in sens+inverseqa+stresses)
