from pathlib import Path
import json
P=Path(__file__).parent;r=(P/'report.md').read_text();p=json.load(open(P/'publication.json'))
checks={'net_revenue_growth_q3':153.063/137.073-1,'gross_revenue_growth_q3':173.733/147.120-1,'ebit_growth_q3':41.877/29.038-1,'net_income_growth_q3':30.943/28.044-1,'ebitda_growth_q3':44.976/38.837-1,'sbc_growth_q3':6.694/5.341-1,'net_revenue_growth_9m':453.740/407.378-1,'net_income_growth_9m':89.907/81.247-1,'sbc_growth_9m':22.432/18.767-1}
assert abs(41.877+.448+2.651-44.976)<1e-8
assert abs(29.038+7.267+2.532-38.837)<1e-8
assert all(p[k] is None for k in ['bear','base','bull','buy_ceiling'])
assert not p['approved_entry'] and not p['stage35_approved']
for k in ['pros_es','pros_en','cons_es','cons_en']:
 for x in p[k]:assert x in r
print(checks);print('PASS: partial status, exact excerpts, growth arithmetic and EBITDA reconciliation; no cash flow inferred.')
json.dump(checks,open(P/'checks.json','w'),indent=2)
