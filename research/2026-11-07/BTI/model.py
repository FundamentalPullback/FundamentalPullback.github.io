"""BTI diagnostic FCFF. GBP millions, 10 annual periods from valuation date.
No trading inputs. Analyst assumptions expressly do not constitute audited forecasts.
"""
import json,csv
from pathlib import Path
P=Path(__file__).parent
PRICE=60.89;FX=1.3352;SHARES=2176
# Keep Canada consolidated in operating flows; subtract future settlement provision once.
BRIDGE={'gross_debt_including_leases':35063,'debt_derivatives':25,'available_cash':2518-386-73,'current_investments':15,'hybrid_claims':1893,'pension_liability_no_surplus_netting':787,'minority_book_proxy':216,'canada_provision_and_payable':2752+83,'itc_2025_market_value_stale_proxy':9558,'other_noncurrent_investments_book_proxy':263}
RF=.0516;ERP=.0441;BETA=.09;CRP=0.;KD=.06007;TAX=.25
E=PRICE/FX*SHARES;D=35063+1893
WACC=(RF+BETA*ERP+CRP)*E/(E+D)+KD*(1-TAX)*D/(E+D)
SCENARIOS={'adverso':dict(volume=-.07,pricing=.04,smokeless=.06,margin=.40,g=.0,roic=.08,wacc=WACC),'central':dict(volume=-.05,pricing=.055,smokeless=.12,margin=.435,g=.015,roic=.12,wacc=WACC),'favorable':dict(volume=-.04,pricing=.065,smokeless=.17,margin=.455,g=.02,roic=.15,wacc=WACC)}
def value(s,wacc=None,g=None,margin=None,itc=None):
 w=s['wacc'] if wacc is None else wacc;g=s['g'] if g is None else g;m=s['margin'] if margin is None else margin
 # Smokeless H1 mix is proxy for TTM, not equivalent to New Categories.
 old=25776*.802;new=25776*.198;rev=old+new;rows=[]
 for t in range(1,11):
  if t<=5:
   old*=1+s['volume']+s['pricing'];new*=1+s['smokeless'];r=old+new;growth=r/rev-1
   da=r*.02;capex=r*.03;wc=max(r-rev,0)*.10
   nopat=r*m*(1-TAX);reinvest=capex-da+wc
  else:
   a=(t-5)/5;growth=rows[4]['growth']*(1-a)+g*a;r=rev*(1+growth);nopat=r*m*(1-TAX)
   # transition net reinvestment ratio to g/ROIC; decompose capex to satisfy identity.
   ratio=rows[4]['reinvestment']/rows[4]['nopat']*(1-a)+(g/s['roic'])*a
   reinvest=nopat*ratio;da=r*.02;wc=max(r-rev,0)*.10;capex=da+reinvest-wc
  fcff=nopat+da-capex-wc
  rows.append(dict(year=t,revenue=r,growth=growth,margin=m,nopat=nopat,da=da,capex=capex,delta_nwc=wc,reinvestment=reinvest,fcff=fcff,pv=fcff/(1+w)**t));rev=r
 terminal_nopat=rows[-1]['nopat']*(1+g);terminal_fcff=terminal_nopat*(1-g/s['roic']);tv=terminal_fcff/(w-g);ev=sum(x['pv'] for x in rows)+tv/(1+w)**10
 b=BRIDGE;equity=ev-b['gross_debt_including_leases']-b['debt_derivatives']+b['available_cash']+b['current_investments']-b['hybrid_claims']-b['pension_liability_no_surplus_netting']-b['minority_book_proxy']-b['canada_provision_and_payable']+(b['itc_2025_market_value_stale_proxy'] if itc is None else itc)+b['other_noncurrent_investments_book_proxy']
 return dict(value_usd=equity/SHARES*FX,value_gbp=equity/SHARES,ev=ev,equity=equity,wacc=w,terminal_g=g,terminal_roic=s['roic'],terminal_fcff=terminal_fcff,terminal_pv_share=tv/(1+w)**10/ev,upside=equity/SHARES*FX/PRICE-1,rows=rows)
r={k:value(s) for k,s in SCENARIOS.items()}
lo,hi=.1,.8
for _ in range(100):
 mid=(lo+hi)/2
 if value(SCENARIOS['central'],margin=mid)['value_usd']<PRICE:lo=mid
 else:hi=mid
out={'canonical_value':None,'completion':False,'fundamentalApproval':False,'stage35Approved':False,'valuation_use':'explanatory diagnostic only','status':'screen-grade; partial material bridge gaps','price':PRICE,'price_time':'2026-11-06T16:00:00-05:00','scannerLast':60.89,'fx_usd_per_gbp':FX,'fx_date':'2026-11-06 daily close, not synchronous NYSE fixing','shares_millions':SHARES,'bridge':BRIDGE,'cost_of_capital':dict(riskfree=RF,erp=ERP,erp_date='2026-11-01',beta_observed=.09,beta_used=BETA,country_risk_overlay=CRP,cost_debt=KD,tax=TAX,wacc=WACC),'scenarios':r,'reverse_central_required_ebit_margin':(lo+hi)/2,'sensitivity':[dict(wacc=w,g=g,value_usd=value(SCENARIOS['central'],wacc=w,g=g)['value_usd']) for w in [.05,.06,.07,.08,.09,.10,.11] for g in [0,.01,.015,.02]],'itc_stale_proxy_sensitivity':{str(x):value(SCENARIOS['central'],itc=x)['value_usd'] for x in [0,5000,9558,14000]},'calibration_sensitivity':[dict(beta=b,country_risk_overlay=crp,kd=kd,wacc=(RF+b*ERP+crp)*E/(E+D)+kd*(1-TAX)*D/(E+D),value_usd=value(SCENARIOS['central'],wacc=(RF+b*ERP+crp)*E/(E+D)+kd*(1-TAX)*D/(E+D))['value_usd']) for b in [.09,.3933,.8,1.] for crp in [0,.005] for kd in [.06007,.0618]],'no_orders':True}
(P/'results.json').write_text(json.dumps(out,indent=2))
for k,v in r.items():
 with (P/f'forecast_{k}.csv').open('w') as f:
  w=csv.DictWriter(f,fieldnames=list(v['rows'][0]));w.writeheader();w.writerows(v['rows'])
checks={'canonical_value_null':out['canonical_value'] is None,'completion_false':out['completion'] is False,'one_wacc_all_operating_cases':len({v['wacc'] for v in r.values()})==1,'positive_capex':all(x['capex']>=0 for v in r.values() for x in v['rows']),'all_ten_years':all(len(v['rows'])==10 for v in r.values()),'fcff_identity':all(abs(x['fcff']-(x['nopat']+x['da']-x['capex']-x['delta_nwc']))<1e-7 for v in r.values() for x in v['rows']),'g_below_wacc':all(v['terminal_g']<v['wacc'] for v in r.values()),'terminal_reinvestment':all(abs(v['rows'][-1]['reinvestment']/v['rows'][-1]['nopat']-v['terminal_g']/v['terminal_roic'])<1e-9 for v in r.values())}
(P/'run_log.json').write_text(json.dumps({'checks':checks,'material_gaps':['current ITC market value','claim fair values and post-June changes','normalized cash/perimeter to operating forecast','matched historical valuation multiples','restricted Canada cash versus settlement funding offset','other associates missing from nonoperating assets','marginal GBP debt yield and beta/geographic exposure calibration'],'posture':'not-decision-ready'},indent=2));assert all(checks.values())
print(json.dumps({k:round(v['value_usd'],2) for k,v in r.items()}));print('WACC',WACC,'reverse margin',(lo+hi)/2)
