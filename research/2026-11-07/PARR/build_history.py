import pathlib,json,re
P=pathlib.Path(__file__).parent
labels={'revenue':['Revenues'],'ebit':['Operating income','Operating income (loss)'],'net_income':['Net income (loss) attributable to Par Pacific stockholders','Net income attributable to Par Pacific stockholders','Net income'],'cfo':['Net cash provided by operating activities','Net cash provided by (used in) operating activities','Net cash used in operating activities'],'da':['Depreciation and amortization'],'sbc':['Stock-based compensation'],'capex':['Capital expenditures'],'turnaround_cash':['Deferred turnaround expenditures']}
def get(f,n=None):
 lines=json.loads((P/'financial_source_inputs.json').read_text())[f];out={}
 if n==3:
  start=max(i for i,x in enumerate(lines) if x.startswith('Revenues | $ | 7,464,650 | $ | 7,974,457'));lines=lines[start:start+125]
 for k,ls in labels.items():
  if k=='net_income' and any(x.split(' | ')[0].lower() in [z.lower() for z in ls[:-1]] for x in lines): ls=ls[:-1]
  for s in lines:
   if s.split(' | ')[0].lower() not in [l.lower() for l in ls]:continue
   v=[]
   for x in s.split(' | ')[1:]:
    if re.fullmatch(r'\(?[\d,]+(?:\.\d+)?\)?|—',x):v.append((-float(x[1:-1].replace(',','')) if x.startswith('(') else float(x.replace(',','').replace('—','0')))/1000)
   if len(v)==n or (n is None and len(v) in [2,4]):out[k]=v;break
 return out
an=get('2026-02-25_parr-20251231.htm.rows',3);a={str(y):{k:v[i] for k,v in an.items()} for i,y in enumerate([2025,2024,2023])};files={'q3_26':'2026-11-04_parr-20260930.htm.rows','q2_26':'2026-08-05_parr-20260630.htm.rows','q1_26':'2026-05-06_parr-20260331.htm.rows','q3_25':'2025-11-05_parr-20250930.htm.rows'};raw={k:get(f) for k,f in files.items()};q={k:{z:v[0] for z,v in d.items()} for k,d in raw.items()}
for k in ['cfo','sbc','capex','turnaround_cash']:
 for x,y in [('q3_26','q2_26'),('q2_26','q1_26')]:
  if k in q[x] and k in raw[y]:q[x][k]-=raw[y][k][0]
q['q4_25']={k:a['2025'][k]-raw['q3_26'][k][3 if len(raw['q3_26'][k])==4 else 1] for k in a['2025'] if k in raw['q3_26']};ttm={}
for yr,tag in [(2026,'q3_26'),(2025,'q3_25')]:ttm[str(yr)]={k:a[str(yr-1)][k]+v[2 if len(v)==4 else 0]-v[3 if len(v)==4 else 1] for k,v in raw[tag].items() if k in a[str(yr-1)]}
for d in list(a.values())+list(q.values())+list(ttm.values()):
 if all(k in d for k in ['cfo','capex','sbc']):d['fcf_after_turnarounds']=d['cfo']+d['capex'];d['owner_cash_after_sbc']=d['fcf_after_turnarounds']-d['sbc']
j={'units':'USD millions; outflows negative; turnaround cash already in CFO, do not deduct twice','annual':a,'quarters':{k:v for k,v in q.items() if k!='q3_25'},'paired_ttm':ttm,'raw':raw,'source_map':files,'perimeter':'2023 Montana acquired June1: not full current perimeter. Renewables commercial April2026,63.5% consolidated; Q3 presentation recasts 2026. Laramie pending disposal not closed.'};(P/'history.json').write_text(json.dumps(j,indent=2));print(json.dumps(j,indent=2))
