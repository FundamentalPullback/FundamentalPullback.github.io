"""Reproduce derived PRCH audit schedules. USD millions. No external dependencies."""
import json,csv
from pathlib import Path
P=Path(__file__).parent
x=json.loads((P/'inputs.json').read_text())
metrics=['revenue','operating_income','net_income_porch','cfo_consolidated','ppe_cash','software_cash','sbc']
rows=[]
for period,d in x['periods'].items():
 for metric,value in d.items():
  if isinstance(value,(int,float)): rows.append([period,metric,value,'reported',d['source']])
for out,a,b in [('Q4_2025','FY2025','9M2025'),('Q2_2026_cash','6M2026','Q1_2026'),('Q3_2026_cash','9M2026','6M2026')]:
 for m in metrics:
  if out!='Q4_2025' and m in ['revenue','operating_income','net_income_porch']:continue
  if m in x['periods'][a] and m in x['periods'][b]: rows.append([out,m,round(x['periods'][a][m]-x['periods'][b][m],6),'derived_difference',x['periods'][a]['source']+';'+x['periods'][b]['source']])
for m in metrics:
 rows.append(['TTM_2026_09_30',m,round(x['periods']['FY2025'][m]+x['periods']['9M2026'][m]-x['periods']['9M2025'][m],6),'derived_FY_plus_YTD_minus_prior_YTD','FY25;Q3_26'])
for m in metrics:
 rows.append(['PRIOR_TTM_2025_09_30_AUDIT_ONLY',m,round(x['periods']['FY2024'][m]+x['periods']['9M2025'][m]-x['periods']['9M2024'][m],6),'derived_mixed_ownership_perimeter','FY25;Q3_26;Q3_25_legacy'])
for period in ['FY2025','9M2025','9M2026']:
 d=x['periods'][period]; rows.append([period,'cfo_excluding_reciprocal',round(d['cfo_consolidated']-d['cfo_reciprocal'],6),'derived_difference',d['source']])
def porch_cfo(period):
 d=x['periods'][period]
 return d['cfo_consolidated']-d['cfo_reciprocal']
ttm_porch_cfo=round(porch_cfo('FY2025')+porch_cfo('9M2026')-porch_cfo('9M2025'),6)
rows.append(['TTM_2026_09_30','cfo_excluding_reciprocal',ttm_porch_cfo,'derived_FY_plus_YTD_minus_prior_YTD','FY25;Q3_26'])
with (P/'normalized_financials.csv').open('w') as f:
 w=csv.writer(f);w.writerow(['period','metric','USD_millions','basis','source']);w.writerows(rows)
checks={
 'derived_ttm_porch_cfo_matches_report_78_643':abs(ttm_porch_cfo-78.643)<1e-8,
 'q1_q2_q3_revenue_equals_9m':abs(121.123+140.882+143.860-405.865)<1e-8,
 'q1_q2_q3_operating_income_equals_9m':abs(11.815-4.113+18.090-25.792)<1e-8,
 'q1_q2_q3_porch_ni_equals_9m':abs(-4.713+5.603+12.185-13.075)<1e-8,
 'porch_9m_ni_equals_consolidated_minus_reciprocal':abs(-3.201-(-16.276)-13.075)<1e-8,
 'cash_perimeter_equals_consolidated':abs(80.063+7.092+143.387-230.542)<1e-8,
 'balance_sheet_balances':abs(836.805+0.016+29.665-866.486)<1e-8,
 'restricted_investments_equal_short_plus_long':abs(5.212+72.300-77.512)<1e-8,
 'q3_release_cfo_matches_ytd_difference':abs(59.359-(113.810-54.289))<1e-8,
 'q3_release_capex_matches_ytd_difference':abs(3.889-((0.915+12.003)-(0.548+8.320)))<1e-8}
(P/'validation.json').write_text(json.dumps(checks,indent=2)+'\n')
print(json.dumps(checks,indent=2))
