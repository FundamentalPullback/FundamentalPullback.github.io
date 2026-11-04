"""Offline reproducible LRCX normalization. Only Python standard library required.
Run: python build_history.py. Inputs: source_facts.json; outputs: history.json,csv,checks.json.
All currency in USD, shares in units, EPS in USD/share. No zeros imputed.
"""
import json,csv,datetime,math
from pathlib import Path
H=Path(__file__).parent
pack=json.loads((H/'source_facts.json').read_text())
supp=json.loads((H/'supplemental_facts.json').read_text())
facts=pack['facts']+supp['facts'];sources={s['id']:s for s in pack['sources']+supp['sources']}
metrics=['revenue','ebit','net_income','cfo','capex_including_intangibles','sbc_expense','da','depreciation','eps_basic','eps_diluted','shares_basic','shares_diluted','pretax_income','income_tax']
flows=[m for m in metrics if not m.startswith(('eps_','shares_'))]
checks=[]
def exact(m,start,end):
 fs=[f for f in facts if f['metric']==m and f['start']==start and f['end']==end]
 if not fs:return None,None
 f=max(fs,key=lambda f:sources[f['source']]['filed'])
 return f['value'],{'method':'reported','source':f['source'],'context':f['context'],'tag':f['tag']}
def period(label,start,end):
 row={'period':label,'start':start,'end':end,'weeks':((datetime.date.fromisoformat(end)-datetime.date.fromisoformat(start)).days+1)/7,'provenance':{}}
 for m in metrics: row[m],row['provenance'][m]=exact(m,start,end)
 return row
fy={2024:period('FY2024','2023-06-26','2024-06-30'),2025:period('FY2025','2024-07-01','2025-06-29'),2026:period('FY2026','2025-06-30','2026-06-28')}
quarters=[]
qdates={2025:['2024-07-01','2024-09-29','2024-12-29','2025-03-30','2025-06-29'],2026:['2025-06-30','2025-09-28','2025-12-28','2026-03-29','2026-06-28'],2027:['2026-06-29','2026-09-27']}
for year,dates in qdates.items():
 for q,end in enumerate(dates[1:],1):
  start=dates[0] if q==1 else (datetime.date.fromisoformat(dates[q-1])+datetime.timedelta(days=1)).isoformat()
  row=period(f'Q{q}FY{year}',start,end)
  if q>1:
   for m in metrics:
    if row[m] is not None:continue
    cur,cp=exact(m,dates[0],end);prev,pp=exact(m,dates[0],dates[q-1])
    if cur is None or prev is None:continue
    if m in flows:row[m]=cur-prev;method='cumulative_difference'
    elif m.startswith('shares_'):
     row[m]=q*cur-(q-1)*prev;method='equal_13_week_weighted_average_difference'
    else:continue
    row['provenance'][m]={'method':method,'current':cp,'previous':pp}
  for suffix in ['basic','diluted']:
   m='eps_'+suffix
   if row[m] is None and row['net_income'] is not None and row['shares_'+suffix]:
    row[m]=row['net_income']/row['shares_'+suffix];row['provenance'][m]={'method':'NI/derived_weighted_shares_unrounded'}
  quarters.append(row)
# TTM financial flows are annual + latest Q1 - prior Q1. Avoid adding EPS or shares.
ttms=[]
for year in [2026,2027]:
 latest=next(q for q in quarters if q['period']==f'Q1FY{year}');prior=next(q for q in quarters if q['period']==f'Q1FY{year-1}')
 annual=fy[year-1]
 row={'period':'TTM_'+latest['end'],'start':(datetime.date.fromisoformat(prior['end'])+datetime.timedelta(days=1)).isoformat(),'end':latest['end'],'weeks':52,'provenance':{}}
 for m in flows:
  inputs=[annual[m],latest[m],prior[m]]
  row[m]=inputs[0]+inputs[1]-inputs[2] if all(v is not None for v in inputs) else None
  row['provenance'][m]={'method':'FY+currentQ1-priorQ1','periods':[annual['period'],latest['period'],prior['period']]}
 for suf in ['basic','diluted']:
  m='shares_'+suf
  row[m]=(annual[m]*4+latest[m]-prior[m])/4
  row['eps_'+suf]=row['net_income']/row[m]
  row['provenance'][m]={'method':'52-week_average=(4*FY+currentQ1-priorQ1)/4'}
  row['provenance']['eps_'+suf]={'method':'TTM_NI/TTM_average_shares_not_sum_of_rounded_EPS'}
 ttms.append(row)
for r in [*fy.values(),*quarters,*ttms]:
 # Acquired amortization separately verified in earnings release for Q4FY26/Q1FY27.
 for m in ['amortization_acquired_cogs','amortization_acquired_sga']:
  r[m],r['provenance'][m]=exact(m,r['start'],r['end'])
 r['amortization_acquired']=r['amortization_acquired_cogs']+r['amortization_acquired_sga'] if r['amortization_acquired_cogs'] is not None and r['amortization_acquired_sga'] is not None else None
 r['ebit_before_acquired_amortization']=r['ebit']+r['amortization_acquired'] if r['amortization_acquired'] is not None else None
 # Disaggregation is not disclosed, not zero. Residual is not asserted intangible amortization.
 r.update({'capex_physical_gross':None,'capex_software_gross':None,'sbc_capitalized':None,'amortization_separately_disclosed':None,'da_less_depreciation_residual':r['da']-r['depreciation'] if r['da'] is not None and r['depreciation'] is not None else None})
 r['fcf_reported_capex']=r['cfo']-r['capex_including_intangibles']
 r['fcf_after_sbc_expense']=r['fcf_reported_capex']-r['sbc_expense']
 r['ebit_margin']=r['ebit']/r['revenue'];r['tax_rate']=r['income_tax']/r['pretax_income'];r['cfo_to_ni']=r['cfo']/r['net_income']
 r['fcf_after_sbc_margin']=r['fcf_after_sbc_expense']/r['revenue']
 r['tax_normalized_NI_at_17pct_sensitivity']=r['pretax_income']*.83
 if r['shares_diluted']:
  delta=abs(r['net_income']/r['shares_diluted']-r['eps_diluted']);checks.append({'test':r['period']+' diluted EPS rounding','pass':delta<=.0051,'delta':delta})
 checks.append({'test':r['period']+' pretax-tax=NI','pass':abs(r['pretax_income']-r['income_tax']-r['net_income'])<=1000})
for year in [2025,2026]:
 qs=[r for r in quarters if r['period'].endswith(str(year))]
 for m in flows:
  if all(r[m] is not None for r in qs):checks.append({'test':f'FY{year} sum quarters {m}','pass':abs(sum(r[m] for r in qs)-fy[year][m])<1,'delta':sum(r[m] for r in qs)-fy[year][m]})
last4=quarters[-4:];prior4=quarters[-8:-4]
for t,qs in zip(ttms,[prior4,last4]):
 for m in flows:
  if all(r[m] is not None for r in qs) and t[m] is not None:checks.append({'test':t['period']+' four quarters '+m,'pass':abs(sum(r[m] for r in qs)-t[m])<1})
growth={m:(ttms[1][m]/ttms[0][m]-1 if ttms[0].get(m) and ttms[1].get(m) is not None else None) for m in metrics+['fcf_reported_capex','fcf_after_sbc_expense']}
output={'ticker':'LRCX','as_of':'2026-11-04','units':'USD absolute; shares absolute; ratios decimal','annual':list(fy.values()),'quarters':quarters,'last_four_quarters':[q['period'] for q in last4],'ttm':ttms,'ttm_growth':growth,'limitations':['Physical/software capex not separately disclosed; aggregate includes intangible assets, no disposal proceeds netted.','Capitalized SBC not separately disclosed; no zero assumption. FCF after SBC expense does not claim to capture unreported capitalized SBC.','D&A less reported depreciation is an approximate residual, not a separately disclosed intangible amortization amount. Annual depreciation rounded to nearest $0.1m. Quarterly depreciation unavailable.','Q4 EPS reconstructed from NI / implied weighted shares; not annual EPS minus YTD EPS.','FY2024 53 weeks; FY2025/26 and both TTMs 52 weeks. No mechanically invented weekly sales normalization.','Use post-split historical comparatives in FY2026 10-K. 2024 original filing has pre-split shares/EPS; do not mix.','17% tax sensitivity is analyst assumption, not management guidance or reported normalized earnings.']}
(H/'history.json').write_text(json.dumps(output,indent=2)+'\n')
rows=[*fy.values(),*quarters,*ttms];fields=[k for k in rows[0] if k!='provenance']
with (H/'history.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows({k:v for k,v in r.items() if k!='provenance'} for r in rows)
(H/'checks.json').write_text(json.dumps({'all_pass':all(c['pass'] for c in checks),'checks':checks},indent=2)+'\n')
assert all(c['pass'] for c in checks),[c for c in checks if not c['pass']]
print('PASS',len(checks),'checks')
for r in rows:
 print(r['period'],*[round(r[m]/1e6,3) if r[m] is not None else None for m in ['revenue','ebit','net_income','cfo','capex_including_intangibles','sbc_expense','fcf_after_sbc_expense']])
print('TTM growth',growth)
