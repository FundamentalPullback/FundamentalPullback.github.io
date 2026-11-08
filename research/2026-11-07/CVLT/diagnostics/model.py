"""Bounded diagnostic only. USD millions. No canonical valuation or approval."""
import json,csv,copy
from pathlib import Path
P=Path(__file__).resolve().parent
price=158.36;shares=42.221;cash=897.250;debt=900.;r0=1252.044
rf=.0486;erp=.0441;beta=.90
# Historical operating balance coefficients are rounded analyst proxies, not forecast facts.
# Deferred revenue 763.860 / TTM sales = 61%; AR 280.575 / sales =22.4%.
# Other operating net assets lift ex-commission asset coefficient to31%; net noncommission WC=-30%.
cases={
 'adverso':dict(growth=[.10,.08,.06,.05,.04],margin=[.09,.095,.10,.105,.11],terminal_margin=.12,sbc=[.12,.115,.11,.105,.10],terminal_sbc=.09,g=.02,roic=.12,spread=.04,cash_reserve=180.,contingency=75.),
 'central':dict(growth=[.14,.13,.11,.09,.07],margin=[.105,.12,.135,.15,.16],terminal_margin=.18,sbc=[.11,.105,.10,.095,.09],terminal_sbc=.08,g=.025,roic=.18,spread=.025,cash_reserve=125.,contingency=25.),
 'favorable':dict(growth=[.18,.17,.15,.12,.10],margin=[.12,.14,.16,.18,.20],terminal_margin=.24,sbc=[.105,.10,.095,.09,.085],terminal_sbc=.07,g=.03,roic=.24,spread=.015,cash_reserve=80.,contingency=0.)}
def lerp(a,b,t):return a+(b-a)*t
def calc(c,wacc_override=None,margin_add=0):
 tax=.24;ke=rf+beta*erp;kd=rf+c['spread'];E=price*shares;wacc=E/(E+debt)*ke+debt/(E+debt)*kd*(1-tax)
 if wacc_override is not None:wacc=wacc_override
 rows=[];rev=r0
 for i in range(10):
  t=max(0,(i-4)/5);growth=c['growth'][i] if i<5 else lerp(c['growth'][-1],c['g'],t)
  margin=(c['margin'][i] if i<5 else lerp(c['margin'][-1],c['terminal_margin'],t))+margin_add
  sbc=c['sbc'][i] if i<5 else lerp(c['sbc'][-1],c['terminal_sbc'],t)
  prev=rev;rev*=1+growth;ebit=rev*margin;nopat=ebit*(1-tax)
  da=rev*.0082;capex=rev*.008
  commission_cash=rev*lerp(.068,.060,t);commission_amort=rev*lerp(.0447,.052,t)
  delta_op_assets=.31*(rev-prev);delta_deferred=.61*(rev-prev)
  # Marketplace and other operating assets reside in .31 coefficient; no duplicate standalone addback.
  dnwc=delta_op_assets-delta_deferred
  raw_reinvestment=capex-da+commission_cash-commission_amort+dnwc
  # Transition to sustainable reinvestment. Residual is explicit cash spending, not a free profitability credit.
  target=nopat*growth/c['roic'];extra=max(0,target-raw_reinvestment)*t
  reinvestment=raw_reinvestment+extra;fcff=nopat-reinvestment
  rows.append(dict(year=i+1,phase='explicit' if i<5 else 'transition',revenue=rev,growth=growth,gaap_margin_including_sbc=margin,sbc_ratio=sbc,sbc_cost=rev*sbc,ebit_before_sbc_diagnostic=ebit+rev*sbc,ebit=ebit,tax=tax,nopat=nopat,da=da,capex=capex,commission_cash=commission_cash,commission_amort=commission_amort,delta_other_operating_assets=delta_op_assets,delta_deferred_revenue=delta_deferred,delta_other_nwc=dnwc,additional_transition_investment=extra,reinvestment=reinvestment,fcff=fcff,pv=fcff/(1+wacc)**(i+1)))
 term_nopat=rows[-1]['nopat']*(1+c['g']);term_reinvestment=term_nopat*c['g']/c['roic'];term_fcff=term_nopat-term_reinvestment
 tpv=term_fcff/(wacc-c['g'])/(1+wacc)**10;ev=sum(x['pv'] for x in rows)+tpv
 equity=ev+cash-c['cash_reserve']-debt-c['contingency'];v=equity/shares
 assert wacc>c['g'];assert all(abs(x['fcff']-(x['nopat']+x['da']-x['capex']+x['commission_amort']-x['commission_cash']-x['delta_other_nwc']-x['additional_transition_investment']))<1e-8 for x in rows)
 return dict(value=v,wacc=wacc,ke=ke,kd=kd,ev=ev,equity=equity,terminal_weight=tpv/ev,terminal_fcff=term_fcff,terminal_reinvestment=term_reinvestment,rows=rows,below_conversion_threshold=v<236.88)
results={}
for name,c in cases.items():
 r=calc(c);results[name]={k:v for k,v in r.items() if k!='rows'}
 with (P/f'forecast_{name}.csv').open('w') as f:
  w=csv.DictWriter(f,fieldnames=r['rows'][0]);w.writeheader();w.writerows(r['rows'])
sensitivity=[]
for w in [.075,.085,.095,.105]:
 for g in [.02,.025,.03]:
  c=copy.deepcopy(cases['central']);c['g']=g;sensitivity.append(dict(wacc=w,g=g,value=calc(c,w)['value']))
# Same model inverse: increase GAAP margins all years, including terminal, with unchanged SBC costs.
inverse=[]
for growthshift in [-.02,0,.02]:
 c=copy.deepcopy(cases['central']);c['growth']=[x+growthshift for x in c['growth']]
 lo,hi=-.09,.8
 for _ in range(80):
  mid=(lo+hi)/2
  if calc(c,margin_add=mid)['value']<price:lo=mid
  else:hi=mid
 inverse.append(dict(growth_shift_first_five=growthshift,margin_uplift=(lo+hi)/2,year1_margin=c['margin'][0]+(lo+hi)/2,terminal_margin=c['terminal_margin']+(lo+hi)/2,implied_value=calc(c,margin_add=(lo+hi)/2)['value']))
output=dict(status='diagnostic_only_partial_not_decision_ready',canonical_valuation=None,rf=rf,rf_date='2026-11-06',erp=erp,erp_date='2026-11-01',beta=beta,beta_observation_date='2026-11-08',assumptions=cases,scenarios=results,sensitivity=sensitivity,inverse=inverse,checks=dict(no_sbc_addback=True,fcff_identity=True,ten_years=True,terminal_reinvestment_tied_to_roic=True,no_orders=True))
(P/'results.json').write_text(json.dumps(output,indent=2));print(json.dumps(results,indent=2));print(json.dumps(inverse,indent=2))
