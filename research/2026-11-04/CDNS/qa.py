"""Non-mutating consistency audit, separate from independent investment review."""
from pathlib import Path
import json,math
P=Path(__file__).parent;m=json.load(open(P/'model.json'));f=json.load(open(P/'financials.json'));p=json.load(open(P/'publication.json'));r=(P/'report.md').read_text()
assert len(f['annual'])==3 and len(f['quarters'])==4 and len(f['ttm'])==2
for k in ['revenue','ebit','net_income','cfo','capex','sbc']:
 assert abs(sum(x[k] for x in f['quarters'])-f['ttm'][1][k])<1e-6,k
for name,c in m['cases'].items():
 a=c['assumptions'];assert a['wacc']>a['g'];assert len(c['rows'])==10
 pv=0
 for row in c['rows']:
  assert abs(row['nopat']-row['ebit']*(1-a['tax']))<1e-6
  assert abs(row['fcff']-(row['nopat']-row['reinvestment']))<1e-6
  pv+=row['fcff']/(1+a['wacc'])**row['year']
 assert abs(pv-c['pv_explicit'])<1e-6
 assert abs(c['rows'][-1]['reinvestment']-c['rows'][-1]['nopat']*a['g']/a['roic'])<1e-6
 assert abs((c['ev']+c['net_bridge'])/a['shares']-c['value'])<1e-6
 assert abs(c['value']-p[name])<.005
for k in ['pros_es','cons_es','pros_en','cons_en']:
 for item in p[k]:assert item in r
assert not p['approved_entry'] and not p['stage35_approved'] and p['buy_ceiling'] is None
for k,target in [('bear',87.57),('base',150.68),('bull',271.08)]:assert abs(m['historical_A106'][k]['value']-target)<.005
print('PASS: 3FY/4Q/TTM, ten-year FCFF, terminal transition, exact historical replication, evidence excerpts, no entry.')
