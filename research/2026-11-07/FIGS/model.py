"""FIGS screening FCFF; USD millions; assumptions are not company guidance unless marked."""
import json,csv
from pathlib import Path
P=Path(__file__).parent
# Historical inputs frozen from SEC companyfacts; extract_history.py rebuilds from archived source.
h={'2023': {'revenue': 545.646, 'ebit': 34.045, 'cfo': 100.915, 'capex': 16.348, 'sbc': 45.799, 'da': 2.942, 'reported_fcf': 84.56700000000001}, '2024': {'revenue': 555.558, 'ebit': 2.265, 'cfo': 81.162, 'capex': 17.021, 'sbc': 42.673, 'da': 6.694, 'reported_fcf': 64.141}, '2025': {'revenue': 631.098, 'ebit': 38.147, 'cfo': 61.17, 'capex': 8.168, 'sbc': 26.874, 'da': 9.035, 'reported_fcf': 53.002}, 'Q4_2025': {'revenue': 201.89599999999996, 'ebit': 18.808, 'cfo': 60.928000000000004, 'capex': 2.8629999999999995, 'sbc': 5.190999999999999, 'da': 2.5570000000000004, 'reported_fcf': 58.065000000000005}, 'Q1_2026': {'revenue': 159.902, 'ebit': 4.483, 'cfo': -3.204, 'capex': 2.424, 'sbc': 5.451, 'da': 3.411, 'reported_fcf': -5.628}, 'Q2_2026': {'revenue': 196.61900000000003, 'ebit': 35.262, 'cfo': 46.857, 'capex': 2.602, 'sbc': 6.7299999999999995, 'da': 2.371, 'reported_fcf': 44.254999999999995}, 'Q3_2026': {'revenue': 190.68900000000002, 'ebit': 22.209000000000003, 'cfo': 56.86900000000001, 'capex': 5.693, 'sbc': 7.421000000000001, 'da': 2.333, 'reported_fcf': 51.176000000000016}, 'TTM_Sep2026': {'revenue': 749.106, 'ebit': 80.762, 'cfo': 161.45000000000002, 'capex': 13.581999999999999, 'sbc': 24.793, 'da': 10.672, 'reported_fcf': 147.86800000000002}}
price=19.82;rf=.0486;erp=.0441;beta=1.06;wacc=rf+beta*erp
shares=(157487979+8283641+23942640+3337542)/1e6
cash=76.470+254.696;reserve=75.;equity_investment=0.;netcash=cash-reserve
base=631.098*1.235
# FY26 bridge: adjusted EBITDA guidance15.8%, SBC/payroll3.6%, D&A1.4% => EBIT10.8%.
# Model starts FY27: FY26 anchor is not yet audited; no Q4 stub cash added.
def model(g=.15,m5=.14,mt=.14,roic=.20,terminalroic=.15,w=wacc,gt=.025,sales_to_capital=3.):
 revenue=base;previousnopat=base*.108*.75;pv=0.;rows=[]
 for n in range(1,11):
  z=max(0,(n-5)/5);growth=g if n<=5 else g+(gt-g)*z
  margin=.108+(m5-.108)*n/5 if n<=5 else m5+(mt-m5)*z
  r=revenue*(1+growth);nopat=r*margin*.75
  # Growth-funded operating capital includes net capex and working capital; marketing remains expensed.
  # Transition explicitly to NOPAT*g/ROIC; no separate capex add-back/deduction.
  return_on_new=roic+(terminalroic-roic)*z
  economic=(r-revenue)/sales_to_capital
  reinvestment=economic*(1-z)+(nopat*growth/return_on_new)*z
  fcf=nopat-reinvestment;pv+=fcf/(1+w)**n
  rows.append(dict(year=2026+n,revenue=r,ebit_margin=margin,nopat=nopat,incremental_roic=return_on_new,reinvestment=reinvestment,fcff=fcf))
  revenue=r;previousnopat=nopat
 terminalnopat=nopat*(1+gt);terminal_reinvestment=terminalnopat*gt/terminalroic
 terminalfcf=terminalnopat-terminal_reinvestment;tv=terminalfcf/(w-gt)/(1+w)**10
 return dict(value=(pv+tv+netcash)/shares,ev=pv+tv,pv_explicit=pv,pv_terminal=tv,terminal_weight=tv/(pv+tv),terminal_reinvestment=terminal_reinvestment,rows=rows)
cases={'adverse':model(g=.05,m5=.08,mt=.08,roic=.15,terminalroic=.12,gt=.02,sales_to_capital=2.),'central':model(),'favorable':model(g=.22,m5=.20,mt=.18,roic=.30,terminalroic=.20,sales_to_capital=5.)}
def solve(fn,target):
 lo,hi=0.,.8
 for _ in range(100):
  m=(lo+hi)/2
  if fn(m)<target:lo=m
  else:hi=m
 return (lo+hi)/2
out={'asof':'2026-11-06 regular close','price':price,'scanner_last_uncertified':19.5232,'history':h,'normalized_ttm_ebit':h['TTM_Sep2026']['ebit']-7.899,'fy26_sales_guidance_anchor':base,'capital':dict(rf=rf,erp=erp,beta=beta,wacc=wacc,tax=.25,shares_proxy=shares),'cash_bridge':dict(liquid_assets=cash,operating_reserve=reserve,OOG_value_added=equity_investment,financial_debt=0,netcash=netcash),'cases':cases,'inverse':{'growth_5y_with_base_margins':solve(lambda x:model(g=x)['value'],price),'margin5_and_terminal_with_15pct_growth':solve(lambda x:model(m5=x,mt=x)['value'],price)},'sensitivity':{'wacc':{str(x):model(w=x)['value'] for x in [.08,.09,.10,.11]},'no_cash_reserve':cases['central']['value']+reserve/shares,'OOG_at_book':cases['central']['value']+27.735/shares,'use_basic_shares':(cases['central']['ev']+netcash)/165.771620,'future_tax21pct':'not modeled; tax25pct assumption flagged','terminal_roic10pct':model(terminalroic=.10)['value'],'sales_to_capital_2':model(sales_to_capital=2.)['value'],'sales_to_capital_5':model(sales_to_capital=5.)['value']},'checks':{'ten_years':all(len(v['rows'])==10 for v in cases.values()),'positive_terminal_funding':all(v['terminal_reinvestment']>0 for v in cases.values()),'scenario_order':cases['adverse']['value']<cases['central']['value']<cases['favorable']['value'],'wacc_above_g':wacc>.025}}
(P/'calculations.json').write_text(json.dumps(out,indent=2)); print(json.dumps({k:out[k] for k in ['normalized_ttm_ebit','capital','inverse','sensitivity']},indent=2));print({k:round(v['value'],2) for k,v in cases.items()})
