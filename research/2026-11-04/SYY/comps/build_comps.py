#!/usr/bin/env python3
"""Offline, standard-library-only peer comparison. USD millions except prices/multiples."""
import json
from pathlib import Path
P = Path(__file__).resolve().parent

def build(inputs):
    rows = []
    for x in inputs['peers']:
        ebit = x['ebit']['fy'] + x['ebit']['current_ytd'] - x['ebit']['prior_ytd']
        amort = x['intangible_amortization']['fy'] + x['intangible_amortization']['current_ytd'] - x['intangible_amortization']['prior_ytd']
        equity = x['close_usd'] * x['shares_outstanding'] / 1_000_000
        capital = x['capital']
        principal = capital['financial_debt_principal_m']
        ev = None if principal is None else equity + principal + capital['finance_leases_m'] - capital['unrestricted_cash_m']
        proxy = equity + capital['financial_debt_carrying_m'] + capital['finance_leases_m'] - capital['unrestricted_cash_m']
        r = {'ticker': x['ticker'], 'price_date': inputs['price_date'], 'close_usd': x['close_usd'],
             'shares_date': x['shares_date'], 'capital_date': capital['date'], 'ttm_end': x['ttm_end'],
             'market_cap_m': round(equity, 6), 'ttm_gaap_ebit_m': round(ebit, 6),
             'ttm_intangible_amortization_m': round(amort, 6),
             'ttm_ebit_plus_intangible_amortization_m': round(ebit + amort, 6),
             'principal_based_ev_m': None if ev is None else round(ev,6),
             'principal_based_ev_to_gaap_ebit': None if ev is None else round(ev / ebit, 6),
             'principal_based_ev_to_ebit_plus_amortization': None if ev is None else round(ev / (ebit+amort),6),
             'carrying_debt_ev_proxy_m': round(proxy,6),
             'carrying_debt_ev_proxy_to_gaap_ebit': round(proxy/ebit,6),
             'carrying_debt_ev_proxy_to_ebit_plus_amortization': round(proxy/(ebit+amort),6),
             'limitations': x['limitations']}
        assert ebit > 0 and amort >= 0 and equity > 0
        if principal is not None: assert principal >= capital['financial_debt_carrying_m']
        rows.append(r)
    return {'as_of':inputs['as_of'],'units':'USD millions except share prices, actual share counts and multiples',
            'methodology':inputs['methodology'], 'peers':rows,
            'conclusion':'Context only. No peer median, implied SYY target, or claim of synchronized current capital. PFGC exact principal EV is unresolved.'}

if __name__ == '__main__':
    result = build(json.loads((P/'inputs.json').read_text()))
    (P/'outputs.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
