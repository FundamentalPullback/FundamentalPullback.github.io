#!/usr/bin/env python3
"""Portable OFFLINE rebuild. Python standard library only; no filings or network needed."""
import pathlib,json,csv,datetime,hashlib
P=pathlib.Path(__file__).resolve().parent;D=json.loads((P/'numeric_inputs.json').read_text());M=D['metric_definitions'];L={};conflicts=[];checks=[];cache={}
BAL={m for m in M if M[m]['kind']=='balance'};NONADD={m for m in M if M[m]['kind'] in ['eps','shares']}
ENDS={y:[f'{y-1}-12-31',f'{y}-03-31',f'{y}-06-30',f'{y}-09-30',f'{y}-12-31'] for y in range(2023,2027)}
def nextday(x):return str(datetime.date.fromisoformat(x)+datetime.timedelta(days=1))
def node(m,s,e):return m+'|'+str(s)+'|'+e
def log(m,s,e,v,method,ids,formula='',url=''):
 L[node(m,s,e)]=dict(node_id=node(m,s,e),metric=m,start=s,end=e,value=v,method=method,input_ids=';'.join(ids),formula=formula,source_url=url);return v
def direct(m,s,e):
 fs=[f for f in D['facts'] if f['metric']==m and f['end']==e and (f['start'] is None if m in BAL else f['start']==s)]
 if not fs:return None
 def rank(f):return(f['filed'],999 if f['decimals']=='INF' else int(f['decimals']))
 a=max(fs,key=rank)
 for b in fs:
  tol=(10**(-int(a['decimals']))+10**(-int(b['decimals'])))/ (1 if m.startswith('eps') else 1e6)/2 if a['decimals']!='INF' and b['decimals']!='INF' else .000001
  if abs(a['value']-b['value'])>tol+1e-8:conflicts.append(dict(metric=m,start=s,end=e,selected=a['id'],selected_value=a['value'],other=b['id'],other_value=b['value'],resolution='Latest filing, then highest precision'))
 return log(m,s,e,a['value'],'direct',[a['id']],url=a['source_url'])
def get(m,s,e):
 if m in BAL:s=None
 key=(m,s,e)
 if key in cache:return cache[key]
 v=direct(m,s,e)
 if v is None and m not in NONADD|BAL:
  for fy,ends in ENDS.items():
   if e in ends[1:] and s and s>nextday(ends[0]):
    pe=str(datetime.date.fromisoformat(s)-datetime.timedelta(days=1));ys=nextday(ends[0]);a=get(m,ys,e);b=get(m,ys,pe)
    if a is not None and b is not None:v=log(m,s,e,round(a-b,6),'YTD subtraction',[node(m,ys,e),node(m,ys,pe)],'current YTD - previous YTD')
    break
 cache[key]=v;return v
def derive(r):
 def calc(n,keys,fn,formula):
  v=round(fn(*[r[k] for k in keys]),6) if all(r.get(k) is not None for k in keys) else None;r[n]=v
  if v is not None:log(n,r['start'],r['end'],v,'derived metric',[node(k,None if k in BAL else r['start'],r['end']) for k in keys],formula)
 calc('capex_total_cash',['capex_ppe','capex_software'],lambda a,b:a+b,'Cash PP&E purchases plus separately reported internally developed software capitalization')
 calc('fcf_ppe_only_incomplete',['cfo','capex_ppe'],lambda a,b:a-b,'CFO minus PP&E only; INCOMPLETE for this business because software cash capex is separate')
 calc('fcf_after_ppe_software',['cfo','capex_ppe','capex_software'],lambda a,b,c:a-b-c,'CFO minus PP&E minus cash software capitalization')
 calc('fcf_after_sbc_proxy',['cfo','capex_ppe','capex_software','sbc'],lambda a,b,c,d:a-b-c-d,'CFO minus PP&E minus software minus SBC; not normalized owner earnings')
 calc('cash_after_acquisitions',['cfo','capex_ppe','capex_software','acquisitions_cash','deferred_acquisition_cash_financing'],lambda a,b,c,d,e:a-b-c-d-e,'CFO minus PP&E/software minus acquisition cash including deferred acquisition cash in financing')
 calc('debt_carrying',['debt_current','debt_noncurrent'],lambda a,b:a+b,'Current plus noncurrent debt carrying amount')
 calc('net_debt_carrying',['debt_current','debt_noncurrent','cash'],lambda a,b,c:a+b-c,'Current plus noncurrent carrying debt less cash')
 calc('net_debt_face',['debt_face','cash'],lambda a,b:a-b,'Debt principal stated in note less cash; unamortized costs not deducted')
 calc('operating_lease_liabilities',['lease_current','lease_noncurrent'],lambda a,b:a+b,'Operating lease current plus noncurrent; separately shown, not automatically added to debt')
 calc('working_capital_cash',['ar_change','unbilled_change','tax_wc_change','other_assets_change','ap_accruals_change','payroll_change','deferred_revenue_change'],lambda *v:sum(v),'Sum seven signed operating asset/liability cash changes')
 calc('cfo_before_working_capital',['cfo','working_capital_cash'],lambda a,b:a-b,'CFO less signed working capital; NOT normalized CFO because tax/payroll seasonal and other noncash adjustments remain')
 calc('ebit_margin_gaap_pct',['ebit','revenue_gaap'],lambda a,b:100*a/b,'100*EBIT/GAAP total revenue')
 calc('ebit_margin_rbr_pct',['ebit','revenue_rbr'],lambda a,b:100*a/b,'100*EBIT/revenue BEFORE reimbursable expenses')
 calc('ni_margin_gaap_pct',['ni','revenue_gaap'],lambda a,b:100*a/b,'100*NI/GAAP total revenue')
 calc('fcf_margin_rbr_pct',['fcf_after_ppe_software','revenue_rbr'],lambda a,b:100*a/b,'100*(CFO minus PP&E and software)/RBR')
 calc('cfo_to_ni',['cfo','ni'],lambda a,b:a/b,'CFO/NI')
 calc('non_acquired_da_residual',['da_cf','amort_acquired_intangibles'],lambda a,b:a-b,'CF D&A less acquired-intangible amortization; residual not pure depreciation; acquired amortization may be rounded')
 r['owner_earnings']=None;r['maintenance_capex']=None
 if all(r.get(x) is not None for x in ['assets','liabilities_current','liabilities_noncurrent','equity']):checks.append(dict(check='Balance equation',period=r['period'],residual=round(r['assets']-r['liabilities_current']-r['liabilities_noncurrent']-r['equity'],6)))
 if all(r.get(x) is not None for x in ['revenue_gaap','revenue_rbr','reimbursable_revenue']):checks.append(dict(check='Revenue total equals RBR plus reimbursements',period=r['period'],residual=round(r['revenue_gaap']-r['revenue_rbr']-r['reimbursable_revenue'],6)))
 if all(r.get(x) is not None for x in ['cfo','cash_investing','cash_financing','cash_fx','cash_change']):checks.append(dict(check='Cash flow bridge',period=r['period'],residual=round(r['cfo']+r['cash_investing']+r['cash_financing']+r['cash_fx']-r['cash_change'],6)))
rows=[]
def row(label,s,e):
 r=dict(period=label,start=s,end=e,basis='reported consolidated; calendar year; RBR and total GAAP revenue separately identified')
 for m in M:r[m]=get(m,s,e)
 derive(r);rows.append(r)
for y in [2023,2024,2025]:row(f'FY{y}',f'{y}-01-01',f'{y}-12-31')
for y,q in [(2024,4)]+[(2025,q) for q in range(1,5)]+[(2026,q) for q in range(1,4)]:row(f'Q{q} {y}',nextday(ENDS[y][q-1]),ENDS[y][q])
for y in [2024,2025,2026]:row(f'9M {y}',f'{y}-01-01',f'{y}-09-30')
for y in [2025,2026]:
 s=f'{y-1}-10-01';e=f'{y}-09-30';r=dict(period=f'TTM Sep {y}',start=s,end=e,basis='Prior FY + current 9M - prior 9M; no acquisition pro forma adjustment')
 for m in M:
  if m in BAL:r[m]=get(m,None,e)
  elif m in NONADD:r[m]=None
  else:
   ps=[(f'{y-1}-01-01',f'{y-1}-12-31'),(f'{y}-01-01',e),(f'{y-1}-01-01',f'{y-1}-09-30')];vs=[get(m,a,b) for a,b in ps];r[m]=log(m,s,e,round(vs[0]+vs[1]-vs[2],6),'TTM bridge',[node(m,a,b) for a,b in ps],'Prior FY + current 9M - prior 9M') if all(v is not None for v in vs) else None
 derive(r);rows.append(r)
for r in rows:
 p=r['period'];old=next((a for a in rows if a['period']==p[:-4]+str(int(p[-4:])-1)),None)
 for m in ['revenue_gaap','revenue_rbr','ebit','ni','cfo','fcf_after_ppe_software','fcf_after_sbc_proxy']:
  r[m+'_yoy_pct']=round(100*(r[m]/old[m]-1),6) if old and r.get(m) is not None and old.get(m) else None
# Validate additive bridges independently against assembled quarterly rows.
by={r['period']:r for r in rows}
for target,quarters in [('FY2025',[f'Q{q} 2025' for q in range(1,5)]),('TTM Sep 2025',['Q4 2024','Q1 2025','Q2 2025','Q3 2025']),('TTM Sep 2026',['Q4 2025','Q1 2026','Q2 2026','Q3 2026'])]:
 for m in ['revenue_gaap','revenue_rbr','ebit','ni','cfo','capex_ppe','capex_software','sbc','da_cf','da_income','working_capital_cash','fcf_after_ppe_software']:
  a=by[target].get(m);bs=[by[q].get(m) for q in quarters]
  if a is not None and all(v is not None for v in bs):checks.append(dict(check='Additive quarter bridge '+m,period=target,residual=round(a-sum(bs),6)))
for c in checks:c['status']='PASS' if abs(c['residual'])<=.002 else 'FAIL'
def csvwrite(name,rs):
 keys=list(dict.fromkeys(k for r in rs for k in r)) or ['none'];f=(P/name).open('w',newline='');w=csv.DictWriter(f,fieldnames=keys);w.writeheader();w.writerows(rs);f.close()
(P/'history.json').write_text(json.dumps(dict(asof=D['asof'],units=D['units'],rows=rows),indent=2)+'\n');csvwrite('history.csv',rows);csvwrite('ledger.csv',list(L.values()));csvwrite('conflicts.csv',conflicts);csvwrite('validation_checks.csv',checks);csvwrite('source_index.csv',D['sources'])
assert all(x['status']=='PASS' for x in checks),'Validation failed'
(P/'qa.txt').write_text(f'{len(rows)} periods; {len(L)} lineage nodes; {len(checks)} accounting checks PASS; {len(conflicts)} source conflicts in conflicts.csv.\nEPS are direct only. TTM EPS and diluted weighted shares left null.\nTotal cash capex includes separate software capitalization. Maintenance capex/owner earnings unknown.\n')
print((P/'qa.txt').read_text())
