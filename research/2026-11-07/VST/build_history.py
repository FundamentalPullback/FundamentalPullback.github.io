import pathlib,re,json,csv
P=pathlib.Path(__file__).parent
def rr(g):return json.loads((P/'financial_source_inputs.json').read_text())[g]['rows']
def val(rows,labels,n,positive=False):
 for l in rows:
  if l.split(' | ')[0] not in labels:continue
  a=[]
  for t in l.split(' | ')[1:]:
   if re.fullmatch(r'\(?-?[\d,]+(?:\.\d+)?\)?|—',t):a.append(0 if t=='—' else float(t.replace(',','').replace('(','-').replace(')','')))
  if len(a)==n and (not positive or a[0]>0):return a
 raise ValueError((labels,n))
L={'revenue':['Operating revenues'],'ebit':['Operating income','Operating income (loss)'],'net_common':['Net income attributable to Vistra common stock','Net income (loss) attributable to Vistra common stock'],'cfo':['Cash provided by operating activities'],'capex':['Capital expenditures, including nuclear fuel purchases and LTSA prepayments'],'da_cash':['Depreciation and amortization'],'sbc':['Stock-based compensation expense'],'mtm_commodity_cash_adjustment':['Unrealized net (gain) loss from mark-to-market valuations of commodities'],'margin_deposit_cash_flow':['Margin deposits, net']}
fy=rr('2026-02-27*.rows');r3=rr('release.htm.rows');r2=rr('2026-08-10*.rows');r1=rr('2026-05-08*.rows');old=rr('2025-11-07*.rows')
H={}
for y,c in [(2025,0),(2024,1),(2023,2)]:H[str(y)]={k:val(fy,v,3,k=='da_cash')[c] for k,v in L.items()}
for per,rows,col in [('9M2026',r3,0),('9M2025',r3,1),('9M2024',old,1),('H12026',r2,0),('Q12026',r1,0)]:
 H[per]={k:val(rows,v,2 if per=='Q12026' or k not in ['revenue','ebit','net_common'] else 4,k=='da_cash')[col if per=='Q12026' or k not in ['revenue','ebit','net_common'] else col+2] for k,v in L.items()}
for per,a,b in [('Q42025','2025','9M2025'),('Q22026','H12026','Q12026'),('Q32026','9M2026','H12026')]:H[per]={k:H[a][k]-H[b][k] for k in L}
for y in [2025,2026]:H['TTM'+str(y)]={k:H[str(y-1)][k]+H['9M'+str(y)][k]-H['9M'+str(y-1)][k] for k in L}
for r in H.values():r['cfo_less_capex']=r['cfo']+r['capex'];r['cfo_less_capex_ex_margin']=r['cfo_less_capex']-r['margin_deposit_cash_flow'];r['after_sbc_proxy']=r['cfo_less_capex_ex_margin']-r['sbc']
(P/'history.json').write_text(json.dumps(H,indent=2))
with (P/'history.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=['period']+list(next(iter(H.values()))));w.writeheader()
 for per,r in H.items():w.writerow({'period':per}|r)
print(json.dumps(H,indent=2))
