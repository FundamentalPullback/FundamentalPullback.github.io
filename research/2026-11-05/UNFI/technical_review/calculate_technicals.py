from pathlib import Path
import json,csv,datetime,hashlib,statistics
P=Path(__file__).resolve().parent
D=json.loads((P/'yahoo_chart.json').read_text())['chart']['result'][0];Q=D['indicators']['quote'][0];A=D['indicators']['adjclose'][0]['adjclose'];rows=[];missing=[]
for i,t in enumerate(D['timestamp']):
 date=datetime.datetime.fromtimestamp(t,datetime.timezone.utc).date().isoformat()
 if any(Q[x][i] is None for x in ['open','high','low','close','volume']) or A[i] is None:missing.append(date);continue
 if date>='2026-11-04':continue
 r={'date':date,**{x:Q[x][i] for x in ['open','high','low','close','volume']}};r['factor']=A[i]/r['close']
 r.update({'adj_'+x:r[x]*r['factor'] for x in ['open','high','low','close']});rows.append(r)
assert rows[-1]['date']=='2026-11-03'
r={'date':'2026-11-04','open':46.41,'high':48.44,'low':46.14,'close':48.29,'volume':783406,'factor':1.0}
r.update({'adj_'+x:r[x] for x in ['open','high','low','close']});rows.append(r)
def ema(a,n):
 o=[];e=a[0]
 for x in a:e=x*2/(n+1)+e*(1-2/(n+1));o.append(e)
 return o
def wilder(a,n=14):
 o=[None]*len(a);v=sum(a[:n])/n;o[n-1]=v
 for i in range(n,len(a)):v=(v*(n-1)+a[i])/n;o[i]=v
 return o
series={};daily={}
for name,pre in [('raw',''),('dividend_adjusted','adj_')]:
 cs=[r[pre+'close'] for r in rows];hs=[r[pre+'high'] for r in rows];ls=[r[pre+'low'] for r in rows]
 e20,e50,e200=[ema(cs,n) for n in [20,50,200]]
 tr=[hs[0]-ls[0]]+[max(hs[i]-ls[i],abs(hs[i]-cs[i-1]),abs(ls[i]-cs[i-1])) for i in range(1,len(cs))]
 atr=wilder(tr);g=wilder([max(0,cs[i]-cs[i-1]) for i in range(1,len(cs))]);l=wilder([max(0,cs[i-1]-cs[i]) for i in range(1,len(cs))]);rsi=100-100/(1+g[-1]/l[-1]) if l[-1] else 100
 series[name]={'EMA20':e20[-1],'EMA50':e50[-1],'EMA200':e200[-1],'EMA200_20session_change_pct':100*(e200[-1]/e200[-21]-1),'EMA50_above_EMA200':e50[-1]>e200[-1],'close_above_EMA50':cs[-1]>e50[-1],'EMA20_above_EMA50':e20[-1]>e50[-1],'ATR14':atr[-1],'RSI14':rsi,'high252':max(hs[-252:]),'pullback252_pct':100*(cs[-1]/max(hs[-252:])-1)}
 daily[name]=[dict(date=r['date'],close=cs[i],EMA20=e20[i],EMA50=e50[i],EMA200=e200[i],ATR14=atr[i]) for i,r in enumerate(rows)]
pivots=[]
for i in range(len(rows)-100,len(rows)-2):
 if rows[i]['high']==max(r['high'] for r in rows[i-2:i+3]):pivots.append(dict(type='high',date=rows[i]['date'],price=rows[i]['high']))
 if rows[i]['low']==min(r['low'] for r in rows[i-2:i+3]):pivots.append(dict(type='low',date=rows[i]['date'],price=rows[i]['low']))
out={'ticker':'UNFI','as_of_utc':'2026-11-05T03:19:00Z','regular_close':48.29,'price_date':'2026-11-04','regular_close_source':'https://stockanalysis.com/stocks/unfi/history/','history_source':'https://query1.finance.yahoo.com/v8/finance/chart/UNFI?interval=1d&range=5y&events=div%2Csplits','history_sha256':hashlib.sha256((P/'yahoo_chart.json').read_bytes()).hexdigest(),'method':'Yahoo complete history through November 3 plus final rounded OHLCV from fresh StockAnalysis November 4 historical bar. Both sources and SA historical header confirm regular close48.29. Summary48.32 seen earlier remains archived; not automatically an after-hours explanation. Yahoo volume783300 in bar and783346 metadata differs from SA783406, no volume signal assigned.','rows':len(rows),'omitted_null_rows':missing,'series':series,'avg_volume20':statistics.mean(r['volume'] for r in rows[-20:]),'last_20_bars':rows[-20:],'pivots_2sessions_each_side':pivots,'current_low_is_confirmed_pivot':False,'entryApproved':False,'approved_quantity':0}
(P/'technicals.json').write_text(json.dumps(out,indent=2));(P/'daily_indicators.json').write_text(json.dumps(daily,indent=2))
with (P/'daily_prices.csv').open('w') as f:w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)
print(json.dumps({'series':series,'avg_volume20':out['avg_volume20'],'pivots':pivots[-14:]},indent=2))
