"""Incremental source arithmetic only. Not FCFF, actual November balances, or valuation."""
import json
from pathlib import Path
p=Path(__file__).resolve().parent
x=json.loads((p/'calculations.json').read_text())
# Official September 10-Q Note 15: $125m cash consideration and $45m revolver borrowing.
consideration=125.0; revolver=45.0; september_cash=240.902
principal=x['principal_debt_sept30']; implied_cash_use=consideration-revolver
illustrative_debt=principal+revolver; illustrative_cash=september_cash-implied_cash_use
scanner_price=21.13; scanner_high=25.15; export_pullback=14.2; offering_price=21.80
out={'units':'USD millions except per-share prices and percentages','consideration':consideration,'revolver_borrowing':revolver,'implied_existing_cash_use':implied_cash_use,'illustrative_debt':illustrative_debt,'illustrative_cash':illustrative_cash,'illustrative_net_debt':illustrative_debt-illustrative_cash,'selling_holder_gross_proceeds_before_expenses':15*offering_price,'issuer_proceeds':0,'new_shares_issued_in_secondary':0,'scanner_vs_offering_price_pct':(scanner_price/offering_price-1)*100,'mechanical_scanner_pullback_pct':(1-scanner_price/scanner_high)*100,'difference_vs_export_percentage_points':(1-scanner_price/scanner_high)*100-export_pullback,'limits':'Balances isolate acquisition movements against September only; not actual November balances. No fees, acquired balances, adjustments or intervening cash flows assumed. Secondary sale and separate LP distribution do not add issuer proceeds or new shares. Closing remains prospective. Prices are not synchronized closes.'}
assert abs(out['illustrative_net_debt']-1903.635)<1e-9
(p/'incremental_calculations.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
