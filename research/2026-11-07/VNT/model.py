import json
from pathlib import Path
# USD millions except per share. Valuation dated 6Nov2026. First annual period forward12m.
# Forward12m timing avoids adding a full Q4 stub to an annual forecast.
P=42.23
base=dict(revenue=2930,growth=.04,margin=.21,terminal_margin=.215,tax=.25,roic=.20,terminal_roic=.15,wacc=.085,terminal_growth=.025,shares=133.1,cash=218.4,operating_reserve=60,debt=1905.7,notes=99.8,minority_asset=23.4,net_asbestos=34.6,nci=5.6,pension=5,contingent=20.3)
def calc(**kw):
 a=base|kw; rev=a['revenue']; rows=[]; pv=0
 for year in range(1,11):
  f=max(0,year-5)/5; g=a['growth']+(a['terminal_growth']-a['growth'])*f
  rev*=1+g; margin=a['margin']+(a['terminal_margin']-a['margin'])*min(year/5,1)
  nopat=rev*margin*(1-a['tax']); roic=a['roic']+(a['terminal_roic']-a['roic'])*f
  # Total NET reinvestment, including acquired growth, working capital, software and maintenance net of D&A.
  reinvest=nopat*g/roic; fcff=nopat-reinvest; discounted=fcff/(1+a['wacc'])**year;pv+=discounted
  rows.append(dict(year=year,revenue=rev,growth=g,margin=margin,nopat=nopat,incremental_roic=roic,net_reinvestment=reinvest,fcff=fcff,pv=discounted))
 terminal_nopat=rows[-1]['nopat']*(1+a['terminal_growth'])
 terminal_fcff=terminal_nopat*(1-a['terminal_growth']/a['terminal_roic'])
 terminal_pv=terminal_fcff/(a['wacc']-a['terminal_growth'])/(1+a['wacc'])**10
 bridge=a['cash']-a['operating_reserve']+a['notes']+a['minority_asset']-a['debt']-a['net_asbestos']-a['nci']-a['pension']-a['contingent']
 equity=pv+terminal_pv+bridge; value=equity/a['shares']
 return dict(assumptions=a,rows=rows,pv_explicit=pv,pv_terminal=terminal_pv,terminal_ev_weight=terminal_pv/(pv+terminal_pv),equity_bridge=bridge,value=value,discount_to_value=1-P/value)
def inverse(parameter,lo,hi):
 for _ in range(80):
  m=(lo+hi)/2; v=calc(**{parameter:m})['value']
  if (v<P)==(parameter!='wacc'):lo=m
  else:hi=m
 return (lo+hi)/2
out=dict(reference_price=P,scenarios={
 'adverse':calc(growth=.015,margin=.19,terminal_margin=.19,roic=.15,terminal_roic=.12,wacc=.095,terminal_growth=.02,notes=79.84,minority_asset=11.7),
 'central':calc(),
 'favorable':calc(growth=.06,margin=.225,terminal_margin=.235,roic=.25,terminal_roic=.20,wacc=.08,terminal_growth=.025)},
 sensitivity_wacc_growth=[dict(wacc=w,growth=g,value=calc(wacc=w,growth=g)['value']) for w in [.08,.085,.09,.095,.10] for g in [.02,.04,.06]],
 sensitivity_incremental_roic=[dict(roic=r,value=calc(roic=r)['value']) for r in [.15,.20,.25,.40]],
 inverse=dict(growth=inverse('growth',-.01,.15),wacc=inverse('wacc',.05,.15)),
 treasury=.0486,beta=1.12,erp_assumption=.045,marginal_debt_cost_assumption=.0586)
out['calibrated_wacc']=(P*133.1/(P*133.1+1905.7))*(.0486+1.12*.045)+(1905.7/(P*133.1+1905.7))*.0586*.75
Path(__file__).with_name('calculations.json').write_text(json.dumps(out,indent=2))
print({k:round(v['value'],2) for k,v in out['scenarios'].items()});print(out['inverse']); print(out['calibrated_wacc'])
# Exact bridge from stored A288 to forward12m model, isolating timing and model assumptions.
legacy=json.loads(Path(__file__).with_name('legacy_A288.json').read_text())
a=legacy['scenarios']['central']['assumptions']; oldded=legacy['bridge']['net_deduction']
def comparable(wacc=.1,ded=oldded,shares=135.4,flatgrowth=False,newmargin=False,economic_reinvestment=False):
 rev=2930; pv=0
 for i in range(10):
  gs=[.04]*5 if flatgrowth else a['growth'];g=gs[i] if i<5 else gs[-1]+(.025-gs[-1])*(i-4)/5
  m=(.21+.005*min((i+1)/5,1)) if newmargin else a['margin'][min(i,4)]
  prev=rev;rev*=1+g;nopat=rev*m*.75
  if economic_reinvestment:roic=.20+(.15-.20)*max(0,i+1-5)/5;rr=g/roic
  elif i<5:rr=(rev*.005+(rev-prev)*.2)/nopat;rr5=rr
  else:rr=rr5+(.025/.15-rr5)*(i-4)/5
  fcff=nopat*(1-rr);pv+=fcff/(1+wacc)**(i+1)
 tv=nopat*1.025*(1-.025/.15)/(wacc-.025)/(1+wacc)**10
 return (pv+tv-ded)/shares
bridge=[('A288, Oct2 anchor including Q4 stub',legacy['scenarios']['central']['value']),('Forward12m annual timing; no separate Q4 stub',comparable()),('WACC calibrated to 8.5%',comparable(wacc=.085)),('Updated net claims and 133.1m shares',comparable(wacc=.085,ded=1689.6,shares=133.1)),('4% first-five-year growth',comparable(wacc=.085,ded=1689.6,shares=133.1,flatgrowth=True)),('Smooth 21%-21.5% margin ramp',comparable(wacc=.085,ded=1689.6,shares=133.1,flatgrowth=True,newmargin=True)),('Fund all net reinvestment via growth/ROIC',comparable(wacc=.085,ded=1689.6,shares=133.1,flatgrowth=True,newmargin=True,economic_reinvestment=True))]
out['bridge_from_A288']=[dict(step=k,value=v,change=0 if i==0 else v-bridge[i-1][1]) for i,(k,v) in enumerate(bridge)]
assert abs(bridge[-1][1]-out['scenarios']['central']['value'])<1e-8
out['cash_reserve_sensitivity']=[dict(operating_reserve=r,excess_cash=218.4-r,value=calc(operating_reserve=r)['value']) for r in [0,30,60,100,150,218.4]]
out['checks']={'ten_years':len(out['scenarios']['central']['rows'])==10,'terminal_reinvestment':abs(out['scenarios']['central']['rows'][-1]['net_reinvestment']/out['scenarios']['central']['rows'][-1]['nopat']-.025/.15)<1e-9,'bridge_reconciles':True,'scenario_order':out['scenarios']['adverse']['value']<out['scenarios']['central']['value']<out['scenarios']['favorable']['value']}
assert all(out['checks'].values())
Path(__file__).with_name('calculations.json').write_text(json.dumps(out,indent=2))
print(out['bridge_from_A288'])
