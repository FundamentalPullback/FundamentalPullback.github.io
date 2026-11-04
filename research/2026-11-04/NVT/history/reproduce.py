#!/usr/bin/env python3
"""Offline NVT financial history. Python stdlib only; consumes compact numeric_ledger.json."""
import json,csv,pathlib
P=pathlib.Path(__file__).resolve().parent
src=json.loads((P/'numeric_ledger.json').read_text()); facts={x['id']:x for x in src['facts']}; metrics=list(src['metrics']); balances=src['balance_metrics']; flows=[m for m in metrics if m not in balances]
rows=[]; audit=[]
def direct(period,metric):
 f=facts.get(period+':'+metric)
 return (f['value'],[f['id']],'direct') if f else (None,[],'not separately available')
def calc(terms,metric,label):
 a=[direct(period,metric) for period,sign in terms]
 if any(x[0] is None for x in a):return None,[k for x in a for k in x[1]],'missing component: '+label
 return round(sum(x[0]*sign for x,(_,sign) in zip(a,terms)),6),[k for x in a for k in x[1]],label
def add(period,start,end,kind):
 row=dict(period=period,start=start,end=end,kind=kind)
 for m in metrics:
  if m in balances:
   base=('FY'+end[:4] if end.endswith('12-31') else end[:4]+'_YTD'+str(int(end[5:7])//3))
   v,ids,method=direct(base,m)
  elif kind=='FY':v,ids,method=direct(period,m)
  elif kind=='TTM':
   if m.startswith('eps'):v,ids,method=None,[],'TTM EPS not directly disclosed; never subtract EPS'
   else:
    y=int(end[:4]);v,ids,method=calc([(f'FY{y-1}',1),(f'{y}_YTD3',1),(f'{y-1}_YTD3',-1)],m,'prior FY + current 9M - prior 9M')
  else:
   y=int(period[:4]);q=int(period[-1]);v,ids,method=direct(period,m)
   if v is None and not m.startswith('eps'):
    terms=[(f'FY{y}',1),(f'{y}_YTD3',-1)] if q==4 else [(f'{y}_YTD{q}',1)]+([(f'{y}_YTD{q-1}',-1)] if q>1 else [])
    v,ids,method=calc(terms,m,'quarter from matching-scope cumulative dollar amounts')
  row[m]=v;audit.append(dict(period=period,metric=m,value=v,input_ids=ids,method=method))
 row['capex_intangible_separate']=None
 row['acquired_intangible_amortization_separate']=None
 def derived(name,components,fn):
  vals=[row[k] for k in components];row[name]=round(fn(*vals),6) if all(x is not None for x in vals) else None
  audit.append(dict(period=period,metric=name,value=row[name],input_ids=[period+':'+x for x in components],method='derived from normalized row: '+name))
 derived('da_continuing',['depreciation_continuing','intangible_amortization_continuing'],lambda d,a:d+a)
 derived('fcf_continuing_strict',['cfo_continuing','capex_ppe_continuing'],lambda c,k:c-k)
 derived('fcf_continuing_company_definition',['cfo_continuing','capex_ppe_continuing','ppe_sale_proceeds_continuing'],lambda c,k,p:c-k+p)
 derived('fcf_continuing_after_sbc',['cfo_continuing','capex_ppe_continuing','sbc_continuing'],lambda c,k,s:c-k-s)
 derived('effective_tax_rate_pct',['income_tax_continuing','pretax_income_continuing'],lambda t,p:100*t/p if p else 0)
 derived('operating_margin_pct',['operating_income_continuing','revenue_continuing'],lambda e,r:100*e/r)
 derived('cfo_to_continuing_ni',['cfo_continuing','net_income_continuing'],lambda c,n:c/n if n else 0)
 derived('debt_carrying_value',['debt_current','debt_noncurrent'],lambda c,l:c+l)
 rows.append(row)
for y in [2023,2024,2025]:add(f'FY{y}',f'{y}-01-01',f'{y}-12-31','FY')
for y,q in [(2024,4),(2025,1),(2025,2),(2025,3),(2025,4),(2026,1),(2026,2),(2026,3)]:
 ends={1:'03-31',2:'06-30',3:'09-30',4:'12-31'};starts={1:'01-01',2:'04-01',3:'07-01',4:'10-01'}
 add(f'{y}Q{q}',f'{y}-{starts[q]}',f'{y}-{ends[q]}','quarter')
for y in [2025,2026]:add(f'TTM_{y}-09-30',f'{y-1}-10-01',f'{y}-09-30','TTM')
checks=[]
def check(label,a,b,tol=.11):
 if a is None or b is None:checks.append({'check':label,'status':'not_testable'})
 else:
  ok=abs(a-b)<=tol;checks.append({'check':label,'status':'pass' if ok else 'FAIL','left':a,'right':b});assert ok,(label,a,b)
for r in rows:
 p=r['period'];check(p+' CFO continuing + discontinued = consolidated',None if any(r[k] is None for k in ['cfo_continuing','cfo_discontinued']) else r['cfo_continuing']+r['cfo_discontinued'],r['cfo_consolidated'])
 check(p+' NI continuing + discontinued = consolidated',None if any(r[k] is None for k in ['net_income_continuing','net_income_discontinued']) else r['net_income_continuing']+r['net_income_discontinued'],r['net_income_consolidated'])
 check(p+' pretax - tax = continuing NI',None if any(r[k] is None for k in ['pretax_income_continuing','income_tax_continuing']) else r['pretax_income_continuing']-r['income_tax_continuing'],r['net_income_continuing'])
 check(p+' assets = liabilities + equity',None if any(r[k] is None for k in ['liabilities','equity']) else r['liabilities']+r['equity'],r['assets'])
lookup={r['period']:r for r in rows}
for y in [2025,2026]:
 for m in flows:
  if m.startswith('eps'):continue
  qs=[lookup[f'{y-1}Q4'][m]]+[lookup[f'{y}Q{q}'][m] for q in [1,2,3]]
  check(f'TTM {y} {m} = four quarters',sum(qs) if all(v is not None for v in qs) else None,lookup[f'TTM_{y}-09-30'][m])
for r in rows:
 if r['kind']=='quarter':assert r['eps_diluted_continuing'] is not None
(P/'history.json').write_text(json.dumps({'as_of':src['as_of'],'units':'USD million except EPS USD/share, ratios, and pct fields','rows':rows},indent=2)+'\n')
(P/'derivation_audit.json').write_text(json.dumps(audit,indent=2)+'\n')
(P/'qa.json').write_text(json.dumps({'status':'PASS','checks':checks,'null_fields':{r['period']:[k for k,v in r.items() if v is None] for r in rows}},indent=2)+'\n')
for name,data in [('history.csv',rows),('numeric_ledger.csv',src['facts'])]:
 with (P/name).open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(data[0]));w.writeheader();w.writerows(data)
print('PASS:',len(rows),'periods;',len(src['facts']),'source facts;',len(checks),'checks. No network used.')
