"""Conditional research model, USDm/ADS. Public sources only. No approved valuation.
Royalty, licensing and silicon separated. GAAP-like margins retain SBC and R&D.
Capitalized licensed IP/EDA replacement is separate from expensed engineering.
Scenario margins describe the physical-budget baseline. Incremental ROIC capital
incurs matched depreciation/amortization expense, not a free additional addback.
"""
from pathlib import Path
import json,csv,copy
P=Path(__file__).resolve().parent
PRICE=174.62; SHARES=1080 # 1070 September actual +10 Q2 incremental, proxy not all 23m unvested added again
BASE_ROYALTY=2793;BASE_LICENSE=2671
# Long-term contract assets included; tax and payroll withholding claims excluded from operating NWC.
NWC=1086+1014+436+220+107-195-680-142-170-56
BRIDGE={'cash_short_investments':3621,'operating_cash_reserve':-650,'finance_lease_proxy':-36,'EDA_financing_existing':-130,'current_tax_liability':-114,'employee_withholding_payables':-185,'noncurrent_compensation':-33,'other_noncurrent_liabilities_ex_finance_proxy':-35}
S={
'adverso':dict(rg=[.08,.10,.10,.08,.06],lg=[.10,.04,.02,.04,.04],sil=[100,350,600,750,900],m1=.14,m5=.20,mt=.20,sm=.08,tax=.27,wacc=.20,g=.025,nwc=.38,snwc=.40,maint=.055,capacity=.22,ip=.025,roic=.20,rt=.15,claims=400,invest=200),
'central':dict(rg=[.18,.24,.25,.22,.18],lg=[.22,.15,.15,.12,.10],sil=[300,1700,2500,4000,5500],m1=.20,m5=.30,mt=.32,sm=.20,tax=.25,wacc=.14,g=.03,nwc=.32,snwc=.30,maint=.045,capacity=.18,ip=.022,roic=.30,rt=.25,claims=200,invest=400),
'favorable':dict(rg=[.28,.35,.35,.30,.25],lg=[.30,.25,.23,.20,.18],sil=[500,2000,4000,6500,9000],m1=.24,m5=.38,mt=.40,sm=.28,tax=.22,wacc=.11,g=.035,nwc=.27,snwc=.24,maint=.035,capacity=.14,ip=.018,roic=.45,rt=.35,claims=75,invest=599)}
def calc(s,gs=0,ms=0,floor=True,tail_years=300):
 r=BASE_ROYALTY;l=BASE_LICENSE;sil=0;nwc=NWC;gross=1600;basegross=1600;ipstock=385;pv=tail=0;rows=[]
 for y in range(1,11+tail_years):
  old=r+l+sil;oldip=r+l
  rg=s['rg'][y-1] if y<=5 else s['rg'][-1]+(s['g']-s['rg'][-1])*min(y-5,5)/5
  lg=s['lg'][y-1] if y<=5 else s['lg'][-1]+(s['g']-s['lg'][-1])*min(y-5,5)/5
  shift=gs*max(0,(10-y)/8) if y>=2 else 0;r*=1+rg+shift;l*=1+lg+shift
  sil=s['sil'][y-1] if y<=5 else sil*(1+(.20+(s['g']-.20)*min(y-5,5)/5))
  sales=r+l+sil;g=sales/old-1
  m=s['m1']+(s['m5']-s['m1'])*min(y-1,4)/4 if y<=5 else s['m5']+(s['mt']-s['m5'])*min(y-5,5)/5
  m+=ms*min(y-1,4)/4;baseline_ebit=(r+l)*m+sil*s['sm'];incremental_da=(gross-basegross)*.12+(ipstock-385)*.25;ebit=baseline_ebit-incremental_da;nopat=ebit*(1-s['tax'])
  # DA excludes acquired IP from perpetual free addback: all purchased-IP stock receives renewal budget.
  da=gross*.12;amort=ipstock*.25;maintenance=max(sales*s['maint'],1.05*da);capacity=max(0,sales-old)*s['capacity']
  iprenew=max(sales*s['ip'],amort);target=(r+l)*s['nwc']+sil*s['snwc'];wc=target-nwc;nwc=target
  advance=200 if y==1 else 0 # known new advance, no second subtraction in bridge and no automatic terminal release
  explicit=maintenance+capacity+iprenew-da-amort+wc+advance
  roic=s['roic']+(s['rt']-s['roic'])*min(max(y-5,0),5)/5;funding=nopat*max(0,g)/roic
  extra=max(0,funding-explicit) if floor else 0
  # Conditional allocation to owned compute capacity and externally purchased tools/IP, not expensed R&D.
  capex=maintenance+capacity+.6*extra;ipbuy=iprenew+.4*extra;reinv=capex+ipbuy-da-amort+wc+advance;fcff=nopat-reinv
  gross+=capacity+.6*extra;basegross+=capacity;ipstock+=.4*extra
  row=dict(year=y,royalty=r,license=l,silicon=sil,sales=sales,growth=g,ip_operating_margin=m,silicon_operating_margin=s['sm'],baseline_ebit=baseline_ebit,incremental_da_expense=incremental_da,ebit=ebit,nopat=nopat,physical_da=da,ip_amortization=amort,maintenance=maintenance,growth_capacity=capacity,additional_funded_capital=extra,capex=capex,purchased_ip=ipbuy,nwc=target,delta_nwc=wc,supplier_advance=advance,roic=roic,reinvestment_floor=funding,reinvestment=reinv,fcff=fcff)
  if y<=11:rows.append(row)
  if y<=10:pv+=fcff/(1+s['wacc'])**y
  else:tail+=fcff/(1+s['wacc'])**y
 rem=fcff*(1+s['g'])/(s['wacc']-s['g'])/(1+s['wacc'])**(10+tail_years);tail+=rem;ev=pv+tail;bridge=sum(BRIDGE.values())+s['invest']-s['claims']
 return dict(value_per_share=(ev+bridge)/SHARES,enterprise_value=ev,equity_value=ev+bridge,bridge=bridge,terminal_weight=tail/ev,terminal_remainder_pv=rem,calibration_validated=False,terminal_pv=tail,explicit_pv=pv,rows=rows)
def inverse(kind):
 lo,hi=(0,5) if kind=='margin' else (0,2)
 def f(x):return calc(S['central'],ms=x if kind=='margin' else 0,gs=x if kind=='growth' else 0)['value_per_share']
 if not f(lo)<=PRICE<=f(hi):return None
 for _ in range(80):
  m=(lo+hi)/2
  if f(m)<PRICE:lo=m
  else:hi=m
 return (lo+hi)/2

def main():
 scenarios={k:calc(s) for k,s in S.items()}
 for k,v in scenarios.items():
  with (P/f'forecast_{k}.csv').open('w') as f:w=csv.DictWriter(f,fieldnames=v['rows'][0]);w.writeheader();w.writerows(v['rows'])
 ke=.0486+3.94*.0441;s=copy.deepcopy(S['central']);s['wacc']=ke
 result=dict(ticker='ARM',as_of='2026-11-08',status='material_partial',quality='screen-grade',price=PRICE,price_date='2026-11-06',price_session='regular_close',ads_ratio=1,shares_actual=1070,shares_date='2026-09-30',shares_model=SHARES,opening_nwc=NWC,base_royalty=BASE_ROYALTY,base_license=BASE_LICENSE,bridge_items=BRIDGE,scenarios=scenarios,physical_budget_only={k:calc(s,floor=False)['value_per_share'] for k,s in S.items()},inverse_margin_shift=inverse('margin'),inverse_growth_shift=inverse('growth'),cost_of_capital=dict(rf=.0486,rf_date='2026-11-06',erp=.0441,erp_date='2026-11-01',observed_beta=3.94,ke_observed=ke,observed_ke_central_case=calc(s)['value_per_share'],central_wacc=.14,normalized_beta_implied=(.14-.0486)/.0441,normalization_validated=False,kd_current=None,debt_weight_assumption=0,lease_historical_rate=.0507),approved_values=dict(fair_value=None,buy_max=None,adverse=None,central=None,favorable=None),entry_approved=False,stage3_approved=False,stage3_5_approved=False,next_earnings='2027-02-03',gaps=['Silicon versus IP standalone costs, margin and capital conversion not yet reported; scenarios are hypotheses, not management guidance.', 'Supplier minimum-volume and quarterly price economics, recovery of advances, agency timing/counterparty exposure and liability overlap are not bounded.', 'Replacement compute/IP mix, incremental ROIC and margin improvement require calibration; expensed R&D is retained, no artificial capitalization.', 'Normalized beta is not validated against a sufficiently long listing or peer regression; observed beta implies Ke22.2354%.', 'September share/claim bridge to November, existing award dilution versus future SBC overlap, finance lease rollforward and tax contingency netting are incomplete.', 'Investment realization and unresolved Qualcomm bench rulings have no reliable bounded current valuation; explicit reserves are assumptions not claims estimates.'])
 (P/'results.json').write_text(json.dumps(result,indent=2));(P/'model_results.json').write_text(json.dumps(result,indent=2));print({k:v['value_per_share'] for k,v in scenarios.items()});print('inverse',result['inverse_margin_shift'],result['inverse_growth_shift'])
if __name__=='__main__':main()
