import pathlib,json,csv,re
p=pathlib.Path(__file__).parent
L={'revenue':'Total revenues','ebit':'Income (loss) from operations','net_parent':'Net income (loss) attributable to Diamondback Energy, Inc.','net_consolidated':'Net income (loss)','cfo':'Net cash provided by (used in) operating activities','capex':'Additions to oil and natural gas properties','dda':'Depreciation, depletion, amortization and accretion','derivative_adjustment':'(Gain) loss on derivative instruments, net','derivative_settlement':'Cash received (paid) on settlement of derivative instruments','nci_dividends':'Dividends to non-controlling interest'}
def rows(g):return json.loads((p/'financial_source_inputs.json').read_text())[g]['rows']
def value(r,label,n):
 for s in r:
  a=s.split(' | ')
  if a[0]!=label and not (label=='Dividends to non-controlling interest' and a[0]=='Dividends/distributions to non-controlling interest'):continue
  b=[0 if v=='—' else float(v.replace(',','').replace('(','-').replace(')','')) for v in a[1:] if re.fullmatch(r'\(?-?[\d,]+(?:\.\d+)?\)?|—',v)]
  if len(b)==n and not (label=='Depreciation, depletion, amortization and accretion' and max(b)<100):return b
 raise ValueError((label,n))
h={};fy=rows('2026-02-25*.rows')
for y,c in [(2025,0),(2024,1),(2023,2)]:h[str(y)]={k:value(fy,l,3)[c] for k,l in L.items()}
for per,g,col in [('9M2026','2026-11-04*.rows',0),('9M2025','2026-11-04*.rows',1),('9M2024','2025-11-05*.rows',1),('H12026','2026-08-05*.rows',0),('Q12026','2026-05-06*.rows',0)]:
 r=rows(g);h[per]={k:value(r,l,4 if k in ['revenue','ebit','net_parent','net_consolidated'] and per!='Q12026' else 2)[col+2 if k in ['revenue','ebit','net_parent','net_consolidated'] and per!='Q12026' else col] for k,l in L.items()}
for per,a,b in [('Q42025','2025','9M2025'),('Q22026','H12026','Q12026'),('Q32026','9M2026','H12026')]:h[per]={k:h[a][k]-h[b][k] for k in L}
for y in [2025,2026]:h['TTM'+str(y)]={k:h[str(y-1)][k]+h['9M'+str(y)][k]-h['9M'+str(y-1)][k] for k in L}
for r in h.values():r['cfo_less_capex']=r['cfo']+r['capex'];r['after_nci_distributions_proxy']=r['cfo_less_capex']+r['nci_dividends']
(p/'history.json').write_text(json.dumps(h,indent=2))
with (p/'history.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=['period']+list(h['2025']));w.writeheader()
 for k,v in h.items():w.writerow({'period':k}|v)
print(json.dumps(h['TTM2026'],indent=2))
