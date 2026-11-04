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
 d={k:row(file,l,n,last=k=='shares') for k,l in {'revenue':'Net sales','ebit':'Operating income','net_income':'Net income','eps':'Diluted','shares':'Diluted'}.items()};return [{k:v[i]/(1 if k=='eps' else 1000) for k,v in d.items()} for i in range(n)]
def cf(file,n):
 d={k:row(file,l,n) for k,l in {'cfo':'Net cash provided by operating activities','capex':'Purchases of property, plant and equipment','depreciation':'Depreciation','amortization':'Amortization of intangible assets','sbc':'Share-based compensation expense'}.items()};return [{k:abs(v[i])/1000 for k,v in d.items()} for i in range(n)]
def diff(a,b):return {k:a[k]-b[k] for k in b}
a=inc('k26_table_24.txt',3);c=cf('k26_table_27.txt',3);annual=[dict(period=f'FY{2026-i}',**a[i],**c[i]) for i in range(3)]
i3=inc('q3prev_table_4.txt',4);i1=inc('q1_table_4.txt',2);i2=inc('q2_table_4.txt',4)
c3=cf('q3prev_table_7.txt',2);c1=cf('q1_table_7.txt',2);c2=cf('q2_table_7.txt',2);cp=cf('q2prev_table_7.txt',2);ip=inc('q2prev_table_4.txt',4)
q4={k:a[0][k]-i3[2][k] for k in ['revenue','ebit','net_income']};q4.update(eps=inc('q4_table_1.txt',4)[0]['eps'],shares=inc('q4_table_1.txt',4)[0]['shares'])
quarters=[dict(period='Q3 FY2026',**i3[0],**diff(c3[0],cp[0])),dict(period='Q4 FY2026',**q4,**diff(c[0],c3[0])),dict(period='Q1 FY2027',**i1[0],**c1[0]),dict(period='Q2 FY2027',**i2[0],**diff(c2[0],c1[0]))]
ttm=[]
for j in range(2):
 cur= dict(period='TTM September '+str(2026-j))
 for k in ['revenue','ebit','net_income']:cur[k]=a[j][k]+(i2[2][k] if j==0 else ip[2][k])-(ip[2][k] if j==0 else ip[3][k])
 for k in c[0]:cur[k]=c[j][k]+(c2[0][k] if j==0 else cp[0][k])-(cp[0][k] if j==0 else cp[1][k])
 ttm.append(cur)
for d in annual+quarters+ttm:d.update(fcf=d['cfo']-d['capex'],fcf_less_sbc=d['cfo']-d['capex']-d['sbc'],da=d['depreciation']+d['amortization'])
json.dump(dict(units='USD millions; EPS USD; diluted shares millions. Q4 EPS/shares direct quarterly release, not annual minus YTD.',annual=annual[::-1],quarters=quarters,ttm=ttm[::-1],source_tables=sorted(set(used))),open(P/'financials.json','w'),indent=2)
