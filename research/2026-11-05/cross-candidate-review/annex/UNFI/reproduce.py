"""Frozen research arithmetic plus separately labeled current-price scenarios. No new financial forecast or trade engine."""
import json,math,datetime
from pathlib import Path
P=Path(__file__).parent
PRICE=48.29
OFFSET=(datetime.date(2026,11,4)-datetime.date(2026,8,1)).days/365.25 # no duplicated cash stub
BASIC=60.053154
SHARES=BASIC+2.1 # FY26 treasury-stock equivalent existing dilution proxy; sensitivity to full target awards separately
BRIDGE=1583+13+13+1 # principal debt + finance leases + pension obligation + minority; all cash retained operationally
RF=.049;BETA=1.08;ERP=.0441;SIZE=0.0;KD=.07;DEBTW=.35;TAX=.26
WACC=(RF+BETA*ERP+SIZE)*(1-DEBTW)+KD*(1-TAX)*DEBTW
CASES={
'base':dict(rev1=31500,growth=[.02]*4,margin=[.012,.0125,.013,.0135,.014],wacc=WACC,g=.02,roic=.12,da=.008,capex=300/31500,nwc=.05,terminal_margin=.014),
'bear':dict(rev1=30900,growth=[0,.005,.01,.01],margin=[.010,.010,.0105,.011,.0115],wacc=.105,g=.015,roic=.09,da=.008,capex=.010,nwc=.06,terminal_margin=.0115),
'bull':dict(rev1=31800,growth=[.035,.03,.025,.025],margin=[.0135,.0145,.0155,.016,.0165],wacc=.08,g=.025,roic=.14,da=.008,capex=.0095,nwc=.045,terminal_margin=.0165)}
def model(c, shares=SHARES,bridge=BRIDGE,offset=OFFSET):
 rev=31152; rows=[]
 for t in range(1,11):
  prev=rev
  if t==1:rev=c['rev1'];growth=rev/prev-1
  elif t<=5:growth=c['growth'][t-2];rev*=1+growth
  else:growth=c['growth'][-1]+(c['g']-c['growth'][-1])*(t-5)/5;rev*=1+growth
  margin=c['margin'][t-1] if t<=5 else c['margin'][-1]+(c['terminal_margin']-c['margin'][-1])*(t-5)/5
  ebit=rev*margin;nopat=ebit*(1-TAX);da=rev*c['da'];capex=rev*c['capex'];dWC=(rev-prev)*c['nwc'];explicit=capex-da+dWC
  # Y6-10 blend explicit reinvestment towards paid growth; total reinvestment represented by capex balance, no double deduction
  weight=max(0,(t-5)/5);reinvest=explicit*(1-weight)+nopat*growth/c['roic']*weight
  capex=da+reinvest-dWC
  fcff=nopat-reinvest;pv=fcff/(1+c['wacc'])**(t-offset)
  rows.append(dict(year=2026+t,revenue=rev,growth=growth,margin=margin,ebit=ebit,nopat=nopat,da=da,capex_including_cloud=capex,delta_nwc=dWC,reinvestment=reinvest,fcff=fcff,pv=pv))
 terminal_nopat=rows[-1]['nopat']*(1+c['g']);terminal_reinv=terminal_nopat*c['g']/c['roic'];terminal_fcff=terminal_nopat-terminal_reinv;tv=terminal_fcff/(c['wacc']-c['g']);pvtv=tv/(1+c['wacc'])**(10-offset);ev=sum(r['pv'] for r in rows)+pvtv;eq=ev-bridge
 return dict(price=eq/shares,ev=ev,equity=eq,bridge=bridge,shares=shares,pv_explicit=sum(r['pv'] for r in rows),pv_terminal=pvtv,terminal_weight=pvtv/ev,terminal_fcff=terminal_fcff,terminal_nopat=terminal_nopat,terminal_reinvestment=terminal_reinv,terminal_value=tv,upside=eq/shares/PRICE-1,rows=rows)
def solve(fn,target,lo,hi):
 for _ in range(100):
  m=(lo+hi)/2
  if fn(m)<target:lo=m
  else:hi=m
 return (lo+hi)/2

c=json.loads((P/'current_comparison.json').read_text());a=json.loads((P/'acceleration_scenario.json').read_text());q=json.loads((P/'status.json').read_text());checks=[]
def ck(name,x):
 checks.append((name,bool(x)));assert x,name
for key,case in CASES.items():ck('frozen_'+key,abs(model(case)['price']-c['scenarios'][key]['value'])<1e-8)
for key,z in c['scenarios'].items():ck('return_'+key,abs(z['return_pct']-100*(z['value']/c['quote']['price']-1))<1e-8)
b=CASES['base'];base=model(b)['price'];shift=c['reverse_margin']['parallel_addition'];inverse=model(dict(b,margin=[m+shift for m in b['margin']],terminal_margin=b['terminal_margin']+shift))['price'];ck('reverse_margin',abs(inverse-c['quote']['price'])<1e-8)
gap=300-65+115*(1-TAX)-model(b)['rows'][0]['fcff'];finite=base+sum(gap/(1+WACC)**(t-OFFSET) for t in [1,2])/SHARES;ck('finite_cash',abs(finite-c['scenarios']['limited_two_year_value']['value'])<1e-8)
shield=finite+sum(66*TAX/(1+WACC)**(t-OFFSET) for t in [3,4,5])/SHARES;ck('finite_no_overlap_shield',abs(shield-c['scenarios']['limited_two_year_plus_later_shield_value']['value'])<1e-8)
margin28=(755*1.1-(65+240+35+17+20)*1.02)/32130;accelerated=dict(b,margin=[.012,margin28,.014,.014,.014]);ck('finite_operating_acceleration',abs(model(accelerated)['price']-a['result'])<1e-8);ck('terminal_not_raised',accelerated['terminal_margin']==b['terminal_margin']);ck('no_cash_double_count',a['cash_gap_not_added'])
s=c['finite_cash_bridge_stress'];ck('bridge_100',abs(s['plus100_net_debt_value']-(finite-100/SHARES))<1e-8);ck('awards_only',abs(s['full_target_awards_value']-finite*SHARES/(BASIC+5.814628))<1e-8);ck('bridge_plus_awards',abs(s['plus100_net_debt_and_full_awards_value']-(finite*SHARES-100)/(BASIC+5.814628))<1e-8)
ck('no_entry',not q['entryApproved'] and not q['stage35Approved'] and q['approvedQuantity']==0);ck('no_stop_manufactured',q['M'] is None and q['S'] is None)
print(json.dumps({'passed':True,'checks':len(checks),'scope':'Frozen model replay, current-price comparisons and explicitly separate scenarios. Not trade or account verification.'}))
