"""MCD FCFF, USD millions; analyst scenarios, not trading instructions.
Run python model.py. All inputs sourced/labelled in report.md. Standard library only.
"""
import json, pathlib, math
ROOT=pathlib.Path(__file__).resolve().parent
P=276.52
SH=705.784744+1.7 # current basic + latest treasury-stock dilution; no future buybacks
DEBT=39820; CASH=193 # 1193 less 1000 operating reserve
AFFIL=2985; BENEFITS=70 # book investment value / net supplemental benefits proxy
BRIDGE=CASH+AFFIL-DEBT-BENEFITS
STUB_YEARS=54/365
STUB_FCFF=(12586*.78+2274-3460-532-15.18)*STUB_YEARS # analyst prorating, not reported guidance
raw={
'2023':[25494,11647,8469,11.56,9612,1978,2357,175,676],
'2024':[25920,11712,8223,11.39,9447,2097,2775,172,498],
'2025':[26885,12393,8563,11.95,10551,2199,3365,165,579],
'9M2024':[19532,8844,6207,8.59,6816,1544,1968,128,392],
'9M2025':[19876,9237,6399,8.92,7854,1623,2306,128,430],
'9M2026':[20773,9887,6831,9.61,8254,1698,2401,145,383],
'Q1_2026':[6517,2953,1983,2.78,2412,566,682,60,122],
'Q2_2026':[7099,3338,2362,3.32,2807,565,831,39,121],
'Q3_2026':[7157,3595,2486,3.51,3031,567,884,46,139]}
keys=['revenue','ebit','net_income','eps','cfo','da','capex','sbc','other_investing_outflow']
H={k:dict(zip(keys,v)) for k,v in raw.items()}
for label,a,b,c in [('TTM2026','2025','9M2026','9M2025'),('TTM2025','2024','9M2025','9M2024'),('Q4_2025','2025',None,'9M2025')]:
 H[label]={k:H[a][k]+(H[b][k] if b else 0)-H[c][k] for k in keys}
# Other investing is reported, not all identified as software.
for h in H.values():h['fcf_reported']=h['cfo']-h['capex'];h['fcf_after_sbc_other']=None if h['other_investing_outflow'] is None else h['fcf_reported']-h['sbc']-h['other_investing_outflow']
rf=.0486; erp=.0441; beta=.43*2/3+1/3; kd=rf+.01; tax=.22
weightD=36500/(36500+P*SH)
wacc= (rf+beta*erp)*(1-weightD)+kd*(1-tax)*weightD+.005
SC={'adverso':dict(sss=.01,unit=.02,margin5=.47,marginT=.45,w=.085,g=.02,roic=.15),
'base':dict(sss=.025,unit=.025,margin5=.535,marginT=.52,w=wacc,g=.025,roic=.20),
'favorable':dict(sss=.04,unit=.0275,margin5=.56,marginT=.55,w=.07,g=.03,roic=.25)}
def run(c,sss=None,w=None,g=None,margin=None,other_scale=1):
 c=c.copy(); c['sss']=c['sss'] if sss is None else sss;c['w']=c['w'] if w is None else w;c['g']=c['g'] if g is None else g
 if margin is not None:c['margin5']=margin;c['marginT']=margin-.015
 fr,co,oth=17197.,9858.,727.; prev=fr+co+oth; out=[]
 for y in range(1,11):
  tr=max(0,(y-5)/5); u=c['unit']+(0.02-c['unit'])*min(y-1,3)/3
  fg=(1+c['sss'])*(1+u)-1; cg=c['sss']-.01; og=.03
  fg=fg*(1-tr)+c['g']*tr;cg=cg*(1-tr)+c['g']*tr;og=og*(1-tr)+c['g']*tr
  fr*=1+fg;co*=1+cg;oth*=1+og; rev=fr+co+oth
  # Pre-relief operating margin excludes affiliate earnings/disposal gains; retains SBC.
  m=(12586/27782)+(c['margin5']-(12586/27782))*min(y,5)/5
  if y>5:m=c['margin5']+(c['marginT']-c['margin5'])*tr
  rent=812.5 if y<=4 else 2500/6
  partner=437.5 if y<=4 else 1000/6
  ebit=rev*m-rent;nopat=ebit*(1-tax); da=2274*(rev/27782);dnwc=.01*(rev-prev)
  software=550*(1.03**(y-1))*other_scale
  directcap=3000*(1.025**max(0,y-4))+partner+software
  terminal_reinv=nopat*c['g']/c['roic']
  capex=directcap*(1-tr)+(da+terminal_reinv-dnwc)*tr
  reinv=capex-da+dnwc;fcff=nopat-reinv
  assert capex>=partner+software and fcff>0
  out.append(dict(year=2026+y,franchise_revenue=fr,company_sales=co,other_revenue=oth,revenue=rev,pre_relief_margin=m,rent_support=rent,ebit=ebit,nopat=nopat,da=da,baseline_capex=capex-partner-software,partner_capex=partner,software_other_capex=software,capex=capex,dnwc=dnwc,reinvestment=reinv,fcff=fcff,pv=fcff/(1+c['w'])**(y+STUB_YEARS)))
  prev=rev
 last=out[-1]; nt=last['nopat']*(1+c['g']);ft=nt*(1-c['g']/c['roic']);tv=ft/(c['w']-c['g']); pvt=tv/(1+c['w'])**(10+STUB_YEARS);stubpv=STUB_FCFF/(1+c['w'])**STUB_YEARS;ev=sum(r['pv'] for r in out)+pvt+stubpv
 assert abs(last['reinvestment']/last['nopat']-c['g']/c['roic'])<1e-10
 assert abs(sum(r['partner_capex']+r['rent_support'] for r in out)-8500)<1e-7
 return dict(inputs=c,stub_years=STUB_YEARS,stub_fcff=STUB_FCFF,stub_pv=stubpv,years=out,terminal_nopat=nt,terminal_fcff=ft,terminal_da=last['da']*(1+c['g']),terminal_dnwc=.01*last['revenue']*c['g'],terminal_capex=last['da']*(1+c['g'])+nt*c['g']/c['roic']-.01*last['revenue']*c['g'],ev=ev,bridge=BRIDGE,equity=ev+BRIDGE,shares=SH,value=(ev+BRIDGE)/SH,upside=(ev+BRIDGE)/SH/P-1,terminal_weight=pvt/ev)
def bisect(fn,target,lo,hi):
 if (fn(lo)-target)*(fn(hi)-target)>0:return None
 for _ in range(100):
  mid=(lo+hi)/2
  if fn(mid)>target:hi=mid
  else:lo=mid
 return (lo+hi)/2
R={k:run(v) for k,v in SC.items()}
S=[dict(wacc=w,g=g,value=run(SC['base'],w=w,g=g)['value']) for w in [.07,.075,.08,.085,.09] for g in [.02,.025,.03]]
inv=[dict(margin5=m,sss=bisect(lambda s:run(SC['base'],sss=s,margin=m)['value'],P,-.05,.15)) for m in [.50,.535,.56]]
result=dict(as_of='2026-11-07',price=dict(close=P,date='2026-11-06',time='16:00 America/New_York',scanner_last=277.0999),history=H,cost_capital=dict(rf=rf,erp=erp,beta_raw=.43,beta_adjusted=beta,cost_debt=kd,debt_weight=weightD,execution_premium=.005,wacc=wacc),scenarios=R,sensitivity=S,inverse=inv,proxy_tests=dict(no_software_other=run(SC['base'],other_scale=0)['value'],double_software_other=run(SC['base'],other_scale=2)['value'],affiliate_zero=R['base']['value']-AFFIL/SH,all_other_longterm_liabilities=R['base']['value']-(666-BENEFITS)/SH,all_cash_excess=R['base']['value']+1000/SH,market_value_debt=R['base']['value']+(39820-36500)/SH,full_antidilution=R['base']['equity']/(SH+4.4)))
(ROOT/'results.json').write_text(json.dumps(result,indent=2));print(json.dumps({k:{a:v[a] for a in ['value','upside','terminal_weight']} for k,v in R.items()},indent=2));print('WACC',wacc,'inverse',inv,'proxy',result['proxy_tests'])
