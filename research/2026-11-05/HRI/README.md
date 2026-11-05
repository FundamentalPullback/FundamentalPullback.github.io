# HRI — economic FCFF research, 5 November 2026

Open `report.md` first (Spanish). This is an analytical valuation supplement to the audited factual packet at `hri_completion_20261104`, preserved unchanged. No site publication or entry approval was performed.

- `model.py`, `inputs.json`: deterministic, standard-library-only economic fleet model. Run `python model.py` from any directory.
- `results.json`: all three primary cases, five diagnostic alternatives and reverse cases. Scenario inputs explicitly differ; no probability-weighted target.
- `*_forecast.csv`: complete ten annual rows for each case/alternative.
- `sensitivity.csv`: WACC versus holding-life sensitivity.
- `source_ledger.json`, `sources/`: reported/guidance/analyst assumptions separated; original sources and peer snapshot.
- `history/`: copied factual three-year/four-quarter/TTM history and original QA; not revised by this model.
- `qa.py`, `QA.json`: 310 builder checks. Run after `model.py`. **Independent audit completed: 103 additional checks pass; read independent_audit/report.md. Builder qa.py remains preserved and its pending label is historical to the original author package.**
- `run_log.json`, `manifest.sha256`: build status and integrity.

Evidence status: screen-grade. Decision-useful conclusion: $158.10 is not supported by central cash conversion; it is supportable in the explicitly favorable case. The near-zero central residual is a financing gap, not a precise fair-price forecast. The report explains more favorable capex/tax/terminal alternatives, and no artificial margin-of-safety or investor return threshold is imposed.

Model convention: operating leases expensed; finance leases debt; paid-for prospective fleet investment; current unpaid fleet purchase balance deducted once; no debt principal repayments in FCFF; no free acquisitions or buybacks. Economic depreciation is an analytical capital-maintenance measure, not reported GAAP D&A or a full tax depreciation schedule.

Conditional research and review are completed. Stage3 outcome is observation, not approval or passage to Stage3.5. The reproducible code/inputs/results remain unchanged from the author package. This is not a banker-formula XLSX workbook and makes no such claim.
