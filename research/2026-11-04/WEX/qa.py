from pathlib import Path
import json,math,re
P=Path(__file__).parent;f=json.load(open(P/'financials.json'));c=json.load(open(P/'capital.json'));m=json.load(open(P/'publication.json'));s=(P/'report.md').read_text()
for k in ['revenue','operating_income','net_income','cfo','capex','sbc','da','credit_provision']:
 assert math.isclose(sum(x[k] for x in f['quarters']),f['ttm'][-1][k],abs_tol=.11),k
for r in f['annual']+f['quarters']+f['ttm']:
 assert math.isclose(r['raw_cfo_less_capex_sbc'],r['cfo']-r['capex']-r['sbc'],abs_tol=1e-8)
assert f['quarters'][0]['eps']==2.41 and f['quarters'][0]['shares']==35
assert math.isclose(c['adjusted_fcf']['component_sum'],502.9,abs_tol=1e-8)
assert math.isclose(c['adjusted_fcf']['rounding_residual'],-.1,abs_tol=1e-8)
assert c['adjusted_fcf']['reported']==502.8
assert c['bank']['rwa_approx']==7742 and c['bank']['prior_rwa_approx']==5101
for r in c['bank']['target_total_capital_sensitivity']:
 assert math.isclose(r['required_capital']+r['arithmetical_headroom'],1007.5,abs_tol=1e-8)
assert c['cash']['corporate_covenant'] < c['cash']['nonbank_arithmetic'] < c['cash']['consolidated']
assert m['base'] is None and m['bear'] is None and m['bull'] is None
assert c['valuation']['base'] is None and c['valuation']['reverse'] is None
assert not m['approved_entry'] and not m['stage35_approved'] and m['buy_ceiling'] is None
for key in ['pros_es','cons_es','pros_en','cons_en']:
 for t in m[key]:assert t in s
assert 'no demuestra un dividendo' in s and 'terminó el 15 octubre 2026' in s
assert 'no se identifica todo ese incremento como beneficio retenido' in s
print('PASS: 3FY/4Q/TTM, signed CFO, capital arithmetic, rounding residual, exact bilingual evidence, valuation null and no entry approval.')
