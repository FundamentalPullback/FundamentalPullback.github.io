#!/usr/bin/env python3
"""Rebuild YOU historical schedules offline using Python standard library only.
Run: python scripts/rebuild.py. Inputs contain limited numerical reported facts,
not complete SEC documents. USD thousands unless a column states otherwise.
"""
from pathlib import Path
from decimal import Decimal as D
import csv,json
B=Path(__file__).resolve().parents[1];O=B/'derived';O.mkdir(exist_ok=True)
R=list(csv.DictReader((B/'inputs'/'reported_facts.csv').open()))
F={};prov={};checks=[];flags=[]
for r in R:
 k=(r['period'],r['metric']);v=D(r['value'])
 if k in F and F[k]!=v:flags.append({'flag':'source_conflict','period':k[0],'metric':k[1],'detail':f'{F[k]} vs {v}'})
 F[k]=v;prov.setdefault(k,[]).append(r['source_id']+':'+r['location'])
def get(p,m):return F.get((p,m))
def put(p,m,v,formula):F[(p,m)]=v;prov[(p,m)]=[formula]
additive={r['metric'] for r in R if r['unit']=='USD_thousands' and r['period'].startswith(('FY','9M','6M','Q'))}-{'partnership_settlement_approx','fcf_company_reported'}
# Derive missing quarter cash-flow components from cumulative statements.
for y in (2025,2026):
 for q,a,b in [(2,'6M','Q1'),(3,'9M','6M')]:
  for m in sorted(additive):
   p=f'Q{q}{y}';x=get(f'{a}{y}',m);z=get(f'{b}{y}',m)
   if x is not None and z is not None:
    if get(p,m) is None:put(p,m,x-z,f'{a}{y} - {b}{y}')
    elif abs(get(p,m)-(x-z))>0:
     checks.append(dict(check='quarter cumulative tie-out',period=p,metric=m,difference=str(get(p,m)-(x-z)),status='rounding_difference' if abs(get(p,m)-(x-z))<=1 else 'FAIL'))
for y in (2024,2025):
 for m in sorted(additive):
  x=get(f'FY{y}',m);z=get(f'9M{y}',m)
  if x is not None and z is not None and get(f'Q4{y}',m) is None:put(f'Q4{y}',m,x-z,f'FY{y} - 9M{y}')
for y in (2025,2026):
 for m in sorted(additive):
  x=get(f'FY{y-1}',m);z=get(f'9M{y-1}',m);a=get(f'9M{y}',m)
  if None not in (x,z,a):put(f'TTM{y}-09-30',m,x-z+a,f'FY{y-1} - 9M{y-1} + 9M{y}')
periods=['FY2023','FY2024','FY2025','Q42024','Q12025','Q22025','Q32025','Q42025','Q12026','Q22026','Q32026','TTM2025-09-30','TTM2026-09-30']
for p in periods:
 r=get(p,'revenue');cfo=get(p,'cfo');cap=get(p,'ppe_capex_signed');sbc=get(p,'stock_compensation')
 if None not in (cfo,cap):
  fcf=cfo+cap;put(p,'fcf_cfo_less_ppe',fcf,'cfo + ppe_capex_signed')
  if sbc is not None:put(p,'fcf_less_sbc_diagnostic',fcf-sbc,'fcf_cfo_less_ppe - stock_compensation; not owner earnings')
  icap=get(p,'intangibles_capex_signed')
  if icap is not None:put(p,'fcf_after_ppe_and_intangible_capex',fcf+icap,'cfo + ppe_capex_signed + intangibles_capex_signed')
 for name,base in [('operating_margin','operating_income'),('adjusted_ebitda_margin','adjusted_ebitda'),('net_margin_consolidated','net_income_consolidated'),('fcf_margin','fcf_cfo_less_ppe'),('sbc_pct_revenue','stock_compensation')]:
  if r and get(p,base) is not None:put(p,name,get(p,base)/r,base+' / revenue')
 if get(p,'pretax_income') and get(p,'tax_pnl_signed') is not None:put(p,'effective_tax_rate',-get(p,'tax_pnl_signed')/get(p,'pretax_income'),'-tax_pnl_signed / pretax_income')
 if r:
  costs=[get(p,m) for m in ['revenue_share_cost','direct_salaries_cost','research_development','sales_marketing','general_administrative','depreciation_amortization']]
  if all(x is not None for x in costs):checks.append(dict(check='operating statement',period=p,metric='operating_income',difference=str(r-sum(costs)-get(p,'operating_income')),status='PASS' if abs(r-sum(costs)-get(p,'operating_income'))<=1 else 'FAIL'))
 for lhs,parts in [('pretax_income',['operating_income','interest_income_net','other_income_net']),('net_income_consolidated',['pretax_income','tax_pnl_signed']),('net_income_consolidated',['net_income_parent','net_income_nci'])]:
  a=get(p,lhs);vs=[get(p,m) for m in parts]
  if a is not None and all(x is not None for x in vs):checks.append(dict(check=' + '.join(parts),period=p,metric=lhs,difference=str(a-sum(vs)),status='PASS' if abs(a-sum(vs))<=1 else 'FAIL'))
# Period metadata are from statement headers, not inferred reporting dates.
def dates(p):
 if p.startswith('FY'):return p[2:]+'-01-01',p[2:]+'-12-31'
 if p.startswith('TTM'):return str(int(p[3:7])-1)+'-10-01',p[3:]
 q=int(p[1]);y=p[2:];return y+['-01-01','-04-01','-07-01','-10-01'][q-1],y+['-03-31','-06-30','-09-30','-12-31'][q-1]
metrics=['ppe_depreciation','intangible_amortization','software_capitalized','sbc_capitalized_software','software_amortization','revenue','revenue_share_cost','direct_salaries_cost','research_development','sales_marketing','general_administrative','depreciation_amortization','operating_income','operating_margin','adjusted_ebitda','adjusted_ebitda_margin','interest_income_net','other_income_net','pretax_income','tax_pnl_signed','effective_tax_rate','net_income_consolidated','net_income_parent','net_income_nci','eps_basic','eps_diluted','cfo','ppe_capex_signed','intangibles_capex_signed','fcf_cfo_less_ppe','fcf_company_reported','fcf_margin','stock_compensation','sbc_pct_revenue','fcf_less_sbc_diagnostic','deferred_revenue_cf','accrued_liabilities_cf','deferred_tax_cf','repurchases_signed','ordinary_dividend_signed','special_dividend_signed','nci_distributions_signed','nci_tax_distributions_signed','stock_withholding_signed','tra_cash_signed','financing_cf']
def fmt(v):return '' if v is None else format(v.quantize(D('0.000001')),'f').rstrip('0').rstrip('.') if v!=v.to_integral_value() else str(int(v))
with (O/'financial_history.csv').open('w',newline='') as f:
 w=csv.writer(f);w.writerow(['period','period_start','period_end']+metrics)
 for p in periods:w.writerow([p,*dates(p)]+[fmt(get(p,m)) for m in metrics])
# The latest TTM and prior TTM comparison is additive through the reported 9M totals.
comparison=[]
for m in metrics:
 a=get('TTM2026-09-30',m);b=get('TTM2025-09-30',m)
 if None not in (a,b):comparison.append(dict(metric=m,ttm_2026=fmt(a),ttm_2025=fmt(b),change=fmt(a-b),growth_pct=fmt((a/b-1)*100) if b>0 and 'margin' not in m and 'rate' not in m else ''))
with (O/'ttm_comparison.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(comparison[0]));w.writeheader();w.writerows(comparison)
bs_periods=['2023-12-31','2024-12-31','2025-12-31','2026-03-31','2026-06-30','2026-09-30','2026-10-30']
bs_metrics=['treasury_shares','founder_psus_unvested_remaining','rsus_vest_within_1y','rsus_vest_1to2y','rsus_vest_2to3y','rsu_unrecognized_expense','rsu_expense_years','total_net_deferred_tax_asset','dilutive_increment_Q3_EPS','cash','marketable_securities','liquid_assets','restricted_cash','current_assets','assets','current_liabilities','liabilities','deferred_revenue','accrued_liabilities','equity_total','equity_parent','equity_nci','shares_A','shares_B','shares_C_Alclear','shares_D_Alclear','economic_units_basic','nci_ownership','debt_drawn','partnership_current','partnership_noncurrent','partnership_total','tra_current','tra_noncurrent','tra_total','lease_current','lease_noncurrent','lease_total','tax_basis_dta','unvested_rsus','performance_condition_shares_excluded','rsus_antidilutive_excluded','undrawn_capacity_net_lc']
for p in bs_periods:
 for dest,items in [('liquid_assets',['cash','marketable_securities']),('economic_units_basic',['shares_A','shares_B','shares_C_Alclear','shares_D_Alclear']),('partnership_total',['partnership_current','partnership_noncurrent']),('tra_total',['tra_current','tra_noncurrent']),('lease_total',['lease_current','lease_noncurrent'])]:
  vals=[get(p,m) for m in items]
  if all(x is not None for x in vals):put(p,dest,sum(vals),' + '.join(items))
 if get(p,'economic_units_basic'):put(p,'nci_ownership',(get(p,'shares_C_Alclear')+get(p,'shares_D_Alclear'))/get(p,'economic_units_basic'),'(C+D)/(A+B+C+D); exchange units only once')
 if get(p,'assets'):checks.append(dict(check='balance sheet',period=p,metric='assets',difference=str(get(p,'assets')-get(p,'liabilities')-get(p,'equity_total')),status='PASS' if get(p,'assets')==get(p,'liabilities')+get(p,'equity_total') else 'FAIL'))
with (O/'capital_perimeter.csv').open('w',newline='') as f:
 w=csv.writer(f);w.writerow(['as_of']+bs_metrics)
 for p in bs_periods:w.writerow([p]+[fmt(get(p,m)) for m in bs_metrics])
# Settlement illustration is not a normalization: the contractual cost recurs in revenue.
settle=get('Q32026','partnership_settlement_approx')
bridge={'units':'USD_thousands','reported_quarter_cfo':fmt(get('Q32026','cfo')),'reported_quarter_ppe_capex':fmt(get('Q32026','ppe_capex_signed')),'reported_quarter_fcf':fmt(get('Q32026','fcf_company_reported')),'settlement_approx':fmt(settle),'cash_flow_before_this_payment_only_cfo':fmt(get('Q32026','cfo')+settle),'cash_flow_before_this_payment_only_fcf':fmt(get('Q32026','fcf_company_reported')+settle),'warning':'Timing illustration only. Not recurring FCF, not an income addback. Cost is recognized as a revenue reduction. Do not add 315m to annual/TTM cash flow.'}
(O/'settlement_timing_bridge.json').write_text(json.dumps(bridge,indent=2)+'\n')
flags += [
{'flag':'cash_timing_not_exceptional_economic_cost','period':'Q32026','metric':'fcf','detail':'Approximately 315m partnership payment settles recurring credit-card subsidy liabilities. It is not a litigation settlement or a permanent FCF addback.'},
{'flag':'perimeter_mismatch_risk','period':'2026-09-30','metric':'economic_units_basic','detail':'Consolidated cash flow includes NCI economics. 31.779772m exchangeable Alclear units are excluded from diluted EPS as anti-dilutive; include relevant economic ownership only once.'},
{'flag':'tax_comparability_break','period':'FY2024 and TTM2025-09-30','metric':'net_income','detail':'2024 includes 175.548m release of valuation allowance through income tax and roughly 90.8m TRA establishment charge. NI and EPS are not clean operating growth comparators.'},
{'flag':'fcf_definition','period':'all','metric':'fcf_cfo_less_ppe','detail':'Company FCF deducts PPE purchases only. It is not unlevered FCF or cash attributable solely to class A, and excludes financing-classified TRA/NCI distributions and stock-withholding payments.'},
{'flag':'missing_eps_for_ttm','period':'TTM','metric':'eps','detail':'Not inferred by subtraction of year-to-date EPS or annual denominator. Use reported quarter EPS separately; no TTM EPS valuation supplied.'},
{'flag':'partial_dilution','period':'2026-09-30','metric':'share_count','detail':'Basic economic denominator excludes RSU/PSU vesting scenarios. 4.213967m unvested RSUs require explicit treatment; 0.893234m performance-condition excluded shares are not established as incremental to this pool. Founder PSUs remaining were forfeited July 2, 2026.'},
{'flag':'cash_allocation_not_disclosed','period':'2026-09-30','metric':'liquid_assets','detail':'No parent/Alclear entity split found in Q3 10-Q or FY25 10-K. Consolidated cash cannot automatically be allocated pro rata; TRA is a parent obligation and associated tax benefits must be matched without double counting.'},
{'flag':'software_prior_comparative_inconsistency','period':'2025','metric':'software_capitalized','detail':'Q2 2026 note6 gives 6M2025 software capitalization 6.244m but Q3 2026 note6 gives 9M2025 4.027m; no reconciliation found. FY25 and latest 9M disclosures used for TTM only, not a fabricated quarterly bridge.'},
{'flag':'undisclosed_disaggregation','period':'2026','metric':'partnership_accruals','detail':'Full payment/accrual/reclassification ledger is not disclosed. Do not equate change in total accrued liabilities with solely partnership cost.'}]
with (O/'validation_checks.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=['check','period','metric','difference','status']);w.writeheader();w.writerows(checks)
with (O/'qa_flags.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=['flag','period','metric','detail']);w.writeheader();w.writerows(flags)
with (O/'derivation_provenance.csv').open('w',newline='') as f:
 w=csv.writer(f);w.writerow(['period','metric','value','source_or_formula'])
 for (p,m),v in sorted(F.items()):w.writerow([p,m,fmt(v),'; '.join(prov[(p,m)])])
print('Rebuilt history, TTM comparison, capital perimeter, settlement timing bridge, provenance and QA.')
print('Checks:',len(checks),'failures:',sum(r['status']=='FAIL' for r in checks),'small rounding differences:',sum(r['status']=='rounding_difference' for r in checks))
for p in ['FY2023','FY2024','FY2025','Q42025','Q12026','Q22026','Q32026','TTM2025-09-30','TTM2026-09-30']:
 print(p,{m:fmt(get(p,m)) for m in ['revenue','operating_income','adjusted_ebitda','net_income_parent','cfo','fcf_cfo_less_ppe','stock_compensation']})
if any(r['status']=='FAIL' for r in checks):raise SystemExit('Failed financial checks')
