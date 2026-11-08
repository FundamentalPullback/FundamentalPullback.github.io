import json,pathlib,csv
P=pathlib.Path(__file__).parent;keys=['revenue','operating_income','net_income','cfo','cash_ppe','cashflow_dda']
def row(a):return dict(zip(keys,a))
h={
'FY2023':row([1094.897,17.845,-81.278,245.597,85.306,129.692]),
'FY2024':row([1214.503,76.517,80.394,298.401,159.791,130.662]),
'FY2025':row([1384.562,669.746,583.988,348.632,253.612,115.636]),
'9M2024':row([912.116,186.211,132.892,205.627,114.024,98.836]),
'9M2025':row([983.005,427.481,391.216,245.569,162.461,87.839]),
'Q12026':row([484.694,108.780,79.431,120.094,71.084,34.103]),
'H12026':row([927.406,229.291,151.549,186.274,160.223,68.813]),
'9M2026':row([1427.653,336.067,240.237,329.409,286.244,103.094])}
def diff(a,b):return {k:round(h[a][k]-h[b][k],6) for k in keys}
h['Q42025']=diff('FY2025','9M2025');h['Q22026']=diff('H12026','Q12026');h['Q32026']=diff('9M2026','H12026')
for name,annual,new,old in [('TTM202609','FY2025','9M2026','9M2025'),('TTM202509','FY2024','9M2025','9M2024')]:h[name]={k:round(h[annual][k]+h[new][k]-h[old][k],6) for k in keys}
for k in keys:assert abs(sum(h[q][k] for q in ['Q42025','Q12026','Q22026','Q32026'])-h['TTM202609'][k])<1e-6
for d in h.values():d['cfo_less_cash_ppe']=round(d['cfo']-d['cash_ppe'],6)
(P/'history.json').write_text(json.dumps(h,indent=2))
with (P/'history.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=['period']+list(h['FY2023']));w.writeheader();w.writerows(dict(period=k,**v) for k,v in h.items())
print({k:h[k] for k in ['TTM202609','TTM202509']})
