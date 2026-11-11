"""Conditional HRB 10-year EBIT/FCFF model. USD millions except shares and price.
Annual seasonal business: no Q1 annualization, no recurring IRS settlement gain.
"""
from pathlib import Path
import json
P=Path(__file__).parent
PRICE=50.99;SHARES=124.5;DEBT=1500;CASH=390.498;RF=.0498;ERP=.0441;KD=.065;E=PRICE*SHARES
rate=lambda beta:(RF+beta*ERP)*E/(E+DEBT)+KD*.75*DEBT/(E+DEBT)
BASE=dict(startrev=3966.177,year1rev=4135,growth=.035,startmargin=.225,endmargin=.23,wacc=rate(1),g=.02,tax=.25,da=.031,capex=.025,acq=.014,wc=.10,roic=.15,cash_credit=0,otherclaims=29.8)
def run(c):
 rev=c['startrev'];rows=[]
 for y in range(1,11):
  prev=rev;growth=c['growth'] if y<=5 else c['growth']+(c['g']-c['growth'])*(y-5)/5;rev=c['year1rev'] if y==1 else prev*(1+growth)
  margin=c['startmargin']+(c['endmargin']-c['startmargin'])*min((y-1)/4,1);ebit=rev*margin;nopat=ebit*(1-c['tax']);da=rev*c['da'];gross=rev*(c['capex']+c['acq']);wc=(rev-prev)*c['wc'];raw=gross+wc-da;fade=max(0,(y-5)/5);ri=raw*(1-fade)+nopat*growth/c['roic']*fade;fcff=nopat-ri
  rows.append(dict(year=y,revenue=rev,ebit=ebit,nopat=nopat,da=da,gross_investment=gross,delta_wc=wc,raw_reinvestment=raw,fade=fade,reinvestment=ri,fcff=fcff,pv=fcff/(1+c['wacc'])**y))
 tf=rev*(1+c['g'])*c['endmargin']*(1-c['tax'])*(1-c['g']/c['roic']);tpv=tf/(c['wacc']-c['g'])/(1+c['wacc'])**10;ev=sum(x['pv'] for x in rows)+tpv;eq=ev-DEBT+c['cash_credit']-c['otherclaims'];return dict(inputs=c,forecast=rows,ev=ev,equity=eq,value=eq/SHARES,terminal_fcff=tf,terminal_pv=tpv,terminal_share=tpv/ev)
cases={}
for k,d in [('observed_beta_diagnostic',dict(wacc=rate(.41))),('normalized_beta_base',{}),('return_hurdle10',dict(wacc=.10)),('moderate_stress',dict(year1rev=4050,growth=.02,startmargin=.215,endmargin=.21,wacc=.10,g=.015,roic=.12)),('bear',dict(year1rev=3966.177,growth=0,startmargin=.20,endmargin=.19,wacc=.115,g=.01,roic=.10)),('recovery',dict(year1rev=4160,growth=.045,startmargin=.235,endmargin=.24,wacc=rate(1),g=.025,roic=.17))]:cases[k]=run(BASE|d)
sens=[]
for k,d in [('tax23',dict(tax=.23)),('capex3_5',dict(capex=.035)),('acquisitions2',dict(acq=.02)),('no_claims_deduction',dict(otherclaims=0)),('cash_credit200',dict(cash_credit=200)),('terminal_roic10',dict(roic=.10)),('margin21',dict(startmargin=.21,endmargin=.21))]:sens.append(dict(test=k,value=run(BASE|d)['value']))
reverse=[]
for w in [rate(1),.09,.10,.11]:
 lo,hi=.10,.35
 for _ in range(80):
  mid=(lo+hi)/2
  if run(BASE|dict(wacc=w,startmargin=mid,endmargin=mid))['value']<PRICE:lo=mid
  else:hi=mid
 reverse.append(dict(wacc=w,constant_margin=(lo+hi)/2,value=run(BASE|dict(wacc=w,startmargin=(lo+hi)/2,endmargin=(lo+hi)/2))['value']))
r=dict(price=PRICE,price_timestamp='2026-11-10 16:00 EST regular',shares=SHARES,debt=DEBT,cash=CASH,cash_credit=0,rf=RF,erp=ERP,kd_assumption=KD,beta_observed=.41,beta_normalized_assumption=1,wacc_observed=rate(.41),wacc_normalized=rate(1),cases=cases,sensitivities=sens,reverse=reverse,canonical_value=None,entry_approved=False)
(P/'results.json').write_text(json.dumps(r,indent=2));print({k:round(v['value'],2) for k,v in cases.items()});print(sens);print(reverse)
