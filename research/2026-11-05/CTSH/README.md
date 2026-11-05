# CTSH research package — November5,2026

Start with report.html or report.md. All monetary model data are USD millions except per-share values.

Status: conditional reasonable-price fundamental approval up toUSD66.50. No executable entry, order, quantity or account/cash verification. Prospective technical draft is routeA only, maximumUSD65.25, expiresNov10.

Reproduction: Python3 with numpy, scipy and pandas; pandoc forHTML. Run `python reproduce_all.py` for9steps. Outputs include results.json, forecast_rows.csv, sensitivity.json, technical.json, QA.json and report.html. The model is deterministic support for the web report, not a formulaXLSX or an Excel-native tested workbook.

Independent audit: run `python independent_audit/audit.py .` and `python independent_audit/technical_audit.py .`. These do not import value.py.

Source posture: normalized numerical history, selected source metadata, primary URLs and raw-source hashes are included. Full third-party filings/transcripts/HTML and prior-author research copies are not redistributed. Reproduction recalculates selected source data, not a fresh retrieval or full filing extraction. Fresh-source availability/changes are outside the offline replay. Original source snapshots were inspected and retained during research.

Capital bridge mixes Septemberreported cash/debt, Octoberactual shares and explicit estimates forQ4cash, postSeptemberbuybacks, currentawarddilution and lastDecemberpensiondeficit. It is not a certified currentbalance. See report for all sensitivities.

This package does not publish itself or place trades.
