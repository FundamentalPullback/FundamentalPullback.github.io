import json,csv,pathlib,math
P=pathlib.Path(__file__).parent
# All financial input rows in RMB millions; sources S1-S4. Never annualize one quarter.
cols=['revenue','ebit','net_income','cfo','capex_incl_intangibles','da','sbc','other_operating_income']
a={
'FY2023':[4665.967,924.034,739.057,1988.674,41.724,85.021,163.978,83.179],
'FY2024':[7247.932,1622.302,1272.984,1725.948,58.179,65.232,32.792,70.231],
'FY2025':[9790.159,2306.677,1621.262,1992.822,86.029,54.106,131.472,184.089],
'H12024':[3265.340,716.040,561.614,719.877,33.033,33.839,27.027,4.066],
'H12025':[4374.363,951.463,668.428,768.471,48.498,25.996,103.387,17.723],
'H12026':[6301.588,1436.208,1011.411,1127.552,12.097,29.092,36.785,135.246],
'Q42025':[2787.826,703.758,478.444,593.512,11.676,13.789,14.771,153.696],
'Q22026':[3490.347,773.247,547.927,835.227,6.537,14.464,10.302,43.981]}
a['Q32025']=[x-y-z for x,y,z in zip(a['FY2025'],a['H12025'],a['Q42025'])]
a['Q12026']=[x-y for x,y in zip(a['H12026'],a['Q22026'])]
for yr in [2025,2026]: a[f'TTM{yr}']=[x+y-z for x,y,z in zip(a[f'FY{yr-1}'],a[f'H1{yr}'],a[f'H1{yr-1}'])]
actual={k:dict(zip(cols,v)) for k,v in a.items()}
for row in actual.values():row.update(cash_fcf=row['cfo']-row['capex_incl_intangibles'],ebit_margin=row['ebit']/row['revenue'])
with open(P/'actuals.csv','w') as f:
 w=csv.DictWriter(f,fieldnames=['period']+list(next(iter(actual.values()))));w.writeheader();w.writerows(dict(period=k,**v) for k,v in actual.items())
# Diagnostic USD nominal model: each RMB operating forecast translated at fixed FX assumption.
# Not an investable target; missing interim operating cash reconciliation and current balance claims.
fx=6.6765;close=35.91;ads=410.476026/3
rf=.0486-.0022;erp=.0441;crp=.008727858397633674;beta=.67
ke=rf+beta*erp+crp
# 100% equity diagnostic financing policy; do not mix RMB historical borrowing rate into USD WACC.
wacc=ke
# Aggregate liquid assets before minimum liquidity/distribution restrictions. Deduction is an assumption, not proven excess cash.
cash=3924.845+1797.192;reserve=1500;debt=237;other_claims=0
net_adjustment=(cash-reserve-debt-other_claims)/fx
base=actual['TTM2026'];normebit=base['ebit']-base['other_operating_income'];tax=.32
bridge={'cash_fcf':base['cash_fcf'],'remove_sbc':-base['sbc'],'unresolved_other_cfo_adjustments':-(base['cfo']-base['net_income']-base['da']-base['sbc']), 'replace_net_income_with_normalized_nopat':normebit*(1-tax)-base['net_income'],'normalized_fcff_before_wc':normebit*(1-tax)+base['da']-base['capex_incl_intangibles']}
scenarios={
'adverso':{'growth':[.12,.09,.07,.05,.04],'margin':[.19,.185,.18,.18,.18],'terminal_margin':.18,'g':.02,'sales_capital':2.,'roic':.15},
'central':{'growth':[.22,.18,.15,.12,.09],'margin':[.21,.21,.21,.21,.21],'terminal_margin':.21,'g':.025,'sales_capital':3.,'roic':.20},
'favorable':{'growth':[.28,.24,.20,.16,.12],'margin':[.22,.225,.23,.23,.23],'terminal_margin':.23,'g':.03,'sales_capital':4.,'roic':.25}}
def value(s,w=wacc,fxv=fx,mm=0):
 assert w>s['g'], "Discount rate must exceed terminal growth"
 assert fxv>0 and ads>0 and s['roic']>s['g']
 rev=base['revenue']/fxv;rows=[];pv=0
 for y in range(1,11):
  g=s['growth'][y-1] if y<=5 else s['growth'][-1]+(s['g']-s['growth'][-1])*(y-5)/5
  m=s['margin'][y-1] if y<=5 else s['margin'][-1]+(s['terminal_margin']-s['margin'][-1])*(y-5)/5
  m+=mm;old=rev;rev*=1+g;nopat=rev*m*(1-tax);da=rev*.005
  # Years 1-5 investment paid for each incremental sales dollar. During transition fade to g/ROIC.
  nr=(rev-old)/s['sales_capital'];terminal_reinvest=nopat*g/s['roic'];fade=max(0,(y-5)/5);nr=nr*(1-fade)+terminal_reinvest*fade
  wc=.2*nr;capex=da+.8*nr;fcff=nopat+da-capex-wc;discounted=fcff/(1+w)**y;pv+=discounted
  rows.append(dict(year=y,revenue=rev,growth=g,ebit_margin=m,ebit=rev*m,nopat=nopat,da=da,total_capex_incl_software=capex,delta_wc=wc,net_reinvestment=nr,fcff=fcff,pv_fcff=discounted))
 terminal_nopat=rev*(1+s['g'])*(s['terminal_margin']+mm)*(1-tax);terminal_fcff=terminal_nopat*(1-s['g']/s['roic']);tv=terminal_fcff/(w-s['g']);pvt=tv/(1+w)**10;ev=pv+pvt;adj=(cash-reserve-debt-other_claims)/fxv
 return dict(value_per_ads=(ev+adj)/ads,ev=ev,equity=ev+adj,pv_terminal=pvt,terminal_weight=pvt/ev,terminal_nopat=terminal_nopat,terminal_reinvestment=terminal_nopat*s['g']/s['roic'],terminal_fcff=terminal_fcff,rows=rows)
results={'as_of':'2026-11-08','status':'bounded_partial_diagnostic_not_fair_value','actuals':actual,'bridge_rmb_m':bridge,'price':{'scanner_last':35.4,'regular_close':close,'session':'2026-11-06','time':'16:00 EST'},'discount':{'usd_treasury':.0486,'us_default_spread':.0022,'usd_riskfree':rf,'mature_erp':erp,'china_crp_july2026':crp,'beta_5y_label_short_listing_history':beta,'ke':ke,'diagnostic_wacc_100pct_equity':wacc,'historical_rmb_borrowing_rate_not_used':.027},'capital':{'fx_cny_per_usd':fx,'diluted_weighted_ads_proxy_m':ads,'cash_shortinvest_rmb_m':cash,'liquidity_reserve_assumed_rmb_m':reserve,'debt_rmb_m':debt,'net_equity_adjustment_usd_m':net_adjustment,'nci_negative_book_not_added':-12.338,'leases_rmb_m_not_subtracted_twice':1057.821},'assumptions':scenarios,'scenarios':{},'sensitivity':[],'inverse_diagnostic':[],'approval':False}
for k,s in scenarios.items():
 v=value(s);rows=v.pop('rows');results['scenarios'][k]=v
 with open(P/f'forecast_{k}.csv','w') as f:w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
for w in [wacc-.01,wacc,wacc+.01,wacc+.02]:
 for g in [.02,.025,.03]:results['sensitivity'].append({'wacc':w,'g':g,'value_per_ads':value(dict(scenarios['central'],g=g),w)['value_per_ads']})
for label,s in scenarios.items():
 lo=-.17;hi=.2
 for _ in range(90):
  mid=(lo+hi)/2
  if value(s,mm=mid)['value_per_ads']>close:hi=mid
  else:lo=mid
 results['inverse_diagnostic'].append({'growth_case':label,'constant_margin_shift_to_equal_close':mid,'year1_margin':s['margin'][0]+mid,'year10_margin':s['terminal_margin']+mid})
# Controls cover all 30 forecast rows, not only the central case.
for case in scenarios.values():
 v=value(case)
 assert len(v['rows'])==10
 for row in v['rows']:
  assert math.isclose(row['fcff'],row['nopat']+row['da']-row['total_capex_incl_software']-row['delta_wc'],abs_tol=1e-9)
  assert math.isclose(row['net_reinvestment'],row['total_capex_incl_software']-row['da']+row['delta_wc'],abs_tol=1e-9)
 assert math.isclose(v['terminal_fcff'],v['terminal_nopat']-v['terminal_reinvestment'],abs_tol=1e-9)
 assert math.isclose(v['ev'],sum(row['pv_fcff'] for row in v['rows'])+v['pv_terminal'],abs_tol=1e-8)
 assert math.isclose(v['equity'],v['ev']+net_adjustment,abs_tol=1e-8)
 assert math.isclose(v['rows'][-1]['growth'],case['g'],abs_tol=1e-12)
 assert math.isclose(v['rows'][-1]['ebit_margin'],case['terminal_margin'],abs_tol=1e-12)
assert abs(sum(bridge[k] for k in ['cash_fcf','remove_sbc','unresolved_other_cfo_adjustments','replace_net_income_with_normalized_nopat'])-bridge['normalized_fcff_before_wc'])<1e-8
(P/'results.json').write_text(json.dumps(results,indent=2));print(json.dumps({k:results[k] for k in ['bridge_rmb_m','discount','scenarios','inverse_diagnostic']},indent=2))
