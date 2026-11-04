"""Rebuild selected history from observations only. No network or source documents required."""
from pathlib import Path
import json,csv
D=Path(__file__).resolve().parent
O=json.loads((D/'observations.json').read_text())
METRICS=['revenue','ebit','net_income_consolidated','net_income_parent','net_income_nci','cfo','gross_capex','cash_turnaround','sbc','da','cash_taxes','income_tax','net_interest','return_of_equity_investment','change_tax_payable','change_other_operating_liabilities']
def get(m,s,e,source=None):
 a=[o for o in O if o['metric']==m and not o['dimensions'] and o.get('start')==s and o.get('end')==e and (source is None or o['source']==source)]
 if not a:return {'value':None,'observation_ids':[],'source_urls':[],'method':'not available'}
 # Fiscal-year filing first for full-year; most recent quarterly filing for comparative YTD.
 priority={'q326':0,'q226':1,'q126':2,'fy25':3,'q325':4}
 a.sort(key=lambda o:priority[o['source']]);x=a[0]
 return {'value':x['value'],'observation_ids':[x['observation_id']],'source_urls':[x['source_url']],'method':'reported'}
def calc(terms,method):
 return {'value':None if any(t['value'] is None for _,t in terms) else round(sum(w*t['value'] for w,t in terms),6),'observation_ids':list(dict.fromkeys(i for _,t in terms for i in t['observation_ids'])),'source_urls':list(dict.fromkeys(u for _,t in terms for u in t['source_urls'])),'method':method}
def period(label,s,e,formula=None):
 r={'period':label,'start':s,'end':e,'unit':'USD million','metrics':{}}
 for m in METRICS:
  direct=get(m,s,e)
  if direct['value'] is not None:r['metrics'][m]=direct
  elif formula:r['metrics'][m]=calc([(w,get(m,a,b)) for w,a,b in formula],' + '.join(f'{w}*{a}/{b}' for w,a,b in formula))
  else:r['metrics'][m]=direct
 for name,terms in {'fcf_after_turnaround':[(1,'cfo'),(-1,'gross_capex'),(-1,'cash_turnaround')],'fcf_after_turnaround_and_sbc':[(1,'cfo'),(-1,'gross_capex'),(-1,'cash_turnaround'),(-1,'sbc')],'company_fcf':[(1,'cfo'),(-1,'gross_capex'),(-1,'cash_turnaround'),(1,'return_of_equity_investment')]}.items():
  r['metrics'][name]=calc([(w,r['metrics'][m]) for w,m in terms],' + '.join(f'{w}*{m}' for w,m in terms))
 return r
R=[period('FY'+str(y),f'{y}-01-01',f'{y}-12-31') for y in [2023,2024,2025]]
R += [period('Q4 2025','2025-10-01','2025-12-31',[(1,'2025-01-01','2025-12-31'),(-1,'2025-01-01','2025-09-30')]),period('Q1 2026','2026-01-01','2026-03-31'),period('Q2 2026','2026-04-01','2026-06-30',[(1,'2026-01-01','2026-06-30'),(-1,'2026-01-01','2026-03-31')]),period('Q3 2026','2026-07-01','2026-09-30',[(1,'2026-01-01','2026-09-30'),(-1,'2026-01-01','2026-06-30')])]
R += [period('TTM Sep 2026','2025-10-01','2026-09-30',[(1,'2025-01-01','2025-12-31'),(1,'2026-01-01','2026-09-30'),(-1,'2025-01-01','2025-09-30')]),period('TTM Sep 2025','2024-10-01','2025-09-30',[(1,'2024-01-01','2024-12-31'),(1,'2025-01-01','2025-09-30'),(-1,'2024-01-01','2024-09-30')])]
(D/'history.json').write_text(json.dumps({'units':'USD million','periods':R,'scope':'Consolidated historical GAAP, before pending acquisition or equity financing. Cash flow includes 100% of UAN; not wholly attributable to CVI common holders.'},indent=2)+'\n')
with (D/'history.csv').open('w') as f:
 w=csv.writer(f);ms=list(R[0]['metrics']);w.writerow(['period','start','end']+ms)
 for r in R:w.writerow([r['period'],r['start'],r['end']]+[r['metrics'][m]['value'] for m in ms])
# Preserve segment disclosures without summing across overlapping product/consolidation axes.
S=[o for o in O if 'us-gaap:StatementBusinessSegmentsAxis' in o['dimensions'] and o['metric'] in ['revenue','ebit','da','segment_capex_accrual','cash','book_debt_including_finance_leases','cash_turnaround'] and len(o['dimensions'])<=2]
(D/'segment_observations.json').write_text(json.dumps({'warning':'Segment accrual capex excludes capitalized turnarounds; not cash capex. 2026 removes Renewables as a separate reportable segment. Preserve every dimension and use the chosen filing basis; do not add overlapping rows.','observations':S},indent=2)+'\n')
print((D/'history.csv').read_text())

def segget(m,seg,s,e,source=None):
 a=[]
 for o in O:
  d=o['dimensions']
  if o['metric']!=m or o.get('start')!=s or o.get('end')!=e or d.get('us-gaap:StatementBusinessSegmentsAxis')!='cvi:'+seg+'SegmentMember':continue
  if source and o['source']!=source:continue
  if d.get('srt:ConsolidationItemsAxis')!='us-gaap:OperatingSegmentsMember':continue
  if 'srt:ProductOrServiceAxis' in d and d['srt:ProductOrServiceAxis']!='cvi:ProductSalesExcludingCreditFromRenewableFuelActivityMember':continue
  a.append(o)
 if not a:return {'value':None,'observation_ids':[],'source_urls':[],'method':'not available'}
 a.sort(key=lambda o:{'q326':0,'q226':1,'q126':2,'fy25':3,'q325':4}[o['source']]);x=a[0]
 return {'value':x['value'],'observation_ids':[x['observation_id']],'source_urls':[x['source_url']],'method':'reported segment total; includes intersegment sales where applicable'}
SEG=[]
for r in R:
 for seg in ['Petroleum','NitrogenFertilizer']:
  rr={'period':r['period'],'segment':seg,'unit':'USD million','metrics':{}}
  for m in ['revenue','ebit','da','segment_capex_accrual']:
   v=segget(m,seg,r['start'],r['end'])
   if v['value'] is None:
    if r['period']=='Q4 2025':terms=[(1,'2025-01-01','2025-12-31'),(-1,'2025-01-01','2025-09-30')]
    elif r['period']=='TTM Sep 2026':terms=[(1,'2025-01-01','2025-12-31'),(1,'2026-01-01','2026-09-30'),(-1,'2025-01-01','2025-09-30')]
    elif r['period']=='TTM Sep 2025':terms=[(1,'2024-01-01','2024-12-31'),(1,'2025-01-01','2025-09-30'),(-1,'2024-01-01','2024-09-30')]
    else:terms=[]
    if terms:v=calc([(w,segget(m,seg,s,e)) for w,s,e in terms],' + '.join(f'{w}*{s}/{e}' for w,s,e in terms))
   rr['metrics'][m]=v
  SEG.append(rr)
(D/'segment_history.json').write_text(json.dumps({'warning':'Includes reportable Petroleum and Nitrogen only, not former Renewables/corporate/eliminations. Revenue includes intersegment sales; capex is accrual additions excluding turnarounds, NOT cash flow capex. TTM segment definition follows reported disclosures with Renewables left outside Petroleum.','periods':SEG},indent=2)+'\n')
with (D/'segment_history.csv').open('w') as f:
 w=csv.writer(f);ms=['revenue','ebit','da','segment_capex_accrual'];w.writerow(['period','segment']+ms)
 for r in SEG:w.writerow([r['period'],r['segment']]+[r['metrics'][m]['value'] for m in ms])
N=json.loads((D/'normalizations.json').read_text())['adjustment_observations']
def nf(p,m):
 a=[x for x in N if x['period']==p and x['metric']==m]
 if not a:return None
 return a[0]['value']
X=[]
for r in R:
 s=next(s for s in SEG if s['period']==r['period'] and s['segment']=='NitrogenFertilizer')
 z={'period':r['period'],'ex_uan_ebit':calc([(1,r['metrics']['ebit']),(-1,s['metrics']['ebit'])],'Consolidated EBIT minus UAN EBIT'), 'ex_uan_da':calc([(1,r['metrics']['da']),(-1,s['metrics']['da'])],'Consolidated D&A minus UAN D&A')}
 z['ex_uan_ebit_plus_da']=calc([(1,z['ex_uan_ebit']),(1,z['ex_uan_da'])],'ex-UAN EBIT plus D&A; includes corporate and former renewables')
 X.append(z)
for z in X:
 p=z['period'];terms=[(1,p)] if p.startswith('FY') else [(1,'FY2025'),(1,'9M2026'),(-1,'9M2025')] if p=='TTM Sep 2026' else [(1,'FY2024'),(1,'9M2025'),(-1,'9M2024')] if p=='TTM Sep 2025' else [(1,'Q32026')] if p=='Q3 2026' else []
 for m in ['petroleum_company_ebitda','petroleum_company_adjusted_ebitda','consolidated_derivative_total_pnl','consolidated_derivative_unrealized_pnl','rin_waiver']:
  v=[(w,nf(k,m)) for w,k in terms];z[m]=sum(w*x for w,x in v) if v and all(x is not None for w,x in v) else None
 if z['consolidated_derivative_total_pnl'] is not None:z['consolidated_derivative_realized_pnl_inferred']=z['consolidated_derivative_total_pnl']-z['consolidated_derivative_unrealized_pnl']
 if z['rin_waiver'] is not None:z['petroleum_company_ebitda_less_specific_waiver']=z['petroleum_company_ebitda']-z['rin_waiver']
 z['adjustment_source_observation_ids']=[x['observation_id'] for x in N if any(x['period']==k for _,k in terms)]
(D/'ex_uan_and_adjustments.json').write_text(json.dumps({'units':'USD million','warning':'Ex-UAN operating metrics retain corporate/reconciling/former renewables. Pure Petroleum company EBITDA is distinct from operating EBIT+D&A. Waiver-only adjustment leaves other RFS remeasurement. Derivative realized figures are inferred consolidated residuals.','periods':X},indent=2)+'\n')
