"""CLX scenario FCFF; USD millions except per share. Sources and assumptions: CLX_report.md. No trading instruction."""
import json
from pathlib import Path
P=Path(__file__).parent
price=99.96; shares=122.027; debt=5158.; cash_available=0.; pension=98.; nci=160.
rf=.0486; erp=.0441; observed_beta=.58; beta=2/3*observed_beta+1/3; kd=.0586; tax=.23
E=price*shares; wacc=E/(E+debt)*(rf+beta*erp)+debt/(E+debt)*kd*(1-tax)
# Acquisition already in sales base/debt; growth after FY27 is organic, no future acquired growth assumed.
configs={
 'adverso':dict(growth=.005,margin1=.135,margin5=.135,terminal_margin=.135,terminal_g=.015,terminal_roic=.12,wacc=wacc+.01,capex_ratio=.042,saas_ratio=.005),
 'central':dict(growth=.025,margin1=.143,margin5=.15,terminal_margin=.15,terminal_g=.02,terminal_roic=.15,wacc=wacc,capex_ratio=.038,saas_ratio=.004),
 'favorable':dict(growth=.04,margin1=.146,margin5=.165,terminal_margin=.16,terminal_g=.025,terminal_roic=.18,wacc=wacc-.005,capex_ratio=.037,saas_ratio=.003)}
def value(c):
 rev=7593.6;rows=[];pv=0.;prev_revenue=7331. # FY26 proforma GOJO sales; do not fund acquisition increase twice.
 for year in range(1,11):
  if year>1:
   g=c['growth'] if year<=5 else c['growth']+(c['terminal_g']-c['growth'])*(year-5)/5
   rev*=1+g
  if year<=5:
   margin=c['margin1']+(c['margin5']-c['margin1'])*(year-1)/4
  else:margin=c['margin5']+(c['terminal_margin']-c['margin5'])*(year-5)/5
  amort=[52,51,34,34,34][min(year,5)-1]
  ebit=rev*margin-amort; nopat=ebit*(1-tax)
  da=rev*.032 + amort # PPE/deferred implementation depreciation proxy + disclosed intangible amortization schedule.
  capex=rev*c['capex_ratio'];saas=rev*c['saas_ratio'];wc=max(0,rev-prev_revenue)*.10
  explicit_reinv=capex+saas+wc-da
  # No perpetual excess D&A: gradual transition to growth/ROIC reinvestment.
  mature_reinv=nopat*c['terminal_g']/c['terminal_roic']
  blend=max(0,year-5)/5
  reinv=(1-blend)*explicit_reinv+blend*mature_reinv
  fcff=nopat-reinv;disc=(1+c['wacc'])**year;pv+=fcff/disc
  rows.append(dict(year=year,revenue=rev,ebit=ebit,nopat=nopat,da=da,capex=capex,saas=saas,working_capital=wc,net_reinvestment=reinv,fcff=fcff,pv=fcff/disc));prev_revenue=rev
 next_nopat=rows[-1]['nopat']*(1+c['terminal_g']);terminal_fcff=next_nopat*(1-c['terminal_g']/c['terminal_roic']);tv=terminal_fcff/(c['wacc']-c['terminal_g']);pvtv=tv/(1+c['wacc'])**10
 ev=pv+pvtv; equity=ev-debt-pension-nci+cash_available
 return dict(assumptions=c,rows=rows,terminal_fcff=terminal_fcff,enterprise_value=ev,equity_value=equity,per_share=equity/shares,pv_terminal_share=pvtv/ev,price_upside=equity/shares/price-1)
out={'as_of':'2026-11-07','price_date':'2026-11-06 regular close 16:00 EST','price':price,'scanner_last':99.9079,'shares_m':shares,'debt_m':debt,'cash_m':184,'cash_available_m':cash_available,'pension_m':pension,'nci_m':nci,'wacc_calibration':dict(rf=rf,erp=erp,observed_beta=observed_beta,blume_beta=beta,kd_assumed=kd,tax=tax,wacc=wacc),'scenarios':{k:value(c) for k,c in configs.items()}}
out['sensitivity']=[dict(wacc=w,terminal_g=g,per_share=value(dict(configs['central'],wacc=w,terminal_g=g))['per_share']) for w in [wacc-.01,wacc,wacc+.01] for g in [.015,.02,.025]]
lo=-.03;hi=.12
for _ in range(80):
 mid=(lo+hi)/2
 if value(dict(configs['central'],growth=mid))['per_share']<price:lo=mid
 else:hi=mid
out['inverse_growth_years2to5']=(lo+hi)/2
lo=.04;hi=.12
for _ in range(80):
 mid=(lo+hi)/2
 if value(dict(configs['central'],wacc=mid))['per_share']>price:lo=mid
 else:hi=mid
out['inverse_wacc']=(lo+hi)/2
out['capex_sensitivity']=[dict(capex_ratio=x,per_share=value(dict(configs['central'],capex_ratio=x))['per_share']) for x in [.032,.035,.038,.042]]
(P/'CLX_model_output.json').write_text(json.dumps(out,indent=2))
print('WACC',wacc, 'values', {k:round(v['per_share'],2) for k,v in out['scenarios'].items()},'inverse',out['inverse_growth_years2to5'])
