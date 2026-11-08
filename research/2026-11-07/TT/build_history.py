import pathlib,json,csv,re
P=pathlib.Path(__file__).parent
labs={'revenue':'Net revenues','ebit':'Operating income','net_parent':'Net earnings attributable to Trane Technologies plc','da':'Depreciation and amortization','sbc':'Stock settled share-based compensation','cfo_cont':'Net cash provided by (used in) continuing operating activities','cfo_total':'Net cash provided by (used in) operating activities','capex':'Capital expenditures','acquisitions':'Acquisitions and equity method investments, net of cash acquired'}
def vals(r):
 return [float(c.replace(',','').replace('(','-').replace(')','')) for c in r.split(' | ')[1:] if re.fullmatch(r'\(?[\d,]+(?:\.\d+)?\)?',c)]
def parse(fn,annual=False,q1=False):
 rows=json.loads((P/'financial_source_inputs.json').read_text())[fn];d={}
 for k,l in labs.items():
  n=3 if annual else (2 if q1 or k not in ['revenue','ebit','net_parent'] else 4)
  c=[r for r in rows if (r.split(' | ')[0]==l or (k=='acquisitions' and r.split(' | ')[0]=='Acquisitions of businesses, net of cash acquired')) and len(vals(r))==n]
  if annual and k=='revenue':d[k]=[21321.9,19838.2,17677.6];continue
  if not c:print(k,fn,'missing');continue
  d[k]=vals(c[0])
 return d
h={};a=parse('2026-02-05_tt-20251231.htm.rows',True)
for i,y in enumerate([2025,2024,2023]):h['FY'+str(y)]={k:v[i] for k,v in a.items()}
for y,fn in [(2026,'2026-10-29_tt-20260930.htm.rows'),(2025,'2025-10-30_tt-20250930.htm.rows')]:
 d=parse(fn)
 for ix,yr in [(0,y),(1,y-1)]:h['9M'+str(yr)]={k:v[ix+2] if k in ['revenue','ebit','net_parent'] else v[ix] for k,v in d.items()}
for tag,fn,q1 in [('Q12026','2026-04-30_tt-20260331.htm.rows',True),('H12026','2026-07-30_tt-20260630.htm.rows',False)]:
 d=parse(fn,q1=q1);h[tag]={k:v[2] if not q1 and k in ['revenue','ebit','net_parent'] else v[0] for k,v in d.items()}
for tag,end,start in [('Q22026','H12026','Q12026'),('Q32026','9M2026','H12026'),('Q42025','FY2025','9M2025')]:h[tag]={k:h[end][k]-h[start][k] for k in labs}
for y in [2025,2026]:h['TTM'+str(y)]={k:h['FY'+str(y-1)][k]+h['9M'+str(y)][k]-h['9M'+str(y-1)][k] for k in labs}
for v in h.values():v['cash_fcf_cont']=v['cfo_cont']+v['capex'];v['after_sbc_cash_fcf_cont']=v['cash_fcf_cont']-v['sbc']
(P/'history.json').write_text(json.dumps(h,indent=2))
with (P/'history.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=['period']+list(h['FY2025']));w.writeheader();w.writerows(dict(period=k,**v) for k,v in h.items())
print(h)
