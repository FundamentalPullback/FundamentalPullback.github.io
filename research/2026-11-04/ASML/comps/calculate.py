import json,csv
from pathlib import Path
P=Path(__file__).parent
sources={
'KLAC_FY':'https://ir.kla.com/sec-filings/annual-reports/content/0000319201-26-000027/klac-20260630.htm',
'KLAC_Q1':'https://ir.kla.com/sec-filings/all-sec-filings/content/0000319201-26-000032/exhibit991earningsrelease0.htm',
'KLAC_10Q':'https://ir.kla.com/sec-filings/all-sec-filings/content/0000319201-26-000034/klac-20260930.htm',
'LRCX_FY':'https://investor.lamresearch.com/2026-07-29-Lam-Research-Corporation-Reports-Financial-Results-for-the-Quarter-Ended-June-28%2C-2026',
'LRCX_Q1':'https://investor.lamresearch.com/2026-10-21-Lam-Research-Corporation-Reports-Financial-Results-for-the-Quarter-Ended-September-27%2C-2026',
'LRCX_10Q':'https://www.sec.gov/Archives/edgar/data/707549/000070754926000054/lrcx-20260927.htm',
'KLAC_PRICE':'https://stockanalysis.com/stocks/klac/history/',
'LRCX_PRICE':'https://stockanalysis.com/stocks/lrcx/history/'}
# All statement inputs below USD thousands; shares subsequently expressed in millions.
raw={
'KLAC': {'period':'2026-09-30','fy_end':'2026-06-30','prior_q':'2025-09-30','sales':[13579476,4136015,3209696], 'cogs':[5255060,1577791,1243070], 'rd':[1532118,395096,360461], 'sga':[1131518,301458,268988], 'cfo':[4143079,1530939,1161591], 'capex':[375945,194756,95894], 'sbc':[310171,84073,70182], 'cash':1531950,'short_investments':3209241,'principal_debt':5950000,'carrying_debt':5723289,'shares_m':1302.962435,'shares_date':'2026-10-26','diluted_wavg_m':1311.064,'price':156.20},
'LRCX': {'period':'2026-09-27','fy_end':'2026-06-28','prior_q':'2025-09-28','sales':[23232690,8219418,5324173],'ebit':[8199795,3283727,1829088], 'cfo':[5857657,3497652,1778964], 'capex':[966405,257697,185121], 'sbc':[386381,114696,97241], 'cash':7437384,'short_investments':0,'principal_debt':3750000,'carrying_debt_incl_finance_leases':3735444,'shares_m':1249.171,'shares_date':'2026-10-20','diluted_wavg_m':1255.768,'price':230.72}}
rows=[];results=[]
for ticker,x in raw.items():
 if 'ebit' not in x:x['ebit']=[x['sales'][i]-x['cogs'][i]-x['rd'][i]-x['sga'][i] for i in range(3)]
 r={'ticker':ticker,'currency':'USD','price_date':'2026-11-03','financial_period_end':x['period'],'shares_date':x['shares_date'],'price':x['price'],'shares_m':x['shares_m']}
 for metric in ['sales','ebit','cfo','capex','sbc']:
  v=x[metric];r[metric+'_ttm_m']=(v[0]+v[1]-v[2])/1000
  for period,value,source in zip([x['fy_end']+' FY',x['period']+' Q',x['prior_q']+' Q'],v,[ticker+'_FY',ticker+'_Q1',ticker+'_Q1']):rows.append({'ticker':ticker,'metric':metric,'period':period,'value':value,'units':'USD thousands','source':sources[source]})
 for metric in ['cash','short_investments','principal_debt']:
  r[metric+'_m']=x[metric]/1000;rows.append({'ticker':ticker,'metric':metric,'period':x['period'],'value':x[metric],'units':'USD thousands','source':sources[ticker+'_10Q']})
 for metric,units,period,source in [('shares_m','million shares',x['shares_date'],ticker+'_10Q'),('price','USD per share','2026-11-03',ticker+'_PRICE')]:rows.append({'ticker':ticker,'metric':metric,'period':period,'value':x[metric],'units':units,'source':sources[source]})
 r['market_cap_m']=r['price']*r['shares_m'];r['ev_m']=r['market_cap_m']+r['principal_debt_m']-r['cash_m']-r['short_investments_m'];r['ev_ebit']=r['ev_m']/r['ebit_ttm_m'];r['owner_fcf_m']=r['cfo_ttm_m']-r['capex_ttm_m']-r['sbc_ttm_m'];r['owner_fcf_yield_pct']=r['owner_fcf_m']/r['market_cap_m']*100;r['reported_fcf_yield_pct']=(r['cfo_ttm_m']-r['capex_ttm_m'])/r['market_cap_m']*100;results.append(r)
(P/'inputs.json').write_text(json.dumps({'sources':sources,'series_order':'FY + latest Q - prior-year Q','inputs':raw},indent=2))
(P/'results.json').write_text(json.dumps(results,indent=2))
with (P/'numeric_rows.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
print(json.dumps(results,indent=2))
