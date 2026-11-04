from pathlib import Path
import json,re
P=Path(__file__).parent;used=[]
def row(file,label,n,last=False):
 used.append(file);out=[]
 for l in (P/'sources'/file).read_text().splitlines():
  if l.split('|')[0].strip()==label:
   v=[]
   for a in l.split('|')[1:]:
    a=a.strip().replace(',','')
    if a in ['—','–']:v.append(0.)
    elif re.fullmatch(r'\(?-?\d+(?:\.\d+)?\)?',a):v.append(float(a.strip('()'))*(-1 if a.startswith('(') else 1))
   if len(v)>=n:out.append(v[-n:])
 assert out,(file,label)
 return out[-1 if last else 0]
def match(file,stem):return next(l.split('|')[0].strip() for l in (P/'sources'/file).read_text().splitlines() if l.split('|')[0].strip().startswith(stem))
def inc(file,n):
 labs={'revenue':'Net revenues','operating_income':match(file,'Operating profit'),'net_income':match(file,'Net '+('(loss)' if file.startswith('k25') else 'earnings')+' earnings attributable') if False else next(l.split('|')[0].strip() for l in (P/'sources'/file).read_text().splitlines() if 'attributable to Hasbro, Inc.' in l),'eps':'Diluted','tax':'Income tax expense' if file!='k25_table_16.txt' else 'Income tax expense (benefit)','interest':'Interest expense'}
 d={k:row(file,l,n) for k,l in labs.items()}
 return [{k:v[i] for k,v in d.items()} for i in range(n)]
def cf(file,n):
 labs={'cfo':'Net cash provided by operating activities','ppe':'Additions to property, plant and equipment','software':'Additions to software development','sbc':('Stock-based compensation' if file.startswith('q3prev') else 'Share-based compensation'),'depreciation':'Depreciation of property, plant and equipment','amortization':'Amortization of intangible assets','program_amortization':'Program cost amortization','program_cash':'Program production costs'}
 d={k:row(file,l,n) for k,l in labs.items()}
 for k in ['ppe','software','program_cash']:d[k]=[-v for v in d[k]]
 return [{k:v[i] for k,v in d.items()} for i in range(n)]
a=inc('k25_table_16.txt',3);ac=cf('k25_table_18.txt',3);i3=inc('q3_table_7.txt',4);ip=inc('q3prev_table_7.txt',4);i2=inc('q2_table_7.txt',4);i1=inc('q1_table_7.txt',2);c3=cf('q3_table_9.txt',2);cp=cf('q3prev_table_9.txt',2);c2=cf('q2_table_9.txt',2);c1=cf('q1_table_9.txt',2)
annual=[dict(period=f'FY{2025-i}',**a[i],**ac[i]) for i in range(3)][::-1]
def diff(a,b):return {k:a[k]-b[k] for k in b}
q4=diff(a[0],ip[2]);q4['eps']=row('q4release_table_1.txt','Diluted',4)[0]
quarters=[dict(period='Q4 2025',**q4,**diff(ac[0],cp[0])),dict(period='Q1 2026',**i1[0],**c1[0]),dict(period='Q2 2026',**i2[0],**diff(c2[0],c1[0])),dict(period='Q3 2026',**i3[0],**diff(c3[0],c2[0]))]
ttm=[]
for j in [1,0]:
 d={'period':f'TTM September {2026-j}'}
 for k in a[0]:
  if k!='eps':d[k]=a[j][k]+(i3[2][k] if j==0 else ip[2][k])-(ip[2][k] if j==0 else ip[3][k])
 for k in ac[0]:d[k]=ac[j][k]+(c3[0][k] if j==0 else cp[0][k])-(cp[0][k] if j==0 else cp[1][k])
 ttm.append(d)
for d in annual+quarters+ttm:
 d['capex']=d['ppe']+d['software'];d['fcf']=d['cfo']-d['capex'];d['owner_cash_proxy']=d['fcf']-d['sbc']
json.dump(dict(units='USD millions except per-share EPS. Fiscal 2023 includes eOne through disposal; comparisons are not constant perimeter.',annual=annual,quarters=quarters,ttm=ttm,source_tables=sorted(set(used))),open(P/'financials.json','w'),indent=2)
print(ttm)
