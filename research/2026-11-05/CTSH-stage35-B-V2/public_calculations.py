"""Offline reconstruction of public technical and risk calculations. No account data."""
from pathlib import Path
import csv,json,math
P=Path(__file__).parent
rows=list(csv.DictReader(open(P/'ohlcv_indicators.csv')))
for r in rows:
 for k in r:
  if k!='date':r[k]=float(r[k]) if r[k] else None
es={n:rows[0]['close']for n in [20,50,200]};trs=[];gain=loss=0;checks=[]
for i,r in enumerate(rows):
 for n in es:
  es[n]=r['close']*2/(n+1)+es[n]*(1-2/(n+1));checks.append(abs(es[n]-r['ema'+str(n)])<1e-10)
 prev=rows[i-1]['close']if i else r['close'];tr=max(r['high']-r['low'],abs(r['high']-prev),abs(r['low']-prev));trs.append(tr)
 if i==13:atr=sum(trs)/14
 elif i>13:atr=(atr*13+tr)/14
 if i>=13:checks.append(abs(atr-r['atr14'])<1e-10)
 if i:
  ch=r['close']-prev
  if i<=14:gain+=max(ch,0)/14;loss+=max(-ch,0)/14
  else:gain=(gain*13+max(ch,0))/14;loss=(loss*13+max(-ch,0))/14
 if i>=14 and loss:checks.append(abs(100-100/(1+gain/loss)-r['rsi14'])<1e-10)
j=json.load(open(P/'results.json'));checks.extend([len(rows)==501,rows[-1]['date']=='2026-11-04',sum(x['volume']for x in rows[-20:])/20==j['technical']['volume20_prior_for_Nov5'],j['proposal']['signal_exists'] is False,j['proposal']['current_approved_quantity']==0,j['proposal']['authorized_cap_if_all_conditions_met']==min(j['stage3']['fundamental_cap'],j['proposal']['technical_cap'])])
R=j['risk']['E_worst']-j['risk']['S'];checks.append(abs(R-j['risk']['R_provisional'])<1e-10)
for c in j['risk']['rr_cases']:
 checks.extend([abs(c['reward_to_risk']-(c['level']-j['risk']['E_worst'])/R)<1e-10,abs(c['return_pct']-(c['level']/j['risk']['E_worst']-1)*100)<1e-10])
out={'pass':all(checks),'count':len(checks),'method':'Offline recalculation of technical indicators and scenario arithmetic from derived historical rows. No real-time quote, signal, execution or account approval.'};print(json.dumps(out,indent=2));(P/'public_replay.json').write_text(json.dumps(out,indent=2));assert all(checks)
