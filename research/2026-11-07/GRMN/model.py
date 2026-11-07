"""GRMN FCFF 5+5, USD millions. Analyst scenarios, not trade instructions."""
import json,csv
from pathlib import Path
P=Path(__file__).parent
PRICE=285.57; SHARES=193.617; REV=7886.613
# Restricted cash excluded. 5% operating cash reserve, declared dividends deducted conservatively.
BRIDGE=2039.779+299.693+1727.086-.05*REV-404.779
H=[dict(period='FY2023',revenue=5228.252,ebit=1092.160,net=1289.636,cfo=1376.265,capex=193.524,da=177.572,sbc=101.422),dict(period='FY2024',revenue=6296.903,ebit=1593.994,net=1411.436,cfo=1432.471,capex=193.571,da=179.735,sbc=137.162),dict(period='FY2025',revenue=7245.519,ebit=1876.076,net=1663.887,cfo=1633.359,capex=270.446,da=188.759,sbc=166.003)]
N26=dict(revenue=5761.658,ebit=1658.821,net=1488.660,cfo=1333.399,capex=294.982,da=149.211,sbc=133.526)
N25=dict(revenue=5120.564,ebit=1261.922,net=1135.206,cfo=1079.574,capex=146.273,da=142.507,sbc=125.003)
N24=dict(revenue=4474.342,ebit=1077.913,net=975.703,cfo=948.581,capex=108.869,da=133.192,sbc=101.039)
for base,cur,prev,label in [(H[1],N25,N24,'TTM2025Q3'),(H[2],N26,N25,'TTM2026Q3')]:H.append(dict(period=label,**{k:base[k]+cur[k]-prev[k] for k in cur}))
for h in H:h.update(fcf=h['cfo']-h['capex'],margin=h['ebit']/h['revenue'])
CASES={
'bear':dict(growth=[.04,.04,.04,.035,.03],margins=[.25,.25,.25,.25,.25],tm=.24,tax=.20,wacc=.105,g=.02,roic=.14,capex=.05,da=.025,nwc=.30),
'base':dict(growth=[.10,.09,.08,.07,.06],margins=[.285,.285,.28,.28,.28],tm=.265,tax=.18,wacc=.095,g=.025,roic=.18,capex=.045,da=.025,nwc=.25),
'bull':dict(growth=[.14,.12,.11,.10,.09],margins=[.30,.30,.30,.30,.30],tm=.29,tax=.17,wacc=.085,g=.03,roic=.22,capex=.04,da=.025,nwc=.22)}
def model(c):
 revenue=REV; rows=[]
 for i in range(1,11):
  a=max(0,(i-5)/5)
  growth=c['growth'][i-1] if i<=5 else c['growth'][-1]*(1-a)+c['g']*a
  margin=c['margins'][i-1] if i<=5 else c['margins'][-1]*(1-a)+c['tm']*a
  old=revenue;revenue*=1+growth;ebit=revenue*margin;nopat=ebit*(1-c['tax']);da=revenue*c['da'];dnwc=(revenue-old)*c['nwc']
  capex=revenue*c['capex'];reinv=capex-da+dnwc
  # Transition total net investment gradually to sustainable NOPAT*g/ROIC.
  if i>5:
   reinv=reinv*(1-a)+(nopat*growth/c['roic'])*a
   capex=reinv+da-dnwc
  fcff=nopat-reinv;pv=fcff/(1+c['wacc'])**i
  rows.append(dict(year=i,revenue=revenue,growth=growth,margin=margin,ebit=ebit,nopat=nopat,da=da,capex=capex,dnwc=dnwc,reinvestment=reinv,fcff=fcff,pv=pv))
 terminal_nopat=rows[-1]['nopat']*(1+c['g']);terminal_reinvestment=terminal_nopat*c['g']/c['roic'];terminal_fcff=terminal_nopat-terminal_reinvestment
 tv=terminal_fcff/(c['wacc']-c['g']);pvtv=tv/(1+c['wacc'])**10;ev=sum(x['pv'] for x in rows)+pvtv;price=(ev+BRIDGE)/SHARES
 return dict(price=price,ev=ev,bridge=BRIDGE,terminal_weight=pvtv/ev,terminal_fcff=terminal_fcff,terminal_reinvestment=terminal_reinvestment,rows=rows,upside=price/PRICE-1,mos=1-PRICE/price)
def solve_growth(margin,wacc):
 lo,hi=-.02,.40
 for _ in range(100):
  mid=(lo+hi)/2;c=dict(CASES['base'],growth=[mid]*5,margins=[margin]*5,tm=margin,wacc=wacc)
  if model(c)['price']<PRICE:lo=mid
  else:hi=mid
 return (lo+hi)/2
R={'price':PRICE,'price_at':'2026-11-06T16:00:00-05:00','shares':SHARES,'history':H,'cases':{k:model(c) for k,c in CASES.items()},'inputs':CASES,'sensitivity':[dict(wacc=w,g=g,value=model(dict(CASES['base'],wacc=w,g=g))['price']) for w in [.085,.095,.105] for g in [.02,.025,.03]],'inverse':[dict(margin=m,wacc=w,constant_growth_first5=solve_growth(m,w)) for m,w in [(.265,.095),(.29,.095),(.265,.085)]], 'bridge_sensitivity_per_100m':100/SHARES}
R['checks']={'ten_years':all(len(v['rows'])==10 for v in R['cases'].values()),'wacc_gt_g':all(c['wacc']>c['g'] for c in CASES.values()),'fcff_identity':all(abs(r['fcff']-(r['nopat']+r['da']-r['capex']-r['dnwc']))<1e-8 for v in R['cases'].values() for r in v['rows']), 'ttm_revenue':abs(H[-1]['revenue']-REV)<1e-6}
(P/'calculations.json').write_text(json.dumps(R,indent=2))
with (P/'history.csv').open('w') as f:w=csv.DictWriter(f,fieldnames=list(H[0]));w.writeheader();w.writerows(H)
print(json.dumps({k:{x:v[x] for x in ['price','upside','mos','terminal_weight']} for k,v in R['cases'].items()},indent=2));print(R['inverse']); print(H[-2:]);print(R['sensitivity'])
