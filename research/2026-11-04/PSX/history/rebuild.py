#!/usr/bin/env python3
"""Offline rebuild, Python standard library only. USD million except noted.
Inputs contain minimal sourced facts, never full filings. No DCF or price target.
"""
import json,csv
from pathlib import Path
P=Path(__file__).resolve().parent
facts=json.loads((P/'source_facts.json').read_text())
def get(start,end,seg='consolidated'):
 return {r['metric']:r['value'] for r in facts if r['start']==start and r['end']==end and r['segment']==seg}
def diff(a,b):return {k:a[k]-b[k] for k in sorted(a.keys()&b.keys()) if k!='eps_diluted'}
def plus(a,b):return {k:a[k]+b[k] for k in sorted(a.keys()&b.keys()) if k!='eps_diluted'}
def enrich(x):
 if all(k in x for k in ['wc_receivables_increase','wc_inventories_increase','wc_prepaids_increase','wc_payables_increase','wc_tax_other_increase']):
  x['wc_cash_effect']=-x['wc_receivables_increase']-x['wc_inventories_increase']-x['wc_prepaids_increase']+x['wc_payables_increase']+x['wc_tax_other_increase']
  x['cfo_ex_wc']=x['cfo']-x['wc_cash_effect']
 if 'cfo' in x and 'capex_investments' in x:
  x['fcf_cfo_minus_capex']=x['cfo']-x['capex_investments']
  if 'cfo_ex_wc' in x:x['fcf_ex_wc']=x['cfo_ex_wc']-x['capex_investments']
 if 'equity_earnings' in x and 'undistributed_equity_earnings' in x:x['equity_distributions_in_cfo']=x['equity_earnings']-x['undistributed_equity_earnings']
 if all(k in x for k in ['pretax_income','interest_expense','equity_earnings']):
  x['pretax_plus_interest_includes_equity_income']=x['pretax_income']+x['interest_expense']
  x['pretax_plus_interest_ex_equity_income']=x['pretax_income']+x['interest_expense']-x['equity_earnings']
 if 'pretax_income' in x and 'tax_expense' in x and x['pretax_income']:x['effective_tax_rate_pct']=round(100*x['tax_expense']/x['pretax_income'],4)
 return x
fy={y:get(f'{y}-01-01',f'{y}-12-31') for y in [2023,2024,2025]}
y25=get('2025-01-01','2025-09-30');y26=get('2026-01-01','2026-09-30');y24=get('2024-01-01','2024-09-30')
h26=get('2026-01-01','2026-06-30');q226=get('2026-04-01','2026-06-30');q326=get('2026-07-01','2026-09-30')
# CFO is cumulative only: Q2 = H1 minus Q1; Q3 = 9M minus H1.
q126=get('2026-01-01','2026-03-31')
q226.update(diff(h26,q126))
q326.update(diff(y26,h26))
rows=[{'period':f'FY{y}','basis':'reported','metrics':enrich(v)} for y,v in fy.items()]
rows += [{'period':name,'basis':basis,'metrics':enrich(v)} for name,basis,v in [('Q4 2025','FY2025 minus 9M2025',diff(fy[2025],y25)),('Q1 2026','reported Q1 10-Q',q126),('Q2 2026','reported income; cash flows H1 minus Q1',q226),('Q3 2026','reported income; cash flows 9M minus H1',q326),('9M 2025','reported',y25),('9M 2026','reported',y26),('TTM Sep2025','FY2024 minus 9M2024 plus 9M2025',plus(diff(fy[2024],y24),y25)),('TTM Sep2026','FY2025 minus 9M2025 plus 9M2026',plus(diff(fy[2025],y25),y26))]]
for r in rows:
 if r['period']=='Q4 2025':r['metrics']['eps_diluted']=get('2025-10-01','2025-12-31')['eps_diluted']
for r in rows:
 if r['period']=='TTM Sep2026':r['metrics']['sum_reported_quarterly_eps_not_reweighted']=round(sum(get(a,b)['eps_diluted'] for a,b in [('2025-10-01','2025-12-31'),('2026-01-01','2026-03-31'),('2026-04-01','2026-06-30'),('2026-07-01','2026-09-30')]),2)
 if r['period']=='TTM Sep2025':r['metrics']['sum_reported_quarterly_eps_not_reweighted']=round(sum(get(a,b)['eps_diluted'] for a,b in [('2024-10-01','2024-12-31'),('2025-01-01','2025-03-31'),('2025-04-01','2025-06-30'),('2025-07-01','2025-09-30')]),2)
# Validate primary accounting identity. No derived EPS because changing share counts make subtraction unreliable.
for r in rows:
 m=r['metrics']
 if all(k in m for k in ['pretax_income','tax_expense','nci_income','net_income_parent']):assert abs(m['pretax_income']-m['tax_expense']-m['nci_income']-m['net_income_parent'])<.01,r
(P/'financial_history.json').write_text(json.dumps(rows,indent=2))
cols=['period','basis']+sorted(set().union(*(r['metrics'] for r in rows)))
with (P/'financial_history.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,cols);w.writeheader();w.writerows({'period':r['period'],'basis':r['basis'],**r['metrics']} for r in rows)
segments=sorted({r['segment'] for r in facts if r['segment']!='consolidated'})
out=[]
for seg in segments:
 periods={f'FY{y}':get(f'{y}-01-01',f'{y}-12-31',seg) for y in [2023,2024,2025]}
 a=get('2025-01-01','2025-09-30',seg);b=get('2026-01-01','2026-09-30',seg);h=get('2026-01-01','2026-06-30',seg);q=get('2026-04-01','2026-06-30',seg)
 periods.update({'Q4 2025':diff(periods['FY2025'],a),'Q1 2026':diff(h,q),'Q2 2026':q,'Q3 2026':get('2026-07-01','2026-09-30',seg),'TTM Sep2025':plus(diff(periods['FY2024'],get('2024-01-01','2024-09-30',seg)),a),'TTM Sep2026':plus(diff(periods['FY2025'],a),b)})
 out.extend({'segment':seg,'period':period,**m} for period,m in periods.items())
for r in rows:
 vals=[x['pretax_income'] for x in out if x['period']==r['period'] and 'pretax_income' in x]
 if len(vals)==6:assert abs(sum(vals)-r['metrics']['pretax_income'])<.01, r['period']
(P/'segment_history.json').write_text(json.dumps(out,indent=2))
with (P/'segment_history.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,['segment','period','pretax_income','equity_earnings']);w.writeheader();w.writerows(out)
print('Rebuilt and accounting identities verified:',len(rows),'periods',len(out),'segment rows')
