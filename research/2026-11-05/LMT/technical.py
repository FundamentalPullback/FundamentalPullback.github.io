from pathlib import Path
import json,csv,datetime
import pandas as pd
from io import StringIO
P=Path(__file__).parent;S=P/'sources';j=json.load(open(S/'LMT_daily.json'))['chart']['result'][0];q=j['indicators']['quote'][0]
a={datetime.datetime.fromtimestamp(t,datetime.timezone.utc).strftime('%Y-%m-%d'):{k:round(v[i],4) if v[i] is not None else None for k,v in q.items()} for i,t in enumerate(j['timestamp']) if q['close'][i] is not None}
t=pd.DataFrame(json.loads((P/'model/recent_price_rows.json').read_text()));overlap=[]
for _,r in t.iterrows():
 d=pd.to_datetime(r['Date']).strftime('%Y-%m-%d');v={k:float(r[k.title()])for k in ['open','high','low','close','volume']}
 if d in a:overlap.append(dict(date=d,max_ohlc_difference=max(abs(a[d][k]-v[k])for k in ['open','high','low','close'])))
 a[d]=v
rows=[dict(date=d,**a[d]) for d in sorted(a) if d<='2026-11-04']
assert max(x['max_ohlc_difference']for x in overlap)<.011
es={n:rows[0]['close'] for n in [20,50,200]};tr=[];atrs=[];gain=loss=0
for i,r in enumerate(rows):
 for n in es:es[n]=r['close']*2/(n+1)+es[n]*(1-2/(n+1));r['ema'+str(n)]=es[n]
 prev=rows[i-1]['close']if i else r['close'];tv=max(r['high']-r['low'],abs(r['high']-prev),abs(r['low']-prev));tr.append(tv)
 if i==13:atr=sum(tr)/14
 elif i>13:atr=(atr*13+tv)/14
 else:atr=None
 r['atr14']=atr
 if i:
  ch=r['close']-prev
  if i<=14:gain+=max(ch,0)/14;loss+=max(-ch,0)/14
  else:gain=(gain*13+max(ch,0))/14;loss=(loss*13+max(-ch,0))/14
 r['rsi14']=100-100/(1+gain/loss) if i>=14 and loss else None
last=rows[-1];h=max(x['high']for x in rows[-252:]);v20=sum(x['volume']for x in rows[-20:])/20
out=dict(date=last['date'],close=last['close'],high_252=h,pullback_pct=100*(last['close']/h-1),volume_20=v20,ema20=last['ema20'],ema50=last['ema50'],ema200=last['ema200'],ema200_20_sessions_ago=rows[-21]['ema200'],ema200_slope_20_pct=100*(last['ema200']/rows[-21]['ema200']-1),atr14=last['atr14'],rsi14=last['rsi14'],day_change_pct=100*(last['close']/rows[-2]['close']-1),day_volume_ratio=last['volume']/v20,history_sessions=len(rows),overlap_rows=len(overlap),max_overlap_ohlc_difference=max(x['max_ohlc_difference']for x in overlap),method='Split-adjusted, not dividend-total-return OHLC. Yahoo older daily rows; replace 50 recent rows with StockAnalysis same-price-basis history, all 49 overlaps agree within $0.01. EMA recursively seeded at first close with >500 observations; Wilder ATR and RSI.',long_trend_supportive=True,technical_entry_approved=False,source_latest='https://stockanalysis.com/stocks/lmt/history/')
(P/'technical.json').write_text(json.dumps(out,indent=2));(P/'model/technical_overlap.json').write_text(json.dumps(overlap,indent=2))
with(P/'model/ohlcv_indicators.csv').open('w')as f:w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
print(json.dumps(out,indent=2))
