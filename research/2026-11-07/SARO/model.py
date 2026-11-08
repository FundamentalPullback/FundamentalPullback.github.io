"""Reconciliación histórica reproducible; no genera valor intrínseco sin inputs defendibles."""
import json
from pathlib import Path
P=Path(__file__).parent
keys=['revenue','ebit','net_income','cfo','ppe_cash','intangible_cash','ppe_disposals','sbc','interest']
def r(a):return dict(zip(keys,a))
a={'2023':r([4563.284,337.358,-35.061,67.893,55.129,30.180,3.508,0,309.645]),'2024':r([5237.161,403.219,10.974,76.330,102.935,20.250,1.812,17.376,282.507]),'2025':r([6062.513,551.069,277.417,316.705,82.408,30.403,5.124,13.237,174.217])}
y={'9M2024':r([3827.548,308.631,25.027,-32.019,70.422,.214,.571,0,235.496]),'9M2025':r([4462.493,401.835,198.776,-6.304,66.733,30,4.341,10.017,132.192]),'9M2026':r([4783.999,472.645,270.007,81.671,67.343,180.595,1.799,15.743,119.933])}
q={'Q42025':{k:a['2025'][k]-y['9M2025'][k] for k in keys},'Q12026':{'revenue':1626.857,'ebit':143.098,'net_income':79.930,'cfo':-119.555,'ppe_cash':15.590,'intangible_cash':0,'ppe_disposals':1.406,'diluted_eps':.24},'Q22026':{'revenue':1599.693,'ebit':168.483,'net_income':97.278,'cfo':72.328,'ppe_cash':21.051,'intangible_cash':.476,'ppe_disposals':-.578,'diluted_eps':.29},'Q32026':{'revenue':1557.449,'ebit':161.064,'net_income':92.799,'cfo':128.898,'ppe_cash':30.702,'intangible_cash':180.119,'ppe_disposals':.971,'diluted_eps':.28}}
q['Q42025']['diluted_eps']=.24
# 0.476 is H1 intangible purchases from released cash-flow reconciliation.
t={}
for name,fy,new,old in [('TTM2025','2024','9M2025','9M2024'),('TTM2026','2025','9M2026','9M2025')]:t[name]={k:a[fy][k]+y[new][k]-y[old][k] for k in keys}
for group in [a,y,q,t]:
 for v in group.values():
  v['fcf_gross_investment']=v['cfo']-v['ppe_cash']-v['intangible_cash']
  v['fcf_after_disposals']=v['fcf_gross_investment']+v['ppe_disposals']
  v['operating_margin']=v['ebit']/v['revenue']
  if v['net_income']>0:v['cfo_to_net_income']=v['cfo']/v['net_income']
  for k in v:v[k]=round(v[k],6)
changes={k:t['TTM2026'][k]/t['TTM2025'][k]-1 for k in ['revenue','ebit','net_income','cfo']}
results={'status':'partial_no_approved_valuation','currency':'USD','units':'millions except EPS','annual':a,'nine_months':y,'last_four_quarters':q,'paired_ttm':t,'ttm_growth':changes,'quote':{'regular_close':27.63,'date':'2026-11-06','scanner_price':27.52,'scanner_session':'unverified'},'valuation':{'adverse':None,'base':None,'favorable':None,'wacc':None,'terminal_growth':None,'entry_price':None},'balance':{'cash':191.329,'gross_debt_including_finance_leases':2499.233,'net_debt_all_cash_deduction_diagnostic':2307.904,'operating_leases':247.099,'q3_diluted_weighted_shares':331.051,'asr_intended_not_executed':350,'shares_outstanding_2026_09_30':328.699971,'shares_outstanding_2026_10_30':328.231433,'restricted_shares_in_september_balance':5.823554,'acquisition_contingent_consideration_fair_value':5.3,'oem_license_180_cash_paid_q3_not_future_obligation':True},'checks':{'q3_fcf_after_disposals_equals_release':abs(q['Q32026']['fcf_after_disposals']+80.952)<1e-6,'9m_fcf_equals_release':abs(y['9M2026']['fcf_after_disposals']+164.468)<1e-6,'four_quarters_revenue_equals_ttm':abs(sum(x['revenue'] for x in q.values())-t['TTM2026']['revenue'])<1e-6}}
results['cash_scope']={'fcf_definition':'CFO menos inversión física e intangibles más disposiciones, antes de adquisiciones netas y otros','9M2026_acquisitions_net_and_other_cash_flow':-33.142,'TTM2026_acquisitions_net_and_other_cash_flow':-33.142,'9M2026_total_investing_cash_flow':-279.281,'TTM2026_total_investing_cash_flow':-294.576,'9M2026_cfo_plus_total_investing':round(y['9M2026']['fcf_after_disposals']-33.142,3),'TTM2026_cfo_plus_total_investing':round(t['TTM2026']['fcf_after_disposals']-33.142,3),'not_normalized_sustainable_fcf':True}
results['checks']['9m_full_investing_bridge']=abs(results['cash_scope']['9M2026_cfo_plus_total_investing']-(-197.610))<1e-6
results['checks']['ttm_full_investing_bridge']=abs(results['cash_scope']['TTM2026_cfo_plus_total_investing']-110.104)<1e-6
assert all(results['checks'].values())
(P/'results.json').write_text(json.dumps(results,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({'ttm':t,'checks':results['checks']},indent=2))
