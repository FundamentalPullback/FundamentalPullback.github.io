# CBOE independent research package

As of November 4, 2026. Independent research-grade audit completed November 4 at 17:40 UTC. Conditional research, not entry approval. Exact next earnings date, post-September capital movements and Canadian closing economics remain unresolved.

All monetary model inputs are USD millions unless labeled per-share. Price uses November 3 regular close; scanner October 30 is a separate immutable observation. Scenarios, valuation caveats and original references are in report.md. history and comps preserve their own methodological limits. Full third-party filings in private sources/ are deliberately excluded from the deliverable.

Reproduce offline from the package root with Python 3:

    python history/calculate.py
    python history/validate.py
    python comps/comps.py
    python model/model.py
    python valuation_checks.py
    python qa.py

history has 915 arithmetic/provenance checks; comps has 49. valuation_checks independently reconciles annual FCFF, terminal/license tail and equity. These are program checks, not an assurance opinion or proof of forecast accuracy. No external packages or network are required.

build_report.py generates the own narrative using deterministic model results. prepare.py writes the audited conditional research metadata. The final publisher assigns public ID and fingerprint; author package contains no trading approval.
