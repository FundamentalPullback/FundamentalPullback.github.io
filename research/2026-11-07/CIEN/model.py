"""Conditional FCFF; USD millions. FY2026 base is management guidance, not reported FY results.
R&D and SBC stay expensed. Convert option offset assumes purchased matching hedge performs;
sold warrants retain positive time value. Principal debt is deducted, not unhedged conversion shares too.
"""
from pathlib import Path
import json,csv,copy,math
P=Path(__file__).resolve().parent
PRICE=243.39;SHARES=141.808525+3.906;BASE=6420
NWC=1233.610+871.987+527.014-654.070-311.281-248.651-35.743-66.500
BRIDGE={'cash_and_investments':2843.554,'post_balance_repurchase':-36,'operating_cash_reserve':-600,'debt_principal':-3275,'finance_lease_rollforward_proxy':-39.772,'income_tax_liability_annual_proxy':-102.718,'fx_derivative_liability':-11.003,'deferred_compensation_net_proxy':-.017,'restructuring_current':-.539,'unquoted_investments_selected_proxy':15}
S={'adverso':dict(growth=[.15,.10,-.05,.05,.05],m1=.18,m5=.18,mt=.17,tax=.24,wacc=.12,g=.025,nwc=.32,roic=.25,rt=.20,maint=.03,capacity=.18,prepay=600,claims=200,sigma=.80,shield=75),
'central':dict(growth=[.30,.30,.30,.15,.10],m1=.225,m5=.28,mt=.25,tax=.22,wacc=.105,g=.03,nwc=.28,roic=.40,rt=.30,maint=.025,capacity=.14,prepay=400,claims=100,sigma=.65,shield=150),
'favorable':dict(growth=[.40,.35,.32,.22,.15],m1=.25,m5=.32,mt=.30,tax=.20,wacc=.095,g=.035,nwc=.24,roic=.55,rt=.40,maint=.022,capacity=.12,prepay=250,claims=40,sigma=.50,shield=225)}
def call(spot,strike,t,sigma,r=.0486):
 n=lambda x:(1+math.erf(x/math.sqrt(2)))/2
 d1=(math.log(spot/strike)+(r+.5*sigma*sigma)*t)/(sigma*math.sqrt(t));d2=d1-sigma*math.sqrt(t)
 return spot*n(d1)-strike*math.exp(-r*t)*n(d2)
def calc(s,ms=0,gs=0,physical_only=False,tail_years=300):
 sales=BASE;nwc=NWC;gross=1231.409;pv=0;rows=[]
 tail=0
 for y in range(1,11+tail_years):
  gr=s['growth'][y-1] if y<=5 else s['growth'][-1]+(s['g']-s['growth'][-1])*min(y-5,5)/5
  if 2<=y<=10:gr+=gs*(10-y)/8
  old=sales;sales*=1+gr;m=s['m1']+(s['m5']-s['m1'])*min(y-1,4)/4 if y<=5 else s['m5']+(s['mt']-s['m5'])*min(y-5,5)/5;m+=ms*min(y-1,4)/4
  nopat=sales*m*(1-s['tax']);da=gross*.105;maint=max(sales*s['maint'],da*1.10);capacity=max(0,sales-old)*s['capacity'];target=sales*s['nwc'];wc=target-nwc;nwc=target
  unrecovered=max(0,-wc)*.4;wc+=unrecovered
  # Supplier advances are funded once, not also subtracted as debt. No automatic terminal release.
  prepay=s['prepay'] if y==1 else 0
  explicit=maint+capacity-da+wc+prepay;roic=s['roic']+(s['rt']-s['roic'])*min(max(y-5,0),5)/5;floor=nopat*max(gr,0)/roic
  extra=0 if physical_only else max(0,floor-explicit);capex=maint+capacity+extra;reinv=capex-da+wc+prepay;fcff=nopat-reinv;gross+=capacity+extra
  row=dict(year=y,sales=sales,growth=gr,cash_ebita_margin=m,nopat=nopat,physical_da=da,replacement_capex=maint,growth_capex=capacity,additional_capacity_capex=extra,capex=capex,delta_nwc=wc,nwc_target=target,unrecovered_inventory_cash=unrecovered,supplier_advance=prepay,roic_assumption=roic,roic_funding_floor=floor,reinvestment=reinv,fcff=fcff,gross_physical_assets=gross);
  if y<=11:rows.append(row)
  if y<=10:pv+=fcff/(1+s['wacc'])**y
  else:tail+=fcff/(1+s['wacc'])**y
 remainder=fcff*(1+s['g'])/(s['wacc']-s['g'])/(1+s['wacc'])**(10+tail_years);tv=tail+remainder;ev=pv+tv
 warrants=3.8504875*call(PRICE,1000,5.19,s['sigma']);bridge=sum(BRIDGE.values())-warrants-s['claims']+s['shield'];eq=ev+bridge
 return dict(value_per_share=eq/SHARES,enterprise_value=ev,equity_value=eq,bridge=bridge,warrant_claim=warrants,convert_hedge_finite_tax_shield_proxy=s['shield'],terminal_weight=tv/ev,terminal_method="constant mature-policy dynamic physical-stock tail",terminal_remainder_pv=remainder,calibration_validated=False,terminal_pv=tv,explicit_pv=pv,rows=rows)
def root(kind):
 lo,hi=(-.2,.8) if kind=='margin' else (-.05,.7)
 fn=lambda x:calc(S['central'],ms=x if kind=='margin' else 0,gs=x if kind=='growth' else 0)['value_per_share']
 if not fn(lo)<=PRICE<=fn(hi):return None
 for _ in range(100):
  mid=(lo+hi)/2
  if fn(mid)<PRICE:lo=mid
  else:hi=mid
 return (lo+hi)/2

def main():
 out={k:calc(s) for k,s in S.items()};sens=[]
 for k,v in out.items():
  with (P/f'forecast_{k}.csv').open('w') as f:w=csv.DictWriter(f,fieldnames=v['rows'][0]);w.writeheader();w.writerows(v['rows'])
 for w in [.095,.105,.12]:
  for g in [.025,.03,.035]:
   s=copy.deepcopy(S['central']);s.update(wacc=w,g=g);sens.append(dict(wacc=w,g=g,value=calc(s)['value_per_share']))
 ke=.0486+1.35*.0441;dw=3275/(3275+PRICE*141.808525)
 r=dict(ticker='CIEN',as_of='2026-11-08',status='material_partial',quality='screen-grade',price=PRICE,price_date='2026-11-06',price_session='regular_close',shares_actual=141.808525,shares_date='2026-08-28',shares_model=SHARES,base_sales=BASE,base_status='FY2026 revenue guidance midpoint; not reported fiscal-year results',opening_nwc=NWC,bridge_items=BRIDGE,scenarios=out,physical_budget_only={k:calc(s,physical_only=True)['value_per_share'] for k,s in S.items()},sensitivity=sens,inverse_margin_shift=root('margin'),inverse_growth_shift=root('growth'),convert_principal_discounting_sensitivity_per_share=(2875-2875/(1+.0674)**4.85)/SHARES,remaining_dta_not_valued_book_upper_sensitivity_per_share=(1092.726-230)/SHARES,cost_of_capital=dict(rf=.0486,rf_date='2026-11-06',erp=.0441,erp_date='2026-11-01',observed_beta=1.35,ke=ke,kd_proxy=.0674,kd_date='2026-11-05',kd_source='FRED BB effective yield; financing proxy, not a current issuer quote',debt_weight=dw,mechanical_wacc=ke*(1-dw)+.0674*.78*dw,central_wacc=.105),approved_values=dict(fair_value=None,buy_max=None,adverse=None,central=None,favorable=None),stage3_approved=False,stage3_5_approved=False,entry_approved=False,gaps=['FY2026 full-year results not reported; model uses guidance and August balance, with post-balance buyback adjustment and explicit supplier-advance scenarios. Exact August-to-November bridge remains unknown.', 'Supplier advance amount, capacity productivity, cancellation exposure and incremental ROIC require calibration. Scenarios are not loss bounds.', 'Convert hedge offset is approximate: the filed hedge form excludes Indenture sections 14.04(g) and 14.03; make-whole/adjustment and counterparty mismatch are not fully valued. Warrants expire across 40 trading days beginning December 15, 2031; 5.19 years is an averaging proxy and volatility is assumed. Current ordinary dilution remains an August proxy.', 'Finite convert tax shield uses explicit proxies. Other deferred tax assets remain unvalued, not asserted worthless; tax-payable and finance-lease rollforwards require latest annual notes.', 'Unquoted investment fair value, current deferred-compensation matching, contingent liabilities and noncurrent claim splits remain partly judgmental.', 'Exact next primary earnings date unannounced. Annual discounting does not precisely model the November stub.'])
 for n in ['results.json','model_results.json']:(P/n).write_text(json.dumps(r,indent=2))
 print({k:(v['value_per_share'],v['warrant_claim'],v['terminal_weight']) for k,v in out.items()});print('inverse',r['inverse_margin_shift'],r['inverse_growth_shift'],'physical',r['physical_budget_only'])
if __name__=='__main__':main()
