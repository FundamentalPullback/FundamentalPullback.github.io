# FormFactor factual financial history

As of November 4, 2026. Run `python reproduce.py` in this directory. No network, third-party libraries, or full filing text is needed: inputs.json is the minimal numerical input set, factual_ledger.json provides original numerical facts, period dates, XBRL concepts/contexts and SEC links. Derived data are in normalized.csv, normalized.json and ttm_comparison.json. Full filings and source-download/extraction scripts are kept separately under ../sources/.

All monetary values are USD millions, share counts millions, EPS dollars/share, ratios decimal fractions. Figures are GAAP unless labeled a segment management measure or a mechanically calculated cash proxy. These files contain historical analysis, not forecasts or adjusted valuation inputs.

## Primary sources

- FY2025 10-K, including FY2023 and FY2024 comparative statements: https://www.sec.gov/Archives/edgar/data/1039399/000103939926000009/form-20251227.htm
- FY2024 10-K (FY2023 balance sheet): https://www.sec.gov/Archives/edgar/data/1039399/000103939925000023/form-20241228.htm
- Q3 FY2026 10-Q: https://www.sec.gov/Archives/edgar/data/1039399/000103939926000043/form-20260926.htm
- Q2 FY2026 10-Q: https://www.sec.gov/Archives/edgar/data/1039399/000103939926000033/form-20260627.htm
- Q1 FY2026 10-Q: https://www.sec.gov/Archives/edgar/data/1039399/000103939926000023/form-20260328.htm
- Q3 FY2025 10-Q: https://www.sec.gov/Archives/edgar/data/1039399/000103939925000113/form-20250927.htm
- Q3 FY2024 10-Q: https://www.sec.gov/Archives/edgar/data/1039399/000103939924000035/form-20240928.htm

## Definitions and cautions

All annual and TTM intervals shown are 52 weeks; quarters are 13 weeks. Q4 is the difference of FY and 9M. Cash-flow quarter values are exact cumulative differences, not averages. Q4 diluted shares are estimated algebraically from rounded annual and 9M weighted shares, and EPS is then computed; no separately reported Q4 EPS is claimed. TTM EPS and weighted shares are similarly computed.

SBC expense, cash-flow addback and equity credit are separate fields. No capitalized SBC amount is invented. Q3 2026 expense is $8.835m, and 9M expense $25.556m. Those are not the issuer's non-GAAP SBC adjustment of $8.802m/$25.395m. Note 7's $0.161m restructuring SBC explains the nine-month gap; avoid double counting it as both SBC and restructuring. Quarterly allocation of the gap is not independently inferred.

Acquired intangible amortization is distinct from software amortization and total cash-flow D&A. The latter is tagged Depreciation in XBRL but titled depreciation and amortization in the statement. Do not add acquired amortization to total D&A twice. Software amortization and capitalized SBC are not separately quantified here.

Trade working capital equals AR + inventories - AP, a balance-sheet snapshot rather than the statement-of-cash-flows working-capital change. No days ratios are reported using inappropriate annualized/ending-balance shortcuts. Segment gross profit and net contribution exclude corporate allocations and are not consolidated operating profit.

CFO minus gross PP&E purchases is explicitly unadjusted FCF. Q3 2026 is $104.270m - $39.648m = $64.622m. Issuer-adjusted FCF is a different measure. TTM capex is $103.658m FY2025 - $92.345m 9M2025 + $64.439m 9M2026 = $75.752m. Acquisition spending and equity-investment purchases are separate, not capex.

Restructuring, factory startup, sale gains and equity-method income are retained as reported. Do not automatically add them back. Q3 factory startup is $6.375m. Null means not separately available, not zero. In particular missing quarterly gain/acquisition lines are not assumed zero merely to fill a model. FY2025 restructuring $5.7m is a rounded annual note disclosure; quarter-to-year math may not be exact.

Teradyne's $300m October 6 investment agreement was pending as of the November 3 filing. No cash proceeds or new shares from an assumed closing are inserted in historical figures.

## Checks

The offline script checks revenue minus cost of revenue equals gross profit and pretax income minus tax plus equity-method income equals net income across all nine output periods, within source rounding. Raw statement signs are preserved according to accounting concept (for example cash capex is a positive outflow).

## Capex timing

Prior TTM cash capex was $100.008m versus current TTM $75.752m. The Q3 FY2025 MD&A specifically identifies $55.0m of the $92.345m nine-month PP&E spending as the June 2025 Farmers Branch purchase. That purchase falls within prior TTM but outside current TTM. The lower current-TTM figure therefore is not evidence of a permanently lower maintenance/investment run rate, especially while factory buildout and startup continue. No unverified forward capex guidance is substituted for these cash-history facts.

Diluted shares derived by time-weighting are analytical proxies: treasury-stock effects, changing price and antidilution can prevent reconstruction of an actual GAAP quarterly/TTM denominator. Derived diluted EPS likewise is not a reported GAAP measure or a certified reconstruction. The valuation uses actual shares plus a separately selected awards proxy instead.
