"""Controlled diagnostic FCFF, not an approved fair value. USD millions.
Primary base: 2025 10K and 2026 Q3 10Q. All forward economics are analyst stress assumptions.
No pasted/private contrast values used. Lease operating costs remain in EBIT; no second lease debt subtraction.
"""
import json,csv
from pathlib import Path
P=Path(__file__).parent
S=657.912380+4 # actual issued outstanding plus Q3 dilutive instruments proxy; NOT certified fully diluted spot.
price=87.20; E=price*657.912380; D=11900+746+1100 # debt fair value + finance leases book + fuel card
rf=.0486; erp=.0441; tax=.25
beta=.76*(1+(1-tax)*D/E)
kd=rf+.0125 # 10y Treasury + latest SkyMiles floating spread: diagnostic maturity/security mismatch disclosed
wacc=(rf+beta*erp)*E/(E+D)+kd*(1-tax)*D/(E+D)
# Earnings perimeter removes third-party refinery sales; refinery EBIT separate to avoid sales denominator distortion.
base_rev=58287+49451-43681
base_air_ebit=5665+3541-4313
# Reported gross assets; replacement uplift and economic lives are deliberately sensitivities, not company estimates.
assets={'flight':47981+1185,'ground':11165,'IT':3167}
# Net PPE bridge uses reported values; residual captures disposals/reclassifications and mixed DA scope.
asset_bridge={'PPE_2025':39743,'cash_additions_9M':4071,'finance_lease_non_cash_additions':79,'operating_to_finance_lease_transfers':562,'reported_DA_9M':1964,'PPE_2026_09':42206}
asset_bridge.update({'gross_PPE_2025':64462,'gross_PPE_2026_09':68575,'advance_payments_2025':964,'gross_change':4113,'gross_residual_after_cash_and_noncash_additions':-599})
asset_bridge['unallocated_net_residual']=42206-(39743+4071+79+562-1964)
# Valuation date Nov6, after 37/92 days of Q4. Actual Oct-Nov6 cash not reported.
# Explicit uniform-Q4 accrual/cash allocation assumption, not actual results.
stub_fraction_remaining=55/92; stub_discount_years=55/365
q4_revenue=14606*1.20 # Oct9 company guidance ~20% growth; includes loyalty/MRO, excludes refinery external sales
fy2026_revenue=49451+q4_revenue
commit=[4930,4730,5040,2720]+[8380/5]*5+[0] # 2027-36; post2030 timing is only a scenario allocation
scenarios={'adverso':dict(capacity=.00,price_growth=.015,margin=.065,refinery=-100,uplift=1.8,life=28,discount=wacc+.025,advance_increase_9M=0,q4_margin=.07,q4_flight_cash=1250,q4_ground_cash=300,q4_retired=0),
'central_diagnostico':dict(capacity=.015,price_growth=.025,margin=.095,refinery=150,uplift=1.5,life=30,discount=wacc+.01,advance_increase_9M=500,q4_margin=.08,q4_flight_cash=1100,q4_ground_cash=250,q4_retired=250),
'favorable':dict(capacity=.025,price_growth=.025,margin=.12,refinery=300,uplift=1.2,life=34,discount=wacc,advance_increase_9M=1000,q4_margin=.09,q4_flight_cash=910,q4_ground_cash=209,q4_retired=500)}
results={}
def run(c,margin_override=None):
 # Gross asset allocation is explicitly conditional because filings do not disclose gross disposals or advance movement at Q3.
 flight_sep=assets['flight']+3444+79+562-599-c['advance_increase_9M']
 ground_sep=assets['ground']+627*.7;it_sep=assets['IT']+627*.3 # 30% IT allocation sensitivity assumption
 q4_flight=max(910,c['q4_flight_cash']);q4_ground=c['q4_ground_cash']
 q4_capex=q4_flight+q4_ground # includes refinery; do not add it twice
 q4_refinery_ebit=0 # no separate increment: Q4 guidance margin is consolidated adjusted, not airline standalone
 q4_ebit=q4_revenue*c['q4_margin']+q4_refinery_ebit; q4_da=673+28 # airline plus refinery segment DA latest-quarter run rate, assumption
 q4_nwc=.03*(q4_revenue-14606)
 q4_fcff=q4_ebit*(1-tax)+q4_da-q4_capex-q4_nwc
 stub_fcff=q4_fcff*stub_fraction_remaining
 rev=fy2026_revenue
 q4_advance=q4_flight*.25 # cash advance timing hypothesis; not expense or second capex
 gross=(flight_sep+q4_flight-q4_advance-c['q4_retired'])*c['uplift']
 ground=ground_sep+q4_ground*.7;it=it_sep+q4_ground*.3
 base_da=1964+85+q4_da
 da=base_da
 rows=[];pv=stub_fcff/(1+c['discount'])**stub_discount_years
 stub={'period':'2026-11-07_to_2026-12-31','Q4_full_revenue':q4_revenue,'Q4_full_EBIT':q4_ebit,'Q4_refinery_EBIT_assumption':q4_refinery_ebit,'Q4_full_capex':q4_capex,'Q4_aircraft_commitment':910,'Q4_full_fcff':q4_fcff,'elapsed_fraction_assumed':37/92,'future_fraction':stub_fraction_remaining,'future_fcff':stub_fcff,'discount_years':stub_discount_years,'flight_gross_Sep_proxy':flight_sep,'flight_gross_Dec_proxy':gross/c['uplift'],'advance_Sep_proxy':964+c['advance_increase_9M'],'advance_Dec_proxy':964+c['advance_increase_9M']+q4_advance,'gross_PPE_Sep_tieout':flight_sep+ground_sep+it_sep+964+c['advance_increase_9M'],'Q4_gross_removals_proxy':c['q4_retired'],'not_reported_actuals':True}

 for t in range(1,11):
  revprev=rev; gr=(1+c['capacity'])*(1+c['price_growth'])-1 if t<=5 else .025+(max(0,(1+c['capacity'])*(1+c['price_growth'])-1-.025))*(10-t)/5
  rev*=1+gr; capgrowth=c['capacity'] if t<=5 else c['capacity']*(10-t)/5
  infl=.025; target=(margin_override if margin_override is not None else c['margin']);m=base_air_ebit/base_rev+(target-base_air_ebit/base_rev)*min(t/5,1)
  air_ebit=rev*m; refinery=c['refinery']*(1+infl)**t; ebit=air_ebit+refinery
  flight_maint=gross/c['life']; ground_maint=ground/20;it_maint=it/7
  # positive growth additions separately; floor contractual cash flows without adding replacements a second time
  fleet_cash=max(commit[t-1],flight_maint+gross*capgrowth)
  ground_cash=ground_maint+it_maint+(ground+it)*capgrowth
  capex=fleet_cash+ground_cash # consolidated ground/IT already contains refinery; no separate80 added
  # old asset depreciation fades toward new economic replacement base; no capex=DA terminal reset
  vintage=lambda life:sum((1+infl)**(-a) for a in range(int(life)))/life
  economic_da=.925*flight_maint*vintage(c['life'])+ground_maint*vintage(20)+it_maint*vintage(7)
  da=base_da*(1-t/10)+economic_da*(t/10)
  nwc=.03*(rev-revprev) # explicit stress assumption, not observed normalized NWC
  fcff=ebit*(1-tax)+da-capex-nwc
  pv+=fcff/(1+c['discount'])**(t+stub_discount_years)
  rows.append(dict(year=2026+t,revenue=rev,airline_ebit=air_ebit,refinery_ebit=refinery,ebit=ebit,tax=ebit*tax,da=da,flight_maintenance=flight_maint,flight_cash=fleet_cash,ground_IT_cash=ground_cash,capex=capex,nwc=nwc,fcff=fcff,gross_flight=gross))
  gross*= (1+infl)*(1+capgrowth);ground*=(1+infl)*(1+capgrowth);it*=(1+infl)*(1+capgrowth)
 # steady revenue grows 2.5% inflation only, capacity flat; physical replacement fully funded.
 g=.025;terminal_ebit=(rev*(margin_override if margin_override is not None else c['margin'])+refinery)*(1+g)
 maint=gross/c['life']+ground/20+it/7
 terminal_da=.925*(gross/c['life'])*vintage(c['life'])+(ground/20)*vintage(20)+(it/7)*vintage(7);terminal_capex=maint;terminal_nwc=.03*rev*g
 terminal_fcff=terminal_ebit*(1-tax)+terminal_da-terminal_capex-terminal_nwc
 tv=terminal_fcff/(c['discount']-g);pvt=tv/(1+c['discount'])**(10+stub_discount_years);ev=pv+pvt
 # Current benefit claim not separately reported. No numerical lower/upper equity bound.
 # C=unknown current benefits; L=other settlement/tax/support adjustments; chosen asset realization A.
 expression={'equity_M_formula':'EV - 13746 - 3031 - C - L + A + U',
 'noncurrent_benefits_only':3031,'current_benefits_C':None,'interim_balance_movement_U':None,'other_adjustments_L':None,
 'realizable_cash_and_stakes_A':None,'A_gross_book_ceiling_not_net_realization':3787+3824,
 'per_share_formula':'(EV - 16777 - C - L + A + U) / 661.91238',
 'no_proven_equity_bound':True}
 return {'ev':ev,'pv_explicit_including_stub':pv,'pv_terminal':pvt,'terminal_weight':pvt/ev,'terminal_maintenance':maint,'terminal_fcff':terminal_fcff,'terminal_da':terminal_da,'discount':c['discount'],'equity_bridge':expression,'conditional_equity_per_share_bounds':None,'stub':stub,'rows':rows}
for k,c in scenarios.items():
 r=run(c)
 with (P/f'diagnostic_forecast_{k}.csv').open('w') as f:
  w=csv.DictWriter(f,fieldnames=r['rows'][0]);w.writeheader();w.writerows(r.pop('rows'))
 r['reverse_airline_margin_strict_bridge']=None # missing C/L/A prevents defined equity-price target
 results[k]=r
out={'status':'not-decision-ready','purpose':'diagnostic assumptions only; no approved fair value or entry','market_cap_actual_shares':E,'debt_claim_proxy':D,'share_proxy':S,'wacc_build':{'rf':rf,'erp':erp,'sector_cash_adjusted_unlevered_beta':.76,'relevered_beta':beta,'kd_proxy':kd,'calculated_wacc':wacc,'limitations':['sector January beta, mixed airlines','ERP Nov1 calibrated with Treasury5.29%; combined with Nov6 Treasury4.86% without recalibration; US0.22% default adjustment not netted from either input','kd uses secured floating spread with long treasury not observed bond YTM','market capital weights not target or lease-adjusted sector weights']},'scenarios':scenarios,'results':results,'sensitivity':{str(round(wacc+x,6)):run({**scenarios['central_diagnostico'],'discount':wacc+x})['ev'] for x in [0,.01,.02,.03]},'valuation_date':'2026-11-06','cashflow_timing':'55-day forecast stub then annual year-end cashflows','asset_bridge':asset_bridge,'approval':False}
(P/'diagnostic_results.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
