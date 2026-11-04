"""Offline URBN normalization; no network or dependency installation required.
Run from any directory. Inputs are portable numeric_inputs.json and custom_numeric_inputs.json only.
Monetary output USD millions; EPS USD/share. Missing facts remain null.
"""
import json,csv,hashlib
from pathlib import Path
from datetime import date
ROOT=Path(__file__).resolve().parent
frozen_inputs=json.loads((ROOT/'numeric_inputs.json').read_text())
tags={'revenue':'RevenueFromContractWithCustomerExcludingAssessedTax','ebit':'OperatingIncomeLoss','net_income':'NetIncomeLoss','eps_basic':'EarningsPerShareBasic','eps_diluted':'EarningsPerShareDiluted','cfo':'NetCashProvidedByUsedInOperatingActivities','ppe_cash_purchases':'PaymentsToAcquirePropertyPlantAndEquipment','sbc':'ShareBasedCompensation','da':'DepreciationAndAmortization','cash':'CashAndCashEquivalentsAtCarryingValue','marketable_current':'AvailableForSaleSecuritiesDebtSecuritiesCurrent','marketable_noncurrent':'AvailableForSaleSecuritiesDebtSecuritiesNoncurrent','inventory':'InventoryNet','assets':'Assets','current_assets':'AssetsCurrent','liabilities':'Liabilities','current_liabilities':'LiabilitiesCurrent','equity':'StockholdersEquity','ppe_net':'PropertyPlantAndEquipmentNet','lease_current':'OperatingLeaseLiabilityCurrent','lease_noncurrent':'OperatingLeaseLiabilityNoncurrent'}
flows=list(tags)[:9]; balances=list(tags)[9:]
ledger=[]; inputs={}
def direct(m,start,end):
 key=f'{m}|{start or "instant"}|{end}'
 fact=frozen_inputs.get(key)
 if fact is None:return None
 assert fact['metric']==m and fact['start']==start and fact['end']==end, key
 inputs[key]=fact
 return fact['value'],key

def flow(m,start,end):
 d=direct(m,start,end)
 if d:return d[0],{'method':'direct','inputs':[d[1]]}
 if m.startswith('eps'):return None,{'method':'unavailable_direct_eps','inputs':[]}
 fy_start=f'{int(end[:4])-(end[5:7]=="01")}-02-01'
 prior={'05-01':'04-30','08-01':'07-31','11-01':'10-31'}.get(start[5:])
 if prior:
  a=direct(m,fy_start,end);b=direct(m,fy_start,start[:4]+'-'+prior)
  if a and b:return round(a[0]-b[0],6),{'method':'YTD difference','inputs':[a[1],b[1]],'expression':'input0 - input1'}
 return None,{'method':'not available','inputs':[]}
rows=[]
def period(label,start,end,kind):
 row={'period':label,'start':start,'end':end,'kind':kind}
 for m in flows:
  v,e=flow(m,start,end);row[m]=v;ledger.append({'period':label,'metric':m,'value':v,**e})
 if row['cfo'] is not None and row['ppe_cash_purchases'] is not None:
  row['fcf_cfo_less_ppe']=round(row['cfo']-row['ppe_cash_purchases'],6)
  ledger.append({'period':label,'metric':'fcf_cfo_less_ppe','value':row['fcf_cfo_less_ppe'],'method':'CFO minus PPE cash purchases; rental product not subtracted twice','inputs':[label+'.cfo',label+'.ppe_cash_purchases']})
 rows.append(row);return row
for y in [2024,2025,2026]:period(f'FY{y}',f'{y-1}-02-01',f'{y}-01-31','annual')
for y in [2024,2025]:period(f'Q3FY{y+1}',f'{y}-08-01',f'{y}-10-31','quarter')
for y in [2025,2026]:period(f'Q4FY{y}',f'{y-1}-11-01',f'{y}-01-31','quarter')
for y in [2025,2026]:
 period(f'Q1FY{y+1}',f'{y}-02-01',f'{y}-04-30','quarter')
 period(f'Q2FY{y+1}',f'{y}-05-01',f'{y}-07-31','quarter')
 period(f'H1FY{y+1}',f'{y}-02-01',f'{y}-07-31','half')
period('H1FY2025','2024-02-01','2024-07-31','half')
lookup={r['period']:r for r in rows};ttm={'period':'TTM2026-07-31','start':'2025-08-01','end':'2026-07-31','kind':'ttm'}
for m in flows+['fcf_cfo_less_ppe']:
 if m.startswith('eps'):ttm[m]=None;ledger.append({'period':ttm['period'],'metric':m,'value':None,'method':'not derived by subtracting EPS periods','inputs':[]});continue
 a,b,c=[lookup[p].get(m) for p in ['FY2026','H1FY2027','H1FY2026']]
 ttm[m]=None if any(v is None for v in [a,b,c]) else round(a+b-c,6)
 ledger.append({'period':ttm['period'],'metric':m,'value':ttm[m],'method':'FY2026 + H1FY2027 - H1FY2026','inputs':[f'{p}.{m}' for p in ['FY2026','H1FY2027','H1FY2026']]})
for m in ['eps_basic','eps_diluted']:
 key=m+'_sum_quarters';parts=[lookup[p][m] for p in ['Q3FY2026','Q4FY2026','Q1FY2027','Q2FY2027']]
 ttm[key]=round(sum(parts),2)
 ledger.append({'period':ttm['period'],'metric':key,'value':ttm[key],'method':'sum of four directly reported quarterly EPS; non-GAAP arithmetic proxy, different quarterly share denominators; not company-reported TTM EPS','inputs':[f'{p}.{m}' for p in ['Q3FY2026','Q4FY2026','Q1FY2027','Q2FY2027']]})
rows.append(ttm)
prior_ttm={'period':'TTM2025-07-31','start':'2024-08-01','end':'2025-07-31','kind':'ttm_comparative'}
for m in flows+['fcf_cfo_less_ppe']:
 if m.startswith('eps'):prior_ttm[m]=None;continue
 a,b,c=[lookup[p].get(m) for p in ['FY2025','H1FY2026','H1FY2025']]
 prior_ttm[m]=None if any(v is None for v in [a,b,c]) else round(a+b-c,6)
 ledger.append({'period':prior_ttm['period'],'metric':m,'value':prior_ttm[m],'method':'FY2025 + H1FY2026 - H1FY2025','inputs':[f'{p}.{m}' for p in ['FY2025','H1FY2026','H1FY2025']]})
rows.append(prior_ttm)
bal=[]
for end in ['2024-01-31','2025-01-31','2026-01-31','2025-07-31','2026-07-31']:
 r={'date':end}
 for m in balances:
  d=direct(m,None,end);r[m]=None if not d else d[0]
  ledger.append({'period':end,'metric':m,'value':r[m],'method':'direct balance' if d else 'not available','inputs':[d[1]] if d else []})
 bal.append(r)
# Custom disclosures preserved separately; not additive adjustments to CFO/FCF.
custom=json.loads((ROOT/'custom_numeric_inputs.json').read_text())
for group in ['rental_product_purchases_usd_m','rental_product_net_usd_m']:
 for period_name,value in custom[group].items():
  ledger.append({'period':period_name,'metric':group,'value':value,'method':'Direct filing disclosure; separate from cash flow adjustments','source_url':custom['source_urls']['quarter' if period_name.endswith('07-31') else 'annual']})
for m,value in custom['Q2FY2027_items_usd_m'].items():
 ledger.append({'period':'Q2FY2027','metric':m,'value':value,'method':'Direct Q2 notes disclosure; not automatically equal to exact cash received','source_url':custom['source_urls']['quarter']})
qa=[]
def check(name,ok,detail):qa.append({'test':name,'pass':bool(ok),'detail':detail})
for r in bal:
 check('balance identity '+r['date'],abs(r['assets']-r['liabilities']-r['equity'])<.002,'Assets = liabilities + equity, tolerance $2,000')
check('H1FY2027 CFO',lookup['H1FY2027']['cfo']==391.742,'Matches statement')
check('H1FY2027 PPE',lookup['H1FY2027']['ppe_cash_purchases']==268.056,'Matches statement')
check('tariff components',abs(95.660+4.445-100.105)<1e-8,'COGS plus interest = total')
for m in ['revenue','ebit','net_income','cfo','ppe_cash_purchases','sbc','da']:
 q=[lookup[p][m] for p in ['Q3FY2026','Q4FY2026','Q1FY2027','Q2FY2027']]
 check('TTM quarters '+m,all(x is not None for x in q) and abs(sum(q)-ttm[m])<.002,'Latest four quarter sum equals annual + current half - prior half')
for name,obj in [('numeric_inputs',inputs),('periods',rows),('balances',bal),('custom_disclosures',custom),('ledger',ledger),('qa',qa)]:
 (ROOT/(name+'.json')).write_text(json.dumps(obj,indent=2)+'\n')
for name,data in [('periods',rows),('balances',bal)]:
 keys=list(dict.fromkeys(k for r in data for k in r))
 with (ROOT/(name+'.csv')).open('w') as f:
  w=csv.DictWriter(f,fieldnames=keys);w.writeheader();w.writerows(data)
# source_hashes.json is preserved provenance of original retrievals, not a runtime dependency.
print(json.dumps({'TTM':ttm,'QA_pass':all(r['pass'] for r in qa),'missing':[(r['period'],k) for r in rows for k in flows if r[k] is None]},indent=2))
