from pathlib import Path
import json
P=Path(__file__).parent;f=json.load(open(P/'financials.json'));m=json.load(open(P/'model.json'));p=json.load(open(P/'publication.json'));s=(P/'report.md').read_text()
assert [len(f[k]) for k in ['annual','quarters','ttm']]==[3,4,2]
for k in ['revenue','ebit','net_income','cfo','capex','da','sbc','eps']:
 assert abs(sum(d[k] for d in f['quarters'])-f['ttm'][1][k])<1e-8,k
for c in list(m['cases'].values())+[m['explicit_only_stress']]:
 a=c['assumptions'];pv=0
 for r in c['rows']:
  assert abs(r['nopat']-r['ebit']*(1-a['tax']))<1e-8
  assert abs(r['fcff']-r['nopat']+r['reinvestment'])<1e-8
  pv+=r['fcff']/(1+a['wacc'])**r['year']
 assert abs(pv-c['pv_explicit'])<1e-8
 assert abs(c['rows'][-1]['reinvestment']-c['rows'][-1]['nopat']*a['g']/a['roic'])<1e-8
 assert abs((c['ev']+c['net_bridge'])/a['shares']-c['value'])<1e-8
 assert a['wacc']>a['g']
for k,c in m['cases'].items():assert abs(c['value']-p[k])<.005
for k in ['pros_es','cons_es','pros_en','cons_en']:
 for line in p[k]:assert line in s
assert p['buy_ceiling'] is None and not p['approved_entry'] and not p['stage35_approved']
assert abs(m['capital_bridge']['net']+411.203)<1e-8
assert abs(m['historical_A003']['base']-38)<1e-8
print('PASS: primary history, cash bridge, funded FCFF, terminal, exact pros/cons and no trade approval.')
