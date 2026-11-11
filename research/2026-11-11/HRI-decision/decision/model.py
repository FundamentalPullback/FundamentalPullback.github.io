"""HRI replacement-cost FCFF support model. USD millions except per share.
No leverage repayments/interest in FCFF. All fleet acquisitions paid when incurred.
Y1-5 explicit operating cases; Y6-10 linear transition to mature margins/reinvestment.
"""
import json,csv,math,copy
from pathlib import Path
P=Path(__file__).parent
I=json.loads((P/'inputs.json').read_text())
def run(case, overrides=None):
 c=copy.deepcopy(I['scenarios'][case]);c.update(overrides or {})
 rental=I['rental_revenue_2026'];fleet=I['fleet_oec']*c['replacement_cost_premium'];rows=[]
 for year in range(1,11):
  a=max(0,(year-5)/5)
  growth=c['growth'][year-1] if year<=5 else c['growth'][-1]*(1-a)+c['terminal_g']*a
  price=c['price_growth'];infl=c['equipment_inflation']*(1-a)+price*a;eff=c['efficiency'][year-1] if year<=5 else 0
  volume=max(0,(1+growth)/((1+price)*(1+eff))-1) # no forced liquidation in downturn
  prev_rental=rental;rental*=1+growth
  fleet_begin=fleet;fleet*= (1+volume)*(1+infl)
  # Existing fleet's maintenance replacement and disposal, no sale gain double count.
  gross_replace=fleet_begin*(1+infl)/c['holding_life']
  proceeds=gross_replace*c['residual_fraction']/((1+infl)**c['holding_life'])
  net_replace=gross_replace-proceeds
  # New capacity separate from replacing old units; utilization gains can avoid purchases.
  fleet_growth=fleet_begin*(1+infl)*volume
  margin=(c['core_margin_start']+(c['core_margin_y5']-c['core_margin_start'])*year/5) if year<=5 else c['core_margin_y5']*(1-a)+c['core_margin_terminal']*a
  ebitda=rental*margin # includes ancillary profits, SBC, operating lease expense; excludes used-fleet gain
  other_maintenance=I['other_net_maintenance_2026']*rental/I['rental_revenue_2026']
  econ_da=net_replace+other_maintenance
  ebit=ebitda-econ_da;tax=c['tax_first5'][year-1] if year<=5 else c['tax'];nopat=ebit*(1-tax)
  other_growth=max(0,rental-prev_rental)*c['other_growth_ratio']
  nwc=(rental-prev_rental)*c['nwc_ratio']
  physical_reinvest=fleet_growth+other_growth+nwc
  if c.get('guided_net_capex_ratio') is not None:
   physical_reinvest=c['guided_net_capex_ratio']*rental-net_replace+other_growth+nwc
  mature_reinvest=nopat*growth/c['terminal_roic']
  reinvest=physical_reinvest*(1-a)+mature_reinvest*a
  fcff=nopat-reinvest
  rows.append(dict(year=year,rental_revenue=rental,growth=growth,core_cash_ebitda=ebitda,core_margin=margin,fleet_replacement_cost_begin=fleet_begin,fleet_gross_replacement=gross_replace,fleet_disposal_proceeds=proceeds,fleet_net_replacement=net_replace,other_net_maintenance=other_maintenance,economic_da=econ_da,economic_ebit=ebit,unlevered_cash_tax_rate=tax,nopat=nopat,capacity_growth=volume,fleet_growth_capex=fleet_growth,other_growth_capex=other_growth,delta_nwc=nwc,physical_reinvestment=physical_reinvest,terminal_transition_weight=a,modeled_growth_reinvestment=reinvest,fcff=fcff,pv_fcff=fcff/(1+c['wacc'])**year))
 # Stabilize mature operating economics in perpetuity: year11 NOPAT grows at g.
 terminal_nopat=rows[-1]['nopat']*(1+c['terminal_g'])
 terminal_fcff=terminal_nopat*(1-c['terminal_g']/c['terminal_roic'])
 terminal_value=terminal_fcff/(c['wacc']-c['terminal_g']);pv_terminal=terminal_value/(1+c['wacc'])**10
 ev=sum(r['pv_fcff'] for r in rows)+pv_terminal
 bridge=I['gross_debt']+I['financing_obligations']+I['fleet_purchase_payables']+c['accrued_interest_reserve']+c['pension_reserve']+c['other_claim_reserve']-(I['cash']-c['operating_cash_buffer'])-c['earnout_value']
 equity=ev-bridge;value=max(0,equity)/c['shares']
 return dict(case=case,assumptions=c,rows=rows,enterprise_value=ev,bridge=bridge,equity_raw=equity,value_per_share=value,pv_terminal=pv_terminal,terminal_share_ev=pv_terminal/ev,terminal_nopat=terminal_nopat,terminal_fcff=terminal_fcff,terminal_value=terminal_value,implied_ev_core_ebitda=ev/rows[0]['core_cash_ebitda'],price=I['price'],price_implied_ev=I['price']*c['shares']+bridge)
def solve(key,lo,hi):
 for _ in range(100):
  mid=(lo+hi)/2
  if run('base',{key:mid})['value_per_share']<I['price']:
   if key=='wacc':hi=mid
   else:lo=mid
  else:
   if key=='wacc':lo=mid
   else:hi=mid
 return (lo+hi)/2
if __name__=='__main__':
 out={k:run(k) for k in I['scenarios']}
 out['guided_conversion']=run('base',{'guided_net_capex_ratio':1050/4512.5})
 out['enhanced_margin_conversion']=run('base',{'guided_net_capex_ratio':1050/4512.5,'core_margin_start':.465,'core_margin_y5':.475,'core_margin_terminal':.46})
 out['q3_margin_conversion']=run('base',{'guided_net_capex_ratio':1050/4512.5,'core_margin_start':.446,'core_margin_y5':.46,'core_margin_terminal':.45})
 out['fleet_only_terminal']=run('base',{'terminal_roic':out['base']['rows'][-1]['nopat']*.025/out['base']['rows'][-1]['physical_reinvestment']})
 out['joint_favorable_sensitivity']=run('base',{'guided_net_capex_ratio':1050/4512.5,'core_margin_start':.465,'core_margin_y5':.475,'core_margin_terminal':.46,'terminal_roic':.25,'tax_first5':[.05]*5,'wacc':.095})
 out['reverse']={'base_break_even_wacc':solve('wacc',.035,.2),'base_break_even_holding_life':solve('holding_life',4,30),'base_break_even_terminal_margin':solve('core_margin_terminal',.2,.8),'note':'Each reverse changes one variable only; not independent forecasts.'}
 lo,hi=0,.3
 for _ in range(100):
  mid=(lo+hi)/2
  z=run('base',{k:I['scenarios']['base'][k]+mid for k in ['core_margin_start','core_margin_y5','core_margin_terminal']})
  if z['value_per_share']<I['price']:lo=mid
  else:hi=mid
 out['reverse']['uniform_core_margin_uplift']=(lo+hi)/2
 out['reverse']['uniform_margin_result']=run('base',{k:I['scenarios']['base'][k]+(lo+hi)/2 for k in ['core_margin_start','core_margin_y5','core_margin_terminal']})
 (P/'results.json').write_text(json.dumps(out,indent=2))
 for k in [x for x in out if x!='reverse']:
  with (P/(k+'_forecast.csv')).open('w') as f:
   w=csv.DictWriter(f,fieldnames=list(out[k]['rows'][0]));w.writeheader();w.writerows(out[k]['rows'])
 sensitivities=[]
 for w in [.085,.095,.10,.105,.115]:
  for life in [7,7.5,8,8.5,9]:
   r=run('base',{'wacc':w,'holding_life':life});sensitivities.append({'wacc':w,'holding_life':life,'value_per_share':r['value_per_share']})
 with (P/'sensitivity.csv').open('w') as f:
  w=csv.DictWriter(f,fieldnames=list(sensitivities[0]));w.writeheader();w.writerows(sensitivities)
 print(json.dumps({k:{x:v for x,v in out[k].items() if x not in ['rows','assumptions']} for k in I['scenarios']},indent=2));print(out['reverse'])
