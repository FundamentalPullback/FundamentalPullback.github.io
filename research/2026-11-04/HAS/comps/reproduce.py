#!/usr/bin/env python3
"""Offline comparables reconstruction. USD millions, shares millions, price USD.
Run python reproduce.py from any directory; no network/packages required.
Input values transcribed from source statements, NOT provider forward estimates.
"""
import json,csv,pathlib
D=pathlib.Path(__file__).parent
inputs={
'MAT':{'fy2025':{'sales':5347.623,'ebit':546.424,'cfo':593.255,'capex':181.992,'sbc':79.719},'ytd2026':{'sales':1987.497,'ebit':-91.808,'cfo':-202.134,'capex':125.809,'sbc':32.907},'ytd2025':{'sales':1845.191,'ebit':25.519,'cfo':-275.268,'capex':76.019,'sbc':38.624},'ttm_end':'2026-06-30','latest_quarter':'Q2 2026','price_date':'2026-11-03','price':15.29,'shares_diluted':288.930,'debt_nominal':2350.0,'cash_unrestricted':523.856,'restricted_cash':None,'tariff_cash_sensitivity':None},
'JAKK':{'fy2025':{'sales':570.671,'ebit':14.218,'cfo':8.492,'capex':9.563,'sbc':10.913},'ytd2026':{'sales':500.136,'ebit':31.657,'cfo':17.430,'capex':13.226,'sbc':9.122},'ytd2025':{'sales':443.557,'ebit':22.823,'cfo':-24.753,'capex':7.850,'sbc':8.132},'ttm_end':'2026-09-30','latest_quarter':'Q3 2026','price_date':'2026-11-03','price':31.65,'shares_diluted':12.051,'debt_nominal':0.0,'cash_unrestricted':43.999,'restricted_cash':1.133,'tariff_cash_sensitivity':11.1}}
results=[]
for ticker,x in inputs.items():
 t={k:round(x['fy2025'][k]+x['ytd2026'][k]-x['ytd2025'][k],6) for k in x['fy2025']}
 mc=x['price']*x['shares_diluted']; ev=mc+x['debt_nominal']-x['cash_unrestricted']; oc=t['cfo']-t['capex']-t['sbc']
 r={'ticker':ticker,'ttm_end':x['ttm_end'],'price_date':x['price_date'],'price':x['price'],'shares_proxy':x['shares_diluted'],'equity_proxy':mc,'debt_nominal':x['debt_nominal'],'cash_unrestricted':x['cash_unrestricted'],'ev_proxy':ev,**{'ttm_'+k:v for k,v in t.items()},'ebit_margin':t['ebit']/t['sales'],'ev_ebit':ev/t['ebit'],'owner_cash':oc,'owner_cash_yield':oc/mc,'owner_cash_ex_gross_refund_sensitivity':None,'owner_cash_yield_ex_gross_refund_sensitivity':None}
 if x['tariff_cash_sensitivity'] is not None:
  r['owner_cash_ex_gross_refund_sensitivity']=oc-x['tariff_cash_sensitivity'];r['owner_cash_yield_ex_gross_refund_sensitivity']=(oc-x['tariff_cash_sensitivity'])/mc
 results.append(r)
(D/'inputs.json').write_text(json.dumps(inputs,indent=2)+'\n');(D/'results.json').write_text(json.dumps(results,indent=2)+'\n')
with (D/'results.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=results[0].keys());w.writeheader();w.writerows(results)
with (D/'bridge.csv').open('w') as f:
 w=csv.writer(f);w.writerow(['ticker','metric','FY2025','YTD2026','YTD2025','TTM','units','period'])
 for ticker,x in inputs.items():
  for k in x['fy2025']:w.writerow([ticker,k,x['fy2025'][k],x['ytd2026'][k],x['ytd2025'][k],round(x['fy2025'][k]+x['ytd2026'][k]-x['ytd2025'][k],6),'USD millions','6M for MAT; 9M for JAKK'])
print(json.dumps(results,indent=2))
