import json,pathlib,csv
P=pathlib.Path(__file__).parent;raw=json.loads((P/'mtm_source_rows.json').read_text());years=list(range(2025,2047))
scenarios={'prudente':dict(gold=3200,copper=4.5,mo=22,real_discount=.10,cost_factor=1.20,cap_factor=1.25),'central':dict(gold=4000,copper=5.5,mo=28,real_discount=.08,cost_factor=1.12,cap_factor=1.15),'favorable':dict(gold=4800,copper=6.5,mo=34,real_discount=.065,cost_factor=1.07,cap_factor=1.05)}
def stream_gold(p,y):return 435 if y<2030 else max(435,min(850,.5*p)) if y<2036 else max(435,min(1050,.66*p))
def stream_copper(y):return .15 if y<2030 else .5 if y<2036 else .66
def mtm(s,cutoff=2045):
 rows=[];nav=0
 for i,y in enumerate(years):
  if y<2027:continue
  if y>cutoff and y<2046:continue
  gq=raw['gold_koz'][i]/1000;cq=raw['copper_mlb'][i]
  if y==2046:cf=-103*s['cap_factor'];row=dict(year=cutoff+1,source_closure_bucket=2046,net_cf=cf,discount_time=cutoff-2026+.5,description='Closure 96 plus royalty7 from source; accelerated after cutoff')
  else:
   pg=raw['gold_price'][i];pc=raw['copper_price'][i]
   delta_gold=gq*((.65*s['gold']+.35*stream_gold(s['gold'],y))-(.65*pg+.35*stream_gold(pg,y)))
   delta_copper=cq*(.8125+.1875*stream_copper(y))*(s['copper']-pc)
   delta=delta_gold+delta_copper
   incremental_opex=-(raw['opex'][i]+raw['selling'][i])*(s['cost_factor']-1)
   incremental_cap=-(raw['sustaining'][i]+raw['growth'][i]+raw['leases'][i])*(s['cap_factor']-1)
   # HRS upper-exposure correction: full property coverage, no recovery of already-paid $22.4m.
   stream_value_lost=gq*.35*(s['gold']-stream_gold(s['gold'],y))+cq*.1875*s['copper']*(1-stream_copper(y))
   gross_delta=gq*(s['gold']-pg)+cq*(s['copper']-pc)
   hrs_extra=.02*(max(stream_value_lost,0)+max(gross_delta,0))
   # Incremental FCF royalty highest10%; overlaid conservatively, no tax shield on adverse costs.
   fcf_royalty_extra=.10*max(delta-incremental_opex-incremental_cap-hrs_extra,0)
   extra_tax=.40*max(delta-incremental_opex-hrs_extra-fcf_royalty_extra,0)
   wc=.03*max(delta,0) if y==2027 else 0 # no terminal recovery assigned
   cf=raw['net_cf'][i]+delta-incremental_opex-incremental_cap-hrs_extra-fcf_royalty_extra-extra_tax-wc
   row=dict(year=y,gold_koz=raw['gold_koz'][i],copper_mlb=cq,source_net_cf=raw['net_cf'][i],delta_revenue=delta,incremental_opex=incremental_opex,incremental_capex=incremental_cap,incremental_hrs_upper_exposure=hrs_extra,incremental_fcf_royalty=fcf_royalty_extra,incremental_tax=extra_tax,incremental_wc=wc,net_cf=cf,discount_time=y-2026-.5)
  row['pv']=cf/(1+s['real_discount'])**row['discount_time'];nav+=row['pv'];rows.append(row)
 return dict(project_only_nav=nav,rows=rows,cutoff=cutoff,corporate_equity_value=None)
# Thompson Creek Table22-2; source 2024 constant dollars, updated spending overlay.
tc={'mo_mlb':[4.7,12.4,14.5,14.7,13.7,9.7,7.8,15.9,19.3,12.2,9.1,9.1,2.4], 'netcf':[-65,72,114,127,77,25,-6,146,228,120,91,93,-196], 'opex':[82,162,162,153,157,157,154,150,135,108,82,77,42], 'capex':[70,6,4,4,31,4,4,7,4,3,1,0,0]}
def thompson(s):
 remaining=450-337.3 # latest cap estimate high end minus cumulative restart cap Sept30; funding still required
 rows=[];nav=-remaining*s['cap_factor']
 for i,y in enumerate(range(2027,2040)):
  delta=tc['mo_mlb'][i]*.953*.99*(s['mo']-20) # HPM4.7% held at source price, not repriced as ordinary oxide
  extra_cost=tc['opex'][i]*(s['cost_factor']-1)
  extra_cap=(tc['capex'][i] if i>0 else 0)*(s['cap_factor']-1)
  closure_extra=200*(s['cap_factor']-1) if y==2039 else 0
  extra_tax=.26*max(delta-extra_cost,0)
  cf=tc['netcf'][i]+(70 if i==0 else 0)+delta-extra_cost-extra_cap-extra_tax-closure_extra
  if i==0:cf-=.05*max(tc['mo_mlb'][i]*(s['mo']-20),0)
  pv=cf/(1+s['real_discount'])**(y-2026-.5);nav+=pv
  rows.append(dict(year=y,mo_mlb=tc['mo_mlb'][i],source_net_cf=tc['netcf'][i],incremental_revenue=delta,incremental_cost=extra_cost,incremental_capital=extra_cap,incremental_tax=extra_tax,incremental_closure=closure_extra,net_cf=cf,pv=pv))
 return dict(project_only_nav=nav,restart_remaining_immediate=remaining*s['cap_factor'],rows=rows,corporate_equity_value=None)
out={k:dict(mount_milligan_full=mtm(s),mount_milligan_2035_permission_case=mtm(s,2035),thompson_creek=thompson(s)) for k,s in scenarios.items()}
# Commodity breakevens are project tests, not whole-company inverse valuations.
inverse={}
for name,fn,metal,lo,hi in [('mtm_gold_breakeven',mtm,'gold',500,10000),('tc_mo_breakeven',thompson,'mo',5,80)]:
 for _ in range(100):
  mid=(lo+hi)/2;s=dict(scenarios['central']);s[metal]=mid
  if fn(s)['project_only_nav']<0:lo=mid
  else:hi=mid
 inverse[name]=(lo+hi)/2
result=dict(valuation_date='2027-01-01 conditional project reference, not Nov6 equity value',asof_sources='2026-11-08',units='USD million; explicit finite cash flows, no Gordon terminal',scenarios=scenarios,results=out,inverse=inverse,other_assets={'Oksut':None,'Goldfield':None,'Kemess':None,'Langeloth_standalone':None,'Endako_net_closure':None},combined_enterprise_value=None,total_company_per_share=None,approved_value=None)
(P/'results.json').write_text(json.dumps(result,indent=2))
for k,projects in out.items():
 for n,r in projects.items():
  fields=list(dict.fromkeys(x for row in r['rows'] for x in row))
  with (P/f'{k}_{n}.csv').open('w') as f:
   w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(r['rows'])
print({k:{n:round(v['project_only_nav'],3) for n,v in d.items()} for k,d in out.items()});print(inverse)
