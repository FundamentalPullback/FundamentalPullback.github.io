# HRI reproducible factual research

Offline, standard Python only:
1. python history/build_history.py
2. python comparables/reproduce.py
3. python analyze.py
4. python report.py
5. python prepare.py
6. python qa.py

Optional python package.py rebuilds archive and manifest. Inputs are selected primary numeric observations with URLs and XBRL contexts where available. Full filings are excluded. History uses reported cash purchases, not presumed maintenance capex. Disposal proceeds and gains are distinct. Finance leases, failed-sale financing and operating leases are separate. Supplier payable sensitivity is an illustration, not a correction of cash flow. TTM periods have different H&E coverage; EPS sums are not GAAP TTM EPS. All valuation, owner FCF and integral equity bridge fields remain null.
