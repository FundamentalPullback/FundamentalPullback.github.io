"""PEP reproducible FCFF. USD millions, except per share. Run from any directory."""
import json,csv
from pathlib import Path
P=Path(__file__).parent
price=141.34; shares=1367
hist={
'FY2023':dict(revenue=91471,ebit=11986,net_income=9074,cfo=13442,capex=5518,da=2948,sbc=380,disposals=198,eps=6.56,shares=1383),
'FY2024':dict(revenue=91854,ebit=12887,net_income=9578,cfo=12507,capex=5318,da=3160,sbc=362,disposals=342,eps=6.95,shares=1378),
'FY2025':dict(revenue=93925,ebit=11498,net_income=8240,cfo=12087,capex=4415,da=3451,sbc=288,disposals=528,eps=6,shares=1373),
'YTD2025Q3':dict(revenue=64582,ebit=7941,net_income=5700,cfo=5468,capex=2499,da=2315,sbc=207,disposals=272,eps=4.15),
'YTD2026Q3':dict(revenue=68898,ebit=11496,net_income=8356,cfo=7950,capex=2182,da=2531,sbc=240,disposals=89,eps=6.10),
'Q12026':dict(revenue=19443,ebit=3213,net_income=2327,cfo=41,capex=447,da=742,sbc=93,disposals=13,eps=1.70),
'H12026':dict(revenue=43624,ebit=7236,net_income=5308,cfo=2365,capex=1266,da=1639,sbc=162,disposals=71,eps=3.88)}
keys=list(hist['YTD2026Q3'])
for name,a,b in [('Q42025','FY2025','YTD2025Q3'),('Q22026','H12026','Q12026'),('Q32026','YTD2026Q3','H12026')]:hist[name]={k:round(hist[a][k]-hist[b][k],6) for k in keys}
hist['Q32026']['eps']=2.23 # reported quarter; never difference rounded cumulative EPS
hist['TTM']={k:round(hist['FY2025'][k]+hist['YTD2026Q3'][k]-hist['YTD2025Q3'][k],6) for k in keys}
for h in hist.values():h.update(fcf_cfo_capex=h['cfo']-h['capex'],fcf_company=h['cfo']-h['capex']+h['disposals'],operating_margin=h['ebit']/h['revenue'])
bridge={'gross_debt':51881,'cash_total':10675,'russia_excluded':2135,'short_investments':488,'employee_hedge_excluded':382,'operating_cash_reserve':1000,'excess_cash':7646,'pension_gross_deficits_after_tax':1372*.79,'minority_capitalized':(55+56-40)*15,'earnout':12,'nonoperating_investments_added':0}
netclaims=bridge['gross_debt']+bridge['pension_gross_deficits_after_tax']+bridge['minority_capitalized']+bridge['earnout']-bridge['excess_cash']
rf=.0486;erp=.0441;beta_raw=.32;beta_normalized=.85;kd=.0586;tax=.21
eqweight=price*1362.741092/(price*1362.741092+51881)
wacc_derived=eqweight*(rf+beta_normalized*erp)+(1-eqweight)*kd*(1-tax)
scenarios={
'bear':dict(growth=[0,.01,.015,.02,.02],margins=[.14,.138,.14,.142,.145],terminal_margin=.145,wacc=.09,g=.02,roic=.13,capex=.05,da=.037),
'base':dict(growth=[.03,.035,.04,.04,.035],margins=[.15,.153,.156,.158,.16],terminal_margin=.155,wacc=.08,g=.025,roic=.18,capex=.045,da=.037),
'bull':dict(growth=[.045,.05,.05,.045,.04],margins=[.157,.163,.167,.17,.172],terminal_margin=.17,wacc=.07,g=.03,roic=.22,capex=.043,da=.037)}
def dcf(case,wacc=None,g=None,margin_shift=0,growth_shift=0):
 s=dict(case);w=wacc or s['wacc'];g=s['g'] if g is None else g;assert w>g
 rev=hist['TTM']['revenue'];rows=[]
 for y in range(1,11):
  f=max(0,(y-5)/5)
  gr=s['growth'][y-1]+growth_shift if y<=5 else (s['growth'][-1]+growth_shift)*(1-f)+g*f
  margin=s['margins'][y-1]+margin_shift if y<=5 else (s['margins'][-1]+margin_shift)*(1-f)+(s['terminal_margin']+margin_shift)*f
  old=rev;rev*=1+gr;ebit=rev*margin;nopat=ebit*(1-tax);da=rev*s['da'];nwc=.05*(rev-old)
  raw_reinvestment=rev*s['capex']-da+nwc
  reinvest=raw_reinvestment*(1-f)+(nopat*g/s['roic'])*f
  capex=reinvest+da-nwc;fcff=nopat+da-capex-nwc
  rows.append(dict(year=y,revenue=rev,growth=gr,margin=margin,ebit=ebit,tax=ebit*tax,nopat=nopat,da=da,capex=capex,change_nwc=nwc,reinvestment=reinvest,fcff=fcff,pv=fcff/(1+w)**y))
 terminal_nopat=rows[-1]['nopat']*(1+g);terminal_reinvest=terminal_nopat*g/s['roic'];terminal_fcf=terminal_nopat-terminal_reinvest
 tv=terminal_fcf/(w-g);pvt=tv/(1+w)**10;ev=sum(x['pv'] for x in rows)+pvt;fair=(ev-netclaims)/shares
 return dict(rows=rows,ev=ev,equity=ev-netclaims,fair_value=fair,upside=fair/price-1,margin_safety=1-price/fair,terminal_value=tv,pv_terminal=pvt,terminal_weight=pvt/ev,terminal_nopat=terminal_nopat,terminal_reinvestment=terminal_reinvest,terminal_fcff=terminal_fcf,wacc=w,g=g,roic=s['roic'])
results={k:dcf(v) for k,v in scenarios.items()}
def solve(param,lo,hi):
 for _ in range(100):
  m=(lo+hi)/2;v=dcf(scenarios['base'],**{param:m})['fair_value']
  if (v<price)==(param!='wacc'):lo=m
  else:hi=m
 return (lo+hi)/2
inverse={k:solve(k,*bounds) for k,bounds in {'margin_shift':(-.10,.10),'growth_shift':(-.04,.10),'wacc':(.04,.14)}.items()}
comparisons=[]
for year,pr in [('FY2023',169.84),('FY2024',152.06),('FY2025',143.52)]:
 h=hist[year];comparisons.append(dict(period=year,price=pr,pe=pr/h['eps'],p_fcf=pr*h['shares']/h['fcf_cfo_capex']))
comparisons.append(dict(period='TTM Nov6',price=price,pe=price/hist['TTM']['eps'],p_fcf=price*shares/hist['TTM']['fcf_cfo_capex']))
normalized_ebit=14912+11394-10837-500-160
normalization=dict(core_ttm=15469,recurring_restructuring_allowance=500,tariff_refund_allowance=160,normalized_ebit=normalized_ebit,tax=tax,da=3667,capex=4400,nwc=500,fcff=normalized_ebit*(1-tax)+3667-4400-500,ttm_cfo_capex=10471,ttm_company_fcf=10816,ttm_sbc=321,after_sbc_cfo_capex=10150,net_interest_after_tax_proxy=1106*.79)
wacc_raw=eqweight*(rf+beta_raw*erp)+(1-eqweight)*kd*(1-tax)
raw_beta_value=dcf(scenarios['base'],wacc=wacc_raw)['fair_value']
beta_sensitivity=[dict(beta=b,wacc=(w:=eqweight*(rf+b*erp)+(1-eqweight)*kd*(1-tax)),value=(v:=dcf(scenarios['base'],wacc=w)['fair_value']),upside=v/price-1,price_premium_to_value=price/v-1) for b in [.32,.50,.65,.85,1.0]]
breakeven_beta=(inverse['wacc']-(1-eqweight)*kd*(1-tax)-eqweight*rf)/(eqweight*erp)
out=dict(beta_sensitivity=beta_sensitivity,breakeven_beta=breakeven_beta,raw_beta_sensitivity={'wacc':wacc_raw,'value':raw_beta_value},asof='2026-11-07',close={'price':price,'date':'2026-11-06','time':'16:00 America/New_York','scanner_last':141.70},units='USD millions except per share',historical=hist,bridge=bridge,net_claims=netclaims,shares=shares,normalization=normalization,wacc=dict(rf=rf,erp=erp,beta_observed=beta_raw,beta_analyst=beta_normalized,kd_analyst=kd,equity_weight=eqweight,derived=wacc_derived,selected=.08),scenarios=results,sensitivity=[dict(wacc=w,g=g,value=dcf(scenarios['base'],wacc=w,g=g)['fair_value']) for w in [wacc_raw,.06,.065,.07,.075,.08,.085,.09] for g in [.02,.025,.03]],inverse=inverse,comparisons=comparisons)
(P/'results.json').write_text(json.dumps(out,indent=2))
with (P/'history.csv').open('w') as f:
 wr=csv.DictWriter(f,fieldnames=['period']+list(hist['FY2023']));wr.writeheader();wr.writerows(dict(period=k,**v) for k,v in hist.items())
assert all(abs(sum(hist[q][k] for q in ['Q42025','Q12026','Q22026','Q32026'])-hist['TTM'][k])<1e-6 for k in keys if k!='eps')
assert all(abs(solve_value['fair_value']-price)<1e-6 for solve_value in [dcf(scenarios['base'],**{k:v}) for k,v in inverse.items()])
assert abs(sum(hist[k]['revenue'] for k in ['Q42025','Q12026','Q22026','Q32026'])-hist['TTM']['revenue'])<1e-6
assert results['bear']['fair_value']<results['base']['fair_value']<results['bull']['fair_value']
print(json.dumps({k:{x:v[x] for x in ['fair_value','upside','terminal_weight']} for k,v in results.items()},indent=2));print('inverse',inverse,'WACC',wacc_derived,'FCFF',normalization['fcff'])
