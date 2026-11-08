"""Revisión de filtros, no valoración. USD millones salvo acciones/precio."""
import json
from pathlib import Path
p=Path(__file__).parent
q=[dict(period='2025Q4',revenue=172.113,operating_income=-8.294,net_income=-1.394),dict(period='2026Q1',revenue=165.798,operating_income=2.094,net_income=7.834),dict(period='2026Q2',revenue=175.995,operating_income=3.636,net_income=7.567),dict(period='2026Q3',revenue=176.179,operating_income=6.275,net_income=115.442)]
t={k:sum(x[k] for x in q) for k in ['revenue','operating_income','net_income']}
a,b,price=96014739,7796104,18.59
r=dict(asof='2026-11-08',price=price,price_session='2026-11-06 16:00 America/New_York',shares_date='2026-10-30',class_A=a,class_B=b,total_shares=a+b,market_cap_million=(a+b)*price/1e6,capitalization_basis='Latest disclosed October30 actual shares times November6 ClassA regularclose; not verified same-day sharecount',same_day_share_count_verified=False,additional_shares_to_2bn_at_fixed_price=2e9/price-(a+b),capitalization_minimum_million=2000,capitalization_gate_pass=(a+b)*price>=2e9,price_gate_pass=price>=15,ttm=t,operating_margin=t['operating_income']/t['revenue'],net_margin=t['net_income']/t['revenue'],profit_gate_pass=t['operating_income']>=0 and t['net_income']>=0,price_at_2bn_if_shares_unchanged=2e9/(a+b),approved_values=None,valuation=None)
(p/'model_results.json').write_text(json.dumps(r,indent=2));(p/'financial_history.json').write_text(json.dumps(dict(scope='four_quarters_profit_screen_only',units='USD million',quarters=q,ttm=t),indent=2));print(json.dumps(r,indent=2))
