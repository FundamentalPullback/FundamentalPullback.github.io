from pathlib import Path
import json,re
P=Path(__file__).parent;used=[]
def row(file,label,n):
 used.append(file)
 for l in (P/'sources'/file).read_text().splitlines():
  if l.split('|')[0].strip()==label:
   nums=[]
   for v in l.split('|')[1:]:
    v=v.strip().replace(',','')
    if v in ['—','–']:nums.append(0.)
    elif re.fullmatch(r'\(?-?\d+(?:\.\d+)?\)?',v):nums.append(float(v.strip('()'))*(-1 if v.startswith('(') else 1))
   assert len(nums)>=n,(file,label,nums)
   return nums[-n:]
 raise ValueError((file,label))
def income(file,n):
 d={k:row(file,l,n) for k,l in {'revenue':'Revenues','ebit':'Operating income','net_income':'Net income','eps':'Diluted earnings per common share','shares':'Diluted weighted average common shares'}.items()};return [{k:v[i]/(1 if k=='eps' else 1000) for k,v in d.items()} for i in range(n)]
def cf(file,n):
 d={k:row(file,l,n) for k,l in {'cfo':'Net cash provided by operating activities','capex':'Purchases of property, equipment, leasehold improvements and capitalized internal-use software','da':'Depreciation and amortization','sbc':'Stock-based compensation expense'}.items()};return [{k:(abs(v[i]) if k=='capex' else v[i])/1000 for k,v in d.items()} for i in range(n)]
a=income('k26_table_26.txt',3);c=cf('k26_table_29.txt',3);annual=[dict(period=f'FY{2026-i}',**a[i],**c[i]) for i in range(3)]
inc1=income('q1_table_7.txt',2);inc2=income('q2_table_7.txt',4);inc3=income('q3_table_7.txt',4);inc4=income('q4_table_4.txt',4)
c1=cf('q1_table_10.txt',2);c2=cf('q2_table_10.txt',2);c3=cf('q3_table_10.txt',2)
def diff(a,b):return {k:a[k]-b[k] for k in b}
quarters=[dict(period='Q1 FY2026',**inc1[0],**c1[0]),dict(period='Q2 FY2026',**inc2[0],**diff(c2[0],c1[0])),dict(period='Q3 FY2026',**inc3[0],**diff(c3[0],c2[0])),dict(period='Q4 FY2026',**inc4[0],**diff(c[0],c3[0]))]
for d in annual+quarters:d.update(fcf=d['cfo']-d['capex'],fcf_less_sbc=d['cfo']-d['capex']-d['sbc'])
out=dict(units='USD millions except EPS; diluted shares millions; TTM ending August31 equals full fiscal year',annual=annual[::-1],quarters=quarters,ttm=[dict(annual[1]),dict(annual[0])],source_tables=sorted(set(used)))
json.dump(out,open(P/'financials.json','w'),indent=2);print(json.dumps(out,indent=2))
