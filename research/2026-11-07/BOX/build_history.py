import pathlib,json,re
P=pathlib.Path(__file__).resolve().parent
fields={'revenue':'Revenue','ebit':'Income from operations','ni':'Net income','common_ni':'Net income attributable to common stockholders','pbt':'Income before income taxes','rd':'Research and development','da':'Depreciation and amortization','sbc':'Stock-based compensation expense','commission_amort':'Amortization of deferred commissions','commission_cash':'Deferred commissions','cfo':'Net cash provided by operating activities','capex':'Purchases of property and equipment','software':'Capitalized software costs'}
cfkeys=['da','sbc','commission_amort','commission_cash','cfo','capex','software']
def row(file,label,cf=False):
 rows=json.loads((P/'financial_source_inputs.json').read_text())[file]
 if cf:
  starts=[i for i,r in enumerate(rows) if 'CASH FLOWS FROM OPERATING ACTIVITIES' in r]
  if starts:rows=rows[starts[-1]:]
 if label=='Purchases of property and equipment' and not any(r.startswith(label+' | ') for r in rows):label='Purchases of property and equipment, net of sale proceeds'
 if label=='Capitalized software costs' and not any(r.startswith(label+' | ') for r in rows):label='Capitalized internal-use software costs'
 for r in rows:
  if r.startswith(label+' | ') or r.startswith(label+' (1) | '):
   out=[]
   for v in r.split(' | ')[1:]:
    v=v.strip()
    if re.fullmatch(r'\(?-?[\d,]+(?:\.\d+)?\)?|—|-',v):out.append(0 if v in ['—','-'] else float(v.replace(',','').replace('(','-').replace(')',''))/1000)
   return out
 raise ValueError((file,label))
def read(file,idx,incidx=None):
 d={}
 for k,v in fields.items():
  z=row(file,v,k in cfkeys);i=idx if k in cfkeys or incidx is None else incidx;d[k]=z[i]
  if k in ['capex','software','commission_cash']:d[k]=abs(d[k])
 return d
annual={str(2026-i):read('box-20260131.htm.rows',i) for i in range(3)}
half={str(2026-i):read('box-20260731.htm.rows',i,2+i) for i in range(2)}
old=read('box-20250731.htm.rows',1,3)
ttm={str(y):{k:annual[str(y)][k]+half[str(y)][k]-(half['2025'][k] if y==2026 else old[k]) for k in fields} for y in [2026,2025]}
q3=read('box-20251031.htm.rows',0,0);ytd9=read('box-20251031.htm.rows',0,2)
for k in cfkeys:q3[k]=ytd9[k]-half['2025'][k]
q1=read('box-20260430.htm.rows',0);q2={k:half['2026'][k]-q1[k] for k in fields};q4={k:annual['2026'][k]-ytd9[k] for k in fields}
for d in list(annual.values())+list(ttm.values()):d['cash_after_capex_software_sbc']=d['cfo']-d['capex']-d['software']-d['sbc']
h=dict(units='USD millions; financial statement source amounts in thousands',annual=annual,quarters=dict(Q3FY2026=q3,Q4FY2026=q4,Q1FY2027=q1,Q2FY2027=q2),half_year_july=half,paired_ttm_july=ttm,method='FY plus current H1 less prior H1. Q4=FY-9M, Q2=H1-Q1. Cash-flow software differs from non-GAAP FCF reconciliation; both disclosed, not silently equated.')
(P/'history.json').write_text(json.dumps(h,indent=2)+'\n');print(json.dumps(ttm,indent=2))
