# AWI conditional research package

As of November 7, 2026. USD millions except per-share amounts. No trades or execution approval.

Start with report.md or report.html, then summary.json and evidence-cards.json. Stage 3 is incomplete: a homogeneous historical-multiple study is not complete and future WAVE capital/distribution constraints remain qualified. Values are analyst scenarios, not an approved valuation. The report explains the historical cash classification and the explicit terminal maintenance reset.

Reproduction: run `python build_report.py` in this directory using standard-library Python. It imports model.py, rebuilds the numerical inputs, historical and forecast schedules, cases, inverse valuation, sensitivities, arithmetic QA, bilingual report and conditional flags. Alternatively `python model.py` rebuilds numerical calculations only; it does not replace the full report's economic-readiness qualifications. No network access or third-party package is needed.

Provenance: source-ledger.json contains only public URLs, titles, dates and purposes. Primary historical figures and company guidance are distinguished from analyst forecast assumptions. Scanner scores are supplied screening inputs, not fundamental approval. evidence-cards.json contains exact bilingual card text, provenance and public supporting URLs. No complete source filing, private source inventory or private-source hash is included.

The public manifest names only the explicitly permitted generated research files. Its hashes identify generated public deliverables, never private source documents. Case values remain unchanged after independent review. No remote publication is performed by these scripts.
