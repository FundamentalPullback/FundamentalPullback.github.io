#!/usr/bin/env python3
"""Offline reproduction from the accompanying compact factual ledger; stdlib only."""
import json,csv,pathlib,datetime
ROOT=pathlib.Path(__file__).resolve().parent
facts=json.loads((ROOT/'facts_ledger.json').read_text()) + json.loads((ROOT/'manual_facts.json').read_text())
metrics=sorted(set(f['metric'] for f in facts)); out=[]; audit=[]
STOCK={'cash','assets','liabilities','equity','debt_gross_reported','debt_noncurrent_net','debt_current','ppe_net','software_gross_balance'}
SHARES={'shares_basic','shares_diluted'};EPS={'eps_basic','eps_diluted'}
def get(src,metric,start,end):
 fs=[x for x in facts if x['source_id']==src and x['metric']==metric and x['start']==start and x['end']==end]
 return fs[-1]['value'] if fs else None
def build(name,start,end,terms,stocksrc,quarter=False):
 row={'period':name,'start':start,'end':end,'perimeter':'Aireon consolidated from 2026-07-02 only' if end>='2026-07-02' else 'Aireon equity method; Satelles consolidated from 2024-04-01'}
 days=(datetime.date.fromisoformat(end)-datetime.date.fromisoformat(start)).days+1
 for m in metrics:
  if m in STOCK:
   v=get(stocksrc,m,None,end); formula=f'{stocksrc}: balance at {end}'
  else:
   vs=[get(s,m,a,b) for s,a,b,c in terms]
   coeff=[c for s,a,b,c in terms]
   formula=' + '.join(f'{c}*{s}[{a}:{b}]' for s,a,b,c in terms)
   if m in SHARES:
    coeff=[c*((datetime.date.fromisoformat(b)-datetime.date.fromisoformat(a)).days+1)/days for s,a,b,c in terms]
    formula='duration-weighted: '+formula
   v=sum(x*c for x,c in zip(vs,coeff)) if all(x is not None for x in vs) else None
   # Use directly reported quarter for financial statement income flows where available.
   if quarter:
    direct=get(stocksrc,m,start,end)
    if direct is not None: v=direct; formula=f'{stocksrc}: reported {start}:{end}'
   if m in EPS and len(terms)>1 and not (quarter and get(stocksrc,m,start,end) is not None):
    v=None;formula='Not additive; calculated below from period NI / duration-weighted shares'
  row[m]=round(v if m in EPS else v/1e6,6) if v is not None else None
  audit.append({'period':name,'metric':m,'formula':formula,'status':'available' if v is not None else 'not separately available / non-additive'})
 for e,s in [('eps_basic','shares_basic'),('eps_diluted','shares_diluted')]:
  if row.get(e) is None and row.get(s) and row.get('net_income') is not None:
   row[e]=round(row['net_income']/row[s],4);row[e+'_basis']='calculated NI / duration-weighted shares; not reported GAAP EPS'
  else:row[e+'_basis']='reported'
 for m,a,b in [('fcf_cfo_less_gross_cash_capex','cfo','gross_cash_capex'),('da_less_identifiable_intangible_amortization','da_total','intangible_amortization')]:
  row[m]=round(row[a]-row[b],6) if row.get(a) is not None and row.get(b) is not None else None
 row['sbc_tie_check']=round(row['sbc_total_recognized']-row['sbc_expense_cf']-row['sbc_capitalized'],6) if all(row.get(x) is not None for x in ['sbc_total_recognized','sbc_expense_cf','sbc_capitalized']) else None
 out.append(row)
for y in [2023,2024,2025]:
 src='fy25'; stock='fy24' if y==2023 else src
 build(f'FY{y}',f'{y}-01-01',f'{y}-12-31',[(src,f'{y}-01-01',f'{y}-12-31',1)],stock)
build('Q4_2025','2025-10-01','2025-12-31',[('fy25','2025-01-01','2025-12-31',1),('q3','2025-01-01','2025-09-30',-1)],'fy25')
build('Q1_2026','2026-01-01','2026-03-31',[('q1','2026-01-01','2026-03-31',1)],'q1',True)
build('Q2_2026','2026-04-01','2026-06-30',[('q2','2026-01-01','2026-06-30',1),('q1','2026-01-01','2026-03-31',-1)],'q2',True)
build('Q3_2026','2026-07-01','2026-09-30',[('q3','2026-01-01','2026-09-30',1),('q2','2026-01-01','2026-06-30',-1)],'q3',True)
build('9M_2026','2026-01-01','2026-09-30',[('q3','2026-01-01','2026-09-30',1)],'q3')
build('9M_2025','2025-01-01','2025-09-30',[('q3','2025-01-01','2025-09-30',1)],'q325')
build('TTM_2026Q3','2025-10-01','2026-09-30',[('fy25','2025-01-01','2025-12-31',1),('q3','2025-01-01','2025-09-30',-1),('q3','2026-01-01','2026-09-30',1)],'q3')
build('TTM_2025Q3','2024-10-01','2025-09-30',[('fy25','2024-01-01','2024-12-31',1),('q324','2024-01-01','2024-09-30',-1),('q3','2025-01-01','2025-09-30',1)],'q325')
# Narrow explicit normalizations, not replacement of GAAP history. SBC is retained.
for r in out:
 r['transaction_cost_addback']= {'Q3_2026':21.294,'9M_2026':36.318,'TTM_2026Q3':36.318}.get(r['period'])
 r['ebit_ex_identified_transaction_costs']=round(r['ebit']+r['transaction_cost_addback'],6) if r['transaction_cost_addback'] is not None else None
 r['software_capitalization_flow']=None
 r['satellite_only_depreciation']=None
(ROOT/'normalized_history.json').write_text(json.dumps({'units':'USD millions and shares millions; EPS USD/share; null means unavailable, not zero','rows':out},indent=2)+'\n')
keys=list(dict.fromkeys(k for r in out for k in r))
with (ROOT/'normalized_history.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=keys);w.writeheader();w.writerows(out)
(ROOT/'derivation_audit.json').write_text(json.dumps(audit,indent=2)+'\n')
for r in out:
 assert r['sbc_tie_check'] is None or abs(r['sbc_tie_check']) <= 0.0011,r
print('Reproduced',len(out),'periods; SBC expense + capitalized reconciles to total recognized wherever available.')
for r in out:print(r['period'],*[f'{k}={r[k]}' for k in ['revenue','ebit','net_income','cfo','gross_cash_capex','sbc_expense_cf']])
