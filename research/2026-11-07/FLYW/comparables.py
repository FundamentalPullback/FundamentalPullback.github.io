import pathlib,json,re
P=pathlib.Path(__file__).parent
def row(f,label):
 for l in json.loads((P/'peer_source_inputs.json').read_text())[f]:
  if l.split(' | ')[0]==label:
   return [float(t.replace(',','').replace('(','-').replace(')','')) for t in l.split(' | ')[1:] if re.fullmatch(r'\(?[0-9,]+(?:\.[0-9]+)?\)?',t)]
r=row('peer_PAYO_FY.html.rows','Revenues')[0]+row('peer_PAYO_Q3.html.rows','Revenues')[2]-row('peer_PAYO_Q3.html.rows','Revenues')[3]
eb=row('peer_PAYO_FY.html.rows','Operating income')[0]+row('peer_PAYO_Q3.html.rows','Operating income')[2]-row('peer_PAYO_Q3.html.rows','Operating income')[3]
r/=1000;eb/=1000
h=json.loads((P/'history.json').read_text())['TTM2026']
a=[]
for t,px,sh,cash,rev,ebit in [('PAYO',7.15,340.918977,362.635,r,eb),('FLYW',21.57,122.542824,234.014,h['rev'],h['ebit'])]:
 ev=px*sh-cash
 a.append(dict(ticker=t,price=px,price_date='2026-11-06',shares_date='2026-10-30',shares_m=sh,cash_proxy=cash,limited_enterprise_proxy=ev,revenue_ttm=rev,ebit_ttm=ebit,ev_sales=ev/rev,ev_ebit=ev/ebit,ebit_margin=ebit/rev,period_end='2026-09-30',note='Not full EV: excludes lease-style financing and unquantified claims; all customer assets excluded, no automatic peer target.'))
(P/'comparables.json').write_text(json.dumps(a,indent=2));print(a)
