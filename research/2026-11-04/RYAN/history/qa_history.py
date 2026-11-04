from pathlib import Path
import json
p=Path(__file__).resolve().parent;x=json.load(open(p/'periods.json'));k=json.load(open(p/'reported_kpis.json'))['values'];checks=[]
def check(name,a,b,tol=0.00001):
 assert abs(a-b)<tol,(name,a,b);checks.append({'check':name,'actual':a,'expected':b,'pass':True})
for period,v in x.items():
 check(period+' revenue',v['revenue'],v['net_commissions_fees']+v['fiduciary_income'])
 check(period+' income attribution',v['net_income_consolidated'],v['net_income_parent']+v['net_income_nci'])
 check(period+' tax',v['net_income_consolidated'],v['pretax_income']-v['tax_expense'])
 check(period+' normalization',v['ebita_ex_remeasurement_retains_sbc_restructuring'],v['operating_income']+v['amortization']+v['contingent_remeasurement'])
for m in x['TTM Q3 2026']:
 if all(x[q][m] is not None for q in ['TTM Q3 2026','Q4 2025','Q1 2026','Q2 2026','Q3 2026']): check(m+' TTM=sum4Q',x['TTM Q3 2026'][m],sum(x[q][m] for q in ['Q4 2025','Q1 2026','Q2 2026','Q3 2026']))
for metric in ['Adjusted EBITDAC','Adjusted net income']:
 a=k[metric];check(metric+' TTM=sum4Q',a['TTM Q3 2026'],sum(a[q] for q in ['Q4 2025','Q1 2026','Q2 2026','Q3 2026']),tol=0.002)
(p/'qa_result.json').write_text(json.dumps({'status':'PASS','checks_count':len(checks),'checks':checks,'limitations':'Arithmetic/source identities only. Not validation of economic normalization or complete diluted capitalization.'},indent=2));print('PASS',len(checks))
