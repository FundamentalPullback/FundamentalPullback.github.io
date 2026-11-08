import json,pathlib,csv,math
P=pathlib.Path(__file__).parent
h=json.loads((P/'history.json').read_text());ttm=h['TTM202609'];R0=ttm['revenue'];price=77.06
shares=47.426142; dilution=.490 # incremental diluted vs basic Q1, explicitly proxy
D=571.289; pension=9.658; cash=193.653;ppe0=593.238
E=price*shares;wd=D/(D+E);rf=.0486;erp=.0441;tax=.30
scenarios={
'prudente':dict(growth=.02,g=.015,margin=.19,terminal_margin=.175,beta=1.50,kd=.065,cash_reserve=.20,capital_ratio=.65,extra_initial_capex=50),
'central':dict(growth=.05,g=.025,margin=.22,terminal_margin=.21,beta=1.25,kd=.059,cash_reserve=.15,capital_ratio=.53,extra_initial_capex=25),
'favorable':dict(growth=.075,g=.03,margin=.25,terminal_margin=.235,beta=1.0,kd=.059,cash_reserve=.12,capital_ratio=.53,extra_initial_capex=0)}
def calc(s,margin_shift=0):
 ke=rf+s['beta']*erp;wacc=(1-wd)*ke+wd*s['kd']*(1-tax)
 r=R0;stock=ppe0;dr=ttm['da']/ppe0;rows=[];pv=0
 for t in range(1,12):
  fade=max(0,min(1,(t-5)/5));g=s['growth']+(s['g']-s['growth'])*fade
  prev=r;r*=1+g; margin=s['margin']+(s['terminal_margin']-s['margin'])*fade+margin_shift
  da=stock*dr
  # Operating cash margin after SBC, content, software, marketing and lease charges. No SBC addback.
  # Additional 8m annual rental renewal reserve grows with revenue, beyond current accounting expense.
  cash_ebit=r*margin-8*r/R0
  ebit=cash_ebit-da;nopat=ebit*(1-tax)
  # replacement fully funded plus capacity; no free capital release when growth slows.
  growth_cap=s['capital_ratio']*max(r-prev,0)
  if t==10: growth_cap=max(growth_cap,s['capital_ratio']*r-stock,0)
  if t==11: growth_cap=stock*s['g'] # exact stable asset/revenue ratio from terminal onwards
  special=s['extra_initial_capex'] if t==1 else 0
  capex=da+growth_cap+special
  wc=.03*max(r-prev,0) # customer float does not fund incremental growth for free
  fcff=nopat+da-capex-wc
  stock+=capex-da
  row=dict(year=t,revenue=r,growth=g,cash_margin=margin,cash_ebit=cash_ebit,da=da,ebit=ebit,nopat=nopat,capex=capex,incremental_wc=wc,ppe_end=stock,fcff=fcff)
  rows.append(row)
  if t<=10:pv+=fcff/(1+wacc)**t
 tv=rows[10]['fcff']/(wacc-s['g']);pvtv=tv/(1+wacc)**10
 excess=max(0,cash-s['cash_reserve']*R0)
 eq=pv+pvtv-D-pension+excess
 return dict(wacc=wacc,ke=ke,rows=rows,ev=pv+pvtv,explicit_pv=pv,terminal_pv=pvtv,terminal_share=pvtv/(pv+pvtv),excess_cash=excess,equity_conditional=eq,value_conditional=eq/(shares+dilution),no_terminal_equity=(pv-D-pension+excess)/(shares+dilution),unknown_claims_adjustment=None)
out={k:calc(s) for k,s in scenarios.items()}
lo,hi=-.15,.5
for _ in range(100):
 mid=(lo+hi)/2
 if calc(scenarios['central'],mid)['value_conditional']<price:lo=mid
 else:hi=mid
inverse=dict(required_cash_margin_shift=(lo+hi)/2,year1_cash_margin=scenarios['central']['margin']+(lo+hi)/2,terminal_cash_margin=scenarios['central']['terminal_margin']+(lo+hi)/2,condition='All central growth, funding, leases, shares and discount inputs fixed; not consensus or approval.')
res=dict(asof='2026-11-08',price=price,quote_session='2026-11-06 NYSE regular close',shares_current_m=shares,incremental_dilution_proxy_m=dilution,market_cap=E,bridge=dict(debt_principal=D,unrestricted_cash=cash,restricted_cash_excluded=.559,pension_deficit_dated_20260630=pension,operating_lease_liabilities_in_rent_not_debt=599.934,unknown_legal_claims=None),assumptions=scenarios,scenarios=out,inverse=inverse,approved_value=None,approved_entry=None)
(P/'results.json').write_text(json.dumps(res,indent=2))
for k,v in out.items():
 with (P/(k+'_10year.csv')).open('w') as f:
  w=csv.DictWriter(f,fieldnames=v['rows'][0]);w.writeheader();w.writerows(v['rows'])
print(json.dumps({k:{x:v[x] for x in ['wacc','value_conditional','terminal_share','no_terminal_equity']} for k,v in out.items()},indent=2));print(inverse)
