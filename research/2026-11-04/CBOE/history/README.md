# CBOE financial history, as of November 4, 2026

This directory contains the model-loading support package. All monetary values are USD millions except EPS (USD per share) and shares (millions). Latest financial period: September 30, 2026; latest statements filed October 30, 2026.

Reproduce entirely offline with Python 3:

    python calculate.py
    python validate.py

No third-party Python packages, network connection, raw filings, or hidden external files are needed for these two commands.

- `inputs.json`: selected source-reported facts and source URLs/locators; no raw filings.
- `calculate.py`: transparent fiscal-quarter, TTM, margin, cash-flow and normalization calculations.
- `history.json` / `history.csv`: full history, including supporting YTD periods, three annual years, eight comparison quarters and two TTMs.
- `balance_sheet.csv`: point-in-time balances, never summed into TTM.
- `summary.json`: readily reusable current/prior TTM, latest quarter, cash/debt and readiness information.
- `source_facts.csv` / `source_index.csv`: reported facts, direct Q4 share counts and CF-quarter derivation provenance.
- `analysis.md`: interpretation and comparability cautions.
- `validate.py`, `validation.json` / `validation.csv`: exact checks performed and their results.
- `qa_flags.csv`: material analytical caveats that remain even though technical reconciliation passes.

Raw source documents and the extraction helper remain in the sibling `sources` directory and are not part of this deliverable. HTML table indices in source locators are zero-based and count all `<table>` elements in the saved SEC HTML. Income and cash-flow figures were read from complete primary statements, not inferred from reported growth rates.

The parent research report owns valuation. Liquidity proxies here are factual bridges and are not assertions that cash is immediately distributable or that a minimum regulatory reserve is sufficient for all corporate needs.
