"""Stdlib rebuild of all derived periods from portable observations.json, no network."""
import json,csv
from pathlib import Path
P=Path(__file__).resolve().parent
obs=json.loads((P/'observations.json').read_text())
index={(x['metric'],tuple(x['dates'])):x for x in obs}
rows=[]
def direct(label,dates):
 for (m,d),x in index.items():
  if list(d)==dates:rows.append(dict(period=label,metric=m,value=x['value'],unit=x['unit'],basis='observed',inputs=[x['id']]))
def derived(label,parts,shares=False):
 metrics=sorted({m for m,d in index})
 for m in metrics:
  if m.startswith('shares_'):continue # Weighted averages are not additive flow measures.
  xs=[index.get((m,tuple(d))) for coef,d in parts]
  if all(xs):rows.append(dict(period=label,metric=m,value=round(sum(c*x['value'] for (c,d),x in zip(parts,xs)),9),unit=xs[0]['unit'],basis='derived',inputs=[{'observation':x['id'],'coefficient':c} for (c,d),x in zip(parts,xs)]))
for y in (2023,2024,2025):direct(f'FY{y}',[f'{y}-01-01',f'{y}-12-31'])
for y in (2024,2025,2026):direct(f'9M{y}',[f'{y}-01-01',f'{y}-09-30'])
for y,q,start,end in [(2025,3,'07-01','09-30'),(2025,4,'10-01','12-31'),(2026,1,'01-01','03-31'),(2026,2,'04-01','06-30'),(2026,3,'07-01','09-30')]:direct(f'Q{q}-{y}',[f'{y}-{start}',f'{y}-{end}'])
derived('Q4-2025',[(1,['2025-01-01','2025-12-31']),(-1,['2025-01-01','2025-09-30'])])
# Cash flow statement is YTD; derive discrete Q2/Q3 only where direct observations unavailable.
for q,cur,prev in [(2,'06-30','03-31'),(3,'09-30','06-30')]:
 existing={(x['period'],x['metric']) for x in rows};old=len(rows)
 derived(f'Q{q}-2026',[(1,['2026-01-01',f'2026-{cur}']),(-1,['2026-01-01',f'2026-{prev}'])])
 rows[old:]=[x for x in rows[old:] if (x['period'],x['metric']) not in existing]
for y in (2025,2026):derived(f'TTM-September-{y}',[(1,[f'{y-1}-01-01',f'{y-1}-12-31']),(1,[f'{y}-01-01',f'{y}-09-30']),(-1,[f'{y-1}-01-01',f'{y-1}-09-30'])])
for d in sorted({d[0] for m,d in index if len(d)==1}):direct(d,[d])
# Transparent CF diagnostics: unadjusted FCF and SBC subtraction, not company non-GAAP FCF.
for period in sorted({x['period'] for x in rows}):
 r={x['metric']:x for x in rows if x['period']==period}
 for m,components in [('fcf_cfo_minus_ppe',[(1,'cfo'),(-1,'capex_ppe')]),('fcf_less_sbc_pnl',[(1,'cfo'),(-1,'capex_ppe'),(-1,'sbc_pnl')]),('working_capital_cash_effect',[(1,'wc_receivables'),(1,'wc_deferred_commissions'),(1,'wc_prepaid_other'),(1,'wc_payables'),(1,'wc_deferred_revenue'),(1,'wc_accruals_other')])]:
  if all(k in r for c,k in components):rows.append(dict(period=period,metric=m,value=round(sum(c*r[k]['value'] for c,k in components),9),unit='USD million',basis='derived',inputs=[{'metric':k,'coefficient':c} for c,k in components]))
(P/'history.json').write_text(json.dumps(rows,indent=2)+'\n')
with (P/'history.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=['period','metric','value','unit','basis','inputs']);w.writeheader()
 for x in rows:w.writerow({**x,'inputs':json.dumps(x['inputs'],separators=(',',':'))})
print(f'{len(obs)} portable observations, {len(rows)} output rows')
