from pathlib import Path
import json
p=Path(__file__).parent;i=json.loads((p/'inputs.json').read_text());out={}
for k,a in i.items():
 rev=a.get('revenue') or a['fy_revenue']+a['current_ytd_revenue']-a['prior_ytd_revenue'];ebit=a.get('ebit_comparison') or a['fy_ebit']+a['current_ytd_ebit']-a['prior_ytd_ebit']
 ev=a['price']*a['shares']+a['debt']+a['nci']-a['cash']
 out[k]={'revenueTTM':rev,'ebitSelected':ebit,'operatingMargin':ebit/rev,'basicEquityMarketProxy':a['price']*a['shares'],'simpleEVExLeasesAndOtherClaims':ev,'simpleEVtoEBIT':ev/ebit,'notes':'Comparison only, not target. Dated capital, heterogeneous plan adjustments and business mixes. All operating leases excluded and lease expense retained. MAN swaps/pensions/tax claims not in this simple EV; not model bridge.'}
(p/'outputs.json').write_text(json.dumps(out,indent=2)+'\n');print(out)
