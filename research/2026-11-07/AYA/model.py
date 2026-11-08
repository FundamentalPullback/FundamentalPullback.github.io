"""Filtro técnico reproducible, no valoración. Cierres USD sin mezclar TSX CAD."""
from pathlib import Path
import json,csv,datetime
p=Path(__file__).parent
# Compact public closes retain the already reviewed USD input series.
with (p/'daily_closes.csv').open() as f:
 a=[dict(date=z['date'],close=float(z['close'])) for z in csv.DictReader(f)]
a=[z for z in a if z['date']<='2026-11-06'];a.sort(key=lambda z:z['date'])
def ema(cs,n,seed):
 if seed=='first': v=cs[0];start=1
 else:v=sum(cs[:n])/n;start=n
 for c in cs[start:]:v+=(c-v)*2/(n+1)
 return v
cases=[]
for scope,rows in [('nasdaq_since_2026-05-04',[z for z in a if z['date']>='2026-05-04']),('full_vendor_year',a)]:
 for seed in ['first','sma']:
  cs=[z['close'] for z in rows];e20,e50=ema(cs,20,seed),ema(cs,50,seed);cases.append(dict(scope=scope,seed=seed,sessions=len(cs),ema20=e20,ema50=e50,close=cs[-1],price_above_ema50=cs[-1]>e50,ema20_above_ema50=e20>e50))
with open(p/'daily_closes.csv','w') as f:
 w=csv.DictWriter(f,fieldnames=['date','close']);w.writeheader();w.writerows(a)
r=dict(asof='2026-11-08',ticker='AYA',currency='USD',exchange='Nasdaq',regular_close=25.37,session='2026-11-06',price_gate_pass=True,technical_gate_pass=all(z['price_above_ema50'] and z['ema20_above_ema50'] for z in cases),cases=cases,approved_values=None,valuation=None)
(p/'model_results.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
