import pathlib,json,re,csv
P=pathlib.Path(__file__).parent
def rows(g):return json.loads((P/'financial_source_inputs.json').read_text())[g]['rows']
def vals(rr,labels,n):
 for line in rr:
  line=re.sub(r'\(([^|]+) \| \)',r'(\1)',line)
  if line.split(' | ')[0] in labels:
   a=[]
   for t in line.split(' | ')[1:]:
    if re.fullmatch(r'\(?-?[\d,]+(?:\.\d+)?\)?|—',t):a.append(0 if t=='—' else float(t.replace(',','').replace('(','-').replace(')','')))
   if len(a)>=n:return a
 raise ValueError(labels)
L={'revenue':['Total revenues'],'upstream_sales':['Oil, gas and NGL sales'],'pretax':['Earnings before income taxes'],'financing_net':['Financing costs, net'],'net_parent':['Net earnings attributable to Devon'],'cfo':['Net cash from operating activities'],'capex':['Capital expenditures'],'ddna':['Depreciation, depletion and amortization'],'derivatives':['Oil, gas and NGL derivatives'],'dispositions':['Asset dispositions'],'sbc':['Share-based compensation'],'restructuring':['Restructuring and transaction costs']}
FY=rows('2026-02-18*.rows');q3=rows('2026-11-06*.rows');q2=rows('2026-08-05*.rows');q1=rows('2026-05*.rows');old=rows('2025-11*.rows')
H={}
for yr,col in [(2025,0),(2024,1),(2023,2)]:H[str(yr)]={k:vals(FY,v,3)[col] for k,v in L.items()}
for per,rr,col in [('9M2026',q3,2),('9M2025',q3,3),('9M2024',old,3),('H12026',q2,2),('Q12026',q1,0)]:
 H[per]={k:vals(rr,v,4 if col>1 else 2)[col] for k,v in L.items()}
H['9M2024']['restructuring']=8.0 # 2025 Q3 reconciliation table: nine-month restructuring expense8; included in Other net under old presentation.
for per,a,b in [('Q42025','2025','9M2025'),('Q22026','H12026','Q12026'),('Q32026','9M2026','H12026')]:H[per]={k:H[a][k]-H[b][k] for k in L}
for yr in [2025,2026]:H['TTM'+str(yr)]={k:H[str(yr-1)][k]+H['9M'+str(yr)][k]-H['9M'+str(yr-1)][k] for k in L}
for r in H.values():
 r['ebit_proxy']=r['pretax']+r['financing_net'];r['physical_capex']=-r['capex'];r['cfo_less_capex']=r['cfo']+r['capex']
 r['ebit_before_derivatives_disposals']=r['ebit_proxy']-r['derivatives']+r['dispositions']
(P/'history.json').write_text(json.dumps(H,indent=2))
with (P/'history.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=['period']+list(next(iter(H.values()))));w.writeheader()
 for k,v in H.items():w.writerow({'period':k}|v)
print(json.dumps(H,indent=2))
