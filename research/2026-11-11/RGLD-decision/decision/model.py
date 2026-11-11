import pathlib,json,runpy,contextlib,io,hashlib
B=pathlib.Path(__file__).resolve().parent
with contextlib.redirect_stdout(io.StringIO()):m=runpy.run_path(str(B/'legacy_model.py'))
c=m['calc'];price=274.57;rf=.0498;erp=.0441;beta=.46
rates={'shrunk_beta':rf+(2*beta/3+1/3)*erp,'raw_beta':rf+beta*erp}
grid={k:{str(r):c(wacc=w,replacement=r)['value'] for r in [0,.06,.12,.18,.22]} for k,w in rates.items()}
# A completed cash payment replaces the already-reserved commitment. No double subtraction.
bridge=m['bridge'].copy();bridge['warintza_final_payment_nov9'] = bridge.pop('warintza_committed_payment');assert sum(bridge.values())==m['net']
# This central-operations sensitivity is not an upper bound across all operating/metal scenarios.
fav=c(g=.035,metal=1.1,margin=.67,wacc=rates['raw_beta'],roic=.15,terminalg=.02,replacement=.18)
result=dict(as_of='2026-11-11',reference_close=price,price_date='2026-11-10 16:00 EST',legacy_sha256=hashlib.sha256((B/'legacy_model.py').read_bytes()).hexdigest(),rate_assumptions=dict(rf=rf,erp=erp,preserved_beta=beta,shrunk_beta=2*beta/3+1/3),rates=rates,grid=grid,bridge=bridge,net_bridge=sum(bridge.values()),favorable_updated_rate=fav['value'],zero_replacement_raw_discount_pct=(grid['raw_beta']['0']/price-1)*100,scope='Unchanged Nov7 operating assumptions and dated capital bridge. Rate/replacement sensitivity, not asset NAV or fresh balance-sheet certification. Zero replacement is deliberately generous counterfactual, not sustainable cash forecast.')
(B/'results.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
