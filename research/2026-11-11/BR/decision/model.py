"""Bounded BR decision update: exact reconstruction of four A186 scenarios.
USD millions, except per-share values. Forecast clock/perimeter preserved; no
new-quarter balance or financing roll is claimed. No trade/entry approval.
"""
from pathlib import Path
import json,copy,hashlib
P=Path(__file__).parent;OLD=json.loads((P.parent/'prior/model_results.json').read_text())
PRICE=192.96;SHARES=OLD['shares'];DEBT=OLD['debt'];E=PRICE*SHARES;RF=.0498;ERP=.0441
NETCLAIMS=OLD['net_claims'];CASH=OLD['cash']-OLD['regulated_cash']-OLD['operating_cash']
def rate(beta=1,erp=ERP,kd=.0625):return (RF+beta*erp)*E/(E+DEBT)+kd*.75*DEBT/(E+DEBT)
def run(c):
 rev=7460.3;rows=[]
 for y in range(1,11):
  growth=c['growth'] if y<=5 else c['growth']+(c['g']-c['growth'])*(y-5)/5
  prev=rev;rev*=1+growth
  margin=c['startmargin']+(c['endmargin']-c['startmargin'])*min((y-1)/4,1)
  ppa=c['ppa_opening']*([.35,.27,.18,.10,.06,.04][y-1] if y<=6 else 0)
  ebit=rev*margin-ppa;da=rev*c['maintenance_da']+ppa
  nopat=ebit*(1-c['tax']);initial=rev*c['investment'];wc=(rev-prev)*c['wc'];raw=initial+wc-da
  weight=max(0,(y-5)/5);ri=raw*(1-weight)+nopat*growth/c['roic']*weight;fcff=nopat-ri
  rows.append(dict(year=y,revenue=rev,growth=growth,margin_before_acquired_amortization=margin,ebit=ebit,acquired_amortization=ppa,da=da,nopat=nopat,initial_cash_investment=initial,delta_wc=wc,raw_net_reinvestment=raw,transition_weight=weight,net_reinvestment=ri,fcff=fcff,pv_fcff=fcff/(1+c['wacc'])**y))
 terminal=rev*(1+c['g'])*c['endmargin']*(1-c['tax'])*(1-c['g']/c['roic']);pvterm=terminal/(c['wacc']-c['g'])/(1+c['wacc'])**10;ev=sum(r['pv_fcff'] for r in rows)+pvterm
 return dict(value=(ev+CASH-NETCLAIMS)/SHARES,ev=ev,terminal_fcff=terminal,terminal_pv_share=pvterm/ev,inputs=c,forecast=rows)
checks={}
for name in ['bear','base','recovery','bull']:
 old=OLD['cases'][name];new=run(old['inputs'].copy())
 for key in ['value','ev','terminal_fcff','terminal_pv_share']:checks[f'{name}.{key}']=abs(old[key]-new[key])<1e-7
 for i,(a,b) in enumerate(zip(old['forecast'],new['forecast'])):
  for key,val in a.items():checks[f'{name}.year{i+1}.{key}']=abs(val-b[key])<1e-7
assert all(checks.values()),[k for k,v in checks.items() if not v]
cases={}
for label,beta in [('observed_beta',.9),('normalized_beta',1)]:
 for name in ['base','recovery']:
  c=OLD['cases'][name]['inputs'].copy();c['wacc']=rate(beta);cases[label+'_'+name]=run(c)
def reverse(margin,beta):
 c=OLD['cases']['base']['inputs'].copy();c.update(endmargin=margin,wacc=rate(beta));lo,hi=0,.2
 for _ in range(80):
  mid=(lo+hi)/2;c['growth']=mid
  if run(c)['value']<PRICE:lo=mid
  else:hi=mid
 c['growth']=(lo+hi)/2
 return dict(beta=beta,wacc=c['wacc'],margin=margin,growth=c['growth'],value=run(c)['value'])
grid=[]
for beta in [.9,1]:
 for growth in [.05,.06,.065,.07]:
  for margin in [.22,.23,.24]:
   c=OLD['cases']['base']['inputs'].copy();c.update(growth=growth,endmargin=margin,wacc=rate(beta));grid.append(dict(beta=beta,growth=growth,margin=margin,value=run(c)['value']))
sens=[]
for beta in [.9,1]:
 for name in ['base','recovery']:
  for label,kw in [('extra_investment_1pct',{'investment':.0265}),('terminal_roic15',{'roic':.15}),('constant_market_return_erp',{'wacc':rate(beta,erp=.0494+.0441-RF)})]:
   c=OLD['cases'][name]['inputs'].copy();c['wacc']=rate(beta);c.update(kw);sens.append(dict(case=name,beta=beta,test=label,value=run(c)['value']))
R=dict(as_of='2026-11-11 premarket; Nov10 regular-close reference',price=PRICE,close_time='2026-11-10 16:00 EST',forecast_and_balance_scope='A186 September2026 perimeter; unchanged forecast clock, not a fresh cash/debt roll',inputs=dict(rf=RF,erp=ERP,beta_observed=.9,beta_normalized=1,kd_assumption=.0625,shares=SHARES,debt=DEBT,net_claims=NETCLAIMS,cash_credit=CASH),canonical_value=None,entry_approved=False,new_quantity=0,reproduction_checks=checks,cases=cases,reverse=[reverse(m,b) for b in [.9,1] for m in [.22,.23,.24]],grid=grid,sensitivities=sens,source_prior_model_sha256=hashlib.sha256((P.parent/'prior/model_results.json').read_bytes()).hexdigest())
(P/'results.json').write_text(json.dumps(R,indent=2));print('Reproduction',len(checks),'passed');print({k:round(v['value'],2) for k,v in cases.items()});print(R['reverse'])
