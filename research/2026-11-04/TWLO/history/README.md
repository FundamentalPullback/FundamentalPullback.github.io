# TWLO historical reconstruction, as of 2026-11-04

Run `python recompute.py`. Inputs are compact primary-source numerical observations in `source_numeric_extracts.json`; outputs are history.json, history.csv and qa.json. No full SEC filings are included. Amounts are USD thousands except EPS and percentages. Cash capex/software are shown as positive uses.

Coverage: FY23–25, Q4 2025 through Q3 2026 with same-quarter prior-year comparatives, and TTM through Q3 2026 versus Q3 2025. TTM uses FY + current 9M - prior 9M and is cross-checked to four quarters. Direct quarterly diluted EPS retained; TTM EPS is explicitly a sum of quarterly EPS, not a company-reported measure or reconstructed quotient.

Main issue: GAAP NI/EPS include a substantial noncash deferred-tax valuation allowance release. Do not use this as recurring operating earnings. CFO removes the release. Operating prepaid impairment remains a business risk rather than a free normalization. See accounting_perimeter_notes.json for capitalization, D&A, acquired amortization, SBC, commission and scope caveats.

Missing information remains missing: separate commission cash additions and an accessible primary excerpt confirming the historical Zipwhip software sunset. No invented organic bridge, valuation, next-result date, or publication.
