import pathlib,json
P=pathlib.Path(__file__).parent;h=json.loads((P/'history.json').read_text());m=json.loads((P/'model_results.json').read_text());c=[]
def ck(n,b):c.append(dict(check=n,passed=bool(b)))
for k in ['revenue','ebit','net_income','cfo','capex','depreciation','amortization','sbc']:ck('TTM sum '+k,abs(sum(h['quarters'][q][k] for q in ['q4_25','q1_26','q2_26','q3_26'])-h['paired_ttm']['2026'][k])<.01)
ck('FY25 consolidated not segment EBIT',h['annual']['2025']['ebit']==1277)
ck('Q4 depreciation positive',h['quarters']['q4_25']['depreciation']>0)
for n,x in m['cases'].items():
 for k in ['core','cleanwater1']:
  z=x[k];ck(n+k+' funded stock',all(abs(r['closing_stock'][a]-r['opening_stock'][a]-r['investment'][a]+r['da'][a])<1e-8 and r['closing_stock'][a]>=r['opening_stock'][a]*(1+r['g'])-1e-8 for r in z['years'] for a in r['opening_stock']))
  ck(n+k+' cash identity',all(abs(r['fcff']-r['nopat']-sum(r['da'].values())+sum(r['investment'].values())+r['delta_wc'])<1e-8 for r in z['years']))
  ck(n+k+' transition',abs(z['years'][9]['g']-x['assumptions']['g'])<1e-10)
 ck(n+' program funded',abs(sum(r['program_cash'] for r in x['core']['years'])-x['assumptions']['program'])<1e-8)
 ck(n+' acquisition paired',abs(x['conditional_equity']-x['core']['ev']-x['cleanwater1']['ev']-x['bridge'])<1e-8)
 ck(n+' approved null',x['approved_value'] is None)
ck('unknown claims null',all(v is None for v in m['unknowns'].values()))
(P/'checks.json').write_text(json.dumps(c,indent=2));assert all(x['passed'] for x in c);print(len(c),'checks pass')
