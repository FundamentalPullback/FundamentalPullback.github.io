# ASML US GAAP history, cutoff 4 November 2026

All money is EUR millions, except EPS (EUR/share). Financials are consolidated US GAAP. Annual 2023/2024/2025 values are from the audited 2025 20-F. Quarterly values are reported unaudited figures from ASML's Q3 2025 and Q3 2026 IR spreadsheets. The latter were cross-checked against the official Q3 2026 PDF (printed pages 2, 5, 6 and 9). No valuation or publication is performed.

## Reproduction and files

Run `python build_history.py` from any directory. It uses Python standard library and lxml, reads preserved local sources, and regenerates extracts without internet. `extracts/core_history.csv` and JSON contain annual, quarterly and TTM series. `quarterly_rows.json` preserves selected numeric rows with workbook, sheet, cell, actual reporting date and metric; `annual_rows.json` preserves statement/table attribution. `qa.json` reports tie-outs. Original documents, OCR and source renderings are under `sources/`; do NOT expose that whole folder publicly. The extracts contain numerical facts, not full issuer prose.

TTM labels ending 09-30 are calendar labels: actual quarter ends are 27 September 2026 and 28 September 2025. TTM sums Q4 prior year + Q1/Q2/Q3 current year. EPS basic and diluted for TTM are sums of reported quarterly EPS, not issuer-reported annual EPS or EPS recomputed using a fresh full-year weighted denominator. FY EPS is reported annual EPS. Dates in quarterly rows preserve issuer fiscal dates. Never compare a TTM with 9M as if both covered 12 months.

Capex is the positive sum of purchases of PPE and intangible assets, not all investing cash flows. FCF = CFO minus that capex. SBC is not subtracted again in FCF and remains an economic dilution/cost consideration. No unsupported numerical normalization is applied. Blank/null means not separately reported in the selected line, NOT zero.

## Quality checks

Q1+Q2+Q3 2026 tie exactly to the Q3 PDF 9M controls: sales 29,755.4, NI 10,634.7, CFO 11,315.0. Prior-year controls: 22,949.2 / 6,769.8 / 1,248.2. FY2025 less sum of four quarters is zero for revenue, NI, CFO, capex and SBC; EBIT and D&A differences are -0.1 each from published rounding. Keep audited FY values rather than replacing them with rounded-quarter sums.

## Q3 2026 gain and tax

The rise from Q2 NI 2,917.6 to Q3 NI 4,960.4 includes a separately reported equity-investment gain of 509.7 BEFORE tax. EBIT is 5,172.8 and excludes that gain. Interest/other is 68.2. Pretax income is 5,750.7, tax expense 925.0 (effective rate about 16.1%), and equity-method profit 134.7. The cash-flow statement reverses equity-investment gain by 508.8. The difference from 509.7 must not be silently discarded or invented as a tax item.

The gain's identity is not established by these financial-statement tables alone; use the separately verified official management commentary for Mistral identification. No numerical tax benefit specific to the gain is disclosed in the captured statements. Do not assume the gain is tax-free or subtract the full pretax amount from net income as though it were after tax. Q3 effective tax is lower than Q2's 17.5%, but that alone does not prove a discrete tax windfall.

NI bridge Q2 to Q3: EBIT +1,716.7; equity gain +509.7; interest/other +38.2; tax expense increase -315.4; equity-method profit +93.6 = NI +2,042.8. Most of the NI increase is operating, though the equity gain is material.

## Cash flow and customer advances

Q3 CFO 11,797.6 contains +7,009.0 of changes in assets and liabilities; CFO before this aggregate movement is 4,788.6. Q3 FCF 11,350.4 should not be annualized. TTM CFO 22,725.3 contains +7,876.9 of aggregate changes in assets/liabilities; FCF before those movements is 13,122.5. This aggregate includes tax and other items, not just customer advances, so it is not a pure working-capital or advance-normalized cash flow.

Nine-month 2026 aggregate change is only +236.2 because Q1 and Q2 had large cash absorption. The TTM contains the strong Q4 2025 inflow (+7,640.7) AND Q3 2026 inflow (+7,009.0), offset by Q1/Q2. TTM FCF rose from 8,926.7 to 20,999.4, but the difference in aggregate asset/liability movements explains 8,254.1 of that 12,072.7 increase.

Noncurrent contract liabilities rise from 3,366.3 at FY2025 to 9,300.6 at Q3 2026. Q3 statements aggregate ALL current liabilities at 24,904.3, so current contract liabilities and current debt cannot be isolated from this report. Do not equate noncurrent contract-liability change with all cash advances, and do not assume current debt is zero. FY2025 audited current contract liabilities were 16,006.3; noncurrent 3,366.3, total 19,372.6. FY2024 comparable 12,570.8 + 5,625.4 = 18,196.2. FY2025 current debt was 1,681.9; noncurrent 2,709.0.

## Primary sources

- 2025 20-F: https://www.sec.gov/Archives/edgar/data/937966/000162828026011378/asml-20251231.htm (HTML zero-based tables 1335 operations, 1351 cash flow, 1342 liabilities)
- Q3 2026 official PDF: https://investor.asml.com/static-files/d310262b-d037-485d-83b5-92c93cc462f0
- Q3 2026 workbook: https://investor.asml.com/static-files/78b1af6f-9c6e-4e5c-b229-a418251687ff
- Q3 2025 workbook: https://investor.asml.com/static-files/8eb7be33-3fef-490d-a21c-f02161a47268
- SEC Q3 2026 financial statements: https://www.sec.gov/Archives/edgar/data/937966/000162828026065813/financial_statementsxusx.htm (image-based)
- Source link listing: https://investor.asml.com/quarterly-results

Other quarterly filing wrappers and some JPG pages are retained as secondary originals. Their OCR is not the computational source of this package. Primary workbook sources are unmodified; formulas, if present, are read from published cached values, not recalculated or overwritten.
