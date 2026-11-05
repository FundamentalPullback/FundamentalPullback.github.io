# LMT conditional valuation, 5 November 2026

All amounts USD millions except shares/price. This is completed conditional research with a proposed observation outcome, not an approved trade. Independent economic and reproducibility audit passed with caveats. See independent_audit/report.md. Publication is coordinated separately.

Reproduce offline:

1. python history/build_history.py
2. python beta.py
3. python model.py
4. python technical.py
5. python comparables.py
6. python qa.py
7. python render_report.py
8. python package.py

Model and comparable calculation use Python standard library. Beta additionally uses numpy/scipy; technical reconstruction uses pandas/lxml; HTML rendering uses pandoc. Raw website captures support audit only and are not included in the distributable support archive. Selected numerical facts, cash-flow schedules, market return data, sources, code, generated report and QA are included.

The historical source reconstruction already passed independent audit for the earlier factual report. The new conditional model has its own independent audit, and remains conditional on the economic assumptions. Inspect assumptions.md, source_ledger.json and model/inputs.json before using any result.
