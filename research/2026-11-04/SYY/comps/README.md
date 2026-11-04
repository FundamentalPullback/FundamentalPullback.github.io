# SYY peer context: USFD and PFGC

Research cut: November 4, 2026. Prices: November 3, 2026 close. All financial amounts are USD millions. This is a limited public-source comparison, not a SYY valuation target or a current synchronized trading screen.

## Results

- **USFD:** $101.36 price; July 31 actual shares 216.330723m; June 27 capital. TTM GAAP EBIT $1,262m, intangible amortization $57m, EBIT plus amortization $1,319m. Principal-debt EV $27,129.28m implies **21.50x GAAP EBIT / 20.57x EBIT plus amortization**. Capital is stale, not Nov3 actual net debt. Q3 results are scheduled November 5.
- **PFGC:** $96.51 price; September 30 actual shares 157.786138m; September 26 balance sheet. TTM GAAP EBIT $935.0m, intangible amortization $266.3m, EBIT plus amortization $1,201.3m. **Exact principal-debt EV and multiples are deliberately null.** A separately labeled carrying-debt EV proxy of $22,141.14m gives **23.68x / 18.43x**, respectively. This proxy is not an exact normalized EV.

The ranking reverses between GAAP EBIT and the amortization-only sensitivity. That illustrates why acquisition accounting matters; it does not establish which stock is cheaper on economic earnings. PFGC also has substantial Convenience and Specialty operations. These two companies do not support a mechanical peer median or a SYY price target.

## Reconciliation and boundary conditions

USFD GAAP EBIT = 1,199 FY2025 + 659 H1 2026 - 596 H1 2025 = 1,262. Intangible amortization = 56 + 28 - 27 = 57. Financial principal debt = 5,237 reported total debt - 591 finance leases + 21 deferred financing costs = 4,667. Add finance leases once: 5,258 total financial principal plus leases. Deduct unrestricted cash 56. Outstanding-check overdraft 168 is operating working capital, not an added financial borrowing.

USFD's October 2 8-K describes an $810m refinancing that repaid the 2028 term loan, partially prepaid the 2031 term loan and revolver, and funded fees. Do not add $810m to June debt. The filing does not provide a complete updated debt/cash balance, and later buybacks could change both shares and cash. Thus the June balance-sheet bridge remains explicitly dated and limited.

PFGC GAAP EBIT = 887.5 FY2026 + 272.2 Q1 FY2027 - 224.7 Q1 FY2026 = 935.0. Intangible amortization = 272.0 + 61.0 - 66.7 = 266.3. Release balance-sheet debt carrying value = 5,170.0; finance leases = 263.8 current + 1,515.3 noncurrent = 1,779.1; cash = 35.9. Restricted cash 10.7 is not deducted. The June note's debt principal 5,031.0 and carrying value 5,006.8 cannot establish September principal: the release shows net ABL borrowings 162.3 and other-debt payments 5.8, but no complete September debt/fee note. Do not silently carry June deferred fees 24.2 forward or imply a complete principal roll-forward.

PFGC released September-quarter results on November 4. November 3's close was **before that earnings release**. These calculations mix a pre-event price with subsequently published financials, explicitly as a retrospective snapshot, not as a valuation that could have been executed with that information on November 3.

All SBC remains expensed. No restructuring, LIFO, integration, business transformation, or other company EBITDA add-backs are made. Only separately disclosed intangible amortization is shown in a second denominator, without treating that accounting cost as economically irrelevant. Depreciation, including finance-lease depreciation, stays in earnings. Operating leases are not added to EV and lease expense stays in EBIT. No forward consensus metrics, peer medians, or valuation target are used.

## Reproduce

Run `python3 build_comps.py` from any directory. The script reads its neighboring `inputs.json` and writes `outputs.json`, using only the Python standard library and no network access. The input numbers, formulas, dates and qualifications are explicit. `sources.json` records exact source URLs and statement locations. Sources are issuer SEC/IR materials for fundamentals, with labeled secondary market-data sources and cross-checks for daily closes. No full filings are included in this deliverable.

## Required next refresh

1. Replace USFD earnings/capital/shares after the November 5 results and 10-Q; reconcile the October refinancing and intervening buybacks.
2. Read PFGC Q1 FY2027 10-Q debt note to replace the carrying proxy with principal debt. Check current cover shares.
3. Use a common post-results closing price date before presenting a synchronized live comparison.
