#!/usr/bin/env python3
"""Offline, standard-library reproduction from preserved numeric SEC extracts."""
import csv,json,hashlib
from pathlib import Path
from decimal import Decimal
B=Path(__file__).resolve().parent
ledger=json.loads((B/'source_numeric_ledger.json').read_text())
priority={'q2':0,'q1':1,'fy26':2,'q3fy26':3,'q2fy26':4,'fy25':5,'q4release':6,'q1fy26':7,'q3fy25':8,'q2fy25':9}
L=sorted(ledger,key=lambda x:priority[x['source_id']]);lookup={}
for x in L:lookup.setdefault((x['metric'],x['start'],x['end']),x)
periods={
 'FY24':('2023-01-30','2024-01-28'),'FY25':('2024-01-29','2025-01-26'),'FY26':('2025-01-27','2026-01-25'),
 'Q3FY25':('2024-07-29','2024-10-27'),'Q4FY25':('2024-10-28','2025-01-26'),'Q1FY26':('2025-01-27','2025-04-27'),'Q2FY26':('2025-04-28','2025-07-27'),
 'Q3FY26':('2025-07-28','2025-10-26'),'Q4FY26':('2025-10-27','2026-01-25'),'Q1FY27':('2026-01-26','2026-04-26'),'Q2FY27':('2026-04-27','2026-07-26'),
 'H1FY25':('2024-01-29','2024-07-28'),'H1FY26':('2025-01-27','2025-07-27'),'H1FY27':('2026-01-26','2026-07-26'),
 '9MFY25':('2024-01-29','2024-10-27'),'9MFY26':('2025-01-27','2025-10-26'),
 'TTM_Q2FY26':('2024-07-29','2025-07-27'),'TTM_Q2FY27':('2025-07-28','2026-07-26')}
flow=['revenue','gross_profit','ebit','net_income','consolidated_net_income','eps_basic','eps_diluted','basic_shares','diluted_shares','tax_expense','cfo','capex_ppe','capex_intangibles','sbc_cf','sbc_pnl','da_cf','intangible_amortization_total','acquired_technology_amortization','acquired_customer_trade_amortization']
bal=['cash','debt_current','debt_long_term','assets','current_assets','current_liabilities','equity','liabilities_and_equity','inventory','receivables','payables','accrued_liabilities','goodwill','intangibles','assets_held_for_sale','liabilities_held_for_sale','ppe']
rows=[];checks=[];issues=[];R={}
def put(p,m,v,ids,basis,formula='',comp='comparable'):
 a,b=periods[p];row=dict(period=p,start=None if m in bal or m in ['total_debt_carrying','net_debt_carrying','liabilities'] else a,end=b,metric=m,value=round(float(v),6) if v is not None else None,unit='USD/share' if m.startswith('eps_') else 'million shares' if m.endswith('_shares') else 'percent' if m.endswith('_pct') else 'USD million',basis=basis,source_ids=','.join(sorted(set(ids))),formula=formula,comparability=comp)
 rows.append(row);R[p,m]=row;return row
def direct(p,m):
 a,b=periods[p];x=lookup.get((m,None if m in bal else a,b))
 if x:return put(p,m,x['value'],[x['id']],'fact_source_reported',comp=x['comparability'])
def derive(p,m,terms,formula=None):
 vals=[];ids=[]
 for q,n,c in terms:
  r=R.get((q,n))
  if not r or r['value'] is None:return None
  vals.append(Decimal(str(r['value']))*Decimal(str(c)));ids.extend(r['source_ids'].split(','))
 return put(p,m,sum(vals),ids,'derived_calculation',formula or ' + '.join(f'{c} * {q}.{n}' for q,n,c in terms))
for p in periods:
 if p.startswith('TTM'):continue
 for m in flow+bal:direct(p,m)
# Q1FY27 presents only payables and accrued liabilities under current liabilities; no current debt line.
derive('Q1FY27','debt_current',[('Q1FY27','current_liabilities',1),('Q1FY27','payables',-1),('Q1FY27','accrued_liabilities',-1)],'Current liabilities less the two disclosed current-liability components; residual is zero, corroborating no current debt')
# Standalone cash-flow and additive statement lines from cumulative filings.
bridges={'Q2FY26':[('H1FY26',1),('Q1FY26',-1)],'Q2FY27':[('H1FY27',1),('Q1FY27',-1)],'Q3FY25':[('9MFY25',1),('H1FY25',-1)],'Q3FY26':[('9MFY26',1),('H1FY26',-1)],'Q4FY25':[('FY25',1),('9MFY25',-1)],'Q4FY26':[('FY26',1),('9MFY26',-1)]}
for p,terms in bridges.items():
 for m in flow:
  if (p,m) in R or m.startswith('eps_') or m.endswith('_shares') or m in ['net_income','consolidated_net_income']:continue
  derive(p,m,[(q,m,c) for q,c in terms])
for p,terms,quarters in [('TTM_Q2FY26',[('FY25',1),('H1FY26',1),('H1FY25',-1)],['Q3FY25','Q4FY25','Q1FY26','Q2FY26']),('TTM_Q2FY27',[('FY26',1),('H1FY27',1),('H1FY26',-1)],['Q3FY26','Q4FY26','Q1FY27','Q2FY27'])]:
 for m in flow:
  if m.startswith('eps_'):derive(p,m,[(q,m,1) for q in quarters], 'Sum of four directly reported quarterly EPS; analytical sum, not issuer-reported annual GAAP EPS')
  elif m.endswith('_shares'):continue
  else:derive(p,m,[(q,m,c) for q,c in terms])
 for m in bal:direct(p,m)
for p in periods:
 for m,terms in {'acquired_amortization':[('acquired_technology_amortization',1),('acquired_customer_trade_amortization',1)],'fcf_ppe':[('cfo',1),('capex_ppe',-1)],'fcf_ppe_and_intangibles':[('cfo',1),('capex_ppe',-1),('capex_intangibles',-1)],'fcf_less_sbc_proxy':[('cfo',1),('capex_ppe',-1),('sbc_cf',-1)],'total_debt_carrying':[('debt_current',1),('debt_long_term',1)],'net_debt_carrying':[('debt_current',1),('debt_long_term',1),('cash',-1)],'liabilities':[('liabilities_and_equity',1),('equity',-1)]}.items():derive(p,m,[(p,n,c) for n,c in terms])
 for m,n,d in [('ebit_margin_pct','ebit','revenue'),('fcf_margin_pct','fcf_ppe','revenue'),('sbc_pct_revenue','sbc_cf','revenue')]:
  if (p,n) in R and (p,d) in R:put(p,m,100*R[p,n]['value']/R[p,d]['value'],R[p,n]['source_ids'].split(',')+R[p,d]['source_ids'].split(','),'derived_calculation',f'100 * {n} / {d}')
 for m in flow:
  if (p,m) not in R:
   put(p,m,None,[],'missing_required_source',comp='unavailable');issues.append(dict(period=p,metric=m,severity='info',reason='Not directly reported or unavailable; weighted shares deliberately not bridged; quarterly EPS/NI never subtracted.'))
 for a,b in [('assets','liabilities_and_equity'),('sbc_cf','sbc_pnl')]:
  if (p,a) in R and (p,b) in R and R[p,a]['value'] is not None and R[p,b]['value'] is not None:
   delta=round(R[p,a]['value']-R[p,b]['value'],6);checks.append(dict(check=f'{a} equals {b}',period=p,delta=delta,status='PASS' if abs(delta)<.0011 else 'REVIEW'))
# Selected contemporaneous comparative disclosures must match newer filings.
for key,x in lookup.items():
 peers=[y for y in ledger if (y['metric'],y['start'],y['end'])==key and y['source_id']!=x['source_id']]
 for y in peers:
  d=round(x['value']-y['value'],6)
  checks.append(dict(check='Repeated source numeric agreement: '+key[0],period=str(key[1])+':'+key[2],delta=d,status='PASS' if abs(d)<.0011 else 'REVIEW'))
# TTM annual bridges tie to four quarters, allowing rounded direct Q4 NI.
for p,qs in [('TTM_Q2FY26',['Q3FY25','Q4FY25','Q1FY26','Q2FY26']),('TTM_Q2FY27',['Q3FY26','Q4FY26','Q1FY27','Q2FY27'])]:
 for m in ['revenue','ebit','net_income','cfo','capex_ppe','sbc_cf','da_cf']:
  d=round(R[p,m]['value']-sum(R[q,m]['value'] for q in qs),6);tol=.051 if m=='net_income' else .0011
  checks.append(dict(check='TTM annual bridge equals four quarters: '+m,period=p,delta=d,status='PASS' if abs(d)<=tol else 'FAIL'))
def csvout(name,rs):
 with (B/name).open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rs[0]));w.writeheader();w.writerows(rs)
rows.sort(key=lambda x:(list(periods).index(x['period']),x['metric']))
csvout('normalized_financials_long.csv',rows);csvout('source_numeric_ledger.csv',ledger);csvout('validation_checks.csv',checks);csvout('missing_fields.csv',issues)
wide=[]
for p,(a,b) in periods.items():
 w={'period':p,'start':a,'end':b};w.update({m:R[p,m]['value'] for m in sorted({m for q,m in R}) if (p,m) in R});wide.append(w)
fields=['period','start','end']+sorted(set().union(*(set(w) for w in wide))-{'period','start','end'})
with (B/'financial_history.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(wide)
(B/'financial_history.json').write_text(json.dumps({'issuer':'Semtech Corporation','ticker':'SMTC','currency':'USD','monetary_units':'million','as_of':'2026-11-04','periods':wide,'methodology':'All direct SEC data. TTM additive lines = FY + current H1 - prior H1. EPS is sum of four direct quarterly EPS, never annual EPS subtraction. Quarterly NI is direct and Q4 rounded. Cash-flow quarterization uses subtraction of cumulative values.'},indent=2)+'\n')
(B/'qa_summary.json').write_text(json.dumps({'checks':len(checks),'pass':sum(x['status']=='PASS' for x in checks),'review':sum(x['status']=='REVIEW' for x in checks),'fail':sum(x['status']=='FAIL' for x in checks),'missing_fields':len(issues),'requires_readme':True},indent=2)+'\n')
print((B/'qa_summary.json').read_text())
