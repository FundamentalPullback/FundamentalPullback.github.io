"""Independent reconstruction from Yahoo raw bars, without importing technical review engine."""
from pathlib import Path
import json,datetime,math
P=Path(__file__).resolve().parent
x=json.loads((P/'sources/yahoo_chart.json').read_text())['chart']['result'][0];q=x['indicators']['quote'][0]
rows=[]
for i,t in enumerate(x['timestamp']):
 date=datetime.datetime.fromtimestamp(t,datetime.timezone.utc).date().isoformat()
 if date>'2026-11-04' or any(q[k][i] is None for k in ['close','high','low','volume']):continue
 rows.append(dict(date=date,**{k:q[k][i] for k in ['close','high','low','volume']}))
cl=[r['close'] for r in rows]
def ema(n):
 e=cl[0];out=[]
 for c in cl:e+=(c-e)*2/(n+1);out.append(e)
 return out
def smooth(v,n=14):
 e=sum(v[:n])/n
 for z in v[n:]:e=(e*(n-1)+z)/n
 return e
tr=[r['high']-r['low'] if i==0 else max(r['high']-r['low'],abs(r['high']-cl[i-1]),abs(r['low']-cl[i-1])) for i,r in enumerate(rows)]
chg=[cl[i]-cl[i-1] for i in range(1,len(cl))];up=smooth([max(z,0) for z in chg]);dn=smooth([max(-z,0) for z in chg]);e200=ema(200);high=max(r['high'] for r in rows[-252:])
o={'source':'Yahoo raw chart independently recomputed, not importing parent engine','date':rows[-1]['date'],'close':cl[-1],'ema20':ema(20)[-1],'ema50':ema(50)[-1],'ema200':e200[-1],'ema200_change20':e200[-1]/e200[-21]-1,'volume20':sum(r['volume'] for r in rows[-20:])/20,'high252':high,'pullback':1-cl[-1]/high,'atr14':smooth(tr),'rsi14':100-100/(1+up/dn)}
expected=json.loads((P/'technical_independent_check.json').read_text());checks={k:abs(o[k]-v)<1e-8 for k,v in expected.items() if isinstance(v,(int,float))};print(json.dumps({'computed':o,'matches_saved':checks},indent=2));assert all(checks.values())
