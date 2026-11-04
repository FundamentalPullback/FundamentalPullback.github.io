#!/usr/bin/env python3
"""Offline normalization from manually transcribed, source-linked facts. USD millions.
No valuation. Re-run: python build_history.py. Python stdlib only.
"""
import json,csv,pathlib
P=pathlib.Path(__file__).parent
D=json.loads((P/'inputs.json').read_text()); F=D['periods']; O={}
for k,v in F.items():O[k]=dict(v['values'])
def bridge(new,a,b,c):
 O[new]={k:O[a][k]+O[b][k]-O[c][k] for k in O[a].keys()&O[b].keys()&O[c].keys()}
def difference(new,a,b):
 O[new]={k:O[a][k]-O[b][k] for k in O[a].keys()&O[b].keys()}
difference('Q4_2025','FY2025','9M2025');difference('Q2_2026','H1_2026','Q1_2026');difference('Q3_2026','9M2026','H1_2026')
bridge('TTM_20260930','FY2025','9M2026','9M2025');bridge('TTM_20250930','FY2024','9M2025','9M2024')
for k,r in O.items():
 r['ebit_ex_tariff_refund']=r['ebit']-r['tariff_refund_benefit']
 r['gross_profit_ex_tariff_refund']=r['gross_profit']-r['tariff_refund_benefit']
 r['fcf_reported']=r['cfo']-r['capex_cash']
 r['fcf_after_loan_funding']=r['fcf_reported']-r['net_loan_funding']
 r['cash_after_funding_and_expensed_sbc']=r['fcf_after_loan_funding']-r['sbc_expensed']
 r['cash_after_funding_and_equity_sbc']=r['fcf_after_loan_funding']-r['sbc_equity']
 r['non_expensed_sbc_gap']=r['sbc_equity']-r['sbc_expensed']
 r['ebit_margin_revenue_pct']=100*r['ebit']/r['revenue']
 r['recurring_gp_gaap']=r['subscription_revenue']+r['fintech_revenue']-r['subscription_cost']-r['fintech_cost']
 r['ebit_margin_recurring_gp_pct']=100*r['ebit']/r['recurring_gp_gaap']
 r['pretax_ex_interest_and_warrants']=r['pretax']-r['interest_net']-r['warrant_gain']-r['other_income']
 r['cfo_less_net_income']=r['cfo']-r['net_income']
 r['net_contract_cost_cash_drag']=r['contract_cost_cash']-r['contract_cost_amort']
checks=[]
for k,r in O.items():
 for label,ok in [('revenue_components',r['revenue']==r['subscription_revenue']+r['fintech_revenue']+r['hardware_revenue']),('pretax_to_ebit',r['pretax_ex_interest_and_warrants']==r['ebit']),('net_income',r['pretax']-r['tax_expense']==r['net_income']),('cap_sbc_nonnegative',r['non_expensed_sbc_gap']>=0)]:checks.append({'period':k,'check':label,'pass':ok})
checks.append({'period':'TTM_20260930','check':'four_quarters_sum','pass':all(sum(O[q][m] for q in ['Q4_2025','Q1_2026','Q2_2026','Q3_2026'])==O['TTM_20260930'][m] for m in F['9M2026']['values'])})
assert all(c['pass'] for c in checks),checks
(P/'normalized_history.json').write_text(json.dumps(O,indent=2,sort_keys=True)+'\n')
keys=sorted(set().union(*(r.keys() for r in O.values())))
with (P/'normalized_history.csv').open('w') as f:
 w=csv.writer(f);w.writerow(['period']+keys)
 for k in ['FY2023','FY2024','FY2025','Q4_2025','Q1_2026','Q2_2026','Q3_2026','9M2024','9M2025','9M2026','TTM_20250930','TTM_20260930']:w.writerow([k]+[O[k].get(m,'') for m in keys])
(P/'qa.json').write_text(json.dumps({'checks':checks,'passed':len(checks),'failed':0,'limitations':D['limitations']},indent=2)+'\n')
print('PASS',len(checks),'checks')
for k in ['TTM_20250930','TTM_20260930']:
 print(k,{m:O[k][m] for m in ['revenue','ebit','net_income','cfo','fcf_reported','fcf_after_loan_funding','sbc_expensed','sbc_equity','cash_after_funding_and_equity_sbc']})
