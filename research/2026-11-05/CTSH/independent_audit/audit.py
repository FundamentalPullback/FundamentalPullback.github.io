"""Independent CTSH audit. Does not import author code or mutate author files."""
import json,csv,math,hashlib,statistics,datetime,sys
from pathlib import Path
O=Path(__file__).parent; P=Path(sys.argv[1]) if len(sys.argv)>1 else O/'model_snapshot'
I=json.loads((P/'model/inputs.json').read_text()); published=json.loads((P/'results.json').read_text())

def beta_fit(x,y):
 mx=statistics.mean(x); my=statistics.mean(y); xx=sum((v-mx)**2 for v in x); xy=sum((a-mx)*(b-my) for a,b in zip(x,y)); yy=sum((v-my)**2 for v in y)
 slope=xy/xx; residual=sum((b-my-slope*(a-mx))**2 for a,b in zip(x,y));se=math.sqrt(residual/(len(x)-2)/xx)
 return dict(n=len(x),beta=slope,standard_error=se,r_squared=xy*xy/xx/yy,intercept=my-slope*mx)
D={}
for ticker in ['CTSH','SPY']:
 j=json.loads((P/'sources'/f'{ticker}_monthly.json').read_text())['chart']['result'][0]
 D[ticker]={datetime.datetime.fromtimestamp(t,datetime.timezone.utc).strftime('%Y-%m'):p for t,p in zip(j['timestamp'],j['indicators']['adjclose'][0]['adjclose']) if p is not None and datetime.datetime.fromtimestamp(t,datetime.timezone.utc).strftime('%Y-%m')<'2026-11'}
months=sorted(D['CTSH'].keys()&D['SPY'].keys());ret={k:[D[k][b]/D[k][a]-1 for a,b in zip(months,months[1:])] for k in D}
B=beta_fit(ret['SPY'],ret['CTSH']); B['first_month']=months[1];B['last_month']=months[-1]
B['subsamples']={f'last_{n}':beta_fit(ret['SPY'][-n:],ret['CTSH'][-n:]) for n in [24,36,48]}
B['normalized']=(2*B['beta']+1)/3
shares=I['shares_actual_oct23']+I['incremental_dilution'];dw=I['debt']/(I['price']*shares+I['debt'])
def cost_capital(beta=B['normalized'],rf=I['risk_free'],erp=I['erp']):return (1-dw)*(rf+beta*erp)+dw*I['cost_debt']*(1-I['capital_tax'])
wacc=cost_capital()

def rebuild(case='base',changes=None,owned=False,acq_midyear=True,operating_midyear=False,bridge=None,stub_spread=False):
 c=dict(I['cases'][case]);c.update(changes or {});b=dict(I);b.update(bridge or {})
 w=c.get('wacc',wacc+c['wacc_spread']);g=c['terminal_g'];tau=I['stub_days']/I['stub_year_days'];rows=[];cohorts=[];prior=I['base_revenue'];netpvs=0
 for yr in range(1,11):
  if yr<6:
   original=I['base_revenue']*(1+c['organic_growth'])**yr
   inherited=I['base_revenue']*c['inherited_growth_2027']*(1+c['organic_growth'])**(yr-1)
   dyflex_run=I['dyflex_cash']/c['acquisition_multiple'] if yr==1 else 0
   purchase=dyflex_run if owned else prior*c['new_acquired_runrate']
   other_run=max(0,purchase-dyflex_run);recognized=other_run*c['recognition_fraction']+dyflex_run*I['dyflex_first_year_recognition']
   cohorts.append((other_run+dyflex_run,recognized))
   bought=sum(rec if j==yr-1 else q*(1+c['organic_growth'])**(yr-1-j) for j,(q,rec) in enumerate(cohorts))
   rev=original+inherited+bought;growth=rev/prior-1
   da=rev*I['owned_ppe_depreciation_pct']+I['owned_intangible_amortization'][yr-1]+I['dyflex_cash']*I['dyflex_new_intangibles_share']/I['dyflex_intangible_life']*(I['dyflex_first_year_recognition'] if yr==1 else 1) if owned else rev*c['da_pct']
   ebit=rev*(c['margins'][yr-1]+c['da_pct'])-da if owned else rev*c['margins'][yr-1]
   investment=rev*(c['capex_pct']+c['contract_capitalization'])+prior*c['organic_growth']*c['nwc_incremental']-da
   if yr==1:investment+=c['dso_cash_stress_2027']
   acq=other_run*c['acquisition_multiple']+(I['dyflex_cash'] if yr==1 else 0);investment+=acq
   if yr==5:g5=growth; ir5=investment/rev; m5=ebit/rev
  else:
   progress=(yr-5)/5;growth=(1-progress)*g5+progress*g;rev=prior*(1+growth);ebit=rev*((1-progress)*m5+progress*c['terminal_margin'])
   investment=(1-progress)*rev*ir5+progress*ebit*(1-c['tax'])*g/c['terminal_roic'];acq=0
  cf=ebit*(1-c['tax'])-investment;t=yr+tau
  # Distinguish acquisition settlement from the usual conservative year-end operating convention.
  operating_time=t-.5 if operating_midyear else t
  dy_cash=I['dyflex_cash'] if yr==1 else 0
  other_cash=acq-dy_cash
  pv_acq=dy_cash/(1+w)**(t-I['dyflex_first_year_recognition'] if acq_midyear else t)+other_cash/(1+w)**(t-c['recognition_fraction'] if acq_midyear else t)
  pvcf=(cf+acq)/(1+w)**operating_time-pv_acq
  rows.append(dict(year=2026+yr,revenue=rev,growth=growth,ebit=ebit,net_reinvestment=investment,acquisition_cash=acq,fcff=cf,pv_fcff=pvcf,time=t));netpvs+=pvcf;prior=rev
 terminal_cf=prior*(1+g)*c['terminal_margin']*(1-c['tax'])*(1-g/c['terminal_roic']);pvt=terminal_cf/(w-g)/(1+w)**(10+tau)
 stub=c['stub_issuer_fcf']-I['stub_sbc']+I['stub_net_interest_expense']*(1-c['tax'])
 pvstub=stub/(1+w)**tau
 if stub_spread:
  # Simple 35/92 accrued cash at November 4 plus remaining 57/92, latter at midpoint.
  pvstub=stub*(35/92+57/92/(1+w)**(tau/2))
 ev=netpvs+pvt+pvstub
 claims=b['debt']+b['pension_deficit']+b['contingent_consideration']+b['post_september_buyback_cash'];excess=b['cash']+b['short_investments']-b['operating_cash'];ss=b['shares_actual_oct23']+b['incremental_dilution'];price=(ev+excess-claims)/ss
 return dict(value=price,ev=ev,equity=ev+excess-claims,pv_explicit=netpvs,pv_terminal=pvt,pv_stub=pvstub,wacc=w,rows=rows)

def root(fn,lo,hi):
 assert fn(lo)*fn(hi)<0
 for _ in range(90):
  m=(lo+hi)/2
  if fn(lo)*fn(m)<0:hi=m
  else:lo=m
 return (lo+hi)/2

out={'timestamp_utc':'2026-11-05','audit_scope':'Independent rebuild, timing/economic challenges, no author-code import','beta':B,'wacc':wacc,'checks':[]}
for case in ['base','bear','bull','owned_business_crosscheck']:
 a=rebuild(owned=True) if case=='owned_business_crosscheck' else rebuild(case)
 p=published[case];out[case]=a
 for field,auth in [('value','per_share'),('ev','enterprise_value'),('equity','equity_value'),('pv_explicit','pv_explicit'),('pv_terminal','pv_terminal'),('pv_stub','pv_stub')]:
  diff=a[field]-p[auth];out['checks'].append(dict(check=case+'_'+field,difference=diff,pass_check=abs(diff)<1e-7))
 for row,pr in zip(a['rows'],p['rows']):
  for k in ['revenue','growth','ebit','net_reinvestment','fcff','pv_fcff']:
   diff=row[k]-pr[k];out['checks'].append(dict(check=f'{case}_{row["year"]}_{k}',difference=diff,pass_check=abs(diff)<1e-7))
old_owned=rebuild(owned=True);out['owned_revised']=old_owned
moderate=dict(organic_growth=.02,margins=[m-.005 for m in I['cases']['base']['margins']],terminal_margin=.155,acquisition_multiple=3.5,tax=.27,capex_pct=.018)
scenarios={}
for k,w in [('fitted',wacc),('nine_pct',.09),('beta_one',cost_capital(beta=1)),('nine_half_pct',.095),('ten_pct',.10),('damodaran_rf_same_month',cost_capital(rf=.0529))]:
 scenarios[k]={'wacc':w,'base':rebuild(changes={'wacc':w})['value'],'moderate':rebuild(changes={**moderate,'wacc':w})['value'],'moderate_plus_dso':rebuild(changes={**moderate,'wacc':w,'dso_cash_stress_2027':308})['value'],'moderate_plus_dso_year_end_acq_comparison':rebuild(changes={**moderate,'wacc':w,'dso_cash_stress_2027':308},acq_midyear=False)['value']}
out['combined_scenarios']=scenarios
out['timing']={k:rebuild(**v)['value'] for k,v in {'revised_acquisition_settlement':{},'year_end_acquisition_comparison':{'acq_midyear':False},'all_explicit_cash_midyear':{'acq_midyear':True,'operating_midyear':True},'stub_separate_accrued_and_future':{'stub_spread':True}}.items()}
out['reverse_wacc_base']=root(lambda w:rebuild(changes={'wacc':w})['value']-I['price'],.03,.2)
out['reverse_wacc_moderate']=root(lambda w:rebuild(changes={**moderate,'wacc':w})['value']-I['price'],.03,.2)
out['reverse_wacc_moderate_dso']=root(lambda w:rebuild(changes={**moderate,'wacc':w,'dso_cash_stress_2027':308})['value']-I['price'],.03,.2)
out['dyflex_committed_cash_only_haircut']=210/(1+wacc)**(.15616438356+.25)/shares
out['dyflex_committed_cash_note']='Haircut is informational, already included in revised owned-business cash flow; do not deduct again.'
out['snapshot_hashes']={str(p.relative_to(P)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [P/'value.py',P/'model/inputs.json',P/'results.json',P/'beta_estimate.json',P/'source_review/source_review.md']}
out['all_numerical_checks_pass']=all(x['pass_check'] for x in out['checks']);out['numerical_check_count']=len(out['checks'])
(O/'independent_results.json').write_text(json.dumps(out,indent=2))
with (O/'independent_forecast_rows.csv').open('w') as f:
 writer=csv.DictWriter(f,fieldnames=['scenario']+list(out['base']['rows'][0]));writer.writeheader()
 for name in ['base','bear','bull']:
  for row in out[name]['rows']:writer.writerow({'scenario':name,**row})
print(json.dumps({k:v for k,v in out.items() if k not in ['base','bear','bull','owned_revised','owned_business_crosscheck','checks','snapshot_hashes']},indent=2))
