"""Conditional standalone equipment FCFF plus quoted 27% Rigaku stake. USDm.
June balance rolled for August purchase, not a September balance. R&D/SBC remain expensed.
Scenario margins apply to physical-budget baseline; extra ROIC-capital depreciation
is expensed before NOPAT as well as added back in cashflow.
Zero-coupon convert is not free equity; residual option above capped-call cap has time value.
"""
from pathlib import Path
import json,csv,copy,math
P=Path(__file__).resolve().parent
PRICE=173.28;SHARES=49.074247+.270;BASE=1120.137
NWC=337.384+379.243+43.164-139.430-55.286-44.592
RIGAKU_SHARES=61.123436;RIGAKU_PRICE=1155;FX=158.48;RIGAKU=RIGAKU_SHARES*RIGAKU_PRICE/FX
BRIDGE={'cash_and_marketable_securities_june':1882.150,'rigaku_purchase_august':-720,'operating_cash_reserve_assumption':-150,'convert_face':-1500,'current_income_tax_proxy':-5.256,'unrecognized_tax_including_interest_proxy':-9.037,'unpaid_buyback_excise':-2.050,'unpaid_debt_issuance_costs':-1.941,'unpaid_bridge_fees':-.678,'nonmarketable_equity_selected_proxy':8}
S={'adverso':dict(growth=[.10,-.15,.03,.06,.05],m1=.19,m5=.21,mt=.20,tax=.24,wacc=.13,g=.02,nwc=.50,maint=.035,capacity=.22,roic=.20,rt=.15,claims=75,sigma=.65,stake=.75,shield=10),
'central':dict(growth=[.30,.20,.15,.12,.10],m1=.26,m5=.29,mt=.26,tax=.22,wacc=.1125,g=.025,nwc=.44,maint=.03,capacity=.18,roic=.30,rt=.25,claims=35,sigma=.50,stake=.90,shield=18),
'favorable':dict(growth=[.45,.30,.25,.20,.15],m1=.29,m5=.35,mt=.32,tax=.20,wacc=.10,g=.03,nwc=.38,maint=.025,capacity=.14,roic=.45,rt=.35,claims=15,sigma=.40,stake=1,shield=23)}
def call(spot,strike,t,sigma,r=.0486):
 n=lambda x:(1+math.erf(x/math.sqrt(2)))/2;d1=(math.log(spot/strike)+(r+.5*sigma*sigma)*t)/(sigma*math.sqrt(t));d2=d1-sigma*math.sqrt(t)
 return spot*n(d1)-strike*math.exp(-r*t)*n(d2)
def calc(s,ms=0,gs=0,physical_only=False,tail_years=300):
 sales=BASE;nwc=NWC;gross=217.806;basegross=217.806;pv=tail=0;rows=[]
 for y in range(1,11+tail_years):
  g=s['growth'][y-1] if y<=5 else s['growth'][-1]+(s['g']-s['growth'][-1])*min(y-5,5)/5
  if 2<=y<=10:g+=gs*(10-y)/8
  old=sales;sales*=1+g;m=s['m1']+(s['m5']-s['m1'])*min(y-1,4)/4 if y<=5 else s['m5']+(s['mt']-s['m5'])*min(y-5,5)/5;m+=ms*min(y-1,4)/4
  incremental_da=(gross-basegross)*.105;ebit=sales*m-incremental_da;nopat=ebit*(1-s['tax']);da=gross*.105;maint=max(sales*s['maint'],da*1.05);growthcap=max(0,sales-old)*s['capacity'];target=sales*s['nwc'];wc=target-nwc;nwc=target
  unrecovered=max(0,-wc)*.35;wc+=unrecovered
  explicit=maint+growthcap-da+wc;roic=s['roic']+(s['rt']-s['roic'])*min(max(y-5,0),5)/5;floor=nopat*max(g,0)/roic;extra=0 if physical_only else max(0,floor-explicit)
  capex=maint+growthcap+extra;reinv=capex-da+wc;fcff=nopat-reinv;gross+=growthcap+extra;basegross+=growthcap
  row=dict(year=y,sales=sales,growth=g,cash_ebita_margin=m,incremental_da_expense=incremental_da,ebit=ebit,nopat=nopat,physical_da=da,replacement_capex=maint,growth_capex=growthcap,additional_capacity_capex=extra,capex=capex,delta_nwc=wc,nwc_target=target,unrecovered_inventory_cash=unrecovered,roic=roic,reinvestment_floor=floor,reinvestment=reinv,fcff=fcff,gross_physical_assets=gross)
  if y<=11:rows.append(row)
  if y<=10:pv+=fcff/(1+s['wacc'])**y
  else:tail+=fcff/(1+s['wacc'])**y
 rem=fcff*(1+s['g'])/(s['wacc']-s['g'])/(1+s['wacc'])**(10+tail_years);tail+=rem;ev=pv+tail
 residual=3.9288*call(PRICE,509.06,4.57,s['sigma']);stake=RIGAKU*s['stake'];bridge=sum(BRIDGE.values())+stake-residual-s['claims']+s['shield']
 return dict(value_per_share=(ev+bridge)/SHARES,enterprise_value=ev,equity_value=ev+bridge,bridge=bridge,rigaku_stake_value=stake,residual_convert_option_claim=residual,finite_tax_shield=s['shield'],calibration_validated=False,terminal_remainder_pv=rem,terminal_weight=tail/ev,terminal_pv=tail,explicit_pv=pv,rows=rows)
def inverse(kind):
 lo,hi=(0,2) if kind=='margin' else (0,1)
 def f(x):return calc(S['central'],ms=x if kind=='margin' else 0,gs=x if kind=='growth' else 0)['value_per_share']
 if not f(lo)<=PRICE<=f(hi):return None
 for _ in range(90):
  m=(lo+hi)/2
  if f(m)<PRICE:lo=m
  else:hi=m
 return (lo+hi)/2

def main():
 out={k:calc(s) for k,s in S.items()}
 for k,v in out.items():
  with (P/f'forecast_{k}.csv').open('w') as f:w=csv.DictWriter(f,fieldnames=v['rows'][0]);w.writeheader();w.writerows(v['rows'])
 ke=.0486+1.68*.0441;dw=1500/(1500+PRICE*49.074247)
 sensitivity=[]
 for w in [.10,.1125,.13]:
  for g in [.02,.025,.03]:
   s=copy.deepcopy(S['central']);s.update(wacc=w,g=g);sensitivity.append(dict(wacc=w,g=g,value=calc(s)['value_per_share']))
 r=dict(ticker='ONTO',as_of='2026-11-08',status='material_partial_with_current_stage1_gate',price=PRICE,price_date='2026-11-06',price_session='regular_close',current_stage1=dict(high_252_proxy=386.46,high_date_public_quote=None,high_basis='published52weekhigh; exact252sessionadjustedseriesnotvalidated',pullback=1-PRICE/386.46,pullback_max=.50,proxy_pullback_gate_failed=True,pullback_gate_failed=None,reported_earnings_positive=True,full_technical_clearance=False),shares_actual=49.074247,shares_date='2026-07-31',shares_model=SHARES,base_sales=BASE,base_status='June TTM includes different fiscal week lengths and partial Semilab perimeter',opening_nwc=NWC,bridge_items=BRIDGE,rigaku_mark=dict(shares_m=RIGAKU_SHARES,jpy_close=RIGAKU_PRICE,fx_jpy_per_usd=FX,date='2026-11-06',gross_usdm=RIGAKU,note='Tokyo equity close and later FX daily close not synchronized; block liquidity/control/restrictions adjustment hypothetical'),scenarios=out,physical_budget_only={k:calc(s,physical_only=True)['value_per_share'] for k,s in S.items()},sensitivity=sensitivity,inverse_margin_shift=inverse('margin'),inverse_growth_shift=inverse('growth'),cost_of_capital=dict(rf=.0486,rf_date='2026-11-06',erp=.0441,erp_date='2026-11-01',observed_beta=1.68,ke=ke,kd_proxy=.0674,kd_date='2026-11-05',kd_source='FRED BB yield proxy; issuer rating not asserted',debt_weight=dw,mechanical_wacc=ke*(1-dw)+.0674*.78*dw,central_wacc=.1125),next_earnings='2026-11-09',event_time='16:30 America/New_York',approved_values=dict(fair_value=None,buy_max=None,adverse=None,central=None,favorable=None),stage3_approved=False,stage3_5_approved=False,entry_approved=False,gaps=['Tomorrow November9 earnings and September balance pending; June-to-November bridge only adjusts known Rigaku purchase, not unreported operating cash or buybacks.', 'Normalized capacity, marginal ROIC and maintenance versus growth allocation are conditional; acquired IP renewal is retained in expensed engineering/marketing, no duplicate capitalization.', 'Current supplier commitments, backlog cancellation/acceptance and remaining-performance disclosure are not interchangeable; no claimed cash conversion of $1bn backlog.', 'Convert residual option valuation uses assumed volatility and approximate hedge offset; filed hedge excludes Indenture5.06/5.07. Makewhole/early conversion and counterparty risk not fully priced.', 'Rigaku marked stake includes scenario liquidity discounts, not independently appraised economic value; exact transfer rights/FX settlement and realization costs uncertain.', 'Current tax/noncurrent claim splits and existing award dilution remain partly stale; explicit contingency reserves are not maximum-loss bounds.'])
 for n in ['results.json','model_results.json']:(P/n).write_text(json.dumps(r,indent=2))
 print({k:v['value_per_share'] for k,v in out.items()});print('inverse',r['inverse_margin_shift'],r['inverse_growth_shift'],'rigaku',RIGAKU)
if __name__=='__main__':main()
