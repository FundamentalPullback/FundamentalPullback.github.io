import pathlib,json,re
P=pathlib.Path(__file__).resolve().parent
fields={'revenue':'Total revenue','ebit':'Operating income','ni':'Net income','dep':'Depreciation','amort':'Amortization','sbc':'Stock-based compensation','cfo':'Net cash provided by operating activities','capex':'Capital expenditures','rental_net_funding':'Uniforms and other rental items in service','combined_prepaid_contract_funding':'Prepaid expenses and other current assets and capitalized contract costs','acquisitions':'Acquisitions of businesses, net of cash acquired'}
cf=set(fields)-{'revenue','ebit','ni'}
def read(file,idx,inc=None,annual=False):
 rows=json.loads((P/'financial_source_inputs.json').read_text())[file];d={}
 for k,label in fields.items():
  rr=rows
  if k in cf:rr=rr[next(i for i,r in enumerate(rr) if r=='Cash flows from operating activities:'):]
  for row in rr:
   if not (row.startswith(label+' | ') or (k=='amort' and row.startswith('Amortization of intangible assets'))):continue
   if '%' in row:continue
   a=[]
   for v in row.split(' | ')[1:]:
    if re.fullmatch(r'\(?[\d,]+(?:\.\d+)?\)?|—',v):a.append(0 if v=='—' else float(v.replace(',','').replace('(','-').replace(')',''))/1000)
   if len(a)>=(3 if annual else (4 if inc is not None and k not in cf else 2)):
    d[k]=a[inc if inc is not None and k not in cf else idx];break
  else:raise ValueError((file,label))
  if k in ['capex','acquisitions','rental_net_funding','combined_prepaid_contract_funding']:d[k]=-d[k]
 return d
ann={str(2026-i):read('ctas-20260531.htm.rows',i,annual=True) for i in range(3)}
q1={str(2027-i):read('ctas-20260831.htm.rows',i) for i in range(2)}
old=read('ctas-20250831.htm.rows',1);h1=read('ctas-20251130.htm.rows',0,2);m9=read('ctas-20260228.htm.rows',0,2)
qs={'Q2FY2026':{k:h1[k]-q1['2026'][k] for k in fields},'Q3FY2026':{k:m9[k]-h1[k] for k in fields},'Q4FY2026':{k:ann['2026'][k]-m9[k] for k in fields},'Q1FY2027':q1['2027']}
ttm={str(y):{k:ann[str(y-1)][k]+q1[str(y)][k]-(q1['2026'][k] if y==2027 else old[k]) for k in fields} for y in [2027,2026]}
for d in list(ann.values())+list(ttm.values())+list(qs.values()):d['owner_cash']=d['cfo']-d['capex']-d['sbc']
(P/'history.json').write_text(json.dumps(dict(units='USD millions',annual=ann,quarters=qs,paired_ttm_august=ttm,method='Audited annuals; Q2=H1-Q1;Q3=9M-H1;Q4=FY-9M;TTM=priorFY+currentQ1-priorQ1. CFO already funds commissions/rental replacement; do not subtract their cash a second time.'),indent=2)+'\n');print(ttm)
