#!/usr/bin/env python3
"""Independent accounting and reproducibility checks; run after calculate.py."""
import json,subprocess,sys
from pathlib import Path
P=Path(__file__).resolve().parent
before=(P/'history.json').read_bytes()
subprocess.run([sys.executable,str(P/'calculate.py')],check=True,capture_output=True)
assert before==(P/'history.json').read_bytes(),'Non-reproducible output'
x=json.loads(before);r={p['period']:p for p in x['periods']}
for p in r.values():
 assert p['cash_generated']==p['ebit']-p['jv_profit']+p['consolidated_da']+p['sbc']-p['working_capital_outflow'],p['period']
 assert p['cfo']==p['cash_generated']-p['interest_paid']+p['interest_received']-p['tax_paid'],p['period']
 assert p['owner_fcf']==p['cfo']-p['ppe_capex']-p['software_capex']-p['lease_principal']+p['sublease_receipts']+p['jv_dividends']-p['sbc']-p['nci_dividends']
 assert p['owner_fcf_after_acquisitions']==p['owner_fcf']-p['acquisition_cash']
 assert p['acquisition_cash']>0
 if p['diluted_eps_p'] is not None: assert abs(p['diluted_eps_ni_over_shares_p']-p['diluted_eps_p'])<0.06
for k in ['revenue','ebit','parent_net_income','cfo','owner_fcf','ordinary_da','acquisition_cash','prepublication_capitalized']:
 assert r['FY2025'][k]==r['H12025'][k]+r['H22025'][k]
 assert r['TTMJune2026'][k]==r['FY2025'][k]-r['H12025'][k]+r['H12026'][k]
assert r['TTMJune2026']['owner_fcf']==2256
assert r['TTMJune2026']['ordinary_da']==513
assert r['FY2023']['consolidated_da']==793 # Published 794 total includes £1m JV acquired amortization; cash-flow bridge excludes it.
assert r['FY2023']['prepublication_capitalized'] is None
assert len(r)==9 and not any(k.startswith('Q') for k in r)
print('PASS: deterministic reproduction, accounting reconciliations, half-year/TTM bridges, EPS and null checks.')
