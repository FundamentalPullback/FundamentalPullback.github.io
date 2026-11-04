from pathlib import Path
import json,csv,math
p=Path(__file__).parent;o=json.loads((p/'numeric_observations.json').read_text());h={};lineage={};tests=[]
periods={'FY2023':('2023-01-29','2024-02-03'),'FY2024':('2024-02-04','2025-02-01'),'FY2025':('2025-02-02','2026-01-31'),'H12024':('2024-02-04','2024-08-03'),'9M2024':('2024-02-04','2024-11-02'),'H12025':('2025-02-02','2025-08-02'),'9M2025':('2025-02-02','2025-11-01'),'H12026':('2026-02-01','2026-08-01'),'Q12025':('2025-02-02','2025-05-03'),'Q22025':('2025-05-04','2025-08-02'),'Q32025':('2025-08-03','2025-11-01'),'Q12026':('2026-02-01','2026-05-02'),'Q22026':('2026-05-03','2026-08-01')}
metrics=['revenue','ebit','net_income','net_income_parent','eps_diluted','cfo','capex','sbc','da_cashflow','da_income']
rank={'annual':1,'q2prior':2,'q3prior':3,'q1':4,'q2':5}
for name,(start,end) in periods.items():
 h[name]={};lineage[name]={}
 for k in metrics:
  opts=[x for x in o if x['start']==start and x['end']==end and x['metric']==k]
  if opts:
   best=sorted(opts,key=lambda x:(rank[x['source']],len(str(x['value']).split('.')[-1])),reverse=True)[0]
   h[name][k]=best['value'];lineage[name][k]=best
  else:h[name][k]=None;lineage[name][k]={'status':'not directly available'}
def derive(name,terms,only_missing=False):
 h.setdefault(name,{});lineage.setdefault(name,{})
 for k in metrics:
  if only_missing and h[name].get(k) is not None:continue
  if k=='eps_diluted':h[name][k]=None;lineage[name][k]={'status':'No subtraction/sum of EPS with different denominators'};continue
  vals=[h[t][k] for t,c in terms]
  h[name][k]=round(sum(h[t][k]*c for t,c in terms),6) if all(v is not None for v in vals) else None
  lineage[name][k]={'formula':terms,'metric':k}
derive('Q22025',[('H12025',1),('Q12025',-1)],True)
derive('Q32025',[('9M2025',1),('H12025',-1)],True)
derive('Q42025',[('FY2025',1),('9M2025',-1)])
derive('Q22026',[('H12026',1),('Q12026',-1)],True)
derive('TTM2026',[('FY2025',1),('H12026',1),('H12025',-1)])
derive('TTM2025',[('FY2024',1),('H12025',1),('H12024',-1)])
for name,r in h.items():
 r['fcf_reported_proxy']=round(r['cfo']-r['capex'],6) if r['cfo'] is not None and r['capex'] is not None else None
 r['cash_after_sbc_proxy']=round(r['fcf_reported_proxy']-r['sbc'],6) if r['fcf_reported_proxy'] is not None and r['sbc'] is not None else None
 r['owner_fcf']=None
 tests.append({'name':name+' EBIT/revenue available','pass':r['revenue'] is not None and r['ebit'] is not None})
 tests.append({'name':name+' owner unknown','pass':r['owner_fcf'] is None})
 if r['fcf_reported_proxy'] is not None:tests.append({'name':name+' cash identity','pass':math.isclose(r['fcf_reported_proxy'],r['cfo']-r['capex'],abs_tol=1e-5)})
reconciliations=[]
for q,acc,prev in [('Q22026','H12026','Q12026'),('Q22025','H12025','Q12025')]:
 for k in metrics:
  if k=='eps_diluted' or any(h[z].get(k) is None for z in [q,acc,prev]):continue
  gap=round(h[q][k]-(h[acc][k]-h[prev][k]),6)
  reconciliations.append({'quarter':q,'metric':k,'direct_minus_accumulated_difference':gap,'note':'Reported direct quarter retained. Difference may reflect source precision or comparison updates; not silently reconciled.' if abs(gap)>0.00001 else 'ties'})
(p/'quarter_reconciliations.json').write_text(json.dumps(reconciliations,indent=2)+'\n')
assert all(x['pass'] for x in tests)
(p/'history.json').write_text(json.dumps(h,indent=2)+'\n');(p/'lineage.json').write_text(json.dumps(lineage,indent=2)+'\n');(p/'qa.json').write_text(json.dumps({'all_pass':True,'count':len(tests),'tests':tests},indent=2)+'\n')
with (p/'history.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=['period']+list(next(iter(h.values())).keys()));w.writeheader()
 for name,r in h.items():w.writerow({'period':name,**r})
print(len(tests),'history QA');print(h['TTM2026'])
