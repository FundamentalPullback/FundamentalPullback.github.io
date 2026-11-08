import json,pathlib,csv
P=pathlib.Path(__file__).parent;a=list(csv.DictReader((P/'daily_closes.csv').open()));h=json.loads((P/'history.json').read_text())['TTM2026'];r=json.loads((P/'model_results.json').read_text())
emas={}
for n in [20,50,200]:
 e=float(a[0]['close'])
 for x in a[1:]:e+=2/(n+1)*(float(x['close'])-e)
 emas[n]=e
price=21.57;high=max(float(x['high']) for x in a[-252:]);vol=sum(float(x['volume']) for x in list(csv.DictReader((P/'volume_screen_input.csv').open())))/20
ans={'date':'2026-11-06','price':price,'price_provenance':'two secondary historical feeds, regular session 16:00 EST; not issuer primary quote','price_gate':price>=15,'market_cap':r['market_cap'],'market_cap_gate':r['market_cap']>=2000,'ebit_margin_ttm':h['ebit']/h['rev'],'net_margin_ttm':h['ni']/h['rev'],'volume20':vol,'high252':high,'pullback':1-price/high,'ema':emas,'pullback_gate':.08<=1-price/high<=.5,'trend_intermediate_gate':price>emas[50] and emas[20]>emas[50],'approved_entry':None,'scope':'Fundamental research continues despite technical pullback failure'}
(P/'screen_results.json').write_text(json.dumps(ans,indent=2));print(ans)
