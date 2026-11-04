# TRMD reproducible partial research

USD millions except EPS and daily charter rates. Offline steps:
1. python history/build_history.py
2. python comparables/reproduce.py
3. python analyze.py
4. python report.py
5. python prepare.py
6. python qa.py

Optional: python package.py regenerates the support archive. No network or external Python packages required. Selected numeric inputs and provenance are included; complete company filings are excluded. Historical reported NAV and mechanical sensitivities are not an intrinsic valuation. All valuation, owner FCF and integral equity-bridge fields remain null. Distinguish capex commitments already deducted in NAV from subsequent JV funding and dividends. Historical capital and quote references do not certify current execution. History README documents rounding and SBC/EPS limits.
