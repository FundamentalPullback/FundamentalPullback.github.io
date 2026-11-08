import pathlib,json,csv
p=pathlib.Path(__file__).parent;h=json.loads((p/'history.json').read_text());r=json.loads((p/'model_results.json').read_text());a=list(csv.DictReader((p/'finite_cash_scenarios.csv').open()))
for k in h['TTM2026']:assert abs(h['TTM2026'][k]-sum(h[q][k] for q in ['Q42025','Q12026','Q22026','Q32026']))<1e-6,k
for name,s in r['scenarios'].items():
 rows=[x for x in a if x['case']==name];assert len(rows)==10
 assert abs(sum(float(x['pv_cash']) for x in rows)-s['pv_finite_cash_bucket'])<1e-6
 for prod,col in [('oil','oil_mmbbl'),('gas','gas_bcf'),('ngl','ngl_mmbbl')]:assert sum(float(x[col]) for x in rows)<=r['historical_budget_after_assumed_2026_production'][prod]+1e-6
 assert all(float(x['funded_dc_capex'])>0 for x in rows if float(x['production_mmboe'])>0)
 assert all(float(x['existing_hedge_settlement'])==0 for x in rows[1:])
 assert s['whole_equity_value'] is None
assert r['approved_value'] is None
(p/'checks.json').write_text(json.dumps({'quarter_ttm_tie':True,'separate_product_finite_budget':True,'funded_production':True,'hedges_only_disclosed_period':True,'PV_ties':True,'no_equity_target':True},indent=2))
