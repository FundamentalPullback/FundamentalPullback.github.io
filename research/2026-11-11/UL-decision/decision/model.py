"""UL conditional forward deal-package SOTP, not execution approval.
EURbn HPC, USDbn Foods, sharesbn. One timeline; no guaranteed closing.
"""
from pathlib import Path
import json,copy,datetime
P=Path(__file__).parent
L=json.loads((P/'legacy_inputs.json').read_text())
fx=1.1214;shares=L['shares'];price=66.47
# Proposed June30 close, calendar-days from Nov10; analytical date, not approved transaction.
delay=(datetime.date(2027,6,30)-datetime.date(2026,11,10)).days/365

def op(p):
 sales=p['revenue'];rows=[]
 for y in range(1,11):
  growth=p['growth'] if y<=5 else p['growth']+(p['growth10']-p['growth'])*(y-5)/5
  prior=sales;sales*=1+growth; margin=p['margin0']+(p['margin5']-p['margin0'])*min(y,p.get('margin_year',5))/p.get('margin_year',5)
  restruct=0 if p.get('restruct_reserved') and y<=3 else p['restruct']
  nopat=sales*(margin-restruct)*(1-p['tax'])+p.get('synergy',0)*min(y/3,1)*(1-p['tax'])
  capex=p['capex'];lease=p['lease_capex']
  inv=sales*(capex+lease-p['da'])+(sales-prior)*p['nwc'];fade=max(0,(y-5)/5)
  inv=inv*(1-fade)+nopat*growth/p['terminal_roic']*fade
  extra=p.get('extra_costs',{}).get(str(y),0);fcff=nopat-inv-extra
  rows.append(dict(year_after_close=y,revenue=sales,margin=margin,restruct_rate=restruct,nopat=nopat,reinvestment=inv,extra=extra,fcff=fcff))
 pv=sum(q['fcff']/(1+p['wacc'])**q['year_after_close'] for q in rows)
 tv=rows[-1]['nopat']*(1+p['tg'])*(1-p['tg']/p['terminal_roic'])/(p['wacc']-p['tg'])/(1+p['wacc'])**10
 return dict(ev=pv+tv,terminal_share=tv/(pv+tv),rows=rows)

h=dict(L['deal']['hpc']['inputs'],margin0=.191,capex=.036,restruct_reserved=True,extra_costs={})
f=dict(L['deal']['foods']['inputs'])
base=dict(hpc=h,foods=f,fx=fx,cost=5,delay=delay,claims=L['operating_claims'],assets=L['nonoperating_assets']-(.121534*19.39/1.1179)+(.121533558*19.89/fx),shares=shares,pre=L['direct']['base']['inputs'])
def run(c):
 h,f=op(c['hpc']),op(c['foods']);w=c['hpc']['wacc'];fw=c['foods']['wacc'];d=c['delay'];x=c['fx']
 pre=op(c['pre'])['rows'][0]['fcff']*d/(1+w)**(d/2)
 costpv=c['cost']*sum(weight/(1+w)**(d+t) for t,weight in [(0,.5),(1,.3),(2,.2)])
 hopv=h['ev']/(1+w)**d;cash=15.7/x/(1+w)**d
 feq=f['ev']-4.6871-15.7-.75;foodpv=.65*feq/x/(1+fw)**d
 assets=c['assets']-(.121533558*19.89/fx)+(.121533558*19.89/x)
 eq=pre+hopv+cash+foodpv-c['claims']+assets-costpv
 return dict(value_usd=eq/c['shares']*x,preclose_fcff_pv_eur=pre,hpc_ev_pv_eur=hopv,deal_cash_pv_eur=cash,food_equity_pv_eur=foodpv,cost_pv_eur=costpv,claims=c['claims'],assets=assets,hpc=h,foods=f)
cases={'central':base,'lease_included':dict(base,hpc=dict(h,lease_capex=0)),'all_restruct_additional':dict(base,hpc=dict(h,restruct_reserved=False,extra_costs={'1':.45,'2':.3,'3':.15})),'adverse':dict(base,fx=1.05,cost=6,hpc=dict(h,growth=.025,growth10=.02,margin5=.19,wacc=.085,tg=.02,terminal_roic=.17),foods=dict(f,growth=.015,growth10=.02,synergy=.3,wacc=.095,tg=.02,terminal_roic=.13)),'recovery':dict(base,hpc=dict(h,growth=.06,margin5=.225,margin_year=10),foods=dict(f,growth=.04,synergy=.6))}
sens={}
sens['sales_roll_to_assumed_close']=run(dict(base,hpc=dict(h,revenue=h['revenue']*(1+h['growth'])**delay),foods=dict(f,revenue=f['revenue']*(1+f['growth'])**delay)))['value_usd']
for w in [.07,.08,.085]:sens['hpc_wacc_'+str(w)]=run(dict(base,hpc=dict(h,wacc=w)))['value_usd']
for fxv in [1.05,1.18]:sens['fx_'+str(fxv)]=run(dict(base,fx=fxv))['value_usd']
for claims in [-3,3]:sens['claims_delta_'+str(claims)]=run(dict(base,claims=base['claims']+claims))['value_usd']
for cost in [4,6]:sens['cost_'+str(cost)]=run(dict(base,cost=cost))['value_usd']
for margin in [.22,.225,.23]:sens['margin_year10_'+str(margin)]=run(dict(base,hpc=dict(h,margin5=margin,margin_year=10)))['value_usd']
lo,hi=.15,.35
for _ in range(100):
 mid=(lo+hi)/2
 if run(dict(base,hpc=dict(h,margin5=mid,margin_year=10)))['value_usd']<price:lo=mid
 else:hi=mid
out=dict(asof='2026-11-11',price=price,price_date='2026-11-10',fx_ecb_reference=fx,delay_years_assumption=delay,cases={k:dict(assumptions=c,result=run(c)) for k,c in cases.items()},sensitivity=sens,reverse_margin_year10=(lo+hi)/2,limitations=['Deal pending; closingdateassumptionnotfact','CashbridgeJunehistoricalnotcurrentbrokerbalance','Leaseinclusionandcostoverlapmodeledasbounds','NCI/JVvalueshistoricalconditionalestimates','Noacquisitiongrowthorfreebuybacks; futureM&AassumedzeroNPV'])
(P/'results.json').write_text(json.dumps(out,indent=2));print(json.dumps({'cases':{k:v['result']['value_usd'] for k,v in out['cases'].items()},'sensitivity':sens,'reverse':out['reverse_margin_year10']},indent=2))
