#!/usr/bin/env python3
"""Offline, stdlib-only reproducible GPC bridge. All amounts USD millions except EPS.
No network or dependencies. Run in any directory. Outputs beside this script.
"""
import json,csv
from pathlib import Path
P=Path(__file__).resolve().parent
facts=json.loads((P/'source_numeric_facts.json').read_text()) + json.loads((P/'manual_numeric_facts.json').read_text())
MAP={'revenue':'RevenueFromContractWithCustomerExcludingAssessedTax','gross_profit':'GrossProfit','opex':'OperatingExpenses','da':'DepreciationAndAmortization','sbc':'ShareBasedCompensation','cfo':'NetCashProvidedByUsedInOperatingActivities','capex':'PaymentsToAcquirePropertyPlantAndEquipment','acquisition_cash':'PaymentsToAcquireBusinessesAndInterestInAffiliates','acquired_intangible_amortization':'AmortizationOfIntangibleAssets','interest_net':'InterestExpenseNonoperating','ebt':'IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest','tax':'IncomeTaxExpenseBenefit','net_income':'NetIncomeLoss','restructuring':'RestructuringCharges','pension_settlement':'PensionSettlementChargeNonoperating','ar_sales':'AccountsReceivableSale','ar_collections':'ProceedsFromSaleOfAccountReceivable','ar_fees':'AccountsReceivableSalesTransactionsFees','restructuring_cash_payments':'PaymentsForRestructuring','diluted_shares':'WeightedAverageNumberOfDilutedSharesOutstanding','eps_diluted':'EarningsPerShareDiluted'}
def extract(start,end):
 out={};src={}
 for k,t in MAP.items():
  xs=[x for x in facts if x['tag'].split(':')[-1]==t and x['start']==start and x['end']==end]
  if xs:
   x=max(xs,key=lambda z:(z['source_date'],99 if z['decimals']=='INF' else int(z['decimals'])))
   out[k]=x['value'] if k=='eps_diluted' else x['value']/1e6;src[k]={v:x[v] for v in ['url','fact_id','tag','start','end','value']}
  else:out[k]=None
 return out,src
raw={};evidence={}
for yr in [2023,2024,2025]:
 k=f'FY{yr}';raw[k],evidence[k]=extract(f'{yr}-01-01',f'{yr}-12-31')
for yr in [2024,2025,2026]:
 for q,end in [(1,'03-31'),(2,'06-30'),(3,'09-30')]:
  k=f'{q*3}M{yr}';v,s=extract(f'{yr}-01-01',f'{yr}-{end}')
  if v['revenue'] is not None:raw[k]=v;evidence[k]=s

def sub(a,b):
 return {k: None if a[k] is None or b[k] is None else a[k]-b[k] for k in MAP}
def metrics(x):
 x=x.copy()
 def calc(name,keys,fn):x[name]=None if any(x[k] is None for k in keys) else fn(*[x[k] for k in keys])
 calc('ebit_operating',['gross_profit','opex'],lambda a,b:a-b)
 calc('ebit_ebt_plus_interest',['ebt','interest_net'],lambda a,b:a+b)
 calc('fcf',['cfo','capex'],lambda a,b:a-b)
 calc('fcf_after_sbc',['fcf','sbc'],lambda a,b:a-b)
 calc('ebit_margin_pct',['ebit_operating','revenue'],lambda a,b:100*a/b)
 calc('ar_financing_in_cfo',['ar_sales','ar_collections'],lambda a,b:a-b)
 calc('fcf_less_ar_financing',['fcf','ar_financing_in_cfo'],lambda a,b:a-b)
 return {k:round(v,6) if v is not None else None for k,v in x.items()}
rows={k:metrics(v) for k,v in raw.items()}
bridges={}
for yr in [2024,2025]:
 k=f'Q4{yr}';v=sub(raw[f'FY{yr}'],raw[f'9M{yr}'])
 v['eps_diluted']=None # EPS is not additive; do not subtract FY minus 9M.
 v['diluted_shares']=4*raw[f'FY{yr}']['diluted_shares']-3*raw[f'9M{yr}']['diluted_shares']
 rows[k]=metrics(v);bridges[k]=f'FY{yr} - 9M{yr}; diluted shares use 4*FY-3*9M approximation, not exact daily weighting'
for yr in [2025,2026]:
 for q in [1,2,3]:
  k=f'Q{q}{yr}';end=f'{yr}-'+{1:'03-31',2:'06-30',3:'09-30'}[q];start=f'{yr}-'+{1:'01-01',2:'04-01',3:'07-01'}[q]
  direct,ev=extract(start,end)
  v=raw[f'3M{yr}'].copy() if q==1 else sub(raw[f'{q*3}M{yr}'],raw[f'{(q-1)*3}M{yr}'])
  v['eps_diluted']=None # Only a direct fact may populate quarterly EPS.
  for m in MAP:
   if direct[m] is not None:v[m]=direct[m]
  rows[k]=metrics(v);evidence[k]=ev;bridges[k]='Direct quarterly income facts; cash-flow quarter = current YTD - preceding YTD'
for year in [2025,2026]:
 bases=[f'FY{year-1}',f'9M{year}',f'9M{year-1}']
 v={k:None if any(raw[z][k] is None for z in bases) else raw[bases[0]][k]+raw[bases[1]][k]-raw[bases[2]][k] for k in MAP}
 v['diluted_shares']=None
 v['eps_diluted']=None # Q4 direct EPS unavailable in retained facts, so TTM EPS null.
 ttm=f'TTM{year}0930'
 rows[ttm]=metrics(v)
 bridges[ttm]=f'{bases[0]} + {bases[1]} - {bases[2]}; equivalent to Q4{year-1}+Q1{year}+Q2{year}+Q3{year}. Diluted shares null; no additive EPS or TTM share shortcut.'
(P/'history.json').write_text(json.dumps({'currency':'USD millions except eps_diluted in USD/share and diluted_shares in millions' ,'as_of':'2026-11-04','periods':rows,'bridges':bridges},indent=2)+'\n')
(P/'evidence.json').write_text(json.dumps(evidence,indent=2)+'\n')
with (P/'history.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=['period']+list(next(iter(rows.values()))));w.writeheader()
 for k,v in rows.items():w.writerow({'period':k,**v})
# Validate both actual four-quarter windows against independent FY+9M-9M bridge.
for year in [2025,2026]:
 for m in ['revenue','ebit_operating','ebit_ebt_plus_interest','cfo','capex','sbc','fcf','restructuring_cash_payments']:
  assert abs(sum(rows[q][m] for q in [f'Q4{year-1}',f'Q1{year}',f'Q2{year}',f'Q3{year}'])-rows[f'TTM{year}0930'][m])<.00001,(year,m)
for k in ['FY2023','FY2024','FY2025','Q42024','Q42025','Q12025','Q12026','Q22025','Q22026','Q32025','Q32026','TTM20250930','TTM20260930']:
 print(k, {m:rows[k][m] for m in ['revenue','ebit_operating','ebit_ebt_plus_interest','cfo','capex','fcf','sbc','acquired_intangible_amortization','eps_diluted']})
print('PASS: both TTM20250930 and TTM20260930 four-quarter sums equal FY+9M-9M for revenue, operating EBIT, EBT-plus-interest, CFO, capex, SBC, FCF and restructuring cash payments')
