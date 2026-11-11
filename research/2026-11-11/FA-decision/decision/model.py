"""Conditional First Advantage ten-year FCFF. USD millions, per share USD.
PPA excluded from normalized EBIT; no perpetual PPA tax benefit.
Current capital is illustrative September + known Nov4 acquisition only.
"""
from pathlib import Path
import json,copy
P=Path(__file__).parent
PRICE=21.58; SHARES=175.435437; DEBT=2019.537+45; CASH=240.902-80; RESERVE=60
RF=.0498;ERP=.0441;BETA=1.14;KD=.075;TAX=.28
E=PRICE*SHARES
WACC=(RF+BETA*ERP)*E/(E+DEBT)+KD*(1-TAX)*DEBT/(E+DEBT)
BASE=dict(initial_revenue=(1732.5-20*2/12)*1.05+20,prior_revenue=1732.5,first_margin=.275,final_margin=.29,growth=.06,g=.025,tax=TAX,da=.03,investment=.05,acquisitions=.01,wc=.08,roic=.13,wacc=WACC,ppa_shield=0)
def run(c):
 prev=c['prior_revenue'];rows=[]
 for y in range(1,11):
  g=c['growth'] if y<=5 else c['growth']+(c['g']-c['growth'])*(y-5)/5
  rev=c['initial_revenue'] if y==1 else prev*(1+g)
  margin=c['first_margin']+(c['final_margin']-c['first_margin'])*min((y-1)/4,1)
  da=rev*c['da'];ebitda=rev*margin;ebit=ebitda-da;tax=ebit*c['tax'];nopat=ebit-tax
  gross=rev*(c['investment']+c['acquisitions']);wc=(rev-prev)*c['wc'];raw_ri=gross+wc-da
  transition=max(0,(y-5)/5);ri=raw_ri*(1-transition)+nopat*g/c['roic']*transition
  shield=c['ppa_shield']*max(0,1-(y-1)/5)
  fcff=nopat-ri+shield
  rows.append(dict(year=y,revenue=rev,ebitda_after_sbc=ebitda,maintenance_da=da,normalized_ebit=ebit,tax=tax,nopat=nopat,gross_investment=gross,delta_wc=wc,raw_net_reinvestment=raw_ri,roic_transition=transition,reinvestment=ri,temporary_tax_shield=shield,fcff=fcff,pv=fcff/(1+c['wacc'])**y));prev=rev
 terminal_nopat=rev*(1+c['g'])*(c['final_margin']-c['da'])*(1-c['tax']);terminal_fcff=terminal_nopat*(1-c['g']/c['roic']);pvterminal=terminal_fcff/(c['wacc']-c['g'])/(1+c['wacc'])**10
 ev=sum(r['pv'] for r in rows)+pvterminal
 return dict(inputs=c,forecast=rows,ev=ev,equity=ev-DEBT+CASH-RESERVE,value=(ev-DEBT+CASH-RESERVE)/SHARES,terminal_fcff=terminal_fcff,pvterminal=pvterminal,terminal_weight=pvterminal/ev)
cases={}
for name,kw in [('bear',dict(initial_revenue=1780,first_margin=.26,final_margin=.27,growth=.03,g=.02,roic=.10,wacc=WACC+.01)),('base',{}),('recovery',dict(initial_revenue=1900,first_margin=.28,final_margin=.31,growth=.08,g=.025,roic=.15)),('bull',dict(initial_revenue=1940,first_margin=.29,final_margin=.32,growth=.10,g=.03,roic=.16,wacc=WACC-.005))]:
 c=BASE|kw;cases[name]=run(c)
grid=[]
for w in [.075,.08,WACC,.09,.10,.105]:
 for m in [.28,.29,.30,.31]:
  grid.append(dict(wacc=w,margin=m,value=run(BASE|dict(wacc=w,final_margin=m))['value']))
sens=[]
for n,kw in [('supplier_elimination_2m_revenue_only_stress',dict(initial_revenue=(1732.5-18*2/12)*1.05+18)),('tax25',dict(tax=.25)),('tax30',dict(tax=.30)),('investment7pct',dict(investment=.07)),('no_future_acquisitions',dict(acquisitions=0)),('terminal_roic10',dict(roic=.10)),('terminal_roic18',dict(roic=.18)),('PPA_shield_assumed50_finite',dict(ppa_shield=50)),('SBC_pressure_50bp',dict(first_margin=.270,final_margin=.285)),('no_interest_tax_shield',dict(wacc=(RF+BETA*ERP)*E/(E+DEBT)+KD*DEBT/(E+DEBT))),('debt_cost6_5pct',dict(wacc=(RF+BETA*ERP)*E/(E+DEBT)+.065*(1-TAX)*DEBT/(E+DEBT)))]:sens.append(dict(test=n,value=run(BASE|kw)['value']))
rev=[]
for w in [WACC,.09,.10,.105]:
 lo,hi=.20,.50
 for _ in range(80):
  mid=(lo+hi)/2
  if run(BASE|dict(wacc=w,final_margin=mid))['value']<PRICE:lo=mid
  else:hi=mid
 rev.append(dict(wacc=w,year5_ebitda_margin=(lo+hi)/2,value=run(BASE|dict(wacc=w,final_margin=(lo+hi)/2))['value']))
r=dict(price=PRICE,price_timestamp='2026-11-10 16:00 EST regular session',balance_scope='September30 plus only disclosed acquisition; not actual November cash',rf=RF,erp=ERP,beta=BETA,kd_assumption=KD,tax=TAX,wacc=WACC,shares=SHARES,debt=DEBT,cash=CASH,operating_cash=RESERVE,cases=cases,grid=grid,sensitivities=sens,reverse=rev,canonical_value=None,entry_approved=False)
(P/'results.json').write_text(json.dumps(r,indent=2));print('WACC',WACC);print({k:round(v['value'],2) for k,v in cases.items()});print(sens);print(rev)
