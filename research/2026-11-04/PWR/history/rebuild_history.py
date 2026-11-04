#!/usr/bin/env python3
"""Rebuild all outputs offline from this directory's numeric_inputs.json; standard library only."""
import calendar,csv,hashlib,json,pathlib
P=pathlib.Path(__file__).resolve().parent
D=json.loads((P/'numeric_inputs.json').read_text());S=D['metric_definitions'];L={};CONFLICT=[];CHECK=[];FLAGS=[]
MET=list(S);BAL={m for m in S if S[m]['kind']=='balance'};NONADD={m for m in S if S[m]['kind'] in ['eps','shares']}
CACHE={}
def qend(y,q):
 m=q*3;return f'{y}-{m:02d}-{calendar.monthrange(int(y),m)[1]}'
def qstart(y,q):return f'{y}-{q*3-2:02d}-01'
def node(m,s,e):return f'{m}|{s or "snapshot"}|{e}'
def record(m,s,e,value,method,ids,formula='',source=''):
 k=node(m,s,e)
 L[k]={'node_id':k,'metric':m,'start':s,'end':e,'value':value,'unit':S[m]['unit'] if m in S else 'derived (see metric name)','method':method,'input_ids':';'.join(ids),'formula':formula,'source_url':source,'evidence':'fact_source_reported' if method=='direct' else 'derived_calculation','confidence':'high'}
 return value
def direct(m,s,e):
 rr=[x for x in D['facts'] if x['metric']==m and x['end']==e and (x['start'] is None if m in BAL else x['start']==s)]
 if not rr:return None
 # Most recent comparative, highest accuracy in same filing; preserves conflicts for audit.
 a=max(rr,key=lambda x:(x['filed'],x['precision_decimals']));prec=a['precision_decimals'];v=round(a['value'],9)
 for b in rr:
  # At most half rounding unit per number, plus binary arithmetic tolerance.
  unit=1 if S[m]['kind']=='eps' else 1e6
  tol=(10**(-a['precision_decimals'])+10**(-b['precision_decimals']))/unit/2+1e-8
  if abs(a['value']-b['value'])>tol:
   CONFLICT.append({'metric':m,'start':s,'end':e,'selected_id':a['id'],'selected_value':a['value'],'other_id':b['id'],'other_value':b['value'],'resolution':'Most recent filed comparative, highest available precision'})
 return record(m,s,e,v,'direct' if a['evidence']=='fact_source_reported' else 'explicit statement classification',[a['id']],source=a['source_url'])
def get(m,s,e):
 if m in BAL:s=None
 k=(m,s,e)
 if k in CACHE:return CACHE[k]
 v=direct(m,s,e)
 if v is not None:
  candidates=[x for x in D['facts'] if x['metric']==m and x['start']==s and x['end']==e]
  chosen=max(candidates,key=lambda x:(x['filed'],x['precision_decimals'])) if candidates else None
  prefer_precise_ytd=bool(m not in NONADD|BAL and s and s[5:]!='01-01' and chosen and chosen['precision_decimals'] < -3)
  if not prefer_precise_ytd:CACHE[k]=v;return v
 if m in NONADD or m in BAL:CACHE[k]=None;return None
 if s and s[5:]!='01-01':
  y=s[:4];mo=int(s[5:7])-1;pe=f'{y}-{mo:02d}-{calendar.monthrange(int(y),mo)[1]}'
  a=get(m,y+'-01-01',e);b=get(m,y+'-01-01',pe)
  if a is not None and b is not None:v=record(m,s,e,round(a-b,6),'YTD subtraction',[node(m,y+'-01-01',e),node(m,y+'-01-01',pe)],'current YTD - previous YTD')
 elif s and s[5:]=='01-01' and e[5:] in ['06-30','09-30']:
  # Equity statements disclose NCI distributions by quarter, not a YTD total.
  y=s[:4];n=int(e[5:7])//3;vals=[direct(m,qstart(y,q),qend(y,q)) for q in range(1,n+1)]
  if all(z is not None for z in vals):v=record(m,s,e,round(sum(vals),6),'sum directly reported additive quarters',[node(m,qstart(y,q),qend(y,q)) for q in range(1,n+1)],'sum direct quarters')
 CACHE[k]=v;return v

def addderived(r):
 def calc(name,keys,fn,formula):
  v=round(fn(*[r[k] for k in keys]),6) if all(r.get(k) is not None for k in keys) else None;r[name]=v
  if v is not None:record(name,r['start'],r['end'],v,'derived metric',[node(k,None if k in BAL else r['start'],r['end']) for k in keys],formula)
 calc('da',['depreciation','amortization_intangibles'],lambda a,b:a+b,'depreciation + intangible amortization')
 calc('fcf_gross_ppe',['cfo','capex_ppe'],lambda a,b:a-b,'CFO - gross cash PP&E capex')
 calc('fcf_company_definition',['cfo','capex_ppe','ppe_disposals_insurance_proceeds'],lambda a,b,c:a-b+c,'CFO - cash PP&E capex + PP&E disposal/insurance cash')
 calc('fcf_gross_ppe_after_sbc_proxy',['fcf_gross_ppe','sbc'],lambda a,b:a-b,'gross PP&E FCF - SBC; proxy, NOT owner earnings')
 calc('fcf_after_separate_asset_acquisitions_sbc_proxy',['fcf_gross_ppe_after_sbc_proxy','asset_acquisitions_cash_separate'],lambda a,b:a-b,'after-SBC proxy less separately identified asset acquisition cash; does not deduct business acquisitions')
 calc('debt_total_carrying',['debt_current','debt_noncurrent'],lambda a,b:a+b,'balance-sheet current + noncurrent debt')
 calc('shortterm_debt_derived',['debt_current','longterm_debt_current'],lambda a,b:a-b,'current total debt less current long-term debt')
 calc('net_debt',['debt_current','debt_noncurrent','cash'],lambda a,b,c:a+b-c,'current + noncurrent carrying debt (includes finance leases) - unrestricted cash')
 calc('operating_lease_liabilities',['operating_lease_current','operating_lease_noncurrent'],lambda a,b:a+b,'current + noncurrent operating lease liabilities; not in net_debt')
 calc('equity_unclassified_residual',['assets','liabilities','equity_total'],lambda a,b,c:a-b-c,'assets - liabilities - permanent total equity')
 wc=['wc_receivables_cash','wc_contract_assets_cash','wc_inventory_cash','wc_prepaids_other_cash','wc_payables_accruals_cash','wc_contract_liabilities_cash','wc_other_cash']
 calc('working_capital_cash_contribution',wc,lambda *v:sum(v),'sum signed changes in operating assets and liabilities')
 calc('cfo_before_working_capital',['cfo','working_capital_cash_contribution'],lambda a,b:a-b,'CFO less signed working-capital cash contribution; not normalized CFO')
 calc('ebit_margin_pct',['ebit','revenue'],lambda a,b:100*a/b,'100 * EBIT/revenue')
 calc('net_margin_attributable_pct',['ni_attributable','revenue'],lambda a,b:100*a/b,'100 * NI attributable / revenue')
 calc('cfo_to_consolidated_ni',['cfo','ni_consolidated'],lambda a,b:a/b,'CFO / consolidated NI, matching ownership perimeter')
 calc('fcf_gross_ppe_margin_pct',['fcf_gross_ppe','revenue'],lambda a,b:100*a/b,'100 * gross PP&E FCF / revenue')
 r['software_capex_separate']=None;r['redeemable_noncontrolling_interests']=None;r['preferred_equity']=None
rows=[]
periods=[(f'FY{y}',f'{y}-01-01',f'{y}-12-31') for y in [2023,2024,2025]]
periods += [(f'Q{q} {y}',qstart(y,q),qend(y,q)) for y,q in [(2024,4)]+[(2025,q) for q in range(1,5)]+[(2026,q) for q in range(1,4)]]
periods += [(f'9M {y}',f'{y}-01-01',f'{y}-09-30') for y in [2025,2026]]
for label,s,e in periods:
 r={'period':label,'start':s,'end':e,'basis':'reported consolidated; attributable NI and EPS identified separately'}
 for m in MET:r[m]=get(m,s,e)
 addderived(r);rows.append(r)
for y in [2025,2026]:
 label=f'TTM Sep {y}';s=f'{y-1}-10-01';e=f'{y}-09-30';r={'period':label,'start':s,'end':e,'basis':'calculated from reported consolidated periods'}
 for m in MET:
  if m in BAL:r[m]=get(m,None,e)
  elif m in NONADD:r[m]=None
  else:
   vals=[get(m,f'{y-1}-01-01',f'{y-1}-12-31'),get(m,f'{y}-01-01',e),get(m,f'{y-1}-01-01',f'{y-1}-09-30')]
   r[m]=round(vals[0]+vals[1]-vals[2],6) if all(x is not None for x in vals) else None
   if r[m] is not None:record(m,s,e,r[m],'TTM from reported periods',[node(m,f'{y-1}-01-01',f'{y-1}-12-31'),node(m,f'{y}-01-01',e),node(m,f'{y-1}-01-01',f'{y-1}-09-30')],'previous FY + current 9M - previous 9M')
 qs=[a for a in rows if a['period'] in [f'Q4 {y-1}',f'Q1 {y}',f'Q2 {y}',f'Q3 {y}']]
 for m in ['eps_diluted','eps_basic']:
  nm=m+'_sum_quarters_calculated';r[nm]=round(sum(a[m] for a in qs),4) if len(qs)==4 and all(a[m] is not None for a in qs) else None
  if r[nm] is not None:record(nm,s,e,r[nm],'calculated sum, not GAAP reported TTM EPS',[node(m,a['start'],a['end']) for a in qs],'sum of four directly reported quarterly EPS; no annual/cumulative EPS subtraction')
 addderived(r);rows.append(r)
# QA checks are explicit, reproducible and persisted.
def check(label,value,tol=0.00001):
 assert abs(value)<=tol,(label,value);CHECK.append({'check':label,'residual':round(value,9),'tolerance':tol,'status':'PASS'})
for r in rows:
 label=r['period']
 def identity(title,keys,fn,tol=0.00001):
  if all(r.get(k) is not None for k in keys):check(label+' '+title,fn(*[r[k] for k in keys]),tol)
 identity('NI consolidated = attributable + NCI',['ni_consolidated','ni_attributable','ni_noncontrolling'],lambda a,b,c:a-b-c)
 identity('NI consolidated = pretax - tax',['ni_consolidated','pretax_income','income_tax'],lambda a,b,c:a-b+c)
 identity('assets = liabilities + total equity',['assets','liabilities','equity_total'],lambda a,b,c:a-b-c)
 identity('total equity = parent equity + NCI',['equity_total','equity_parent','noncontrolling_interests'],lambda a,b,c:a-b-c)
 identity('long-term debt total = current long-term + noncurrent',['longterm_debt_total_including_finance_leases','longterm_debt_current','debt_noncurrent'],lambda a,b,c:a-b-c)
 identity('CFO reconciles from NI, noncash and WC',['cfo','ni_consolidated','depreciation','amortization_intangibles','sbc','other_noncash_cfo','working_capital_cash_contribution'],lambda a,*v:a-sum(v))
 identity('cash-change = CFO + CFI + CFF + FX',['cash_change_including_restricted','cfo','cfi','cff','cash_fx_effect'],lambda a,*v:a-sum(v))
 for m in ['revenue','ebit','ni_consolidated','ni_attributable','cfo','capex_ppe','sbc','depreciation','amortization_intangibles']:
  assert r[m] is not None,(label,'missing core',m)
 for m in ['cash','assets','liabilities','equity_total','noncontrolling_interests','debt_current','debt_noncurrent']:
  assert r[m] is not None,(label,'missing balance',m)
 if label.startswith('TTM'):
  assert all(r[m] is None for m in NONADD)
 else:
  assert r['eps_diluted'] is not None,(label,'missing direct diluted EPS')
for y in [2025,2026]:
 t=next(r for r in rows if r['period']==f'TTM Sep {y}');qs=[r for r in rows if r['period'] in [f'Q4 {y-1}',f'Q1 {y}',f'Q2 {y}',f'Q3 {y}']]
 for m in MET:
  if m not in BAL|NONADD and t[m] is not None and all(r[m] is not None for r in qs):check(f'{y} {m} TTM equals four quarters',t[m]-sum(r[m] for r in qs))
for y in [2024,2025]:
 q=next(r for r in rows if r['period']==f'Q4 {y}')
 for m in ['revenue','ebit','ni_consolidated','ni_attributable','ni_noncontrolling','cfo','capex_ppe','depreciation','amortization_intangibles','sbc']:
  a=get(m,f'{y}-01-01',f'{y}-12-31');b=get(m,f'{y}-01-01',f'{y}-09-30')
  if a is not None and b is not None:check(f'{y} Q4 {m} direct release equals FY less 9M',q[m]-(a-b))
 check(f'{y} direct Q4 EPS',q['eps_diluted']-({2024:2.03,2025:2.08}[y]))
check('Sep 2026 minority interests',next(r for r in rows if r['period']=='Q3 2026')['noncontrolling_interests']-86.186)
check('9M2026 contract-liability CFO contribution',next(r for r in rows if r['period']=='9M 2026')['wc_contract_liabilities_cash']-1983.686)
# Do not erase material disclosure gaps merely because accounting checks tie.
FLAGS=[{'topic':n['topic'],'severity':'interpretation','note':n['note'],'source_ids':';'.join(n['sources'])} for n in D['disclosure_notes']]
for r in rows:
 for m in MET:
  if r[m] is None and not (r['period'].startswith('TTM') and m in NONADD):FLAGS.append({'topic':r['period']+' '+m,'severity':'missing optional source','note':'Not available in selected dimension-free source facts; null retained.','source_ids':''})
OUTPUT={'issuer':D['issuer'],'ticker':'PWR','as_of':D['as_of'],'units':'USD millions except EPS USD/share, shares millions, ratios and percent as named','rows':rows,'disclosure_notes':D['disclosure_notes'],'source_index':D['sources']}
(P/'history.json').write_text(json.dumps(OUTPUT,indent=2)+'\n')
def csvout(name,rr,fields=None):
 fields=fields or list(dict.fromkeys(k for r in rr for k in r))
 with (P/name).open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rr)
csvout('history.csv',rows);csvout('ledger.csv',list(L.values()));csvout('source_index.csv',D['sources']);csvout('qa_flags.csv',FLAGS);csvout('validation_checks.csv',CHECK)
csvout('conflicts.csv',CONFLICT,['metric','start','end','selected_id','selected_value','other_id','other_value','resolution'])
(P/'qa.txt').write_text('\n'.join(f"{x['status']}: {x['check']} (residual {x['residual']})" for x in CHECK)+f'\n{len(CHECK)} accounting/period checks PASS; {len(CONFLICT)} source conflicts retained.\nCore requested series complete. Nulls/disclosure limitations are in qa_flags.csv.\n')
files=['numeric_inputs.json','rebuild_history.py','history.json','history.csv','ledger.csv','source_index.csv','qa_flags.csv','validation_checks.csv','conflicts.csv','qa.txt']
(P/'checksums.txt').write_text(''.join(hashlib.sha256((P/f).read_bytes()).hexdigest()+'  '+f+'\n' for f in files))
print(json.dumps([{k:r.get(k) for k in ['period','revenue','ebit','ni_consolidated','ni_attributable','eps_diluted','eps_diluted_sum_quarters_calculated','cfo','capex_ppe','asset_acquisitions_cash_separate','sbc','da','fcf_gross_ppe_after_sbc_proxy','net_debt']} for r in rows],indent=2))
print(f'{len(CHECK)} accounting/period checks PASS; {len(CONFLICT)} source conflicts retained.')
