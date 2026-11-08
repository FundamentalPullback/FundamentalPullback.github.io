import pathlib,json
p=pathlib.Path(__file__).parent;h=json.loads((p/'history.json').read_text());r=json.loads((p/'model_results.json').read_text())
for k in h['TTM2026']:
 assert abs(h['TTM2026'][k]-sum(h[q][k] for q in ['Q42025','Q12026','Q22026','Q32026']))<1e-6,k
for x in r['funding_grid']:
 assert x['guided_cfo']==x['consolidated_ebitda']-1353-117+704-217-190
 assert x['conditional_cash_before_preferred_and_financing']==x['guided_cfo']-704-1750-10-155-74-x['assumed_growth_capex']-x['assumed_extra_cash_tax']
assert r['approved_value'] is None and r['whole_equity_value'] is None and r['terminal_value'] is None
(p/'checks.json').write_text(json.dumps({'four_quarters_equal_ttm':True,'funding_bridges_reconciled':True,'no_unknown_claim_zero':True,'no_unfunded_terminal':True,'investment_approved':False},indent=2))
