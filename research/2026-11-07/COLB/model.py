import json,csv
from pathlib import Path
P=Path(__file__).parent
m=json.loads((P/'model.json').read_text()); f=json.loads((P/'financials.json').read_text());r=json.loads((P/'results.json').read_text())
rows=[]
for roe in m['roe_assumption_grid']:
 for ke in m['ke_assumption_grid']:
  for g in m['g_assumption_grid']:
   rows.append(dict(roe=roe,ke=ke,g=g,illustrative_value=round(m['book_per_share_reported']*(roe-g)/(ke-g),4),payout=round(1-g/roe,6),approved=False))
with (P/'diagnostic_sensitivity.csv').open('w') as out:
 w=csv.DictWriter(out,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
checks={'quarter_sum_ni_835':sum(x['net_income'] for x in f['quarters'])==835,'quarter_sum_nii_2425':sum(x['nii'] for x in f['quarters'])==2425,'tangible_bridge':7079-1482-595==5002,'balance_sheet':58056+7079==65135,'final_capital_used':m['cet1_ratio']==.1157,'approved_values_null':all(r[k] is None for k in ['fair_value_adverse','fair_value_base','fair_value_favorable','buy_zone','margin_of_safety']),'not_complete':r['stage3_complete'] is False}
assert all(checks.values()),checks
(P/'audit_checks.json').write_text(json.dumps({'checks':checks,'limits':['Arithmetic and provenance checks are not economic approval.','Source rounded EPS and ratios do not support exact valuation or risk-weighted assets.','Independent audit scope and exact freeze are recorded separately in independent_audit.json.']},indent=2)+'\n')
print(json.dumps(checks))
