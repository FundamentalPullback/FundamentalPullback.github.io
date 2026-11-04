"""Offline stdlib-only rebuild from minimal primary-source facts, USD millions."""
import json,csv
from pathlib import Path
P=Path(__file__).resolve().parent
inp=json.loads((P/'financial_inputs.json').read_text())
rows={r['period']:dict(r['values']) for r in inp['periods']}
def calc(name,terms):
 keys=rows[terms[0][1]]
 rows[name]={k:None if any(rows[p][k] is None for c,p in terms) else sum(c*rows[p][k] for c,p in terms) for k in keys}
calc('Q42025',[(1,'FY2025'),(-1,'9M2025')]);calc('Q22026',[(1,'H12026'),(-1,'Q12026')]);calc('Q32026',[(1,'9M2026'),(-1,'H12026')])
calc('TTM2026-09',[(1,'FY2025'),(1,'9M2026'),(-1,'9M2025')]);calc('TTM2025-09',[(1,'FY2024'),(1,'9M2025'),(-1,'9M2024')])
checks=[]
for name,r in rows.items():
 r['ebit_operating_reported_reconstructed']=r['revenue']-r['operating_costs_total']
 r['ebit_partial_normalized']=r['ebit_operating_reported_reconstructed']+r['impairment_separate_line']+r['asset_sale_loss_gain']
 r['fcf_cfo_less_capex']=r['cfo']-r['capex_cash']
 r['fcf_continuing']=None if r['cfo_continuing'] is None else r['cfo_continuing']-r['capex_cash']
 r['capex_accrual_to_cash_adjustment']=r['capex_cash']-r['capex_development_accrual']-r['capex_sustaining_accrual']
 assert r['ni_consolidated']-r['nci_income']==r['ni_parent'],(name,'NCI')
 assert r['ebit_operating_reported_reconstructed']+r['nonoperating_income_expense']==r['pretax_before_equity_income'],(name,'EBIT')
 checks.extend([f'{name}: NI consolidated - NCI = NI parent PASS',f'{name}: operating EBIT + nonoperating income/expense = pretax before equity affiliates PASS'])
for k in rows['TTM2026-09']:
 vals=[rows[p][k] for p in ['Q42025','Q12026','Q22026','Q32026']]
 if all(v is not None for v in vals):assert sum(vals)==rows['TTM2026-09'][k],k
checks.append('Last four quarters equal current TTM for all non-null metrics PASS')
order=['FY2023','FY2024','FY2025','Q42025','Q12026','Q22026','Q32026','TTM2025-09','TTM2026-09']
out={'units':'USD millions','basis':'reported consolidated perimeter; not same-mine or attributable owner cash flow','periods':{p:rows[p] for p in order},'supporting_periods':{p:rows[p] for p in rows if p not in order},'ttm_yoy_pct':{k:None if rows['TTM2026-09'][k] is None or rows['TTM2025-09'][k] in [None,0] else (rows['TTM2026-09'][k]/rows['TTM2025-09'][k]-1)*100 for k in rows['TTM2026-09']},'checks':checks}
(P/'financial_history.json').write_text(json.dumps(out,indent=2))
with open(P/'financial_history.csv','w') as f:
 w=csv.writer(f);w.writerow(['metric']+order)
 for k in rows['FY2023']:w.writerow([k]+[rows[p][k] for p in order])
(P/'checks.txt').write_text('\n'.join(checks)+'\n')
print(json.dumps({p:{k:rows[p][k] for k in ['revenue','ebit_operating_reported_reconstructed','ebit_partial_normalized','ni_parent','cfo','capex_cash','fcf_cfo_less_capex','sbc_expense']} for p in order},indent=2))
