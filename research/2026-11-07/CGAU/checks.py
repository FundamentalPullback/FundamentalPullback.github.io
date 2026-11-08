import json,pathlib,datetime,csv
P=pathlib.Path(__file__).parent
with (P/'daily_closes.csv').open() as f:
 a=[dict(date=z['date'],close=float(z['close']),high=float(z['high']),volume=int(z['volume'])) for z in csv.DictReader(f)]
a=[v for v in a if v['date']<='2026-11-06']
def ema(n):
 e=sum(v['close'] for v in a[:n])/n
 for v in a[n:]:e=v['close']*2/(n+1)+e*(1-2/(n+1))
 return e
# Price row volume exact source distinct from Yahoo consolidated close volume.
with (P/'volume_screen_input.csv').open() as f:vol=[int(z['volume']) for z in csv.DictReader(f)]
c=dict(price=21.78,price_date='2026-11-06',shares_date='2026-10-31',shares_m=193.671809,market_cap=21.78*193.671809,average_volume20=sum(vol)/20,ema20=ema(20),ema50=ema(50),ema200=ema(200),high252=max(x['high'] for x in a[-252:]),approved_entry=None)
c['pullback']=1-c['price']/c['high252'];c['price_gate']=c['price']>=15;c['market_cap_gate']=c['market_cap']>=2000;c['volume_gate']=c['average_volume20']>=500000;c['ema_gate']=c['price']>c['ema50'] and c['ema20']>c['ema50']
(P/'gate_checks.json').write_text(json.dumps(c,indent=2))
with (P/'daily_closes.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=a[0]);w.writeheader();w.writerows(a)

print(json.dumps(c,indent=2))
