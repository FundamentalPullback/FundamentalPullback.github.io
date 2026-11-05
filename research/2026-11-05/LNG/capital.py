from pathlib import Path
import json
from datetime import datetime,timezone
from scipy.stats import linregress,t
import numpy as np
P=Path(__file__).parent;d={}
for sym in ['LNG','CQP','SPY']:
 j=json.loads((P/'sources'/(sym+'_monthly.json')).read_text())['chart']['result'][0]
 d[sym]={datetime.fromtimestamp(x,timezone.utc).strftime('%Y-%m'):y for x,y in zip(j['timestamp'],j['indicators']['adjclose'][0]['adjclose']) if y is not None and datetime.fromtimestamp(x,timezone.utc).strftime('%Y-%m-%d')<'2026-11-01'}
out={}
for sym in ['LNG','CQP']:
 m=sorted(set(d[sym])&set(d['SPY']));y=np.array([d[sym][x]for x in m]);x=np.array([d['SPY'][z]for z in m]);y=y[1:]/y[:-1]-1;x=x[1:]/x[:-1]-1;r=linregress(x,y);ci=t.ppf(.975,len(x)-2)*r.stderr
 out[sym]=dict(beta=r.slope,normalized_beta=(2*r.slope+1)/3,se=r.stderr,ci95=[r.slope-ci,r.slope+ci],r_squared=r.rvalue**2,n=len(x),first=m[1],last=m[-1])
shares=204.203914+.6;price=292.02;cqp_price=56.68;outside_units=(484057704-239872502)/1e6;nci=outside_units*cqp_price;E=shares*price+nci;D=24138+1385;beta=(out['LNG']['normalized_beta']*shares*price+out['CQP']['normalized_beta']*nci)/E;rf=.049;erp=.0441;ke=rf+beta*erp;kd=.058;tax=.18;dw=D/(D+E);wacc=ke*(1-dw)+kd*(1-tax)*dw
out['capital']=dict(shares_proxy_m=shares,price=price,cqp_price=cqp_price,cqp_outside_units_m=outside_units,nci_market_equity=nci,parent_market_equity=shares*price,total_market_equity=E,nominal_debt=24138,finance_leases=1385,total_financial_debt=D,consolidated_equity_beta=beta,risk_free=rf,equity_risk_premium=erp,cost_equity=ke,cost_debt=kd,taxshield_rate=tax,debt_weight=dw,wacc=wacc)
(P/'capital.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
