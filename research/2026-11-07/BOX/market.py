import pathlib,json,csv,datetime,statistics,math
P=pathlib.Path(__file__).resolve().parent
J=lambda n,o:(P/n).write_text(json.dumps(o,indent=2,ensure_ascii=False)+'\n')
h=json.loads((P/'history.json').read_text());t=h['paired_ttm_july']['2026']
prices=list(csv.DictReader((P/'daily_closes.csv').open()));prices=[r for r in prices if r['date']<='2026-11-06'];cl=[float(r['close']) for r in prices];price=41.95;shares=137.200773;cap=price*shares
def ema(n,ls):
 z=ls[0]
 for v in ls[1:]:z+=(v-z)*2/(n+1)
 return z
es={str(n):ema(n,cl) for n in [20,50,200]};vol=list(csv.DictReader((P/'volume_screen_input.csv').open()));high=max(float(x['high']) for x in prices[-252:]);pull=1-price/high
market=dict(as_of='2026-11-06 16:00 EST',price=price,shares_m=shares,shares_date='2026-07-31',market_cap=cap,ema=es,ema200_20_sessions_ago=ema(200,cl[:-20]),volume20=sum(float(r['volume']) for r in vol)/20,high252=high,pullback=pull,entry_technical_pass=price>es['50'] and es['20']>es['50'] and .08<=pull<=.5,price_source='StockAnalysis; Yahoo crosscheck',source_series_sessions=len(cl))
J('market.json',market)
