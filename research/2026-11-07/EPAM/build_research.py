import json,csv,math,pathlib
P=pathlib.Path(__file__).resolve().parent
S={
'FY25':{'url':'https://www.sec.gov/Archives/edgar/data/1352010/000135201026000015/epam-20251231.htm','title':'EPAM 2025 Form 10-K','date':'2026-02-26','purpose':'Three annual financial statements, accounting policies, utilization, geography and acquisitions'},
'Q326':{'url':'https://www.sec.gov/Archives/edgar/data/1352010/000135201026000052/epam-20260930.htm','title':'EPAM Q3 2026 Form 10-Q','date':'2026-11-05','purpose':'Current financial statements, working capital, latest shares, commitments and cash bridge'},
'Q226':{'url':'https://www.sec.gov/Archives/edgar/data/1352010/000135201026000046/epam-20260630.htm','title':'EPAM Q2 2026 Form 10-Q','date':'2026-08-06','purpose':'Quarter and half-year financial statements'},
'Q126':{'url':'https://www.sec.gov/Archives/edgar/data/1352010/000135201026000029/epam-20260331.htm','title':'EPAM Q1 2026 Form 10-Q','date':'2026-05-07','purpose':'First-quarter financial statements'},
'Q325':{'url':'https://www.sec.gov/Archives/edgar/data/1352010/000135201025000056/epam-20250930.htm','title':'EPAM Q3 2025 Form 10-Q','date':'2025-11-06','purpose':'Prior TTM calculation, 2024 and 2025 comparative nine months'},
'Q425':{'url':'https://www.sec.gov/Archives/edgar/data/1352010/000135201026000010/exhibit99_q4x2025.htm','title':'EPAM Q4 and FY2025 earnings release','date':'2026-02-19','purpose':'Quarter, GAAP reconciliation and acquisition-adjusted growth'},
'RELEASE':{'url':'https://www.sec.gov/Archives/edgar/data/1352010/000135201026000048/exhibit99_q3x2026.htm','title':'EPAM Q3 2026 earnings release','date':'2026-11-05','purpose':'Earnings date, guidance, planned repurchase, organic growth'},
'PRESENTATION':{'url':'https://s202.q4cdn.com/436759741/files/doc_financials/2026/q3/EPAM-Q3-2026-Investor-Presentation.pdf','title':'EPAM November 2026 investor presentation','date':'2026-11-05','purpose':'Management AI-native claims and 2026-2028 targets'},
'RATE':{'url':'https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?field_tdr_date_value=2026&type=daily_treasury_yield_curve','title':'Daily Treasury par yields','date':'2026-11-06','purpose':'4.86% ten-year USD risk-free anchor'},
'CTSH':{'url':'https://www.sec.gov/Archives/edgar/data/1058290/000105829026000039/exhibit9919302026.htm','title':'Cognizant Q3 2026 results','date':'2026-10-29','purpose':'Operating peer calibration, not a comparable market multiple'},
'ACN':{'url':'https://www.sec.gov/Archives/edgar/data/1467373/000146737326000037/q4fy26earnings8-kexhibit.htm','title':'Accenture FY2026 results','date':'2026-10-01','purpose':'Operating peer calibration, not a comparable market multiple'},
'PRICE':{'url':'https://www.marketwatch.com/data-news/epam-systems-inc-stock-underperforms-friday-when-compared-to-competitors-90da7c55-8f028801c915','title':'EPAM November 6 closing-market recap','date':'2026-11-06','purpose':'Independent confirmation of $159.31 regular-session close'},
'EVENTS':{'url':'https://investors.epam.com/events/default.aspx','title':'EPAM investor events','date':'2026-11-07','purpose':'Calendar review; no verified next earnings date assigned'}
}
# USD millions and million shares. EPS USD. Transcribed financial statement values; signs preserved.
keys=['revenue','ebit','net_income','da','sbc','cfo','capex','eps','diluted_shares']
raw={
'FY2023':[4690.540,501.239,417.083,91.800,147.730,562.634,28.415,7.06,59.085],
'FY2024':[4727.940,544.584,454.533,89.559,167.297,559.168,32.146,7.84,57.983],
'FY2025':[5457.056,520.003,377.678,124.811,176.764,654.934,42.243,6.72,56.233],
'9M2024':[3479.589,408.072,351.234,63.003,122.599,428.909,16.419,6.04,58.166],
'9M2025':[4049.508,370.749,268.324,94.024,131.618,372.044,27.462,4.75,56.534],
'9M2026':[4241.258,444.918,315.811,96.260,138.798,250.052,47.749,6.00,52.630],
'H12026':[2814.828,268.990,185.500,63.640,96.320,-38.784,33.071,3.49,53.220],
'Q12026':[1400.061,116.768,82.521,31.539,49.919,-36.360,17.857,1.52,54.183],
'Q22026':[1414.767,152.222,102.979,32.101,46.401,-2.424,15.214,1.97,52.267],
'Q32026':[1426.430,175.928,130.311,32.620,42.478,288.836,14.678,2.53,51.469],
'Q42025':[1407.548,149.254,109.354,30.787,45.146,282.890,14.781,1.98,55.341]
}
a={p:dict(zip(keys,v)) for p,v in raw.items()}
for label,fy,ytd,prev in [('TTM2026','FY2025','9M2026','9M2025'),('TTM2025','FY2024','9M2025','9M2024')]:
 a[label]={k:a[fy][k]+a[ytd][k]-a[prev][k] for k in keys if k not in ['diluted_shares','eps']}
 a[label]['eps']=a[fy]['eps']+a[ytd]['eps']-a[prev]['eps']
 a[label]['diluted_shares']=None # EPS uses FY + current nine months - prior nine months; not the sum of quarterly EPS.
for p,r in a.items():
 r.update(fcf=r['cfo']-r['capex'],owner_cash_proxy=r['cfo']-r['capex']-r['sbc'],op_margin=r['ebit']/r['revenue'],net_margin=r['net_income']/r['revenue'])
bridge={'cash_reported':965.173,'restricted_cash_excluded':4.769,'short_term_investments':4.6,'debt':25.,'contingent_consideration':9.473,'software_deferred_consideration':18.5,'net_derivative_liability':13.864-2.746,'noncontrolling_interest':.582,'operating_cash_reserve':a['TTM2026']['revenue']*.03,'lease_liability_operating_treatment':121.328,'shares_cover_Nov3':51.023335,'dilution_buffer':.445665,'valuation_shares':51.469}
bridge['equity_adjustment']=bridge['cash_reported']+bridge['short_term_investments']-sum(bridge[k] for k in ['debt','contingent_consideration','software_deferred_consideration','net_derivative_liability','noncontrolling_interest','operating_cash_reserve'])
case_specs={
'bear':{'growth':[0,0,.01,.02,.02,.02,.02,.02,.02,.02],'margins':[.105,.10,.10,.10,.10,.10,.10,.10,.10,.10],'tax':.28,'wacc':.12,'terminal_growth':.02,'roic':.20},
'base':{'growth':[.03,.04,.05,.05,.045,.04,.04,.035,.03,.03],'margins':[.112,.118,.122,.125,.125,.125,.125,.125,.125,.125],'tax':.27,'wacc':.11,'terminal_growth':.025,'roic':.25},
'bull':{'growth':[.05,.07,.08,.08,.07,.06,.05,.045,.04,.035],'margins':[.12,.13,.135,.14,.14,.14,.14,.14,.14,.14],'tax':.26,'wacc':.10,'terminal_growth':.03,'roic':.30}}
def calc(c):
 r=a['TTM2026']['revenue']; n=a['TTM2026']['ebit']*(1-c['tax']); rows=[];pv=0
 for y in range(1,12):
  g=c['growth'][y-1] if y<=10 else c['terminal_growth']; m=c['margins'][y-1] if y<=10 else c['margins'][-1]
  nr=r*(1+g); nn=nr*m*(1-c['tax']); nwc=max(0,nr-r)*.15
  # Entire positive NOPAT increase, including margin gains, must be funded; no release assumed on contraction.
  economic=max(0,nn-n)/c['roic']; physical_floor=nr*.005
  reinvest=max(economic,nwc+physical_floor); growth_capex=reinvest-nwc;physical_da=nr*.01;capex=physical_da+growth_capex
  fcff=nn+physical_da-capex-nwc
  row=dict(year=y,revenue=nr,growth=g,margin=m,ebit=nr*m,tax=c['tax'],nopat=nn,delta_nopat=nn-n,nwc_reinvestment=nwc,economic_reinvestment=economic,net_physical_floor=physical_floor,growth_capex=growth_capex,physical_da=physical_da,capex=capex,reinvestment=reinvest,fcff=fcff,discount_factor=(1+c['wacc'])**y)
  rows.append(row)
  if y<=10:pv+=fcff/row['discount_factor']
  r,n=nr,nn
 tv=rows[-1]['fcff']/(c['wacc']-c['terminal_growth']);pvt=tv/(1+c['wacc'])**10;ev=pv+pvt
 return {'assumptions':c,'rows':rows,'pv_explicit':pv,'pv_terminal':pvt,'terminal_share_ev':pvt/ev,'ev':ev,'equity':ev+bridge['equity_adjustment'],'value':(ev+bridge['equity_adjustment'])/bridge['valuation_shares']}
cases={k:calc(v) for k,v in case_specs.items()}
sens=[]
for w in [.09,.10,.11,.12,.13]:
 for g in [.015,.02,.025,.03]:
  c=dict(case_specs['base'],wacc=w,terminal_growth=g);sens.append({'wacc':w,'g':g,'value':calc(c)['value']})
stress=[]
for roic in [.15,.20,.25,.30,.40]:stress.append({'roic':roic,'value':calc(dict(case_specs['base'],roic=roic))['value']})
# Solve fixed 10-year annual sales growth, retaining the base margin ramp and all reinvestment constraints.
lo,hi=-.05,.25
for _ in range(100):
 mid=(lo+hi)/2;v=calc(dict(case_specs['base'],growth=[mid]*10))['value']
 if v<159.31:lo=mid
 else:hi=mid
reverse={'target_price':159.31,'fixed_10yr_sales_growth':(lo+hi)/2,'conditions':'Base margin ramp to 12.5%, 11% discount, 2.5% terminal growth, 25% incremental ROIC, same funded-growth floors; not a forecast.'}
reverse_grid=[{'growth':-.05+i*.0005,'value':calc(dict(case_specs['base'],growth=[-.05+i*.0005]*10))['value']} for i in range(601)]
reverse['qa']={'bracket_growth':[-.05,.25],'bracket_values':[reverse_grid[0]['value'],reverse_grid[-1]['value']],'grid_points':601,'strictly_monotonic':all(reverse_grid[i+1]['value']>reverse_grid[i]['value'] for i in range(600)),'target_bracketed':reverse_grid[0]['value']<159.31<reverse_grid[-1]['value'],'solved_value':calc(dict(case_specs['base'],growth=[reverse['fixed_10yr_sales_growth']]*10))['value']}
reverse['qa']['residual']=reverse['qa']['solved_value']-159.31
reverse['grid']=reverse_grid

checks={'three_fiscal_years':all(k in a for k in ['FY2023','FY2024','FY2025']),'four_quarters_sum_revenue':abs(sum(a[k]['revenue'] for k in ['Q42025','Q12026','Q22026','Q32026'])-a['TTM2026']['revenue'])<1e-6,'four_quarters_sum_cfo':abs(sum(a[k]['cfo'] for k in ['Q42025','Q12026','Q22026','Q32026'])-a['TTM2026']['cfo'])<1e-6,'all_years_and_terminal_funded':all(r['reinvestment']+1e-8>=max(r['economic_reinvestment'],r['nwc_reinvestment']+r['net_physical_floor']) for c in cases.values() for r in c['rows']),'all_wacc_gt_g':all(c['assumptions']['wacc']>c['assumptions']['terminal_growth'] for c in cases.values()),'ordered_cases':cases['bear']['value']<cases['base']['value']<cases['bull']['value'],'no_asr_execution_assumed':True,'no_lease_double_deduction':True,'no_sbc_addback_in_fcff':True}
out={'as_of':'2026-11-07','price':159.31,'units':'USD millions, million shares; per-share amounts USD','historical':a,'bridge':bridge,'cases':cases,'sensitivities':sens,'roic_stress':stress,'reverse_dcf':reverse,'checks':checks,'status':'screen-grade','notes':['Model is deterministic report support, not a banker formula workbook or technical entry approval.','GAAP-based forecast margins retain SBC, operating lease expense and intangible consumption. No amortization or SBC addback.','Physical DA assumed 1% of revenue, offset by maintenance capex. Growth capex and working capital charged each year and terminal.','Dilution buffer makes current valuation denominator equal to latest quarterly diluted shares; no forecast ASR benefit.','TTM EPS is an approximate FY plus current nine months minus prior nine months calculation across different weighted-share periods; not a quarterly EPS sum or NI/current shares. Current actual quarterly EPS sum is 8.00.','Capex excludes acquisitions; owner_cash_proxy is CFO minus reported capex minus SBC, not FCFF.']}
out.update(stage3_complete=False, entry_approved=False, approved_value=None, approved_target=None, approved_entry=None, approved_stop=None, approved_quantity=None, publication_scope='provisional_research_only', timing_convention='Ten full forward annual cash flows discounted at year end; terminal value at end of year 10 using funded year-11 cash flow. September 2026 TTM anchor; no calendar-date stub or partial-year catch-up adjustment.')
out['historical_sources']={
 'FY2023':{'type':'reported','urls':[S['FY25']['url']]},'FY2024':{'type':'reported','urls':[S['FY25']['url']]},'FY2025':{'type':'reported','urls':[S['FY25']['url']]},
 '9M2024':{'type':'reported','urls':[S['Q325']['url']]},'9M2025':{'type':'reported','urls':[S['Q326']['url'],S['Q325']['url']]},'9M2026':{'type':'reported','urls':[S['Q326']['url']]},
 'H12026':{'type':'reported','urls':[S['Q226']['url']]},'Q12026':{'type':'reported','urls':[S['Q126']['url']]},
 'Q22026':{'type':'reported and derived','urls':[S['Q226']['url'],S['Q126']['url']],'calculation':'CFO and capex: H12026 - Q12026'},
 'Q32026':{'type':'reported and derived','urls':[S['Q326']['url'],S['Q226']['url']],'calculation':'CFO and capex: 9M2026 - H12026'},
 'Q42025':{'type':'reported and derived','urls':[S['Q425']['url'],S['FY25']['url'],S['Q325']['url']],'calculation':'CFO, capex and SBC: FY2025 - 9M2025'},
 'TTM2026':{'type':'derived','calculation':'FY2025 + 9M2026 - 9M2025'},'TTM2025':{'type':'derived','calculation':'FY2024 + 9M2025 - 9M2024'}}
out['additional_stresses']={
 'all_excluded_awards_added_no_exercise_proceeds':{'shares':51.469+1.642,'value':cases['base']['equity']/(51.469+1.642),'purpose':'Harsh dilution sensitivity, not treasury-stock-method estimate; retained SBC means this is not the main model.'},
 'base_margin_minus_100bp':calc(dict(case_specs['base'],margins=[m-.01 for m in case_specs['base']['margins']]))['value'],
 'base_margin_plus_100bp':calc(dict(case_specs['base'],margins=[m+.01 for m in case_specs['base']['margins']]))['value'],
 'conditional_500m_asr_at_reference_price':{'net_cash_change':-500,'share_change':-500/159.31,'value':(cases['base']['equity']-500)/(bridge['valuation_shares']-500/159.31),'status':'Illustrative only; not an execution assumption'},
 'no_operating_cash_reserve':(cases['base']['equity']+bridge['operating_cash_reserve'])/bridge['valuation_shares']}
(P/'derived_inputs_and_model.json').write_text(json.dumps(out,indent=2))
(P/'source_ledger.json').write_text(json.dumps(list(S.values()),indent=2))
(P/'qa.json').write_text(json.dumps({'status':'screen-grade','checks':checks,'hard_failures':[k for k,v in checks.items() if not v],'limitations':['No current independent utilization/rate decomposition, customer-level AI profitability or consensus dataset.','Growth, margin, ROIC, ERP and beta are analyst assumptions, not reported forecasts.','Post-September cash bridge is not a November 6 balance sheet.','Same-date peer trading multiples and homogeneous historical EPAM/peer multiple ranges were not verified; operating comparison only.']},indent=2))
with (P/'annual_forecast.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=['case']+list(cases['base']['rows'][0]));w.writeheader()
 for case,c in cases.items():
  for row in c['rows']:w.writerow(dict(case=case,**row))
print(json.dumps({'cases':{k:{x:v[x] for x in ['value','ev','terminal_share_ev']} for k,v in cases.items()},'reverse':reverse,'roic_stress':stress,'bridge':bridge,'checks':checks,'ttm':a['TTM2026'],'prior_ttm':a['TTM2025']},indent=2))
