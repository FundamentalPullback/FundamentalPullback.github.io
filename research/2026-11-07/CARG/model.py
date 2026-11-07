"""CARG: deterministic research model. USD millions except per share/dealers.
Run python model.py. All forecasts analyst estimates, not company guidance.
Sources and accounting policy in report.md/sources.json. No trading output.
"""
import json, math, pathlib
P=pathlib.Path(__file__).parent
PRICE=33.74
SHARES=75.632371+13.763613+1.016344
CASH=164.910; OPERATING_CASH=35.; FINANCE_LEASE_PROXY=.1
BRIDGE=CASH-OPERATING_CASH-FINANCE_LEASE_PROXY
WACC=.0486+1.24*.0441
SCENARIOS={
 'adverso':dict(ud=[-.02,0,.005,.005,.005],up=[0,.01,.02,.02,.02],id=[.01,.01,.02,.02,.02],ip=[.02,.03,.03,.03,.03],other=[0,.01,.02,.02,.02],m=[.22,.22,.225,.23,.23],mt=.22,w=.115,g=.02,roic=.15,cap=.043),
 'central':dict(ud=[.015,.013,.012,.01,.008],up=[.05,.045,.04,.035,.03],id=[.04,.035,.03,.025,.02],ip=[.07,.06,.05,.04,.03],other=[.05,.04,.04,.03,.03],m=[.26,.265,.27,.275,.28],mt=.265,w=WACC,g=.025,roic=.20,cap=.038),
 'favorable':dict(ud=[.025,.025,.02,.02,.015],up=[.07,.06,.055,.05,.04],id=[.05,.05,.04,.035,.03],ip=[.10,.09,.08,.07,.06],other=[.08,.07,.06,.05,.04],m=[.28,.29,.30,.31,.31],mt=.29,w=.095,g=.03,roic=.25,cap=.038)}
# Quarterly ending dealer counts are a proxy for quarterly average billable dealers.
# Revenue residual deliberately absorbs advertising, timing and KPI-definition differences.
US0=26402*8308*4/1e6; INT0=8299*2715*4/1e6; OTHER0=258.366*4-US0-INT0
SCALE=1014/(258.366*4)
def model(case='central',w=None,g=None,margin_shift=0,price_growth_shift=0):
 s=SCENARIOS[case]; w=s['w'] if w is None else w; g=s['g'] if g is None else g
 assert w>g and s['roic']>g, 'Invalid terminal assumptions'
 ud,up,idd,ip=26402.,8308.*SCALE,8299.,2715.*SCALE;other=OTHER0*SCALE
 rev0=1014.; rows=[]
 for t in range(1,11):
  if t<=5:
   ug=s['ud'][t-1];pg=s['up'][t-1]+price_growth_shift;ig=s['id'][t-1];iq=s['ip'][t-1]+price_growth_shift;og=s['other'][t-1]
   margin=s['m'][t-1]+margin_shift
  else:
   f=(t-5)/5
   # Fade EACH physical revenue component to the SAME terminal growth g.
   ug=s['ud'][-1]*(1-f);pg=(s['up'][-1]+price_growth_shift)*(1-f)+g*f
   ig=s['id'][-1]*(1-f);iq=(s['ip'][-1]+price_growth_shift)*(1-f)+g*f
   og=s['other'][-1]*(1-f)+g*f;margin=(s['m'][-1]+margin_shift)*(1-f)+(s['mt']+margin_shift)*f
  ud*=1+ug;up*=1+pg;idd*=1+ig;ip*=1+iq;other*=1+og
  us=ud*up*4/1e6;intl=idd*ip*4/1e6;rev=us+intl+other
  ebit=rev*margin;nopat=ebit*.75;da=rev*.032;dnwc=(rev-rev0)*.02
  ordinary_capex=rev*s['cap'] # cash capex + economic capitalized SBC
  reinvest0=ordinary_capex-da+dnwc
  if t<=5: reinvest=reinvest0
  else:
   f=(t-5)/5;reinvest=reinvest0*(1-f)+(nopat*g/s['roic'])*f
  capex=da+reinvest-dnwc
  fcff=nopat+da-capex-dnwc
  row=dict(year=2026+t,us_dealers=ud,us_quarterly_yield=up,int_dealers=idd,int_quarterly_yield=ip,other_revenue=other,us_subscription=us,int_subscription=intl,revenue=rev,growth=rev/rev0-1,ebit_margin=margin,ebit=ebit,tax=.25,nopat=nopat,da=da,economic_capex=capex,capitalized_sbc=rev*.0055,cash_capex=capex-rev*.0055,dnwc=dnwc,reinvestment=reinvest,fcff=fcff,pv=fcff/(1+w)**t)
  assert abs(fcff-(nopat-reinvest))<1e-8 and capex>=0
  rows.append(row);rev0=rev
 nt=rows[-1]['nopat']*(1+g);rt=nt*g/s['roic'];ft=nt-rt;tv=ft/(w-g);pvt=tv/(1+w)**10;ev=sum(x['pv'] for x in rows)+pvt
 return dict(case=case,wacc=w,g=g,terminal_roic=s['roic'],rows=rows,terminal_nopat=nt,terminal_reinvestment=rt,terminal_fcff=ft,terminal_ev=tv,pv_terminal=pvt,terminal_weight=pvt/ev,ev=ev,equity=ev+BRIDGE,shares=SHARES,fair=(ev+BRIDGE)/SHARES,upside=(ev+BRIDGE)/SHARES/PRICE-1,bridge=BRIDGE)
def solve(which):
 lo,hi=(-.1,.2) if which=='price_growth_shift' else (-.15,.2)
 for _ in range(100):
  mid=(lo+hi)/2
  if model(**{which:mid})['fair']<PRICE:lo=mid
  else:hi=mid
 return mid
annual={
 '2023':dict(rev=698.421,ebit=120.329,ni=92.435,eps=.81,cfo=124.527,cash_capex=41.211,sbc=63.737,da=48.474,discontinued_loss=70.382),
 '2024':dict(rev=798.044,ebit=157.147,ni=128.737,eps=1.21,cfo=255.494,cash_capex=93.949,sbc=62.272,da=25.360,discontinued_loss=107.765),
 '2025':dict(rev=906.980,ebit=244.445,ni=196.742,eps=1.96,cfo=295.280,cash_capex=29.316,sbc=50.439,da=28.346,discontinued_loss=40.839)}
q={
 '2025Q4':dict(rev=241.094,ebit=69.127,ni=53.738,eps=.56,cfo=83.117,cash_capex=6.684,sbc=11.887,da=7.754,impair=0),
 '2026Q1':dict(rev=243.555,ebit=40.079,ni=32.228,eps=.34,cfo=69.849,cash_capex=6.692,sbc=13.272,da=7.170,impair=19.711),
 '2026Q2':dict(rev=250.971,ebit=62.982,ni=49.193,eps=.54,cfo=94.591,cash_capex=6.910,sbc=13.358,da=7.929,impair=.450),
 '2026Q3':dict(rev=258.366,ebit=67.932,ni=52.789,eps=.59,cfo=80.813,cash_capex=6.943,sbc=13.003,da=8.722,impair=0)}
ttm={k:sum(x[k] for x in q.values()) for k in q['2025Q4']};ttm['reported_fcf']=ttm['cfo']-ttm['cash_capex'];ttm['norm_ebit']=ttm['ebit']+ttm['impair']
prior=dict(rev=210.244+665.886,ebit=57.762+175.318,ni=48.075+143.004,eps=.45+1.41,cfo=75.737+212.163,cash_capex=13.698+22.632,impair=.499)
prior['norm_ebit']=prior['ebit']+prior['impair'];prior['reported_fcf']=prior['cfo']-prior['cash_capex']
# Normalized CFO-to-FCFF bridge: exact reported reconciliation, followed by economic adjustments.
normal_fcff=ttm['norm_ebit']*.75+(7.514+23.821)-ttm['cash_capex']-5.5-2.38
# Historical price 20 Feb2026 after FY2025 reporting; same continuing-operations GAAP EPS definition.
historical_pe=30.17/1.96
out=dict(price=PRICE,price_date='2026-11-06',price_time='16:00 America/New_York (regular-session daily close)',scanner_last=33.74,annual=annual,quarters=q,ttm=ttm,prior_ttm=prior,normalized_ttm_fcff=normal_fcff,historical_pe=historical_pe,current_ttm_pe=PRICE/ttm['eps'],historical_pe_applied_to_current_eps=historical_pe*ttm['eps'],scenarios={k:model(k) for k in SCENARIOS},sensitivity=[dict(wacc=w,g=g,fair=model(w=w,g=g)['fair']) for w in [.09,.10,WACC,.11,.12] for g in [.02,.025,.03]],inverse=dict(price_growth_shift=solve('price_growth_shift'),margin_shift=solve('margin_shift')),cash_normalization=dict(reported_fcf=ttm['reported_fcf'],expensed_sbc=ttm['sbc'],capitalized_sbc_estimate=5.5,deferred_tax_timing=24.496,normalized_fcff=normal_fcff),checks=dict(horizon=10,explicit=5,transition=5,all_wacc_gt_g=all(s['w']>s['g'] for s in SCENARIOS.values()),no_future_buybacks=True,leases_operating_expense=True,sbc_retained_in_ebit=True))
out['cash_normalization']['exact_bridge']=[['FCF publicado',301.141],['Quitar SBC devuelta en CFO',-51.52],['Sustituir beneficio neto consolidado por NOPAT normalizado',11.20275],['Eliminar impuestos diferidos no monetarios',-24.496],['Eliminar devolución impairment en CFO',-20.161],['Eliminar resto ajustes CFO y movimiento circulante netos',-16.61],['D&A discontinuada Q4 2025',-.240],['SBC capitalizada económica estimada',-5.5],['Inversión normalizada circulante',-2.38]]
out['cash_normalization']['bridge_sum']=sum(v for _,v in out['cash_normalization']['exact_bridge'])
assert abs(out['cash_normalization']['bridge_sum']-normal_fcff)<1e-8
# Independent audit controls and explicit source-line reconciliation (FY25 - 9M25 + 9M26).
rest_lines={
 'currency':[-.404,-.446,.197], 'other_non_cash':[-.101,-.101,0.],
 'doubtful_accounts':[2.415,2.047,2.143], 'financing_amortization':[.515,.387,.474],
 'contract_amortization':[16.406,11.986,14.510], 'receivables':[.675,3.404,-7.383],
 'inventory':[.338,.338,0.], 'prepaids':[-7.790,-8.452,14.790],
 'contract_costs':[-19.240,-13.707,-13.489], 'payables':[3.557,4.227,1.948],
 'accrued_liabilities':[.336,-6.058,3.994], 'deferred_revenue':[1.853,1.933,2.091],
 'lease_obligations':[3.593,4.838,-4.422]}
out['cash_normalization']['other_cfo_line_inputs_fy25_9m25_9m26']=rest_lines
out['cash_normalization']['other_cfo_ttm_lines']={k:a-b+c for k,(a,b,c) in rest_lines.items()}
assert abs(sum(out['cash_normalization']['other_cfo_ttm_lines'].values())-16.610)<1e-8
assert abs((155.903-106.105+134.210)-184.008)<1e-8
assert abs((25.887-13.966+12.575)-24.496)<1e-8
for result in out['scenarios'].values():
 assert abs(result['rows'][-1]['growth']-result['g'])<1e-10
 assert abs(result['rows'][-1]['reinvestment']/result['rows'][-1]['nopat']-result['g']/result['terminal_roic'])<1e-10
 assert abs(result['terminal_fcff']/result['rows'][-1]['fcff']-(1+result['g']))<1e-10
for name,shift in out['inverse'].items():
 assert abs(model(**{name:shift})['fair']-PRICE)<1e-8
out['illustrative_audit_sensitivity']={'year_end_delay_years':.15,
 'year_end_delayed_no_stub_fair':{k:(v['ev']/(1+v['wacc'])**.15+BRIDGE)/SHARES for k,v in out['scenarios'].items()},
 'note':'Diagnostic only: delays all annual cash flows and terminal value 0.15 years; no Q4 2026 stub added; not a revised base case.'}
out['checks'].update(other_cfo_lines_tie=True,terminal_components_tie=True,inverse_prices_tie=True)
P.joinpath('results.json').write_text(json.dumps(out,indent=2))
for k,m in out['scenarios'].items():print(k,round(m['fair'],2),round(m['upside']*100,2),round(m['terminal_weight']*100,2))
print('TTM',ttm,'prior',prior,'normal FCFF',normal_fcff,'inverse',out['inverse'])
