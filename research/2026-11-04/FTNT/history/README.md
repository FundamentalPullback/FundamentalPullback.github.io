# Fortinet: financial history and cash-quality notes

As of November 4, 2026. USD millions except per-share figures. This package contains compact numeric source subsets and source excerpts, not full filings. Run `python reproduce.py` with Python 3, offline and without third-party packages. It regenerates financial_history.json, financial_history.csv and ttm_comparison.json from inputs.json. The inputs include row-level source mapping and URLs.

## Coverage and calculation policy

Three annual periods FY2023–FY2025; latest four quarters Q4 2025–Q3 2026; prior four quarters Q4 2024–Q3 2025; TTM ending September 2026 and prior TTM ending September 2025. Quarter income is directly reported except Q4 additive flows, which use FY less nine-month figures. Quarterly cash flow uses cumulative-YTD differences. Q4 diluted EPS is directly reported in the February 5, 2026 earnings release for both Q4 2025 and comparative Q4 2024 ($0.68 each). TTM EPS is the sum of four rounded, reported quarterly diluted EPS, not annual EPS less nine-month EPS and not a separately reported GAAP TTM measure. Accordingly its growth and P/E should be described as approximate.

Operating income is GAAP EBIT. D&A and SBC are the cash-flow-statement reconciliation amounts. SBC can differ from the income-statement non-GAAP bridge due to capitalization; do not silently substitute one for the other. Cash-flow working-capital changes are net of business combinations and are not the raw changes in balance-sheet accounts. Capex is cash PPE purchases only; inventory transferred into PPE is noncash, while acquisitions are separately reported.

## Main findings

TTM revenue rose from $6,554.7m to $7,880.9m; EBIT from $2,033.2m to $2,599.2m; net income from $1,873.6m to $2,282.3m. Summed quarterly diluted EPS rose from $2.43 to $3.08. Operating cash flow increased from $2,448.0m to $3,686.9m.

Simple CFO minus capex increased from $2,028.4m to $3,431.3m. The company's FCF definition additionally excludes specified non-recurring receipts: $14.0m IP proceeds in Q1 2025, and $17.0m escrow-settlement proceeds in Q3 2026. Company-definition TTM FCF therefore increased from $2,014.4m to $3,414.3m. FY2025 simple FCF was $2,225.8m versus company FCF of $2,211.8m. No real-estate capex addback is applied in this package.

Cash conversion is strong but headline FCF growth is not entirely earnings growth. The $1,399.9m increase in company-definition TTM FCF comprises $1,238.9m more CFO, $164.0m less capex, and $3.0m more excluded receipts. The deferred-revenue cash contribution increased $652.4m, from $631.5m to $1,283.9m. That is an important customer-prepayment benefit, not perpetual incremental earnings, and supports a conservative normalized DCF cash-conversion assumption. Deferred contract spending and its amortization must also remain in view. Removing all deferred-revenue contribution is only a sensitivity, not a preferred valuation measure; recurring subscriptions structurally involve advance payments.

TTM SBC cash-flow addback rose from $272.8m to $304.4m. FCF less SBC is an explicit economic-dilution sensitivity, not GAAP or company-reported FCF, and does not replace a share-count/dilution model. Never deduct SBC here and independently apply the same economic cost again without explaining the overlap. Likewise, CFO minus capex is a levered cash measure, not directly unlevered FCFF for an enterprise DCF.

## Comparability and earnings quality

Linksys became fully consolidated on January 31, 2025 after Fortinet acquired the remaining stake. The prior TTM contains only eight months of consolidated Linksys results, versus twelve months in the current TTM. Do not present total growth as organic: no verified quantitative organic/acquisition bridge is available in this dataset. Lacework's 2024 acquisition is another historical comparability issue.

Linksys generated a $39.9m bargain-purchase gain in other income and a $10.8m remeasurement gain in equity-method investments in Q1 2025, with a $30.6m deferred-tax-asset derecognition tax charge. These are below GAAP operating income. They affect net income/EPS and tax comparisons, not EBIT, and should not be removed from EBIT a second time. The 2024 bargain-purchase gain relating to Lacework was $106.3m, also below operating income. Gains on intellectual-property matters, in contrast, appear within operating expenses and therefore affect EBIT.

Q3 2026 effective tax rate was approximately 16% versus 20% in Q3 2025. Benefits from the FDDEI deduction were $36.2m versus $11.1m; excess SBC tax benefits were $25.5m versus $9.2m. Nine-month 2026 FDDEI benefits were $104.1m and excess SBC tax benefits $52.5m, versus $62.0m and $58.5m in nine-month 2025. These benefit levels should not be assumed invariant in a long-term tax-rate forecast. Cash taxes are separately available in the financial series.

## Audit boundaries

Ratios are derived rather than company guidance. FCF ex-deferred-revenue and FCF less SBC are isolated sensitivities, not a combined recommended normalization. All latest-period financial statements use filings available by the stated date. This package makes no trading recommendation or current-price claim. Source excerpt filenames and input evidence identify statements and columns; original SEC URLs permit independent verification.
