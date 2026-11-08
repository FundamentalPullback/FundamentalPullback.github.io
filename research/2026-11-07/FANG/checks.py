import pathlib,json,csv
p=pathlib.Path(__file__).parent;h=json.loads((p/'history.json').read_text());r=json.loads((p/'model_results.json').read_text())
for k in h['TTM2026']:assert abs(h['TTM2026'][k]-sum(h[q][k] for q in ['Q42025','Q12026','Q22026','Q32026']))<1e-6,k
for s in r['scenarios'].values():assert s['cumulative_mmboe']<=3617.856-1015*365/1000+1e-6;assert s['whole_equity_value'] is None
for case,s in r['scenarios'].items():
 rows=[x for x in csv.DictReader((p/'finite_cash_scenarios.csv').open()) if x['case']==case]
 assert len(rows)==10 and abs(sum(float(x['pv_cash']) for x in rows)-s['pv_ten_year_cash_window'])<1e-6
 assert all(float(x['funded_drilling_capex'])>=3975 for x in rows)
assert r['approved_value'] is None
(p/'checks.json').write_text(json.dumps({'quarter_ttm_tie':True,'finite_volume_budget':True,'capex_funded_all_ten_years':True,'pv_tie':True,'equity_target_not_asserted':True},indent=2))
