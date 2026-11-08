# Model input lineage and judgment ledger

All amounts are USD millions. Current share and price inputs are post June 2026 10-for-1 split.

## Reported base
- Revenue 14,505.795, EBIT 6,185.273, CFO 4,512.427, capex 474.807, SBC 324.062 and R&D 1,566.753: companyfacts matched to FY2026 annual and Q1 FY2027/prior-year 10-Q statements. historical_source_facts.json retains exact SEC accession evidence. EBIT is derived, not pretax earnings.
- Current common shares 1,302.962435 million on October 26: Q1 cover. Incremental diluted-share proxy 5.734 is Q1 diluted weighted average minus basic weighted average. Existing RSUs and future SBC may partly overlap; no certification of a precise current claim.
- Price 138.49: November 6 regular session close. After-hours 139.42 and historical scanner 195.57 are not interchangeable.
- September cash and marketable securities 4,741.191, debt face 5,950, book debt 5,723.289, bond fair value 5,080 and interest swap liability 165.644: Q1 notes 3 and 7. Main bridge uses bond market value plus swaps; face plus swap alternative retained. November debt mark not verified.
- EDSP assets 411.061 minus liability 413.197; net ordinary hedges 11.550 minus 25.198; pension noncurrent 43.733; noncurrent income-tax payable 299.437: Q1 notes. June restructuring 5.3 is latest separately disclosed proxy. Current tax payable 142.281 and annual uncertain tax reserve 257.767 are not blindly stacked on top of selected noncurrent tax obligation.
- Operating leases 269.355 liabilities: rents stay in EBITA; do not also subtract full operating lease debt. Minor finance-lease balances and current pension components are not fully separated.
- Cash LTI commitment 100 requires future employment and is included in operating compensation, not unconditional debt. Contingency reserves are assumptions, not established loss bounds.

## Physical and operating capital
- Opening depreciable gross assets 3,079.788 equals gross PPE 3,282.320 less land 202.532. Annual physical depreciation 214.5 supports starting 7% rate. Maintenance is at least 110% of modeled depreciation and 1.7–2.2% of sales. Growth capacity costs 16–25% of incremental revenue. These are analyst calibration assumptions.
- Opening selected net working capital is fully enumerated in model.py: current/long receivables, inventory, contract assets, deferred costs and prepayments, less suppliers, contract liabilities, customer deposits and compensation. Other mixed accruals excluded pending clean split. Target ratios 30–40% are assumptions.
- Purchase commitments 8,870, versus 5,970 in June, are not deducted as debt and also funded through capex/cost/working capital. Cancellations may create incremental losses; scenario reserves 300/150/50 are selected stress amounts, not quantified maximums.
- Factoring/LC flows are not outstanding debt. Additional funding normalization 150/75/25 over three years is an assumption, charged only once.
- ROIC constraint refers to net operating capital after expensed R&D. Any extra required investment goes into capacity capex and raises subsequent replacement needs. No additional intangible charge or R&D capitalization is included. A physical-budget-only variant isolates the assumption's impact.
- R&D remains expensed. Tax-capitalized R&D deferred-tax balance is not an operating asset added to enterprise value. SBC is retained as operating cost; capitalized inventory SBC is not added back as free cash.
- EBITA avoids indefinite acquired-amortization expense, but does not separately capitalize an indefinite amortization tax shield. Acquired businesses remain in sales and cost base.

## Capital cost, growth and taxes
- Treasury November 6 10-year 4.86%, Damodaran November ERP 4.41%, market-statistics observed beta 1.50. Ke 11.475%.
- FRED Single-A effective yield 5.54% on November 5 is a rating-class financing proxy, not issuer-specific marginal quote. WACC mechanical 11.2745%; central 11.25%, scenario 10–12.5%.
- Taxes, growth, margins, working-capital ratios and net operating ROIC are scenario judgments in model.py. No probability weights or approved aggregate valuation.
- Mature margin, tax and ROIC are reached in year10. The terminal value carries physical stock/renewal dynamics forward under constant mature policies; it is not a year11 FCFF Gordon shortcut. The 300-year numerical tail converges against400 years, with a tiny residual.
- Distribution treatment is cum-dividend: November 5 declaration of $0.23 payable December 1, record November 16. Cash and distribution entitlement are not double-subtracted.
- BIS public inspection final rule filed November 5 supersedes stale annual-report Affiliates Rule expiry language; effective November 9, suspension through January 10, 2027. This is not removal of all China controls.
