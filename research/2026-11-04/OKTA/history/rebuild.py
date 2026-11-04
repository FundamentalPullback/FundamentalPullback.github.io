#!/usr/bin/env python3
"""Offline deterministic normalization from compact primary-source numeric extracts."""
import csv,json,pathlib,copy
P=pathlib.Path(__file__).resolve().parent
D=json.loads((P/'raw_inputs.json').read_text());R=copy.deepcopy(D['records'])
def derive(target,terms,only_missing=False):
 r=R.setdefault(target,{'period':target,'metrics':{},'provenance':{}})
 common=set.intersection(*(set(R[p]['metrics']) for p,sign in terms))
 for k in sorted(common):
  if k.startswith('eps_'):continue
  if only_missing and k in r['metrics']:continue
  r['metrics'][k]=sum(R[p]['metrics'][k]*sign for p,sign in terms)
  r['provenance'][k]={'method':'arithmetic_period_bridge','terms':[{'period':p,'coefficient':sign} for p,sign in terms]}
for fy in [2026,2025]:
 derive(f'Q3FY{fy}',[(f'9MFY{fy}',1),(f'H1FY{fy}',-1)],True)
 derive(f'Q4FY{fy}',[(f'FY{fy}',1),(f'9MFY{fy}',-1)],True)
for fy in [2027,2026]:derive(f'Q2FY{fy}',[(f'H1FY{fy}',1),(f'Q1FY{fy}',-1)],True)
derive('TTM20260731',[('FY2026',1),('H1FY2027',1),('H1FY2026',-1)])
derive('TTM20250731',[('FY2025',1),('H1FY2026',1),('H1FY2025',-1)])
for p,r in sorted(R.items()):
 m=r['metrics']
 if all(k in m for k in ['cfo','ppe_cash_signed','software_cash_signed']):m['fcf_company_definition']=m['cfo']+m['ppe_cash_signed']+m['software_cash_signed']
 if 'fcf_company_definition' in m and 'sbc' in m:m['fcf_less_sbc_sensitivity']=m['fcf_company_definition']-m['sbc']
 if 'da' in m and 'acquired_intangibles_amortization' in m:m['da_ex_acquired_intangibles']=m['da']-m['acquired_intangibles_amortization']
 for k in ['ebit_gaap','net_income_gaap','cfo','sbc','fcf_company_definition']:
  if k in m and 'revenue' in m:m[k+'_margin_pct']=100*m[k]/m['revenue']
for new,old in [('Q3FY2026','Q3FY2025'),('Q4FY2026','Q4FY2025'),('Q1FY2027','Q1FY2026'),('Q2FY2027','Q2FY2026'),('TTM20260731','TTM20250731')]:
 R[new]['comparison_period']=old;R[new]['yoy']={}
 for k in sorted(set(R[new]['metrics'])&set(R[old]['metrics'])):
  a,b=R[new]['metrics'][k],R[old]['metrics'][k]
  R[new]['yoy'][k]={'absolute_change':a-b,'growth_pct':100*(a/b-1) if b>0 else None}
checks=[]
def check(name,actual,expected):
 ok=abs(actual-expected)<1e-8;checks.append({'check':name,'actual':actual,'expected':expected,'pass':ok});assert ok,(name,actual,expected)
for p,expected in [('FY2026',863),('FY2025',730),('FY2024',489),('Q3FY2026',211),('Q4FY2026',252),('Q1FY2027',271),('Q2FY2027',227)]:check(p+' FCF',R[p]['metrics']['fcf_company_definition'],expected)
for k in ['revenue','ebit_gaap','net_income_gaap','cfo','sbc','da','fcf_company_definition']:
 check('TTM sum quarters '+k,sum(R[p]['metrics'][k] for p in ['Q3FY2026','Q4FY2026','Q1FY2027','Q2FY2027']),R['TTM20260731']['metrics'][k])
check('TTM revenue',R['TTM20260731']['metrics']['revenue'],3073)
check('TTM EBIT',R['TTM20260731']['metrics']['ebit_gaap'],232)
assert all('eps_diluted' not in R[p]['metrics'] for p in ['TTM20260731','TTM20250731'])
(P/'normalized_history.json').write_text(json.dumps({'units':D['units'],'as_of':D['as_of'],'sources':D['sources'],'records':R},indent=2,sort_keys=True)+'\n')
rows=[dict(period=p,**r['metrics']) for p,r in sorted(R.items())];keys=['period']+sorted(set().union(*(set(r)-{'period'} for r in rows)))
with (P/'normalized_history.csv').open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=keys);w.writeheader();w.writerows(rows)
(P/'qa.json').write_text(json.dumps({'checks':checks,'all_pass':all(c['pass'] for c in checks),'eps_ttm':'not produced; quarterly EPS is not additive or subtractable to yield annual GAAP EPS'},indent=2,sort_keys=True)+'\n')
print(json.dumps({p:R[p]['metrics'] for p in ['TTM20260731','TTM20250731']},indent=2,sort_keys=True))
