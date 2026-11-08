import pathlib,json,csv,re
p=pathlib.Path(__file__).parent
L={'revenue':'Total revenues','ebit':'OPERATING INCOME','net_parent':'NET INCOME ATTRIBUTABLE TO CLASS A COMMON STOCK','net_consolidated':'NET INCOME','cfo':'Net cash provided by operating activities','capex_accrual':'Additions to oil and natural gas properties','capex_wc':'Changes in working capital associated with additions to oil and natural gas properties','dda':'Depreciation, depletion and amortization','sbc':'Stock based compensation','nci_distributions':'Distributions to noncontrolling interest owners'}
def rows(g):return json.loads((p/'financial_source_inputs.json').read_text())[g]['rows']
def value(r,label,n):
 for s in r:
  a=s.split(' | ')
  if a[0]!=label:continue
  b=[0 if v=='—' else float(v.replace(',','').replace('(','-').replace(')',''))/1000 for v in a[1:] if re.fullmatch(r'\(?-?[\d,]+(?:\.\d+)?\)?|—',v)]
  if len(b)==n:return b
 raise ValueError((label,n))
h={};fy=rows('2026-02-12*.rows')
for y,c in [(2025,0),(2024,1),(2023,2)]:h[str(y)]={k:value(fy,l,3)[c] for k,l in L.items()}
for per,g,col in [('9M2026','2026-11-05*.rows',0),('9M2025','2026-11-05*.rows',1),('9M2024','2025-10-30*.rows',1),('H12026','2026-08-06*.rows',0),('Q12026','2026-05-07*.rows',0)]:
 r=rows(g);h[per]={k:value(r,l,4 if k in ['revenue','ebit','net_parent','net_consolidated'] and per!='Q12026' else 2)[col+2 if k in ['revenue','ebit','net_parent','net_consolidated'] and per!='Q12026' else col] for k,l in L.items()}
for per,a,b in [('Q42025','2025','9M2025'),('Q22026','H12026','Q12026'),('Q32026','9M2026','H12026')]:h[per]={k:h[a][k]-h[b][k] for k in L}
for y in [2025,2026]:h['TTM'+str(y)]={k:h[str(y-1)][k]+h['9M'+str(y)][k]-h['9M'+str(y-1)][k] for k in L}
for r in h.values():r['cash_capex']=-(r['capex_accrual']+r['capex_wc']);r['cfo_less_cash_capex']=r['cfo']-r['cash_capex'];r['after_sbc_nci_proxy']=r['cfo_less_cash_capex']-r['sbc']+r['nci_distributions']
(p/'history.json').write_text(json.dumps(h,indent=2))
with (p/'history.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=['period']+list(h['2025']));w.writeheader()
 for k,v in h.items():w.writerow({'period':k}|v)
print(json.dumps(h['TTM2026'],indent=2))
