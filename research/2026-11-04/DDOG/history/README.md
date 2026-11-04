# Datadog normalized financial history, November 4, 2026

## Use
Run `python reproduce.py` offline using only the Python standard library and bundled `source_subset.json`. It recreates `normalized_history.json`, `normalized_history.csv`, and `validation_checks.json`. The JSON numeric values are USD thousands except EPS (USD per share) and percentage fields. All expense/cash investment fields are positive amounts; GAAP EBIT and net income preserve signed profit/loss. Full downloaded source files are segregated in `full_filings/`; the portable subset does not require them. `build_inputs.py` documents initial transcription and annual SEC-fact selection but is not required for portable reproduction.

Scope: FY2023, FY2024, FY2025; direct-reported Q4 2025, Q1/Q2/Q3 2026; latest TTM through September 30, 2026 and prior comparable TTM. Q4 2024 and comparative 9M2025 are provided as the prior-TTM bridge. No forecasts or future-quarter actuals are used.

## Source posture
All releases are issuer primary sources, preserved as PDFs and extracted text. Annual core income/cash-flow items are independently tied to exact annual observations from the FY2025 10-K accession 0001628280-26-008819, filed February 18, 2026, via SEC companyfacts. Selecting that accession avoids lower-precision proxy-statement NetIncomeLoss values in later filings. Use `DepreciationAndAmortization`, not the narrower `DepreciationDepletionAndAmortization` tag: the latter excludes acquired-intangible amortization.

Q3 2026 release was published November 4, 2026 at 7:00 a.m. EST. It is an actual released result, not an upcoming earnings event. Its statement columns include quarter and nine-month periods ended September 30. SEC submissions and companyfacts downloaded at approximately 19:05 UTC did not identify a Q3 2026 10-Q; the latest 10-Q was for June 30, 2026, filed August 6. Do not interpret this as proving no later filing on November 4. No Q3 footnote-only data is invented.

## Definitions and interpretation
- GAAP EBIT means reported operating income (loss), not non-GAAP operating income or earnings before tax.
- D&A is the total cash-flow statement adjustment, including acquired-intangible amortization. SBC is expensed SBC net of capitalized amounts, matching CFO reconciliation.
- Issuer FCF = CFO minus cash purchases of PPE minus cash capitalized software development costs. CFO minus PPE alone overstates issuer-defined FCF and is shown separately only for transparency.
- FCF less expensed SBC is an analytical dilution-cost sensitivity, not GAAP, issuer FCF, owner earnings, or actual cash paid. Capitalized SBC is not included in that deduction. Annual capitalized SBC is separately provided from 10-K facts; Q3/TTM capitalized SBC is unknown pending the relevant filing evidence.
- Cash acquisitions are separately disclosed and not silently netted against issuer FCF. Equity-related employer payroll taxes and M&A transaction costs are expenses included in GAAP income/CFO; they are not proven period cash outlays and must not be subtracted again from CFO. Annual income taxes paid are also already reflected in CFO.
- M&A expense adjustments began April 1, 2025. Earlier undisclosed amounts are null, not assumed zero. Prior-TTM M&A expense therefore remains null.
- Direct quarter diluted EPS is reported at $0.13 / $0.15 / $0.12 / $0.32. Do not derive it by subtracting YTD EPS. TTM EPS is null because adding quarter EPS does not create properly weighted full-year diluted EPS. Quarter EPS remains usable as reported.

## QA and comparability
TTM additive metrics use directly reported Q4 2025 plus latest reported 9M2026; prior TTM uses Q4 2024 plus comparative 9M2025. They do not use an invented Q4 2026.

52 logged checks compare issuer FCF bridges, selected annual items against the 10-K, and direct quarterly sums against the latest 9M2026. Five immaterial source inconsistencies are preserved: direct three-quarter sums are $1k lower for CFO, SBC, and FCF; $2k lower for employer payroll-tax expense; and $1k higher for M&A transaction expense. They are source presentation/rounding differences of unknown precise origin, not corrections authorized by evidence. The latest cumulative values govern TTM; direct quarter disclosures remain unchanged. All FCF bridges and annual 10-K comparisons pass.

Missing quarter/TTM cash taxes and capitalized SBC remain null. Latest quarter financial statements are unaudited release evidence. This package supports financial-history analysis, not by itself a trade decision or valuation conclusion.
