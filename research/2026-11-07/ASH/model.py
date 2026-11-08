"""Conditional FCFF in USD millions. Claims and current portions are explicit proxies.
Restricted trusts offset designated claims only, never added as excess cash separately.
"""
from pathlib import Path
import json,csv,copy,math
P=Path(__file__).resolve().parent
PRICE=76.62;SHARES=46;SALES=1863
# Gross trust rollforward: prior347 + contributions9 + return21 - reimbursements74 =303.
BRIDGE={'cash':480,'operating_cash_reserve':-125,'debt_principal_proxy':-1377,'asbestos_noncurrent_current_proxy':-(385+46),'environment_june_gross':-231,'restricted_trusts_derived':303,'asbestos_insurance_gross_proxy':154,'environment_insurance_june':13,'employee_benefits_including_current_proxy':-88,'unrecognized_tax_benefits_june':-66,'tax_interest_penalties_annual':-19,'transition_tax_annual_proxy':-13,'restructuring_unpaid_proxy':-10,'equity_options_reserve_proxy':-25}
S={'adverso':dict(growth=[.01,.015,.02,.025,.025],margin1=.13,margin5=.14,wacc=.10,g=.02,roic=.12,rt=.10,maint=.07,gcap=.20,nwc=.30,ip=.005,claims_extra=120,insurance_haircut=.25,factoring_unwind=180),
'central':dict(growth=[1940/1863-1,.045,.04,.035,.03],margin1=.152,margin5=.18,wacc=.09,g=.025,roic=.16,rt=.14,maint=.064,gcap=.15,nwc=.25,ip=.004,claims_extra=60,insurance_haircut=.10,factoring_unwind=90),
'favorable':dict(growth=[.06,.06,.055,.05,.045],margin1=.16,margin5=.21,wacc=.08,g=.03,roic=.20,rt=.18,maint=.062,gcap=.15,nwc=.22,ip=.004,claims_extra=25,insurance_haircut=0,factoring_unwind=0)}
def calc(s,override_margin=None,physical_only=False):
 sales=SALES;pv=0;rows=[]
 for y in range(1,12):
  gr=s['growth'][y-1] if y<=5 else s['growth'][-1]+(s['g']-s['growth'][-1])*min(y-5,5)/5
  old=sales;sales*=1+gr;mt=s['margin5'] if override_margin is None else override_margin;mar=s['margin1']+(mt-s['margin1'])*min(y-1,4)/4
  ebita=sales*mar;nopat=ebita*.74;da=sales*.067;maintenance=max(sales*s['maint'],125*1.02**min(y,10)*(1+s['g'])**max(y-10,0));growthcap=max(0,sales-old)*s['gcap'];capex=maintenance+growthcap;wc=(sales-old)*s['nwc'];ip=sales*s['ip'];roic=s['roic']+(s['rt']-s['roic'])*min(max(y-5,0),5)/5
  explicit=capex-da+wc+ip;reinv=max(explicit,0) if physical_only else max(explicit,nopat*max(gr,0)/roic)
  # Factoring normalization is incremental to organic working capital, spread over3years.
  unwind=s['factoring_unwind']/3 if y<=3 else 0;fcff=nopat-reinv-unwind
  row=dict(year=y,sales=sales,growth=gr,cash_ebita_margin=mar,cash_ebita=ebita,nopat=nopat,physical_da=da,maintenance_capex=maintenance,growth_capex=growthcap,capex=capex,delta_nwc=wc,incremental_intangible_budget=ip,explicit_reinvestment=explicit,roic=roic,reinvestment=reinv,factoring_normalization=unwind,other_funded_capital=max(0,reinv-explicit),fcff=fcff);rows.append(row)
  if y<=10:pv+=fcff/(1+s['wacc'])**y
 tv=rows[-1]['fcff']/(s['wacc']-s['g'])/(1+s['wacc'])**10;ev=pv+tv;bridge=sum(BRIDGE.values())-s['claims_extra']-167*s['insurance_haircut'];eq=ev+bridge
 return dict(value_per_share=eq/SHARES,enterprise_value=ev,equity_value=eq,bridge=bridge,terminal_pv=tv,explicit_pv=pv,terminal_weight=tv/ev,rows=rows)
def main():
 out={k:calc(s) for k,s in S.items()}
 for k,v in out.items():
  with (P/f'forecast_{k}.csv').open('w') as f:w=csv.DictWriter(f,fieldnames=v['rows'][0]);w.writeheader();w.writerows(v['rows'])
 lo,hi=.05,.6
 for _ in range(100):
  m=(lo+hi)/2
  if calc(S['central'],m)['value_per_share']<PRICE:lo=m
  else:hi=m
 sens=[]
 for w in [.08,.09,.10]:
  for g in [.02,.025,.03]:
   s=copy.deepcopy(S['central']);s.update(wacc=w,g=g);sens.append(dict(wacc=w,g=g,value=calc(s)['value_per_share']))
 ke=.0486+.36*.0441;normalized=.0486+1*.0441;dw=1377/(1377+PRICE*SHARES)
 r=dict(ticker='ASH',date='2026-11-08',status='material_partial',quality='screen-grade',price=PRICE,price_date='2026-11-06',price_session='regular_close',shares=SHARES,bridge_items=BRIDGE,scenarios=out,physical_only={k:calc(s,physical_only=True)['value_per_share'] for k,s in S.items()},sensitivity=sens,inverse_mature_cash_ebita_margin=(lo+hi)/2,approved_values=dict(fair_value=None,buy_max=None,adverse=None,central=None,favorable=None),stage3_approved=False,stage3_5_approved=False,entry_approved=False,cost_of_capital=dict(rf=.0486,rf_date='2026-11-06',erp=.0441,erp_date='2026-11-01',erp_source_rf=.0529,date_basis_mismatch=True,observed_beta=.36,observed_ke=ke,normalized_beta_assumed=1,normalized_ke=normalized,marginal_kd_assumed=.0636,debt_weight=dw,observed_beta_mechanical_wacc=ke*(1-dw)+.0636*.74*dw,normalized_mechanical_wacc=normalized*(1-dw)+.0636*.74*dw,base_wacc=.09),gaps=['FY2026 release preliminary; audited footnotes not yet filed. Gross September asbestos/current insurance and environmental balances use explicit latest-note proxies.','Restricted trust303 derived rollforward requires annual-note confirmation and allocation between trusts; not excess cash.','Legacy loss tails, insurance recovery and asbestos estimation horizon remain uncertain; buffers not proven bounds.','Maintenance/productivity and long-run incremental ROIC calibration; Hopewell execution not proven by guidance.','Current options/warrants economically nonzero but exact composition/tenor not valued; explicit25 reserve proxy and46m diluted shares.','Factoring normalization and September closing balances incomplete; next primary earnings date unannounced.'])
 r['gaps'] += ['Annual discounting does not include a precise November valuation stub.', 'Incremental intangible budget assumes no overlap with expensed R&D or physical capex; the primary split does not validate this assumption.', 'Current restructuring, tax and benefit claims use explicit stale or judgmental proxies, not verified September balances; possible overlap must be reconciled.', 'Marginal debt cost is assumed, not a verified current bond yield.']
 for n in ['results.json','model_results.json']:(P/n).write_text(json.dumps(r,indent=2))
 print({k:{a:v[a] for a in ['value_per_share','enterprise_value','terminal_weight']} for k,v in out.items()});print('inverse',r['inverse_mature_cash_ebita_margin'],'physical',r['physical_only'],'capital',r['cost_of_capital'])
if __name__=='__main__':main()
