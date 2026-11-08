"""EPAC: historia reconciliada y prueba inversa condicional financiada; no valoración aprobada.
USD millones. Datos primarios en sources; hipótesis explícitas, SFE proforma pendiente.
"""
import pathlib,json,csv
P=pathlib.Path(__file__).parent
A={2024:dict(revenue=589.5,ebit=121.6,ni_cont=82.2,ni_total=85.7,cfo_cont=84.,cfo_total=81.3,capex=11.4,da=13.3,sbc=10.9,amort=3.3,restructuring=7.4),2025:dict(revenue=616.9,ebit=133.5,ni_cont=92.7,ni_total=92.7,cfo_cont=111.3,cfo_total=111.3,capex=19.3,da=15.7,sbc=13.,amort=5.6,restructuring=5.9),2026:dict(revenue=652.3,ebit=129.2,ni_cont=89.7,ni_total=89.7,cfo_cont=130.2,cfo_total=130.2,capex=10.6,da=17.5,sbc=12.1,amort=6.3,restructuring=3.3)}
Y={2025:dict(revenue=449.385,ebit=93.633,ni_cont=64.668,cfo_cont=56.030,capex=16.360,da=10.706,sbc=9.525),2026:dict(revenue=466.568,ebit=94.877,ni_cont=65.238,cfo_cont=69.263,capex=9.241,da=13.133,sbc=9.394)}
Q={'2026Q1':dict(revenue=144.208,ebit=28.490,ni_cont=19.131,cfo_cont=15.976,capex=2.677,da=4.448,sbc=2.975),'2026Q2':dict(revenue=154.807,ebit=25.020,ni_cont=16.308,cfo_cont=29.027-15.976,capex=5.734-2.677,da=8.784-4.448,sbc=5.916-2.975),'2026Q3':dict(revenue=167.553,ebit=41.368,ni_cont=29.798,cfo_cont=69.263-29.027,capex=9.241-5.734,da=13.133-8.784,sbc=9.394-5.916),'2026Q4_derived_rounded':{k:A[2026][k]-Y[2026][k] for k in Y[2026]}}
T={y:{k:A[y-1][k]+Y[y][k]-Y[y-1][k] for k in Y[y]} for y in [2026]}
# Latest paired TTM at August fiscal year-end are FY2025 and FY2026, no stub arithmetic needed.
for d in [*A.values(),*Q.values(),*T.values()]:d.update(fcf_reported=d['cfo_cont']-d['capex'],op_margin=d['ebit']/d['revenue'])
price=38.83;basic=51.305685;legacy_dilution_proxy=.4;inducement_plan_capacity=.621622;shares=basic+legacy_dilution_proxy+inducement_plan_capacity
net_debt_est=2.3*(154.3+44);gross_debt=300+312;cash_implied=gross_debt-net_debt_est
# Not a closing balance: issuer leverage estimate rounded and covenant-defined.
bridge=dict(post_close_gross_debt=612,issuer_leverage_estimate=2.3,reference_adjusted_ebitda=198.3,net_debt_proxy=net_debt_est,cash_implied_not_verified=cash_implied,operating_cash_assumption=.02*(835+170/6),legacy_pension_opeb_serp=0.4+1.1+1.4+.6,unfunded_deferred_comp=4.5,sfe_other_claims=None,ppa=None,closing_adjustments=None)
netclaims=net_debt_est+bridge['operating_cash_assumption']+bridge['legacy_pension_opeb_serp']+4.5
rf=.0486;erp=.0441;beta_observed=.81;beta_test=1.2;ke=rf+beta_test*erp;kd=.06;dw=612/(price*basic+612);wacc=ke*(1-dw)+kd*.75*dw
# Inverse only: EBITA cash-tax proxy deliberately gives no PPA amortization tax shield.
# Missing SFE physical depreciation, NWC, capex and taxes prevent certification.
# Scenarios are funding stress tests, not company forecasts or fair-value cases.
base_nwc=113+70.7-42.8+.22*170
parameters={'prudente':dict(growth=.03,wacc=.10,capex=.03,nwc=.26,gt=.02,roic=.12),'intermedio':dict(growth=.05,wacc=.09,capex=.025,nwc=.24,gt=.025,roic=.15),'expansivo':dict(growth=.07,wacc=.08,capex=.025,nwc=.22,gt=.03,roic=.18)}
def run(p,margin):
 r=835.+170/6;wc=base_nwc;rows=[];pv=0;rr5=None
 for y in range(1,11):
  if y>1:
   g=p['growth'] if y<=5 else p['growth']+(p['gt']-p['growth'])*(y-5)/5
   r=r*(1+g) # SFE calendarization already in initial 12-month run-rate proxy; do not add again
  tax=.25;ebita=r*margin;nopat=ebita*(1-tax);dep=.02*r;capex=p['capex']*r;newwc=p['nwc']*r;deltawc=newwc-wc;wc=newwc
  integration=12*(1-tax) if y==1 else 0 # midpoint known $10-14m integration budget, assumed year1
  raw_reinvestment=capex-dep+deltawc
  if y<=5:reinvest=raw_reinvestment;rr5=reinvest/nopat
  else:
   f=(y-5)/5;reinvest=max(raw_reinvestment,nopat*(rr5*(1-f)+(p['gt']/p['roic'])*f))
  supplemental_reinvestment=reinvest-raw_reinvestment
  fcff=nopat-reinvest-integration;discount=(1+p['wacc'])**y;pv+=fcff/discount
  rows.append(dict(year=y,revenue=r,ebita_margin=margin,ebita=ebita,cash_tax_proxy=tax,nopat_proxy=nopat,physical_depreciation_assumption=dep,capex=capex,selected_nwc=wc,delta_nwc=deltawc,raw_reinvestment=raw_reinvestment,supplemental_reinvestment=supplemental_reinvestment,net_reinvestment=reinvest,integration_after_tax=integration,conditional_fcff=fcff,pv=fcff/discount))
 tn=rows[-1]['nopat_proxy']*(1+p['gt']);terminal_physical_floor=r*(1+p['gt'])*(p['capex']-.02)+r*p['gt']*p['nwc'];tr=max(terminal_physical_floor,tn*p['gt']/p['roic']);tf=tn-tr;pvt=tf/(p['wacc']-p['gt'])/(1+p['wacc'])**10;ev=pv+pvt
 return dict(parameters=p,required_ebita_margin=margin,rows=rows,terminal_nopat_proxy=tn,terminal_physical_floor=terminal_physical_floor,terminal_roic_effective=tn*p['gt']/tr,terminal_reinvestment=tr,terminal_fcff=tf,terminal_pv=pvt,terminal_weight=pvt/ev,enterprise_hurdle=ev,equity_hurdle=ev-netclaims,implied_price_check=(ev-netclaims)/shares)
inverses={}
for name,p in parameters.items():
 lo,hi=.01,.6
 for _ in range(100):
  mid=(lo+hi)/2
  if run(p,mid)['implied_price_check']<price:lo=mid
  else:hi=mid
 inverses[name]=run(p,(lo+hi)/2)
O=dict(ticker='EPAC',as_of='2026-11-08',status='partial_post_acquisition_perimeter',research_threshold=65,research_eligible=True,stage3_completed=False,stage35_approved=False,approved_values=None,approved_price=None,price=dict(regular_close=price,date='2026-11-06',session='16:00 America/New_York',scanner_last=39.54,scanner_date='2026-11-05',opportunity=80),annual=A,quarters=Q,paired_ttm_latest={'2025-08-31':A[2025],'2026-08-31':A[2026]},supplementary_ttm_2026q3=T[2026],quarter_precision='Q4 derived from rounded annual minus precise interim; do not mistake for exact filed quarterly amounts',bridge=bridge,conditional_net_claims=netclaims,share_denominator=dict(basic_oct26=basic,legacy_dilution_proxy=legacy_dilution_proxy,inducement_capacity_not_actual_grants=inducement_plan_capacity,conservative_sensitivity_denominator=shares),capital_cost=dict(rf=rf,rf_date='2026-11-06 primary Treasury table independently verified',erp=erp,erp_date='2026-11-01 Damodaran',erp_source_rf=.0529,historical_beta=beta_observed,source='StockAnalysis Nov6',mechanical_ke=rf+erp*beta_observed,scenario_beta=beta_test,scenario_ke=ke,kd_assumed=kd,gross_debt_weight=dw,wacc_illustrative=wacc,warning='Historical beta predates SFE; debt market value approximated by principal; 6% Kd is assumption not live SOFR quotation'),inverse_tests=inverses,initial_revenue_proxy=835+170/6,forecast_time_basis='Year1 next12-month run-rate approximation: FY2027 guide midpoint plus two SFE months; not issuer NTM guidance, no exact fiscal-stub reconciliation',valuation_cases=None,legacy_roic_proxy=.75*129.2/((433.7+189.7-151.6+453.1+182.3-174.7)/2),unresolved=['SFE audited financial statements and SEC pro forma expressly deferred in closing 8-K; no amendment found as of Nov8','SFE NWC, physical depreciation, replacement capex/software and cash tax not reconciled','PPA and actual acquisition amortization/tax shields unavailable','Closing cash/net-debt adjustments and SFE other claims not finalized','Actual inducement units and vesting/performance outcomes not reconciled; plan capacity used only as sensitivity'])
(P/'results.json').write_text(json.dumps(O,indent=2,ensure_ascii=False))
fields=['revenue','ebit','ni_cont','cfo_cont','capex','fcf_reported','da','sbc','op_margin']
with (P/'financial_history.csv').open('w') as f:
 w=csv.writer(f);w.writerow(['period']+fields)
 for name,d in [(f'FY{k}',v) for k,v in A.items()]+list(Q.items())+[(f'TTM_Aug{k}',A[k]) for k in [2025,2026]]:w.writerow([name]+[d.get(k) for k in fields])
assert all(abs(sum(v[k] for v in Q.values())-A[2026][k])<.002 for k in Y[2026])
assert all(abs(v['implied_price_check']-price)<1e-8 for v in inverses.values())
assert all(r['net_reinvestment']>0 for v in inverses.values() for r in v['rows'])
print(json.dumps({'netclaims':netclaims,'shares':shares,'wacc':wacc,'inverse':{k:dict(margin=v['required_ebita_margin'],terminal_weight=v['terminal_weight']) for k,v in inverses.items()}},indent=2))

assert all(a['net_reinvestment']+1e-9>=a['raw_reinvestment'] for z in inverses.values() for a in z['rows'])
assert all(abs(z['terminal_fcff']-z['rows'][-1]['conditional_fcff']*(1+z['parameters']['gt']))<1e-7 for z in inverses.values())
