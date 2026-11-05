import json,csv,datetime,math,sys
from pathlib import Path
O=Path(__file__).parent; P=Path(sys.argv[1]) if len(sys.argv)>1 else O/'model_snapshot'
j=json.loads((P/'sources/CTSH_daily.json').read_text())['chart']['result'][0]; q=j['indicators']['quote'][0]
price={datetime.datetime.fromtimestamp(t,datetime.timezone.utc).strftime('%Y-%m-%d'):{k:v[i] for k,v in q.items()} for i,t in enumerate(j['timestamp']) if q['close'][i] is not None}
recent=json.loads((P/'model/price_rows.json').read_text());matches=[]
for r in recent:
 d=datetime.datetime.strptime(r['Date'],'%b %d, %Y').strftime('%Y-%m-%d') if ',' in r['Date'] else r['Date']
 p={k:float(r[k.title()]) for k in ['open','close','high','low','volume']}
 if d in price:matches.append(max(abs(p[k]-price[d][k]) for k in ['open','close','high','low']))
 price[d]=p
rows=[(d,price[d]) for d in sorted(price) if d<='2026-11-04'];close=[r[1]['close'] for r in rows]
def ema(n,end=None):
 x=close if end is None else close[:end];a=2/(n+1)
 return x[0]*(1-a)**(len(x)-1)+sum(a*v*(1-a)**(len(x)-1-i) for i,v in enumerate(x[1:],start=1))
tr=[max(v['high']-v['low'],abs(v['high']-(rows[i-1][1]['close'] if i else v['close'])),abs(v['low']-(rows[i-1][1]['close'] if i else v['close']))) for i,(d,v) in enumerate(rows)]
atr=sum(tr[:14])/14
for v in tr[14:]:atr=(atr*13+v)/14
gains=[max(b-a,0) for a,b in zip(close,close[1:])];losses=[max(a-b,0) for a,b in zip(close,close[1:])]
ga=sum(gains[:14])/14;lo=sum(losses[:14])/14
for a,b in zip(gains[14:],losses[14:]):ga=(ga*13+a)/14;lo=(lo*13+b)/14
calc=dict(close=close[-1],ema20=ema(20),ema50=ema(50),ema200=ema(200),ema200_20_sessions_ago=ema(200,-20),atr14=atr,rsi14=100-100/(1+ga/lo),high_252=max(r[1]['high'] for r in rows[-252:]),volume_20=sum(r[1]['volume'] for r in rows[-20:])/20)
reported=json.loads((P/'technical.json').read_text());out=dict(calculated=calc,errors={k:v-reported[k] for k,v in calc.items()},rows=len(rows),overlap_rows=len(matches),max_source_ohlc_difference=max(matches),status='Independent indicator reproduction; no technical entry authorization')
prior20=sum(r[1]['volume'] for r in rows[-21:-1])/20
out['prior20_volume_excluding_last']=prior20
out['latest_volume_vs_prior20']=rows[-1][1]['volume']/prior20
out['prospective_trigger_review']={'old_Oct30_high':price['2026-10-30']['high'],'Nov2_high':price['2026-11-02']['high'],'latest_Nov4_high':price['2026-11-04']['high'],'proposed_entry_cap':66.50,'finding':'A 66.10 close threshold is below two subsequent rebound highs. It must not be described as a current resistance breakout. A genuine breakout above66.77 does not fit the66.50 cap. Wait for a new structure or explicitly justify a different pullback/recovery setup; do not raise the cap to manufacture compatibility.','technical_entry_approved':False}
out['prospective_trigger_review']['historical_proposal_withdrawn']=True
out['revised_prospective_setup_review']={'type':'Analyst-defined A pullback/stabilization, not statistically validated','low_test':[62.50,64.00],'close_above':64.75,'close_max':65.25,'also_requires':'Close above open and EMA50; volume at least prior20 sessions excluding signal day','last_signal_date':'2026-11-09','last_proposed_DAY_order_date':'2026-11-10','fundamental_cap':66.50,'technical_cap':65.25,'reference_low':61.55,'proposed_manual_stop':61.20,'review':'Coherently specified prospectively; old-high selection concern resolved','current_signal_approved':False,'stage35_approved':False,'order_approved':False}
(O/'technical_audit.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
