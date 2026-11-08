import pathlib,json,csv
P=pathlib.Path(__file__).parent;a=list(csv.DictReader((P/'daily_closes.csv').open()));ema={}
for n in [20,50,200]:
 e=float(a[0]['close'])
 for r in a[1:]:e+=2/(n+1)*(float(r['close'])-e)
 ema[n]=e
vol=sum(float(x['volume']) for x in list(csv.DictReader((P/'volume_screen_input.csv').open())))/20
high=max(float(r['high']) for r in a[-252:])
h=json.loads((P/'history.json').read_text())['TTM2026']
r={'date':'2026-11-06','regular_close':42.21,'issuer_quote_verified':True,'market_cap':42.21*1139.714310,'price_gate':True,'cap_gate':True,'volume20':vol,'ema':ema,'high252':high,'pullback':1-42.21/high,'trend_gate':42.21>ema[50] and ema[20]>ema[50],'ttm_parent_net_margin':h['net_parent']/h['revenue'],'ttm_ebit_proxy_margin':h['ebit_proxy']/h['revenue'],'ttm_eps_sum_quarters':.90+.19+2.03+.88,'eps_source':'Quarterly supplemental table; not annual EPS difference across changing shares','approved_entry':None,'warning':'Reported TTM is mixed pre/post Coterra, not current combined run rate. EBIT proxy retains nonoperating gains other than financing.'}
(P/'screen_results.json').write_text(json.dumps(r,indent=2));print(r)
