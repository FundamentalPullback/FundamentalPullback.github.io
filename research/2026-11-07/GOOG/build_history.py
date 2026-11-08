import pathlib,json,csv,re
P=pathlib.Path(__file__).parent
labs={'revenue':'Revenues','ebit':'Income from operations','net':'Net income','depreciation':'Depreciation of property and equipment','sbc':'Stock-based compensation expense','cfo':'Net cash provided by operating activities','capex':'Purchases of property and equipment'}
def vals(s):
 out=[]
 for c in s.split(' | ')[1:]:
  if re.fullmatch(r'\(?[0-9,]+\)?',c):out.append(float(c.replace(',','').replace('(','-').replace(')','')))
 return out
def dat(fn,annual=False):
 rows=json.loads((P/'financial_source_inputs.json').read_text())[fn];o={}
 for k,l in labs.items():
  c=[r for r in rows if r.split(' | ')[0]==l]
  if annual:c=[r for r in c if len(vals(r))==3]
  else:
   if k in ['revenue','ebit','net']:c=[r for r in c if len(vals(r))==4]
   else:c=[r for r in c if len(vals(r))==2]
  o[k]=vals(c[0])
 return o
h={};a=dat('annual.htm.rows',True)
for i,y in enumerate([2023,2024,2025]):h['FY'+str(y)]={k:v[i] for k,v in a.items()}
for y,fn in [(2026,'current_10q.htm.rows'),(2025,'2025-10-30_goog-20250930.htm.rows')]:
 d=dat(fn)
 for i,period in [(2,'9M'+str(y-1)),(3,'9M'+str(y))]:h[period]={k:v[i] if k in ['revenue','ebit','net'] else v[i-2] for k,v in d.items()}
 h['Q3'+str(y)]={k:v[1] for k,v in d.items() if k in ['revenue','ebit','net']}
# Q1 filing has two income columns, distinct parser
rows=json.loads((P/'financial_source_inputs.json').read_text())['2026-04-30_goog-20260331.htm.rows'];h['Q12026']={k:vals(next(r for r in rows if r.split(' | ')[0]==l and len(vals(r))==2))[1] for k,l in labs.items()}
d=dat('2026-07-23_goog-20260630.htm.rows');h['H12026']={k:v[3] if k in ['revenue','ebit','net'] else v[1] for k,v in d.items()}
h['Q22026']={k:h['H12026'][k]-h['Q12026'][k] for k in labs};h['Q32026']={k:h['9M2026'][k]-h['H12026'][k] for k in labs}
h['Q42025']={k:h['FY2025'][k]-h['9M2025'][k] for k in labs}
for y in [2025,2026]:h['TTM'+str(y)]={k:h['FY'+str(y-1)][k]+h['9M'+str(y)][k]-h['9M'+str(y-1)][k] for k in labs}
for x in h.values():
 if 'cfo'in x:x['cash_fcf']=x['cfo']+x['capex'];x['after_sbc_cash_fcf']=x['cash_fcf']-x['sbc']
(P/'history.json').write_text(json.dumps(h,indent=2))
with (P/'history.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=['period']+list(h['FY2025']));w.writeheader();w.writerows(dict(period=k,**v) for k,v in h.items())
print(json.dumps(h,indent=2))
