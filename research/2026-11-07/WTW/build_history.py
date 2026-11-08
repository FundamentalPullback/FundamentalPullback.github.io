import pathlib,json,re
P=pathlib.Path(__file__).parent
labs={'revenue':['Revenue'],'ebit':['Income from operations','Income/(loss) from operations'],'net_income':['NET INCOME/(LOSS) ATTRIBUTABLE TO WTW','NET INCOME ATTRIBUTABLE TO WTW'],'cfo':['Net cash from operating activities','Net cash used in operating activities'],'depreciation':['Depreciation'],'amortization':['Amortization'],'sbc':['Share-based compensation'],'capex':['Additions to fixed assets and software'],'acquisitions':['Acquisitions of operations, net of cash acquired'],'interest':['Interest expense'],'program_cost':['Transaction and program expenses','Transaction and transformation','Transaction and integration expenses'],'restructuring':['Restructuring costs'],'nci_earnings':['Income attributable to non-controlling interests']}
def vals(s):
 s=s.replace(' | )',')');out=[]
 for v in s.split(' | ')[1:]:
  if re.fullmatch(r'\(?[\d,]+(?:\.\d+)?\)?|—',v):out.append(-float(v[1:-1].replace(',','')) if v.startswith('(') else float(v.replace(',','').replace('—','0')))
 return out
def get(file,n=None):
 lines=json.loads((P/'financial_source_inputs.json').read_text())[file];d={}
 for k,names in labs.items():
  for s in lines:
   if s.split(' | ')[0] in names and '%' not in s:
    v=vals(s)
    if (n is None and len(v) in [2,4]) or len(v)==n:d[k]=v;break
 return d
annual=get('2026-02-25_wtw-20251231.htm.rows',3);a={str(y):{k:v[i] for k,v in annual.items()} for i,y in enumerate([2025,2024,2023])}
files={'q3_26':'2026-10-29_wtw-20260930.htm.rows','q2_26':'2026-07-30_wtw-20260630.htm.rows','q1_26':'2026-04-30_wtw-20260331.htm.rows','q3_25':'2025-10-30_wtw-20250930.htm.rows'};raw={k:get(f) for k,f in files.items()};q={k:{z:v[0] for z,v in d.items()} for k,d in raw.items()};flows=['cfo','sbc','capex','acquisitions']
for k in flows:
 for x,y in [('q3_26','q2_26'),('q2_26','q1_26')]:
  if k in q[x] and k in raw[y]:q[x][k]-=raw[y][k][0]
q['q4_25']={k:a['2025'][k]-raw['q3_26'][k][3 if len(raw['q3_26'][k])==4 else 1] for k in a['2025'] if k in raw['q3_26']}
ttm={}
for year,tag in [(2026,'q3_26'),(2025,'q3_25')]:
 ttm[str(year)]={k:a[str(year-1)][k]+v[2 if len(v)==4 else 0]-v[3 if len(v)==4 else 1] for k,v in raw[tag].items() if k in a[str(year-1)]}
for d in list(a.values())+list(q.values())+list(ttm.values()):
 if all(k in d for k in ['cfo','capex','sbc']):d['fcf_gross_capex']=d['cfo']+d['capex'];d['cash_after_sbc']=d['fcf_gross_capex']-d['sbc']
j={'units':'USD millions; cash investment signed negative','annual':a,'quarters':{k:v for k,v in q.items() if k!='q3_25'},'paired_ttm':ttm,'raw':raw,'source_map':files,'warning':'TRANZACT sold 2024-12-31: FY2024 and prior TTM include sold business; 2026 acquisitions not full-year. Reported is not organic.'};(P/'history.json').write_text(json.dumps(j,indent=2));print(json.dumps({'annual':a,'quarters':{k:v for k,v in q.items() if k!='q3_25'},'ttm':ttm},indent=2))
