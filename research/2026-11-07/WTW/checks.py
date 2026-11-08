import pathlib,json
P=pathlib.Path(__file__).parent;h=json.loads((P/'history.json').read_text());m=json.loads((P/'model_results.json').read_text());c=[]
def ck(n,b):c.append(dict(check=n,pass_=bool(b)))
for k in ['revenue','ebit','net_income','cfo','capex','sbc','depreciation','amortization']:
 ck('TTM sum '+k,abs(sum(h['quarters'][q][k] for q in ['q4_25','q1_26','q2_26','q3_26'])-h['paired_ttm']['2026'][k])<.01)
for name,x in m['cases'].items():
 ck(name+' stock rollforward',all(abs(r['stock_close'][k]-r['stock_open'][k]-r['investment'][k]+r['da'][k])<1e-7 for r in x['years'] for k in r['stock_open']))
 ck(name+' funded expansion and renewal',all(r['stock_close'][k]>=r['stock_open'][k]*(1+r['g'])-1e-7 for r in x['years'] for k in r['stock_open']))
 ck(name+' cash identity',all(abs(r['fcff']-r['nopat']-sum(r['da'].values())+sum(r['investment'].values())+r['delta_wc'])<1e-7 for r in x['years']))
 ck(name+' Propel funding',abs(sum(r['propel_cash_cost'] for r in x['years'])-618)<1e-8)
 ck(name+' explicit transition',abs(x['years'][9]['g']-x['assumptions']['g'])<1e-10)
 ck(name+' discount spread',x['wacc']>x['assumptions']['g'])
 ck(name+' no approved price',x['approved_value'] is None)
ck('unvalued not zero',all(v is None for v in m['unvalued_assets'].values()))
(P/'checks.json').write_text(json.dumps(c,indent=2));assert all(x['pass_'] for x in c);print(len(c),'checks pass')
