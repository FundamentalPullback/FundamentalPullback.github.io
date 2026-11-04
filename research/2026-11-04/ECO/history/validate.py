"""Independent numerical tests, written to Validation_Checks.csv and validation.json."""
import json,csv,math
from pathlib import Path
P=Path(__file__).resolve().parent
I=json.loads((P/'inputs.json').read_text());H=json.loads((P/'history.json').read_text());checks=[]
def test(name,actual,expected,tol=1,status='pass'):
 diff=actual-expected
 ok=abs(diff)<=tol
 checks.append(dict(check=name,status=status if ok else'FAIL',actual=actual,expected=expected,difference=diff,tolerance=tol))
for p,r in H['periods'].items():
 f=r['metrics']
 test(p+': revenue less voyage/commissions = TCE',f['revenue_usd']-f['voyage_expenses_usd']-f['commissions_usd'],f['tce_revenue_usd'])
 test(p+': TCE less operating costs = EBIT',f['tce_revenue_usd']-f['vessel_opex_usd']-f['management_fees_usd']-f['da_usd']-f['gna_usd'],f['ebit_reported_usd'])
 test(p+': EBIT to net income',f['ebit_reported_usd']+f['interest_income_usd']-f['finance_cost_usd']+f['unrealized_derivative_gain_usd']+f['realized_derivative_gain_usd']-f['debt_extinguishment_loss_usd']+f['loan_modification_gain_usd']+f['fx_gain_usd'],f['net_income_reported_usd'])
 test(p+': NI plus adjustments plus WC minus paid interest = CFO',f['net_income_reported_usd']+f['cf_reconciliation_adjustments_usd']+f['working_capital_cash_change_usd']-f['interest_paid_usd'],f['cfo_reported_usd'])
 test(p+': investment cash flow',f['restricted_cash_decrease_usd']-f['restricted_cash_increase_usd']-f['drydock_capex_usd']-f['vessel_acquisition_cash_usd']+f['interest_received_usd'],f['cfi_reported_usd'])
 test(p+': financing cash flow',f['debt_draws_usd']-f['debt_repayments_usd']+f['equity_issuance_cash_usd']-f['dividends_paid_usd']-f['capital_distributions_usd']-f['financing_fees_paid_usd'],f['cff_reported_usd'])
 test(p+': CFO plus CFI plus CFF = change excluding FX',f['cfo_reported_usd']+f['cfi_reported_usd']+f['cff_reported_usd'],f['net_cash_change_ex_fx_usd'])
 test(p+': cash opening to closing',f['beginning_cash_usd']+f['net_cash_change_ex_fx_usd']+f['cash_fx_change_usd'],f['ending_cash_usd'])
 test(p+': no unsupported EBIT addback',f['ebit_normalized_usd'],f['ebit_reported_usd'],0)
 test(p+': actual FCF subtracts acquisitions and drydock only',f['fcf_after_actual_investment_usd'],f['cfo_reported_usd']-f['vessel_acquisition_cash_usd']-f['drydock_capex_usd'],0)
 test(p+': normalized NI bridge',f['net_income_normalized_usd'],f['net_income_reported_usd']-f['unrealized_derivative_gain_usd']+f['debt_extinguishment_loss_usd']-f['loan_modification_gain_usd'],0)
 if f['eps_reported_usd'] is not None:test(p+': reported EPS and direct period shares',f['eps_reported_usd'],f['net_income_reported_usd']/f['weighted_average_shares'],.00501)
 if f['daily_tce_reported_usd'] is not None:
  # Vessels' days disclosed to the integer; implied unrounded days may differ <=0.5 day.
  test(p+': daily TCE within half-day reporting precision',f['tce_revenue_usd']/f['daily_tce_reported_usd'],f['operating_days'],.51)

flows=['revenue_usd','tce_revenue_usd','commissions_usd','voyage_expenses_usd','vessel_opex_usd','management_fees_usd','da_usd','gna_usd','ebit_reported_usd','net_income_reported_usd','interest_paid_usd','cfo_reported_usd','drydock_capex_usd','vessel_acquisition_cash_usd','cfi_reported_usd','cff_reported_usd','unrealized_derivative_gain_usd','debt_extinguishment_loss_usd','loan_modification_gain_usd']
for p,parts in [('FY2025',['H12025','Q32025','Q42025']),('FY2024',['H12024','Q32024','Q42024']),('H12026',['Q12026','Q22026']),('H12025',['Q12025','Q22025']),('TTM2026-06',['Q32025','Q42025','Q12026','Q22026']),('TTM2025-06',['Q32024','Q42024','Q12025','Q22025'])]:
 for k in flows:test(p+': independent component sum '+k,sum(H['periods'][q]['metrics'][k]for q in parts),H['periods'][p]['metrics'][k])
 test(p+': displayed operating-day component bridge',sum(H['periods'][q]['metrics']['operating_days']for q in parts),H['periods'][p]['metrics']['operating_days'],len(parts)*.5,'pass_with_rounding_caveat')
# Deliberately frozen source spot checks independent of formula outputs.
for p,k,v in [('FY2023','cfo_reported_usd',174032110),('FY2024','net_income_reported_usd',108863270),('FY2025','revenue_usd',391548819),('Q42025','eps_reported_usd',1.76),('Q42025','weighted_average_shares',33708192),('Q12026','weighted_average_shares',38161939),('Q22026','weighted_average_shares',39044655),('Q22026','tce_revenue_usd',268140097),('H12026','cfo_reported_usd',298897293),('H12026','vessel_acquisition_cash_usd',275819213),('H12026','drydock_capex_usd',1611947),('H12026','interest_paid_usd',18242263)]:test('Frozen primary-source check '+p+' '+k,H['periods'][p]['metrics'][k],v,0)
# Separate 6-K financial-statements exhibit cross-check against the earnings release.
for current,official in [('H12026','H12026_STATEMENTS'),('H12025','H12025_STATEMENTS')]:
 for k in flows:test(current+': separate financial statements exhibit '+k,I['periods'][current]['fields'][k]['value'],I['periods'][official]['fields'][k]['value'])
# Every factual input has source and source row; missing SBC remains null.
for p,r in I['periods'].items():
 for k,f in r['fields'].items():
  assert f['source_id'] in I['sources'] and f['locator'],(p,k)
  if k=='sbc_usd':assert f['value'] is None
fail=[c for c in checks if c['status']=='FAIL']
report={'as_of':I['as_of'],'checks_performed':len(checks),'failed':len(fail),'passed':len(checks)-len(fail),'result':'PASS'if not fail else'FAIL','failures':fail,'material_qa_flags':[{'severity':'caveat','issue':'Operating days are displayed as integers; source quarter/annual bridges differ by one day and daily TCE implies fractional days. Financial USD bridges reconcile.','model_treatment':'Preserve original reported daily rates; calculated TTM daily rate is approximate.'},{'severity':'caveat','issue':'FY2025 audited debt current/non-current split differs from preliminary Q4 release by $88,041,433, with unchanged total debt.','model_treatment':'Use audited 20-F for the balance-sheet maturity classification.'},{'severity':'caveat','issue':'SBC not separately quantified; no zero assumption and no addback.','model_treatment':'Retain all reported G&A.'},{'severity':'caveat','issue':'Derived TTM EPS uses day-weighted shares; there is no company-reported TTM EPS. Current shares differ after issuance.','model_treatment':'Do not divide current stock price by mixed-denominator EPS without disclosure.'},{'severity':'caveat','issue':'Low drydock capex does not include economic fleet replacement.','model_treatment':'Do not label CFO less drydock as sustainable owner FCF.'}]}
(P/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
with(P/'Validation_Checks.csv').open('w',newline='')as f:
 w=csv.DictWriter(f,fieldnames=list(checks[0].keys()));w.writeheader();w.writerows(checks)
with(P/'QA_Flags.csv').open('w',newline='')as f:
 w=csv.DictWriter(f,fieldnames=['severity','issue','model_treatment']);w.writeheader();w.writerows(report['material_qa_flags'])
print(json.dumps(report,indent=2))
if fail:raise SystemExit(1)
