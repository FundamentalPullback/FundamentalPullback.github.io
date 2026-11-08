import pathlib,json,re
P=pathlib.Path(__file__).resolve().parent
fields={'revenue':'Net sales','ebit':'Earnings before interest and taxes','ni':'Net earnings attributable to The Campbell\'s Company','da':'Depreciation and amortization','sbc':'Stock-based compensation','cfo':'Net cash provided by operating activities','capex':'Purchases of plant assets','route_buy':'Purchases of routes','route_sell':'Sales of routes','finance_principal':'Financing cash flows from finance leases'}
cf={'da','sbc','cfo','capex','route_buy','route_sell','finance_principal'}
def read(file,idx,inc=None,annual=False):
 rows=json.loads((P/'financial_source_inputs.json').read_text())[file];d={}
 for k,label in fields.items():
  rr=rows
  if k in cf:rr=rr[next(i for i,r in enumerate(rr) if r=='Cash flows from operating activities:'):]
  for r in rr:
   if not r.startswith(label+' | '):continue
   a=[]
   for v in r.split(' | ')[1:]:
    if re.fullmatch(r'\(?[\d,]+(?:\.\d+)?\)?|—',v):a.append(0 if v=='—' else float(v.replace(',','').replace('(','-').replace(')','')))
   if len(a)>=(3 if annual else (4 if inc is not None and k not in cf else 2)):
    d[k]=a[inc if inc is not None and k not in cf else idx];break
  else:raise ValueError((file,label))
  if k in ['capex','route_buy']:d[k]=abs(d[k])
 return d
ann={str(2026-i):read('cpb-20260802.htm.rows',i,annual=True) for i in range(3)}
q1=read('cpb-20251102.htm.rows',0);h1=read('cpb-20260201.htm.rows',0,2);m9=read('cpb-20260503.htm.rows',0,2)
qs={'Q12026':q1,'Q22026':{k:h1[k]-q1[k] for k in fields},'Q32026':{k:m9[k]-h1[k] for k in fields},'Q42026':{k:ann['2026'][k]-m9[k] for k in fields}}
for d in list(ann.values())+list(qs.values()):d['owner_cash']=d['cfo']-d['capex']-d['sbc']-d['route_buy']+d['route_sell']-d['finance_principal']
h={'units':'USD millions','annual':ann,'quarters':qs,'paired_ttm':{y:ann[y] for y in ['2026','2025']},'method':'TTM at fiscal year end equals audited annual. FY2025 53 weeks, FY2024 and FY2026 52. Q2=H1-Q1, Q3=9M-H1, Q4=FY-9M. Perimeter not constant: Sovos acquired March2024, LaRegina consolidated May2026.'}
(P/'history.json').write_text(json.dumps(h,indent=2)+'\n');print(h)
