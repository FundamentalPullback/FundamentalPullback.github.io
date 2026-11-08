"""HON diagnostic FCFF, not decision-ready. USD millions; no network. Run python model.py.
Historical continuing cash and quarterly operating reconciliation remain unresolved.
No numeric outputs confer approval. Source/assumption classification in report.md.
"""
import json,csv,pathlib,math
P=pathlib.Path(__file__).resolve().parent
PRICE=220.05;SHARES=319.2;REV=20050.;RF=.0486;ERP=.0441;BETA=.88;KD=RF+.010;TAX=.24
DEBT=2424+3783+10386; CASH=5694+492;OPERATING_CASH=1000
# QNT market value is haircut, never added alongside its equity-method carrying value.
QNT_GROSS=124.628729*37.57
# Book balances are provisional bridge proxies, not certified economic claims.
MINORITY_BOOK=237; LEGACY_ENVIRONMENTAL=68; NONPENSION_NONCURRENT=80
OTHER=MINORITY_BOOK+LEGACY_ENVIRONMENTAL+NONPENSION_NONCURRENT
# R is UNKNOWN. It includes residual pensions, current nonpension benefits, guarantee
# costs and corrections to book/minority/tax assumptions, net of any proven overlap.
# No value for R is assumed; outputs are intercepts V0 for V(R)=V0-R/SHARES.
WACC=(RF+BETA*ERP)*(PRICE*SHARES)/(PRICE*SHARES+DEBT)+KD*(1-TAX)*DEBT/(PRICE*SHARES+DEBT)
cases={'adverse':dict(growth=.02,m0=.155,m5=.175,m10=.17,wacc=WACC+.015,g=.02,roic=.10,qnt_haircut=.65), 'central':dict(growth=.05,m0=.17,m5=.20,m10=.20,wacc=WACC,g=.025,roic=.15,qnt_haircut=.30), 'favorable':dict(growth=.065,m0=.18,m5=.215,m10=.22,wacc=WACC-.0075,g=.03,roic=.20,qnt_haircut=.15)}
def calc(a,growth=None,margin=None):
 r=REV; rows=[]
 for y in range(1,11):
  growth1=a['growth'] if growth is None else growth
  gr=growth1 if y<=5 else growth1+(a['g']-growth1)*(y-5)/5
  m5=a['m5'] if margin is None else margin
  m10=a['m10'] if margin is None else margin
  mar=a['m0']+(m5-a['m0'])*y/5 if y<=5 else m5+(m10-m5)*(y-5)/5
  nr=r*(1+gr);ebit=nr*mar;nop=ebit*(1-TAX)
  # All D&A includes intangible amortization. Reinvestment funds physical and intangible replacement.
  da=.045*nr;dNWC=.15*(nr-r)
  growth_reinvest=max(0,(nr-r)/2.)
  transition_weight=max(0,(y-5)/5)
  terminal_productivity_reinvestment=nop*gr/a['roic']
  required_net_reinvestment=(1-transition_weight)*growth_reinvest+transition_weight*terminal_productivity_reinvestment
  capex=max(.035*nr,da+required_net_reinvestment-dNWC)
  fcff=nop+da-capex-dNWC
  rows.append(dict(year=2026+y,revenue=nr,growth=gr,margin=mar,ebit=ebit,tax=ebit*TAX,nopat=nop,da=da,capex_and_intangible_reinvestment=capex,change_nwc=dNWC,net_reinvestment=capex+dNWC-da,transition_weight=transition_weight,fcff=fcff,pv=fcff/(1+a['wacc'])**y))
  r=nr
 termnop=rows[-1]['nopat']*(1+a['g']);termreinv=termnop*a['g']/a['roic'];tv=(termnop-termreinv)/(a['wacc']-a['g']);pvtv=tv/(1+a['wacc'])**10
 ev=sum(v['pv'] for v in rows)+pvtv
 qnt=QNT_GROSS*(1-a['qnt_haircut']);equity=ev-DEBT+CASH-OPERATING_CASH-OTHER+qnt
 return dict(value_before_unknown_R=equity/SHARES,value_equation="V(R) = V0 - R/319.2; R in USD millions, unknown, not assumed zero",operating_ev=ev,pv_terminal=pvtv,terminal_weight=pvtv/ev,qnt_value=qnt,equity=equity,terminal_nopat=termnop,terminal_reinvestment=termreinv,terminal_roic=a['roic'],rows=rows)
results={k:calc(a) for k,a in cases.items()}
for k,v in results.items():
 with open(P/(k+'_forecast.csv'),'w') as f:
  w=csv.DictWriter(f,fieldnames=v['rows'][0].keys());w.writeheader();w.writerows(v['rows'])
reverse=[]
for mar in [.18,.20,.22,.24]:
 lo,hi=-.01,.30
 for _ in range(80):
  mid=(lo+hi)/2
  if calc(cases['central'],mid,mar)['value_before_unknown_R']<PRICE:lo=mid
  else:hi=mid
 reverse.append(dict(margin_year5_and10=mar,required_growth_years1to5=(lo+hi)/2,value_before_unknown_R=calc(cases['central'],(lo+hi)/2,mar)['value_before_unknown_R'],condition='Illustrative R=0 intercept only; unknown R changes required growth'))
sens=[]
for w in [WACC-.01,WACC,WACC+.01]:
 for g in [.02,.025,.03]:
  a={**cases['central'],'wacc':w,'g':g};sens.append(dict(wacc=w,g=g,value_before_unknown_R=calc(a)['value_before_unknown_R'],condition='Before unknown R'))
# June recast numbers, plus later releases. These are not silently treated as final same-cost-perimeter quarters.
hist=[['2023',19407,2099,None,None,None,None,'June pro forma; discontinued aerospace removed; not fully final cost-perimeter'],['2024',19281,2173,3327,None,None,153,'June recast annual'],['2025',19945,1171,3507,None,None,153,'June recast annual'],['2024Q4',5188,648,985,None,None,29,'June recast'],['2025Q1',4756,535,793,None,None,48,'June recast'],['2025Q2',5018,666,904,187,None,45,'June recast and July release ex aerospace CFO'],['2025Q3',4929,413,866,2306,150,22,'Q3 2026 comparative'],['2025Q4',5242,-443,944,None,None,38,'June recast'],['2026Q1',4823,317,944,None,None,42,'June recast; not final Q3 cost perimeter'],['2026Q2',5187,662,985,563,None,None,'July release excluding aerospace; not final Q3 cost perimeter'],['2026Q3',4994,740,1062,607,77,104,'Q3 2026 release'],['2025_9M',14703,1614,2563,2610,375,115,'Q3 2026 comparative income/cash statements'],['2026_9M',15004,1776,2991,932,369,182,'Q32026 income statement: sales minus COGS R&D SG&A impairment']]
with open(P/'history.csv','w') as f:
 w=csv.writer(f);w.writerow(['period','revenue','operating_income','segment_profit','continuing_cfo','continuing_capex','sbc','source_basis']);w.writerows(hist)
paired={'TTM_2025Q3':{'revenue':5188+14703,'operating_income':648+1614,'segment_profit':985+2563,'sbc':29+115,'cfo':None,'capex':None},'TTM_2026Q3':{'revenue':5242+15004,'operating_income':-443+1776,'segment_profit':944+2991,'sbc':38+182,'cfo':None,'capex':None}}
checks={'fcff_identity':all(abs(v['nopat']+v['da']-v['capex_and_intangible_reinvestment']-v['change_nwc']-v['fcff'])<1e-8 for r in results.values() for v in r['rows']),'funded_reinvestment':all(v['capex_and_intangible_reinvestment']+v['change_nwc']>=v['da'] for r in results.values() for v in r['rows']),'wacc_gt_terminal_g':all(a['wacc']>a['g'] for a in cases.values()),'reverse_intercept_reprices':all(abs(v['value_before_unknown_R']-PRICE)<1e-6 for v in reverse),'terminal_reinvestment_smooth':all(abs(v['terminal_reinvestment']/v['rows'][-1]['net_reinvestment']-(1+cases[k]['g']))<1e-8 for k,v in results.items()),'historical_quarterly_operating_mismatch':1776-(317+662+740),'annual_and_ttm_cash_missing':True,'pension_guarantee_reserve_unverified':True,'entry_approved':False}
out=dict(status='diagnostic_partial_not_decision_ready',price=PRICE,price_date='2026-11-06 16:00 America/New_York',wacc_inputs=dict(rf=RF,rf_date='2026-11-06',rf_tenor='10 years; unadjusted US Treasury',erp=ERP,erp_date='2026-11-01',erp_source_treasury=.0529,source_us_default_spread=.0022,convention_note='Lagged adjusted-payout ERP retained while Treasury is updated; not a contemporaneous implied-ERP recalculation. No sovereign spread is subtracted from Treasury or added to ERP.',beta=BETA,cost_debt=KD,tax=TAX,wacc=WACC),bridge=dict(debt=DEBT,cash_and_short_investments=CASH,operating_cash_reserve=OPERATING_CASH,known_book_claim_proxies=OTHER,minority_book=MINORITY_BOOK,environmental_recorded_total=LEGACY_ENVIRONMENTAL,nonpension_noncurrent_only=NONPENSION_NONCURRENT,unknown_residual_R=None,residual_equation='V(R)=V0-R/319.2',legacy_claim_settlement_in_fcff=False,qnt_gross=QNT_GROSS,shares=SHARES),approved_values=None,residual_R_illustrations=[dict(R_millions=r,value_change_per_share=-r/SHARES,label='Illustrative arithmetic only; not a range estimate for R') for r in [0,250,500,1000,2000]],cases=cases,results=results,paired_ttm=paired,reverse=reverse,sensitivity=sens,checks=checks)
(P/'results.json').write_text(json.dumps(out,indent=2));(P/'qa_results.json').write_text(json.dumps(checks,indent=2));print(json.dumps({k:round(v['value_before_unknown_R'],2) for k,v in results.items()}));print('WACC',WACC,'reverse',reverse)
