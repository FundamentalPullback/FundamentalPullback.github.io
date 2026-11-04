#!/usr/bin/env python3
'''Offline stdlib-only. Regenerate normalized schedules from the compact numeric source ledger.'''
import json,csv,pathlib
P=pathlib.Path(__file__).resolve().parent
L=json.loads((P/'source_ledger.json').read_text()); rows=[]; checks=[]; flags=[]
FLOW=['revenue','ebit_reported','net_income','eps_basic','eps_diluted','cfo','ppe_cash_capex','intangible_cash_capex','sbc_cashflow','sbc_pnl','da','acquired_amortization','sbc_plus_related_expense','sbc_tax_benefit','tax_expense','pretax_income','cash_tax_paid','acquisitions_cash','ppe_extended_terms_financing_cash']
BAL=['cash','short_term_investments','assets','liabilities','equity','current_assets','current_liabilities','inventory','receivables','ppe_net','acquired_intangibles_net','goodwill','deferred_tax_assets_net','deferred_tax_liabilities','utb']
def exact(m,s,e):
 a=[r for r in L if r['metric']==m and r['start']==s and r['end']==e]
 if not a:return None
 r=max(a,key=lambda x:x['filed']);return dict(value=r['value'],sources=[r['source_id']],source_urls=[r['source_url']],method='direct reported',unit=r['unit'])
def calc(items,signs,method):
 if any(v is None for v in items):return None
 return dict(value=round(sum(v['value']*s for v,s in zip(items,signs)),6),sources=sorted(set(x for v in items for x in v['sources'])),source_urls=sorted(set(x for v in items for x in v['source_urls'] if x)),method=method,unit=items[0]['unit'])
def period(m,s,e):
 v=exact(m,s,e)
 if v:return v
 if m.startswith('eps'):return None # NEVER subtract annual or YTD EPS
 y=e[:4]
 if s[5:] in ['04-01','07-01','10-01']:
  prev={'04-01':'03-31','07-01':'06-30','10-01':'09-30'}[s[5:]]
  # Q2 acquired amort and payroll can use 9M minus Q1 minus Q3
  if s[5:]=='04-01' and m in ['acquired_amortization','sbc_plus_related_expense']:
   return calc([exact(m,y+'-01-01',y+'-09-30'),exact(m,y+'-01-01',y+'-03-31'),exact(m,y+'-07-01',y+'-09-30')],[1,-1,-1],'9M - Q1 - Q3')
  return calc([exact(m,y+'-01-01',e),exact(m,y+'-01-01',y+'-'+prev)],[1,-1],'FY minus 9M' if s[5:]=='10-01' else 'YTD difference')
 return None
def emit(label,m,s,e,v):
 rows.append(dict(period=label,metric=m,start=s,end=e,value=v['value'] if v else None,unit=v['unit'] if v else ('USD/shares' if m.startswith('eps') else 'USD'),evidence='missing_required_source' if v is None else ('fact_source_reported' if v['method']=='direct reported' else 'derived_calculation'),method=v['method'] if v else 'not separately disclosed or corrected direct source unavailable',source_ids=';'.join(v['sources']) if v else '',source_urls=';'.join(v['source_urls']) if v else ''))
periods=[(f'FY{y}',f'{y}-01-01',f'{y}-12-31') for y in [2023,2024,2025]]+[(f'Q{q}_{y}',f'{y}-{(q-1)*3+1:02d}-01',f'{y}-'+{1:'03-31',2:'06-30',3:'09-30',4:'12-31'}[q]) for y,qs in [(2024,[4]),(2025,[1,2,3,4]),(2026,[1,2,3])] for q in qs] + [(f'9M{y}',f'{y}-01-01',f'{y}-09-30') for y in [2024,2025,2026]]
for label,s,e in periods:
 for m in FLOW:emit(label,m,s,e,period(m,s,e))
for y in [2025,2026]:
 for m in FLOW:
  # EPS TTM is sum of four directly disclosed quarters, never FY+YTD-YTD.
  if m.startswith('eps'):
   v=calc([period(m,f'{y-1}-10-01',f'{y-1}-12-31')]+[period(m,f'{y}-{3*(q-1)+1:02d}-01',f'{y}-'+{1:'03-31',2:'06-30',3:'09-30'}[q]) for q in [1,2,3]],[1]*4,'sum of four direct quarterly EPS (rounded, not reported TTM EPS)')
  else:v=calc([exact(m,f'{y-1}-01-01',f'{y-1}-12-31'),exact(m,f'{y}-01-01',f'{y}-09-30'),exact(m,f'{y-1}-01-01',f'{y-1}-09-30')],[1,1,-1],'prior FY + current 9M - prior 9M')
  if v is None and m in ['acquired_amortization','sbc_plus_related_expense']:
   v=calc([exact(m,f'{y-1}-10-01',f'{y-1}-12-31'),exact(m,f'{y}-01-01',f'{y}-09-30')],[1,1],'prior Q4 + current 9M')
  emit(f'TTM_September_{y}',m,f'{y-1}-10-01',f'{y}-09-30',v)
emit('Q4_2025','net_income_direct_rounded','2025-10-01','2025-12-31',exact('net_income_direct_rounded','2025-10-01','2025-12-31'))
for e in ['2024-12-31','2025-12-31','2026-09-30']:
 for m in BAL:emit('BS_'+e,m,None,e,exact(m,None,e))
for label,_,_ in periods+[(f'TTM_September_{y}',None,None) for y in [2025,2026]]:
 d={r['metric']:r for r in rows if r['period']==label}
 for metric,components,signs in [('fcf_ppe_only',['cfo','ppe_cash_capex'],[1,-1]),('fcf_ppe_intangibles',['cfo','ppe_cash_capex','intangible_cash_capex'],[1,-1,-1]),('fcf_ppe_extended_terms',['cfo','ppe_cash_capex','ppe_extended_terms_financing_cash'],[1,-1,-1]),('fcf_ppe_less_equity_sbc',['cfo','ppe_cash_capex','sbc_cashflow'],[1,-1,-1])]:
  vals=[d[x] for x in components];ok=all(v['value'] is not None for v in vals)
  base=dict(vals[0]);base.update(metric=metric,value=round(sum(v['value']*s for v,s in zip(vals,signs)),6) if ok else None,evidence='derived_calculation' if ok else 'missing_required_source',method=' + '.join(f'{s}*{c}' for c,s in zip(components,signs)),source_ids=';'.join(sorted(set(';'.join(v['source_ids'] for v in vals).split(';')))),source_urls=';'.join(sorted(set(';'.join(v['source_urls'] for v in vals).split(';')))));rows.append(base)
for y in [2024,2025]:
 vals=[exact(m,None,f'{y}-12-31') for m in ['assets','liabilities','equity']];checks.append(dict(check=f'FY{y} balance sheet',result='PASS' if vals[0]['value']==vals[1]['value']+vals[2]['value'] else 'FAIL'))
checks.append(dict(check='No quarterly EPS derived from subtraction',result='PASS' if all('difference' not in r['method'] and 'minus' not in r['method'] for r in rows if r['metric'].startswith('eps')) else 'FAIL'))
checks.append(dict(check='FY24 latest restated NI and EPS',result='PASS' if exact('net_income','2024-01-01','2024-12-31')['value']==1592058000 and exact('eps_diluted','2024-01-01','2024-12-31')['value']==32.60 else 'FAIL'))
checks.append(dict(check='Q4 2025 corrected direct diluted EPS',result='PASS' if period('eps_diluted','2025-10-01','2025-12-31')['value']==3.49 else 'FAIL'))
for e in ['2025-12-31','2026-09-30']:
 s=e[:4]+'-01-01';a=exact('sbc_cashflow',s,e);b=exact('sbc_pnl',s,e);checks.append(dict(check=f'{e} SBC CF equals P&L',result='PASS' if a['value']==b['value'] else 'FAIL'))
for r in rows:
 if r['value'] is None:flags.append(dict(period=r['period'],metric=r['metric'],flag='missing_required_source',severity='warning'))
(P/'normalized_history.json').write_text(json.dumps(rows,indent=2)+'\n');(P/'validation_checks.json').write_text(json.dumps(checks,indent=2)+'\n');(P/'qa_flags.json').write_text(json.dumps(flags,indent=2)+'\n')
def csvout(name,rs):
 with (P/name).open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rs[0]));w.writeheader();w.writerows(rs)
csvout('normalized_history.csv',rows);csvout('validation_checks.csv',checks);csvout('qa_flags.csv',flags)
labels=list(dict.fromkeys(r['period'] for r in rows));metrics=list(dict.fromkeys(r['metric'] for r in rows));lookup={(r['period'],r['metric']):r['value'] for r in rows};csvout('history_wide.csv',[dict(metric=m,**{p:lookup.get((p,m)) for p in labels}) for m in metrics])
print(json.dumps({'rows':len(rows),'checks':checks,'missing':len(flags)},indent=2))
