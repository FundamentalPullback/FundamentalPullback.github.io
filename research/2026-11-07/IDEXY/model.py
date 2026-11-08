"""Controlled conditional FCFF export, EUR millions; not an approved investment value.
Leases treated as operating: cash rent retained, no duplicate lease-debt deduction.
"""
from pathlib import Path
import json,csv,copy
P=Path(__file__).resolve().parent
SALES=41262;SHARES=3116.652;FX=1.1165;ADR_RATIO=4;PRICE=16.41
BRIDGE={'cash_and_current_investments_july':10399,'november_dividend_already_exright':-2727,'operating_cash_reserve_assumed':-2500,'financial_debt':-1,'other_financial_liabilities':-32,'provisions_noncurrent_aggregate':-273,'tempe_annual_equity_book_proxy':399}
S={'adverso':dict(growth=[.025,.03,.03,.03,.03],m1=.17,m5=.17,mt=.17,wacc=.095,g=.02,roic=.25,rt=.20,maint=.042,gcap=.40,nwc=0,shock=400),
'central':dict(growth=[.065,.06,.055,.05,.045],m1=.195,m5=.20,mt=.20,wacc=.0825,g=.025,roic=.30,rt=.25,maint=.04,gcap=.35,nwc=-.05,shock=0),
'favorable':dict(growth=[.09,.085,.08,.07,.06],m1=.20,m5=.22,mt=.22,wacc=.0725,g=.03,roic=.40,rt=.30,maint=.038,gcap=.30,nwc=-.05,shock=0)}
def calc(s,override=None,physical_only=False):
 sales=SALES;rows=[];pv=0
 for y in range(1,12):
  anchor=s['growth'][-1] if override is None else override
  g=(s['growth'][y-1] if override is None else override) if y<=5 else anchor+(s['g']-anchor)*min(y-5,5)/5
  old=sales;sales*=1+g
  margin=s['m1']+(s['m5']-s['m1'])*min(y-1,4)/4 if y<=5 else s['m5']+(s['mt']-s['m5'])*min(y-5,5)/5
  ebit=sales*margin;nopat=ebit*.775;da=sales*.042
  maintenance=max(sales*s['maint'],1700*1.02**min(y,10)*(1+s['g'])**max(y-10,0));growthcap=max(0,sales-old)*s['gcap'];extra=200 if y==1 else 0
  capex=maintenance+growthcap+extra;wc=(sales-old)*s['nwc']+(s['shock'] if y==1 else 0)
  explicit=capex-da+wc;roic=s['roic']+(s['rt']-s['roic'])*min(max(0,y-5),5)/5
  reinvest=max(explicit,0) if physical_only else max(explicit,nopat*max(g,0)/roic)
  fcff=nopat-reinvest
  row=dict(year=y,sales=sales,growth=g,lease_adjusted_ebit_margin=margin,ebit_after_cash_rent=ebit,tax_rate=.225,nopat=nopat,nonlease_da=da,maintenance_capex=maintenance,growth_capex=growthcap,extra_corporate_capex=extra,total_capex=capex,delta_nwc=wc,explicit_net_reinvestment=explicit,roic=roic,net_reinvestment=reinvest,other_funded_capital=max(0,reinvest-explicit),fcff=fcff);rows.append(row)
  if y<=10:pv+=fcff/(1+s['wacc'])**y
 tv=rows[-1]['fcff']/(s['wacc']-s['g'])/(1+s['wacc'])**10;ev=pv+tv;eq=ev+sum(BRIDGE.values());v=eq/SHARES
 return dict(value_eur_ordinary=v,value_usd_adr=v*FX/ADR_RATIO,ev=ev,equity=eq,bridge=sum(BRIDGE.values()),explicit_pv=pv,terminal_pv=tv,terminal_weight=tv/ev,rows=rows)
def main():
 out={k:calc(s) for k,s in S.items()}
 for k,v in out.items():
  with (P/f'forecast_{k}.csv').open('w') as f:w=csv.DictWriter(f,fieldnames=v['rows'][0]);w.writeheader();w.writerows(v['rows'])
 lo,hi=-.05,.5
 for _ in range(100):
  m=(lo+hi)/2
  if calc(S['central'],m)['value_usd_adr']<PRICE:lo=m
  else:hi=m
 sens=[]
 for w in [.0725,.0825,.095]:
  for g in [.02,.025,.03]:
   s=copy.deepcopy(S['central']);s.update(wacc=w,g=g);sens.append(dict(wacc=w,g=g,value=calc(s)['value_usd_adr']))
 r=dict(ticker='IDEXY',date='2026-11-08',status='material_partial',quality='screen-grade',price=PRICE,price_date='2026-11-06',price_session='regular_OTC_close',fx=FX,fx_date='2026-11-06',adr_per_ordinary=4,shares_million=SHARES,share_basis='All issued ordinary shares, conservative allowance for current treasury shares to satisfy plans',bridge_items=BRIDGE,scenarios=out,sensitivity=sens,physical_only={k:calc(v,physical_only=True)['value_usd_adr'] for k,v in S.items()},inverse_first5_growth=(lo+hi)/2,cost_of_capital=dict(currency='EUR',rf=.0322,rf_source='German Finance Agency DE000BU2Z072 November6 reference quote',erp=.0441,erp_date="2026-11-01",erp_source_usd_rf=.0529,erp_cross_currency_transfer_unvalidated=True,beta_observed_adr=.93,mechanical_ke=.0322+.93*.0441,base_wacc=.0825,debt_weight_negligible=True,kd_assumed=.0422),approved_values=dict(fair_value=None,buy_max=None,adverse=None,central=None,favorable=None),stage3_approved=False,stage3_5_approved=False,entry_approved=False,gaps=['Current cash bridge after July omits unknown subsequent trading cash flow; known exright November dividend deducted.','Half-year right-of-use depreciation not separately disclosed; rental-adjusted starting earnings use annual nonlease depreciation calibration.','Store maintenance, technology replacement and growth capex split not certified; incremental ROIC assumptions remain conditional.','Tempe valued at annual book proxy; no stand-alone FCFE valuation, quarterly book rollforward incomplete.','ADR quote beta and fees do not provide a fully calibrated EUR operating beta; FX conversion is dated reference not executable settlement.'])
 for n in ['results.json','model_results.json']:(P/n).write_text(json.dumps(r,indent=2))
 print({k:{a:v[a] for a in ['value_eur_ordinary','value_usd_adr','terminal_weight']} for k,v in out.items()});print('inverse',r['inverse_first5_growth'],'physical',r['physical_only'])
if __name__=='__main__':main()
