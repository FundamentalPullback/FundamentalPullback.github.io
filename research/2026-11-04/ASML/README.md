# ASML research support

Conditional research, 4 November 2026. Not an execution approval or integral Stage3 certification. See report.md for every material qualification.

Offline reproduction, from this folder:
1. python build_financials.py
2. python capital.py
3. python model.py
4. python comps/calculate.py
5. python peers.py
6. python report.py
7. python qa.py

Requires Python standard library only. Regenerated financials/model/report are deterministic. Optional HTML rendering uses Pandoc. prepare.py regenerates editorial publication metadata and its English evidence appendix; it is not required for numeric reproduction. package.py creates a ZIP and per-member hashes. checksums.txt covers all packaged members except itself; manifest.sha256 outside ZIP additionally identifies the ZIP itself.

The public package contains necessary numerical fact extracts and original analysis, not full filings or issuer transcripts. history/README.md documents the original collection workflow; its build_history.py and original documents are local research material deliberately omitted. Use the root build_financials.py to reproduce from portable numeric rows instead. history/source_manifest.json identifies originals for provenance, not as required public files. All essential source links are in the report, evidence/claims.json, the history README and comps inputs/CSV.

Capital and market values in evidence/claims.json are attributed inputs, not independent confirmations of their economic treatment. Model assumptions, debt/tax proxies, incomplete capital rollforward and strategic asset exclusions are intentional qualifications, not assertions of exact current balance sheet.
