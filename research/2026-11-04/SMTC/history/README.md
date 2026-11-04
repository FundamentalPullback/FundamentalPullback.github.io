# Semtech financial history through Q2 FY2027

USD millions except EPS (USD/share), share counts (millions), and percentages. Sources retrieved November 4, 2026. This is reported historical financial data, not a valuation or recommendation.

## Files and reproduction

Run `python reproduce.py` in this directory. Python standard library only; no network, credentials, packages, or raw filing dependency. The script reads the numeric source ledger and writes the long and wide CSVs, JSON history, missing fields, and logged validation checks. `source_index.json` records original SEC URLs, filing/retrieval dates and SHA-256 hashes. Every normalized long-form row links to ledger IDs, which identify the source, XBRL tag/context, original text, scale, sign and date. Raw filings remain outside this directory; this package contains numeric extracts only.

Coverage: FY24/FY25/FY26; latest four quarters Q3FY26–Q2FY27; corresponding prior-year quarters Q3FY25–Q2FY26; H1 and nine-month bridge periods; both TTM periods to Q2. Balance-sheet snapshots cover fiscal year and quarter ends. Four intentional missing fields are TTM weighted-average shares: they cannot be produced by subtracting annual and half-year share averages.

## Definitions and model loading

- Revenue, gross profit and EBIT are consolidated GAAP actuals. EBIT means reported operating income, not net income plus financing/tax adjustments.
- Net income is attributable to Semtech/common shareholders. Consolidated net income is retained separately; FY24 differs by $0.001m due to noncontrolling interests.
- Quarterly net income and EPS are direct, never cumulative subtraction. Q4FY26 NI −$29.8m and Q4FY25 +$39.1m are release-rounded figures; the corresponding diluted EPS −$0.32 and +$0.43 are directly reported. Q4 revenue/EBIT and cash-flow amounts are precise annual-minus-nine-month calculations. A small Q4 NI rounding tolerance is explicit in TTM checks.
- Additive TTM lines = annual FY + current H1 − prior H1. TTM EPS is an analytical sum of four directly reported quarterly EPS, NOT issuer-reported annual GAAP EPS, NOT cumulative EPS subtraction, and NOT a basis for inferring a TTM weighted share count.
- CFO, PP&E capex, intangible purchases, cash-flow SBC and D&A quarterization subtracts cumulative periods. Capex is a positive outflow. FCF = CFO minus PP&E capex; a second FCF measure also deducts intangible purchases.
- `sbc_cf` and `sbc_pnl` remain separate series and happen to reconcile in the periods covered. FCF less SBC is only a conservative sensitivity. Cash-settled award remeasurement means this is not a pure dilution measure or fully normalized owner earnings. Do not subtract cash settlements again without reconciling the CFO working-capital effects.
- `da_cf` is the depreciation/amortization cash-flow addback, excluding separately presented right-of-use amortization. `intangible_amortization_total` includes core technology, customer relationships, trade names, capitalized development and software licenses. `acquired_amortization` is core-technology amortization plus the reported acquired customer/trade-name operating amortization. Do not add either intangible metric to D&A again.
- Debt uses balance-sheet carrying values, not gross principal, market value or fully diluted conversion economics. Net debt = current debt + long-term debt − cash. Q1FY27 current debt is a documented zero residual because the only current-liability components are payables and accrued liabilities. All balances are point-in-time, even when attached to a TTM row.

## Material comparability and QA flags

1. **Cellular business remains in GAAP results.** Q2FY27 classifies $132.235m of assets and $70.693m of liabilities as held for sale. The filing explicitly says the disposal is not discontinued operations. Do not subtract its revenue/earnings from historical actuals. Inventory, receivables, PP&E and other asset components now exclude amounts classified separately as held for sale, creating a balance-sheet presentation break.
2. **Compal proceeds are prospective.** The August 13 agreement contemplated approximately $62m in cash, subject to adjustments and closing conditions. No sale proceeds are added to the July 26 balance sheet. A current closing-status check belongs outside this historical package.
3. **Tax distortion.** Q2FY27 net income $160.121m includes a $101.361m net income-tax benefit. The $112.4m valuation-allowance release is a specific gross noncash tax item, not the same as net quarterly tax benefit. Current TTM NI $154.027m and EPS sum $1.51 should not be treated as normalized earnings.
4. **Acquisition perimeter.** FY27 actuals include the completed HieFo acquisition from its acquisition date; no organic restatement is attempted. Purchase-price cash flows are not PP&E capex. Regulatory/current transaction conclusions are outside this data normalization.
5. **SBC quality.** P&L SBC is $23.846m Q2FY27 / $50.292m H1FY27 / $83.883m TTM. Management attributes much of the SG&A increase to cash-settled award remeasurement as the stock price rose. Keep this caveat beside any FCF less SBC sensitivity.
6. **Impairments and financing.** FY24's large GAAP losses and FY26 Q2/Q4 impairment-related losses are retained, not silently adjusted away. FY25 loss includes debt-extinguishment impacts; comparisons of GAAP NI require context.
7. **Rounding and audit posture.** 10-K annuals are audited; 10-Qs and earnings releases are unaudited. Q4 direct NI/share averages are rounded to $0.1m/million shares. Duplicate-source agreement, balance-sheet equality, SBC identity and TTM quarter sums are logged in `validation_checks.csv`. Passing arithmetic checks does not remove the economic comparability caveats above.

## Snapshot

Current/prior TTM: revenue $1,174.215m/$996.476m; EBIT $94.353m/$58.798m; CFO $214.020m/$135.290m; PP&E FCF $193.108m/$127.640m; FCF after intangible purchases $183.879m/$123.538m; SBC $83.883m/$59.796m. Current cash $204.051m and carrying-value debt $492.730m imply net debt $288.679m.
