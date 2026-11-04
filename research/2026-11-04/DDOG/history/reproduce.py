#!/usr/bin/env python3
"""Offline standard-library reproduction from the bundled source_subset.json."""
import json,csv,pathlib
P=pathlib.Path(__file__).resolve().parent
s=json.loads((P/'source_subset.json').read_text()); r=s['periods']; checks=[]
fields=[k for k in r['FY2025'] if k not in ('source_id','evidence','unaudited_release','period_start','period_end')]
for name,row in r.items():
 residual=row['cfo']-row['ppe_cash']-row['capitalized_software_cash']-row['issuer_fcf']
 checks.append({'check':name+' issuer FCF = CFO - PPE - capitalized software','residual_usd_thousands':residual,'status':'PASS' if residual==0 else 'FLAG'})
for f in s['annual_10k_verification_facts']:
 year='FY'+f['start'][:4];metric=f['metric'];v=f['val']/(1000 if f['unit']=='USD' else 1)
 if metric in r[year]:
  diff=r[year][metric]-v;checks.append({'check':year+' '+metric+' versus audited 2025 10-K','residual_usd_thousands_or_eps':diff,'status':'PASS' if diff==0 else 'FLAG'})
 else:r[year][metric]=v
for name,a,b in [('TTM_2026_09_30','Q4_2025','9M2026'),('PRIOR_TTM_2025_09_30','Q4_2024','9M2025')]:
 r[name]={k:(None if k=='diluted_eps' or r[a].get(k) is None or r[b].get(k) is None else r[a][k]+r[b][k]) for k in fields}
 r[name].update(source_id=r[a]['source_id']+' + '+r[b]['source_id'],evidence='derived_calculation',unaudited_release=True)
 r[name]['period_start']='2025-10-01' if name=='TTM_2026_09_30' else '2024-10-01'
 r[name]['period_end']='2026-09-30' if name=='TTM_2026_09_30' else '2025-09-30'
 r[name]['eps_note']='TTM GAAP diluted EPS not computed by adding quarterly EPS or differencing YTD EPS; direct quarterly EPS retained.'
for k in fields:
 if k=='diluted_eps':continue
 if any(r[q].get(k) is None for q in ['Q1_2026','Q2_2026','Q3_2026']):continue
 diff=sum(r[q][k] for q in ['Q1_2026','Q2_2026','Q3_2026'])-r['9M2026'][k]
 checks.append({'check':k+' direct quarterly sum versus 9M2026','residual_usd_thousands':diff,'status':'PASS' if diff==0 else 'FLAG'})
for row in r.values():
 row['fcf_less_expensed_sbc']=row['issuer_fcf']-row['sbc_expensed']
 row['cfo_less_ppe_only']=row['cfo']-row['ppe_cash']
 row['ebit_margin_pct']=100*row['gaap_ebit']/row['revenue'];row['fcf_margin_pct']=100*row['issuer_fcf']/row['revenue'];row['sbc_revenue_pct']=100*row['sbc_expensed']/row['revenue']
 row.setdefault('income_taxes_paid',None);row.setdefault('capitalized_sbc',None)
 growth={}
for metric in ['revenue','gaap_ebit','net_income','cfo','issuer_fcf','sbc_expensed']:
 prior=r['PRIOR_TTM_2025_09_30'][metric];growth[metric]=100*(r['TTM_2026_09_30'][metric]/prior-1) if prior>0 else None
out={'metadata':{k:v for k,v in s.items() if k not in ['periods','annual_10k_verification_facts']},'periods':r,'ttm_growth_pct':growth,'validation_checks':checks}
(P/'normalized_history.json').write_text(json.dumps(out,indent=2))
cols=['period']+list(dict.fromkeys(k for row in r.values() for k in row))
with (P/'normalized_history.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=cols);w.writeheader();w.writerows({'period':n,**v} for n,v in r.items())
(P/'validation_checks.json').write_text(json.dumps(checks,indent=2))
print(json.dumps({'TTM':r['TTM_2026_09_30'],'prior_TTM':r['PRIOR_TTM_2025_09_30'],'growth':growth,'checks':len(checks),'flags':[x for x in checks if x['status']=='FLAG']},indent=2))
