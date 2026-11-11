"""Standalone FCFE audit. Production code not imported or executed."""
import json,math
from pathlib import Path
B=Path(__file__).resolve().parents[1];o=json.loads((B/'results.json').read_text());count=0
D=dict(growth=.03,margin0=.14,margin5=.145,credit=.02,ke=.115,g=.025,roe=.2,shares=858,permanent_credit=False,extra_cash=0)
def check(a,b):
 global count
 assert math.isclose(a,b,rel_tol=1e-10,abs_tol=1e-7),(a,b)
 count+=1
def calc(over):
 p=D|over; rev=34295;rows=[];pv=0
 for n in range(1,11):
  f=0 if n<6 else (n-5)/5
  growth=p['growth']*(1-f)+p['g']*f
  prior=rev;rev=prior*(1+growth)
  m=p['margin0']+(p['margin5']-p['margin0'])*min(n,5)/5
  ni=rev*m; wc=(rev-prior)*.05
  explicit=rev*(.005+p['credit'])+wc
  target=ni*p['g']/p['roe']
  investment=explicit if p['permanent_credit'] else explicit*(1-f)+target*f
  cash=ni-investment;v=cash/(1+p['ke'])**n;pv+=v
  rows.append(dict(revenue=rev,growth=growth,net_margin=m,net_income=ni,da=rev*.025,capex=rev*.025,acquisitions=rev*.005,credit_funding=rev*p['credit'],nwc=wc,explicit_reinvestment=explicit,roe_reinvestment=target,blended_reinvestment=investment,fcfe=cash,pv=v))
 terminal=rows[-1]['fcfe']*(1+p['g']);tv=terminal/(p['ke']-p['g'])/(1+p['ke'])**10
 eq=pv+tv+p['extra_cash']
 return dict(rows=rows,terminal_fcfe=terminal,terminal_pv=tv,equity=eq,value=eq/p['shares'],terminal_fraction=tv/eq)
check(.0498+1.32*.0441,o['rates']['observed']);check(.0498+.0441,o['rates']['normalized'])
for group in ['cases','sensitivity']:
 for name,item in o[group].items():
  out=calc(item['assumptions'])
  for i,row in enumerate(out['rows']):
   for key,num in row.items():check(num,item['rows'][i][key])
  for key in ['terminal_fcfe','terminal_pv','equity','value','terminal_fraction']:check(out[key],item[key])
roots={};intervals=0
for name,kw in [('legacy_rate',{}),('observed_rate',{'ke':.0498+1.32*.0441}),('permanent_funding',{'permanent_credit':True})]:
 lo=-.02;hi=.15
 assert calc(kw|{'growth':lo})['value']<58.78<calc(kw|{'growth':hi})['value']
 grid=[calc(kw|{'growth':lo+(hi-lo)*i/1000})['value'] for i in range(1001)]
 assert all(b>a for a,b in zip(grid,grid[1:]));intervals+=1000
 for _ in range(100):
  mid=(lo+hi)/2
  if calc(kw|{'growth':mid})['value']>58.78:hi=mid
  else:lo=mid
 roots[name]=(lo+hi)/2;check(roots[name],o['price_implied_growth'][name]['growth']);check(calc(kw|{'growth':roots[name]})['value'],58.78)
summary=dict(status='PASS',numeric_comparisons=count,cases=8,sensitivities=12,growth_roots=roots,monotonic_intervals=intervals,values={k:calc(v['assumptions'])['value'] for k,v in o['cases'].items()},legacy_deviations={k:calc(o['cases'][case]['assumptions'])['value']-o['legacy_reference'][k] for k,case in [('base','reconstructed_base'),('adverse','adverse'),('recovery','recovery')]})
(B/'audit/output.json').write_text(json.dumps(summary,indent=2));print(json.dumps(summary,indent=2))
