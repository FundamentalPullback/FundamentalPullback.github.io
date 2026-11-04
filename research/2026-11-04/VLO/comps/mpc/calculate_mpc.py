"""Reproducible MPC screening comp. Dollars and shares in millions except price.
Sources and limitations are in inputs.json and notes.md. No normalization implied.
"""
import json
from pathlib import Path
p=Path(__file__).parent
x=json.loads((p/'inputs.json').read_text())['values']
ebit=x['fy2025_operating_income']+x['nine_months_2026_operating_income']-x['nine_months_2025_operating_income']
mc=x['mpc_price_2026_11_03']*x['mpc_shares_2026_10_29']/1e6
nci=x['mplx_public_units_2026_09_30_rounded_m']*x['mplx_price_2026_11_03']
net=x['debt_carrying']-x['cash']-x['short_term_investments']
r={'ttm_ebit_gaap_m':ebit,'mpc_market_cap_m':mc,'net_debt_carrying_m':net,'net_debt_principal_m':x['debt_principal_and_finance_leases']-x['cash']-x['short_term_investments'],'mplx_public_nci_market_m_approx':nci,'ev_ex_other_nci_m_approx':mc+net+nci,'ev_ebit_ex_other_nci_approx':(mc+net+nci)/ebit,'ev_including_mplx_subsidiary_nci_book_proxy_m_approx':mc+net+nci+x['mplx_subsidiary_nci_book'],'ev_ebit_including_mplx_subsidiary_nci_book_proxy_approx':(mc+net+nci+x['mplx_subsidiary_nci_book'])/ebit,'invalid_ev_ebit_omitting_nci':(mc+net)/ebit}
(p/'outputs.json').write_text(json.dumps(r,indent=2)+'\n')
print(json.dumps(r,indent=2))
