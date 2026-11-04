from pathlib import Path
import json
P=Path(__file__).resolve().parents[1];H=P/'history';S=P/'sources_private'
facts=json.load(open(H/'factual_inputs.json'))
import csv,json,datetime
metrics={'revenue':'us-gaap:Revenues','net_commissions_fees':'us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax','fiduciary_income':'us-gaap:InvestmentIncomeNet','operating_income':'us-gaap:OperatingIncomeLoss','amortization':'us-gaap:AdjustmentForAmortization','depreciation':'us-gaap:Depreciation','contingent_remeasurement':'us-gaap:BusinessCombinationContingentConsiderationArrangementsChangeInAmountOfContingentConsiderationLiability1','interest_net_income_sign':'us-gaap:InterestIncomeExpenseNonoperatingNet','pretax_income':'us-gaap:IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest','tax_expense':'us-gaap:IncomeTaxExpenseBenefit','net_income_consolidated':'us-gaap:ProfitLoss','net_income_parent':'us-gaap:NetIncomeLoss','net_income_nci':'us-gaap:NetIncomeLossAttributableToNoncontrollingInterest','cfo':'us-gaap:NetCashProvidedByUsedInOperatingActivities','capex':'us-gaap:PaymentsForCapitalImprovements','productive_asset_acquisitions':'us-gaap:PaymentsToAcquireProductiveAssets','sbc_cashflow':'us-gaap:ShareBasedCompensation','acquisitions_net':'us-gaap:PaymentsToAcquireBusinessesNetOfCashAcquired','contingent_payments_financing':'us-gaap:PaymentForContingentConsiderationLiabilityFinancingActivities','contingent_payments_operating':'us-gaap:PaymentForContingentConsiderationLiabilityOperatingActivities'}
lineage=[]
def direct(m,start,end):
 candidates=[f for f in facts if not f['dimensions'] and f['tag']==metrics[m] and f['start']==start and f['end']==end and f['filed']<='2026-11-04']
 if not candidates:return None
 # Latest filing, prefer high-precision primary financial statements (early fact ids) over rounded notes.
 candidates.sort(key=lambda f:(f['filed'],-facts.index(f)),reverse=True)
 f=candidates[0];lineage.append(dict(metric=m,**f));return f['value']/1e6
periods={}
for y in [2023,2024,2025]:periods['FY'+str(y)]={m:direct(m,f'{y}-01-01',f'{y}-12-31') for m in metrics}
for y in [2024,2025,2026]:
 for q,end in [(1,'03-31'),(2,'06-30'),(3,'09-30')]:
  periods[f'{y}YTD{q}']={m:direct(m,f'{y}-01-01',f'{y}-{end}') for m in metrics}
for y,q in [(2025,4),(2026,1),(2026,2),(2026,3)]:
 if q==1: periods[f'Q{q} {y}']=periods[f'{y}YTD1'].copy()
 else:
  a=periods['FY2025'] if q==4 else periods[f'{y}YTD{q}'];b=periods[f'{y}YTD{q-1}']
  periods[f'Q{q} {y}']={m:a[m]-b[m] if a[m] is not None and b[m] is not None else None for m in metrics}
for y in [2025,2026]:
 a,b,c=periods[f'FY{y-1}'],periods[f'{y}YTD3'],periods[f'{y-1}YTD3']
 periods[f'TTM Q3 {y}']={m:a[m]+b[m]-c[m] if all(z[m] is not None for z in [a,b,c]) else None for m in metrics}
for v in periods.values():
 def calc(name,items): v[name]=sum(v[m]*s for m,s in items) if all(v[m] is not None for m,s in items) else None
 calc('ebita_ex_remeasurement_retains_sbc_restructuring',[('operating_income',1),('amortization',1),('contingent_remeasurement',1)])
 calc('cfo_less_capex_not_owner_fcf',[('cfo',1),('capex',-1)])
 # cash taxes reflect mixed Up-C ownership, not whole-company C-corp taxes
 calc('cfo_less_capex_less_sbc_proxy',[('cfo',1),('capex',-1),('sbc_cashflow',-1)])
show=['FY2023','FY2024','FY2025','Q4 2025','Q1 2026','Q2 2026','Q3 2026','TTM Q3 2025','TTM Q3 2026']
with open(H/'normalized_history.csv','w') as f:
 w=csv.writer(f);w.writerow(['metric','unit']+show)
 for m in periods[show[0]]:w.writerow([m,'USD millions']+[round(periods[p][m],6) if periods[p][m] is not None else '' for p in show])
(H/'periods.json').write_text(json.dumps(periods,indent=2));(H/'source_lineage.json').write_text(json.dumps(lineage,indent=2))
print((H/'normalized_history.csv').read_text())
