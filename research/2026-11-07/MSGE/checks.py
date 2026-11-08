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
c=dict(price=77.06,price_date='2026-11-06',shares_date='2026-10-30',shares_m=47.426142,market_cap=77.06*47.426142,average_volume20=sum(vol)/20,ema20=ema(20),ema50=ema(50),ema200=ema(200),high252=max(x['high'] for x in a[-252:]),approved_entry=None)
c['pullback']=1-c['price']/c['high252'];c['price_gate']=c['price']>=15;c['market_cap_gate']=c['market_cap']>=2000;c['volume_gate']=c['average_volume20']>=500000;c['ema_gate']=c['price']>c['ema50'] and c['ema20']>c['ema50']
(P/'gate_checks.json').write_text(json.dumps(c,indent=2))
with (P/'daily_closes.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=a[0]);w.writeheader();w.writerows(a)
# LYV reference only: capital claims dated September 30 and equity October 29; no precise current EV asserted.
lyv_rev=25201.406+21564.922-18887.901;lyv_ebit=1251.217+1043.354-1393.873;lyv_da=638.872+541.070-474.080
lyv_eq=235.696543*175.25;lyv_debt=9749.592+77.455;lyv_nci=1146.991+730.534
lyv_cashmax=8257.468-2700 # rounded disclosed client cash, maximum not available cash
comp=dict(date='2026-11-06',definitions='USD million; GAAP TTM September 2026; debt principal; NCI book proxy, not fair value; operating leases remain expense.',LYV=dict(price=175.25,shares_m=235.696543,equity=lyv_eq,revenue=lyv_rev,ebit=lyv_ebit,da=lyv_da,ebit_margin=lyv_ebit/lyv_rev,equity_sales=lyv_eq/lyv_rev,reference_EV_lower=lyv_eq+lyv_debt+lyv_nci-lyv_cashmax,reference_EV_upper=lyv_eq+lyv_debt+lyv_nci,client_cash_excluded_rounded=2700,post_balance_refinancing='October 15 debt refinancing and revolver extension; no exact Nov6 enterprise bridge certified',legal_expense_9m=450),MSGE=dict(price=77.06,equity=c['market_cap'],revenue=1119.656,ebit=180.999,da=55.788,reference_EV=c['market_cap']+571.289-193.653,ebit_margin=180.999/1119.656,equity_sales=c['market_cap']/1119.656))
l=comp['LYV'];l['ev_ebit_range']=[l['reference_EV_lower']/lyv_ebit,l['reference_EV_upper']/lyv_ebit];l['ev_ebit_before450_reference']=[l['reference_EV_lower']/(lyv_ebit+450),l['reference_EV_upper']/(lyv_ebit+450)]
m=comp['MSGE'];m['ev_ebit']=m['reference_EV']/m['ebit'];m['ev_ebitda']=m['reference_EV']/(m['ebit']+m['da'])
(P/'comparables.json').write_text(json.dumps(comp,indent=2));print(json.dumps(c,indent=2));print(json.dumps(comp,indent=2))
