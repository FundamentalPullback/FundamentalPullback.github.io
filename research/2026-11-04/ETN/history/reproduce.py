#!/usr/bin/env python3
"""Offline financial history reproduction from immutable source_ledger.json, stdlib only.
Run: python reproduce.py. No network and no HTML dependencies.
"""
import csv,json,pathlib
P=pathlib.Path(__file__).resolve().parent
facts=json.loads((P/'source_ledger.json').read_text())
MAP={'revenue':'RevenueFromContractWithCustomerExcludingAssessedTax','cost_of_revenue':'CostOfRevenue','sga':'SellingGeneralAndAdministrativeExpense','rd':'ResearchAndDevelopmentExpense','interest_net':'InterestExpenseNonoperating','other_nonoperating_income':'OtherNonoperatingIncomeExpense','pretax_income':'IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest','tax_expense':'IncomeTaxExpenseBenefit','net_income_consolidated':'ProfitLoss','net_income_parent':'NetIncomeLoss','nci_income':'NetIncomeLossAttributableToNoncontrollingInterest','cfo':'NetCashProvidedByUsedInOperatingActivities','gross_capex':'PaymentsToAcquirePropertyPlantAndEquipment','da':'DepreciationDepletionAndAmortization','depreciation':'Depreciation','sbc_expense':'AllocatedShareBasedCompensationExpense','cash_taxes':'IncomeTaxesPaid','wc_increase_cash_use':'IncreaseDecreaseInOtherOperatingCapitalNet','deferred_tax_cf':'IncreaseDecreaseInDeferredIncomeTaxes','acquisition_cash_net':'PaymentsToAcquireBusinessesNetOfCashAcquired','restructuring_expense':'RestructuringCharges','asset_sale_proceeds':'ProceedsFromSaleOfPropertyPlantAndEquipment','ar_cf_increase':'IncreaseDecreaseInAccountsReceivable','inventory_cf_increase':'IncreaseDecreaseInInventories','ap_cf_increase':'IncreaseDecreaseInAccountsPayable','salaries_cf_increase':'IncreaseDecreaseInAccruedSalaries','taxes_cf_increase':'IncreaseDecreaseInAccruedTaxesPayable'}
BAL={'cash':'CashAndCashEquivalentsAtCarryingValue','ar':'ReceivablesNetCurrent','inventory':'InventoryNet','prepaids_other_current':'PrepaidExpenseAndOtherAssetsCurrent','ap':'AccountsPayableCurrent','current_assets':'AssetsCurrent','current_liabilities':'LiabilitiesCurrent','parent_equity':'StockholdersEquity','equity_including_nci':'StockholdersEquityIncludingPortionAttributableToNoncontrollingInterest','nci_equity':'MinorityInterest','assets':'Assets','liabilities':'Liabilities'}
selected=[]
def get(tag,start,end,dims=None):
 tag=tag if ':' in tag else 'us-gaap:'+tag
 hits=[f for f in facts if f['tag']==tag and f.get('startDate')==start and f.get('endDate',f.get('instant'))==end and f['dimensions']==(dims or {})]
 if not hits:return None
 f=hits[-1];selected.append(f);return f['value']
def add(a,b):return None if a is None or b is None else a+b
def sub(a,b):return None if a is None or b is None else a-b
def calc(r):
 r['gaap_ebit']=add(r['pretax_income'],r['interest_net'])
 r['gaap_operating_income_calculated']=None if any(r[k] is None for k in ['revenue','cost_of_revenue','sga','rd']) else r['revenue']-r['cost_of_revenue']-r['sga']-r['rd']
 r['fcf_cfo_less_gross_capex']=sub(r['cfo'],r['gross_capex'])
 r['wc_cash_flow_contribution']=None if r['wc_increase_cash_use'] is None else -r['wc_increase_cash_use']
 r['deferred_tax_cash_flow_contribution']=None if r['deferred_tax_cf'] is None else -r['deferred_tax_cf']
 r['other_da_ex_intangible_amortization']=sub(r['da'],r['intangible_amortization'])
 r['gaap_ebit_margin']=None if r['gaap_ebit'] is None or not r['revenue'] else r['gaap_ebit']/r['revenue']
 r['effective_tax_rate']=None if r['tax_expense'] is None or not r['pretax_income'] else r['tax_expense']/r['pretax_income']
 return r
def period(label,start,end):
 r=dict(period=label,start=start,end=end,unit='USD million')
 r.update({m:get(t,start,end) for m,t in MAP.items()})
 if r['other_nonoperating_income'] is None:r['other_nonoperating_income']=get('OtherNonoperatingIncome',start,end)
 if r['sbc_expense'] is None:
  parts=[get('AllocatedShareBasedCompensationExpense',start,end,{'us-gaap:AwardTypeAxis':d}) for d in ['etn:RestrictedStockUnitsRSUsAndRestrictedStockMember','us-gaap:PerformanceSharesMember','us-gaap:EmployeeStockOptionMember']]
  r['sbc_expense']=None if any(v is None for v in parts) else sum(parts)
 if r['wc_increase_cash_use'] is None:
  pieces=[(1,'IncreaseDecreaseInAccountsReceivable'),(1,'IncreaseDecreaseInInventories'),(1,'IncreaseDecreaseInContractWithCustomerAsset'),(-1,'IncreaseDecreaseInAccountsPayable'),(-1,'IncreaseDecreaseInAccruedSalaries'),(-1,'IncreaseDecreaseInAccruedTaxesPayable'),(-1,'IncreaseDecreaseInDeferredLiabilities'),(1,'IncreaseDecreaseInOtherCurrentAssets'),(-1,'IncreaseDecreaseInOtherCurrentLiabilities')]
  vals=[get(t,start,end) for _,t in pieces]
  r['wc_increase_cash_use']=None if any(v is None for v in vals) else sum(coef*v for (coef,_),v in zip(pieces,vals))
 r['intangible_amortization']=get('AmortizationOfIntangibleAssets',start,end,{'srt:ConsolidationItemsAxis':'us-gaap:CorporateNonSegmentMember'})
 r['segment_profit_total']=get('OperatingIncomeLoss',start,end,{'srt:ConsolidationItemsAxis':'us-gaap:OperatingSegmentsMember'})
 r['corporate_other_expense']=get('etn:OtherCorporateExpenseNet',start,end,{'srt:ConsolidationItemsAxis':'us-gaap:CorporateNonSegmentMember'})
 r['corporate_pension_expense']=get('PensionAndOtherPostretirementBenefitExpense',start,end,{'srt:ConsolidationItemsAxis':'us-gaap:CorporateNonSegmentMember'})
 if r['corporate_pension_expense'] is None:r['corporate_pension_expense']=get('etn:PensionAndOtherPostretirementBenefitsCostReversalOfCostAdditionalReconciliation',start,end,{'srt:ConsolidationItemsAxis':'us-gaap:CorporateNonSegmentMember'})
 r['sbc_cf_addback']=None;r['sbc_capitalized']=None
 return calc(r)
raw={}
for y in [2023,2024,2025]:raw[f'FY{y}']=period(f'FY{y}',f'{y}-01-01',f'{y}-12-31')
for y in [2024,2025,2026]:raw[f'9M{y}']=period(f'9M{y}',f'{y}-01-01',f'{y}-09-30')
raw['Q1FY2026']=period('Q1FY2026','2026-01-01','2026-03-31');raw['6M2026']=period('6M2026','2026-01-01','2026-06-30')
def combine(label,terms,start,end):
 r=dict(period=label,start=start,end=end,unit='USD million',derivation=' + '.join(f'{coef}*{key}' for coef,key in terms))
 for m in list(MAP)+['intangible_amortization','segment_profit_total','corporate_other_expense','corporate_pension_expense','sbc_cf_addback','sbc_capitalized']:
  vals=[raw[k][m] for _,k in terms];r[m]=None if any(v is None for v in vals) else sum(c*raw[k][m] for c,k in terms)
 return calc(r)
rows=[raw[f'FY{y}'] for y in [2023,2024,2025]]
rows += [combine('Q4FY2025',[(1,'FY2025'),(-1,'9M2025')],'2025-10-01','2025-12-31'),raw['Q1FY2026'],combine('Q2FY2026',[(1,'6M2026'),(-1,'Q1FY2026')],'2026-04-01','2026-06-30'),combine('Q3FY2026',[(1,'9M2026'),(-1,'6M2026')],'2026-07-01','2026-09-30'),combine('TTM_2026Q3',[(1,'FY2025'),(1,'9M2026'),(-1,'9M2025')],'2025-10-01','2026-09-30'),combine('TTM_2025Q3',[(1,'FY2024'),(1,'9M2025'),(-1,'9M2024')],'2024-10-01','2025-09-30')]
balances=[]
for end in ['2023-12-31','2024-12-31','2025-12-31','2026-03-31','2026-06-30','2026-09-30']:
 r=dict(end=end,unit='USD million');r.update({m:get(t,None,end) for m,t in BAL.items()});r['liabilities']=sub(r['assets'],r['equity_including_nci']);r['trade_wc_ar_inventory_less_ap']=sub(add(r['ar'],r['inventory']),r['ap']);balances.append(r)
segments=[]
for f in facts:
 d=f['dimensions'];member=d.get('us-gaap:StatementBusinessSegmentsAxis','')
 if member and f['tag'] in ['us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax','us-gaap:OperatingIncomeLoss'] and len(d)<=2:
  segments.append(f)
def out(name,obj):
 (P/(name+'.json')).write_text(json.dumps(obj,indent=2))
 if obj:
  keys=list(dict.fromkeys(k for r in obj for k in r));w=csv.DictWriter((P/(name+'.csv')).open('w'),fieldnames=keys);w.writeheader();w.writerows(obj)
out('normalized',rows);out('balances',balances);out('segment_source_ledger',segments)
# Segment history uses historical Vehicle + eMobility as combined Mobility where needed.
# This is a segment presentation bridge only, not separation pro forma.
seg_rows=[]
for r in rows:
 for seg in ['ElectricalAmericas','ElectricalGlobal','Aerospace','Mobility']:
  z={'period':r['period'],'segment':seg,'unit':'USD million'}
  terms=[]
  if 'derivation' in r:
   terms=[(int(term.split('*')[0]),raw[term.split('*')[1]]) for term in r['derivation'].split(' + ')]
  else:terms=[(1,r)]
  for field,tag in [('revenue','RevenueFromContractWithCustomerExcludingAssessedTax'),('segment_profit','OperatingIncomeLoss')]:
   vals=[]
   for coef,rr in terms:
    def sg(member):
     return get(tag,rr['start'],rr['end'],{'us-gaap:StatementBusinessSegmentsAxis':'etn:'+member+'SegmentMember','srt:ConsolidationItemsAxis':'us-gaap:OperatingSegmentsMember'})
    v=sg(seg)
    if v is None and seg=='Mobility':v=add(sg('Vehicle'),sg('EMobility'))
    vals.append(None if v is None else coef*v)
   z[field]=None if any(v is None for v in vals) else sum(vals)
  z['segment_margin']=None if z['segment_profit'] is None or not z['revenue'] else z['segment_profit']/z['revenue']
  seg_rows.append(z)
out('segments_normalized',seg_rows)
out('acquiree_actual_contributions',[f for f in facts if 'BusinessCombinationProFormaInformation' in f['tag']])
out('quarter_income_direct',[period('Q4FY2025_direct_unavailable','2025-10-01','2025-12-31'),period('Q1FY2026_direct','2026-01-01','2026-03-31'),period('Q2FY2026_direct','2026-04-01','2026-06-30'),period('Q3FY2026_direct','2026-07-01','2026-09-30')])
# Deduplicate selected source references but preserve their facts and contexts.
selected=list({(f['source'],f['fact_id']):f for f in selected}.values());out('selected_inputs',selected)
qa=[]
for r in rows:
 a=r['pretax_income'];b=add(r['net_income_consolidated'],r['tax_expense']);diff=sub(a,b)
 qa.append({'period':r['period'],'check':'pretax - (consolidated NI + tax)','residual_usd_m':diff,'pass_rounding_tolerance_2m':diff is not None and abs(diff)<=2})
 diff=sub(r['net_income_consolidated'],add(r['net_income_parent'],r['nci_income']))
 qa.append({'period':r['period'],'check':'consolidated NI - (parent NI + NCI)','residual_usd_m':diff,'pass_rounding_tolerance_2m':diff is not None and abs(diff)<=2})
 diff=sub(r['gaap_ebit'],add(r['gaap_operating_income_calculated'],r['other_nonoperating_income']))
 qa.append({'period':r['period'],'check':'EBIT - (calculated operating income + other nonoperating income)','residual_usd_m':diff,'pass_rounding_tolerance_2m':diff is not None and abs(diff)<=2})
for r in rows:
 vals=[r[k] for k in ['segment_profit_total','intangible_amortization','corporate_pension_expense','restructuring_expense','corporate_other_expense']]
 diff=None if any(v is None for v in vals) else r['gaap_ebit']-(vals[0]-sum(vals[1:]))
 qa.append({'period':r['period'],'check':'GAAP EBIT vs segment profit less corporate items excluding interest','residual_usd_m':diff,'pass_rounding_tolerance_2m':diff is not None and abs(diff)<=2})
for r in balances:
 diff=sub(r['equity_including_nci'],add(r['parent_equity'],r['nci_equity']))
 qa.append({'period':r['end'],'check':'total equity equals parent plus NCI','residual_usd_m':diff,'pass_rounding_tolerance_2m':diff is not None and abs(diff)<=2})
out('qa',qa)
# All quarterly cash flow is YTD differenced; no synthetic SBC values or acquisition adjustments.
print(json.dumps([{k:r[k] for k in ['period','revenue','gaap_ebit','cfo','gross_capex','da','intangible_amortization','sbc_expense']} for r in rows],indent=2))
