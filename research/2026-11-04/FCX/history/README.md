# FCX financial history, as of 4 November 2026

Run `python rebuild_history.py` from any directory. Python standard library only; no network or package installation. Copy `numeric_inputs.json` and `rebuild_history.py` into a clean directory to regenerate history JSON/CSV, cell-level ledger JSON/CSV, QA and checksums. These inputs contain selected numeric facts and source references, not whole filings or an entire SEC companyfacts payload.

All dollar values are USD millions, except diluted EPS (USD/share); margins are percentages. Latest four quarters are Q4 2025 through Q3 2026. FY2019–FY2025 extends the cycle, with FY2022 EPS left blank rather than inferred. Two TTM periods end 30 September 2025 and 2026. The full three-year FY2023–2025 core and all latest four quarters have EPS directly reported in SEC filings/releases; Q4 EPS is never annual EPS minus nine-month EPS.

The October 27 2026 earnings release supplies the latest quarter. The latest 10-Q actually retrieved was June 2026, filed August 6. Do not label October release numbers a filed September 10-Q.

`ledger.json` provides every direct input or derived intermediate with units, source URL, XBRL accession/tag or table locator, and dependencies for calculations. `ledger.csv` is the flattened readable equivalent. `history.csv` and `history.json` are outputs. Consult comparability.md before interpretation.

## Crucial CFO exception
The original September 2025 10-Q reports nine-month CFO 4,917. The January 2026 Q4 release reports Q4 CFO 693 and FY2025 CFO 5,610, which reconcile. The October 2026 release instead reports comparative nine-month 2025 CFO 4,942, including Q3 CFO 1,689 rather than the original residual1,664. The reason for this 25 difference has not been established.

Our latest-comparative TTM calculation is 5,610+5,524−4,942 = 6,192. The Q4 2025 table CFO of668 is explicitly a residual using the latest comparative, not a directly reported quarter. The direct-quarter alternative is693+5,524 =6,217. Corresponding consolidated CFO-minus-capex values are1,951 and1,976. Preserve both, and do not claim a verified restatement or reclassification. `Q4_2025.cfo_release_direct` and `YTD3_2025.cfo_original` remain in the input and ledger.

Separate software capex is not available in these excerpts; null is not zero. Reported capex includes productive assets and mine-development spending, not purchases of additional ownership interests. No owner-earnings claim, valuation, publication or forecast is made here.
