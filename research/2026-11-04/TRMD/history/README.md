# TORM historical normalization (as of 4 November 2026)

USD million unless specified. Primary IFRS statements only. No valuation or normalized owner earnings are asserted.

Run `python build_history.py` to reproduce numerical inputs, CSV/JSON normalized periods, field lineage and QA from embedded portable inputs. Sources and selected excerpts remain portable; whole filings are excluded from deliverable. `balance_numeric_inputs.json` contains separately keyed balance-sheet/NAV inputs.

## Definitions and critical cautions

- Revenue is consolidated IFRS revenue; TCE is Tanker-segment revenue less port/bunker/commissions, including freight/bunker derivatives. These are different scopes, not alternative labels for the same revenue. FY23 TCE = tanker revenue 1,491.4 minus 407.6; FY24 =1,544.0 minus409.2.
- EBITDA = EBIT plus D&A. Neither is owner earnings. Vessel sale gains are separately identified; EBIT excluding those gains is only a mechanical bridge, not cycle-normalized EBIT.
- CFO includes cash interest and taxes. Cash tangible investment includes fleet purchases, prepayments and dry-docking; this is not a clean maintenance-versus-growth capex disclosure. Capitalized drydock balance 115.0m at Sep26 is a STOCK, not current cash maintenance spending.
- Issuer FCF reconciles CFO + signed CFI, including asset sales and changes in restricted cash. The prose definition says 'less' net investing cash, but the company's tabular arithmetic adds signed CFI. Follow the table. CFO less all cash capex excludes disposals/restricted releases but still mixes renewal and growth, so it is NOT owner FCF.
- FY25 headline investment in tangible fixed assets 321m differs from CASH capex 308.5m. Use the cash statement for cash bridges. A 17.0m non-cash vessel share issuance is separately disclosed; do not force the headline/cash difference to equal it.
- Borrowings carrying values already include ROU lease liabilities. Do not add ROU again. To recover gross obligations add capitalized borrowing costs to carrying borrowings. Sale/leaseback financial obligations are already represented in borrowings. Cash restricted is separated; do not assume it is freely distributable. NCI book equity is not fair value.
- Owner FCF is null for all periods because maintenance/replacement/growth capital and sustainable mid-cycle earnings are unresolved. Recent very high tanker rates should not be capitalized as perpetuity.

## Construction and QA

Q4 2025 = FY25 minus 9M25. Latest TTM = FY25 + 9M26 minus9M25. Q2/Q3 cash capex/proceeds rows are cumulative differences; reported single-quarter income/CFO used when available. Comparative Q1-Q3 2025 included. EPS is not mechanically summed. All comparisons retain reported one-decimal precision.

QA permits 0.21m for aggregation of rounded tables. Notably Q1 2026 D&A59.7 + Q2 60.5=120.2 while reported H1=120.1. Q1/Q2 2025 and cumulative results also have 0.1m differences. These are disclosed rounding differences, not overwritten inputs.

Source IDs in field_lineage.json reference sources.json. Derived cells reference their input period/metric or documented formulas. Sources are retrieved 4 November2026. No companyfacts or complete SEC filing is needed to rebuild.

Prior TTM Sep25 is now included as FY24+9M25−9M24 from Q3 2025 primary filing. Reported EPS added; discrete Q4/TTM EPS left null rather than summing EPS across changing denominators. SBC EXPENSE: FY23 23.0m, FY24 30.3m, FY25 34.1m from staff note. Changes-in-equity SBC differs (22.5/30.2/34.1m); interim values are labeled equity movement, not misrepresented as expense. Interim SBC expense remains null.
