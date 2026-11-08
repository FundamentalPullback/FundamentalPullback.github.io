"""Control reproducible del filtro de precio; no es una valoración."""
import json
from pathlib import Path
p=Path(__file__).parent
r=dict(ticker='UMC',currency='USD',security='NYSE ADS',ordinary_shares_per_ads=5,regular_close=13.85,session='2026-11-06 16:00 America/New_York',minimum_price=15,price_gate_pass=13.85>=15,shortfall_percent=(13.85/15-1)*100,valuation_per_ads=None,approved_values=None)
(p/'model_results.json').write_text(json.dumps(r,indent=2))
print(json.dumps(r,indent=2))
