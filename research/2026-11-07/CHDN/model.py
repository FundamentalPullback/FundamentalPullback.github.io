"""CHDN diagnostic FCFF; not an approved valuation. USD millions. Run in this directory.
Primary source inputs from SEC filings cited in sources.json. Remaining assumptions
are explicitly analytical, not management guidance. Affiliates treated separately (levered
cash distributions discounted at cost of equity); never add their book value as well.
"""
import json,csv
from pathlib import Path
P=Path(__file__).parent
price=97.94; shares=68.548342; debt=4748; cash=167; minority=24
# Finance leases: last independently quantified annual value, NOT verified Sep26.
finance_lease_proxy=27.8
rf=.0486; beta=.77; erp=.0441; ke=rf+beta*erp
# Historical issuer cost, not current bond yield: 9M26 net interest annualized / avg gross debt.
kd=(211*4/3)/((5155+4748)/2); tax=.26
E=price*shares; D=debt
wacc=ke*E/(E+D)+kd*(1-tax)*D/(E+D)
actual={
'2023':dict(revenue=2461.7,ebit=564,net_income=417.3,cfo=605.3,da=169,sbc=32.9,maintenance=77.7,project=598.8,affiliate_distributions=155.1),
'2024':dict(revenue=2734.3,ebit=709,net_income=426.8,cfo=771.7,da=199.1,sbc=36.1,maintenance=83.6,project=463.4,affiliate_distributions=138.7),
'2025':dict(revenue=2925.9,ebit=683.8,net_income=383,cfo=769.8,da=233.1,sbc=30.2,maintenance=70.2,project=204.7,affiliate_distributions=116),
'9M2024':dict(revenue=2110.1,ebit=582.2,net_income=355.1,cfo=641.1,da=145.7,sbc=23.2,maintenance=49.8,project=367.8,affiliate_distributions=113.8),
'9M2025':dict(revenue=2260,ebit=560.3,net_income=331.7,cfo=673.8,da=173.5,sbc=18.2,maintenance=52.9,project=171.7,affiliate_distributions=91.7),
'9M2026':dict(revenue=2339,ebit=643,net_income=404,cfo=660,da=176,sbc=19,maintenance=57,project=119,affiliate_distributions=106),
'Q1_2026':dict(revenue=663,ebit=143,net_income=83,cfo=295,da=56,sbc=5,maintenance=19,project=40,affiliate_distributions=36),
'Q2_2026':dict(revenue=980,ebit=357,net_income=241,cfo=217,da=59,sbc=8,maintenance=19,project=39,affiliate_distributions=36),
'Q3_2026':dict(revenue=696,ebit=143,net_income=80,cfo=148,da=61,sbc=6,maintenance=19,project=40,affiliate_distributions=34)}
for label,value in {'2023':146.3,'2024':144.9,'2025':139.4,'9M2024':108.9,'9M2025':105.4,'9M2026':115,'Q1_2026':36,'Q2_2026':41,'Q3_2026':38}.items():
 actual[label]['affiliate_equity_income']=value
for label,annual,add,sub in [('TTM2026','2025','9M2026','9M2025'),('TTM2025','2024','9M2025','9M2024')]:
 actual[label]={k:actual[annual][k]+actual[add][k]-actual[sub][k] for k in actual[annual]}
actual['Q4_2025']={k:actual['2025'][k]-actual['9M2025'][k] for k in actual['2025']}
for d in actual.values():d['fcf_after_all_capex']=d['cfo']-d['maintenance']-d['project']
(P/'actuals.json').write_text(json.dumps(actual,indent=2))
cases={'adverso':dict(growth=.01,margin=.23,terminal_g=.015,roic=.08,wacc=wacc+.02,jv_growth=0,jv_haircut=.2), 'central':dict(growth=.04,margin=.26,terminal_g=.025,roic=.10,wacc=wacc+.01,jv_growth=.025,jv_haircut=.1), 'favorable':dict(growth=.065,margin=.28,terminal_g=.03,roic=.12,wacc=wacc,jv_growth=.04,jv_haircut=0)}
def run(c,margin_override=None):
 rev=actual['TTM2026']['revenue']; old_nopat=actual['TTM2026']['ebit']*(1-tax); m0=actual['TTM2026']['ebit']/rev
 rows=[];pv=0;jvpv=0;dist=actual['TTM2026']['affiliate_distributions']*(1-c['jv_haircut']);m5=margin_override or c['margin']
 for y in range(1,11):
  g=c['growth'] if y<=5 else c['growth']+(c['terminal_g']-c['growth'])*(y-5)/5
  margin=m0+(m5-m0)*min(y,5)/5
  rev*=1+g;ebit=rev*margin;nopat=ebit*(1-tax);da=rev*.078
  nwc=.02*(rev/(1+g))*g
  # Gross physical reinvestment includes depreciation replacement, software, and growth.
  growth_reinvest=max(0,(nopat-old_nopat)/c['roic']);capex=da+growth_reinvest-nwc
  # Explicit near-term project burden, no growth without spending. Analyst timing allocation.
  if y<=2:capex=max(capex,350 if y==1 else 320)
  reinvest=capex-da+nwc;fcff=nopat-reinvest;pv+=fcff/(1+c['wacc'])**y
  jg=c['jv_growth'] if y<=5 else c['jv_growth']+(c['terminal_g']-c['jv_growth'])*(y-5)/5
  dist*=1+jg;jvpv+=dist/(1+ke+.02)**y
  rows.append(dict(year=y,revenue=rev,ebit=ebit,nopat=nopat,da=da,capex=capex,delta_nwc=nwc,reinvestment=reinvest,fcff=fcff,jv_distribution=dist));old_nopat=nopat
 terminal_fcff=nopat*(1+c['terminal_g'])*(1-c['terminal_g']/c['roic'])
 tv=terminal_fcff/(c['wacc']-c['terminal_g']);pvtv=tv/(1+c['wacc'])**10
 jvtv=dist*(1+c['terminal_g'])/(ke+.02-c['terminal_g'])/(1+ke+.02)**10
 ev=pv+pvtv;jv=jvpv+jvtv;equity=ev+jv+cash-debt-minority-finance_lease_proxy
 return dict(diagnostic_only=True,operating_ev=ev,operating_explicit_pv=pv,operating_terminal_value_year10=tv,operating_terminal_pv=pvtv,jv_explicit_pv=jvpv,jv_terminal_pv=jvtv,jv_terminal_share=jvtv/jv,jv_equity_value=jv,equity_value=equity,raw_per_share=equity/shares,per_share=max(0,equity/shares),terminal_share_of_operating_ev=pvtv/ev,terminal_fcff=terminal_fcff,rows=rows)
results={}
for name,c in cases.items():
 r=run(c);rows=r.pop('rows');results[name]=r
 with (P/f'forecast_{name}.csv').open('w') as f:
  w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
lo,hi=.05,.6
for _ in range(100):
 mid=(lo+hi)/2
 if run(cases['central'],mid)['per_share']<price:lo=mid
 else:hi=mid
sensitivity=[]
for w in [wacc,wacc+.01,wacc+.02]:
 for g in [.015,.025,.03]:
  c=dict(cases['central'],wacc=w,terminal_g=g);sensitivity.append(dict(wacc=w,g=g,diagnostic_value=run(c)['per_share']))
out=dict(ticker='CHDN',as_of='2026-11-08',status='partial',approved_valuation=None,regular_close=dict(price=price,date='2026-11-06',time='16:00 EST'),market_inputs=dict(rf=rf,beta=beta,erp=erp,ke=ke,kd_historical_proxy=kd,wacc_unadjusted=wacc),bridge=dict(debt=debt,cash=cash,restricted_cash_excluded=92,minority=minority,finance_lease_proxy=finance_lease_proxy,shares=shares,cash_treatment='All unrestricted cash assumed excess for diagnostic only; minimum operating cash unverified'),diagnostic_scenarios=results,sensitivity=sensitivity,inverse_diagnostic_year5_margin=(lo+hi)/2,limitations=['JV distribution sustainability and standalone reinvestment not validated','Current marginal issuer debt yield not independently verified; historical cost proxy','Finance lease roll-forward from Dec25 to Sep26 not isolated','No approved price target; scenarios diagnostic only','Unrestricted cash is not proven excess cash; minimum operating cash unresolved','Post-Oct21 shares and deferred compensation claims unreconciled','Project capex timing and normalized comparable history incomplete'])
(P/'results.json').write_text(json.dumps(out,indent=2));(P/'assumptions.json').write_text(json.dumps(cases,indent=2));print(json.dumps(out,indent=2))
