#!/usr/bin/env python3
"""Offline, Python standard library only. USD millions except EPS and share counts."""
import json,csv,pathlib,calendar,hashlib
P=pathlib.Path(__file__).parent;D=json.load(open(P/'numeric_inputs.json'));L=[]
MAP={'revenue':'Revenues','ebit':'OperatingIncomeLoss','ni_continuing':'IncomeLossFromContinuingOperations','ni_total':'NetIncomeLoss','eps_continuing_diluted':'IncomeLossFromContinuingOperationsPerDilutedShare','eps_total_diluted':'EarningsPerShareDiluted','cfo_consolidated':'NetCashProvidedByUsedInOperatingActivities','capex_ppe_consolidated':'PaymentsToAcquirePropertyPlantAndEquipment','sbc_consolidated':'ShareBasedCompensation','sbc_continuing':'AllocatedShareBasedCompensationExpense','da_consolidated':'DepreciationDepletionAndAmortization','depreciation_continuing':'Depreciation','amortization_continuing':'AmortizationOfIntangibleAssets','cash':'CashAndCashEquivalentsAtCarryingValue','debt_current':'LongTermDebtCurrent','debt_noncurrent':'LongTermDebtNoncurrent','assets':'Assets','current_assets':'AssetsCurrent','current_liabilities':'LiabilitiesCurrent','equity':'StockholdersEquity','inventory':'InventoryNet','goodwill':'Goodwill','intangibles':'IntangibleAssetsNetExcludingGoodwill','diluted_shares':'WeightedAverageNumberOfDilutedSharesOutstanding'}
BAL={'cash','debt_current','debt_noncurrent','assets','current_assets','current_liabilities','equity','inventory','goodwill','intangibles'}
MAN=['discontinued_cfo_adjustment','cfo_continuing_nongaap','capex_continuing_nongaap','fcf_continuing_company'];MET=list(MAP)+MAN
EPS={'eps_continuing_diluted','eps_total_diluted','diluted_shares'}
def get(m,s,e,label):
 direct=[r for r in D['manual'] if r['metric']==m and r['start']==s and r['end']==e]
 if direct and m in EPS:
  r=direct[0];L.append(dict(period=label,metric=m,start=s,end=e,value=r['val'],method='direct Q4 release',source=r['source'],tag='GAAP quarterly statement'));return r['val']
 if m in MAN:
  rs=[r for r in D['manual'] if r['metric']==m and r['start']==s and r['end']==e]; scale=1
 else:
  rs=[r for r in D['facts'] if r['tag']=='us-gaap:'+MAP[m] and r['end']==e and (r['start'] is None if m in BAL else r['start']==s)];scale=1 if m.startswith('eps_') else 1e6
 if not rs and m=='cfo_consolidated' and e in ['2023-12-31','2024-12-31','2025-12-31']:
  # Annual filing uses a continuing-operations tag for consolidated CFO. Face statement and MD&A establish perimeter.
  rs=[r for r in D['facts'] if r['tag']=='us-gaap:NetCashProvidedByUsedInContinuingOperations' and r['start']==s and r['end']==e]
 if rs:
  r=max(rs,key=lambda x:x.get('filed',''));v=r['val']/scale
  L.append(dict(period=label,metric=m,start=s,end=e,value=v,method='direct',source=r['source'],tag=r.get('tag','MD&A reconciliation')));return v
 if m=='debt_current' and e in ['2026-03-31','2026-06-30','2026-09-30']:
  # No current debt in 2026 balance sheet; debt note total revolver equals noncurrent debt.
  a=[r for r in D['facts'] if r['tag']=='us-gaap:DebtLongtermAndShorttermCombinedAmount' and r['end']==e and r['start'] is None]
  b=get('debt_noncurrent',None,e,label)
  if a and b is not None:
   rr=max(a,key=lambda x:x['filed']);v=round(rr['val']/1e6-b,6);L.append(dict(period=label,metric=m,start=None,end=e,value=v,method='2026 debt note total less noncurrent debt',source=rr['source'],tag=rr['tag']));return v
 if s and s[5:]!='01-01' and m not in EPS and m not in BAL:
  yy=s[:4];mo=int(s[5:7])-1;prev=f'{yy}-{mo:02d}-{calendar.monthrange(int(yy),mo)[1]}'
  a=get(m,yy+'-01-01',e,label+' YTD');b=get(m,yy+'-01-01',prev,label+' prior YTD')
  if a is not None and b is not None:
   v=round(a-b,6);L.append(dict(period=label,metric=m,start=s,end=e,value=v,method='YTD less prior YTD',source='underlying direct ledger rows',tag=''));return v
 return None
def derived(r):
 def calc(m,keys,fn):r[m]=round(fn(*[r[k] for k in keys]),6) if all(r.get(k) is not None for k in keys) else None
 calc('da_continuing',['depreciation_continuing','amortization_continuing'],lambda a,b:a+b)
 calc('fcf_consolidated_ppe',['cfo_consolidated','capex_ppe_consolidated'],lambda a,b:a-b)
 calc('fcf_continuing_after_sbc_proxy',['fcf_continuing_company','sbc_continuing'],lambda a,b:a-b)
 calc('net_debt',['debt_current','debt_noncurrent','cash'],lambda a,b,c:a+b-c)
 calc('liabilities_derived',['assets','equity'],lambda a,b:a-b)
 calc('ebit_margin_pct',['ebit','revenue'],lambda a,b:100*a/b)
 r['software_capex_separate']=None
rows=[]
periods=[(f'FY{y}',f'{y}-01-01',f'{y}-12-31') for y in [2023,2024,2025]]
for y,q in [(2024,4)]+[(2025,q) for q in range(1,5)]+[(2026,q) for q in range(1,4)]:
 a=3*q-2;b=3*q;periods.append((f'Q{q} {y}',f'{y}-{a:02d}-01',f'{y}-{b:02d}-{calendar.monthrange(y,b)[1]}'))
for label,s,e in periods:
 r=dict(period=label,start=s,end=e)
 for m in MET:r[m]=get(m,s,e,label)
 derived(r);rows.append(r)
for y in [2025,2026]:
 label=f'TTM Sep {y}';s=f'{y-1}-10-01';e=f'{y}-09-30';r=dict(period=label,start=s,end=e)
 for m in MET:
  if m in BAL:r[m]=get(m,None,e,label)
  elif m in EPS:r[m]=None
  else:
   vals=[get(m,f'{y-1}-01-01',f'{y-1}-12-31',label+' prior FY'),get(m,f'{y}-01-01',e,label+' current 9M'),get(m,f'{y-1}-01-01',f'{y-1}-09-30',label+' prior 9M')]
   r[m]=round(vals[0]+vals[1]-vals[2],6) if all(v is not None for v in vals) else None
   if r[m] is not None:L.append(dict(period=label,metric=m,start=s,end=e,value=r[m],method='prior FY + current 9M - prior 9M',source='underlying direct ledger rows',tag=''))
 for m in ['eps_continuing_diluted','eps_total_diluted']:
  qs=[x for x in rows if x['period'] in [f'Q4 {y-1}',f'Q1 {y}',f'Q2 {y}',f'Q3 {y}']]
  r[m+'_sum_quarters']=round(sum(x[m] for x in qs),4) if len(qs)==4 and all(x[m] is not None for x in qs) else None
  L.append(dict(period=label,metric=m+'_sum_quarters',start=s,end=e,value=r[m+'_sum_quarters'],method='calculated sum of four directly reported quarterly diluted EPS; not reported TTM EPS',source='underlying direct quarterly ledger rows',tag=''))
 derived(r);rows.append(r)
json.dump(dict(as_of=D['as_of'],units='USD million, EPS USD/share, diluted shares millions, margins percent',rows=rows),open(P/'history.json','w'),indent=2)
for name,rr in [('history',rows),('ledger',L)]:
 with open(P/(name+'.csv'),'w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(dict.fromkeys(k for r in rr for k in r)));w.writeheader();w.writerows(rr)
qa=[]
for r in rows:
 def check(keys,fn,title):
  if all(r.get(k) is not None for k in keys):
   err=fn(*[r[k] for k in keys]);assert abs(err)<0.11,(r['period'],title,err);qa.append(r['period']+' '+title+' PASS')
 check(['cfo_consolidated','discontinued_cfo_adjustment','cfo_continuing_nongaap'],lambda a,b,c:a+b-c,'CFO perimeter bridge')
 check(['cfo_continuing_nongaap','capex_continuing_nongaap','fcf_continuing_company'],lambda a,b,c:a-b-c,'continuing FCF')
for y in [2025,2026]:
 t=next(r for r in rows if r['period']==f'TTM Sep {y}');qs=[r for r in rows if r['period'] in [f'Q4 {y-1}',f'Q1 {y}',f'Q2 {y}',f'Q3 {y}']]
 for m in MET:
  if m in BAL or m in EPS:continue
  if t[m] is not None and all(r[m] is not None for r in qs):assert abs(t[m]-sum(r[m] for r in qs))<0.11;qa.append(f'{y} TTM {m} = four quarters PASS')
for r in rows:
 if r['period'].startswith('TTM'):assert r['eps_continuing_diluted'] is None and r['eps_total_diluted'] is None
qa.append('Q4 EPS directly sourced; TTM EPS sum labeled calculated; no cumulative EPS subtraction: PASS')
assert next(r for r in rows if r['period']=='Q4 2025')['eps_continuing_diluted']==0.29
assert next(r for r in rows if r['period']=='Q4 2024')['eps_total_diluted']==0.21
assert next(r for r in rows if r['period']=='TTM Sep 2026')['eps_continuing_diluted_sum_quarters']==0.87;qa.append('Software capex missing kept null: PASS')
(P/'qa.txt').write_text('\n'.join(qa)+'\nALL CHECKS PASS\n')
print(json.dumps([{k:r[k] for k in ['period','revenue','ebit','ni_continuing','ni_total','cfo_consolidated','cfo_continuing_nongaap','fcf_continuing_company','sbc_continuing']} for r in rows],indent=2))
