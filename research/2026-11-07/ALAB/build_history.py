import pathlib,json,re
P=pathlib.Path(__file__).resolve().parent
labels={'revenue':['Revenue'],'ebit':['Operating income (loss)','Operating income','Operating loss'],'net_income':['Net income (loss)','Net income','Net loss'],'rd':['Research and development'],'gross_profit':['Gross profit'],'pbt':['Income (loss) before income taxes','Income before income taxes','Loss before income taxes']}
cf={'cfo':['Net cash provided by (used in) operating activities','Net cash provided by operating activities'],'sbc':['Stock-based compensation'],'da':['Depreciation and amortization','Depreciation'],'warrant_contra':['Warrants contra revenue'],'capex':['Purchases of property and equipment'],'ar_cash':['Accounts receivable, net'],'inventory_cash':['Inventory']}
def vals(line):
 a=[]
 for x in line.split(' | ')[1:]:
  x=x.strip().replace(',','')
  if re.fullmatch(r'\(?-?\d+(\.\d+)?\)?',x):a.append(float(x.strip('()'))*(-1 if '(' in x else 1)/1000)
  elif x=='—':a.append(0.)
 return a
def parse(date):
 s=json.loads((P/'financial_source_inputs.json').read_text())[date];cash=s.split('Cash flows from operating activities')[-1]
 inc=s.split('Years Ended December 31,\n2025 | 2024 | 2023')[1] if date=='20251231' else s
 def find(txt,keys):
  a=[l for l in txt.splitlines() if any(l.startswith(k+' | ') for k in keys)]
  if not a:raise ValueError((date,keys))
  return vals(a[0])
 return {k:find(inc,v) for k,v in labels.items()}|{k:find(cash,v) for k,v in cf.items()}
r=parse('20251231');ann={str(y):{k:v[i] for k,v in r.items()} for i,y in enumerate([2025,2024,2023])};q={};cum={}
for d in ['20240331','20240630','20240930','20250331','20250630','20250930','20260331','20260630','20260930']:
 z=parse(d);q[d]={k:v[0] for k,v in z.items()};cum[d]={k:v[2 if len(v)==4 and k in labels else 0] for k,v in z.items()}
for y in [2024,2025,2026]:
 for mo,prev in [('0630','0331'),('0930','0630')]:
  for k in cf:q[f'{y}{mo}'][k]=cum[f'{y}{mo}'][k]-cum[f'{y}{prev}'][k]
for y in [2024,2025]:q[f'{y}1231']={k:ann[str(y)][k]-cum[f'{y}0930'][k] for k in labels|cf}
ttm={str(y):{k:ann[str(y-1)][k]+cum[f'{y}0930'][k]-cum[f'{y-1}0930'][k] for k in labels|cf} for y in [2025,2026]}
for b in [ann,q,ttm]:
 for v in b.values():v['cfo_less_capex']=v['cfo']+v['capex'];v['economic_cash_after_sbc_customer_warrants']=v['cfo']+v['capex']-v['sbc']-v['warrant_contra']
(P/'history.json').write_text(json.dumps({'units':'USD millions; investment outflows negative','annual':ann,'quarters':q,'paired_ttm_september':ttm},indent=2)+'\n');print(ttm)
