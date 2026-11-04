from pathlib import Path
import json,re
P=Path(__file__).parent;used=[]
def row(file,label,n,last=False):
 used.append(file);matches=[]
 for l in (P/'sources'/file).read_text().splitlines():
  if l.split('|')[0].strip()==label:
   vals=[]
   for v in l.split('|')[1:]:
    v=v.strip().replace(',','')
    if v in ['—','–']:vals.append(0.)
    elif re.fullmatch(r'\(?-?\d+(?:\.\d+)?\)?',v):vals.append(float(v.strip('()'))*(-1 if v.startswith('(') else 1))
   if len(vals)>=n:matches.append(vals[-n:])
 assert matches,(file,label)
 return matches[-1 if last else 0]
def inc(file,n):
 labels={'revenue':'Total revenues','operating_income':'Operating income','net_income':'Net income attributable to shareholders','credit_provision':'Provision for credit losses','operating_interest':'Operating interest','financing_interest':'Financing interest expense, net of financial instruments'}
 
 if file.startswith('q3prev'):labels['net_income']='Net income'
 d={k:row(file,l,n) for k,l in labels.items()};d['eps']=row(file,'Diluted',n);d['shares']=row(file,'Diluted',n,last=True)
 return [{k:v[i] for k,v in d.items()} for i in range(n)]
def cf(file,n):
 lines=(P/'sources'/file).read_text().splitlines();label=next(l.split('|')[0].strip() for l in lines if l.split('|')[0].strip().startswith('Net cash') and 'operating activities' in l)
 d={k:row(file,l,n) for k,l in {'cfo':label,'capex':'Purchases of property, equipment and capitalized software','sbc':'Stock-based compensation','da':'Depreciation and amortization'}.items()};d['capex']=[-v for v in d['capex']]
 return [{k:v[i] for k,v in d.items()} for i in range(n)]
a=inc('k25_table_119.txt',3);ac=cf('k25_table_127.txt',3);i3=inc('q3_table_9.txt',4);ip=inc('q3prev_table_10.txt',4);i2=inc('q2_table_9.txt',4);i1=inc('q1_table_9.txt',2);c3=cf('q3_table_19.txt',2);cp=cf('q3prev_table_20.txt',2);c2=cf('q2_table_19.txt',2);c1=cf('q1_table_18.txt',2)
annual=[dict(period=f'FY{2025-i}',**a[i],**ac[i]) for i in range(3)][::-1]
def diff(x,y):return {k:x[k]-y[k] for k in y}
q4={k:a[0][k]-ip[2][k] for k in a[0] if k not in ['eps','shares']};q4['eps']=row('q4release_table_0.txt','Diluted',4)[0];q4['shares']=row('q4release_table_0.txt','Diluted',4,last=True)[0]
quarters=[dict(period='Q4 2025',**q4,**diff(ac[0],cp[0])),dict(period='Q1 2026',**i1[0],**c1[0]),dict(period='Q2 2026',**i2[0],**diff(c2[0],c1[0])),dict(period='Q3 2026',**i3[0],**diff(c3[0],c2[0]))]
ttm=[]
for j in [1,0]:
 d=dict(period=f'TTM September {2026-j}')
 for k in a[0]:
  if k not in ['eps','shares']:d[k]=a[j][k]+(i3[2][k] if j==0 else ip[2][k])-(ip[2][k] if j==0 else ip[3][k])
 for k in ac[0]:d[k]=ac[j][k]+(c3[0][k] if j==0 else cp[0][k])-(cp[0][k] if j==0 else cp[1][k])
 ttm.append(d)
for d in annual+quarters+ttm:d.update(raw_cfo_less_capex=d['cfo']-d['capex'],raw_cfo_less_capex_sbc=d['cfo']-d['capex']-d['sbc'])
json.dump(dict(units='USD millions except EPS; diluted shares millions. Cash is consolidated and bank financing-sensitive, NOT distributable FCFE.',annual=annual,quarters=quarters,ttm=ttm,source_tables=sorted(set(used))),open(P/'financials.json','w'),indent=2)
print(ttm)
