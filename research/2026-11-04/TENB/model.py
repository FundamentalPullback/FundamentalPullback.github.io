import json,csv,copy,math
from pathlib import Path
p=Path(__file__).parent
R0=1067.486; PRICE=47.03; basic=104.507623; shares=basic+0.576*(1-12.18/PRICE)+max(0,14.436-328.966/PRICE)+max(0,0.985-12.878/PRICE); cash=495.261; reserve=100; debt=800;bridge=cash-reserve-debt
# SBC retained within EBIT. No future share issuance or repurchases assumed. Existing awards proxy separately.
scenarios={
'adverse':dict(growth=[.06,.05,.04,.035,.03],margins=[.065,.08,.09,.10,.11],m10=.12,wacc=.115,g=.02,roic=.15,tax=.25,da=[.035,.032,.029,.026,.023],capex=.03,wc=.03),
'central':dict(growth=[.10,.10,.09,.08,.07],margins=[.09,.12,.15,.175,.20],m10=.22,wacc=.105,g=.025,roic=.25,tax=.23,da=[.035,.032,.029,.026,.023],capex=.03,wc=.02),
'favorable':dict(growth=[.14,.14,.13,.12,.10],margins=[.12,.17,.22,.26,.29],m10=.30,wacc=.095,g=.03,roic=.35,tax=.22,da=[.035,.032,.029,.026,.023],capex=.03,wc=.01)}
def calc(a,den=shares):
 revenue=R0;pv=0;rows=[];terminal_reinvest_rate=a['m10']*(1-a['tax'])*a['g']/a['roic']
 # Detailed years: D&A (includes amortization) minus total capex/software and delta operating WC/commissions.
 # Transition net investment glides from year5 net investment/revenue to terminal g/ROIC requirement.
 y5_net_rate=(a['capex']-a['da'][4])+a['wc']*a['growth'][4]/(1+a['growth'][4])
 for t in range(1,11):
  if t<=5:gr=a['growth'][t-1];margin=a['margins'][t-1]
  else:
   z=(t-5)/5;gr=a['growth'][-1]+(a['g']-a['growth'][-1])*z;margin=a['margins'][-1]+(a['m10']-a['margins'][-1])*z
  old=revenue;revenue*=1+gr;ebit=revenue*margin;nopat=ebit*(1-a['tax'])
  if t<=5:da=revenue*a['da'][t-1];capex=revenue*a['capex'];d_wc=a['wc']*(revenue-old)
  else:
   z=(t-5)/5;da=revenue*.02;d_wc=a['wc']*(revenue-old);netrate=y5_net_rate+(terminal_reinvest_rate-y5_net_rate)*z;capex=da+revenue*netrate-d_wc
  reinvest=capex+d_wc-da;fcff=nopat-reinvest;discount=(1+a['wacc'])**t;pv+=fcff/discount
  rows.append(dict(year=t,growth=gr,revenue=revenue,ebit_margin=margin,ebit=ebit,tax_rate=a['tax'],nopat=nopat,da=da,capex_and_software=capex,delta_wc_and_commissions=d_wc,net_reinvestment=reinvest,fcff=fcff,pv_fcff=fcff/discount))
 terminal_nopat=revenue*(1+a['g'])*a['m10']*(1-a['tax']);terminal_reinvest=terminal_nopat*a['g']/a['roic'];terminal_cf=terminal_nopat-terminal_reinvest;tv=terminal_cf/(a['wacc']-a['g']);pvt=tv/(1+a['wacc'])**10;ev=pv+pvt;eq=ev+bridge
 return dict(value=eq/den,ev=ev,equity=eq,pv_explicit=pv,pv_terminal=pvt,terminal_weight=pvt/ev,terminal_fcff=terminal_cf,terminal_reinvestment=terminal_reinvest,rev10=revenue,rows=rows)
results={k:calc(a) for k,a in scenarios.items()}
# Reverse combinations use constant first5 growth, fade to terminal. Margins interpolate from year1 9% to chosen year5, then fade to stated year10.
def reverse_for_margins(m5,m10,wacc=.105):
 def v(gr):
  a=copy.deepcopy(scenarios['central']);a['growth']=[gr]*5;a['margins']=[.09+(m5-.09)*i/4 for i in range(5)];a['m10']=m10;a['wacc']=wacc;return calc(a)
 lo=-.1;hi=.8
 for _ in range(100):
  mid=(lo+hi)/2
  if v(mid)['value']<PRICE:lo=mid
  else:hi=mid
 r=v((lo+hi)/2);return dict(growth_first5=(lo+hi)/2,margin5=m5,margin10=m10,rev10=r['rev10'],fcff10=r['rows'][-1]['fcff'],value=r['value'])
reverse=[reverse_for_margins(a,b) for a,b in [(.2,.22),(.25,.27),(.3,.32),(.35,.35)]]
sens=[]
for w in [.095,.105,.115]:
 for g in [.02,.025,.03]:
  a=copy.deepcopy(scenarios['central']);a['wacc']=w;a['g']=g;sens.append({'wacc':w,'g':g,'value':calc(a)['value']})
# Solve terminal margin for fixed 10% first5 growth, linear margin ramp year1 9% -> year5 m and flat thereafter.
def margin_solve():
 lo=.05;hi=.9
 for _ in range(100):
  m=(lo+hi)/2;a=copy.deepcopy(scenarios['central']);a['growth']=[.10]*5;a['margins']=[.09+(m-.09)*i/4 for i in range(5)];a['m10']=m
  if calc(a)['value']<PRICE:lo=m
  else:hi=m
 return (lo+hi)/2
out=dict(as_of='2026-11-04',price=PRICE,base_revenue=R0,spot_basic_shares=basic,existing_equity_award_proxy=shares-basic,model_shares=shares,market_equity_basic=basic*PRICE,market_EV_basic=basic*PRICE+debt-cash,bridge=dict(cash_and_investments=cash,minimum_operating_cash=reserve,debt_face=debt,net_bridge=bridge),assumptions=scenarios,results=results,reverse=reverse,reverse_margin_at_10pct_growth=margin_solve(),sensitivities=sens)
joint=[]
for early,m5,m10,wacc in [(.10,.20,.22,.105),(.12,.25,.27,.10),(.14,.29,.30,.095),(.10,.25,.27,.095)]:
 a=copy.deepcopy(scenarios['central']);a['growth']=[early]*5;a['margins']=[.09+(m5-.09)*i/4 for i in range(5)];a['m10']=m10;a['wacc']=wacc; r=calc(a);joint.append(dict(growth_first5=early,margin5=m5,margin10=m10,wacc=wacc,value=r['value'],rev10=r['rev10']))
out['joint_scenarios']=joint
(p/'model.json').write_text(json.dumps(out,indent=2))
for k,r in results.items():
 with (p/(k+'_10year.csv')).open('w') as f:
  w=csv.DictWriter(f,fieldnames=r['rows'][0].keys());w.writeheader();w.writerows(r['rows'])
 print(k,{x:y for x,y in r.items() if x!='rows'})
print('reverse',reverse,'margin at10%',out['reverse_margin_at_10pct_growth']);print('sensitivities',sens)
print('basic denominator values', {k:calc(a,basic)['value'] for k,a in scenarios.items()})
