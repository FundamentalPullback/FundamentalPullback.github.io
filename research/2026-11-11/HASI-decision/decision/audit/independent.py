import json,pathlib,math
p=pathlib.Path(__file__).resolve().parents[1]
r=json.loads((p/'results.json').read_text()); checks=[]
def check(label,a,b):
 assert math.isclose(a,b,abs_tol=1e-10), (label,a,b)
 checks.append(label)
check('annual_coupon',r['annual_initial_coupon'],500*7.85/100)
check('fees',r['offering_cost_estimate'],6.7)
check('net_coupon_ratio',r['coupon_over_net_proceeds'],39.25/493.3)
check('debt_change_full_refi',r['full_refinance_nominal_debt_change'],500-493.3)
for a,rate in zip(r['refinance_scenarios'],[.045,.055,.065,.075]):
 check('avoided_'+str(rate),a['old_interest_avoided'],493.3*rate)
 check('increment_'+str(rate),a['annual_incremental_coupon'],39.25-493.3*rate)
for a,y in zip(r['full_deployment_scenarios'],[.10,.12,.14]):
 check('income_'+str(y),a['gross_cash_income'],493.3*y)
 check('spread_'+str(y),a['coupon_only_residual'],493.3*y-39.25)
 check('losses_overhead_'+str(y),a['after_100bp_losses_and_50bp_overhead'],493.3*(y-.015)-39.25)
assert r['not_yield_to_maturity'] and not r['settled']
out={'status':'PASS','numerical_checks':len(checks),'checks':checks,'review':['No production calculation imported.','39.25 is annual initial-rate run-rate, not first stub payment.','Coupon/net is not effective yield or YTM.','6.7 nominal-debt delta assumes all net proceeds retire existing debt at par; no actual balance certified.','Refinance/deployment alternatives not simultaneous benefits.','Loss/overhead and asset-return assumptions illustrative; no tax, dilution, funding timeline or full valuation inferred.','No equity classification of junior debt or free-proceeds treatment.']}
(pathlib.Path(__file__).parent/'output.json').write_text(json.dumps(out,indent=2)+'\n'); print(json.dumps(out))
