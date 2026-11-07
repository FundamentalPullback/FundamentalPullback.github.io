"""NYT support model, USD millions; analyst scenarios, not company forecasts.
Run: python model.py. S1 annual; S2 Q3; ledger in sources.json.
Ten forward years after 2026-09-30 TTM. End-year discount, no stub precision.
"""
import json, pathlib
P=pathlib.Path(__file__).parent
H={
'2023':dict(revenue=2426.152,ebit=276.272,net=232.387,cfo=360.618,capex=22.669,da=86.115,sbc=54.776,eps=1.40),
'2024':dict(revenue=2585.919,ebit=351.096,net=293.825,cfo=410.512,capex=29.173,da=82.936,sbc=67.499,eps=1.77),
'2025':dict(revenue=2824.918,ebit=431.557,net=343.981,cfo=584.489,capex=33.984,da=85.007,sbc=74.183,eps=2.09)}
y26=dict(revenue=2243.229,ebit=330.573,net=278.696,cfo=462.245,capex=26.442,da=62.831,sbc=58.394,eps=1.71)
y25=dict(revenue=2022.604,ebit=269.973,net=214.143,cfo=420.334,capex=27.451,da=64.115,sbc=53.663,eps=1.30)
H['TTM Sep2026']={k:H['2025'][k]+y26[k]-y25[k] for k in y26}
# Four-quarter income tie-out: S15 Q2 2026 Form10-Q, S1 annual, S2 Q3.
# EPS are sums/differences of rounded period EPS, not an exact reweighted TTM EPS.
QUARTERS={
 '2025Q4':dict(revenue=2824.918-2022.604,ebit=431.557-269.973,net=343.981-214.143,eps=2.09-1.30),
 '2026Q1':dict(revenue=1474.691-762.455,ebit=208.635-118.018,net=181.340-93.418,eps=1.11-.57),
 '2026Q2':dict(revenue=762.455,ebit=118.018,net=93.418,eps=.57),
 '2026Q3':dict(revenue=768.538,ebit=121.938,net=97.356,eps=.60)}
for metric in ('revenue','ebit','net'):
 assert abs(sum(q[metric] for q in QUARTERS.values())-H['TTM Sep2026'][metric])<1e-8
for h in H.values(): h.update(fcf=h['cfo']-h['capex'],margin=h['ebit']/h['revenue'])
R=H['TTM Sep2026']['revenue']; PRICE=68.36
# Updated Oct30 ordinary shares plus Q3 dilutive securities; no free future repurchases.
SHARES=159.124622+.780724+(162.252-161.321)
# September declared dividends37.247m used as conservative proxy for October cash payout (S2).
# Operating cash 5% TTM sales. Pension gross conservative, no inaccessible surplus credit.
# Current pension+postretirement proxy 30 (annual total pension 225.863 + retiree health15.3 - noncurrent210.838).
BRIDGE={'cash_and_securities':221.347+451.520+591.842,'october_buybacks':-33.4,'october_dividend_proxy':-37.247,'operating_cash':-.05*R,'debt':0,'pension_and_retiree_gross':-(205.834+30),'minority':0}
BR=sum(BRIDGE.values())
SEED={'digital':1434.336+1218.221-1052.822,'print':1950.778-1434.336+384.047-387.485,'advertising':565.993+418.520-374.341,'other':308.147+222.441-207.956}
assert abs(sum(SEED.values())-R)<1e-6
CASES={
'adverso':dict(sub=[.04,.035,.03,.025,.02],arpu=[0,0,.005,.005,.005],pr=-.05,ad=[-.08,0,.02,.02,.02],other=.02,margins=[.15,.15,.155,.16,.165],mt=.17,w=.098,g=.02,roic=.12),
'base':dict(sub=[.09,.08,.07,.06,.05],arpu=[.015,.015,.015,.01,.01],pr=-.03,ad=[.05,.05,.04,.04,.04],other=.04,margins=[.173,.18,.187,.194,.20],mt=.205,w=.088,g=.025,roic=.15),
'favorable':dict(sub=[.12,.11,.10,.09,.08],arpu=[.02]*5,pr=-.01,ad=[.08]*5,other=.06,margins=[.18,.195,.21,.22,.23],mt=.24,w=.08,g=.03,roic=.20)}
def model(case='base',w=None,g=None,margin_shift=0,sub_shift=0,pension=None):
 c=CASES[case]; w=c['w'] if w is None else w; g=c['g'] if g is None else g
 assert w>g
 seg=SEED.copy();prev=R;rows=[];last_growth=0
 for t in range(1,11):
  if t<=5:
   rates={'digital':(1+c['sub'][t-1]+sub_shift)*(1+c['arpu'][t-1])-1,'print':c['pr'],'advertising':c['ad'][t-1],'other':c['other']}
   seg={k:v*(1+rates[k]) for k,v in seg.items()};rev=sum(seg.values());growth=rev/prev-1;last_growth=growth
   m=c['margins'][t-1]+margin_shift;da=rev*[.026,.025,.023,.021,.019][t-1];capex=rev*[.015,.016,.017,.018,.019][t-1];wc=.01*(rev-prev)
  else:
   x=(t-5)/5;growth=last_growth*(1-x)+g*x;rev=prev*(1+growth);m=c['margins'][4]*(1-x)+c['mt']*x+margin_shift
   da=.019*rev;wc=.01*(rev-prev);nop=rev*m*.75
   # Fade to sustainable g/ROIC capital spending, avoiding abrupt terminal zero reinvestment.
   reinvest_ratio=(.01*(rows[4]['revenue']-rows[3]['revenue'])/rows[4]['nopat'])*(1-x)+(g/c['roic'])*x
   capex=da+nop*reinvest_ratio-wc
  ebit=rev*m;nop=ebit*.75;fcff=nop+da-capex-wc;pv=fcff/(1+w)**t
  rows.append(dict(year=t,revenue=rev,growth=growth,margin=m,ebit=ebit,tax=ebit*.25,nopat=nop,da=da,capex=capex,delta_nwc=wc,fcff=fcff,pv=pv))
  prev=rev
 terminal_nopat=rows[-1]['nopat']*(1+g);terminal_reinvest=terminal_nopat*g/c['roic'];tv=(terminal_nopat-terminal_reinvest)/(w-g);pvt=tv/(1+w)**10
 ev=sum(r['pv'] for r in rows)+pvt;bridge=BR if pension is None else BR+235.834-pension
 return dict(value=(ev+bridge)/SHARES,ev=ev,bridge=bridge,shares=SHARES,wacc=w,g=g,roic=c['roic'],terminal_nopat=terminal_nopat,terminal_reinvestment=terminal_reinvest,terminal_pv=pvt,terminal_weight=pvt/ev,rows=rows)
def solve(key,lo,hi):
 for _ in range(100):
  mid=(lo+hi)/2;v=model(**{key:mid})['value']
  if v<PRICE:lo=mid
  else:hi=mid
 return (lo+hi)/2
res={k:model(k) for k in CASES}
sens=[dict(wacc=w,g=g,value=model(w=w,g=g)['value']) for w in [.078,.083,.088,.093,.098] for g in [.02,.025,.03]]
# Direct FCFF bridge starts EBIT, no addback SBC, normal tax. Pension adjustment removed to avoid subtraction twice.
norm_ebit=H['TTM Sep2026']['ebit']+(2.967+9.219-4.453)+2.858
norm_fcff=norm_ebit*.75+H['TTM Sep2026']['da']-40-2
out=dict(asof='2026-11-07',price=PRICE,price_timestamp='2026-11-06 16:00 EST',scanner_last=68.36,historical=H,quarters=QUARTERS,eps_method='Rounded period EPS bridge; approximate TTM, no forecast valuation dependence.',seed=SEED,bridge=BRIDGE,assumptions=CASES,cases=res,sensitivity=sens,reverse=dict(margin_shift=solve('margin_shift',0,.2),subscriber_growth_shift=solve('sub_shift',0,.3)),normalized=dict(ebit=norm_ebit,fcff=norm_fcff,capex=40,delta_nwc=2,tax=.25),checks=dict(seed_tie=True,positive_fcff=all(r['fcff']>0 for c in res.values() for r in c['rows']),horizon=10,wacc_gt_g=all(c['wacc']>c['g'] for c in res.values()),four_quarter_tie=all(abs(sum(q[k] for q in QUARTERS.values())-H['TTM Sep2026'][k])<1e-8 for k in ('revenue','ebit','net')),terminal_reinvestment_tie=all(abs(c['rows'][-1]['fcff']*(1+c['g'])-(c['terminal_nopat']-c['terminal_reinvestment']))<1e-8 for c in res.values())),confidence='media',status='completed_conditional_review',decision='Buena empresa; esperar precio',historical_pe={'2023':48.99/1.40,'2024':52.05/1.77,'2025':69.42/2.09,'current_ttm':PRICE/2.50})
(P/'results.json').write_text(json.dumps(out,indent=2));print(json.dumps({k:{a:v[a] for a in ['value','terminal_weight']} for k,v in res.items()},indent=2));print(out['reverse']);print(out['normalized'])
