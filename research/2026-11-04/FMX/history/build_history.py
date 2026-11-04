#!/usr/bin/env python3
"""Offline history build. Inputs are compact extracted primary facts, not full filings.
Run: python build_history.py. No packages, network, or DCF assumptions required.
Amounts: MXN million. Cash outflows: positive deductions. Missing stays null.
"""
import json,csv,pathlib,statistics
P=pathlib.Path(__file__).resolve().parent
raw_path=P/'selected_primary_bmv_facts.json'
if not raw_path.exists():raw_path=P/'bmv_extracted_numeric_facts.json'
raw=json.loads(raw_path.read_text())
manual=json.loads((P/'manual_primary_inputs.json').read_text())
M={
'revenue':'Revenue','ebit_xbrl_raw':'ProfitLossFromOperatingActivities','net_income_consolidated':'ProfitLoss','net_income_attributable':'ProfitLossAttributableToOwnersOfParent','net_income_noncontrolling':'ProfitLossAttributableToNoncontrollingInterests','net_income_continuing':'ProfitLossFromContinuingOperations','net_income_discontinued':'ProfitLossFromDiscontinuedOperations','tax_expense':'IncomeTaxExpenseContinuingOperations',
'cfo_bmv':'CashFlowsFromUsedInOperatingActivities','da_cf':'AdjustmentsForDepreciationAndAmortisationExpense','cash_taxes':'IncomeTaxesPaidRefundClassifiedAsOperatingActivities','cash_ppe':'PurchaseOfPropertyPlantAndEquipmentClassifiedAsInvestingActivities','cash_intangibles':'PurchaseOfIntangibleAssetsClassifiedAsInvestingActivities','cash_other_longterm_assets':'PurchaseOfOtherLongtermAssetsClassifiedAsInvestingActivities','cash_lease_total':'PaymentsOfLeaseLiabilitiesClassifiedAsFinancingActivities','cash_financing_interest_ex_lease':'InterestPaidClassifiedAsFinancingActivities','cash_acquire_control':'CashFlowsUsedInObtainingControlOfSubsidiariesOrOtherBusinessesClassifiedAsInvestingActivities','cash_acquire_jv':'OtherCashPaymentsToAcquireInterestsInJointVenturesClassifiedAsInvestingActivities','cfi_bmv':'CashFlowsFromUsedInInvestingActivities','cff_bmv':'CashFlowsFromUsedInFinancingActivities','cash_increase_before_fx':'IncreaseDecreaseInCashAndCashEquivalentsBeforeEffectOfExchangeRateChanges','cash_fx':'EffectOfExchangeRateChangesOnCashAndCashEquivalents','cash_increase':'IncreaseDecreaseInCashAndCashEquivalents',
'wc_trade_receivables':'AdjustmentsForDecreaseIncreaseInTradeAccountReceivable','wc_other_receivables':'AdjustmentsForDecreaseIncreaseInOtherOperatingReceivables','wc_inventory':'AdjustmentsForDecreaseIncreaseInInventories','wc_trade_payables':'AdjustmentsForIncreaseDecreaseInTradeAccountPayable','wc_other_payables':'AdjustmentsForIncreaseDecreaseInOtherOperatingPayables','sbc_cf_addback':'AdjustmentsForSharebasedPayments'}
perioddefs={
'TTM2026_reported_BMV':('fmx_bmv_q3_2026','2025-10-01','2026-09-30'),
'TTM2025_reported_BMV':('fmx_bmv_q3_2026','2024-10-01','2025-09-30'),
'FY2023_BMV':('fmx_bmv_q4_2024','2023-01-01','2023-12-31'),
'FY2024_BMV':('fmx_bmv_q4_2025','2024-01-01','2024-12-31'),
'FY2025_BMV':('fmx_bmv_q4_2025','2025-01-01','2025-12-31'),
'9M2024_BMV':('fmx_bmv_q3_2025','2024-01-01','2024-09-30'),
'9M2025_BMV':('fmx_bmv_q3_2026','2025-01-01','2025-09-30'),
'9M2026_BMV':('fmx_bmv_q3_2026','2026-01-01','2026-09-30'),
'Q12026_BMV':('fmx_bmv_q1_2026','2026-01-01','2026-03-31'),
'H12026_BMV':('fmx_bmv_q2_2026','2026-01-01','2026-06-30'),
'Q32026_standalone_BMV':('fmx_bmv_q3_2026','2026-07-01','2026-09-30'),
'Q22026_standalone_BMV':('fmx_bmv_q2_2026','2026-04-01','2026-06-30'),
'Q42025_standalone_BMV':('fmx_bmv_q4_2025','2025-10-01','2025-12-31')}
long=[];D={}
for period,(src,start,end) in perioddefs.items():
 d={}
 for metric,concept in M.items():
  a=[r for r in raw if r['source_id']==src and r['start']==start and r['end']==end and r['concept']==concept]
  if len(a)>1:raise ValueError((period,metric,'duplicate'))
  if a:
   x=a[0]; v=x['value_mxn_m']
   # Historic taxonomy names peso unit differently: currency metadata can be verified from source; all monetary M fields are MXN.
   if v is None:v=x['raw_value']/1e6
   d[metric]=v
   long.append({'period':period,'metric':metric,'value':v,'unit':'MXN_m','source_id':src,'source_locator':x['concept']+' | '+x['fact_id'],'evidence':'fact_source_reported','note':'BMV tag presentation; see comparability flags'})
 D[period]=d
for period,data in manual['periods'].items():
 d=D.setdefault(period,{})
 for metric,x in data.items():
  d[metric]=x['value'];long.append({'period':period,'metric':metric,'value':x['value'],'unit':x.get('unit','MXN_m'),'source_id':x['source_id'],'source_locator':x['locator'],'evidence':x.get('evidence','fact_source_reported'),'note':x.get('note','')})
# Append reported annual IR EBIT to same-period BMV basis, never use XBRL raw EBIT for normalized operating earnings.
for per in ['FY2023','FY2024','FY2025','9M2024','9M2025','9M2026','Q12026','H12026']:
 if per in D and per+'_BMV' in D:
  for m,v in D[per].items():
   if m.startswith('ebit_') or m.startswith('adj_') or m.startswith('management_'):D[per+'_BMV'][m]=v
# Deterministic differences are residual quarters, not issuer quarter recasts.
def diff(new,a,b,c=None):
 metrics=set(D[a])&set(D[b])
 if c:metrics &=set(D[c])
 D[new]={}
 for m in sorted(metrics):
  if m in ['sbc_cf_addback'] or m.endswith('_shares_m') or m.startswith('eps_'):continue
  vals=[D[x][m] for x in [a,b]+([c] if c else [])]
  if any(v is None for v in vals):continue
  v=vals[0]+vals[1]-vals[2] if c else vals[0]-vals[1]
  D[new][m]=v
  long.append({'period':new,'metric':m,'value':v,'unit':'MXN_m','source_id':a+';'+b+(';'+c if c else ''),'source_locator':'sum/difference of extracted inputs','evidence':'derived_calculation','note':f'{a}+{b}-{c}' if c else f'{a}-{b}; residual may include revisions/inflation restatement'})
diff('Q42025_residual','FY2025_BMV','9M2025_BMV')
diff('Q22026_residual','H12026_BMV','Q12026_BMV')
diff('Q32026_residual','9M2026_BMV','H12026_BMV')
diff('TTM2026_BMV','FY2025_BMV','9M2026_BMV','9M2025_BMV')
diff('TTM2025_BMV','FY2024_BMV','9M2025_BMV','9M2024_BMV')
for per,d in D.items():
 def calc(k,keys,fn):
  if all(d.get(x) is not None for x in keys):
   d[k]=fn(*[d[x] for x in keys]);long.append({'period':per,'metric':k,'value':d[k],'unit':'MXN_m','source_id':'DERIVED:'+per,'source_locator':','.join(keys),'evidence':'derived_calculation','note':'Not normalized FCFF or parent-attributable cash flow'})
 calc('cash_capex_ppe_intangibles',['cash_ppe','cash_intangibles'],lambda a,b:a+b)
 calc('cash_investment_broader',['cash_capex_ppe_intangibles','cash_other_longterm_assets'],lambda a,b:a+b)
 calc('wc_five_movements',['wc_trade_receivables','wc_other_receivables','wc_inventory','wc_trade_payables','wc_other_payables'],lambda *a:sum(a))
 calc('cfo_before_five_wc_and_cash_tax',['cfo_bmv','wc_five_movements','cash_taxes'],lambda a,b,c:a-b+c)
 calc('cash_residual_after_capex_rent_interest',['cfo_bmv','cash_capex_ppe_intangibles','cash_lease_total','cash_financing_interest_ex_lease'],lambda a,b,c,d:a-b-c-d)
 calc('cash_operating_profit_after_rent',['ebit_management','da_cf','cash_lease_total'],lambda a,b,c:a+b-c)
 calc('da_ex_rou',['da_cf','rou_depreciation'],lambda a,b:a-b)
checks=[]
def chk(name,actual,expected,tol=0.002,note=''):
 delta=actual-expected;checks.append({'check':name,'actual':actual,'expected':expected,'delta':delta,'tolerance':tol,'passed':abs(delta)<=tol,'note':note})
for per,d in D.items():
 if all(k in d for k in ['cfo_bmv','cfi_bmv','cff_bmv','cash_increase_before_fx']):chk(per+' cash activities tie',d['cfo_bmv']+d['cfi_bmv']+d['cff_bmv'],d['cash_increase_before_fx'],.01)
 if all(k in d for k in ['cash_increase','cash_increase_before_fx','cash_fx']):chk(per+' FX tie',d['cash_increase_before_fx']+d['cash_fx'],d['cash_increase'],.01)
 if all(k in d for k in ['net_income_attributable','net_income_noncontrolling','net_income_consolidated']):chk(per+' NI attribution tie',d['net_income_attributable']+d['net_income_noncontrolling'],d['net_income_consolidated'],.01)
for fy in ['FY2023','FY2024','FY2025']:
 d=D[fy];chk(fy+' lease total',d['cash_lease_principal']+d['cash_lease_interest'],d['cash_lease_total'],0)
# Exact prior notes checks and rounding-aware source classification bridges.
a,b=D['9M2026_BMV'],D['9M2025_BMV'];swing=a['wc_five_movements']-b['wc_five_movements'];tax=b['cash_taxes']-a['cash_taxes'];increase=a['cfo_bmv']-b['cfo_bmv']
analytics={'cfo_9m_growth':a['cfo_bmv']/b['cfo_bmv']-1,'wc_swing_9m':swing,'tax_improvement_9m':tax,'cfo_increase_9m':increase,'wc_tax_share_of_cfo_increase':(swing+tax)/increase,'cfo_before_wc_tax_growth':a['cfo_before_five_wc_and_cash_tax']/b['cfo_before_five_wc_and_cash_tax']-1,'consolidated_ni_ex_imperial_gain_9m2026':37456-11952,'unverified_issuer_growth_claim':.121,'computed_ex_gain_growth_vs_prior_ni':25504/20359-1,'normalized_effective_tax_rate_issuer_check':13656/(51167-11952),'source_rounding_tolerance_mxn_m':1}
chk('Prior A127 CFO9M26',a['cfo_bmv'],88749.884,0)
chk('Prior A127 CFO9M25',b['cfo_bmv'],49977.733183,.001)
chk('FY2024 discontinued-cash presentation bridge',D['FY2024']['cfo_audited']-6080-1276+977,D['FY2024_BMV']['cfo_bmv'],1,'Algebraic bridge supports presentation reclassification; audited source is rounded.')
chk('FY2023 discontinued-cash presentation bridge',D['FY2023']['cfo_audited']+25426-20727,D['FY2023_BMV']['cfo_bmv'],1,'Algebraic bridge supports presentation reclassification; audited source is rounded.')
for name,obj in [('history_wide.json',D),('analytics.json',analytics),('validation_checks.json',checks),('history_long.json',long)]: (P/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2,allow_nan=False))
for name,rows in [('history_long.csv',long),('validation_checks.csv',checks)]:
 with (P/name).open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
metrics=sorted(set().union(*(d.keys() for d in D.values())))
with (P/'history_wide.csv').open('w',newline='') as f:
 w=csv.writer(f);w.writerow(['metric']+list(D));[w.writerow([m]+[d.get(m,'') for d in D.values()]) for m in metrics]
selected=[x for x in raw if x['concept'] in set(M.values())];(P/'selected_primary_bmv_facts.json').write_text(json.dumps(selected,indent=2))
print(json.dumps({'periods':len(D),'long_rows':len(long),'checks':len(checks),'failed_checks':[x for x in checks if not x['passed']],'analytics':analytics,'TTM2026':D['TTM2026_BMV']},indent=2))
