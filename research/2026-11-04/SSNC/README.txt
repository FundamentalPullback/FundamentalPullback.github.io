SSNC independent research, 4 November 2026.
Price reference: regular November 3 close, USD80.88. Not a live quote.
STATUS: Independent research audit passed. Released for research publication only. No approved entry, order, size or stop.

All public files are own analysis, minimal numerical inputs, formulas and primary-source links.
Full third-party filings/PDFs in sources/ are private working files and MUST NOT be published.

Reproduction (Python3 standard library):
 python history/calculate.py
 python history/validate.py
 python model.py
 python valuation_checks.py
 python comps.py
 python qa.py

report.md: full Spanish research, caveats and sources.
summary.json: routing and valuation metadata; readyForPublication is true following independent audit.
pros_cons.json: bilingual concise evidence, each quote contiguous in report.md.
model_results.json + ten_year_model.csv: three full 10-year scenarios and sensitivity.
valuation_checks.json: capital-cost calibration, prior-model bridge, reverse scenarios, robustness.
peers.json/csv: comparable figures and conventions, including distinct period dates.
history/inputs.json and calculate.py: minimal factual inputs and reproducible 3FY/4Q/TTM history.
qa.json: numerical and evidence checks.

Known limitations: financing proposed, not closed; conversion/coupon/capped-call terms unknown.
Q3 acquired/software amortization split unknown. Quarterly dilution is not mechanically additive;
Q4 2025 EPS0.77/shares251.5 are directly sourced from issuer quarterly financials.
No subsequent earnings date confirmed. Refresh financing announcements before publication.
