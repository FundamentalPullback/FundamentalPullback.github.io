from pathlib import Path
import json,math
P=Path(__file__).parent;f=json.load(open(P/'financials.json'));m=json.load(open(P/'model.json'));meta=json.load(open(P/'publication.json'));s=(P/'report.md').read_text()
for metric in ['revenue','ebit','net_income','cfo','capex','sbc']:
 assert math.isclose(sum(q[metric] for q in f['quarters']),f['ttm'][-1][metric],abs_tol=1e-8),metric
for d in f['annual']+f['quarters']+f['ttm']:
 assert math.isclose(d['fcf_less_sbc'],d['cfo']-d['capex']-d['sbc'],abs_tol=1e-8)
for name,c in m['cases'].items():
 a=c['assumptions'];rows=c['rows'];assert len(rows)==10
 assert math.isclose(sum(r['pv_fcff'] for r in rows),c['pv_explicit'],abs_tol=1e-8)
 assert math.isclose(c['value'],(c['pv_explicit']+c['pv_terminal']+m['capital_bridge']['net'])/a['shares'],abs_tol=1e-8)
 assert math.isclose(c['terminal_reinvestment'],c['terminal_nopat']*a['g']/a['roic'],abs_tol=1e-8)
 assert math.isclose(rows[-1]['reinvestment'],rows[-1]['nopat']*a['g']/a['roic'],abs_tol=1e-8)
 assert all(r['reinvestment']>=-1e-8 for r in rows)
 for r in rows:assert math.isclose(r['fcff'],r['nopat']+r['da']-r['capex']-r['delta_nwc']-r['additional_reinvestment_reserve'],abs_tol=1e-8)
 assert math.isclose(meta[name],round(c['value'],2),abs_tol=.001)
for k in ['pros_es','cons_es','pros_en','cons_en']:
 for t in meta[k]:assert t in s,(k,t)
assert not meta['stage35_approved'] and not meta['approved_entry']
assert 'reconstrucción FCFF' in s
print('PASS: source-derived 3FY/4Q/TTM, FCFF, funded terminal, exact evidence, capital and no entry certification.')
