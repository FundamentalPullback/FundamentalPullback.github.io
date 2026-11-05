"""Recompute limited, pre-transaction balance-sheet screens; stdlib only."""
import json
from pathlib import Path
P = Path(__file__).resolve().parent
inputs = json.loads((P/'inputs.json').read_text())
result = {'asof': inputs['asof'], 'posture':'screening_only_not_current_EV_or_equal_perimeter_valuation', 'companies':{}}
for ticker, x in inputs['companies'].items():
    if ticker == 'GWRE':
        revenue, ebit, amort = x['revenue_fy'], x['ebit_fy'], x['acquired_amort_fy']
    else:
        revenue = x['revenue_fy'] + x['revenue_h1_current'] - x['revenue_h1_prior']
        ebit = x['ebit_fy'] + x['ebit_h1_current'] - x['ebit_h1_prior']
        amort = x['acquired_amort_fy'] + x['acquired_amort_h1_current'] - x['acquired_amort_h1_prior']
    net_debt = x['debt_principal'] + x['finance_lease_liability'] - x['cash'] - x['marketable']
    cap = x['price']*x['cover_shares_m']
    ev = cap + net_debt
    out = dict(price=x['price'], price_date=x['price_date'], operating_period_end='2026-07-31', revenue=revenue, ebit_gaap=ebit, acquired_amortization=amort, ebit_before_acquired_amortization=ebit+amort, gaap_margin=ebit/revenue, margin_before_acquired_amortization=(ebit+amort)/revenue, historical_share_count_marketcap=cap, july_balance_net_debt=net_debt, july_balance_screen_ev=ev, july_balance_screen_ev_ebit=ev/ebit, july_balance_screen_ev_ebit_before_acquired_amort=ev/(ebit+amort))
    if ticker=='WDAY':
        delta=x['october_new_notes_principal']-x['october_net_proceeds']
        out['october_financing_ONLY_ev_delta']=delta
        out['october_financing_ONLY_ev_ebit']=(ev+delta)/ebit
        out['october_financing_ONLY_ev_ebit_before_acquired_amort']=(ev+delta)/(ebit+amort)
    result['companies'][ticker]=out
assert result['companies']['GWRE']['ebit_gaap']==149.874
assert result['companies']['CRM']['ebit_gaap']==8735
assert result['companies']['WDAY']['ebit_gaap']==1085
(P/'results.json').write_text(json.dumps(result, indent=2)+'\n')
print(json.dumps(result, indent=2))
