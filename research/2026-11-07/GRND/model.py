"""Control de filtros, sin DCF; millones USD salvo precio y acciones."""
import json
from pathlib import Path
p=Path(__file__).parent
r=dict(price=13.54,session='2026-11-06 16:00 America/New_York',minimum_price=15,price_gate_pass=13.54>=15,shares=176729538,shares_date='2026-11-04',market_cap_million=176729538*13.54/1e6,capitalization_gate_pass=176729538*13.54>=2e9,ttm_revenue=439.898+409.456-313.924,ttm_operating_income=126.288+79.315-94.979,ttm_net_income=94.751+37.894-74.491,approved_values=None,valuation=None)
(p/'model_results.json').write_text(json.dumps(r,indent=2));print(r)
