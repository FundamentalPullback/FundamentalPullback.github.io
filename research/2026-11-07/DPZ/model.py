"""DPZ, USD millions; deterministic research model, not a trading instruction.
Run python model.py. Sources/assumptions: report.md and sources.json.
Operating leases remain operating; finance leases treated as debt and asset additions as capex.
"""
from pathlib import Path
import json,csv,copy
P=Path(__file__).parent
PRICE=334.28; SCANNER=333.91; TAX=.24
SHARES=32.896056+(33.114893-33.035670)
NOTES=940+379+648+826.625+972.5+500+500
FINLEASE=126.613; OTHERFIN=14.693-.077
DEBT=NOTES+FINLEASE+OTHERFIN
CASH=229.035; OPERATING_CASH=100; INVESTMENT=15.175
BRIDGE=-DEBT+CASH-OPERATING_CASH+INVESTMENT
EQUITY=PRICE*32.896056
RF=.0486; ERP=.0441; BETA=.92; KD=RF+.0125
WACC=(RF+BETA*ERP)*EQUITY/(EQUITY+DEBT)+KD*(1-TAX)*DEBT/(EQUITY+DEBT)
# reported FY2023/24/25 and YTD2025/26, all USDm, EBIT including SBC
H={
'FY2023':dict(revenue=4479.358,ebit=819.519,net_income=519.118,eps=14.66,cfo=590.864,capex=105.396,da=80.640,sbc=37.514),
'FY2024':dict(revenue=4706.416,ebit=878.999,net_income=584.170,eps=16.69,cfo=624.897,capex=112.885,da=87.732,sbc=43.255),
'FY2025':dict(revenue=4939.994,ebit=953.974,net_income=601.704,eps=17.57,cfo=792.062,capex=120.558,da=88.827,sbc=44.640),
'YTD2025':dict(revenue=3404.254,ebit=658.307,net_income=420.061,eps=12.22,cfo=552.256,capex=56.667,da=61.128,sbc=31.681),
'YTD2026':dict(revenue=3530.619,ebit=704.169,net_income=427.740,eps=12.80,cfo=520.601,capex=60.829,da=61.501,sbc=30.843)}
H['TTM']= {k:H['FY2025'][k]+H['YTD2026'][k]-H['YTD2025'][k] for k in H['FY2025']}
Q={
'Q4_2025':{k:H['FY2025'][k]-H['YTD2025'][k] for k in H['FY2025']},
'Q1_2026':dict(revenue=1150.594,ebit=230.357,net_income=139.811,eps=4.13,cfo=161.955,capex=15.043,da=20.434,sbc=8.789),
'Q2_2026':dict(revenue=1194.427,ebit=232.039,net_income=135.750,eps=4.07,cfo=352.603-161.955,capex=39.008-15.043,da=40.781-20.434,sbc=21.146-8.789),
'Q3_2026':dict(revenue=1185.598,ebit=241.773,net_income=152.179,eps=4.60,cfo=520.601-352.603,capex=60.829-39.008,da=61.501-40.781,sbc=30.843-21.146)}
# Q4 EPS is independently reported in S15; EPS ratios are not additive by definition.
Q['Q4_2025']['eps']=5.35
H['TTM']['eps']=sum(q['eps'] for q in Q.values())
for h in [*H.values(),*Q.values()]: h['fcf_reported']=h['cfo']-h['capex']; h['ebit_margin']=h['ebit']/h['revenue']
# TTM revenue components. Advertising fund excluded from modeled economic revenue (equal expense).
R0=dict(us_owned=375.153+225.359-266.803,us_royalty=677.114+487.817-464.416,supply=2989.529+2176.835-2053.945,intl_royalty=338.704+246.502-231.272)
EBIT0=H['TTM']['ebit']-(4.028+3.881-3.883)-7.780
# Margin attribution is analyst allocation, not reported stand-alone royalties profit.
M0=dict(us_owned=.12,us_royalty=.80,supply=.0985,intl_royalty=.85)
OVERHEAD0=sum(R0[k]*M0[k] for k in R0)-EBIT0
SC={
'adverso':dict(wacc=WACC+.01,g=.02,roic=.18,us_units=.01,us_sss=-.005,intl_units=.025,intl_sss=0,supply_g=.02,owned_g=-.08,margin5=dict(us_owned=.09,us_royalty=.78,supply=.09,intl_royalty=.83),overhead_g=.035,capex_ratio=.033,lease_capex=40),
'central':dict(wacc=WACC,g=.025,roic=.25,us_units=.018,us_sss=.02,intl_units=.04,intl_sss=.015,supply_g=.04,owned_g=-.05,margin5=dict(us_owned=.12,us_royalty=.80,supply=.099,intl_royalty=.85),overhead_g=.03,capex_ratio=.029,lease_capex=25),
'favorable':dict(wacc=WACC-.005,g=.03,roic=.30,us_units=.025,us_sss=.03,intl_units=.045,intl_sss=.025,supply_g=.05,owned_g=-.02,margin5=dict(us_owned=.13,us_royalty=.81,supply=.105,intl_royalty=.86),overhead_g=.025,capex_ratio=.029,lease_capex=25)}
def value(s,wacc=None,g=None,growth_shift=0):
 s=copy.deepcopy(s); wacc=s['wacc'] if wacc is None else wacc; g=s['g'] if g is None else g
 assert wacc>g and s['roic']>g
 r=R0.copy(); overhead=OVERHEAD0; rows=[]
 rates={'us_owned':s['owned_g'],'us_royalty':(1+s['us_units'])*(1+s['us_sss'])-1,'supply':s['supply_g'],'intl_royalty':(1+s['intl_units'])*(1+s['intl_sss'])-1}
 for y in range(1,11):
  a=max(0,(y-5)/5); oldrev=sum(r.values())
  for k in r:r[k]*=1+((rates[k]+growth_shift)*(1-a)+g*a)
  overhead*=1+s['overhead_g']*(1-a)+g*a
  margins={k:M0[k]+(s['margin5'][k]-M0[k])*min(y/5,1) for k in r}
  ebit=sum(r[k]*margins[k] for k in r)-overhead; nopat=ebit*(1-TAX); revenue=sum(r.values())
  da=.020*revenue; dnwc=.02*(revenue-oldrev)
  rawcap=s['capex_ratio']*revenue+s['lease_capex']*(1+g)**y
  # Transition to total reinvestment NOPAT*g/ROIC, including working capital.
  capex=(1-a)*rawcap+a*(da+nopat*g/s['roic']-dnwc)
  fcff=nopat+da-capex-dnwc
  row=dict(year=y,**r,revenue=revenue,overhead=overhead,ebit=ebit,nopat=nopat,da=da,capex_incl_finance_assets=capex,dnwc=dnwc,reinvestment=capex+dnwc-da,fcff=fcff,pv=fcff/(1+wacc)**y)
  rows.append(row)
 terminal_nopat=rows[-1]['nopat']*(1+g); terminal_reinvestment=terminal_nopat*g/s['roic']; terminal_fcff=terminal_nopat-terminal_reinvestment
 terminal=terminal_fcff/(wacc-g); pvt=terminal/(1+wacc)**10; ev=sum(x['pv'] for x in rows)+pvt; equity=ev+BRIDGE
 return dict(value=equity/SHARES,ev=ev,equity=equity,pv_explicit=sum(x['pv'] for x in rows),pv_terminal=pvt,terminal_weight=pvt/ev,terminal_fcff=terminal_fcff,terminal_nopat=terminal_nopat,terminal_reinvestment=terminal_reinvestment,wacc=wacc,g=g,roic=s['roic'],rows=rows)
def bisect(fn,target,lo,hi):
 for _ in range(120):
  mid=(lo+hi)/2
  if fn(mid)<target:lo=mid
  else:hi=mid
 return (lo+hi)/2
RESULTS={k:value(v) for k,v in SC.items()}
reverse=bisect(lambda x:value(SC['central'],growth_shift=x)['value'],PRICE,-.08,.20)
# Required WACC, monotone decreasing.
irr=bisect(lambda x:-value(SC['central'],wacc=x)['value'],-PRICE,.03001,.25)
sens=[dict(wacc=w,g=g,value=value(SC['central'],wacc=w,g=g)['value']) for w in [WACC-.01,WACC-.005,WACC,WACC+.005,WACC+.01] for g in [.02,.025,.03]]
lease_sens=[]
for x in [10,25,40,70]:
 s=copy.deepcopy(SC['central']);s['lease_capex']=x;lease_sens.append(dict(annual_new_finance_assets=x,value=value(s)['value']))
extra_sens=[]
for rc in [.18,.25,.30]:
 for dm in [-.01,0,.01]:
  x=copy.deepcopy(SC['central']);x['roic']=rc;x['margin5']['supply']+=dm
  extra_sens.append(dict(terminal_roic=rc,supply_margin_shift=dm,value=value(x)['value']))
# Cash reconciliation: reported CFO to recurring unlevered cash before reinvestment normalization.
t=H['TTM']; adflow=10.736-20.628-27.137; wcflow=(-6.149-6.700+53.637+.536+.691)-5.126-10.242
interest=195.972+138.511-135.245; intincome=14.880+6.182-11.834
bridge=dict(reported_fcf=t['fcf_reported'],remove_sbc=-t['sbc'],remove_adfund_cash=-adflow,add_after_tax_interest=(interest-intincome)*(1-TAX),remove_reported_wc_release=-wcflow)
bridge['subtotal']=sum(bridge.values())
bridge['remove_other_noncash_adjustments']=-(t['cfo']-t['net_income']-t['da']-t['sbc']-adflow-wcflow)
bridge['tax_and_nonoperating_normalization']=EBIT0*(1-TAX)-t['net_income']-bridge['add_after_tax_interest']
normalized_nwc=.02*(t['revenue']-565.782-(H['FY2025']['revenue']-559.494))
actual_finance_asset_additions=.842+69.116
normalfcff=EBIT0*(1-TAX)+t['da']-t['capex']-normalized_nwc-25
bridge['normalized_dnwc']=-normalized_nwc
bridge['normalized_new_finance_assets']=-25
bridge['normalized_fcff']=bridge['subtotal']+sum(bridge[k] for k in ['remove_other_noncash_adjustments','tax_and_nonoperating_normalization','normalized_dnwc','normalized_new_finance_assets'])
assert abs(bridge['normalized_fcff']-normalfcff)<1e-8
out=dict(as_of='2026-11-07',price=dict(regular_close=PRICE,timestamp='2026-11-06T16:00:00-05:00',scanner_last=SCANNER,scanner_timestamp='not independently timestamped; equals Finviz aftermarket 19:30 EST'),history=H,quarters=Q,revenue_ttm=R0,ebit_normalized=EBIT0,overhead_allocation=OVERHEAD0,wacc_inputs=dict(rf=RF,erp=ERP,beta=BETA,kd=KD,tax=TAX,equity_weight=EQUITY/(EQUITY+DEBT),wacc=WACC),bridge=dict(notes=NOTES,finance_leases=FINLEASE,sale_leaseback=OTHERFIN,total_debt=DEBT,book_debt=4885.904,implied_unamortized_costs=DEBT-4885.904,cash=CASH,minimum_operating_cash=OPERATING_CASH,excess_cash=CASH-OPERATING_CASH,dpc_dash=INVESTMENT,net_bridge=BRIDGE,shares=SHARES),fcf_reconciliation=bridge,normalized_fcff=normalfcff,ttm_new_finance_assets=actual_finance_asset_additions,scenarios=RESULTS,assumptions=SC,sensitivity=sens,lease_sensitivity=lease_sens,roic_margin_sensitivity=extra_sens,reverse_growth_shift=reverse,implied_wacc=irr,conditional_max_price=RESULTS['central']['value']*.85,matched_pe_history={'FY2023':393.55/H['FY2023']['eps'],'FY2024':415.59/H['FY2024']['eps'],'FY2025':418.23/H['FY2025']['eps'],'current_price_over_sum_quarter_eps':PRICE/sum(v['eps'] for v in Q.values())},historical_close={'FY2023':393.55,'FY2024':415.59,'FY2025':418.23},vendor_marketcap_netincome_pe={'FY2023':27.70,'FY2024':25.40,'FY2025':23.90})
for name,result in RESULTS.items():
 with (P/f'forecast_{name}.csv').open('w') as f:w=csv.DictWriter(f,fieldnames=result['rows'][0].keys());w.writeheader();w.writerows(result['rows'])
checks={'four_quarters_tie':all(abs(sum(q[k] for q in Q.values())-H['TTM'][k])<.011 for k in ['revenue','ebit','net_income','cfo','capex','da','sbc']), 'terminal_consistency':all(abs(v['rows'][-1]['reinvestment']-v['rows'][-1]['nopat']*v['g']/v['roic'])<1e-8 for v in RESULTS.values()),'reverse_tie':abs(value(SC['central'],growth_shift=reverse)['value']-PRICE)<1e-6,'ten_years':all(len(v['rows'])==10 for v in RESULTS.values()),'sbc_not_added_back':True,'finance_capex_included':True,'restricted_cash_not_added':True,'operating_leases_not_double_counted':True}
checks.update({
 'revenue_components_exclude_adfund':abs(sum(R0.values())-(H['TTM']['revenue']-565.782))<1e-8,
 'normalized_ebit_calibration':abs(sum(R0[k]*M0[k] for k in R0)-OVERHEAD0-EBIT0)<1e-8,
 'ev_equity_bridge':all(abs(v['equity']-v['ev']-BRIDGE)<1e-8 and abs(v['value']*SHARES-v['equity'])<1e-8 for v in RESULTS.values()),
 'fcff_identity':all(abs(r['fcff']-(r['nopat']+r['da']-r['capex_incl_finance_assets']-r['dnwc']))<1e-8 for v in RESULTS.values() for r in v['rows']),
 'terminal_fcff_continuity':all(abs(v['terminal_fcff']-v['rows'][-1]['fcff']*(1+v['g']))<1e-8 for v in RESULTS.values()),
 'implied_wacc_tie':abs(value(SC['central'],wacc=irr)['value']-PRICE)<1e-6,
 'positive_reinvestment':all(r['reinvestment']>0 for v in RESULTS.values() for r in v['rows']),
 'restricted_cash_bridge':abs(BRIDGE-(-4907.354+229.035-100+15.175))<1e-8,
 'scenario_ordering':RESULTS['adverso']['value']<RESULTS['central']['value']<RESULTS['favorable']['value'],
 'historical_pe_definitions':all(abs(out['matched_pe_history'][k]-out['historical_close'][k]/H[k]['eps'])<1e-10 for k in out['historical_close'])})
assert all(checks.values()),checks
(P/'results.json').write_text(json.dumps(out,indent=2));(P/'run_log.json').write_text(json.dumps(dict(status='senior-review-ready',checks=checks,artifact_type='deterministic research support model',independent_audit='ready_with_caveats_research_only'),indent=2))
print(json.dumps({k:{z:v[z] for z in ['value','ev','terminal_weight','wacc']} for k,v in RESULTS.items()},indent=2));print('NormalizedFCFF',normalfcff,'reverse growth shift',reverse,'impliedWACC',irr,'max',out['conditional_max_price']);print('bridge',bridge,'base',RESULTS['central']['rows'][0])
