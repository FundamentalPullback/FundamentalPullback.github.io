import pathlib,json,re
P=pathlib.Path(__file__).resolve().parent
fields={'revenue':'Revenues','ebit':'Income from operations','ni':'Net income','pbt':'Income before income taxes','da':'Depreciation and amortization expenses','sbc':'Stock-based compensation','cfo':'Cash provided by operating activities','capex':'Additions to property and equipment','intangibles':'Additions to intangible assets','preopening':'Preopening costs','acq_charge':'Acquisition-related contingent consideration, compensation and amortization'}
cf=['sbc','cfo','capex','intangibles']
def row(file,label,mincols,iscf=False):
 rows=json.loads((P/'financial_source_inputs.json').read_text())[file]
 if iscf:
  i=next(i for i,r in enumerate(rows) if r.startswith('Cash flows from operating activities:'));rows=rows[i:]
 for r in rows:
  if r.startswith(label+' | ') or (label.endswith('amortization') and r.startswith(label)):
   if '%' in r:continue
   a=[]
   for v in r.split(' | ')[1:]:
    v=v.replace('\u200b','').strip()
    if re.fullmatch(r'\(?-?[\d,]+(?:\.\d+)?\)?|—|-',v):a.append(0 if v in ['—','-'] else float(v.replace(',','').replace('(','-').replace(')',''))/1000)
   if len(a)>=mincols:return a
 raise ValueError((file,label))
def read(file,idx,inc=None,annual=False):
 d={}
 for k,v in fields.items():
  a=row(file,v,3 if annual else (2 if k in cf else (4 if inc is not None else 2)),k in cf);d[k]=a[idx if k in cf or inc is None else inc]
  if k in ['capex','intangibles']:d[k]=abs(d[k])
 return d
annual={str(2025-i):read('cake-20251230x10k.htm.rows',i,annual=True) for i in range(3)}
ytd={str(2026-i):read('cake-20260929x10q.htm.rows',i,2+i) for i in range(2)}
old=read('cake-20250930x10q.htm.rows',1,3)
ttm={str(y):{k:annual[str(y-1)][k]+ytd[str(y)][k]-(ytd['2025'][k] if y==2026 else old[k]) for k in fields} for y in [2026,2025]}
q1=read('cake-20260331x10q.htm.rows',0);h1=read('cake-20260630x10q.htm.rows',0,2)
qs=dict(Q42025={k:annual['2025'][k]-ytd['2025'][k] for k in fields},Q12026=q1,Q22026={k:h1[k]-q1[k] for k in fields},Q32026={k:ytd['2026'][k]-h1[k] for k in fields})
for d in list(annual.values())+list(ttm.values()):d['cash_after_capex_intangibles_sbc']=d['cfo']-d['capex']-d['intangibles']-d['sbc']
h=dict(units='USD millions, original statements thousands',annual=annual,quarters=qs,ytd_september=ytd,paired_ttm_september=ttm,method='Annual comparative audited columns; Q4=FY-prior9M; Q2=H1-Q1; Q3=9M-H1; TTM=priorFY+current9M-prior9M.')
(P/'history.json').write_text(json.dumps(h,indent=2)+'\n');print(json.dumps(ttm,indent=2))
