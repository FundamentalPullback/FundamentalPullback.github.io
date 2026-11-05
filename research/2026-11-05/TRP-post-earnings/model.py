import json,math,csv,pathlib,copy
B=pathlib.Path(__file__).parent
FX=1.3961
PRICE=64.38
STUB_YEARS=56/365 # 5 Nov to 31 Dec 2026; stub net cash assumed zero, tested separately
SHARES=1042.0 # 1042m reported diluted, no future free buybacks or duplicate option claim
DEBT=2780+3197+44418+12639
BRIDGE={'consolidated_debt':DEBT,'preferred':2255,'affiliate_loan':218,'factoring':84,'postretirement_unfunded':76,'SouthBow_residual_liability':41,'declared_dividends_payable':933,'accrued_interest_payable':904,'excess_cash':749}
# C$m, continuing perimeter. 2024 contributions economically net the CGL circular contribution/loan repayment of 3137, NOT the extra 10m true distribution.
ANNUAL=[dict(year=y,revenue=r,segmented_ebit=e,comp_ebitda=eb,common_net=ni,eps=ep,comp_eps=ce,comp_common_net=cn,cfo_total=cf,cfo_discontinued=dc,core_capex=cap,development=dev,jv_contribution=jv,da=da,shares=sh) for y,r,e,eb,ni,ep,ce,cn,cf,dc,cap,dev,jv,da,sh in [
(2023,13267,5097,9472,2217,2.15,3.78,3896,7268,1026,7958,142,4149,2446,1030),
(2024,13771,7964,10049,4199,4.05,3.73,3865,7696,670,6181,50,1546,2535,1038),
(2025,15239,8036,10952,3612,3.47,3.51,3654,7346,-185,5270,16,1051,2769,1040)]]
for a in ANNUAL:
 a['cfo_cont']=a['cfo_total']-a['cfo_discontinued'];a['cash_reinvestment']=a['core_capex']+a['development']+a['jv_contribution'];a['fcf_before_nci_preferred']=a['cfo_cont']-a['cash_reinvestment'];a['fcf_per_basic_share']=a['fcf_before_nci_preferred']/a['shares'];a['segmented_margin']=a['segmented_ebit']/a['revenue'];a['net_common_margin']=a['common_net']/a['revenue']
Q=[]
# quarter, revenue, EBIT incl JV income, comparable EBITDA, continuing common NI, continuing reported EPS, comparable EPS, comparable NI, CFO total, discontinued CFO, core capex, development, JV cash contribution, DA
raw=[
('2024Q4',3577,7964-6066,10049-7430,1069,1.03,1.05,1094,7696-5612,670-724,6181-(4668-127),50-41,1546-888,2535-(2149-253)),
('2025Q1',3623,1966,2709,978,.94,.95,983,1359,-56,1560,4,245,678),
('2025Q2',3744,1954,2625,862,.83,.82,848,2173,3,1109,6,264,671),
('2025Q3',3704,1928,2654,813,.78,.77,805,1920,12,1255,2,249,701),
('2025Q4',4168,8036-5848,10952-7988,959,.92,.98,1018,7346-5452,-185-(-41),5270-3924,16-12,1051-758,2769-2050),
('2026Q1',3861,2171,3088,899,.86,.99,1031,2603,168,1070,4,233,723),
('2026Q2',3957,2173,2948,987,.95,.94,984,2217,-2,889,5,229,737),
('2026Q3',4030,2262,3004,1026,.98,.94,983,1782,-122,1194,5,213,749)]
for z in raw:
 q=dict(zip(['quarter','revenue','segmented_ebit','comp_ebitda','common_net','eps','comp_eps','comp_common_net','cfo_total','cfo_discontinued','core_capex','development','jv_contribution','da'],z));q['cfo_cont']=q['cfo_total']-q['cfo_discontinued'];q['cash_reinvestment']=q['core_capex']+q['development']+q['jv_contribution'];q['fcf_before_nci_preferred']=q['cfo_cont']-q['cash_reinvestment'];q['segmented_margin']=q['segmented_ebit']/q['revenue'];Q.append(q)
TTM={}
for label,rows in [('2025Q3',Q[:4]),('2026Q3',Q[4:])]:
 TTM[label]={k:sum(q[k] for q in rows) for k in ['revenue','segmented_ebit','comp_ebitda','common_net','eps','comp_eps','comp_common_net','cfo_total','cfo_discontinued','cfo_cont','cash_reinvestment','fcf_before_nci_preferred','da']}
TTM['2026Q3']['nci_distributions']=929+716-414
TTM['2026Q3']['preferred_cash_dividends']=114+84-85
TTM['2026Q3']['common_cash_dividends']=3507+2713-2623
TTM['2026Q3']['common_cash_residual']=TTM['2026Q3']['fcf_before_nci_preferred']-TTM['2026Q3']['nci_distributions']-TTM['2026Q3']['preferred_cash_dividends']
# CGL cash collected October 2025 was recognized as a receivable/in-substance equity distribution in 2024. Remove once from recurring cash, not reported history.
TTM['2026Q3']['cgl_one_off_cash']=199
TTM['2026Q3']['cfo_cont_less_cgl_one_off']=TTM['2026Q3']['cfo_cont']-199
TTM['2026Q3']['fcf_before_nci_preferred_less_cgl_one_off']=TTM['2026Q3']['fcf_before_nci_preferred']-199
TTM['2026Q3']['common_cash_residual_less_cgl_one_off']=TTM['2026Q3']['common_cash_residual']-199
TTM['2026Q3']['common_dividend_cash_coverage_less_cgl_one_off']=TTM['2026Q3']['common_cash_residual_less_cgl_one_off']/TTM['2026Q3']['common_cash_dividends']
TTM['2026Q3']['third_party_settlement_cash_net_of_tax']=78
TTM['2026Q3']['common_cash_residual_illustrative_ex_cgl_plus_settlement']=TTM['2026Q3']['common_cash_residual_less_cgl_one_off']+78
TTM['2026Q3']['illustrative_cash_coverage_ex_cgl_plus_settlement']=(TTM['2026Q3']['common_cash_residual_less_cgl_one_off']+78)/TTM['2026Q3']['common_cash_dividends']
TTM['2026Q3']['normalization_status']='Partial illustrative cash adjustments. CGL receipt verified; precise operating cash-flow subline not independently identified. Settlement addback shown symmetrically but not accepted as fully nonrecurring.'
SCENARIOS={
'adverse':dict(wacc=.0725,ke=.10,rev_growth=.04,margin=.415,tax=.26,da_ratio=.20,capex=[5900,6200,6400,6550,6700],g=.02,roic=.08,jv_growth=.035,jv_earn0=1500,jv_dist0=1800,jv_contrib=[1250,1300,1350,1400,1450],roe=.10,lease=9366*.85,nci=9773*.85),
'base':dict(wacc=.0675,ke=.09,rev_growth=.055,margin=.425,tax=.25,da_ratio=.195,capex=[5750,6000,6200,6350,6500],g=.025,roic=.085,jv_growth=.06,jv_earn0=1550,jv_dist0=1900,jv_contrib=[1200,1200,1250,1300,1300],roe=.12,lease=9366,nci=9773),
'favorable':dict(wacc=.06,ke=.08,rev_growth=.07,margin=.44,tax=.24,da_ratio=.19,capex=[5600,5800,6000,6200,6400],g=.03,roic=.10,jv_growth=.075,jv_earn0=1600,jv_dist0=2100,jv_contrib=[1150,1150,1200,1200,1250],roe=.14,lease=9366*1.15,nci=9773*1.2)}
def calc(s):
 s=copy.deepcopy(s);rev=15070.;rows=[];jve=s['jv_earn0'];jvd=s['jv_dist0'];ev=0;jv=0;cum_capex=0;start_ic=85000.;ic=start_ic;prev_nopat=6410*.75
 for t in range(1,11):
  trans=max(0,(t-5)/5);growth=s['rev_growth']*(1-trans)+s['g']*trans
  oldrev=rev;rev*=1+growth;ebit=rev*s['margin'];nopat=ebit*(1-s['tax']);da=rev*s['da_ratio'];wc=(rev-oldrev)*.01
  if t<=5:
   refg=s.get('reinvestment_reference_growth',s['rev_growth']); refrev=15070*(1+refg)**t; refold=refrev/(1+refg); refnopat=refrev*s['margin']*(1-s['tax']); refda=refrev*s['da_ratio']; refwc=(refrev-refold)*.01
   refnet=s['capex'][t-1]-refda+refwc
   paid_net=refnet*(nopat/refnopat)*(growth/refg)
   capex=da+paid_net-wc
  else:
   full=rows[4]['capex']*(rev/rows[4]['revenue']);sustainable=da+nopat*growth/s['roic']-wc
   capex=full*(1-trans)+sustainable*trans
  netreinvest=capex-da+wc;fcff=nopat-netreinvest;disc=fcff/(1+s['wacc'])**(t+STUB_YEARS);ev+=disc
  oldjve=jve;jve*=1+s['jv_growth']*(1-trans)+s['g']*trans;jvd*=1+s['jv_growth']*(1-trans)+s['g']*trans
  if t<=5:jvc=s['jv_contrib'][t-1];jvcash=jvd-jvc
  else:
   explicit=jvd-s['jv_contrib'][-1]*(jve/(s['jv_earn0']*(1+s['jv_growth'])**5))
   terminal_policy=jve*(1-(s['jv_growth']*(1-trans)+s['g']*trans)/s['roe']);jvcash=explicit*(1-trans)+terminal_policy*trans;jvc=jvd-jvcash
  jv+=jvcash/(1+s['ke'])**(t+STUB_YEARS)
  rows.append(dict(year=2026+t,revenue=rev,revenue_growth=growth,margin=s['margin'],ebit=ebit,tax=s['tax'],nopat=nopat,da=da,capex=capex,delta_wc=wc,net_reinvestment=netreinvest,fcff=fcff,pv_fcff=disc,invested_capital_open=ic,roic_on_open=nopat/ic,incremental_nopat=nopat-prev_nopat,jv_earnings=jve,jv_distributions=jvd,jv_equity_contributions=jvc,jv_net_equity_cash=jvcash))
  ic+=netreinvest;prev_nopat=nopat;cum_capex+=capex
 terminal_nopat=nopat*(1+s['g']);terminal_reinvestment=terminal_nopat*s['g']/s['roic'];terminal_fcff=terminal_nopat-terminal_reinvestment;tv=terminal_fcff/(s['wacc']-s['g']);pvtv=tv/(1+s['wacc'])**(10+STUB_YEARS);ev+=pvtv
 jvt=jve*(1+s['g'])*(1-s['g']/s['roe'])/(s['ke']-s['g']);pvjvt=jvt/(1+s['ke'])**(10+STUB_YEARS);jv+=pvjvt
 claims=sum(v for k,v in BRIDGE.items() if k!='excess_cash')-BRIDGE['excess_cash']
 equity=ev+jv+s['lease']-s['nci']-claims
 return dict(assumptions=s,rows=rows,core_ev=ev,jv_equity_value=jv,lease_value=s['lease'],nci_value=s['nci'],net_financial_claims=claims,equity=equity,raw_equity_cad_per_share=equity/SHARES,value_cad=max(0,equity/SHARES),value_usd=max(0,equity/SHARES/FX),core_terminal_weight=pvtv/ev,total_terminal_weight=(pvtv+pvjvt)/(ev+jv+s['lease']),terminal_nopat=terminal_nopat,terminal_reinvestment=terminal_reinvestment,terminal_fcff=terminal_fcff,core_terminal_value=tv,jv_terminal_value=jvt,cumulative_core_capex=cum_capex)
RESULTS={k:calc(v) for k,v in SCENARIOS.items()}
SENS=[]
for w in [.0575,.0625,.0675,.0725,.0775]:
 for g in [.015,.02,.025,.03]:
  s=copy.deepcopy(SCENARIOS['base']);s.update(wacc=w,g=g);r=calc(s);SENS.append(dict(wacc=w,g=g,value_usd=r['value_usd']))
def bisect(key,lo,hi,target=PRICE):
 for _ in range(70):
  md=(lo+hi)/2;s=copy.deepcopy(SCENARIOS['base']);s[key]=md;s['reinvestment_reference_growth']=SCENARIOS['base']['rev_growth'];v=calc(s)['value_usd']
  if (v<target) == (key!='wacc'):lo=md
  else:hi=md
 return (lo+hi)/2
REVERSE={k:bisect(k,*bounds) for k,bounds in [('wacc',(.035,.12)),('rev_growth',(.0,.30)),('margin',(.2,.8))]}
# current market enterprise approximation deliberately not labeled ownership-homogeneous EV/EBITDA
MARKET={'price_usd':PRICE,'price_time':'2026-11-05T15:34:29Z','fx_cad_per_usd':FX,'fx_date':'2026-11-04','shares_million':SHARES,'market_cap_cad':PRICE*FX*SHARES,'pe_comparable_ttm':PRICE*FX/TTM['2026Q3']['comp_eps'],'pe_reported_cont_ttm':PRICE*FX/TTM['2026Q3']['eps'],'dividend_yield':3.51/(PRICE*FX),'scanner_price_usd':62.71,'scanner_price_date':'2026-11-04'}
OUT=dict(version='TRP-POST-Q326-v2.1',balance_sheet_reference_date='2026-09-30',valuation_date='2026-11-05',balance_roll_forward_status='No complete October/November roll forward. Deduct September declared dividends and accrued interest once against September cash/claims; do not also deduct assumed subsequent payments.',market=MARKET,annual=ANNUAL,quarters=Q,ttm=TTM,bridge=BRIDGE,scenarios=RESULTS,sensitivity=SENS,reverse=REVERSE)
(B/'model_output.json').write_text(json.dumps(OUT,indent=2))
for name,rows in [('history_annual',ANNUAL),('history_quarters',Q),('forecast_base',RESULTS['base']['rows']),('sensitivity',SENS)]:
 with (B/(name+'.csv')).open('w') as f:
  wr=csv.DictWriter(f,fieldnames=list(rows[0]));wr.writeheader();wr.writerows(rows)
print(json.dumps({'ttm':TTM,'bridge':BRIDGE,'scenario_summary':{k:{a:r[a] for a in ['value_cad','value_usd','core_ev','jv_equity_value','lease_value','nci_value','net_financial_claims','core_terminal_weight','total_terminal_weight']} for k,r in RESULTS.items()},'reverse':REVERSE,'market':MARKET},indent=2))
