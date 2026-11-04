from pathlib import Path
import json
P=Path(__file__).parent;I=json.loads((P/'inputs.json').read_text());rows=[]
for t,d in I['inputs'].items():
 v={k:(a[0]+a[1]-a[2])/1000 for k,a in d.items() if isinstance(a,list)}
 cash=(d['cash']+d['short_investments'])/1000;debt=d['principal_debt']/1000+(15.147 if t=='LRCX' else 0);mc=d['shares_m']*d['price'];ev=mc+debt-cash;fcf=v['cfo']-v['capex'];owner=fcf-v['sbc'];rows.append({'ticker':t,'currency':'USD','price':d['price'],'shares':d['shares_m'],'sales':v['sales'],'ebit':v['ebit'],'margin':v['ebit']/v['sales'],'cfo':v['cfo'],'capex':v['capex'],'sbc':v['sbc'],'cash':cash,'debt':debt,'marketCap':mc,'ev':ev,'evSales':ev/v['sales'],'evEbit':ev/v['ebit'],'reportedFcf':fcf,'ownerFcfProxy':owner,'ownerYield':owner/mc,'extraLease50EvEbit':(ev+50)/v['ebit']})
a=I['ASML'];h={k:sum(r[k] for r in a['series'].values()) for k in ['sales','ebit','cfo','capex','sbc','working_capital_change']};mc=a['priceUSD']/a['eurusd']*a['sharesProxy'];ev=mc+a['debtProxy']-a['cash']-a['shortInvestments'];owner=h['cfo']-h['capex']-h['sbc'];rows.append({'ticker':'ASML','currency':'EUR','priceUSD':a['priceUSD'],'fx':a['eurusd'],'shares':a['sharesProxy'],'marketCap':mc,'ev':ev,'sales':h['sales'],'ebit':h['ebit'],'margin':h['ebit']/h['sales'],'cfo':h['cfo'],'capex':h['capex'],'sbc':h['sbc'],'evSales':ev/h['sales'],'evEbit':ev/h['ebit'],'ownerFcfProxy':owner,'ownerYield':owner/mc,'ownerBeforeAggregateWc':owner-h['working_capital_change'],'ownerYieldBeforeAggregateWc':(owner-h['working_capital_change'])/mc})
assert abs(rows[0]['ebit']-6185.273)<1e-6;assert abs(rows[1]['ebit']-9654.434)<1e-6;assert abs(h['ebit']-15217.8)<1e-6
(P/'results.json').write_text(json.dumps({'rows':rows,'limits':I['limits'],'checksPassed':3},indent=2)+'\n');print('3 peer checks PASS')
