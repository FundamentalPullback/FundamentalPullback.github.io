from pathlib import Path
import json,math
P=Path(__file__).parent;f=json.load(open(P/'financials.json'));m=json.load(open(P/'model.json'));meta=json.load(open(P/'publication.json'));s=(P/'report.md').read_text()
for k in ['revenue','ebit','net_income','cfo','capex','sbc','da']:
 assert math.isclose(sum(q[k] for q in f['quarters']),f['ttm'][-1][k],abs_tol=1e-7),k
for d in f['annual']+f['quarters']+f['ttm']:assert math.isclose(d['fcf_less_sbc'],d['cfo']-d['capex']-d['sbc'],abs_tol=1e-8)
assert f['quarters'][1]['eps']==2.56 and f['quarters'][1]['shares']==199.8
for name,c in m['cases'].items():
 a=c['assumptions'];r=c['rows'];assert len(r)==10
 assert math.isclose(sum(x['pv_fcff'] for x in r),c['pv_explicit'],abs_tol=1e-7)
 assert math.isclose(c['value'],(c['pv_explicit']+c['pv_terminal']+m['capital_bridge']['net'])/a['shares'],abs_tol=1e-8)
 assert math.isclose(c['terminal_reinvestment'],max(c['terminal_explicit_reinvestment'],c['terminal_nopat']*a['g']/a['roic']),abs_tol=1e-7)
 assert math.isclose(c['terminal_reinvestment'],r[-1]['reinvestment']*(1+a['g']),abs_tol=1e-7)
 for x in r:
  assert math.isclose(x['fcff'],x['nopat']+x['da']-x['capex']-x['delta_nwc']-x['additional_reinvestment_reserve'],abs_tol=1e-7)
  assert x['additional_reinvestment_reserve']>=-1e-8
  assert math.isclose(x['economic_reinvestment'],x['core_nopat']*x['growth']/a['roic'],abs_tol=1e-7)
 assert meta[name]==round(c['value'],2)
for name,c in m['historical_A113']['reconstruction'].items():assert abs(c['value']-m['historical_A113']['published'][name])<.005
assert max(x['value'] for x in m['reverse']['growth_scan'])<m['price']
from model import calc
assert math.isclose(calc(md=m['reverse']['margin_extra_all_years'])['value'],m['price'],abs_tol=1e-7)
for key in ['pros_es','cons_es','pros_en','cons_en']:
 for t in meta[key]:assert t in s,(key,t)
assert not meta['stage35_approved'] and not meta['approved_entry'] and meta['buy_ceiling'] is None
assert 'no se certifica un cierre normativo integral' in s
assert math.isclose(m['capital_bridge']['net'],-2421.1,abs_tol=1e-8)
print('PASS: source-derived 3FY/4Q/TTM, original FCFF reconstruction, capital, fully financed terminal, non-monotone reverse, bilingual evidence and no entry approval.')
