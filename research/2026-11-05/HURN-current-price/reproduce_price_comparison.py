"""Recheck price arithmetic, not re-audit the historical HURN DCF."""
import json,pathlib
p=pathlib.Path(__file__).parent
price=json.loads((p/'price_snapshot.json').read_text())['price']
a=json.loads((p/'current_price_comparisons.json').read_text())
for k,x in a.items():
 assert abs(x['return_to_value']-(x['value']/price-1))<1e-12
 assert abs(x['margin_of_safety']-(1-price/x['value']))<1e-12
print(json.dumps({'checks':2*len(a),'failed':0,'scope':'current price arithmetic only'}))
