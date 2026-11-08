import pathlib,re,json,csv
p=pathlib.Path(__file__).parent;s=p/'sources'
def nums(line,n):
 a=[]
 for x in line.split(' | '):
  x=x.strip()
  if re.fullmatch(r'\(?[\d,]+(?:\.\d+)?\)?|—',x):a.append(0 if x=='—' else float(x.replace(',','').replace('(','-').replace(')','')))
 return a[-n:]
def read(pattern,n):
 x=json.loads((p/'financial_source_inputs.json').read_text())[pattern]
 assert x['columns']==n
 return x['data'],x['source']
out=[]
def row(label,d,idx,src):return {'period':label,'source':src,**{k:v[idx]/1000 for k,v in d.items()}}
a24,src24=read('*2025-03-06_0989*fsx2024q4.htm.rows',2);a25,src25=read('*2026-03-05_5324*fsx2025q4.htm.rows',2)
q1,s1=read('*2026-05-04*fsx2026q1.htm.rows',2);h,s2=read('*2026-08-05*fsx2026q2.htm.rows',4);nine,s3=read('*2026-11-02*fsx2026q3.htm.rows',4)
old,so=read('*2025-11-04*fsx2025q3.htm.rows',4)
a24['advances']=[22654,0]
old['advances']=[0,0,50000,0]
out=[row('FY2023',a24,1,src24),row('FY2024',a24,0,src24),row('FY2025',a25,0,src25)]
def diff(label,a,b):return {'period':label,'source':a['source']+' minus '+b['source'],**{k:a[k]-b[k] for k in a if k not in ['period','source'] and k in b}}
out +=[diff('Q4_2025',out[2],row('9M2025',nine,3,s3)),row('Q1_2026',q1,0,s1),row('Q2_2026',h,0,s2),row('Q3_2026',nine,0,s3)]
for label,annual,nw,prior in [('TTM202609',out[2],row('',nine,2,s3),row('',nine,3,s3)),('TTM202509',out[1],row('',old,2,so),row('',old,3,so))]:
 out.append({'period':label,'source':'FY + 9M actual - 9M comparable',**{k:annual[k]+nw[k]-prior[k] for k in annual if k not in ['period','source'] and k in nw and k in prior}})
for r in out:
 r['cfo_less_all_capex']=r['cfo']+r['ppe']+r['exploration']
 r['cash_after_capex_interest_lease_other_and_advance_exclusion']=r['cfo_less_all_capex']+r.get('lease_paid',0)+r.get('interest_paid',0)+r.get('other_finance_paid',0)-r.get('advances',0)
(p/'history.json').write_text(json.dumps(out,indent=2));keys=list(dict.fromkeys(k for r in out for k in r));w=csv.DictWriter((p/'history.csv').open('w'),fieldnames=keys);w.writeheader();w.writerows(out)
print(json.dumps(out,indent=2))
