"""Standard-library-only reproducible history. Source inputs copied from cited primary statements.
Run python build_history.py. No network/packages required; creates normalized JSON/CSV.
Amounts USD millions except per share. EPS is direct-disclosed, never annual-minus-YTD.
"""
import json,csv
from pathlib import Path
P=Path(__file__).resolve().parent
raw=json.loads((P/'source_numeric_subset.json').read_text())
cols=raw['columns']; rows={k:dict(zip(cols,v['values']))|{'source':v['source']} for k,v in raw['periods'].items()}
# Cash flow quarters are YTD differences; earnings quarters are direct-disclosed.
cf=['cfo_cont','cfo_disc','da_ex_acq','acq_amort_cf','sbc','ppe_cont','ppe_disc','investment_gains_cf','acquisition_cash_net']
for q,new,old in [('Q2FY2026','H1FY2026','Q1FY2026'),('Q3FY2026','9MFY2026','H1FY2026'),('Q2FY2025','H1FY2025','Q1FY2025'),('Q3FY2025','9MFY2025','H1FY2025')]:
 for c in cf:
  rows[q][c]=rows[new][c]-rows[old][c]
 rows[q]['cashflow_derivation']=new+' - '+old
for label,qs in [('TTM_Q3FY2026',['Q4FY2025','Q1FY2026','Q2FY2026','Q3FY2026']),('TTM_Q3FY2025',['Q4FY2024','Q1FY2025','Q2FY2025','Q3FY2025'])]:
 rows[label]={c:sum(rows[q][c] for q in qs) for c in cols if c not in ['eps_diluted','eps_cont_diluted']}
 rows[label]['eps_diluted']=None;rows[label]['eps_cont_diluted']=None
 rows[label]['sum_quarterly_eps_not_reported_ttm_eps']=round(sum(rows[q]['eps_diluted'] for q in qs),2)
 rows[label]['sum_quarterly_cont_eps_not_reported_ttm_eps']=round(sum(rows[q]['eps_cont_diluted'] for q in qs),2)
 rows[label]['source']=' + '.join(qs)
for k,v in rows.items():
 v['total_da_cf']=v['da_ex_acq']+v['acq_amort_cf']
 v['fcf_cont']=v['cfo_cont']-v['ppe_cont']
 v['fcf_cont_less_sbc']=v['fcf_cont']-v['sbc']
 v['cfo_total']=v['cfo_cont']+v['cfo_disc']
 v['ebit_margin']=v['ebit']/v['revenue']
 v['fcf_cont_margin']=v['fcf_cont']/v['revenue']
 assert abs(v['ni_total']-v['ni_cont']-v['ni_disc'])<.01,k
# Cross-period identities protect FY/Q/YTD alignment.
for c in cols:
 if c not in ['eps_diluted','eps_cont_diluted']:
  assert abs(rows['FY2025'][c]-rows['9MFY2025'][c]-rows['Q4FY2025'][c])<.01,(c,'FY25 bridge')
  assert abs(rows['9MFY2026'][c]-sum(rows[q][c] for q in ['Q1FY2026','Q2FY2026','Q3FY2026']))<.01,(c,'2026 bridge')
(P/'normalized_history.json').write_text(json.dumps({'units':raw['units'],'periods':rows,'segments':raw['segments']},indent=2)+'\n')
fields=['period']+cols+['total_da_cf','fcf_cont','fcf_cont_less_sbc','cfo_total','ebit_margin','fcf_cont_margin','source','cashflow_derivation','sum_quarterly_eps_not_reported_ttm_eps','sum_quarterly_cont_eps_not_reported_ttm_eps']
with (P/'normalized_history.csv').open('w') as f:
 w=csv.DictWriter(f,fields);w.writeheader();w.writerows(dict(period=k,**v) for k,v in rows.items())
print(json.dumps({k:rows[k] for k in ['TTM_Q3FY2026','TTM_Q3FY2025']},indent=2))
