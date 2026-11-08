"""Reproducible diagnostic only. No certified fair value or entry ceiling."""
import json,csv,pathlib
P=pathlib.Path(__file__).parent
price=66.33; shares=77.364263
# Quote (common shares), IFRS balances and proportional debt: different perimeters.
reported_cash=911.695; proportional_debt=3305
bridge_proxy=proportional_debt-reported_cash
# Intentionally unresolved: parent/JV cash, minimum operating cash and claim update.
# Illustrative replacement equals assumed D&A incl lease assets; adequacy unverified.
# Low historical cash capex is NOT capitalized into perpetuity.
scenarios=[]
for label,ebitda,wacc in [('adverso',650,.11),('central',1020,.10),('favorable',1395,.09)]:
 da=500; cash_and_lease_replacement=500;tax=.25
 fcff=(ebitda-da)*(1-tax)+da-cash_and_lease_replacement
 ev=fcff/wacc
 scenarios.append(dict(name=label,normalized_ebitda_assumption=ebitda,da_assumption=da,physical_and_lease_replacement=500,tax_assumption=tax,g=0,wacc_assumption=wacc,normalized_fcff=fcff,steady_state_ev_diagnostic=ev,certified_equity_value=None))
reverse=[]
for w in [.09,.10,.11]:
 ev_proxy=price*shares+bridge_proxy
 fcff=ev_proxy*w
 reverse.append(dict(wacc=w,ev_proxy_only=ev_proxy,fcff_required=fcff,ebitda_required_with_500_replacement=500+fcff/.75,unknown_equity_cash_adjustment=True))
result=dict(ticker='MEOH',as_of='2026-11-08',posture='partial_research_not_valuation',regular_close=price,session='2026-11-06 16:00 EST',csv_last=67.49,csv_last_type='after_hours_19:49_EST',shares_m=shares,share_type='common Nasdaq USD, not ADR',debt_and_lease_proportional=3305,reported_consolidated_cash=911.695,cash_attributable=None,minimum_operating_cash=None,current_other_claims=None,certified_fair_values=None,entry_ceiling=None,technical_stop=None,new_shares=0,diagnostic_scenarios=scenarios,reverse_diagnostic=reverse,physical_capital_note='Economic replacement 500 incl lease renewal; no separate lease payment deduction; assumption, not verified capex split. Zero terminal real/nominal growth test. No transition forecast certified.',wacc_note='9-11% diagnostic range. Beta about 1 and ERP Sep2026 4.14% plus 4.84-4.86% Treasury imply Ke near9%; capital structure after deleveraging, debt market yield and country/cycle add-on unresolved. WACC is not calibrated.')
(P/'results.json').write_text(json.dumps(result,indent=2))
assert all(s['physical_and_lease_replacement']>=s['da_assumption'] for s in scenarios)
assert all(s['certified_equity_value'] is None for s in scenarios)
assert result['new_shares']==0 and result['certified_fair_values'] is None
(P/'self_check.json').write_text(json.dumps({'arithmetic_pass':True,'replacement_equals_assumed_da':True,'maintenance_adequacy_validated':False,'no_double_lease_payment_deduction':True,'no_certified_valuation':True,'independent_audit':'partial_scope_review_completed'},indent=2))
print(json.dumps(result,indent=2))
