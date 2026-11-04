#!/usr/bin/env python3
"""Offline reconciliations. Produces validation.json and validation.csv."""
import json,csv,sys
from pathlib import Path
from calculate import calculate
ROOT=Path(__file__).resolve().parent
D=json.loads((ROOT/'inputs.json').read_text());H=json.loads((ROOT/'history.json').read_text());P=H['periods'];checks=[]
def check(name,actual,expected,tolerance=0.16,scope=''):
 ok=(actual==expected) if not isinstance(actual,(int,float)) else abs(actual-expected)<=tolerance
 checks.append({'name':name,'scope':scope,'actual':actual,'expected':expected,'tolerance':tolerance,'passed':ok})
for k,p in P.items():
 check('gross less revenue costs equals net revenue',p['gross_revenue']-p['cost_of_revenue'],p['net_revenue'],scope=k)
 check('cost components sum',sum(p[m] for m in ['liquidity_payments','routing_clearing_cost','regulatory_fee_cost','royalty_other_cost']),p['cost_of_revenue'],scope=k)
 check('revenue captions sum',sum(p[m] for m in ['gross_cash_spot','gross_data_vantage','gross_derivatives']),p['gross_revenue'],scope=k)
 check('net revenue less opex plus disposal gain equals EBIT',p['net_revenue']-p['operating_expenses']+p['divestiture_gain'],p['ebit'],scope=k)
 check('EBIT plus nonoperating equals pretax income',sum(p[m] for m in ['ebit','interest_expense','interest_income','investment_income','other_income']),p['pretax_income'],scope=k)
 check('pretax less tax equals consolidated income',p['pretax_income']-p['income_tax'],p['net_income'],scope=k)
 check('income less participating allocation equals common income',p['net_income']+p['participating_securities'],p['net_income_common'],scope=k)
 check('ex-clearing cash generation recomputation',p['cfo']-p['clearing_customer_cash_flow']-p['capex_cash'],p['cash_generation_ex_clearing_proxy'],scope=k)
 check('economic SBC deduction',p['cash_generation_ex_clearing_proxy']-p['sbc'],p['cash_generation_ex_clearing_less_sbc_proxy'],scope=k)
 check('conservative EBIT bridge',p['ebit']-p['divestiture_gain']+p['impairment']+p['contingent_remeasurement'],p['normalized_ebit_conservative'],scope=k)
 check('no invented normalized EPS',p['normalized_eps'],None,scope=k)
 if p['period_type']!='TTM':check('diluted EPS tie within source rounding',p['net_income_common']/p['shares_diluted'],p['eps_diluted'],.02,k)
for k in ['Q4_2025','Q4_2024']:
 f=D['periods'][k]['facts']['shares_diluted'];check('Q4 share count direct source',f['source_id'],'q4release_2025',scope=k)
for k,qs in [('TTM2026Q3',['Q4_2025','Q1_2026','Q2_2026','Q3_2026']),('TTM2025Q3',['Q4_2024','Q1_2025','Q2_2025','Q3_2025'])]:
 for m in ['net_revenue','ebit','net_income_common','cfo','clearing_customer_cash_flow','capex_cash','sbc','normalized_ebit_conservative','normalized_ebit_exit_cost_sensitivity']:
  check('four quarters equal TTM',sum(P[q][m] for q in qs),P[k][m],.2,k+'.'+m)
 check('TTM EPS explicitly quarterly sum',sum(P[q]['eps_diluted'] for q in qs),P[k]['eps_diluted_quarterly_sum'],.001,k)
for p in H['balance_sheets']:
 check('balance sheet balances',p['total_liabilities']+p['equity'],p['total_assets'],scope=p['date'])
 check('clearing assets/liabilities match',p['clearing_assets'],p['clearing_liabilities'],scope=p['date'])
 check('safeguarded digital assets/liabilities match',p['digital_safeguarded_assets'],p['digital_safeguarded_liabilities'],scope=p['date'])
l=H['liquidity'];check('latest total cash reconciliation',sum(l[k] for k in ['latest_cash_bs','latest_cash_held_for_sale','latest_clearing_restricted_cash','latest_other_restricted_cash','latest_customer_bank_deposits']),l['latest_cash_flow_total'])
check('issuer adjusted cash reconciliation',l['latest_cash_bs']+l['latest_cash_held_for_sale']+l['latest_financial_investments']-l['latest_deferred_comp_assets'],l['latest_company_adjusted_cash'])
check('corporate ex-held-for-sale cash reconciliation',l['latest_company_adjusted_cash']-l['latest_cash_held_for_sale'],l['corporate_cash_plus_unmatched_financial_investments_ex_hfs'])
check('cash geographic reconciliation',l['latest_foreign_cash_including_hfs']+l['latest_us_cash'],l['latest_cash_bs']+l['latest_cash_held_for_sale'])
check('committed revolver excludes conditional accordion',l['latest_undrawn_corporate_revolver'],400.0)
check('optional revolver accordion separately disclosed',l['latest_optional_uncommitted_revolver_accordion'],200.0)
check('deferred compensation matched',l['latest_deferred_comp_assets'],l['latest_deferred_comp_liabilities'])
check('debt carrying equals face less issuance costs',l['latest_debt_face']-5.7,l['latest_debt_carrying'])
for pid,per in D['periods'].items():
 for metric,f in per['facts'].items():check('reported input has valid source',f['source_id'] in D['sources'],True,scope=pid+'.'+metric)
regen,_=calculate(D);check('offline deterministic reproduction',regen==H,True)
issues=[{'severity':'material_caveat','topic':'CFO','detail':'Reported CFO contains clearing/customer-fund flows. Ex-clearing cash generation is not unrestricted or fully regulatory-adjusted FCF.'},{'severity':'material_caveat','topic':'SBC','detail':'All SBC remains in normalized EBIT; supplemental cash measure deducts SBC rather than treating it as free.'},{'severity':'material_caveat','topic':'Disposals','detail':'Australia gain excluded; Canada remains pending. No fabricated standalone continuing-business TTM.'},{'severity':'material_caveat','topic':'Foreign/regulatory cash','detail':'Corporate cash proxy is not fully distributable. Foreign cash may be indefinitely reinvested; avoid double counting regulatory capital against a combined reserve.'},{'severity':'material_caveat','topic':'EPS','detail':'TTM diluted EPS 14.06 is sum of reported quarters. FY+YTD-minus-priorYTD EPS produces 14.05 due rounding/dilution. Analyst normalized EPS withheld.'},{'severity':'classification','topic':'Section31','detail':'Payable $46.9m is working capital, issuer reports zero collected cash. Matching receivable not separately quantified; do not call payable pure corporate debt.'},{'severity':'comparability','topic':'CAPEX','detail':'2026 cash purchases label explicitly includes data processing software; full reported purchases line retained in every period. Separate incremental licensing cash fees not disclosed.'}]
res={'status':'PASS' if all(x['passed'] for x in checks) else 'FAIL','checks_passed':sum(x['passed'] for x in checks),'checks_total':len(checks),'failed_checks':[x for x in checks if not x['passed']],'checks':checks,'qa_flags':issues}
(ROOT/'validation.json').write_text(json.dumps(res,indent=2)+'\n')
with (ROOT/'validation.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(checks[0]));w.writeheader();w.writerows(checks)
with (ROOT/'qa_flags.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=['severity','topic','detail']);w.writeheader();w.writerows(issues)
print(res['status'],res['checks_passed'],'/',len(checks))
for x in res['failed_checks']:print(x)
sys.exit(0 if res['status']=='PASS' else 1)
