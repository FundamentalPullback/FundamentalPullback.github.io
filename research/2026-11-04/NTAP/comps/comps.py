#!/usr/bin/env python3
"""Rebuild peer calculations offline from pinned, source-attributed inputs.
Usage: python comps.py [input_json] [output_dir]
USD and shares in millions except price and multiples. No live-data dependency.
"""
import json,csv,sys
from pathlib import Path
base=Path(__file__).resolve().parent
inp=Path(sys.argv[1]) if len(sys.argv)>1 else base/'comps_inputs.json'
out=Path(sys.argv[2]) if len(sys.argv)>2 else base
out.mkdir(parents=True,exist_ok=True)
d=json.loads(inp.read_text()); rows=[]; details=[]
for p in d['peers']:
 t={k:v['fy']+v['current_ytd']-v['prior_ytd'] for k,v in p['ttm_inputs'].items()}
 norm=t['gaap_ebit']+sum(t[k] for k in p['normalized_addback_metrics'])
 broad=norm+sum(t[k] for k in p['broader_normalization_metrics'])
 equity=p['price']*p['diluted_share_proxy']
 liquid=p['cash']+p['marketable_investments']
 ev=equity+p['financial_debt']+p['other_claims']+p['nci']-liquid
 assert p['price']>0 and p['diluted_share_proxy']>0 and t['revenue']>0
 if p['ticker']=='P':
  assert abs(t['revenue']-4262.150)<1e-6
  assert abs(t['severance'])<1e-6
  assert abs(norm-229.545)<1e-6
 if p['ticker']=='HPE':
  assert abs(broad-(t['management_non_gaap_ebit']-t['sbc']-t['intangible_amortization']))<1e-6
  assert t['impairment']==260 and t['gaap_ebit']==2602
  assert sum(v for k,v in p['diluted_share_proxy_components_m'].items() if k!='total_diluted')==p['diluted_share_proxy']
 if p['ticker']=='NTAP':
  assert t['revenue']==7391 and t['gaap_ebit']==1849 and norm==1838
  assert ev==37186
 row={'ticker':p['ticker'],'issuer':p['issuer'],'price_date':'2026-11-03','price_usd':p['price'],'balance_date':p['balance_date'],'ttm_end':p['ttm_end'],'diluted_share_proxy_m':p['diluted_share_proxy'],'latest_actual_common_shares_m':p['latest_actual_common_shares'],'equity_value_proxy_usdm':equity,'cash_usdm':p['cash'],'marketable_investments_usdm':p['marketable_investments'],'financial_debt_usdm':p['financial_debt'],'nci_usdm':p['nci'],'other_claims_usdm':p['other_claims'],'enterprise_value_proxy_usdm':ev,'ttm_revenue_usdm':t['revenue'],'ttm_gaap_operating_ebit_usdm':t['gaap_ebit'],'ttm_normalized_operating_ebit_usdm':norm,'ttm_broader_normalized_operating_ebit_sensitivity_usdm':broad,'ttm_sbc_retained_usdm':t['sbc'],'gaap_operating_margin_pct':t['gaap_ebit']/t['revenue']*100,'normalized_operating_margin_pct':norm/t['revenue']*100,'latest_quarter_reported_revenue_growth_pct':(p['latest_quarter_revenue']/p['prior_year_quarter_revenue']-1)*100,'ev_revenue_x':ev/t['revenue'],'ev_gaap_operating_ebit_x':ev/t['gaap_ebit'],'ev_normalized_operating_ebit_x':ev/norm,'ev_broader_operating_ebit_sensitivity_x':ev/broad}
 rows.append({k:round(v,6) if isinstance(v,float) else v for k,v in row.items()})
 detail={'ticker':p['ticker'],'ttm_metric_bridge_usdm':t,'primary_normalization_addbacks_usdm':{k:t[k] for k in p['normalized_addback_metrics']},'broader_sensitivity_addbacks_usdm':{k:t[k] for k in p['broader_normalization_metrics']},'price_source_ids':p['price_source_ids'],'limitations':p['limitations'],'post_balance_events':p['post_balance_events']}
 if p['ticker']=='HPE':
  detail['supplemental_sensitivities']={'ev_if_full_160m_telco_gross_consideration_added_to_cash_usdm':ev-160,'ev_normalized_ebit_if_full_telco_gross_proceeds_x':(ev-160)/norm,'normalized_ebit_before_captive_financing_cost_usdm':norm+t['financing_cost'],'ev_before_captive_financing_cost_ebit_x':ev/(norm+t['financing_cost']),'note':'Sensitivities are not primary multiples or estimates of current net cash. No disposed Telco EBIT restatement or financing receivable value adjustment.'}
 details.append(detail)
with (out/'comps.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
(out/'comps.json').write_text(json.dumps({'as_of':d['as_of'],'price_as_of':d['price_as_of'],'units':'USD millions and shares millions except price and multiples','rows':rows,'details':details,'sources':d['sources'],'qa':'PASS: TTM bridges, Everpure rolled-out severance, HPE non-GAAP less retained SBC/amortization, positive denominators.'},indent=2)+'\n')
for r in rows: print(f"{r['ticker']}: EV ${r['enterprise_value_proxy_usdm']:,.3f}m; TTM revenue ${r['ttm_revenue_usdm']:,.3f}m; GAAP EBIT ${r['ttm_gaap_operating_ebit_usdm']:,.3f}m; normalized EBIT ${r['ttm_normalized_operating_ebit_usdm']:,.3f}m; EV/revenue {r['ev_revenue_x']:.2f}x; EV/GAAP EBIT {r['ev_gaap_operating_ebit_x']:.2f}x; EV/normalized EBIT {r['ev_normalized_operating_ebit_x']:.2f}x")
