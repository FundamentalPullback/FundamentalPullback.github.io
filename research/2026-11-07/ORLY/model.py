import json, pathlib
P=pathlib.Path(__file__).parent
CLOSE=89.89
# Millions USD and million shares. All recurring SBC remains in EBIT.
FY={2023:dict(sales=15812.250,ebit=3186.376,ni=2346.581,cfo=3034.084,da=409.061,capex=1006.264,sbc=27.511,interest=201.668,eps=2.56),2024:dict(sales=16708.479,ebit=3251.157,ni=2386.680,cfo=3049.576,da=461.892,capex=1023.387,sbc=28.931,interest=222.548,eps=2.71),2025:dict(sales=17781.992,ebit=3460.612,ni=2538.209,cfo=2761.993,da=511.230,capex=1168.815,sbc=35.115,interest=235.064,eps=2.97)}
YTD25=dict(sales=13367.678,ebit=2632.003,ni=1932.976,cfo=2128.501,da=375.825,capex=899.783,sbc=27.108,interest=174.467,eps=2.25)
YTD26=dict(sales=14573.842,ebit=2925.645,ni=2104.866,cfo=2598.155,da=413.189,capex=860.273,sbc=26.289,interest=214.466,eps=2.54)
Q1=dict(sales=4560.539,ebit=841.608,ni=604.181,cfo=1032.913,da=135.361,capex=244.447,sbc=8.816,interest=62.745,eps=.72)
H1=dict(sales=9452.552,ebit=1827.354,ni=1319.245,cfo=2039.412,da=273.643,capex=552.050,sbc=17.512,interest=132.616,eps=1.58)
def sub(a,b):return {k:a[k]-b[k] for k in a}
QUARTERS={'Q4_2025':sub(FY[2025],YTD25),'Q1_2026':Q1,'Q2_2026':sub(H1,Q1),'Q3_2026':sub(YTD26,H1)}
# EPS sum quarters differs annual diluted EPS because weighted shares change.
QUARTERS['Q4_2025']['eps']=.71;QUARTERS['Q2_2026']['eps']=.86;QUARTERS['Q3_2026']['eps']=.97
TTM={k:sum(q[k] for q in QUARTERS.values()) for k in Q1}
# Normalized tax assumption, close to 9M2026 reported 22.8%; not a cash-tax forecast.
TAX=.227
# Sep30 principal debt includes current maturities refinanced in CP, not added twice.
# Nov6 repurchase outlay conservatively entirely debt-funded; no credit for interim CFO.
DEBT=7750+262.8
# Minimum operating cash 200 exceeds reported cash 194.445: zero excess cash.
EXCESS_CASH=0
SHARES=804.607512-3.0+3.350 # Nov6 buyback approximation + Q3 incremental options
E=CLOSE*SHARES;D=DEBT
# Rf is RBC report snapshot dated Nov6, not verified end-of-day yield.
rf=.0486;beta=.75;erp=.0441;kd=.05581
WACC=(rf+beta*erp)*E/(E+D)+kd*(1-TAX)*D/(E+D)
SCENARIOS={
 'conservador':dict(growth=[.04,.04,.04,.035,.03],margin=.18,wacc=.09,g=.02,roic=.15,capex=[.07,.068,.066,.064,.062]),
 'base':dict(growth=[.07,.06,.055,.05,.045],margin=.1955,wacc=WACC,g=.025,roic=.20,capex=[.067,.064,.061,.058,.055]),
 'favorable':dict(growth=[.085,.08,.075,.07,.065],margin=.205,wacc=.07,g=.03,roic=.25,capex=[.064,.061,.058,.055,.052])}
def value(cfg,extra_wc=0):
 s=TTM['sales'];rows=[];last_margin=(TTM['ebit']-39)/s;last_reinv=None
 for t in range(1,11):
  u=max(0,(t-5)/5);growth=cfg['growth'][t-1] if t<=5 else cfg['growth'][-1]*(1-u)+cfg['g']*u
  prev=s;s*=1+growth;m=last_margin+(cfg['margin']-last_margin)*min(t/3,1);nopat=s*m*(1-TAX);da=s*.03;wc=(s-prev)*.03
  if t<=5:
   cap=s*cfg['capex'][t-1];reinv=cap-da+wc;last_reinv=reinv/nopat
  else:
   rate=last_reinv*(1-u)+(cfg['g']/cfg['roic'])*u;reinv=nopat*rate;cap=da+reinv-wc
  fcff=nopat+da-cap-wc-(extra_wc if t==1 else 0)
  rows.append(dict(year=t,phase='explicita' if t<=5 else 'transicion',sales=s,growth=growth,margin=m,nopat=nopat,da=da,capex=cap,delta_nwc=wc,reinvestment=reinv,fcff=fcff,pv=fcff/(1+cfg['wacc'])**t))
 terminal_nopat=rows[-1]['nopat']*(1+cfg['g']);terminal_fcff=terminal_nopat*(1-cfg['g']/cfg['roic']);tv=terminal_fcff/(cfg['wacc']-cfg['g']);pvtv=tv/(1+cfg['wacc'])**10;ev=sum(r['pv'] for r in rows)+pvtv;equity=ev-DEBT+EXCESS_CASH
 terminal_sales=rows[-1]['sales']*(1+cfg['g'])
 terminal_da=terminal_sales*.03
 terminal_wc=(terminal_sales-rows[-1]['sales'])*.03
 terminal_reinvestment=terminal_nopat*cfg['g']/cfg['roic']
 terminal_capex=terminal_da+terminal_reinvestment-terminal_wc
 assert cfg['wacc']>cfg['g'] and 0<cfg['g']/cfg['roic']<1
 assert all(r['capex']>=r['da'] and r['reinvestment']>0 for r in rows)
 assert abs(terminal_nopat+terminal_da-terminal_capex-terminal_wc-terminal_fcff)<1e-7
 assert abs(rows[-1]['fcff']*(1+cfg['g'])-terminal_fcff)<1e-7
 terminal_components=dict(sales=terminal_sales,nopat=terminal_nopat,da=terminal_da,capex=terminal_capex,delta_nwc=terminal_wc,reinvestment=terminal_reinvestment,fcff=terminal_fcff)
 return dict(value=equity/SHARES,terminal_components=terminal_components,ev=ev,equity=equity,terminal_fcff=terminal_fcff,terminal_pv_fraction=pvtv/ev,rows=rows,mos=1-CLOSE/(equity/SHARES))
R={k:value(v) for k,v in SCENARIOS.items()}
SENS=[dict(wacc=w,g=g,value=value({**SCENARIOS['base'],'wacc':w,'g':g})['value']) for w in [.07,.075,.08,.085,.09] for g in [.02,.025,.03]]
# Implied growth in years1-5 constant, fade toward unchanged terminal growth over years6-10.
lo,hi=-.05,.30
for _ in range(100):
 mid=(lo+hi)/2;v=value({**SCENARIOS['base'],'growth':[mid]*5})['value']
 if v<CLOSE:lo=mid
 else:hi=mid
INVERSE=(lo+hi)/2
for a in [*FY.values(),*QUARTERS.values(),TTM]:a['cfo_capex']=a['cfo']-a['capex'];a['cash_after_sbc']=a['cfo_capex']-a['sbc'];a['operating_margin']=a['ebit']/a['sales']
result=dict(asof='2026-11-07',price={'regular_close':CLOSE,'session_date':'2026-11-06','session_time':'16:00 America/New_York','scanner_Last':89.85},annual=FY,quarters=QUARTERS,ttm=TTM,cost_capital=dict(rf=rf,beta=beta,erp=erp,kd=kd,tax=TAX,equity_weight=E/(E+D),wacc=WACC),bridge=dict(principal_debt_September30=7750,post_period_buyback_outlay=262.8,modeled_debt=DEBT,reported_cash=194.445,minimum_cash=200,excess_cash=0,shares=SHARES,operating_leases=2584.934,lease_treatment='rent expensed; no lease debt subtraction',supplier_finance=5100,supplier_treatment='operating accounts payable; separate unwind stress'),assumptions=SCENARIOS,scenarios=R,sensitivity=SENS,implied_five_year_growth=INVERSE,supplier_stress_20pct=value(SCENARIOS['base'],1020)['value'],normalized_ttm_ebit=TTM['ebit']-39,normalized_cash_after_sbc_tariff=TTM['cash_after_sbc']-39*(1-TAX),price_ceiling_15pct=R['base']['value']*.85,current_pe_sum_quarter_eps=CLOSE/TTM['eps'])
(P/'results.json').write_text(json.dumps(result,indent=2));print(json.dumps({k:result[k] for k in ['cost_capital','implied_five_year_growth','supplier_stress_20pct','price_ceiling_15pct','current_pe_sum_quarter_eps']},indent=2));print({k:round(v['value'],2) for k,v in R.items()})
