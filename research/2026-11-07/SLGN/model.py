"""SLGN conditional legacy-business FCFF diagnostics. USD million except per share.
Run: python model.py. No target price: acquisition, minority and seasonal bridges remain open.
"""
import json,csv,math,pathlib
P=pathlib.Path(__file__).resolve().parent
src={
'annual':{'url':'https://s29.q4cdn.com/241493639/files/doc_financials/2025/ar/2025-Annual-Report-Web_BMK.pdf','title':'Silgan 2025 annual report','date':'2025-12-31','purpose':'Three annual statements; acquisition, pension, leases and amortization notes'},
'q3':{'url':'https://www.sec.gov/Archives/edgar/data/849869/000162828026070678/slgn-20260930.htm','title':'Silgan September 2026 Form 10-Q','date':'2026-11-05','purpose':'Quarter/YTD financials, LIFO liquidation, debt principal and transaction financing'},
'prior':{'url':'https://www.sec.gov/Archives/edgar/data/849869/000162828025049324/slgn-20250930.htm','title':'Silgan September 2025 Form 10-Q','date':'2025-11-05','purpose':'Prior TTM and comparative quarterly reconstruction'},
'q1':{'url':'https://www.sec.gov/Archives/edgar/data/849869/000162828026028421/a991_33126.htm','title':'Silgan Q1 2026 earnings release','date':'2026-04-29','purpose':'Q1 and prior-year quarter, volume and pass-through'},
'q2':{'url':'https://www.sec.gov/Archives/edgar/data/849869/000162828026050641/a991_63026.htm','title':'Silgan Q2 2026 earnings release','date':'2026-07-29','purpose':'Q2 and six-month cash flow comparisons'},
'q4':{'url':'https://www.sec.gov/Archives/edgar/data/849869/000162828026005470/a991_123125.htm','title':'Silgan Q4 and FY2025 earnings release','date':'2026-02-04','purpose':'Q4 comparisons and company FCF definition'},
'latest':{'url':'https://www.sec.gov/Archives/edgar/data/849869/000162828026068277/a991_93026.htm','title':'Silgan Q3 2026 earnings release','date':'2026-10-29','purpose':'Guidance and segment commercial commentary'},
'deal':{'url':'https://www.sec.gov/Archives/edgar/data/849869/000119312526424669/d152250dex991.htm','title':'Silgan Trivium partnership announcement','date':'2026-10-19','purpose':'Consideration, 60/40 ownership, synergies, timing and transaction multiples'},
'consent':{'url':'https://www.sec.gov/Archives/edgar/data/849869/000162828026071735/slgn-20261106.htm','title':'Silgan lender consent Form 8-K','date':'2026-11-06','purpose':'Guarantor release, unrestricted subsidiary and debt redemption permissions'},
'calendar':{'url':'https://www.silganholdings.com/investor-information/events-and-presentations/events/default.aspx','title':'Silgan official event calendar','date':'2026-11-07','purpose':'Calendar checked; no next earnings date verified in readable page'},
'rates':{'url':'https://www.federalreserve.gov/releases/H15/Current/','title':'Federal Reserve H.15 November 6 release','date':'2026-11-06','purpose':'Approximately 4.8–4.9% Treasury rate calibration; not a precise trade-time fix'},
'aptar':{'url':'https://www.sec.gov/Archives/edgar/data/896622/000089662226000187/atr-20260930x8kexx991.htm','title':'Aptar Q3 2026 release','date':'2026-10-29','purpose':'Dispensing peer operating context'},
'crown':{'url':'https://www.sec.gov/Archives/edgar/data/1219601/000162828026066281/ex99sep2026.htm','title':'Crown Q3 2026 release','date':'2026-10-19','purpose':'Metal packaging peer operating context'},
'quote':{'url':'https://stockanalysis.com/stocks/slgn/history/','title':'Silgan historical prices','date':'2026-11-06','purpose':'Independently verified regular-session close $41.09 at 16:00 EST; not proof of scanner observation identity'},
'crownmultiple':{'url':'https://stockanalysis.com/stocks/cck/statistics/','title':'Crown valuation statistics','date':'2026-11-07','purpose':'Secondary indicative EV/EBITDA 8.71x; not a synchronized comp target'}
}
# USD million, actuals transcribed from the consolidated statements; sources use thousands.
keys=['revenue','ebit','net_income','cfo','capex','da','sbc','rationalization','interest','amortization']
A={
'FY2023':[5988.205,595.436,325.965,482.596,226.810,263.233,15.572,8.412,173.315,53.091],
'FY2024':[5854.694,515.095,276.378,721.873,262.786,275.884,15.524,59.481,167.425,52.620],
'FY2025':[6483.166,597.867,288.403,729.841,307.092,319.163,18.020,60.509,189.365,64.623],
'9M2024':[4443.527,420.859,231.314,-213.888,192.035,198.648,11.727,38.033,121.861,38.004],
'9M2025':[5014.561,496.733,270.199,-563.965,235.791,238.210,12.916,28.012,141.616,47.307],
'9M2026':[5244.718,469.312,243.778,-646.363,229.451,252.455,16.785,44.276,136.823,48.125]
}
A={p:dict(zip(keys,v)) for p,v in A.items()}
for name,fy,ytd,prev in [('TTM2026','FY2025','9M2026','9M2025'),('TTM2025','FY2024','9M2025','9M2024')]:
 A[name]={k:round(A[fy][k]+A[ytd][k]-A[prev][k],6) if all(A[p][k] is not None for p in [fy,ytd,prev]) else None for k in keys}
for v in A.values():v['cfo_less_capex']=v['cfo']-v['capex'];v['ebit_margin']=v['ebit']/v['revenue']
Q=[
{'period':'Q4 2025','revenue':1468.605,'prior_revenue':1411.167,'ebit':101.134,'prior_ebit':94.236,'net_income':18.204,'prior_net_income':45.064,'cfo':1293.806,'prior_cfo':935.761,'capex':71.301,'prior_capex':70.751,'da':80.953,'prior_da':77.236,'source':'annual+q3/prior (FY minus 9M)'},
{'period':'Q1 2026','revenue':1561.3,'prior_revenue':1466.7,'ebit':126.6,'prior_ebit':130.5,'net_income':63.0,'prior_net_income':68.0,'cfo':-799.6,'prior_cfo':-683.4,'capex':82.4,'prior_capex':82.9,'da':84.9,'prior_da':79.4,'source':'q1; rounded'},
{'period':'Q2 2026','revenue':1643.3,'prior_revenue':1539.2,'ebit':151.0,'prior_ebit':167.5,'net_income':75.8,'prior_net_income':89.0,'cfo':-194.3,'prior_cfo':-221.5,'capex':64.3,'prior_capex':72.8,'da':83.8,'prior_da':75.9,'source':'q2; quarterly cash flows = 6M minus Q1; rounded'},
{'period':'Q3 2026','revenue':2040.191,'prior_revenue':2008.739,'ebit':191.672,'prior_ebit':198.658,'net_income':104.981,'prior_net_income':113.293,'cfo':347.537,'prior_cfo':340.935,'capex':82.751,'prior_capex':80.091,'da':83.755,'prior_da':82.910,'source':'q3; quarterly cash flows = 9M minus rounded 6M'}]
t=A['TTM2026'];bridge={'gaap_ebit':t['ebit'],'add_acquired_amortization':t['amortization'],'add_reported_rationalization':t['rationalization'],'add_transaction_cost':10.333,'remove_other_pension_income':-3.635,'remove_lifo_liquidation_benefit':-34,'restore_recurring_rationalization_cost_assumption':-35}
base_ebita=sum(bridge.values()); rev=t['revenue'];tax=.26
# Explicit conditional operating-business DCF. Recurring SBC stays in EBITA, no SBC add-back.
config={'bear':dict(growth=.01,margin=.09,wacc=.10,terminal_g=.015,roic=.09,sales_capital=2.2,nwc=.10),
'base':dict(growth=.03,margin=.105,wacc=.09,terminal_g=.02,roic=.12,sales_capital=2.5,nwc=.08),
'bull':dict(growth=.045,margin=.12,wacc=.08,terminal_g=.025,roic=.15,sales_capital=2.8,nwc=.07)}
# Current debt principal (includes finance leases). Operating leases expensed, not subtracted again.
claims={'debt_principal':4562.071,'cash':324.989,'minimum_operating_cash_assumption':150,'foreign_pension_deficit_2025':91.019,'other_postretirement_deficit_2025':8.583,'shares_diluted_assumption':106.5}
# Cash-flow contributions to foreign deficits are not separately charged; service cost retained.
# Central States 2.6 annual payment IS charged, and its liability is not subtracted again.
def dcf(c,seasonal_release=0):
 rows=[];r=rev;prev_nopat=base_ebita*(1-tax);pv=0
 for y in range(1,12):
  g=c['growth'] if y<=5 else c['growth']+(c['terminal_g']-c['growth'])*min((y-5)/5,1)
  r0=r;r=r0*(1+g);margin=base_ebita/rev+(c['margin']-base_ebita/rev)*min(y/5,1)
  ebita=r*margin;nopat=ebita*(1-tax)
  amort=t['amortization']*max(0,1-y/10);shield=amort*tax
  depreciation=r*(t['da']-t['amortization'])/rev
  # Replacement cost gradually rises to 105% of depreciation; no terminal release.
  maintenance=depreciation*(1+.05*min(y/10,1))
  dnwc=max(r-r0,0)*c['nwc'];physical=max(r-r0,0)/c['sales_capital']
  funded_nopat=max(nopat-prev_nopat,0)/c['roic']
  reinvest=max(funded_nopat,physical+dnwc)
  growth_capex=max(reinvest-dnwc,0);capex=maintenance+growth_capex
  central_states=2.6 if y<=10 else 2.6 # Conservatively carries beyond 2040 in terminal; quantified small limitation.
  fcff=nopat+shield+depreciation-capex-dnwc-central_states
  row=dict(year=y,revenue=r,growth=g,margin=margin,ebita=ebita,nopat=nopat,amort_tax_shield=shield,depreciation=depreciation,maintenance_capex=maintenance,delta_nwc=dnwc,physical_growth_capex_floor=physical,nopat_reinvestment_requirement=funded_nopat,growth_capex=growth_capex,total_capex=capex,reinvestment=reinvest,central_states_payment=central_states,fcff=fcff,pv_fcff=fcff/(1+c['wacc'])**y)
  rows.append(row)
  if y<=10:pv+=row['pv_fcff']
  prev_nopat=nopat
 tv=rows[-1]['fcff']/(c['wacc']-c['terminal_g']);pvtv=tv/(1+c['wacc'])**10;ev=pv+pvtv
 eq=ev-claims['debt_principal']+max(claims['cash']-claims['minimum_operating_cash_assumption'],0)-claims['foreign_pension_deficit_2025']-claims['other_postretirement_deficit_2025']+seasonal_release
 return dict(assumptions=c,years=rows,pv_explicit=pv,pv_terminal=pvtv,enterprise_value=ev,equity_value=eq,conditional_value_per_share=eq/claims['shares_diluted_assumption'],terminal_ev_share=pvtv/ev,terminal_ev_ebitda=tv/(rows[-2]['ebita']+rows[-2]['depreciation']),seasonal_release=seasonal_release)
C={k:dcf(v) for k,v in config.items()}
sens=[dict(wacc=w,g=g,value=dcf(dict(config['base'],wacc=w,terminal_g=g))['conditional_value_per_share']) for w in [.08,.09,.10,.11] for g in [.01,.02,.025]]
price=41.09
# Price-equating margin, held at Y5+; same reinvestment requirements maintained.
lo,hi=.05,.30
for _ in range(100):
 mid=(lo+hi)/2
 if dcf(dict(config['base'],margin=mid))['conditional_value_per_share']<price:lo=mid
 else:hi=mid
inverse={'verified_reference_close':price,'reference_close_date':'2026-11-06','reference_close_time':'16:00 EST','source_url':'https://stockanalysis.com/stocks/slgn/history/','required_y5_ebita_margin_no_seasonal_release':(lo+hi)/2,'required_enterprise_value':price*claims['shares_diluted_assumption']+claims['debt_principal']-max(claims['cash']-claims['minimum_operating_cash_assumption'],0)+claims['foreign_pension_deficit_2025']+claims['other_postretirement_deficit_2025']}
inverse_grid=[dcf(dict(config['base'],margin=.05+i*.25/500))['conditional_value_per_share'] for i in range(501)]
inverse_qa={'endpoint_low':inverse_grid[0],'endpoint_high':inverse_grid[-1],'grid_strictly_monotonic':all(a<b for a,b in zip(inverse_grid,inverse_grid[1:])),'brackets_price':inverse_grid[0]<price<inverse_grid[-1],'residual':dcf(dict(config['base'],margin=inverse['required_y5_ebita_margin_no_seasonal_release']))['conditional_value_per_share']-price}
assert inverse_qa['grid_strictly_monotonic'] and inverse_qa['brackets_price'] and abs(inverse_qa['residual'])<1e-9
flags={'stage3Complete':False,'entryApproved':False,'approvedValuation':None,'marginOfSafety':None}
(P/'decision-status.json').write_text(json.dumps(flags,indent=2))
checks=[]
for k,c in C.items():
 for row in c['years']:
  assert row['reinvestment']+1e-9>=row['nopat_reinvestment_requirement'];assert row['reinvestment']+1e-9>=row['physical_growth_capex_floor']+row['delta_nwc']
  assert abs(row['fcff']-(row['nopat']+row['amort_tax_shield']+row['depreciation']-row['total_capex']-row['delta_nwc']-row['central_states_payment']))<1e-6
 checks.append(f'{k}: all 11 years including terminal fund margin-driven NOPAT and physical+NWC floor; FCFF arithmetic passes')
assert abs(sum(x['revenue'] for x in Q)-t['revenue'])<.2
assert abs(sum(x['ebit'] for x in Q)-t['ebit'])<.2
assert abs(sum(x['cfo'] for x in Q)-t['cfo'])<.2
checks+=['Quarterly revenue, EBIT and CFO reconcile to TTM within $0.2m release rounding','TTM = FY2025 + 9M2026 - 9M2025; prior TTM = FY2024 + 9M2025 - 9M2024','One-sided Q3 removal of disclosed 2026 LIFO benefit: 234.998 - 26.8 = 208.198 versus reported adjusted 221.408 prior; prior comparable benefit not separately quantified, so not fully normalized YoY','Company FCF reconciliation: 729.841 - 307.092 + 10.040 + 12.398 = 445.187','No current fair value, margin of safety or entry approval: seasonal and transaction bridges unresolved']
O=dict(as_of='2026-11-07',units='USD millions except per share',status='conditional_legacy_diagnostics_not_current_fair_value',decision_flags=flags,inverse_qa=inverse_qa,annual_and_ttm=A,quarters=Q,ebita_normalization=bridge,normalized_ebita=base_ebita,claims=claims,cases=C,sensitivity=sens,inverse=inverse,seasonal_release_sensitivity={str(x):{k:dcf(c,x)['conditional_value_per_share'] for k,c in config.items()} for x in [0,600,1000]},qa=checks)
(P/'derived-inputs-and-results.json').write_text(json.dumps(O,indent=2));(P/'source-ledger.json').write_text(json.dumps(list(src.values()),indent=2));(P/'sources-key.json').write_text(json.dumps(src,indent=2))
for name,rows in [('historical', [dict(period=k,**v) for k,v in A.items()]),('quarters',Q),('forecast',[dict(case=k,**r) for k,c in C.items() for r in c['years']]),('sensitivities',sens)]:
 with (P/(name+'.csv')).open('w') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
(P/'qa.json').write_text(json.dumps({'decision_flags':flags,'inverse_qa':inverse_qa,'presentation':'Visual review not performed.','passed':checks,'blocking_gaps':['Deal-inclusive carve-out FCFF, integration costs and minority bridge are not completed','Seasonal NWC/cash-to-valuation-date bridge not verified','Technical trend and entry levels unavailable; regular close independently verified at $41.09 on November 6, 16:00 EST'],'ordinary_assumptions':['Growth, EBITA margin, ROIC, maintenance capex, tax, WACC, sales/capital, normal NWC ratio and operating cash requirement are analyst assumptions, not missing reported figures']},indent=2))
print(json.dumps({k:dict(v=c['conditional_value_per_share'],EV=c['enterprise_value'],tv_share=c['terminal_ev_share'],terminal_multiple=c['terminal_ev_ebitda']) for k,c in C.items()},indent=2));print(inverse);print(A['TTM2026']);print('normalized',base_ebita)
