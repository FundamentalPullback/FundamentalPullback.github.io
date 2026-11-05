from pathlib import Path
import csv,json,math,datetime,hashlib
P=Path(__file__).resolve().parent;SRC=P/'inputs/prior_prices.csv'
rows=[]
for r in csv.DictReader(SRC.open()):
 rows.append({k:(v if k=='date' else float(v) if v else None) for k,v in r.items()})
assert rows[-1]['date']=='2026-11-03'
rows.append({'date':'2026-11-04','open':17.49,'high':17.74,'low':17.39,'close':17.46,'volume':3595789,'factor':1.0,'adj_open':17.49,'adj_high':17.74,'adj_low':17.39,'adj_close':17.46})
def ema(a,n):
 out=[];e=a[0]
 for x in a:
  e=x*2/(n+1)+e*(1-2/(n+1));out.append(e)
 return out
def wilder(a,n=14):
 out=[None]*len(a)
 if len(a)>=n:
  v=sum(a[:n])/n;out[n-1]=v
  for i in range(n,len(a)):v=(v*(n-1)+a[i])/n;out[i]=v
 return out
series={}
for name,c,h,l in [('raw','close','high','low'),('dividend_adjusted','adj_close','adj_high','adj_low')]:
 closes=[r[c] for r in rows];highs=[r[h] for r in rows];lows=[r[l] for r in rows]
 e20,e50,e200=[ema(closes,n) for n in [20,50,200]]
 tr=[highs[0]-lows[0]]+[max(highs[i]-lows[i],abs(highs[i]-closes[i-1]),abs(lows[i]-closes[i-1])) for i in range(1,len(rows))]
 atr=wilder(tr);g=wilder([max(0,closes[i]-closes[i-1]) for i in range(1,len(rows))]);loss=wilder([max(0,closes[i-1]-closes[i]) for i in range(1,len(rows))])
 rsi=100 if loss[-1]==0 else 100-100/(1+g[-1]/loss[-1])
 series[name]={'EMA20':e20[-1],'EMA50':e50[-1],'EMA200':e200[-1],'EMA200_20session_change_pct':(e200[-1]/e200[-21]-1)*100,'EMA50_above_EMA200':e50[-1]>e200[-1],'close_above_EMA50':closes[-1]>e50[-1],'EMA20_above_EMA50':e20[-1]>e50[-1],'ATR14':atr[-1],'RSI14':rsi,'high252':max(highs[-252:]),'pullback252_pct':(closes[-1]/max(highs[-252:])-1)*100}
piv=[]
for i in range(len(rows)-95,len(rows)-2):
 if rows[i]['high']==max(r['high'] for r in rows[i-2:i+3]):piv.append({'type':'high','date':rows[i]['date'],'price':rows[i]['high']})
 if rows[i]['low']==min(r['low'] for r in rows[i-2:i+3]):piv.append({'type':'low','date':rows[i]['date'],'price':rows[i]['low']})
tech={'asof_utc':'2026-11-05T02:03:27Z','price_date':'2026-11-04','price':17.46,'price_revision':{'previously_captured_close':17.45,'verified_current_source_close':17.46,'verified_at_utc':'2026-11-05T01:57:00Z','source':'https://stockanalysis.com/stocks/bz/history/'},'source_history':'inputs/prior_prices.csv','source_history_sha256':hashlib.sha256(SRC.read_bytes()).hexdigest(),'appended_bar_source':'https://stockanalysis.com/stocks/bz/history/','series_method':'Archived Yahoo full series throughNov3 plus current StockAnalysis November4 bar; not a wholly independent refreshed series. Prior Nov3 volumes differ by provider; price matched.','fresh_yahoo_attempt':'Original attempt HTTP429. Independent audit refresh succeeded; November4 quote close remains null, while metadata confirms17.46. Archived prices match1253 overlapping completed sessions; November3 volume differs. No fabricated complete second history.','rows':len(rows),'last_bar':rows[-1],'series':series,'avg_volume20':sum(r['volume'] for r in rows[-20:])/20,'pivots_2sessions_each_side':piv,'approved_entry':False}
(P/'technicals.json').write_text(json.dumps(tech,indent=2))
m=json.load(open(P/'prior_model/model.json'));base=m['scenarios']['Base'];ads=m['ads'];bridge=base['total_bridge_usd'];flows=[r['fcff_distributable_usd'] for r in base['rows']];tv=base['terminal_value_usd']
def npv(rate,fs):return sum(f/(1+rate)**i for i,f in enumerate(fs))
def irr(fs):
 lo,hi=-.9,1
 for i in range(200):
  mid=(lo+hi)/2
  if npv(mid,fs)>0:lo=mid
  else:hi=mid
 return (lo+hi)/2
def full_irr(price,delay,yld,fx=.01):
 fs=[-price*ads]+flows.copy();fs[-1]+=tv
 if delay==0:fs[0]+=bridge
 else:
  for year in range(1,delay+1):fs[year]+=bridge*(1-fx)**(year-1)*yld
  fs[delay]+=bridge*(1-fx)**delay
 return irr(fs)
old=json.load(open(P/'inputs/prior_audit_BZ.json'));test=full_irr(17.12,10,.02)
assert abs(test-old['bridge_timing_irrs']['delay10_yield0.02_fxloss0.01'])<1e-10
p=17.46
results={'source_model':'prior_A174; unchanged operating forecast and capital bridge, no new valuation certified','price':p,'price_date':'2026-11-04','base_value':base['value_per_ads'],'base_distance_pct':(base['value_per_ads']/p-1)*100,'ads_m':ads,'bridge_usd_m':bridge,'bridge_per_ads':bridge/ads,'bridge_fraction_market':bridge/(p*ads),'operating_fcff_usd_m':flows,'fixed_terminal_usd_m':tv,'return_scenarios':[],'price_sensitivity':[],'interest_paid_annually_principal_at_distribution_year':True,'source_reproduction_irr_diff':test-old['bridge_timing_irrs']['delay10_yield0.02_fxloss0.01']}
for delay in [0,3,10]:
 for yld in ([0] if delay==0 else[.02,.04]):results['return_scenarios'].append({'existing_asset_distribution_year':delay,'annual_asset_return_paid_out':yld,'annual_fx_erosion_assumption':.01,'shareholder_irr':full_irr(p,delay,yld),'is_announced_policy':False})
for pp in [15.5,16,16.5,17,17.46]:results['price_sensitivity'].append({'price':pp,'irr_asset_retained10years_return2pct':full_irr(pp,10,.02),'irr_asset_retained10years_return4pct':full_irr(pp,10,.04),'not_buy_ceiling':True})
(P/'return_update.json').write_text(json.dumps(results,indent=2))
print('TECH',json.dumps(series));print('RETURNS',json.dumps(results['return_scenarios']));print('PIVOTS',json.dumps(piv[-15:]));print('SENS',json.dumps(results['price_sensitivity']))
