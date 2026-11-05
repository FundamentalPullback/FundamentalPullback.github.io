# HRI financial-history reconstruction

As of November 4, 2026. All money figures are USD millions, except per-share data.

## Deliverables and offline replay

- `observations.json`: 230 selected reported observations. Each inline-XBRL observation retains original QName, context reference and plain context, date boundaries, reported text, scale/sign, source URL, and source HTML SHA-256. This file contains selected numeric facts, not full filing text. One manually selected Q4 diluted EPS observation is separately identified and cites the SEC earnings exhibit.
- `build_history.py`: standard-library-only offline calculation. Run `python build_history.py` in this directory. It needs only `observations.json`, not web access or full filings. Produces `history.json` and `QA.json`.
- `history.json`: FY2023–FY2025, Q4 2025–Q3 2026, and TTM through September 30, 2025 and 2026. Every field is marked direct or derived with source observation IDs. TTM GAAP EPS is explicitly not reported.
- `history.csv`: convenient flat numeric view. For lineage and definitions, use JSON.
- `QA.json`: 51 passing controls, including selected independent statement totals and all additive four-quarter/TTM reconciliations.

## Definitions

Operating EBIT = income before tax − signed nonoperating interest − signed other nonoperating income/expense. XBRL interest is negative for expense; Other is positive for income. This deliberately excludes both interest and Other, while retaining transaction expenses and gains/losses on assets held for sale. Herc does not report an operating-income subtotal in these statements. The derived measure should not be confused with management adjusted EBITDA or net income plus tax and interest without removing Other.

Capex is positive cash outflow, not accrual-basis purchases. Rental disposal proceeds are investing cash receipts, not reported sales of rental equipment. Net rental capex = gross rental capex − rental disposal proceeds. FCF after net capex includes disposal proceeds for both rental and nonrental assets and excludes acquisitions, business-disposal cash, and other investing activities. Consequently FY2023 net-capex FCF is -$50m, while a management FCF definition including the separate $15m other investing outflow would yield -$65m. No maintenance/growth split is inferred. Debt-financed fleet acquisition is not reclassified as capex.

Q4 financial flows are FY2025 minus 9M2025. Q2/Q3 cash-flow figures use consecutive cumulative YTD differences. Income-statement quarters Q1–Q3 2026 are direct reported quarters; Q4 diluted EPS is direct from the SEC earnings release. Current TTM additive flows are Q4 2025 + 9M2026. Prior TTM is FY2024 − 9M2024 + 9M2025, using the prior Q3 filing for 9M2024. All fifteen overlapping 9M2025 observations agree between the 2025 and 2026 Q3 filings. Original statement rounding applies.

EPS is nonadditive when weighted shares change or loss-period dilution differs. Do not derive Q4 EPS from annual minus nine-month EPS. The sum of four reported quarters is $3.67 and is explicitly labelled `eps_diluted_sum_of_quarters`, not a reported GAAP TTM EPS or recomputation using a valid TTM diluted denominator.

## Acquisition and comparability

H&E results were consolidated beginning June 2, 2025. The prior TTM through September 2025 includes only about four months of H&E, and FY2025 includes approximately seven months; the current TTM (October 1, 2025–September 30, 2026) includes twelve months. FY growth is not organic. No pro forma acquisition revenue is substituted for GAAP history. FY2024 includes a $194m held-for-sale loss, FY2025 $48m, and these remain in the reported-cost EBIT series. Rental depreciation and other D&A are preserved separately. Cash transaction expenses can differ from income-statement transaction expenses, so this file does not treat the latter as a cash-flow addback.

## Primary sources

- FY2025 Form 10-K, filed February 17, 2026: https://www.sec.gov/Archives/edgar/data/1364479/000136447926000050/hri-20251231.htm . Consolidated statements of operations and cash flows include FY2023–FY2025.
- Q3 2025 Form 10-Q, providing the 9M2024 comparison: https://www.sec.gov/Archives/edgar/data/1364479/000136447925000056/hri-20250930.htm
- Q1 2026 Form 10-Q: https://www.sec.gov/Archives/edgar/data/1364479/000136447926000085/hri-20260331.htm
- Q2 2026 Form 10-Q: https://www.sec.gov/Archives/edgar/data/1364479/000136447926000109/hri-20260630.htm
- Q3 2026 Form 10-Q: https://www.sec.gov/Archives/edgar/data/1364479/000162828026067396/hri-20260930.htm
- Q4 2025 earnings release, 8-K Exhibit 99.1, February 17, 2026: https://www.sec.gov/Archives/edgar/data/1364479/000136447926000049/herc2025q4-pressrelease.htm . Fourth Quarter 2025 Highlights and condensed consolidated statements of operations support diluted EPS $0.72.

Full filings are deliberately excluded from this history deliverable. Source HTML can be retained outside this directory for extraction audit, but do not package the `../sources` directory with the selected history.

## Portable file manifest

`PUBLIC_FILES.txt` lists the complete portable deliverable. Extraction code and complete filings are intentionally omitted. The included build uses only the selected observations and Python standard library.
