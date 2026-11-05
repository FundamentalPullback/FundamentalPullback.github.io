import json,csv,copy,math
from pathlib import Path
P=Path(__file__).parent
# Controlled 10-year FCFF supporting calculation, not approved valuation.
# First five years explicit; years 6-10 linearly fade growth to g and reinvestment/NOPAT to g/ROIC.
def model(growth=(.11,.105,.10,.09,.08), margins=(.28,.29,.30,.31,.32),wacc=.09,g=.025,roic=.20,rev0=1640,tax=.21,da=.04,capex=.05,nwc=-.10,bridge=1180.846,shares=311.0,margin_shift=0,growth_shift=0):
 rev=rev0; rows=[]
 for t in range(1,11):
  a=max(0,(t-5)/5)
  growth_t=(growth[t-1]+growth_shift) if t<=5 else (growth[-1]+growth_shift)*(1-a)+g*a
  margin_t=(margins[t-1]+margin_shift) if t<=5 else margins[-1]+margin_shift
  prev=rev;rev*=1+growth_t;ebit=rev*margin_t;nopat=ebit*(1-tax)
  da_t=rev*da;capex_t=rev*capex;d_nwc=(rev-prev)*nwc
  if t<=5:
   ri=capex_t-da_t+d_nwc;rate=ri/nopat
   if t==5:r5=rate
  else:
   rate=r5*(1-a)+(g/roic)*a;ri=nopat*rate
  # Preserve V1 economics; expose the transition funding needed to reach terminal g/ROIC.
  reference_reinvestment=capex_t-da_t+d_nwc
  transition_reinvestment_adjustment=ri-reference_reinvestment
  effective_capex=ri+da_t-d_nwc
  fcff=nopat-ri; pv=fcff/(1+wacc)**t
  rows.append(dict(year=f'Y{t} to {2026+t}-11-05',t=t,revenue=rev,growth=growth_t,ebit_margin=margin_t,ebit=ebit,nopat=nopat,da=da_t,capex=capex_t,delta_nwc=d_nwc,reinvestment=ri,reinvestment_rate=rate,transition_reinvestment_adjustment=transition_reinvestment_adjustment,effective_capex=effective_capex,effective_capex_to_revenue=effective_capex/rev,fcff=fcff,pv=pv))
 terminal_nopat=rows[-1]['nopat']*(1+g);tv=terminal_nopat*(1-g/roic)/(wacc-g);pvt=tv/(1+wacc)**10
 ev=sum(r['pv'] for r in rows)+pvt;price=(ev-bridge)/shares
 return dict(price=price,ev=ev,equity=ev-bridge,bridge=bridge,shares=shares,terminal_weight=pvt/ev,wacc=wacc,g=g,roic=roic,rows=rows)
CASES={
 'adverso':dict(growth=(.07,.065,.06,.055,.05),margins=(.26,.265,.27,.275,.28),wacc=.10,g=.02,roic=.18),
 'central':{},
 'favorable':dict(growth=(.14,.13,.12,.11,.10),margins=(.30,.32,.34,.35,.36),wacc=.08,g=.03,roic=.25)
}
results={k:model(**v) for k,v in CASES.items()}
# Use TTM GAAP - deferred mark-to-market normalization only; do not remove SBC or intangibles.
# Bridge: gross debt 1165, minus excess cash 100.874 (50 reserve), plus DCP 116.672,
# minority .048, subtract no investments; no lease duplication. Cohesive cash excluded already.
# This is pre-Eliis and pre-Naviam values. Exact proforma bridge remains pending.
price=47.09
sensitivity=[]
for w in [.08,.085,.09,.095,.10]:
 for g in [.02,.025,.03]:
  r=model(wacc=w,g=g);sensitivity.append(dict(wacc=w,g=g,price=r['price']))
def root(fn):
 lo,hi=-.05,.5
 for _ in range(100):
  m=(lo+hi)/2
  if fn(m)<price:lo=m
  else:hi=m
 return (lo+hi)/2
revshift=root(lambda x:model(growth_shift=x)['price'])
mshift=root(lambda x:model(margin_shift=x)['price'])
output=dict(as_of='2026-11-05T16:14:40Z',spot=price,scenario=results,sensitivity=sensitivity,reverse_margin_shift=mshift,reverse_final_margin=.32+mshift,reverse_growth_shift=revshift,reverse_y1_growth=.11+revshift,reverse_y5_growth=.08+revshift,reinves_sensitivity=[{'capex':c,'price':model(capex=c)['price']} for c in [.03,.04,.05,.06,.07]],net_transaction_sensitivity_per_100m=100/311,version='BSY-POST-20261105-v2',model_type='partial_counterfactual_calculation',status='screen-grade; not full issuer valuation',output_scope='All price/equity/EV fields and reverse solves are partial counterfactual outputs excluding Eliis contribution and cost, Naviam, existing investments and financing hedge; they are not BSY fair value or market downside.',field_definitions={'price':'Legacy machine field: partial counterfactual output per share, not issuer fair value.', 'capex':'5% of sales investment reference: actual assumption for years 1-5; reference only for years 6-10.', 'transition_reinvestment_adjustment':'Economic reinvestment minus (reference capex minus D&A plus delta NWC); zero for years 1-5.', 'effective_capex':'Economic reinvestment plus D&A minus delta NWC; actual funding implied by transition.', 'reverse':'Partial counterfactual calibration to observed quote; excludes missing business and asset components.'},warnings=['Eliis purchase consideration and balance sheet after October transactions not disclosed in reviewed primary packet.','Naviam interest/warrants value unavailable; excluded, not valued at zero permanently.','2026 normalized starting sales are counterfactual ex-Cohesive, ex-Eliis analyst proxy, not guidance.','WACC is an analyst hurdle assumption, not observed cost of capital.','No homogeneous peer valuation set completed.','Existing investments of USD42.265m and financing hedge value are excluded pending classification, value and tax review; not permanently assumed worthless.','USD550m term loan has conditional maturity 91 days before outstanding convertible debt unless liquidity tests are met; approximately April1 2027 for July1 2027 notes.','311m shares use cash settlement of converts; Q3 award split requires Q3 10-Q.'])
(P/'model_results.json').write_text(json.dumps(output,indent=2))
for k,r in results.items():
 with (P/f'fcff_{k}.csv').open('w') as f:
  w=csv.DictWriter(f,fieldnames=r['rows'][0]);w.writeheader();w.writerows(r['rows'])
print(json.dumps({k:{a:v for a,v in r.items() if a!='rows'} for k,r in results.items()},indent=2))
print('Reverse margins',output['reverse_final_margin'],'reverse growth',output['reverse_y1_growth'],output['reverse_y5_growth'])
print('Sens',sensitivity)
