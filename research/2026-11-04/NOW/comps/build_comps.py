import json
from pathlib import Path
P=Path(__file__).resolve().parent
x=json.loads((P/'inputs.json').read_text());out={}
for ticker,d in x['companies'].items():
 e=d['ebit_fy']+d['ebit_h1_current']-d['ebit_h1_prior']; a=d['acquired_amort_fy']+d['acquired_amort_h1_current']-d['acquired_amort_h1_prior']
 r=d['revenue_fy']+d['revenue_h1_current']-d['revenue_h1_prior']
 cap=d['price']*d['cover_shares_m'];net=d['debt_principal']+d['finance_lease_liability']-d['cash']-d['marketable'];ev=cap+net
 def row(ev):return dict(ev=ev,ev_ebit_gaap=ev/e,ev_ebit_before_acquired_amort=ev/(e+a))
 out[ticker]={'ttm_revenue':r,'ttm_ebit_gaap':e,'ttm_acquired_amort':a,'ttm_ebit_before_acquired_amort':e+a,'gaap_margin':e/r,'cover_share_marketcap':cap,'july_net_debt_including_finance_leases':net,'july_balance_screen':row(ev),'quarter_diluted_share_sensitivity':row(d['price']*d['q2_diluted_avg_shares_m']+net)}
 if ticker=='WDAY':out[ticker]['october_financing_only_bridge']=row(ev+2500-2470)
 if ticker=='CRM':out[ticker]['gross_acquisition_cash_payment_only_sensitivity_NOT_normalized']=row(ev+1500+3600)
 assert e>0 and a>=0 and d['price_date']=='2026-11-03'
(P/'outputs.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
