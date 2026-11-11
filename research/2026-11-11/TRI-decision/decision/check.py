from pathlib import Path
import json,hashlib
b=Path(__file__).resolve().parent;p=b.parent/'site/research/2026-11-04/TRI/model.json';
if not p.exists(): p=b.parents[2]/'2026-11-04/TRI/model.json'
m=json.loads(p.read_text());a=m['base_assumptions'];price=108.41
royalty10=a['annualized_royalty_start_m']*(1+a['royalty_growth'])**10
# Sensitivity ONLY: remove the legacy blended-margin royalty contribution from terminal.
# Not a forecast of contract expiry: initial ten-year term may be renewed. Retained costs unknown.
terminal_contribution=royalty10*(1+a['royalty_growth'])*a['terminal_EBIT_margin']*(1-a['tax'])*(1-a['terminal_core_growth']/a['terminal_incremental_ROIC'])
pv=terminal_contribution/(a['WACC']-a['terminal_core_growth'])/(1+a['WACC'])**10
cf=m['expected_return'];flows=cf['cash_to_common_m'];terminal=cf['terminal_equity_m'];shares=m['shares_m']
def irr(px):
 lo,hi=-.5,1
 for _ in range(120):
  r=(lo+hi)/2;npv=sum(f/(1+r)**i for i,f in enumerate(flows,1))+terminal/(1+r)**10-px*shares
  if npv>0:lo=r
  else:hi=r
 return (lo+hi)/2
assert abs(irr(109.78)-cf['at_price'])<1e-9
assert abs(royalty10-49.69516595678543)<1e-8
assert abs(m['base']['terminal_fcff']-((m['base']['rows'][-1]['rev']-royalty10)*1.03+royalty10*.95)*.325*.79*.88)<1e-8
out={'legacy_model_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'scope':'Frozen November4 model sensitivity; not refreshed fair value','regular_close_20261110':price,'historical_central':m['base']['value'],'historical_favorable':m['bull']['value'],'legacy_illustrative_IRR_at_current_close':irr(price),'royalty_year10':royalty10,'legacy_terminal_FCFF_royalty_component':terminal_contribution,'no_renewal_terminal_only_PV_reduction_m':pv,'per_share_reduction':pv/shares,'central_after_terminal_only_sensitivity':m['base']['value']-pv/shares,'continuing_SBC_9m26':106,'continuing_SBC_9m25':84,'continuing_SBC_growth':106/84-1,'combined_annual25_SBC':111,'cross_perimeter_TTM_arithmetic_NOT_verified':111+106-84,'DCF_SBC_double_subtraction':False,'price_implies_entry':False}
(b/'results.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
