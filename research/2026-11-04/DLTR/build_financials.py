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
 d={k:row(file,l,n,last=k=='eps') for k,l in {'revenue':'Total revenue','ebit':'Operating income','net_income':'Income from continuing operations','eps':'Continuing operations','shares':'Diluted','tsa':'Transition services agreement income, net'}.items()};return [{k:v[i] for k,v in d.items()} for i in range(n)]
def cf(file,n):
 d={k:row(file,l,n) for k,l in {'cfo':'Net cash provided by operating activities of continuing operations','capex':'Capital expenditures','da':'Depreciation and amortization','sbc':'Stock-based compensation expense'}.items()};return [{k:abs(v[i]) for k,v in d.items()} for i in range(n)]
def diff(a,b):return {k:a[k]-b[k] for k in b}
a=inc('k25_table_35.txt',3);c=cf('k25_table_39.txt',3);annual=[dict(period=f'FY{2025-i}',**a[i],**c[i]) for i in range(3)]
i3=inc('q3prev_table_13.txt',4);i1=inc('q1_table_13.txt',2);i2=inc('q2_table_13.txt',4)
c3=cf('q3prev_table_20.txt',2);c1=cf('q1_table_20.txt',2);c2=cf('q2_table_20.txt',2);cp=cf('q2prev_table_20.txt',2);ip=inc('q2prev_table_13.txt',4)
q4={k:a[0][k]-i3[2][k] for k in ['revenue','ebit','net_income','tsa']};q4.update(eps=row("q4release_table_3.txt","Diluted from continuing operations",4)[0],shares=row("q4release_table_3.txt","Diluted weighted average number of shares",4)[0])
quarters=[dict(period='Q3 FY2025',**i3[0],**diff(c3[0],cp[0])),dict(period='Q4 FY2025',**q4,**diff(c[0],c3[0])),dict(period='Q1 FY2026',**i1[0],**c1[0]),dict(period='Q2 FY2026',**i2[0],**diff(c2[0],c1[0]))]
ttm=[]
for j in range(2):
 cur=dict(period='TTM August '+str(2026-j))
 for k in ['revenue','ebit','net_income','tsa']:cur[k]=a[j][k]+(i2[2][k] if j==0 else ip[2][k])-(ip[2][k] if j==0 else ip[3][k])
 for k in c[0]:cur[k]=c[j][k]+(c2[0][k] if j==0 else cp[0][k])-(cp[0][k] if j==0 else cp[1][k])
 ttm.append(cur)
for d in annual+quarters+ttm:d.update(fcf=d['cfo']-d['capex'],fcf_less_sbc=d['cfo']-d['capex']-d['sbc'])
json.dump(dict(units='USD millions except EPS; diluted shares millions. Continuing operations only, FamilyDollar excluded. FY23 has53weeks.',annual=annual[::-1],quarters=quarters,ttm=ttm[::-1],source_tables=sorted(set(used))),open(P/'financials.json','w'),indent=2)
