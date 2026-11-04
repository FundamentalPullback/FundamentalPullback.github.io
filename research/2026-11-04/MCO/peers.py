from pathlib import Path
import json
P=Path(__file__).parent;mc=503.69*173.3;ev=mc+7120+144-1513-108
j=json.load(open(P/'comps/results.json'));j['MCO']=dict(price=503.69,price_date='2026-11-03',shares_diluted_average=173.3,market_cap_proxy=mc,ev_standard_proxy=ev,ev_ebit=ev/3644,owner_fcf=2744,owner_yield=2744/mc,ev_ebit_including_net_derivative_reserve=(ev+488)/3644,limits=['Diluted weighted-average share denominator unlike current actual peer shares.','Standard EV excludes special capital reserves; derivative-included variant also shown.','TTM includes partial divested-business operations; not certified retained-perimeter proforma.'])
json.dump(j,open(P/'peers.json','w'),indent=2);print(j['MCO'])
