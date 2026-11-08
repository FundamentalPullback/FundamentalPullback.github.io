import pathlib,json,csv,math
P=pathlib.Path(__file__).parent;h=json.loads((P/'history.json').read_text());m=json.loads((P/'model_results.json').read_text());s=json.loads((P/'screen_results.json').read_text())
for k in h['TTM2026']:
 assert abs(sum(h[q][k] for q in ['Q42025','Q12026','Q22026','Q32026'])-h['TTM2026'][k])<1e-8
assert h['TTM2026']['cfo_less_capex']==5218
assert abs(m['reserve_reconciliation']['sum_2025_mmboe']-4993.282)<1e-8
assert m['issuer_2027_sources_uses']['identity_difference']==0
assert s['ttm_eps_sum_quarters']==4.
for name,x in m['scenarios'].items():
 rows=list(csv.DictReader((P/('forecast_'+name+'.csv')).open()))
 pv=sum(float(a['pre_financing_cash'])/(1+x['discount_rate_assumption'])**(int(a['year'])-2026) for a in rows)
 assert abs(pv-x['cash_window_pv_end2026_before_closure_basis_hedges_and_unmodeled_assets'])<1e-6
 for a in rows:
  assert abs(float(a['oil_mmbbl'])+float(a['ngl_mmbbl'])+float(a['gas_bcf'])/6-float(a['total_mmboe']))<1e-7
 assert x['current_whole_equity_value'] is None and x['terminal_unmodeled_asset_value'] is None
r={'arithmetic':'pass','ten_year_volume_and_cash_identities':'pass','reported_TTM_vs_4quarters':'pass','sources_uses15.5bn':'pass','scope':'Cash-window diagnostic explicitly NOT reserve-certified, not full NAV and not a price target; economic calibration remains unapproved'}
(P/'checks.json').write_text(json.dumps(r,indent=2));print(r)
