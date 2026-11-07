EPAM fundamental research | 7 November 2026

Read report.md first. The conclusion is watchlist; Stage 3 is not complete and no entry is approved. Conditional research values are not approved targets. The planned ASR remains unexecuted in the main model.

Contents:
report.md — authored report with English/Spanish summary, primary evidence and limitations.
derived_inputs_and_model.json — historical financial inputs, source mapping, forecast assumptions, conditional cases, inverse grid and capital bridge.
annual_forecast.csv — all annual and terminal forecast rows.
build_research.py — deterministic numerical regeneration from embedded, primary-source-labeled financial inputs; Python standard library only.
qa_research.py and qa.json — reproducible numerical, disclosure and release checks.
source_ledger.json — public source URLs, titles, dates and purposes only.
primary_financial_evidence.json — selected source numerical rows, not complete filings.
contiguous_evidence.json — short literal primary excerpts and provenance.
summary_evidence.json — exact bilingual analytical summaries and their primary/derived provenance; not issuer quotations.
collect_evidence.py — optional live retrieval of selected financial rows; requires lxml and network access. It stores selected evidence only, not full filings.
public-whitelist.json — exact set of files included in the public package.

Offline numerical reproduction:
1. Run python build_research.py
2. Run python qa_research.py

This regenerates numerical JSON, annual forecast CSV, source ledger and QA. It does not generate or rewrite the authored report, primary excerpts, source-row evidence or bilingual summary evidence. Those static deliverables were editorially checked against the calculations. Live source retrieval is optional and separate; dynamic sources may change after the stated cutoff.

EPS convention: 7.97 is a FY + current-nine-month minus prior-nine-month proxy across different weighted-share periods. The actual sum of the four listed quarterly EPS values is 8.00. Neither determines the FCFF valuation denominator.

Timing: ten full forward annual cash flows at year-end; no date stub. Terminal value at year 10 uses funded year-11 cash flow. All reported cash/shares/price dates and gaps are disclosed. Same-date and homogeneous historical peer multiples remain unverified.

Only the whitelist files belong in this package. No private originals, internal workflow notes, full filings, or internal library review material are included.
