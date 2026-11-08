import json,csv,pathlib
P=pathlib.Path(__file__).parent
keys=['revenue','ebit','net_income','cfo','capex','da','sbc']
def row(v):return dict(zip(keys,v))
h={
'FY2024':row([959.265,111.941,144.300,111.266,24.181,53.876,31.168]),
'FY2025':row([942.734,122.092,37.431,115.297,22.222,57.768,27.694]),
'FY2026':row([1060.784,141.536,66.186,351.435,28.343,56.069,32.439]),
'Q1FY2025':row([138.714,-18.482,-19.321,-27.359,5.905,13.781,6.262]),
'Q1FY2026':row([158.262,-29.739,-21.654,19.808,5.953,14.074,7.293]),
'H1FY2026':row([618.202,134.076,71.061,184.194,14.282,28.058,17.330]),
'9MFY2026':row([864.462,150.177,76.171,368.053,24.245,41.846,24.019]),
'Q1FY2027':row([217.134,9.724,8.909,-26.200,11.981,13.793,9.594])}
def sub(a,b):return {k:round(h[a][k]-h[b][k],6) for k in keys}
h['Q2FY2026']=sub('H1FY2026','Q1FY2026');h['Q3FY2026']=sub('9MFY2026','H1FY2026');h['Q4FY2026']=sub('FY2026','9MFY2026')
for n,a,b,c in [('TTM202609','FY2026','Q1FY2027','Q1FY2026'),('TTM202509','FY2025','Q1FY2026','Q1FY2025')]:h[n]={k:round(h[a][k]+h[b][k]-h[c][k],6) for k in keys}
for k in keys:assert abs(sum(h[q][k] for q in ['Q2FY2026','Q3FY2026','Q4FY2026','Q1FY2027'])-h['TTM202609'][k])<1e-6
for r in h.values():r.update(cfo_less_capex=round(r['cfo']-r['capex'],6),op_margin=r['ebit']/r['revenue'],net_margin=r['net_income']/r['revenue'])
(P/'history.json').write_text(json.dumps(h,indent=2));
with (P/'history.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=['period']+list(h['FY2024']));w.writeheader();w.writerows(dict(period=k,**v) for k,v in h.items())
print(json.dumps({k:h[k] for k in ['TTM202609','TTM202509']},indent=2))
