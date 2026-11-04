from pathlib import Path
import json
P=Path(__file__).parent;m=json.load(open(P/'model.json'));f=json.load(open(P/'financials.json'));p=json.load(open(P/'publication.json'));r=(P/'report.md').read_text()
assert len(f['annual'])==3 and len(f['quarters'])==4 and len(f['ttm'])==2
for k in ['revenue','ebit','net_income','cfo','capex','sbc']:
 assert abs(sum(d[k] for d in f['quarters'])-f['ttm'][1][k])<1e-6,k
for k,c in m['cases'].items():
 a=c['assumptions'];assert len(c['rows'])==10 and a['wacc']>a['g'];pv=0
 for d in c['rows']:
  assert abs(d['fcff']-d['nopat']+d['reinvestment'])<1e-6
  pv+=d['fcff']/(1+a['wacc'])**d['year']
 assert abs(pv-c['pv_explicit'])<1e-6
 assert abs(c['rows'][-1]['reinvestment']-c['rows'][-1]['nopat']*a['g']/a['roic'])<1e-6
 assert abs((c['ev']+c['net_bridge'])/a['shares']-c['value'])<1e-6
 assert abs(c['value']-p[k])<.005
for k in ['pros_es','cons_es','pros_en','cons_en']:
 for x in p[k]:assert x in r
assert not p['approved_entry'] and not p['stage35_approved']
assert p['buy_ceiling'] is None
assert abs(m['bridge'][-1][1]-m['cases']['base']['value'])<1e-6
b=m['capital_bridge'];assert abs(b['proforma_cash']-339.4)<1e-6 and abs(b['proforma_debt']-2081.2)<1e-6
print('PASS: history, FCFF, transition, old-model bridge, capital bridge and evidence excerpts. No entry approved.')
