import json,pathlib,importlib.util
P=pathlib.Path(__file__).parent
spec=importlib.util.spec_from_file_location('model',P/'model.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
h=json.loads((P/'history.json').read_text());data=json.loads((P/'model_results.json').read_text());r=(P/'report.md').read_text();pc=json.loads((P/'pros_cons.json').read_text());tests=[]
def check(s,ok):tests.append({'test':s,'pass':bool(ok)})
for k in ['revenue','ebit','ebit_ex_sale_loss','cfo','ppe_capex','sbc']:
 check('Quarterly '+k+' adds to TTM',abs(sum(x[k] for x in h[3:7])-h[-1][k])<1e-8)
for k,s in data['scenarios'].items():
 check(k+' 10-year horizon',len(s['rows'])==10)
 check(k+' WACC > g',s['assumptions']['wacc']>s['assumptions']['terminal_growth'])
 check(k+' cash bridge',abs(s['equity']-s['ev']-133.501)<1e-8)
 check(k+' reproducible',abs(m.model(s['assumptions'])['value']-s['value'])<1e-8)
 check(k+' terminal reinvestment',abs(s['terminal_reinvestment']-s['terminal_nopat']*s['assumptions']['terminal_growth']/s['assumptions']['roic_terminal'])<1e-8)
 check(k+' nonnegative additional investment',all(x['additional_economic_reinvestment']>=0 for x in s['rows']))
 check(k+' FCFF bridge',all(abs(x['ebit_after_book_amortization']-x['cash_tax']+x['total_da']-x['total_investment']-x['delta_nwc']-x['fcff'])<1e-8 for x in s['rows']))
for side in ['pros','cons']:
 for i,x in enumerate(pc[side]):
  check(f'{side}{i} exact evidence',x['evidence'] in r)
  check(f'{side}{i} lengths',len(x['es'])<=320 and len(x['en'])<=360)
  check(f'{side}{i} source present',not x['sourceUrl'] or x['sourceUrl'] in r)
for c in json.loads((P/'comps_results.json').read_text()):
 check(c['ticker']+' same close date',c['price_date']=='2026-11-03')
 check(c['ticker']+' EV bridge',abs(c['ev_reported_cash']-(c['close']*c['diluted_shares']+c['financial_debt']-c['cash_and_short_investments']))<1e-8)
 check(c['ticker']+' TTM bridge',abs(c['ttm_gaap_ebit']-(c['fy_ebit']+c['current_ytd_ebit']-c['prior_ytd_ebit']))<1e-8)
check('No approved entry',json.loads((P/'summary.json').read_text())['approvedEntry']==False)
check('Inputs available',(P/'inputs/xbrl_subset.json').exists())
(P/'qa.json').write_text(json.dumps({'automated_checks':tests,'pass':all(t['pass'] for t in tests),'scope':'Arithmetic, source-evidence containment and reproducibility. Forecast uncertainty remains.'},indent=2))
assert all(t['pass'] for t in tests),str([t for t in tests if not t['pass']])
print(len(tests),'checks PASS')
