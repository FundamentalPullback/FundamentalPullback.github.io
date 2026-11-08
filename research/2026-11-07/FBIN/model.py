"""FBIN 2026-11-07. USD millions except per share. No external packages.
Reported inputs: official 2025 10-K and Q3 2026 10-Q / IR releases linked in source_ledger.json.
Assumptions are explicit, not guidance. 10 forward years, years6-10 transition.
"""
import json, math
from pathlib import Path
P=Path(__file__).parent
PRICE=48.08; SHARES=119.3; DEBT=2318.7; CASH=230.9; OPERATING_CASH=100; PENSION=33.4
RF=.0529; ERP=.0441; BETA=1.33; TAX=.25
# Portfolio yield derived from observed Sep26 2026 senior note fair value 2004.2.
# Actual contractual principal/coupon/maturities; semiannual approximate remaining maturities.
BONDS=[(700,.0325,3),(450,.04,5.5),(600,.05875,6.667),(450,.045,25.5)]
def bondvalue(y):
 return sum(sum(p*c/2/(1+y/2)**k for k in range(1,round(t*2)+1))+p/(1+y/2)**round(t*2) for p,c,t in BONDS)
def bisect(fn,lo,hi,target):
 for _ in range(150):
  m=(lo+hi)/2
  if fn(m)>target:hi=m
  else:lo=m
 return (lo+hi)/2
KD=bisect(lambda y:-bondvalue(y),0,.2,-2004.2)
MVDEBT=2122.9; EQUITY=PRICE*SHARES
WACC=(RF+BETA*ERP)*EQUITY/(EQUITY+MVDEBT)+KD*(1-TAX)*MVDEBT/(EQUITY+MVDEBT)
SC={
 'adverso':dict(revenue=[3800,3800,3876,3954,4033],margin=[.10,.115,.12,.125,.13],terminal_margin=.125,g=.02,roic=.10,nwc=.17,capex=.035,da=.033,proceeds=125,exit_costs=100),
 'central':dict(revenue=[3950,4068.5,4231.24,4400.49,4532.50],margin=[.13,.145,.155,.16,.165],terminal_margin=.16,g=.025,roic=.12,nwc=.15,capex=.032,da=.034,proceeds=145,exit_costs=65),
 'favorable':dict(revenue=[4100,4305,4563.3,4791.47,4983.13],margin=[.145,.165,.18,.185,.19],terminal_margin=.18,g=.03,roic=.15,nwc=.14,capex=.033,da=.034,proceeds=160,exit_costs=35)}
def value(name='central',wacc=WACC,g=None,margin_shift=0,growth_extra=0,software_extra=0):
 s=SC[name];g=s['g'] if g is None else g
 rows=[];prev=4240; pv=0
 for y in range(1,11):
  if y<=5:
   sales=s['revenue'][y-1]*(1+growth_extra)**y; margin=s['margin'][y-1]+margin_shift
   da=sales*s['da']; capex=sales*s['capex']+software_extra
   # No artificial WC release from divestment perimeter. Revenues exiting do not create free cash twice.
   dnwc=max(0,sales-prev)*s['nwc'];nopat=sales*margin*(1-TAX)
  else:
   a=(y-5)/5;growth=(1-a)*(.03+growth_extra)+a*g;sales=prev*(1+growth)
   margin=(1-a)*(s['margin'][4]+margin_shift)+a*(s['terminal_margin']+margin_shift)
   nopat=sales*margin*(1-TAX);da=sales*((1-a)*s['da']+a*.025)
   dnwc=(sales-prev)*s['nwc']
   reinv=(1-a)*(sales*(s['capex']-s['da'])+dnwc)+a*nopat*g/s['roic']
   capex=da+reinv-dnwc+software_extra
  fcff=nopat+da-capex-dnwc
  rows.append(dict(year=y,revenue=sales,ebit_margin=margin,ebit=sales*margin,tax=TAX,nopat=nopat,da=da,capex_including_software=capex,delta_nwc=dnwc,fcff=fcff,pv_fcff=fcff/(1+wacc)**y))
  pv+=rows[-1]['pv_fcff'];prev=sales
 # No hidden terminal discontinuity; positive physical capex and WC consistent with g/ROIC.
 terminal_nopat=rows[-1]['nopat']*(1+g); terminal_reinv=terminal_nopat*g/s['roic'];terminal_fcff=terminal_nopat-terminal_reinv-software_extra
 terminal_da=prev*(1+g)*.025;terminal_nwc=prev*g*s['nwc'];terminal_capex=terminal_da+terminal_reinv-terminal_nwc+software_extra
 tv=terminal_fcff/(wacc-g);pvtv=tv/(1+wacc)**10;ev=pv+pvtv
 equity=ev-DEBT+CASH-OPERATING_CASH-PENSION+s['proceeds']-s['exit_costs']
 return dict(scenario=name,wacc=wacc,g=g,roic=s['roic'],rows=rows,terminal=dict(nopat=terminal_nopat,reinvestment=terminal_reinv,da=terminal_da,capex=terminal_capex,delta_nwc=terminal_nwc,fcff=terminal_fcff),pv_explicit=pv,pv_terminal=pvtv,terminal_weight=pvtv/ev,ev=ev,equity=equity,value=equity/SHARES,mos=1-PRICE/(equity/SHARES))
def run():
 annual={'2023':dict(revenue=4626.2,ebit=614.9,net_income=404.5,eps=3.17,cfo=1055.8,capex=256.5,da=168.8,sbc=34.2,cash=366.4,debt=2670.1,shares=127.7), '2024':dict(revenue=4609,ebit=737.9,net_income=471.9,eps=3.75,cfo=667.8,capex=193.3,da=193.6,sbc=39.3,cash=381.1,debt=2673.3,shares=125.7),'2025':dict(revenue=4463.2,ebit=516.1,net_income=298.8,eps=2.47,cfo=478.6,capex=111.8,da=194.4,sbc=20.8,cash=264,debt=2544.9,shares=121.2)}
 q=[dict(period='Q4 2025',revenue=1077.5,ebit=121.6,net_income=76.4,eps=.63,cfo=208.2,capex=24.5,da=42.9),dict(period='Q1 2026',revenue=1011.3,ebit=60.2,net_income=24.2,eps=.20,cfo=-119.2,capex=20.3,da=42.1),dict(period='Q2 2026 derived latest 9m less Q1/Q3',revenue=1153.9,ebit=-8.9,net_income=-22.5,eps=-.19,cfo=202.8,capex=23.5,da=42.6),dict(period='Q3 2026',revenue=1113.7,ebit=60.4,net_income=49.9,eps=.42,cfo=347,capex=15.9,da=36.5)]
 ttm={k:sum(r[k] for r in q) for k in ['revenue','ebit','net_income','cfo','capex','da']}
 prior=dict(revenue=4609-3504.8+3385.7,ebit=737.9-559.6+394.4,net_income=471.9-366.8+222.4,cfo=667.8-395.5+270.4,capex=193.3-133.1+87.3,da=193.6-147.4+151.5)
 for r in list(annual.values())+[ttm,prior]+q:r['fcf']=r['cfo']-r['capex'];r['ebit_margin']=r['ebit']/r['revenue']
 result=dict(as_of='2026-11-07',price=dict(close=PRICE,session='2026-11-06 regular NYSE close',time='16:00 America/New_York; 21:00 UTC',scanner_last=48.08),capital=dict(rf=RF,erp=ERP,beta=BETA,cost_of_equity=RF+BETA*ERP,kd=KD,wacc=WACC,debt_principal=DEBT,debt_market_weight=MVDEBT,cash=CASH,operating_cash_reserve=OPERATING_CASH,pension=PENSION,diluted_shares=SHARES),annual=annual,quarters=q,ttm=ttm,prior_ttm=prior,scenarios={k:value(k) for k in SC},sensitivity=[dict(wacc=w,g=g,value=value(wacc=w,g=g)['value']) for w in [WACC-.01,WACC,WACC+.01] for g in [.02,.025,.03]],reverse=dict(required_margin_shift=bisect(lambda x:value(margin_shift=x)['value'],-.05,.15,PRICE),required_growth_extra=bisect(lambda x:value(growth_extra=x)['value'],-.05,.15,PRICE)),proxy_bounds=dict(software_10m_annual=value(software_extra=10)['value'],full_antidilution_value=value()['equity']/(SHARES+1.8),debt_fair_value_bridge=value()['value']+(DEBT-MVDEBT)/SHARES))
 (P/'model_results.json').write_text(json.dumps(result,indent=2)); print(json.dumps({k:{'value':v['value'],'terminal':v['terminal_weight']} for k,v in result['scenarios'].items()},indent=2));print('wacc',WACC,'kd',KD,'reverse',result['reverse']);print('ttm',ttm,'prior',prior)
if __name__=='__main__':run()
