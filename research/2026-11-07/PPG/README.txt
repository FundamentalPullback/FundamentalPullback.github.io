PPG research, 7 November 2026. Conditional operating FCFF, not approved total fair value or an entry.
Read PPG_report.html or PPG_report.md first. The capital bridge uses carrying debt and recognized noncurrent pension/OPEB proxies; September current claims remain unreconciled. Litigation timing is a schedule, not a confirmed outcome.

Reproduction: Python 3 (standard library only) and pandoc are required. In this directory run:
python rebuild.py
This regenerates inputs_and_results.json, actuals.csv, fcff_projection.csv and QA.json, and renders PPG_report.html from PPG_report.md. model.py contains the transcribed inputs and all numerical assumptions. It funds MAX(physical reinvestment, positive change in NOPAT / incremental ROIC) in each explicit year; terminal economic investment uses terminal growth times next-year NOPAT / ROIC.
PPG_report.md, summary.json and source_ledger.json are frozen authored documents, not automatically rewritten investment prose. The rebuild asserts scenario values, inverse-margin wording, literal bilingual evidence and period math against them. Changing model assumptions requires updating authored text and summary, then rerunning the checks. No external source download is needed to reproduce calculations. Source URLs permit independent verification; full filings are not included.

Public scope is only the filenames in public_manifest.json. No raw filings, private working notes, account data or orders are part of this package. QA does not claim visual review. Any publication requires the separate review process; these files do not publish themselves.
