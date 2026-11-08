"""Conditional pre-divestiture CAE FCFF; CAD millions unless price USD. Standard library only."""
import json,csv
from pathlib import Path
P=Path(__file__).parent
# Primary source: fy25/fy26 statements, q1fy27_mda rolling segment tables,
# q1fy26_mda and q3fy26_mda cash flows; Q2 SBC/leases from six-month cash flow.
# sbc is equity-settled compensation added back in CFO, not total share-based remuneration.
cols='revenue ebit net_parent eps cfo ppe intangible da sbc lease_principal wc_cash jv_profit jv_div jv_contribution'.split()
data={
'FY2024':[4282.8,-185.4,-325.3,-1.02,566.9,329.8,147.9,368.7,14.8,69.5,128.1,72.2,37.1,43.9],
'FY2025':[4707.9,729.2,405.3,1.27,896.5,356.2,87.9,414.7,25.2,59.9,197.1,88.3,28.7,19.0],
'FY2026':[4914.,612.3,313.1,.97,791.9,287.8,73.7,460.1,36.7,61.1,-37.7,82.7,79.6,31.6],
'Q1FY2025':[1072.5,108.6,48.3,.15,-12.9,92.6,28.6,97.8,16.3,13.8,-140.1,24.,10.5,-.1],
'Q1FY2026':[1098.6,133.8,57.2,.18,-15.3,106.9,22.4,113.7,19.5,15.8,-204.5,21.6,20.1,13.1],
'Q2FY2026':[1236.6,155.3,73.9,.23,214.,87.6,20.,114.,6.5,17.7,27.9,15.9,13.9,5.],
'Q3FY2026':[1252.1,195.8,108.9,.34,407.6,50.6,12.8,115.5,5.3,13.9,184.9,25.3,27.,6.2],
'Q4FY2026':[1326.7,127.4,73.1,.23,185.6,42.7,18.5,116.9,5.4,13.7,-46.,19.9,18.6,7.3],
'Q1FY2027':[1173.4,86.8,31.,.10,175.1,51.7,8.8,120.5,12.,20.4,19.,17.,7.1,5.5]}
h={k:dict(zip(cols,v)) for k,v in data.items()}
for name,fy,qnew,qold in [('TTM20260630','FY2026','Q1FY2027','Q1FY2026'),('TTM20250630','FY2025','Q1FY2026','Q1FY2025')]:h[name]={k:h[fy][k]+h[qnew][k]-h[qold][k] for k in cols}
for k,v in h.items():
 v['fcf_simple']=v['cfo']-v['ppe']-v['intangible']
 v['cash_after_sbc_lease_jv']=v['fcf_simple']-v['sbc']-v['lease_principal']+v['jv_div']-v['jv_contribution']
 v['cash_neutral_wc']=v['cash_after_sbc_lease_jv']-v['wc_cash']
 v['ebit_margin']=v['ebit']/v['revenue']
 v['cash_scope']='FY24 cash includes discontinued Healthcare; not used for valuation' if k=='FY2024' else 'continuing operations'
with (P/'history.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=['period']+list(next(iter(h.values())).keys()));w.writeheader();w.writerows(dict(period=k,**v) for k,v in h.items())
PRICE=26.85; FX=1.4113;SHARES=324.;DEBT=3214.9;CASH=568.7;RESERVE=150.;PENSION=109.9;NCI=73.5
RF=.0367;ERP=.0463;BETA=1.2;KE=RF+BETA*ERP;KD=.06;TAX=.25
# Retain US sovereign spread in ERP (4.41+0.22) rather than treating US Treasury as CAD riskfree.
DWEIGHT=DEBT/(DEBT+PRICE*FX*SHARES);WACC=KE*(1-DWEIGHT)+KD*(1-TAX)*DWEIGHT
BASE=h['TTM20260630']['revenue']
cases={
'adverso':dict(growth=[.01,.025,.03,.03,.03],margins=[.105,.11,.115,.12,.12],terminal_margin=.12,g=.02,roic=.10,sc=1.1,wacc=WACC+.01,jv_cash=20.,ke=KE+.01),
'central':dict(growth=[.03,.05,.05,.05,.04],margins=[.117,.122,.13,.137,.143],terminal_margin=.14,g=.025,roic=.125,sc=1.5,wacc=WACC,jv_cash=40.,ke=KE),
'favorable':dict(growth=[.04,.065,.065,.06,.05],margins=[.125,.135,.145,.155,.16],terminal_margin=.16,g=.03,roic=.15,sc=2.,wacc=WACC-.005,jv_cash=55.,ke=KE-.005)}
def value(c):
 revenue=BASE; rows=[];pv=0;jvpv=0
 for y in range(1,11):
  t=max(0,(y-5)/5)
  g=c['growth'][y-1] if y<=5 else c['growth'][-1]*(1-t)+c['g']*t
  margin=c['margins'][y-1] if y<=5 else c['margins'][-1]*(1-t)+c['terminal_margin']*t
  old=revenue;revenue*=1+g;nopat=revenue*margin*(1-TAX)
  net_reinvestment=(revenue-old)/c['sc'] if y<=5 else (1-t)*(revenue-old)/c['sc']+t*nopat*g/c['roic']
  da=revenue*(466.9/BASE);wc=(revenue-old)*.08
  capex=da+net_reinvestment-wc # gross economic investment includes lease additions, software
  transformation=45. if y==1 else 15. if y==2 else 0.
  fcff=nopat+da-capex-wc-transformation
  pv+=fcff/(1+c['wacc'])**y
  jv=c['jv_cash']*(1+.02)**y;jvpv+=jv/(1+c['ke'])**y
  rows.append(dict(year=y,revenue=revenue,margin=margin,nopat=nopat,da=da,capex_including_leases=capex,delta_wc=wc,net_reinvestment=net_reinvestment,transformation_cash=transformation,fcff=fcff,jv_net_distribution=jv))
 terminal_nopat=revenue*(1+c['g'])*c['terminal_margin']*(1-TAX)
 terminal_reinvestment=terminal_nopat*c['g']/c['roic'];tv=(terminal_nopat-terminal_reinvestment)/(c['wacc']-c['g']);pvtv=tv/(1+c['wacc'])**10
 jvterminal=rows[-1]['jv_net_distribution']*1.02/(c['ke']-.02)/(1+c['ke'])**10;jvvalue=jvpv+jvterminal
 ev=pv+pvtv;eq=ev+jvvalue-DEBT+(CASH-RESERVE)-PENSION-NCI
 return dict(value_usd=eq/SHARES/FX,value_cad=eq/SHARES,ev_core=ev,jv_equity_value=jvvalue,equity=eq,pv_terminal=pvtv,terminal_weight=pvtv/ev,terminal_reinvestment=terminal_reinvestment,rows=rows)
res={k:value(v) for k,v in cases.items()}
sensitivity=[dict(wacc=w,g=g,value_usd=value(dict(cases['central'],wacc=w,g=g))['value_usd']) for w in [WACC-.01,WACC,WACC+.01] for g in [.02,.025,.03]]
reverse=[]
for growth in [.03,.05,.07]:
 lo=.05;hi=.35
 for _ in range(80):
  m=(lo+hi)/2;c=dict(cases['central'],growth=[growth]*5,margins=[m]*5,terminal_margin=m)
  if value(c)['value_usd']<PRICE:lo=m
  else:hi=m
 reverse.append(dict(first5_growth=growth,required_constant_core_ebit_margin=(lo+hi)/2))
normalized={'ttm_current_core_ebit_before_recurring_restructure':565.3-78.1+132.7,'ttm_prior_core_ebit_before_recurring_restructure':754.4-85.9+30.9+22.3-72.6+10.6,'recurring_restructure_allowance':30.,'acquisition_amortization_retained':True,'SBC_retained':True}
result=dict(asof='2026-11-08',status='material_partial_conditional_pre_divestiture_model',entry_approved=False,price_usd=PRICE,price_asof='2026-11-06 16:00 America/New_York',fx_cad_per_usd=FX,base_revenue=BASE,history=h,normalization=normalized,discount=dict(rf=RF,rf_date='2026-11-05',erp=ERP,beta_assumed=BETA,ke=KE,kd_assumed=KD,tax=TAX,debt_weight=DWEIGHT,wacc=WACC),bridge=dict(shares=SHARES,debt_including_leases_rd=DEBT,cash=CASH,operating_cash_reserve=RESERVE,pension_gross=PENSION,nci=NCI),cases=cases,results=res,sensitivity=sensitivity,reverse=reverse,flightscape=dict(proceeds_included=0,perimeter='pre-sale group retained',material_gap='Carve-out cash earnings, transferred claims, taxes, fees and net proceeds not disclosed in reviewed sale announcement'),notes=['FY24 net parent and EPS continuing; cash includes discontinued and is explicitly flagged','TTM EPS computed as annual plus new quarter minus old; approximate due denominator rounding','Joint ventures excluded from taxable consolidated EBIT, separately valued net equity distributions at Ke','Lease liabilities deducted once; economic gross capex includes future leased asset renewal; lease principal not subtracted again in FCFF','Book pension assets not credited as distributable cash','No free future buybacks or sale proceeds','No post-June quarterly actuals assumed'])
(P/'results.json').write_text(json.dumps(result,indent=2))
assert abs(sum(h[k]['revenue'] for k in ['Q2FY2026','Q3FY2026','Q4FY2026','Q1FY2027'])-BASE)<1e-6
for x in res.values():
 assert all(abs(r['fcff']-(r['nopat']+r['da']-r['capex_including_leases']-r['delta_wc']-r['transformation_cash']))<1e-6 for r in x['rows'])
print(json.dumps({k:{z:v[z] for z in ['value_usd','terminal_weight','ev_core','jv_equity_value']} for k,v in res.items()},indent=2));print('WACC',WACC,'Reverse',reverse)
