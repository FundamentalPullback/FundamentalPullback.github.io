#!/usr/bin/env python3
"""Portable offline rebuild, Python standard library only. Run from any cwd."""
import json,csv,calendar,pathlib,hashlib
P=pathlib.Path(__file__).resolve().parent;D=json.loads((P/'numeric_inputs.json').read_text());M=D['metric_definitions'];L={};C=[];QA=[];CACHE={}
def key(m,s,e):return '|'.join([m,s or 'snapshot',e])
def put(m,s,e,v,method,ids,formula=''):
 k=key(m,s,e);L[k]=dict(node=k,metric=m,start=s,end=e,value=v,method=method,input_ids=';'.join(ids),formula=formula);return v
def get(m,s,e):
 if M[m]['kind']=='balance':s=None
 k=key(m,s,e)
 if k in CACHE:return CACHE[k]
 ff=[f for f in D['facts'] if f['metric']==m and f['start']==s and f['end']==e]
 v=None
 if ff:
  a=max(ff,key=lambda f:(f['filed'],float(f['decimals'] or 0)));v=a['value']
  for b in ff:
   tol=(10**(-float(a['decimals'] or 0))+10**(-float(b['decimals'] or 0)))/(1 if m.startswith('eps') else 1e6)/2+1e-8
   if abs(b['value']-v)>tol:C.append(dict(node=k,selected=a['id'],other=b['id'],selected_value=v,other_value=b['value'],resolution='latest filed exact-period comparative retained'))
  v=put(m,s,e,v,'direct',[a['id']])
 elif M[m]['kind']=='flow' and s and s[5:]!='01-01':
  y=int(s[:4]);month=int(s[5:7])-1;prev=f'{y}-{month:02d}-{calendar.monthrange(y,month)[1]}'
  a=get(m,f'{y}-01-01',e);b=get(m,f'{y}-01-01',prev)
  if a is not None and b is not None:v=put(m,s,e,round(a-b,6),'derived quarter',[key(m,f'{y}-01-01',e),key(m,f'{y}-01-01',prev)],'current YTD - previous YTD')
 CACHE[k]=v;return v
def derive(r):
 def calc(n,ks,fn,formula):
  v=round(fn(*[r[k] for k in ks]),6) if all(r.get(k) is not None for k in ks) else None;r[n]=v
  if v is not None:put(n,r['start'],r['end'],v,'derived metric',[key(k,None if M.get(k,{}).get('kind')=='balance' else r['start'],r['end']) for k in ks],formula)
 calc('fcf_ppe',['cfo','capex_ppe'],lambda a,b:a-b,'CFO - cash PPE capex')
 calc('fcf_ppe_after_sbc_proxy',['cfo','capex_ppe','sbc_cashflow'],lambda a,b,c:a-b-c,'CFO - cash PPE capex - cash-flow SBC; proxy not owner earnings')
 calc('ebitda_gaap_proxy',['ebit_gaap','da'],lambda a,b:a+b,'GAAP EBIT + combined cash-flow D&A; not company Adjusted EBITDA')
 calc('funded_debt_carrying',['recourse_debt_current','recourse_debt_noncurrent','nonrecourse_debt_current','nonrecourse_debt_noncurrent'],lambda *x:sum(x),'recourse + nonrecourse debt current/noncurrent carrying value')
 calc('financing_obligations_total',['financing_obligation_current','financing_obligation_noncurrent'],lambda a,b:a+b,'financing obligations current + noncurrent')
 calc('debt_including_financing',['funded_debt_carrying','financing_obligations_total'],lambda a,b:a+b,'funded debt + financing obligations; excludes operating leases')
 calc('net_debt_including_financing',['debt_including_financing','cash'],lambda a,b:a-b,'funded debt + financing obligations - unrestricted cash')
 calc('nci_income_bridge_residual',['ni_consolidated','nci_income','ni_attributable'],lambda a,b,c:a-b-c,'consolidated NI - NCI NI - common NI')
 calc('balance_sheet_residual',['assets','liabilities','equity_total'],lambda a,b,c:a-b-c,'assets - liabilities - total equity')
 calc('cash_flow_residual',['cfo','cfi','cff','cash_fx','cash_change'],lambda a,b,c,d,e:a+b+c+d-e,'CFO + CFI + CFF + FX - cash movement')
 calc('pretax_tax_ni_residual',['pretax_income','tax_expense','ni_consolidated'],lambda a,b,c:a-b-c,'pretax - tax provision - consolidated NI')
 calc('cfo_bridge_residual',[k for k in M if k.startswith('cf_bridge_')]+['cfo'],lambda *vs:sum(vs[:-1])-vs[-1],'sum every signed cash-flow bridge line including NI - reported CFO')
 r['capitalized_software_separate']=None;r['amortization_intangibles_separate']=None
 for k in ['nci_income_bridge_residual','balance_sheet_residual','cash_flow_residual','pretax_tax_ni_residual','cfo_bridge_residual']:
  v=r[k];QA.append(dict(period=r['period'],check=k,residual=v,status='PASS' if v is not None and abs(v)<=.0031 else 'NOT_AVAILABLE' if v is None else 'FAIL',tolerance_usd_million=.0031))
 return r
rows=[]
def row(label,s,e):
 r=dict(period=label,start=s,end=e);r.update({m:get(m,s,e) for m in M});rows.append(derive(r))
for y in [2023,2024,2025]:row('FY'+str(y),f'{y}-01-01',f'{y}-12-31')
for y in [2024,2025,2026]:
 for q in range(1,5 if y<2026 else 4):
  mon=3*q;row(f'Q{q}_{y}',f'{y}-{mon-2:02d}-01',f'{y}-{mon:02d}-{calendar.monthrange(y,mon)[1]}')
for y in [2024,2025,2026]:row('9M'+str(y),f'{y}-01-01',f'{y}-09-30')
for y in [2025,2026]:
 r=dict(period='TTM'+str(y)+'Q3',start=f'{y-1}-10-01',end=f'{y}-09-30')
 for m in M:
  if M[m]['kind']=='balance':r[m]=get(m,None,r['end'])
  elif M[m]['kind'] in ['eps','shares']:r[m]=None
  else:
   periods=[(f'{y-1}-01-01',f'{y-1}-12-31'),(f'{y}-01-01',r['end']),(f'{y-1}-01-01',f'{y-1}-09-30')];v=[get(m,s,e) for s,e in periods]
   r[m]=put(m,r['start'],r['end'],round(v[0]+v[1]-v[2],6),'TTM bridge',[key(m,s,e) for s,e in periods],'prior FY + current 9M - prior 9M') if all(x is not None for x in v) else None
 rows.append(derive(r))
def csvout(name,rs):
 keys=list(dict.fromkeys(k for r in rs for k in r))
 with (P/name).open('w',newline='') as f:
  w=csv.DictWriter(f,keys);w.writeheader();w.writerows(rs)
(P/'history.json').write_text(json.dumps(dict(company=D['company'],as_of=D['cutoff'],rows=rows),indent=2)+'\n')
csvout('history.csv',rows);csvout('ledger.csv',list(L.values()));csvout('conflicts.csv',C);csvout('validation_checks.csv',QA);csvout('source_index.csv',D['sources'])
flags=[dict(flag='ISSUER_EPS_SCALE_ERROR',detail='Q3 2025 10-Q comparative Q3/9M 2024 EPS has erroneous inline scale=3 although displayed -0.06/-0.59. Use displayed USD/share, corroborated by original 2024 filing, not raw scaled -60/-590.'),dict(flag='SOFTWARE_NOT_SEPARATELY_DISCLOSED',detail='No standalone capitalized software cash line identified. Null, not zero. Do not add a fabricated software deduction.'),dict(flag='DA_COMBINED',detail='Cash-flow row labelled Depreciation and amortization is tagged us-gaap:Depreciation. Preserve combined D&A. Separate intangible amortization is unavailable, not zero.'),dict(flag='EPS_TTM_NOT_ADDITIVE',detail='No TTM EPS or shares fabricated. Quarter EPS/shares direct only, never FY minus YTD.'),dict(flag='SBC_DEFINITIONS',detail='Cash-flow SBC and income-statement allocated SBC differ; use cash-flow row for cash-flow proxy. Customer warrant consideration is separate, not employee SBC.'),dict(flag='FINANCING_OBLIGATIONS',detail='Show failed sale-leaseback financing obligations separately from recourse/nonrecourse debt and operating leases.'),dict(flag='ROUNDING',detail='Quarter/YTD statements in thousands may differ by $1k from direct earnings release; retain latest filing and tolerance $3.1k.'),dict(flag='FCF_PROXY',detail='FCF PPE excludes affiliate cash investments, financing-obligation repayments, NCI payouts and dilution. It is not cash distributable to common holders.')]
csvout('qa_flags.csv',flags)
(P/'qa.txt').write_text('\n'.join([f"{len(rows)} periods; {len(D['facts'])} direct inputs; {len(L)} ledger nodes",f"Checks: {sum(x['status']=='PASS' for x in QA)} pass, {sum(x['status']=='FAIL' for x in QA)} fail, {sum(x['status']=='NOT_AVAILABLE' for x in QA)} unavailable",f'{len(C)} material conflict comparisons retained']+ [str(x) for x in QA if x['status']=='FAIL'])+'\n')
(P/'checksums.txt').write_text(''.join(hashlib.sha256((P/f).read_bytes()).hexdigest()+'  '+f+'\n' for f in ['numeric_inputs.json','history.json','history.csv','ledger.csv','validation_checks.csv','conflicts.csv','source_index.csv','qa_flags.csv','qa.txt']))
print((P/'qa.txt').read_text())
