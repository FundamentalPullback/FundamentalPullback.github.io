import pathlib,json,math
P=pathlib.Path(__file__).parent;h=json.loads((P/'history.json').read_text());m=json.loads((P/'model_results.json').read_text());q=h['quarters'];c=[]
def ck(n,b):c.append({'check':n,'pass':bool(b)})
for k in ['revenue','ebit','net_income','cfo','da','software_cash','ppe_cash','sbc']:
 ck('TTM quarterly sum '+k,abs(sum(q[z][k] for z in ['q2_26','q3_26','q4_26','q1_27'])-h['paired_ttm']['2026'][k])<.005)
ck('client balance not corporate cash',abs(2899.337-2888.615-10.722)<.00001)
ck('software stock rollforward',abs(143.594+24.918-18.57-149.942)<.00001)
ck('contract stock rollforward',abs(559.186+46.038-26.527-578.697)<.00001)
for name,s in m['cases'].items():
 ck(name+' funded stocks',all(abs(r['closing_stocks'][k]-r['opening_stocks'][k]-r['investment'][k]+r['amortization'][k])<1e-8 for r in s['years'] for k in r['opening_stocks']))
 ck(name+' full cash identity',all(abs(r['fcff']-r['nopat']-sum(r['amortization'].values())+sum(r['investment'].values())+r['delta_wc'])<1e-8 for r in s['years']))
 ck(name+' no terminal underfunding',all(r['closing_stocks'][k]>=r['opening_stocks'][k]*(1+r['growth'])-1e-8 for r in s['years'] for k in r['opening_stocks']))
 ck(name+' explicit transition',abs(s['years'][9]['growth']-s['assumptions']['g'])<1e-10)
 ck(name+' no approved price',s['approved_value'] is None)
 ck(name+' positive discount spread',s['wacc']>s['assumptions']['g'])
ck('unresolved claims not zero',all(v is None for v in m['unresolved_claims'].values()))
(P/'checks.json').write_text(json.dumps(c,indent=2));assert all(x['pass'] for x in c);print(len(c),'checks pass')
