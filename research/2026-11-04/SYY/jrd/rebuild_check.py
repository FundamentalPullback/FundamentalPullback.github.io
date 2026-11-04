import json,csv,math
from pathlib import Path
P=Path(__file__).resolve().parent;x=json.loads((P/'facts.json').read_text());h=x['historical'];checks=[]
def ck(n,v):checks.append({'check':n,'pass':bool(v)})
for k,v in h.items():
 if k not in ['ebit_margin','effective_tax_rate']:ck(k+' LTM',math.isclose(v[4],v[1]-v[2]+v[3],abs_tol=.00011))
for i,period in enumerate(x['periods']):
 ck(period+' owner cash',math.isclose(h['cfo'][i]-h['capex_cash_outflow'][i],h['cfo_less_capex'][i],abs_tol=.00011))
 ck(period+' EBIT margin',math.isclose(h['ebit'][i]/h['revenue'][i],h['ebit_margin'][i],abs_tol=1e-8))
 ck(period+' tax identity',math.isclose(h['pretax_income'][i]-h['income_tax_expense'][i],h['net_income'][i],abs_tol=.00011))
with (P/'historical_financials.csv').open('w',newline='') as f:
 w=csv.writer(f);w.writerow(['metric']+x['periods'])
 for k,v in h.items():w.writerow([k]+v)
r={'passed':sum(c['pass'] for c in checks),'failed':sum(not c['pass'] for c in checks),'checks':checks};(P/'QA.json').write_text(json.dumps(r,indent=2)+'\n');print(r['passed'],'JRD checks',r['failed'],'failed');assert not r['failed'],[c for c in checks if not c['pass']]
