# PWR reproducible partial research
USD millions unless indicated. Run offline in this order:
1. python history/rebuild_history.py
2. python comparables/reproduce.py
3. python analyze.py
4. python report.py
5. python prepare.py
6. python qa.py

Optional: python package.py builds manifest.sha256 and support.zip. No network or external Python packages required. Numeric inputs and source provenance are included; full filings and downloaded webpages are not distributed. The history README explains reported/derived fields and limitations. The report preserves historical scanner dates, discrepant current references, unconfirmed next earnings date, accounting and economic limits. Unknowns are null, not zero. CFO−PPE−SBC is only a mechanical proxy, not owner FCF. There is no DCF, approved entry or completed integral valuation in this package.
