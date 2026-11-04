from pathlib import Path
import json,re
P=Path(__file__).parent
used=[]
def row(file,label,n,last=False):
 used.append(file);lines=(P/'sources'/file).read_text().splitlines();matches=[l for l in lines if l.split('|')[0].strip()==label];s=matches[-1] if last else matches[0]
 nums=[]
 for v in s.split('|')[1:]:
  v=v.strip().replace(',','')
  if v in ['—','–']:nums.append(0.)
  elif re.fullmatch(r'\(?-?\d+(?:\.\d+)?\)?',v):nums.append(float(v.strip('()'))*(-1 if v.startswith('(') else 1))
 assert len(nums)>=n,(file,label,nums)
 return nums[-n:]
def income(file,n):
 d={k:row(file,l,n,last=k=='shares') for k,l in {'revenue':'Revenues, net','ebit':'Income from operations','net_income':'Net income','eps':'Diluted','shares':'Diluted'}.items()}
 return [{k:v[i]/(1 if k=='eps' else 1e6 if k=='shares' else 1000) for k,v in d.items()} for i in range(n)]
def cf(file,n):
 d={k:row(file,l,n) for k,l in {'cfo':'Net cash provided by operating activities','capex':'Purchases of property and equipment','da':'Depreciation and amortization expense','sbc':'Stock-based compensation expense'}.items()}
 return [{k:(abs(v[i]) if k=='capex' else v[i])/1000 for k,v in d.items()} for i in range(n)]
a=income('k25_table_23.txt',3);c=cf('k25_table_26.txt',3)
annual=[dict(period=f'FY{2025-i}',**a[i],**c[i]) for i in range(3)]
q3=income('q10_table_9.txt',4);q2=income('q2_table_9.txt',4);q1=income('q1_table_9.txt',2);pq3=income('priorq3_table_9.txt',4)
ytd=cf('q10_table_15.txt',2);hy=cf('q2_table_15.txt',2);qy=cf('q1_table_12.txt',2);pytd=cf('priorq3_table_15.txt',2)
def diff(a,b):return {k:a[k]-b[k] for k in a if k not in ['period','shares']}
q4=diff(annual[0],dict(**q3[3],**ytd[1]));q4['eps']=.38 # Actual Q4 release https://ir.exlservice.com/node/23211/pdf, not subtraction of rounded annual EPS
quarters=[dict(period='Q4 FY2025',**q4),dict(period='Q1 FY2026',**q1[0],**qy[0]),dict(period='Q2 FY2026',**q2[0],**diff(hy[0],qy[0])),dict(period='Q3 FY2026',**q3[0],**diff(ytd[0],hy[0]))]
ttm=[]
for yr,ai,inc,newcf,oldinc,oldcf in [(2025,annual[1],pq3[2],pytd[0],pq3[3],pytd[1]),(2026,annual[0],q3[2],ytd[0],q3[3],ytd[1])]:
 d={k:ai[k]+dict(**inc,**newcf)[k]-dict(**oldinc,**oldcf)[k] for k in ['revenue','ebit','net_income','eps','cfo','capex','da','sbc']};ttm.append(dict(period=f'TTM September {yr}',**d))
ttm[1]['eps']=sum(d['eps'] for d in quarters)
for d in annual+quarters+ttm:d.update(fcf=d['cfo']-d['capex'],fcf_less_sbc=d['cfo']-d['capex']-d['sbc'])
out=dict(units='USD millions except EPS; diluted shares millions; quarterly EPS as reported; TTM additive EPS approximate; Q4 FY25 EPS .38 from official FY release',annual=annual[::-1],quarters=quarters,ttm=ttm,source_tables=sorted(set(used)))
json.dump(out,open(P/'financials.json','w'),indent=2);print(json.dumps(out,indent=2))
