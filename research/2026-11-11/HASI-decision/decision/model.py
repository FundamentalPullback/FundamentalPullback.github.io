import pathlib,json
B=pathlib.Path(__file__).parent
face=500.;net=493.3;coupon=.0785;cashcoupon=face*coupon;fees=face-net
refi=[]
for oldrate in [.045,.055,.065,.075]:
 avoided=net*oldrate
 refi.append(dict(assumed_repaid_debt_rate=oldrate,old_interest_avoided=avoided,new_cash_coupon=cashcoupon,annual_incremental_coupon=cashcoupon-avoided))
assets=[]
for y in [.10,.12,.14]:
 gross=net*y;assets.append(dict(hypothetical_cash_asset_yield=y,gross_cash_income=gross,coupon_only_residual=gross-cashcoupon,after_100bp_losses_and_50bp_overhead=gross-cashcoupon-net*.015))
x=dict(as_of='2026-11-11',units='USDmillions',face=face,estimated_net_proceeds=net,offering_cost_estimate=fees,annual_initial_coupon=cashcoupon,coupon_over_net_proceeds=cashcoupon/net,not_yield_to_maturity=True,full_refinance_nominal_debt_change=face-net,refinance_scenarios=refi,full_deployment_scenarios=assets,settled=False,scope='Initial-rate annualized diagnostics, not amortized effective yield or post-reset forecast. Full refinancing and full incremental deployment are separate hypothetical states, not additive. No new valuation or assured investment income.')
assert abs(cashcoupon-39.25)<1e-10;assert all(a['annual_incremental_coupon']>b['annual_incremental_coupon'] for a,b in zip(refi,refi[1:]));(B/'results.json').write_text(json.dumps(x,indent=2));print(json.dumps(x,indent=2))
