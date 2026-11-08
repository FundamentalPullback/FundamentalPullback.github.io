"""WH Fundamental Pullback, USD millions; information cut 2026-11-07.
Analyst diagnostic scenarios, not guidance or an approved canonical valuation.
Independent audit: partial_valuation_calibration_pending; see audit.json.
Terminal capex is an ROIC calibration residual, not independent investment evidence.
Run python model.py > results.json; audit_checks.py verifies arithmetic only.
"""
import json
P=77.35; SHARES=73.100802; DEBT=2748.; CASH=0.
RF=.0486; ERP=.0441; BETA=.64; KD=.05625; TAX=.26
E=P*72.900802; WACC=(RF+BETA*ERP)*E/(E+DEBT)+KD*(1-TAX)*DEBT/(E+DEBT)
SC={'adverso':dict(rooms=.005,revpar=-.005,mix=0,other=.01,margin=.60,g=.02,roic=.12), 'central':dict(rooms=.025,revpar=.015,mix=.005,other=.05,margin=.655,g=.025,roic=.15), 'favorable':dict(rooms=.04,revpar=.025,mix=.005,other=.07,margin=.68,g=.03,roic=.18)}
def dcf(c,w=WACC,g=None,shift=0):
 c=c.copy();g=c['g'] if g is None else g
 royalty=530.;other=359.;marketing=557.;prev=1446.;rows=[]
 for y in range(1,12):
  t=max(0,min(1,(y-5)/5)); gr=(1+c['rooms'])*(1+c['revpar'])*(1+c['mix'])-1+shift
  royalty*=1+gr*(1-t)+g*t;other*=1+(c['other']+shift)*(1-t)+g*t;marketing*=1+gr*(1-t)+g*t
  sales=royalty+other+marketing; core=royalty+other
  margin=(579/889)+(c['margin']-579/889)*min(1,y/5)
  ebit=core*margin;nopat=ebit*(1-TAX)
  da=sales*61/1446;dan_amort=sales*35/1446;dan=sales*110/1446;loans=sales*15/1446;wc=(sales-prev)*.10
  explicit_capex=sales*45/1446
  terminal_reinvestment=nopat*g/c['roic']
  target_capex=da+dan_amort+terminal_reinvestment-dan-loans-wc
  capex=explicit_capex*(1-t)+target_capex*t
  reinvest=capex+dan+loans+wc-da-dan_amort
  fcff=nopat-reinvest
  assert capex>=0 and w>g
  rows.append(dict(year=y,royalties=royalty,other_core=other,marketing_passthrough=marketing,revenue=sales,core_margin=margin,ebit=ebit,nopat=nopat,da=da,dan_amortization=dan_amort,capex_including_software=capex,development_notes_net=dan,development_loans_net=loans,delta_wc=wc,reinvestment=reinvest,fcff=fcff))
  prev=sales
 tv=rows[-1]['fcff']/(w-g);pvterminal=tv/(1+w)**10;pv=sum(r['fcff']/(1+w)**r['year'] for r in rows[:10]);ev=pv+pvterminal
 return dict(price=(ev-DEBT+CASH)/SHARES,enterprise_value=ev,equity_value=ev-DEBT+CASH,pv_explicit=pv,pv_terminal=pvterminal,terminal_weight=pvterminal/ev,wacc=w,g=g,terminal_roic=c['roic'],rows=rows)
def reverse(c,margin=None):
 c=c.copy()
 if margin is not None:c['margin']=margin
 lo,hi=-.05,.15
 for _ in range(90):
  mid=(lo+hi)/2
  if dcf(c,shift=mid)['price']<P:lo=mid
  else:hi=mid
 return {'parallel_growth_shift':mid,'royalty_growth_years1to5':(1+c['rooms'])*(1+c['revpar'])*(1+c['mix'])-1+mid,'other_growth_years1to5':c['other']+mid,'core_margin_year5':c['margin']}
if __name__=='__main__':
 out=dict(asof='2026-11-07',price_date='2026-11-06T16:00:00-05:00',price=P,shares=SHARES,debt=DEBT,excess_cash=CASH,riskfree=RF,erp=ERP,beta=BETA,debt_cost=KD,wacc=WACC,scenarios={k:dcf(v) for k,v in SC.items()},inverse=[reverse(SC['central'],x) for x in [.62,.655,.68]],sensitivity=[{'wacc':w,'g':g,'value':dcf(SC['central'],w,g)['price']} for w in [WACC-.01,WACC,WACC+.01,.08,.09] for g in [.02,.025,.03]])
 out['max_fundamental_20pct_mos']=out['scenarios']['central']['price']*.8
 out['mos_at_close']=1-P/out['scenarios']['central']['price']
 print(json.dumps(out,indent=2))
