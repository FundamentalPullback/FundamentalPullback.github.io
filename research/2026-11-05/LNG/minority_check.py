"""Independent cash-flow cross-check of outside CQP common units.
Not an alternative subtraction in the primary market-marked bridge.
Constant nominal CQP debt after $500m estimated paydown; cost of equity
held constant; terminal cash distribution follows nonlinear GP/IDR tiers.
"""
from pathlib import Path
import json,datetime
P=Path(__file__).parent;C=json.loads((P/'capital.json').read_text());I=json.loads((P/'model/inputs.json').read_text());U=484.057704;OUT=(484057704-239872502)/484057704
TIERS=[(0,.489,.02),(.489,.531,.15),(.531,.638,.25),(.638,float('inf'),.5)]
def dist(d):
 lp=d*U;gp=sum(max(0,min(d,hi)-lo)*U*frac/(1-frac)for lo,hi,frac in TIERS);return dict(lp=lp,gp=gp,total=lp+gp,outside=lp*OUT,parent=lp*(1-OUT)+gp)
def allocate(cash):
 if cash<=0:return dict(quarter_lp_distribution=0,outside=0,parent=0,unfunded_cash_deficit=-cash)
 lo=0;hi=20
 for _ in range(100):
  mid=(lo+hi)/2
  if 4*dist(mid)['total']>cash:hi=mid
  else:lo=mid
 d=(lo+hi)/2;r=dist(d);return dict(quarter_lp_distribution=d,outside=4*r['outside'],parent=4*r['parent'],unfunded_cash_deficit=0)
def calc(name):
 c=I['cases'][name];g=c['terminal_growth'];h=c['terminal_fee_haircut'];ke=C['capital']['risk_free']+C['CQP']['normalized_beta']*C['capital']['equity_risk_premium'];ke+=dict(bear=.015,base=0,bull=-.003)[name]
 target_d=dict(bear=3.5,base=4.125,bull=4.25)[name];debt=14523-500;rate=dict(bear=.06,base=.05,bull=.05)[name];interest=debt*rate;maint2029=dict(bear=110,base=80,bull=70)[name]
 # Management's common-unit DCF run-rate anchors distributable cash, not all companyFCFF.
 run_total=dist(target_d/4)['total']*4;ebitda0=run_total+interest+maint2029
 rows=[];first=None;stub=57/365
 for y in range(1,11):
  if y<=5:
   infl=(1+c['unit_profit_inflation'])**max(0,y-3);ebitda=ebitda0*infl+c['temporary_marketing_premium'][y-1]*.8*.55;da=700*infl;maint=maint2029*(1.02)**(y-3);reinv=maint-da
  else:
   k=y-5;f=k/5;ebitda=first['ebitda']*(1+g)**k*(1-h*f);da=first['da']*(1+g)**k;ebit=ebitda-da;young_net=(first['maint']-first['da'])*(1+g)**k;reinv=(1-f)*young_net+f*ebit*g/c['terminal_roic'];maint=reinv+da
  ebit=ebitda-da;fcff=ebit-reinv;paydown=500 if y==1 else 0;available=fcff-interest-paydown;a=allocate(available);r=dict(year=2026+y,ebitda=ebitda,da=da,ebit=ebit,reinvestment=reinv,maint=maint,fcff=fcff,interest=interest,debt_paydown=paydown,cash_available=available,**a);r['pv_outside']=r['outside']/(1+ke)**(y+stub);rows.append(r)
  if y==5:first=r
 # Above top tier, total annual partnershipcash = 2*LPcash - K; LPcash = .5*(cash+K).
 # K is constant because contractual dollar thresholds do not grow.
 d=dist(.638);K=4*(2*d['lp']-d['total']);alpha=OUT/2
 outside_tv=0.;k=1
 while True:
  fcf_next=rows[-1]['fcff']*(1+g)**k;alloc=allocate(fcf_next-interest)
  if alloc['quarter_lp_distribution']>=.638:
   outside_tv+=(alpha*fcf_next/(ke-g)+alpha*(K-interest)/ke)/(1+ke)**(k-1);break
  outside_tv+=alloc['outside']/(1+ke)**k;k+=1
  assert k<1000
 value=sum(r['pv_outside']for r in rows)+outside_tv/(1+ke)**(10+stub)
 return dict(cost_equity=ke,normalized_runrate_lp_dcf_per_unit=target_d,derived_runrate_ebitda=ebitda0,runrate_total_distributable_cash=run_total,assumed_refinancing_rate=rate,constant_nominal_debt_after_paydown=debt,terminal_growth=g,terminal_fee_haircut=h,terminal_gp_threshold_constant=K,outside_alpha=alpha,rows=rows,outside_equity_dcf=value,outside_per_unit=value/(U*OUT),outside_market_equity=C['capital']['nci_market_equity'],parent_valuation_delta_using_this_check=(C['capital']['nci_market_equity']-value)/C['capital']['shares_proxy_m'])
out={name:calc(name)for name in I['cases']};(P/'minority_check.json').write_text(json.dumps(out,indent=2));print(json.dumps({k:{x:v[x]for x in ['cost_equity','derived_runrate_ebitda','outside_equity_dcf','outside_per_unit','parent_valuation_delta_using_this_check']}for k,v in out.items()},indent=2))
