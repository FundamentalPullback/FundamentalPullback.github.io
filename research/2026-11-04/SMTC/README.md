# SMTC reproducible partial research

As of November 4, 2026. No valuation, certified owner FCF, retained-perimeter equity bridge or entry approval. Price reference is November 3 close; capital statements are July 26 with August cover shares and October guidance, not a current pro forma balance.

Run from the extracted folder, Python standard library only, no network:
1. python history/reproduce.py
2. python comparables/calculate.py
3. python analysis.py
4. python prepare.py
5. python report.py
6. python qa.py

`python package.py` regenerates a support archive and internal SHA-256 manifest. The manifest excludes itself to avoid circular hashing. Full source filings are not in the archive: source indexes link originals; numeric extracts and input ledgers reproduce results offline. Read the history README for direct EPS and cash-flow definitions. Numerical checks validate arithmetic, not forecasting, legal conclusions or completeness of undisclosed facts.
