from pathlib import Path
import json
P=Path(__file__).parent
f=json.load(open(P/'financials.json'))['ttm'][-1];m=json.load(open(P/'model.json'));rows=json.load(open(P/'comps/results.json'))
equity=117.97*142.5;ev=equity+3527.8-850.7-576.2
has=dict(ticker='HAS',ttm_end='2026-09-27',price_date='2026-11-03',price=117.97,shares_proxy=142.5,equity_proxy=equity,debt_nominal=3527.8,cash_unrestricted=1426.9,ev_proxy=ev,ttm_sales=f['revenue'],ttm_ebit=f['operating_income'],ebit_margin=f['operating_income']/f['revenue'],ev_ebit=ev/f['operating_income'],ttm_cfo=f['cfo'],ttm_capex=f['capex'],ttm_sbc=f['sbc'],owner_cash=f['owner_cash_proxy'],owner_cash_yield=f['owner_cash_proxy']/equity,normalized_ebit=f['operating_income']-54.5,ev_normalized_ebit=ev/(f['operating_income']-54.5),owner_cash_ex_gross_refund_sensitivity=f['owner_cash_proxy']-43.4,owner_cash_yield_ex_gross_refund_sensitivity=(f['owner_cash_proxy']-43.4)/equity)
json.dump(dict(rows=[has]+rows,method='Common price date and trailing methodology, not common period end. EV proxy uses quarter-average shares and reported cash, no DCF operating cash reserve. Tariff sensitivities separated. JAKK inventory refund pass-through not fully identified; MAT June data pending Nov5 earnings.'),open(P/'peers.json','w'),indent=2)
print(has)
