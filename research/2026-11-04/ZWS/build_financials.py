from pathlib import Path
import json,re
P=Path(__file__).parent;used=[]
def row(file,label,n,last=False):
 used.append(file);matches=[]
 for l in (P/'sources'/file).read_text().splitlines():
  if l.split('|')[0].strip()==label:
   nums=[]
   for v in l.split('|')[1:]:
    v=v.strip().replace(',','')
    if v in ['—','–']:nums.append(0.)
    elif re.fullmatch(r'\(?-?\d+(?:\.\d+)?\)?',v):nums.append(float(v.strip('()'))*(-1 if v.startswith('(') else 1))
   if len(nums)>=n: matches.append(nums[-n:])
 assert matches,(file,label)
 return matches[-1 if last else 0]
def inc(file,n):
 d={k:row(file,l,n,last=k=='eps') for k,l in {'revenue':'Net sales','ebit':'Income from operations','net_income':'Net income from continuing operations','eps':'Continuing operations','shares':'Diluted'}.items()};return [{k:v[i]/(1000 if k=='shares' else 1) for k,v in d.items()} for i in range(n)]
def cf(file,n):
 d={k:row(file,l,n) for k,l in {'cfo':'Cash provided by operating activities','capex':'Expenditures for property, plant and equipment','depreciation':'Depreciation','amortization':'Amortization of intangible assets','sbc':'Stock-based compensation expense'}.items()};return [{k:abs(v[i]) for k,v in d.items()} for i in range(n)]
def diff(a,b):return {k:a[k]-b[k] for k in b}
a=inc('k25_table_18.txt',3);c=cf('k25_table_21.txt',3);annual=[dict(period=f'FY{2025-i}',**a[i],**c[i]) for i in range(3)]
i3=inc('q3_table_10.txt',4);i2=inc('q2_table_10.txt',4);i1=inc('q1_table_10.txt',2);ip=inc('q3prev_table_10.txt',4)
c3=cf('q3_table_12.txt',2);c2=cf('q2_table_12.txt',2);c1=cf('q1_table_12.txt',2);cp=cf('q3prev_table_12.txt',2)
q4={k:a[0][k]-ip[2][k] for k in ['revenue','ebit','net_income']};q4.update(eps=inc('q4_table_1.txt',4)[0]['eps'],shares=inc('q4_table_1.txt',4)[0]['shares'])
quarters=[dict(period='Q4 FY2025',**q4,**diff(c[0],cp[0])),dict(period='Q1 FY2026',**i1[0],**c1[0]),dict(period='Q2 FY2026',**i2[0],**diff(c2[0],c1[0])),dict(period='Q3 FY2026',**i3[0],**diff(c3[0],c2[0]))]
ttm=[]
for j in range(2):
 cur=dict(period='TTM September '+str(2026-j))
 for k in ['revenue','ebit','net_income']:cur[k]=a[j][k]+(i3[2][k] if j==0 else ip[2][k])-(ip[2][k] if j==0 else ip[3][k])
 for k in c[0]:cur[k]=c[j][k]+(c3[0][k] if j==0 else cp[0][k])-(cp[0][k] if j==0 else cp[1][k])
 ttm.append(cur)
for d in annual+quarters+ttm:d.update(fcf=d['cfo']-d['capex'],fcf_less_sbc=d['cfo']-d['capex']-d['sbc'],da=d['depreciation']+d['amortization'])
json.dump(dict(units='USD millions except EPS; diluted shares millions. Net income/EPS continuing operations; CFO consolidated includes undisaggregated discontinued flows.',annual=annual[::-1],quarters=quarters,ttm=ttm[::-1],source_tables=sorted(set(used))),open(P/'financials.json','w'),indent=2)
