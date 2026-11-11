import json,pathlib
base=pathlib.Path(__file__).resolve().parents[2]
s=json.load(open(base/'2026-11-05/trailing-reconciliation/calculations.json'))['levels']
old=json.load(open(base/'2026-11-09/stage4-review/trailing-calculations.json'))['calculations']
bars={'ASO':[(69.12,65.83,67.27),(71.29,67.47,71.18),(70.61,68.10,70.42)],'ULTA':[(649.70,637.64,644.76),(672.70,649.82,665.13),(666.58,656.16,664.68)],'EXLS':[(43.60,41.88,43.15),(43.70,42.80,43.33),(44.35,42.94,44.31)],'DOCU':[(78.50,75.93,77.61),(78.36,76.70,77.75),(77.94,75.62,77.66)]}
result={'session':'2026-11-10','effective_session':'2026-11-11','provider':'ChartExchange','method':'Continue fixed Nov5 A290 seed using refreshed same-provider Nov6/9/10 bars; preserve Nov10 effective published floor; no retrospective signal changes; do not blend StockAnalysis OHLC','calculations':{}}
for t,rows in bars.items():
 a=s[t];atr=a['atr14_wilder'];hc=a['highest_close_since_entry'];c0=a['close'];trail=a['next_session_raw'];out=[]
 for date,(h,l,c) in zip(['2026-11-06','2026-11-09','2026-11-10'],rows):
  tr=max(h-l,abs(h-c0),abs(l-c0));atr=(13*atr+tr)/14;hc=max(hc,c);candidate=hc-3*atr
  if date=='2026-11-10':trail=max(trail,old[t][-1]['nextTrail'])
  prev=trail;trail=max(trail,candidate);out.append(dict(date=date,high=h,low=l,close=c,true_range=tr,atr14=atr,highest_close=hc,candidate=candidate,previous_floor=prev,next_reference=trail));c0=c
 result['calculations'][t]={'seed':a,'refreshed_bars':out,'published_nov10_reference':old[t][-1]['nextTrail'],'nov11_reference':trail,'nov11_display':round(trail,2),'exit_on_nov10_close':rows[-1][2]<old[t][-1]['nextTrail']}
 print(t,atr,candidate,trail)
json.dump(result,open(pathlib.Path(__file__).with_name('calculations.json'),'w'),indent=2)
