# SYY: historical financial audit through September 26, 2026

All money amounts are USD millions; shares are actual shares, not millions. FY24, FY25, FY26 and both trailing periods are 52 weeks. FY27 guidance is a separate 53-week period. These files contain history, not valuation.

## Findings
- TTM sales 85,149 versus 82,034 (+3.8%); EBIT 3,012 versus 3,080 (-2.2%); net income 1,807 versus 1,814 (-0.4%). Revenue growth has not translated into operating-profit growth.
- TTM CFO 2,830 versus 2,543; gross cash PP&E capex 637 versus 944. CFO minus gross capex is 2,193 versus 1,599. After expensing SBC analytically, 2,078 versus 1,505.
- Sysco's company FCF definition additionally includes PP&E sale proceeds: TTM 201 versus 161. Company FCF is therefore 2,394 versus 1,760. Do not confuse asset-sale-enhanced FCF with CFO minus gross capex.
- Core working-capital cash drag eased from 325 to 35 (AR, inventories, prepaids, AP and accruals only); cash taxes declined from 645 to 485; gross capex declined 307. The improvement should not automatically be extrapolated as recurring operating earnings.
- TTM D&A excluding financing-cost amortization is 1,005; acquisition intangible amortization is 168. The latter is a subset, not an additional cash cost. Do not add acquisition amortization again when full D&A has already been added back.
- Q1FY27 includes a 234 deal-contingent rate-lock gain in other income, below EBIT. GAAP EBIT remains 717. Bridge financing amortization of 90 is in interest, not operating profit. Cash-flow D&A excludes debt financing amortization.

## Shares and balance-sheet cutoffs
September 26 cash is 3,171 and book debt including finance leases is 13,820; operating leases are separately 170 current plus 1,349 noncurrent. September cash includes acquisition prefunding. Do not treat this snapshot as November pro forma cash/debt or deduct all of it against debt without a transaction bridge.

The September 16 equity financing issued 12,345,679 shares for gross proceeds of 1,000 and net proceeds of 967. Actual September 26 outstanding shares are 777,520,579 issued minus 285,593,166 treasury = 491,927,413. The October 16 cover-page count is 492,270,756. Q1FY27 diluted weighted-average shares are 482,945,241 and underweight the late-quarter issuance; this is not the forward valuation denominator.

## Reproduction and coverage
Run `python rebuild_history.py` and `python check_history.py` in this directory. Both use only standard Python and local observations.json; neither needs full filings, a browser, proprietary extractors, external packages or network access. Every calculated metric retains observation IDs, source URLs, period, unit and derivation method. source_urls.json identifies the primary SEC documents.

Quarterly cash flows are explicitly derived from YTD differences where not separately reported. Q4 cash flows are annual less nine months. Q4 income and weighted shares are directly reported in the August 4 earnings release (480,232,028 diluted shares). Independently rounded quarterly income may differ from YTD by 1; retain that rounding, rather than inventing a balancing adjustment. No weighted-share or EPS subtraction is permitted. Missing fields remain null, never zero.

Dimensioned pension contribution and expense observations are retained with their plan context; those amounts must not be summed indiscriminately because plan subsets can overlap. Quarterly pension cash contributions are not assumed to be zero. Cash taxes and the core working-capital bridge are explicit and separately labeled.

## Distribution
Only the files named in public_whitelist.json are intended for publication. The sources directory, full filings, text extracts and extraction tooling are excluded. observations.json contains selected numerical observations and short source locators, not reproduced filing text.
