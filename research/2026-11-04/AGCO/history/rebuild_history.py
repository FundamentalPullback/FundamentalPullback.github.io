#!/usr/bin/env python3
"""Offline stdlib rebuild. Inputs contain numeric SEC facts only; no network/HTML required."""
import json,csv,pathlib,calendar
P=pathlib.Path(__file__).parent; D=json.load(open(P/'numeric_inputs.json')); F=D['facts']; LED=[]
MAP={'sales':'RevenueFromContractWithCustomerExcludingAssessedTax','ebit_reported':'OperatingIncomeLoss','ni_attributable':'NetIncomeLoss','eps_diluted':'EarningsPerShareDiluted','cfo':'NetCashProvidedByUsedInOperatingActivities','capex_ppe':'PaymentsToAcquirePropertyPlantAndEquipment','sbc':'ShareBasedCompensation','depreciation':'Depreciation','amortization':'AmortizationOfIntangibleAssets','cash':'CashAndCashEquivalentsAtCarryingValue','debt_current':'DebtCurrent','debt_noncurrent':'LongTermDebtNoncurrent','assets':'Assets','liabilities':'Liabilities','equity':'StockholdersEquity','redeemable_nci':'RedeemableNoncontrollingInterestEquityCarryingAmount','inventory':'InventoryNet','current_assets':'AssetsCurrent','current_liabilities':'LiabilitiesCurrent','goodwill':'Goodwill','intangibles':'IntangibleAssetsNetExcludingGoodwill','diluted_shares':'WeightedAverageNumberOfDilutedSharesOutstanding','affiliate_earnings':'IncomeLossFromEquityMethodInvestments'}
BAL=set(['cash','debt_current','debt_noncurrent','assets','liabilities','equity','redeemable_nci','inventory','current_assets','current_liabilities','goodwill','intangibles'])
def url(r): return 'https://www.sec.gov/Archives/edgar/data/880266/'+r['accn'].replace('-','')+'/'
def get(m,s,e,label):
 for r in D['manual']:
  if r['metric']==m and r['start']==s and r['end']==e:
   LED.append(dict(period=label,metric=m,value=r['val'],unit='USD/share',method='direct release',start=s,end=e,tag='manual direct diluted EPS',source=r['source']));return r['val']
 t=MAP[m]; unit='USD/shares' if m=='eps_diluted' else 'shares' if m=='diluted_shares' else 'USD'
 rs=[r for r in F.get(t,{}).get(unit,[]) if r['end']==e and (m in BAL or r.get('start')==s)]
 if not rs and m=='sales':rs=[r for r in F.get('SalesRevenueGoodsNet',{}).get(unit,[]) if r['end']==e and r.get('start')==s]
 if rs:
  r=max(rs,key=lambda r:(r['filed'],r['accn']));v=r['val']/(1 if m=='eps_diluted' else 1e6)
  LED.append(dict(period=label,metric=m,value=v,unit='USD/share' if m=='eps_diluted' else 'million shares' if m=='diluted_shares' else 'USD million',method='direct',start=s,end=e,tag=t,source=url(r)));return v
 if s and s[5:]!='01-01' and m not in ('eps_diluted','diluted_shares') and m not in BAL:
  year=s[:4]; month=int(s[5:7])-1; prev=f'{year}-{month:02d}-{calendar.monthrange(int(year),month)[1]}'
  a=get(m,year+'-01-01',e,label+' YTD');b=get(m,year+'-01-01',prev,label+' prior YTD')
  if a is not None and b is not None:
   v=round(a-b,6);LED.append(dict(period=label,metric=m,value=v,unit='USD million',method='YTD less prior YTD',start=s,end=e,tag=t,source=f'{label} YTD - {label} prior YTD'));return v
 return None
def derived(row):
 def calc(k,keys,fn):row[k]=round(fn(*[row[x] for x in keys]),6) if all(row.get(x) is not None for x in keys) else None
 calc('da',['depreciation','amortization'],lambda a,b:a+b)
 calc('fcf_ppe_proxy',['cfo','capex_ppe'],lambda a,b:a-b)
 calc('fcf_after_sbc_proxy',['cfo','capex_ppe','sbc'],lambda a,b,c:a-b-c)
 calc('ebit_margin_pct',['ebit_reported','sales'],lambda a,b:100*a/b)
 if 'cash' in row:
  calc('debt_carrying',['debt_current','debt_noncurrent'],lambda a,b:a+b)
  calc('net_debt_carrying',['debt_current','debt_noncurrent','cash'],lambda a,b,c:a+b-c)
 row['software_capex_separate']=None
 row['software_note']='Not separately disclosed in reviewed cash-flow statements; do not assume zero. FCF is CFO less reported PPE purchases.'
rows=[]
for y in range(2019,2026):
 l=f'FY{y}';r={'period':l,'start':f'{y}-01-01','end':f'{y}-12-31'}
 for m in MAP:r[m]=get(m,r['start'],r['end'],l)
 derived(r);rows.append(r)
for y,q in [(2024,4)]+[(2025,q) for q in range(1,5)]+[(2026,q) for q in range(1,4)]:
 a=3*q-2;b=q*3;l=f'Q{q} {y}';r={'period':l,'start':f'{y}-{a:02d}-01','end':f'{y}-{b:02d}-{calendar.monthrange(y,b)[1]}'}
 for m in MAP:r[m]=get(m,r['start'],r['end'],l)
 derived(r);rows.append(r)
for y in [2025,2026]:
 l=f'TTM Sep {y}';r={'period':l,'start':f'{y-1}-10-01','end':f'{y}-09-30'}
 for m in MAP:
  if m in BAL:r[m]=get(m,None,r['end'],l)
  elif m in ['eps_diluted','diluted_shares']:r[m]=None
  else:
   a=get(m,f'{y-1}-01-01',f'{y-1}-12-31',l+' prior FY');b=get(m,f'{y}-01-01',r['end'],l+' current 9M');c=get(m,f'{y-1}-01-01',f'{y-1}-09-30',l+' prior 9M')
   r[m]=round(a+b-c,6) if all(v is not None for v in [a,b,c]) else None
 if y in [2025,2026]:
  qs=[x for x in rows if x['period'] in [f'Q4 {y-1}',f'Q1 {y}',f'Q2 {y}',f'Q3 {y}']]
  r['eps_diluted_sum_quarters']=round(sum(x['eps_diluted'] for x in qs),4)
 r['eps_note']='TTM diluted EPS not a reported measure; sum of directly reported quarterly EPS shown separately where available.'
 derived(r);rows.append(r)
for r in rows:
 for m in ['da','fcf_ppe_proxy','fcf_after_sbc_proxy','ebit_margin_pct','debt_carrying','net_debt_carrying','eps_diluted_sum_quarters']:
  if r.get(m) is not None: LED.append(dict(period=r['period'],metric=m,value=r[m],unit='see history units',method='derived; see script formula',start=r['start'],end=r['end'],tag='',source='underlying ledger facts'))
 if r['period'].startswith('TTM'):
  for m in MAP:
   if m not in BAL and r.get(m) is not None: LED.append(dict(period=r['period'],metric=m,value=r[m],unit='USD million',method='prior FY + current 9M - prior 9M',start=r['start'],end=r['end'],tag=MAP[m],source='underlying three period ledger facts'))
json.dump({'as_of':D['as_of'],'units':'USD million except EPS, shares million, ratios percent','rows':rows},open(P/'history.json','w'),indent=2)
with open(P/'ledger.csv','w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=['period','metric','value','unit','method','start','end','tag','source']);w.writeheader();w.writerows(LED)
with open(P/'history.csv','w',newline='') as f:
 keys=list(dict.fromkeys(k for r in rows for k in r));w=csv.DictWriter(f,fieldnames=keys);w.writeheader();w.writerows(rows)
qa=[]
for r in rows:
 if all(r.get(k) is not None for k in ['assets','liabilities','equity','redeemable_nci']):
  err=round(r['assets']-r['liabilities']-r['equity']-r['redeemable_nci'],5);qa.append(f"{r['period']}: assets minus liabilities/equity/redeemable NCI = {err}");assert abs(err)<=0.21
for m in ['sales','ebit_reported','ni_attributable','cfo','capex_ppe','sbc','da']:
 t=next(x for x in rows if x['period']=='TTM Sep 2026')[m];s=sum(x[m] for x in rows if x['period'] in ['Q4 2025','Q1 2026','Q2 2026','Q3 2026']);assert abs(t-s)<0.01;qa.append(f'TTM {m}: four-quarter sum reconciles {t}')
(P/'qa.txt').write_text('\n'.join(qa)+'\nPASS\n')
print(json.dumps([r for r in rows if r['period'] in ['FY2023','FY2024','FY2025','TTM Sep 2026']],indent=2))

bridge=[dict(r) for r in D['limited_bridge_inputs']]
for year in [2025,2026]:
 q=next(r for r in bridge if r['period']==f'Q4 {year-1}');n=next(r for r in bridge if r['period']==f'9M{year}')
 bridge.append(dict(period=f'TTM Sep {year}',ebit=round(q['ebit']+n['ebit'],4),impairment=round(q['impairment']+n['impairment'],4),loss_on_business_sale=round(q['loss_on_business_sale']+n['loss_on_business_sale'],4),source=f"Q4 {year-1} + 9M{year}; component sources above"))
for r in bridge:r['ebit_ex_only_impairment_business_sale']=round(r['ebit']+r['impairment']+r['loss_on_business_sale'],4)
json.dump({'note':'Limited diagnostic bridge only. Not normalized EBIT. Retains SBC, acquired intangible amortization, restructuring, transaction costs and tariff refunds. Positive sale loss added; sale gain subtracted. No tax effects or nonoperating gains included.','rows':bridge},open(P/'limited_ebit_bridge.json','w'),indent=2)
