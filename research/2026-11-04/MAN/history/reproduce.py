#!/usr/bin/env python3
"""Offline, stdlib-only reconstruction from selected, sourced inputs; no filings required."""
import json,csv
from pathlib import Path
P=Path(__file__).resolve().parent
D=json.loads((P/'inputs.json').read_text()); I=D['inputs'];checks=[]
def get(period,metric):
 a=[x for x in I if x['period']==period and x['metric']==metric]
 if not a:return None
 vals={x['value'] for x in a}
 assert len(vals)==1,(period,metric,vals)
 return a[0]['value']
metrics=list(dict.fromkeys(x['metric'] for x in I))
def base(label,period):return {'period':label,'start':period.split('|')[0],'end':period.split('|')[1],'basis':'reported',**{m:get(period,m) for m in metrics}}
def derive(label,start,end,terms):
 out=dict(period=label,start=start,end=end,basis='derived '+ ' '.join(f'{n:+g}*{r["period"]}' for n,r in terms))
 for m in metrics:
  if m in ['eps_diluted','diluted_shares']:out[m]=None
  else:out[m]=round(sum(n*r[m] for n,r in terms),6) if all(r[m] is not None for n,r in terms) else None
 return out
fy=[base('FY'+str(y),f'{y}-01-01|{y}-12-31') for y in [2023,2024,2025]]
y24=base('9M24','2024-01-01|2024-09-30');y25=base('9M25','2025-01-01|2025-09-30');y26=base('9M26','2026-01-01|2026-09-30')
h26=base('6M26','2026-01-01|2026-06-30');q1=base('Q1_2026','2026-01-01|2026-03-31')
q4=derive('Q4_2025','2025-10-01','2025-12-31',[(1,fy[2]),(-1,y25)]);q4['eps_diluted']=get('2025-10-01|2025-12-31','eps_diluted')
q2=derive('Q2_2026','2026-04-01','2026-06-30',[(1,h26),(-1,q1)])
q3=derive('Q3_2026','2026-07-01','2026-09-30',[(1,y26),(-1,h26)])
for row in [q2,q3]:
 for m in ['revenue','ebit','net_income','eps_diluted','diluted_shares','gross_profit','sga','tax_expense','pretax_income','restructuring','impairment']:
  v=get(row['start']+'|'+row['end'],m)
  if v is not None:
   if row.get(m) is not None:checks.append(dict(check=f'{row["period"]} {m} quarter vs YTD delta',difference=round(row[m]-v,6),pass_check=abs(row[m]-v)<.11))
   row[m]=v
quarters=[q4,q1,q2,q3]
ttm=derive('TTM_Sep2026','2025-10-01','2026-09-30',[(1,fy[2]),(1,y26),(-1,y25)])
prior=derive('TTM_Sep2025','2024-10-01','2025-09-30',[(1,fy[1]),(1,y25),(-1,y24)])
ttm['eps_quarter_sum_proxy']=round(sum(q['eps_diluted'] for q in quarters),2)
prior['eps_quarter_sum_proxy']=round(get('2024-10-01|2024-12-31','eps_diluted') + sum(get(x,'eps_diluted') for x in ['2025-01-01|2025-03-31','2025-04-01|2025-06-30','2025-07-01|2025-09-30']),2)
# Explicitly partial normalization: historical impairment removal only; current TTM additionally excludes identified Jefferson Wells operating gain.
for r in fy+[y24,y25,y26,h26,q1,q2,q3,q4,ttm,prior]:
 r['wc_cash_impact']=round(sum(r[m] for m in ['wc_ar_cash','wc_other_assets_cash','wc_ap_cash','wc_other_liabilities_cash']),6) if all(r[m] is not None for m in ['wc_ar_cash','wc_other_assets_cash','wc_ap_cash','wc_other_liabilities_cash']) else None
 r['fcf_cfo_less_total_capex']=round(r['cfo']-r['capex_including_software'],6) if r['cfo'] is not None and r['capex_including_software'] is not None else None
 r['ebit_margin_pct']=round(100*r['ebit']/r['revenue'],4)
 r['ebit_ex_impairment_partial']=round(r['ebit']+r['impairment']+(r.get('other_impairment') or 0),6) if r['impairment'] is not None else None
 r['ebit_normalized_partial']=r['ebit_ex_impairment_partial']
 r['normalization_note']='Impairment only; restructuring, SBC, transformation costs retained. Disposal/tax normalization incomplete.'
 if r is ttm:
  r['ebit_normalized_partial']=round(r['ebit']+r['impairment']-get('2026-01-01|2026-09-30','operating_disposal_gain'),6)
  r['normalization_note']='Only impairments and identified 28.3 Jefferson Wells operating gain removed; restructuring 43.2, SBC and transformation retained. Not recurring earnings.'
 if r is q2:
  r['ebit_normalized_partial']=round(r['ebit']-30.0,6)
  r['normalization_note']='Remove provisional Jefferson Wells operating gain30.0; other adjustments incomplete; restructuring retained.'
 if r is q3:
  r['ebit_normalized_partial']=round(r['ebit']+1.7,6)
  r['normalization_note']='Reverse Jefferson Wells final working-capital gain adjustment -1.7; other adjustments incomplete; restructuring retained.'
 r['ebit_partial_after_identified_matched_plan']=round(r['ebit_normalized_partial']+r['matched_deferred_compensation_investment_gain'],6) if r.get('ebit_normalized_partial') is not None and r.get('matched_deferred_compensation_investment_gain') is not None else None
 r['da_ex_acquired_intangibles_residual']=round(r['da']-r['acquired_intangible_amortization'],6) if r.get('da') is not None and r.get('acquired_intangible_amortization') is not None else None
 # Test CFO using exact cash-flow sign conventions, including net subsidiary disposal adjustments.
 names=['net_income','da','sbc','deferred_tax_cf','credit_loss_provision','disposal_cf_adjustment','impairment','wc_cash_impact']
 if all(r.get(m) is not None for m in names):
  calc=sum(r[m] for m in names)+(r.get('other_impairment') or 0)
  checks.append(dict(check=r['period']+' CFO bridge',difference=round(calc-r['cfo'],6),pass_check=abs(calc-r['cfo'])<.11))
for m in ['revenue','ebit','net_income','cfo','capex_including_software','da','sbc','wc_cash_impact']:
 v=sum(q[m] for q in quarters)
 checks.append(dict(check='4Q sum vs TTM '+m,difference=round(v-ttm[m],6),pass_check=abs(v-ttm[m])<.11))
for r in [ttm,prior]:
 r['eps_diluted']=None # Not a reported GAAP TTM EPS; quarterly sum stored separately.
for rows,name in [(fy,'annual_3fy'),(quarters,'latest_4q'),([prior,ttm],'ttm_comparison'),([y24,y25,y26,h26],'ytd_support')]:
 (P/(name+'.json')).write_text(json.dumps(rows,indent=2))
 keys=list(dict.fromkeys(k for row in rows for k in row))
 with (P/(name+'.csv')).open('w') as f:
  w=csv.DictWriter(f,keys);w.writeheader();w.writerows(rows)
with (P/'Normalized_Financials_Long.csv').open('w') as f:
 keys=list(I[0]);w=csv.DictWriter(f,keys);w.writeheader();w.writerows(I)
with (P/'Source_Index.csv').open('w') as f:
 w=csv.DictWriter(f,['source_id','url','retrieved','status']);w.writeheader();w.writerows(dict(source_id=k,**v) for k,v in D['sources'].items())
(P/'Validation_Checks.json').write_text(json.dumps(checks,indent=2))
assert all(x['pass_check'] for x in checks),[x for x in checks if not x['pass_check']]
print(json.dumps({'checks':len(checks),'all_pass':True,'ttm':ttm,'prior':prior},indent=2))
