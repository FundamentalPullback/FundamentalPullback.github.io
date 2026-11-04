# LSCC reproducible partial research
Amounts in USD millions in analysis/facts, USD in the history ledger unless noted. No valuation, owner FCF, integral equity bridge or entry approval.
Run with Python standard library, offline, in this order:
1. python history/reproduce.py
2. python comparables/reproduce.py
3. python analysis.py
4. python prepare.py
5. python report.py
6. python qa.py
Run python package.py to recreate the support archive and manifest. All valuation nulls are intentional. The historical numeric extract and selected SEC facts are the inputs, not full filings. The historical scanner and a separately timestamped current price must not be merged.
