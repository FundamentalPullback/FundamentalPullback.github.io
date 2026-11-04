from pathlib import Path
import json
P=Path(__file__).parent;f=json.load(open(P/'financials.json'));m=json.load(open(P/'model.json'));p=json.load(open(P/'publication.json'));r=(P/'report.md').read_text()
assert [len(f[k]) for k in ['annual','quarters','ttm']]==[3,4,2]
for k in ['revenue','ebit','net_income','cfo','capex','da','sbc']:
 assert abs(sum(d[k] for d in f['quarters'])-f['ttm'][1][k])<1e-8,k
for c in list(m['cases'].values())+[m['explicit_only_sensitivity']]:
 a=c['assumptions'];pv=0
 for d in c['rows']:
  assert abs(d['fcff']-d['nopat']+d['reinvestment'])<1e-8
  pv+=d['fcff']/(1+a['wacc'])**d['year']
 assert abs(pv-c['pv_explicit'])<1e-8
 assert abs((c['ev']+c['net_bridge'])/a['shares']-c['value'])<1e-8
 assert abs(c['rows'][-1]['reinvestment']-c['rows'][-1]['nopat']*a['g']/a['roic'])<1e-8
for k,c in m['cases'].items():assert abs(c['value']-p[k])<.005
for k in ['pros_es','cons_es','pros_en','cons_en']:
 for x in p[k]:assert x in r
assert not p['approved_entry'] and not p['stage35_approved'] and p['buy_ceiling'] is None
assert abs(m['capital_bridge']['net']+1286.922)<1e-8
print('PASS history, funded FCFF, transition, capital, exact evidence and no entry approval.')
