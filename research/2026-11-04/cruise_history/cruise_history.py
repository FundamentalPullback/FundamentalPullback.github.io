"""Reproducible as-of-2026-11-04 cruise history. USD millions unless ratios.
Downloaded SEC companyfacts supply GAAP observations; explicitly cited manual inputs
supply non-GAAP/normalization bridges. No source valuation model is edited.
"""
import json,pathlib,csv
P=pathlib.Path(__file__).parent; S=P/'sources'
URLS=json.load(open(S/'cruise_source_urls.json'))
TAGS={'revenue':'RevenueFromContractWithCustomerExcludingAssessedTax','EBIT':'OperatingIncomeLoss','net_income_parent':'NetIncomeLoss','net_income_consolidated':'ProfitLoss','DA':'DepreciationAndAmortization','SBC':'ShareBasedCompensation','CFO':'NetCashProvidedByUsedInOperatingActivities','capex':'PaymentsToAcquirePropertyPlantAndEquipment','interest_expense':'InterestExpenseNonoperating','income_tax':'IncomeTaxExpenseBenefit','equity_method_income':'IncomeLossFromEquityMethodInvestments'}
RCL_RESTRUCT={'FY2023':5,'FY2024':10,'FY2025':8,'9M2024':5,'9M2025':7,'9M2026':11,'H12026':3,'Q12026':3}
RCL_IMPAIR={'FY2023':8,'FY2024':9,'FY2025':0,'9M2024':6,'9M2025':0,'9M2026':0,'H12026':0,'Q12026':0}
RCL_ADJNI={'FY2023':1827,'FY2024':3237,'FY2025':4286,'9M2024':2794,'9M2025':3523,'9M2026':3865,'H12026':2105,'Q12026':975}
CCL_SHIPGAIN={'FY2023':88,'FY2024':39,'FY2025':110,'9M2024':6,'9M2025':101,'9M2026':-2,'H12026':0,'Q12026':0}
CCL_DEBTLOSS={'FY2023':111,'FY2024':79,'FY2025':409,'9M2024':78,'9M2025':366,'9M2026':23,'H12026':0,'Q12026':0}
CCL_ADJEBIT={'FY2023':1887,'FY2024':3556,'FY2025':4396,'9M2025':3656,'9M2026':3732,'H12026':1492,'Q12026':623}
ALL={}; QA=[]
for ticker,cik in [('RCL',884887),('CCL',815097)]:
 a=json.load(open(S/(ticker+'_facts.json')))['facts']['us-gaap'];evidence=[]
 def get(tag,start,end):
  if tag not in a:return None
  rr=[v for v in a[tag]['units']['USD'] if v.get('start')==start and v['end']==end and v['filed']<='2026-11-04' and v.get('form') in ['10-K','10-Q']]
  if not rr:return None
  rr.sort(key=lambda v:(v['filed'],v.get('accn','')));r=rr[-1]
  evidence.append(dict(metric=tag,start=start,end=end,value_m=r['val']/1e6,filed=r['filed'],accession=r['accn'],url=f'https://www.sec.gov/Archives/edgar/data/{cik}/'+r['accn'].replace('-','')+'/'))
  return r['val']/1e6
 def start(y):return f'{y}-01-01' if ticker=='RCL' else f'{y-1}-12-01'
 def ending(y,q):return f'{y}-'+(['03-31','06-30','09-30','12-31'][q-1] if ticker=='RCL' else ['02-28','05-31','08-31','11-30'][q-1])
 def row(y,q):
  out={k:get(tag,start(y),ending(y,q)) for k,tag in TAGS.items()}
  out['interest_income']=get('InterestAndOtherIncome' if ticker=='RCL' else 'InvestmentIncomeInterest',start(y),ending(y,q))
  out['debt_extinguishment_cash_reconciliation']=get('GainsLossesOnExtinguishmentOfDebt',start(y),ending(y,q))
  if ticker=='RCL':out['JV_dividends_received']=get('ProceedsFromDividendsReceived',start(y),ending(y,q))
  return out
 h={f'FY{y}':row(y,4) for y in [2019,2020,2021,2022,2023,2024,2025]}
 h.update({f'9M{y}':row(y,3) for y in [2024,2025,2026]});h['H12026']=row(2026,2);h['Q12026']=row(2026,1)
 for label,r in h.items():
  if ticker=='RCL':
   r['restructuring_adjustment']=RCL_RESTRUCT.get(label)
   r['operating_impairment_adjustment']=RCL_IMPAIR.get(label)
   r['issuer_adjusted_NI']=RCL_ADJNI.get(label)
   r['core_EBIT']=r['EBIT']+RCL_RESTRUCT[label]+RCL_IMPAIR[label] if label in RCL_RESTRUCT else None
  else:
   r['net_ship_sale_impairment_gain']=CCL_SHIPGAIN.get(label)
   r['debt_extinguishment_and_modification_cost']=CCL_DEBTLOSS.get(label)
   r['issuer_adjusted_EBIT']=CCL_ADJEBIT.get(label)
   r['core_EBIT']=r['EBIT']-CCL_SHIPGAIN[label] if label in CCL_SHIPGAIN else None
 for label,x,y in [('Q42025','FY2025','9M2025'),('Q22026','H12026','Q12026'),('Q32026','9M2026','H12026')]:
  h[label]={k:h[x][k]-h[y][k] if h[x][k] is not None and h[y][k] is not None else None for k in h[x]}
 # Quarterly income metrics use exact quarter observations when filed, not subtraction.
 # Cash statements are cumulative: quarter CFO, capex and SBC remain differences.
 for q,begin in [(2,'2026-04-01' if ticker=='RCL' else '2026-03-01'),(3,'2026-07-01' if ticker=='RCL' else '2026-06-01')]:
  r=h[f'Q{q}2026']
  for k in ['revenue','EBIT','net_income_parent','net_income_consolidated','DA','interest_expense','income_tax','equity_method_income']:
   v=get(TAGS[k],begin,ending(2026,q))
   if v is not None:r[k]=v
  v=get('InterestAndOtherIncome' if ticker=='RCL' else 'InvestmentIncomeInterest',begin,ending(2026,q))
  if v is not None:r['interest_income']=v
  if ticker=='RCL':
   if q==3:r['restructuring_adjustment']=9 # Exact quarter reconciliation; cumulative difference is 8 because of rounding.
   r['core_EBIT']=r['EBIT']+r['restructuring_adjustment']+r['operating_impairment_adjustment']
  else:r['core_EBIT']=r['EBIT']-r['net_ship_sale_impairment_gain']
 for label,ann,new,old in [('TTM2026','FY2025','9M2026','9M2025'),('TTM2025','FY2024','9M2025','9M2024')]:
  h[label]={k:h[ann][k]+h[new][k]-h[old][k] if all(h[r][k] is not None for r in [ann,new,old]) else None for k in h[ann]}
 for label,r in h.items():
  r['FCF_after_interest']=r['CFO']-r['capex'] if all(r[k] is not None for k in ['CFO','capex']) else None
  r['FCF_less_SBC']=r['FCF_after_interest']-r['SBC'] if r['FCF_after_interest'] is not None and r['SBC'] is not None else None
  r['EBIT_margin']=r['EBIT']/r['revenue'] if r['EBIT'] is not None else None
  r['normalized_NI_diagnostic']=r.get('issuer_adjusted_NI') if ticker=='RCL' else (r['net_income_parent']+.98*(r['debt_extinguishment_and_modification_cost']-r['net_ship_sale_impairment_gain']) if r.get('debt_extinguishment_and_modification_cost') is not None else None)
  r['core_NOPAT_2pct']=r['core_EBIT']*.98 if r['core_EBIT'] is not None else None
  r['core_FCFF_before_WC_actual_capex']=r['core_NOPAT_2pct']+r['DA']-r['capex'] if r['core_EBIT'] is not None else None
  r['normalized_after_interest_profit_proxy']=.98*(r['core_EBIT']-r['interest_expense']+r['interest_income']) if r['core_EBIT'] is not None else None
 for k in TAGS:
  vals=[h[p][k] for p in ['Q42025','Q12026','Q22026','Q32026']]
  if all(v is not None for v in vals):
   delta=sum(vals)-h['TTM2026'][k];QA.append(dict(ticker=ticker,metric=k,quarter_sum_difference=delta,allowed_rounding_m=2,pass_check=abs(delta)<=2));assert abs(delta)<=2,(ticker,k,delta)
 ALL[ticker]=dict(history=h,evidence=evidence,source_urls={k:v for k,v in URLS.items() if k.startswith(ticker)},normalization_source_note='Annual 2025, Q3 2025 and Q1/Q2/Q3 2026 official statements and non-GAAP/segment reconciliations; see companion addendum for adjustment bridge and units. CCL 9M2024 ship net gain = $8m sale gain minus $2m impairment. No added-back SBC in core EBIT or NOPAT.',periods={'TTM2026':('2025-10-01/2026-09-30' if ticker=='RCL' else '2025-09-01/2026-08-31'),'TTM2025':('2024-10-01/2025-09-30' if ticker=='RCL' else '2024-09-01/2025-08-31')})
(P/'cruise_history.json').write_text(json.dumps(ALL,indent=2))
rows=[dict(ticker=t,period=k,**v) for t,z in ALL.items() for k,v in z['history'].items()]
with open(P/'cruise_history.csv','w') as f:
 w=csv.DictWriter(f,fieldnames=list(dict.fromkeys(k for r in rows for k in r)));w.writeheader();w.writerows(rows)
(P/'cruise_history_qa.json').write_text(json.dumps(QA,indent=2))
print(f'{len(QA)} quarter/TTM consistency checks passed within source rounding.')
for t,z in ALL.items():
 print(t)
 for p in ['FY2019','FY2020','FY2023','FY2024','FY2025','Q42025','Q12026','Q22026','Q32026','TTM2025','TTM2026']:
  r=z['history'][p];print(p,{k:r[k] for k in ['revenue','EBIT','net_income_parent','SBC','CFO','capex','core_EBIT','core_FCFF_before_WC_actual_capex']})
