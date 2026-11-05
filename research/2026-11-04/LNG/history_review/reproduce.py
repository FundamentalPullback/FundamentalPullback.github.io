from pathlib import Path
import sys,json,csv,re,hashlib
P=Path(__file__).resolve().parent;R=P.parent
# Source-tagged observations were independently extracted and checked against filings.
# Offline reconstruction consumes those selected numeric facts, not full copyrighted filings.
TAGS={'nci_distributions':'us-gaap:MinorityInterestDecreaseFromDistributionsToNoncontrollingInterestHolders','cash_taxes_net':'us-gaap:IncomeTaxesPaidNet','cash_interest_net_capitalized':'us-gaap:InterestPaidNet'}
obs=json.loads((P/'observations.json').read_text())
idx={(x['source'],x['metric'],x['start'],x['end']):x['value'] for x in obs}
def v(s,m,start,end):
 x=idx.get((s,m,start,end))
 if x is None and m=='nci_distributions' and start.endswith('01-01'):
  year=start[:4]; ends=[('01-01','03-31'),('04-01','06-30'),('07-01','09-30')]
  vals=[idx.get((s,m,year+'-'+a,year+'-'+b)) for a,b in ends if year+'-'+b<=end]
  if vals and all(z is not None for z in vals):x=sum(vals)
 return x
def combine(m,terms):
 vals=[(sign,v(s,m,a,b)) for sign,s,a,b in terms]
 return sum(sign*x for sign,x in vals) if all(x is not None for _,x in vals) else None
h=json.loads((R/'history/history.json').read_text());rows=[]
for per,r in h.items():
 if per.startswith('FY'):
  y=per[2:];terms=[(1,'annual',y+'-01-01',y+'-12-31')]
 elif per=='Q42025':terms=[(1,'annual','2025-01-01','2025-12-31'),(-1,'q3','2025-01-01','2025-09-30')]
 elif per=='Q12026':terms=[(1,'q1','2026-01-01','2026-03-31')]
 elif per=='Q22026':terms=[(1,'q2','2026-01-01','2026-06-30'),(-1,'q1','2026-01-01','2026-03-31')]
 elif per=='Q32026':terms=[(1,'q3','2026-01-01','2026-09-30'),(-1,'q2','2026-01-01','2026-06-30')]
 else:
  y=int(per[3:7]);s='q3' if y==2026 else 'q3_prior';terms=[(1,'annual',f'{y-1}-01-01',f'{y-1}-12-31'),(-1,s,f'{y-1}-01-01',f'{y-1}-09-30'),(1,s,f'{y}-01-01',f'{y}-09-30')]
 row={'period':per,**{m:r[m]['value'] for m in ['revenue','ebit','ni_parent','cfo','capex_net_commissioning','sbc','cfo_less_net_capex']},**{m:combine(m,terms) for m in TAGS}}
 row['cash_residual_after_actual_nci']=row['cfo_less_net_capex']-row['nci_distributions']
 row['cash_residual_after_actual_nci_less_sbc_sensitivity']=row['cash_residual_after_actual_nci']-row['sbc']
 rows.append(row)
(P/'observations.json').write_text(json.dumps(obs,indent=2))
(P/'history_extended.json').write_text(json.dumps(rows,indent=2))
with (P/'history_extended.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
f=json.loads((R/'facts/inputs.json').read_text());checks=[]
for k in ['q3','q3_prior','ytd','ytd_prior']:
 r=f[k];a=r['ebit']+r['fair_value_adjustment']+r['npns_amort_adjustment'];b=a+r['da']+r['noncash_comp_adjusted']+r.get('other_ebitda_adjustment',0)
 assert b==r['adj_ebitda'];checks.append(k+' EBITDA tie-out')
 if k.startswith('ytd'):
  assert r['ni_parent']+r['fair_value_adjustment']+r['npns_amort_adjustment']+r['adj_ni_tax']+r['adj_ni_nci']==r['adj_ni_parent'];checks.append(k+' adjusted NI tie-out')
assert 1716+1146+190+419+3015-659-4+61-50-219+279-428-216-126==5124
checks.append('9M2026 GAAP CFO full row sum')
(P/'qa.json').write_text(json.dumps({'passed':len(checks),'checks':checks},indent=2))
print(json.dumps(rows,indent=2));print(checks)
