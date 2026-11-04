#!/usr/bin/env python3
import json,math,sys
from pathlib import Path
P=Path(__file__).resolve().parent
sys.path.insert(0,str(P/'model'));from model import calc
h=json.loads((P/'history/summary.json').read_text());m=json.loads((P/'model/results.json').read_text());peers=json.loads((P/'comps/comps.json').read_text())
price=344.28;shares=104.7;ev=price*shares+1450-2663.1
cboe={'ticker':'CBOE','price':price,'price_date':'2026-11-03','balance_date':'2026-09-30','shares_diluted_proxy':shares,'ev':ev,'net_revenue':h['ttm']['net_revenue'],'gaap_ebit':h['ttm']['ebit'],'normalized_ebit':h['ttm']['normalized_ebit_conservative'],'ev_gaap_ebit':ev/h['ttm']['ebit'],'ev_normalized_ebit':ev/h['ttm']['normalized_ebit_conservative'],'ev_net_revenue':ev/h['ttm']['net_revenue'],'pe_quarterly_reported_eps':price/h['ttm']['eps_diluted_quarterly_sum'],'scope':'Screen uses face debt and all corporate cash excluding Canada/matched compensation; no DCF reserve, historical tax or October adjustments. Strategic investments remain in EV; historical earnings include disposal/investment gains.'}
checks=[]
def check(name,ok):checks.append({'name':name,'pass':bool(ok)})
for n,r in m['results'].items():
 c=r['assumptions'];check(n+' recomputed',math.isclose(calc(n)['value'],r['value'],abs_tol=1e-9));check(n+' ten years',len(r['rows'])==10);check(n+' wacc g',c['wacc']>c['g']);check(n+' terminal funded',math.isclose(r['terminal_fcff'],r['next_nopat']*(1-c['g']/c['roic'])));check(n+' equity bridge',math.isclose(r['equity'],r['ev']+r['bridge']));check(n+' share price',math.isclose(r['value']*c['shares'],r['equity']));check(n+' EV sum',math.isclose(r['ev'],r['pv_stub']+sum(x['pv'] for x in r['rows'])+r['pv_terminal']))
 for row in r['rows']:
  y=row['year'];check(f'{n} {y} FCFF',math.isclose(row['fcff'],row['nopat']+row['da']-row['capex']-row['working_capital_investment']-row['regulatory_retention']-row['other_economic_investment'],abs_tol=1e-8));check(f'{n} {y} funded margin uplift',row['total_net_investment']+1e-9>=row['growth_net_investment']);check(f'{n} {y} capex floor',row['total_net_investment']+1e-9>=row['physical_net_investment']);check(f'{n} {y} discount',math.isclose(row['pv'],row['fcff']/(1+c['wacc'])**row['discount_years']))
 # Independent finite tail plus reduced infinite tail, measured at end2036.
 explicit=sum(r['terminal_fcff']*(1+c['g'])**(k-1)/(1+c['wacc'])**k for k in range(1,16));after=r['terminal_fcff']*(1+c['g'])**15*(1-c['license_haircut'])/(c['wacc']-c['g'])/(1+c['wacc'])**15
 check(n+' license split independent',math.isclose(explicit+after,r['terminal_value'],rel_tol=1e-12))
 end=r['rows'][-1];revnext=end['net_revenue']*(1+c['g']);physical=revnext*(c['capex_ratio']-.03)+(revnext-end['net_revenue'])*(.03+.06);check(n+' terminal investment physical floor',r['terminal_reinvestment']>=physical)
for x in m['inverse']:check('inverse '+x['kind'],abs(x['value']-price)<1e-6)
check('clearing removed',math.isclose(h['ttm']['cfo']-h['ttm']['clearing_customer_cash_flow'],h['ttm']['cfo_ex_clearing']));check('capital bridge 247',math.isclose(m['results']['base']['bridge'],247));check('scenario order',m['results']['bear']['value']<m['results']['base']['value']<m['results']['bull']['value']);check('regular vs scanner separate',price!=335.53)
for x in peers['rows']:check(x['ticker']+' EV EBIT',math.isclose(x['ev_gaap_ebit_x'],x['ev_diluted_proxy_ex_restricted_cash_m']/x['ttm_gaap_ebit_m'],rel_tol=1e-8))
out={'cboe':cboe,'checks':checks,'passed':sum(x['pass'] for x in checks),'total':len(checks)}
(P/'valuation_checks.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'passed':out['passed'],'total':out['total'],'cboe':cboe},indent=2));assert all(x['pass'] for x in checks)
