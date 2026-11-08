import pathlib,json,re
P=pathlib.Path(__file__).parent
labels={'revenue':'Sales','ebit':'Operating profit','net_income':'Net earnings','cfo':'Net cash provided by operating activities','depreciation':'Depreciation','amortization':'Amortization of intangible assets','sbc':'Stock-based compensation expense','capex':'Payments for additions to property, plant and equipment','rd':'Research and development expenses','acquisitions':'Cash paid for acquisitions, net of cash acquired'}
def get(f,n=None):
 out={}
 lines=json.loads((P/'financial_source_inputs.json').read_text())[f]
 if n==3:
  start=max(i for i,x in enumerate(lines) if x=='Sales | $ | 5,503 | $ | 5,193 | $ | 5,021');lines=lines[start:start+150]
 for k,l in labels.items():
  for s in lines:
   if s.split(' | ')[0]!=l or '%' in s:continue
   v=[]
   for x in s.replace(' | )',')').split(' | ')[1:]:
    if re.fullmatch(r'\(?[\d,]+(?:\.\d+)?\)?|—',x):v.append(-float(x[1:-1].replace(',','')) if x.startswith('(') else float(x.replace(',','').replace('—','0')))
   if (n and len(v)==n) or (n is None and len(v) in [2,4]):out[k]=v;break
 return out
an=get('2026-02-20_vlto-20251231.htm.rows',3);a={str(y):{k:v[i] for k,v in an.items()} for i,y in enumerate([2025,2024,2023])};files={'q3_26':'2026-10-30_vlto-20261002.htm.rows','q2_26':'2026-07-29_vlto-20260703.htm.rows','q1_26':'2026-04-29_vlto-20260403.htm.rows','q3_25':'2025-10-29_vlto-20251003.htm.rows'};raw={k:get(f) for k,f in files.items()};q={k:{z:v[0] for z,v in d.items()} for k,d in raw.items()}
for k in ['cfo','sbc','capex','depreciation','amortization','acquisitions']:
 for x,y in [('q3_26','q2_26'),('q2_26','q1_26')]:
  if k in q[x] and k in raw[y]:q[x][k]-=raw[y][k][0]
q['q4_25']={k:a['2025'][k]-raw['q3_26'][k][3 if len(raw['q3_26'][k])==4 else 1] for k in a['2025'] if k in raw['q3_26']};ttm={}
for year,tag in [(2026,'q3_26'),(2025,'q3_25')]:ttm[str(year)]={k:a[str(year-1)][k]+v[2 if len(v)==4 else 0]-v[3 if len(v)==4 else 1] for k,v in raw[tag].items() if k in a[str(year-1)]}
for d in list(a.values())+list(q.values())+list(ttm.values()):
 if all(k in d for k in ['cfo','capex','sbc']):d['fcf']=d['cfo']+d['capex'];d['owner_cash_after_sbc']=d['fcf']-d['sbc']
j={'units':'USD millions; capex and RD outflows negative','annual':a,'quarters':{k:v for k,v in q.items() if k!='q3_25'},'paired_ttm':ttm,'raw':raw,'source_map':files,'history_limit':'FY2023 includes carve-out allocations before September30 Danaher separation; not three full standalone years. Cleanwater1 absent October2 financials.'};(P/'history.json').write_text(json.dumps(j,indent=2));print(json.dumps({'annual':a,'quarters':j['quarters'],'ttm':ttm},indent=2))
