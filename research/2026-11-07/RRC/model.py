import json,pathlib
p=pathlib.Path(__file__).parent
r,e,x=48.72,49.40,.987
out={'type':'mechanical_exchange_only_not_fair_value','as_of':'2026-11-06 regular close','rrc':r,'eqt':e,'ratio':x,'exchange_value':e*x,'gross_spread_usd':e*x-r,'gross_spread_pct_rrc':(e*x/r-1)*100,'eqt_break_even_before_costs':r/x,'fair_value':None,'probability':None,'fcff_complete':False,'sensitivities':[{'eqt_change':c,'eqt':e*(1+c),'exchange_value':e*(1+c)*x,'rrc_return_if_exchange_at_that_price':e*(1+c)*x/r-1} for c in [-.2,-.1,0,.1,.2]]}
assert abs(out['exchange_value']-48.7578)<1e-8
(p/'model_results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
