import pathlib,json,hashlib
B=pathlib.Path(__file__).resolve().parent;m=json.loads((B/'legacy_model.json').read_text());bridge=m['bridge'];base=m['cases']['base'];s=bridge['valuation_shares'];v=base['value'];e=base['equity'];p=164.14
cases=[]
for price in [v,140,156.82,164.14,180,200]:
 retired=500/price;ns=s-retired;ne=e-500;value=ne/ns
 cases.append(dict(assumed_effective_final_price=price,shares_retired_m=retired,remaining_shares_m=ns,equity_after_m=ne,value_after=value,change_pct=(value/v-1)*100))
funding=[]
for debt in [0,250,500]:
 funding.append(dict(assumed_new_debt=debt,cash_used=500-debt,net_cash_change=-500,bridge_after=bridge['equity_adjustment']-500,interest_service=[dict(assumed_rate=r,annual_pretax=debt*r,annual_aftertax_if_deductible=debt*r*.73) for r in [.06,.08]]))
w=.0498+1.27*.0441
rows=base['rows'];ev=sum(x['fcff']/(1+w)**x['year'] for x in rows[:10])+rows[10]['fcff']/(w-.025)/(1+w)**10
rate_check=dict(rf=.0498,assumed_erp=.0441,observed_beta=1.27,simple_capm_rate=w,value_before_asr=(ev+bridge['equity_adjustment'])/s,conditional_full_settlement_value=(ev+bridge['equity_adjustment']-500)/(s-500/p),not_post_asr_wacc=True)
r=dict(rate_sensitivity=rate_check,as_of='2026-11-11',reference_close=p,close_date='2026-11-10 16:00 EST',prior_model_sha256=hashlib.sha256((B/'legacy_model.json').read_bytes()).hexdigest(),old_base_value=v,old_equity_m=e,old_shares_proxy_m=s,old_bridge_m=bridge['equity_adjustment'],signed_asr_amount_m=500,expected_initial_shares=2550695,initial_shares_reference_dollars=2550695*156.82,actual_initial_delivery_verified=False,actual_funding_split_verified=False,final_settlement_cases=cases,funding_cases=funding,scope='Static same-EV full share-settlement sensitivity, not signed agreement fair-value accounting or actual settled shares. Final effective prices are scenarios not known VWAP/discount. Interest diagnostic not deducted from FCFF; financing risk/fees/new cash flows excluded.')
assert abs(cases[0]['value_after']-v)<1e-8
assert all(cases[i]['value_after']>cases[i+1]['value_after'] for i in range(len(cases)-1))
(B/'results.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
