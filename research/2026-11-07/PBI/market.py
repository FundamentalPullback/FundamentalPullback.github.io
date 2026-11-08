import pathlib,json,csv
P=pathlib.Path(__file__).parent;a=[x for x in csv.DictReader((P/'daily_closes.csv').open()) if x['date']<='2026-11-06'];e={}
for n in [20,50,200]:
 v=float(a[0]['close'])
 for x in a[1:]:v=float(x['close'])*2/(n+1)+v*(1-2/(n+1))
 e[str(n)]=v
price=float(a[-1]['close']);high=max(float(x['high']) for x in a[-252:]);vol=list(csv.DictReader((P/'volume_screen_input.csv').open()));m=dict(session='2026-11-06 regular close',price=price,cross_price=15.55,ema=e,volume20=sum(float(x['volume']) for x in vol)/20,high252=high,pullback=1-price/high,shares_m=135.554541,shares_date='2026-10-20',cap=price*135.554541,ema_pass=price>e['50'] and e['20']>e['50'],pullback_pass=.08<=1-price/high<=.5)
(P/'market.json').write_text(json.dumps(m,indent=2));print(m)
