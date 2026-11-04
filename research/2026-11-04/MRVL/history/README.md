# MRVL financial history, as of November 4, 2026

## Files and reproduction
- `numeric_facts.json`: manually verified numeric source subsets, source URLs and acquisition/perimeter facts. Currency figures are USD millions; EPS is USD per share; conversion shares are millions.
- `reproduce.py`: Python standard library only. Run `python reproduce.py` from any directory. Reads the JSON adjacent to itself, reproduces `normalized_history.json` and `normalized_history.csv`, and asserts that each additive TTM financial metric equals the sum of four quarters.
- `normalized_history.json` and `.csv`: three fiscal years, last four complete quarters, TTM, prior TTM, cash-investment variants and caveated EPS/common-income measures.
- Full filings are deliberately NOT included in this folder. The sibling `private_sources` folder is a research cache, not a public deliverable.

## Source and period map
FY2024 ended February 3, 2024; FY2025 ended February 1, 2025; FY2026 ended January 31, 2026. The FY2026 10-K supplies all three audited annual income and cash-flow columns. FY2024 was 53 weeks; FY2025 and FY2026 were 52 weeks. Annual comparisons are as reported, not week-normalized.

Latest complete financials are Q2FY2027 ended August 1, 2026, filed August 28. Q3FY2027 preliminary revenue is excluded from every filed-history calculation.

TTM = FY2026 − H1FY2026 + H1FY2027. Prior TTM = FY2025 − H1FY2025 + H1FY2026.

Q3FY2026 income-statement and EPS values are direct in the November 1, 2025 10-Q; cash-flow values are nine months minus first six months. Q4FY2026 income, EPS and cash-flow values come directly from the fiscal-year earnings release and reconcile to annual minus nine months. Q1FY2027 is directly reported. Q2FY2027 income and EPS are directly reported; cash-flow values are six months minus first quarter. H1FY2026 comparative values are in the Q2FY2027 filing. H1FY2025 comes from its own Q2 10-Q. Prior-TTM quarterly EPS is direct Q3FY2025, Q4FY2025, Q1FY2026 and Q2FY2026, obtained from the comparative columns in these same sources, not an annual-minus-YTD EPS bridge.

## Headline results
TTM revenue $9,450.3m; GAAP EBIT $1,561.3m; parent net income $2,639.9m; CFO $2,200.3m. Prior-TTM revenue $7,234.9m; GAAP EBIT $93.1m; parent net loss $103.4m; CFO $1,844.8m.

GAAP EBIT means reported operating income, not pretax income plus interest expense. EBITDA shown is a mechanical, non-GAAP EBIT + both disclosed D&A categories; it is NOT management's adjusted EBITDA.

## Cash investments, D&A and SBC
TTM PPE purchases $470.2m, investing technology-license purchases $7.3m, and financing technology-license obligation payments $130.6m are separate positive cash uses. The financing classification does not make technology-license cash costs disappear economically.

- CFO minus PPE only: $1,730.1m.
- After investing technology-license purchases: $1,722.8m.
- After both investing purchases and financing technology-license payments: $1,592.2m.
- Further subtracting $828.9m SBC gives a rough owner-cash-after-SBC proxy of $763.3m, versus $786.0m prior TTM. This is a deliberately labeled analytical proxy, not a GAAP measure or a substitute for modeling dilution; do not subtract SBC again if a valuation already treats dilution explicitly.

D&A requires TWO disclosed cash-flow lines: TTM regular depreciation/amortization $368.8m plus acquired-intangible amortization $892.7m = $1,261.5m total. H1FY2027 similarly is $188.5m + $440.1m. Do not use only the line named depreciation and amortization. Do not add back SBC or restructuring automatically to economic earnings. SBC uses the income/cash-flow expense amount, not the larger stockholders-equity entry that can include capitalization effects. A standalone internal-use software capex figure is not separately disclosed in these statement excerpts; technology licenses are retained in their own categories, not silently treated as zero or relabeled as software capex.

## Earnings quality and perimeter
The August 14, 2025 automotive Ethernet sale produced $1,830.4m pretax gain in interest income and other, net. The gain inflates FY2026 and current TTM net income but does not inflate GAAP operating income. Cash proceeds net of selling costs were $2,478.6m in investing activities and are excluded from CFO and every FCF variant here. A $14.0m property-sale gain in fiscal 2026 also appears in the cash-flow restructuring reconciliation. Do not mechanically remove a pretax gain dollar for dollar from after-tax net income and label the result normalized after-tax earnings.

FY2025 restructuring costs including COGS totaled $711.8m, versus $131.1m FY2024 and $16.0m FY2026. The prior TTM contains the substantial FY2025 Q3 restructuring episode, so its low GAAP EBIT is not a clean recurring baseline.

Celestial AI closed February 2, 2026 and XConn February 10, 2026. Their results enter consolidation only from their acquisition dates. FY2026 and the prior TTM exclude these businesses; current TTM includes their post-close H1FY2027 results. Neither TTM is full-year acquisition-pro-forma history. As of Q2FY2027, Celestial consideration was $3,533.7m after a $3.7m measurement-period reduction, and XConn consideration was $469.0m. Cash consideration, stock consideration, acquired cash and contingent consideration are distinct from cash-flow acquisition spending. H1FY2027 acquisition cash use, net of acquired cash, was $1,270.9m. Celestial acquisition transaction expense in H1 was $30.1m. Filings describe standalone post-close revenue/earnings of Celestial and XConn as immaterial; that does not imply their acquisition, dilution or future investment economics are immaterial.

H1FY2027 earnings include $433.7m contingent-consideration fair-value expense, offset by a $131.0m forward-stock-purchase-contract fair-value gain, net $302.7m expense below EBIT. Q1 net expense $250.7m, Q2 $52.0m. These noncash movements are in the CFO reconciliation. Retain the associated acquisition/earnout claims in valuation rather than treating an earnings addback as eliminating the liability.

## Parent income, common allocation and EPS: nonadditivity warning
No noncontrolling-interest deduction is presented in the statements used. `net_income_parent` is reported consolidated net income. Beginning March 31, 2026, NVIDIA's $2bn Series A preferred investment creates a second common-stock class for two-class EPS, not a conventional fixed-coupon preferred deduction. It is initially convertible into 21.778m common shares.

Direct basic common-income allocations: Q1FY2027 $33.4m (parent $34.5m); Q2FY2027 $300.5m (parent $308.0m). The H1FY2027 common allocation is $336.0m, although the sum of the two directly reported quarter allocations is $333.9m. The two-class allocation is recomputed for the period using weighted-average shares and declared dividends. This $2.1m difference is genuine period-method nonadditivity, not a summation mistake.

Accordingly, TTM common income is explicitly labeled in two ways:
- Annual-plus-YTD bridge: $2,633.4m.
- Sum of four direct quarter basic common allocations: $2,631.3m.
Neither is an issuer-reported GAAP TTM common numerator. Parent income remains additive at $2,639.9m. Do not force either common figure into reported diluted EPS: the if-converted diluted numerator adds back the preferred allocation and includes conversion shares in the denominator.

Latest direct quarterly diluted EPS, in order Q3FY2026 / Q4FY2026 / Q1FY2027 / Q2FY2027: $2.20 / $0.46 / $0.04 / $0.33. Their sum is $3.03, a sum of rounded direct quarterly EPS, not recomputed GAAP annual EPS. Prior-TTM quarterly diluted EPS sum is −$0.13. Annual-minus-YTD EPS arithmetic and dividing TTM income by spot share count are not substitutes.
