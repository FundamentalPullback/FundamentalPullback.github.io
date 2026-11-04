import json,pathlib,math
P=pathlib.Path(__file__).resolve().parent
rows=json.load(open(P/'financial_history.json'));d={r['period']:r for r in rows};checks=[]
def check(n,a,b):
 ok=abs(a-b)<1e-6;checks.append({'check':n,'actual':a,'expected':b,'pass':ok});assert ok,(n,a,b)
for r in rows:
 p=r['period'];check(p+' pretax-tax=NI',r['pretax_income']-r['tax'],r['net_income']);check(p+' CFO-capex=FCF',r['cfo']-r['capex'],r['fcf']);check(p+' FCF-SBC',r['fcf']-r['sbc'],r['fcf_after_sbc'])
for y in [2025,2026]:
 for m in ['revenue','cogs','ebit','net_income','cfo','capex','sbc','da','tax','pretax_income','interest_expense','fcf']:
  check(f'FY{y} four quarters {m}',sum(d[f'Q{q}FY{y}'][m] for q in [1,2,3,4]),d[f'FY{y}'][m])
for y in [2026,2027]:
 for m in ['revenue','ebit','net_income','cfo','capex','sbc','da','tax','fcf']:
  check(f'TTM{y} annual roll {m}',d[f'FY{y-1}'][m]-d[f'Q1FY{y-1}'][m]+d[f'Q1FY{y}'][m],d[f'TTM_Q1FY{y}'][m])
for r in rows:
 if r['period'].startswith('TTM'):continue
 for m in ['revenue','ebit','net_income','eps_basic','eps_diluted','cfo','capex','sbc','da']:
  assert r[m] is not None
  if m.startswith('eps'):assert r['provenance'][m]['basis']=='reported'
json.dump(checks,open(P/'validation_checks.json','w'),indent=2);print(f'{len(checks)} arithmetic checks passed; required base metrics complete; all FY/quarter EPS directly reported.')
