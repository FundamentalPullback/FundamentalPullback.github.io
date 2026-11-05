from pathlib import Path
import numpy as np,json,csv
from datetime import datetime,timezone
from scipy.stats import linregress,t
P=Path(__file__).parent;data={}
for sym in ['LNG','SPY']:
 j=json.load(open(P/'sources'/(sym+'_monthly.json')))['chart']['result'][0]
 data[sym]={datetime.fromtimestamp(d,timezone.utc).strftime('%Y-%m'):p for d,p in zip(j['timestamp'],j['indicators']['adjclose'][0]['adjclose']) if datetime.fromtimestamp(d,timezone.utc).strftime('%Y-%m-%d')<'2026-11-01' and p is not None}
months=sorted(set(data['LNG'])&set(data['SPY']));fr=np.array([data['LNG'][m]for m in months]);sr=np.array([data['SPY'][m]for m in months]);fr=fr[1:]/fr[:-1]-1;sr=sr[1:]/sr[:-1]-1
r=linregress(sr,fr);width=t.ppf(.975,len(fr)-2)*r.stderr
result=dict(beta=r.slope,beta_standard_error=r.stderr,beta_95pct_low=r.slope-width,beta_95pct_high=r.slope+width,monthly_alpha=r.intercept,r_squared=r.rvalue**2,n=len(fr),first_price_month=months[0],last_price_month=months[-1],method='OLS monthly simple adjusted-close returns LNG on SPY; incomplete November 2026 excluded; market returns not excess returns')
with open(P/'beta_return_series.csv','w')as f:
 w=csv.writer(f);w.writerow(['return_month','LNG_return','SPY_return']);w.writerows(zip(months[1:],fr,sr))
(P/'beta_estimate.json').write_text(json.dumps(result,indent=2));print(result)
