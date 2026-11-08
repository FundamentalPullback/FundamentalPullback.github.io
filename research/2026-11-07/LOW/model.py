"""Explicit lightweight FCFF support model; USD millions. No prices or trading orders written.
Reported data: sources.json. Forecasts are analyst estimates, not company guidance.
Annual future intervals from Nov 6 2026, no capitalization of already earned H1 cash.
"""
import json
from pathlib import Path
P=Path(__file__).parent
CLOSE=224.55; SHARES=562.; DEBT=37556.; EXCESS_CASH=2172.
# Lease-expense convention: operating rents retained in EBIT; operating liabilities not subtracted.
# Finance leases included in DEBT. Capex includes a $30m p.a. finance-lease asset allowance.
CASES={
'bear':dict(rg=[-.03,0,.01,.02,.02],og=[-.06,-.02,.01,.02,.02],rm=[.115,.112,.112,.113,.114],om=[-.01,0,.01,.02,.025],w=.0748,g=.02,roic=.12,cap=.030,wc=.08),
'base':dict(rg=[.01,.02,.025,.03,.03],og=[.02,.03,.04,.04,.035],rm=[.121,.122,.124,.125,.125],om=[.01,.02,.03,.04,.045],w=.0748,g=.025,roic=.16,cap=.028,wc=.06),
'bull':dict(rg=[.03,.04,.04,.04,.035],og=[.05,.06,.06,.05,.045],rm=[.125,.129,.132,.134,.135],om=[.03,.045,.055,.065,.07],w=.0748,g=.03,roic=.20,cap=.028,wc=.05)}
def calc(c,w=None,g=None,margin_shift=0):
 w=c['w'] if w is None else w; g=c['g'] if g is None else g
 r,o=84700.,7300.; prev=r+o; rows=[]; pv=0
 for i in range(10):
  t=max(0,(i-4)/5)
  rg=c['rg'][i] if i<5 else c['rg'][-1]*(1-t)+g*t
  og=c['og'][i] if i<5 else c['og'][-1]*(1-t)+g*t
  r*=1+rg;o*=1+og; rev=r+o
  rm=(c['rm'][i] if i<5 else c['rm'][-1])+margin_shift
  om=(c['om'][i] if i<5 else c['om'][-1])+margin_shift
  ebit=r*rm+o*om;nopat=ebit*.755
  da=rev*.026 # total cash-flow D&A, including distribution and acquisition amortization
  dwc=max(0,rev-prev)*c['wc'] # no perpetual release in contraction
  detailed_cap=rev*c['cap']+30
  detailed_reinv=detailed_cap-da+dwc
  reinv=detailed_reinv*(1-t)+(nopat*g/c['roic'])*t
  cap=da+reinv-dwc
  fcff=nopat+da-cap-dwc; discounted=fcff/(1+w)**(i+1);pv+=discounted
  rows.append(dict(year=i+1,retail_revenue=r,other_revenue=o,revenue=rev,retail_margin=rm,other_margin=om,ebit=ebit,tax=.245,nopat=nopat,da=da,capex=cap,dnwc=dwc,reinvestment=reinv,fcff=fcff,pv=discounted))
  prev=rev
 terminal_nopat=rows[-1]['nopat']*(1+g); terminal_reinv=terminal_nopat*g/c['roic'];tv=(terminal_nopat-terminal_reinv)/(w-g);pvtv=tv/(1+w)**10
 ev=pv+pvtv;equity=ev-DEBT+EXCESS_CASH;price=equity/SHARES
 assert w>g and all(abs(x['fcff']-(x['nopat']+x['da']-x['capex']-x['dnwc']))<1e-7 for x in rows)
 return dict(price=price,upside=price/CLOSE-1,ev=ev,equity=equity,pv_explicit=pv,pv_terminal=pvtv,terminal_weight=pvtv/ev,terminal_nopat=terminal_nopat,terminal_reinvestment=terminal_reinv,wacc=w,g=g,roic=c['roic'],years=rows)
results={k:calc(v) for k,v in CASES.items()}
lo,hi=-.08,.15
for _ in range(100):
 mid=(lo+hi)/2
 if calc(CASES['base'],margin_shift=mid)['price']<CLOSE:lo=mid
 else:hi=mid
results['reverse']={'uniform_operating_margin_addition':mid,'base_path_terminal_margin':results['base']['years'][-1]['ebit']/results['base']['years'][-1]['revenue'],'required_terminal_margin':calc(CASES['base'],margin_shift=mid)['years'][-1]['ebit']/calc(CASES['base'],margin_shift=mid)['years'][-1]['revenue']}
results['sensitivity']=[{'wacc':w,'g':g,'price':calc(CASES['base'],w,g)['price']} for w in [.0648,.0748,.0848] for g in [.02,.025,.03]]
results['bridge']={'debt_including_finance_leases':DEBT,'reported_cash':3172,'operating_cash_retained':1000,'excess_cash':EXCESS_CASH,'excluded_investments':414,'shares_including_participating_awards_allowance':SHARES,'operating_lease_liabilities_not_subtracted':4467}
results['wacc_build']={'rf':.0486,'erp_observed_Nov1':.0441,'beta_5Y_observed':.81,'ke':.0486+.81*.0441,'debt_weight':37556/(37556+CLOSE*SHARES),'kd_market_proxy':.0565,'tax':.245}
z=results['wacc_build'];z['calculated_wacc']=z['ke']*(1-z['debt_weight'])+z['kd_market_proxy']*(1-z['tax'])*z['debt_weight']
results['actuals']={'annual':{'2023':{'sales':86377,'ebit':11557,'ni':7726,'cfo':8140,'da':1923,'capex':1964,'sbc':210},'2024':{'sales':83674,'ebit':10466,'ni':6957,'cfo':9625,'da':1972,'capex':1927,'sbc':221},'2025':{'sales':86286,'ebit':10153,'ni':6654,'cfo':9864,'da':2194,'capex':2213,'sbc':247}},'quarters':{'2025Q3':{'sales':20813,'ebit':2481,'ni':1616,'cfo':8297-7610,'da':1557-1022,'capex':1610-1013,'sbc':177-117},'2025Q4':{'sales':20584,'ebit':1708,'ni':999,'cfo':9864-8297,'da':2194-1557,'capex':2213-1610,'sbc':247-177},'2026Q1':{'sales':23078,'ebit':2554,'ni':1628,'cfo':3350,'da':644,'capex':521,'sbc':65},'2026Q2':{'sales':25956,'ebit':3549,'ni':2399,'cfo':7009-3350,'da':1292-644,'capex':1063-521,'sbc':132-65}},'ttm':{'sales':90432,'ebit':10292,'ni':6643,'cfo':9263,'da':2464,'capex':2263,'sbc':262},'rounding_note':'Sum of quarterly revenues/EBIT/NI differs by $1m from annual minus H1 plus H1; annual comparative preferred. 10-Q ROIC table NI 6642 differs by $1m too.'}
(P/'model_results.json').write_text(json.dumps(results,indent=2))
print({k:round(results[k]['price'],2) for k in CASES});print(results['reverse']);print(z)
