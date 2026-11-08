"""Public, conditional FCFF. USD millions; prices and shares split adjusted.
R&D and SBC stay expensed. No separate capitalization/reinvestment charge for R&D.
Incremental capacity, replacement, working capital and a net operating ROIC constraint are funded.
"""
from pathlib import Path
import json,csv,copy,math
P=Path(__file__).resolve().parent
PRICE=138.49;SHARES=1302.962435+5.734;BASE=14505.795
NWC=3072.087+266.755+4090.426+129.900+219.239+143.971-740.743-1707.802-507.776-574.679
BRIDGE={'cash_and_marketable_securities':4741.191,'operating_cash_reserve':-1000,'debt_september_market_value':-5080,'interest_rate_swap_liabilities':-165.644,'other_hedges_net':11.550-25.198,'pension_noncurrent':-43.733,'edsp_assets_minus_liabilities':411.061-413.197,'noncurrent_tax_payable':-299.437,'restructuring_june_proxy':-5.3}
S={
'adverso':dict(growth=[.10,-.12,.03,.05,.04],margin1=.40,margin5=.35,marginT=.34,tax1=.20,taxT=.24,wacc=.125,g=.025,roic=.40,rt=.30,nwc=.40,maint=.022,capacity=.25,rd=.12,factoring=150,claims=300),
'central':dict(growth=[.25,.18,.12,.10,.08],margin1=.445,margin5=.43,marginT=.41,tax1=.17,taxT=.21,wacc=.1125,g=.03,roic=.55,rt=.40,nwc=.34,maint=.018,capacity=.18,rd=.105,factoring=75,claims=150),
'favorable':dict(growth=[.35,.23,.18,.14,.11],margin1=.46,margin5=.48,marginT=.46,tax1=.155,taxT=.18,wacc=.10,g=.035,roic=.70,rt=.50,nwc=.30,maint=.017,capacity=.16,rd=.10,factoring=25,claims=50)}
def calc(s,margin_shift=0,growth_shift=0,physical_only=False,tail_years=300):
 sales=BASE;nwc=NWC;gross=3282.320-202.532;pv=0;tail_pv=0;rows=[]
 for y in range(1,11+tail_years):
  growth=s['growth'][y-1] if y<=5 else s['growth'][-1]+(s['g']-s['growth'][-1])*min(y-5,5)/5
  if 2<=y<=10:growth+=growth_shift*(10-y)/8
  old=sales;sales*=1+growth
  m=s['margin1']+(s['margin5']-s['margin1'])*min(y-1,4)/4 if y<=5 else s['margin5']+(s['marginT']-s['margin5'])*min(max(y-5,0),5)/5
  m+=margin_shift*min(y-1,4)/4
  tax=s['tax1']+(s['taxT']-s['tax1'])*min(y-1,9)/9;ebita=sales*m;nopat=ebita*(1-tax)
  da=gross*.07;maint=max(sales*s['maint'],da*1.10);growthcap=max(0,sales-old)*s['capacity']
  target=sales*s['nwc'];wc=target-nwc;nwc=target
  # Cash release limited in a contraction; unrecovered inventory is an economic cash loss.
  loss=max(0,-wc)*.4;wc+=loss
  explicit=maint+growthcap-da+wc;roic=s['roic']+(s['rt']-s['roic'])*min(max(y-5,0),5)/5
  floor=nopat*max(growth,0)/roic;extra=0 if physical_only else max(0,floor-explicit)
  capex=maint+growthcap+extra;reinvestment=capex-da+wc;unwind=s['factoring']/3 if y<=3 else 0
  fcff=nopat-reinvestment-unwind;gross+=growthcap+extra
  row=dict(year=y,sales=sales,growth=growth,cash_ebita_margin=m,cash_ebita=ebita,tax_rate=tax,nopat=nopat,rd_expensed_memo=sales*s['rd'],physical_da=da,replacement_capex=maint,growth_capex=growthcap,additional_capacity_capex=extra,total_capex=capex,delta_nwc=wc,nonreleased_inventory_cash=loss,nwc_target=target,roic_assumption=roic,roic_funding_floor=floor,reinvestment=reinvestment,factoring_normalization=unwind,fcff=fcff,gross_depreciable_assets=gross)
  if y<=11:rows.append(row)
  if y<=10:pv+=fcff/(1+s['wacc'])**y
  else:tail_pv+=fcff/(1+s['wacc'])**y
 # Preserve physical-stock dynamics during the perpetual tail; no immediate Gordon shortcut.
 remainder=fcff*(1+s['g'])/(s['wacc']-s['g'])/(1+s['wacc'])**(10+tail_years)
 tv=tail_pv+remainder;ev=pv+tv;bridge=sum(BRIDGE.values())-s['claims'];eq=ev+bridge
 return dict(value_per_share=eq/SHARES,enterprise_value=ev,equity_value=eq,bridge=bridge,terminal_pv=tv,explicit_pv=pv,terminal_weight=tv/ev,terminal_method='constant mature sales growth/margins/tax/ROIC; physical stock and renewal continue dynamically',terminal_tail_years=tail_years,terminal_remainder_pv=remainder,year11_gordon_pv_diagnostic=rows[-1]['fcff']/(s['wacc']-s['g'])/(1+s['wacc'])**10,rows=rows)
def root(kind):
 lo,hi=(-.30,.50) if kind=='margin' else (-.05,.70)
 def val(x):return calc(S['central'],margin_shift=x if kind=='margin' else 0,growth_shift=x if kind=='growth' else 0)['value_per_share']
 if not val(lo)<=PRICE<=val(hi):return None
 for _ in range(100):
  m=(lo+hi)/2
  if val(m)<PRICE:lo=m
  else:hi=m
 return (lo+hi)/2

def main():
 out={k:calc(s) for k,s in S.items()};sens=[]
 for k,v in out.items():
  with (P/f'forecast_{k}.csv').open('w') as f:w=csv.DictWriter(f,fieldnames=v['rows'][0]);w.writeheader();w.writerows(v['rows'])
 for w in [.10,.1125,.125]:
  for g in [.025,.03,.035]:
   s=copy.deepcopy(S['central']);s.update(wacc=w,g=g);sens.append(dict(wacc=w,g=g,value=calc(s)['value_per_share']))
 ke=.0486+1.5*.0441;dw=5245.644/(5245.644+PRICE*1302.962435)
 gaps=['Physical replacement and incremental net operating ROIC are explicit assumptions, not a verified factory-capacity forecast; purchase-commitment cancellation exposure is not quantified.', 'Current incremental diluted shares use the latest quarterly 5.734 million proxy; existing RSU versus future SBC expense overlap needs instrument-level reconciliation.', 'Debt and hedge marks are September 30, not November 6. Face-debt alternative is separately shown.', 'Current tax, minor pension portions, restructuring and contingent legal obligations are not fully separated; scenario reserves are illustrative, not loss bounds.', 'Factored receivable sales are flows, not outstanding exposure; the incremental funding normalization is a sensitivity.', 'Exact next earnings date unannounced; management references late January only.', 'Annual discounting simplifies the November valuation stub. Nonmarket investments inside other assets are not separately valued.']
 r=dict(physical_budget_only={k:calc(s,physical_only=True)['value_per_share'] for k,s in S.items()},ticker='KLAC',as_of='2026-11-08',status='material_partial',quality='screen-grade',price=PRICE,price_date='2026-11-06',price_session='regular_close',shares_actual=1302.962435,shares_actual_date='2026-10-26',shares_model=SHARES,stock_split='10-for-1; trading adjusted June 12, 2026',opening_nwc=NWC,bridge_items=BRIDGE,scenarios=out,sensitivity=sens,inverse_margin_shift=root('margin'),inverse_growth_shift=root('growth'),face_debt_plus_swap_value={k:v['value_per_share']-(5950-5080)/SHARES for k,v in out.items()},cost_of_capital=dict(rf=.0486,rf_date='2026-11-06',erp=.0441,erp_date='2026-11-01',erp_source_rf=.0529,date_basis_mismatch=True,observed_beta=1.5,ke=ke,kd_proxy=.0554,kd_date='2026-11-05',kd_source='FRED Single-A corporate effective yield; not issuer-specific refinancing quote',debt_weight=dw,mechanical_wacc=ke*(1-dw)+.0554*.79*dw,central_wacc=.1125),approved_values=dict(fair_value=None,buy_max=None,adverse=None,central=None,favorable=None),stage3_approved=False,stage3_5_approved=False,entry_approved=False,gaps=gaps)
 for n in ['results.json','model_results.json']:(P/n).write_text(json.dumps(r,indent=2))
 print({k:dict(value=v['value_per_share'],terminal=v['terminal_weight'],year1capex=v['rows'][0]['total_capex'],year11capex=v['rows'][-1]['total_capex']) for k,v in out.items()});print('inverse',r['inverse_margin_shift'],r['inverse_growth_shift']);print('capital',r['cost_of_capital'])
if __name__=='__main__':main()
