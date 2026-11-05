from pathlib import Path
import json,csv,math
p=Path(__file__).parent;obs=json.loads((p/'observations.json').read_text());idx={(x['source_file'][:-5],x['metric'],x['start'],x['end']):x for x in obs};metrics=['revenue','ebit','ni_consolidated','ni_parent','eps_diluted','cfo','capex_net_commissioning','da','sbc'];checks=[]
def raw(src,m,s,e):return idx.get((src,m,s,e))
def direct(src,s,e):
 return {m:({'value':x['value'],'status':'direct','observation_ids':[x['id']]} if (x:=raw(src,m,s,e)) else {'value':None,'status':'unavailable'}) for m in metrics}
def combine(label,terms):
 out={}
 for m in metrics:
  if m=='eps_diluted':out[m]={'value':None,'status':'not_derived','reason':'EPS cannot be subtracted across different share/dilution bases'};continue
  vals=[(sign,raw(src,m,s,e)) for sign,src,s,e in terms]
  out[m]={'value':sum(sign*x['value'] for sign,x in vals),'status':'derived','formula':label,'observation_ids':[x['id'] for sign,x in vals]} if all(x for _,x in vals) else {'value':None,'status':'missing_required_input'}
 return out
h={f'FY{y}':direct('annual',f'{y}-01-01',f'{y}-12-31') for y in [2023,2024,2025]}
h['Q42025']=combine('FY2025 minus 9M2025',[(1,'annual','2025-01-01','2025-12-31'),(-1,'q3','2025-01-01','2025-09-30')])
h['Q12026']=direct('q1','2026-01-01','2026-03-31')
for label,src,prev,s,e in [('Q22026','q2','q1','2026-04-01','2026-06-30'),('Q32026','q3','q2','2026-07-01','2026-09-30')]:
 r=direct(src,s,e);d=combine('YTD less previous YTD',[(1,src,'2026-01-01',e),(-1,prev,'2026-01-01','2026-03-31' if src=='q2' else '2026-06-30')])
 for m in metrics:
  if r[m]['value'] is None:r[m]=d[m]
 h[label]=r
for y in [2025,2026]:
 prior=y-1;src='q3' if y==2026 else 'q3_prior'
 h[f'TTM{y}Q3']=combine(f'FY{prior} minus 9M{prior} plus 9M{y}',[(1,'annual',f'{prior}-01-01',f'{prior}-12-31'),(-1,src,f'{prior}-01-01',f'{prior}-09-30'),(1,src,f'{y}-01-01',f'{y}-09-30')])
for period,r in h.items():
 for m in metrics:
  if m!='eps_diluted':assert r[m]['value'] is not None,(period,m)
 r['cfo_less_net_capex']={'value':r['cfo']['value']-r['capex_net_commissioning']['value'],'status':'derived','formula':'Consolidated CFO less PPE cash spending net of commissioning receipts; not owner FCF'}
 r['cfo_less_net_capex_sbc']={'value':r['cfo_less_net_capex']['value']-r['sbc']['value'],'status':'derived','formula':'Previous proxy less CFO-statement SBC; not owner FCF'}
 checks.extend([period+' inputs present',period+' cash subtraction'])
for m in metrics:
 a=raw('q3',m,'2025-01-01','2025-09-30');b=raw('q3_prior',m,'2025-01-01','2025-09-30')
 if a and b:assert a['value']==b['value'],m;checks.append(m+' same prior YTD')
(p/'history.json').write_text(json.dumps(h,indent=2)+'\n');(p/'qa.json').write_text(json.dumps({'passed':len(checks),'checks':checks},indent=2)+'\n')
with (p/'history.csv').open('w') as f:
 w=csv.writer(f);keys=list(h['FY2023']);w.writerow(['period']+keys)
 for per,r in h.items():w.writerow([per]+[r[k]['value'] for k in keys])
print(len(checks),'history checks')
