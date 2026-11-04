# PANW reported history, verified 4 November 2026

Run `python reproduce.py` (Python standard library, no network). The selected observations are numeric factual extracts, not full filings. `reported_history.csv/json` includes FY2024–FY2026, all eight FY2025–FY2026 quarters, cumulative reconciliation periods, and TTM/prior TTM aliases. Cash amounts are USD millions. TTM ends 31 July 2026 and equals FY2026; no Q1FY2027 actuals are assumed.

## Normalization and limitations
- Quarterly income-statement amounts are direct observations through Q3. Q4 is FY less 9M. Q2/Q3 quarterly cash flows are cumulative differences. These are fiscal quarters ending October, January, April and July, not calendar quarters. All direct quarterly values reconcile with cumulative differences.
- Gross FCF = CFO minus the entire reported purchases of property, equipment and other assets line. It includes relevant capital spending without company adjusted-FCF exclusions. No acquisition cash is mislabeled as capex. Acquisition cash spending is provided separately and is not included in this FCF definition.
- `fcf_less_sbc_cf` deducts the exact equity SBC addback in the cash-flow statement. `fcf_less_sbc_expense` separately deducts total GAAP SBC expense. Neither is statutory FCF, owner earnings, nor a guarantee of distributable cash. These alternative analytical proxies must not be combined by deducting SBC twice.
- Total GAAP SBC expense differs from cash-flow equity SBC. FY2026 expense 1,815 versus CF addback 1,774; FY2025 1,300 versus 1,295; FY2024 1,079 versus 1,076. Do not replace either series with earnings-release share-based-compensation-related charges, which have a different definition.
- Capitalized SBC and separate PPE/software CASH capex were not separately disclosed in the reviewed statements. Missing fields are null, not zero. Do not infer capitalized SBC from differences between equity-statement adjustments and CFO addbacks without a bridge.
- Internally developed software net carrying values were 266 and 167 at July 2026/2025. Annual amortization was 104/83/78 in FY2026/2025/2024. Net asset movement plus amortization does NOT establish cash software additions, especially in an acquisitive year. The source reports aggregate capex 440/247/157, so no additional software subtraction is made.
- Total D&A was 855/343/284. Acquired intangible amortization was 640/166/121. After also deducting software amortization 104/83/78, residual physical/other D&A is 111/94/85, an arithmetic residual rather than a separately named reported line.
- Cash income taxes were 199/505/342. Quarterly cash taxes were not separately disclosed in the reviewed 10-Q cash-flow statements. FY2024 net income 2,578 includes an income-tax benefit of 1,590, so it is not a sustainable earnings baseline.
- Deferred contract costs primarily represent commissions. Their CFO cash-change line is negative; amortization is positive. FY2026 cash-change outflow 795 versus amortization 590 implies a 205 net cash timing drag; FY2025 555 versus 481 implies 74. Do not treat the gross deferred-contract-cost cash change as additional capex on top of CFO.
- Deferred-revenue CFO changes exclude acquisition effects. FY2026 1,202 versus 1,239 in FY2025 and 2,180 in FY2024. These are cash-flow reconciliation changes, not simply year-end balance differences.
- Chronosphere acquired 29 January 2026; CyberArk acquired 11 February 2026. FY2026 reported growth 24.50%, Q3 31.15%, Q4 34.46% is NOT organic growth. Acquisitions, cash taxes, commissions and customer prepayments affect comparability.
- Full-year FY2026 GAAP EBIT margin 6.05% versus 13.48% FY2025. Gross FCF 4,113 versus 3,469; FCF less CF SBC 2,339 versus 2,174. The latter grows only 7.59%, versus reported revenue growth 24.50%. Its margin falls from 23.58% to 20.37%.

## Primary sources
- FY2026 10-K, FY2024–26 comparative statements: https://www.sec.gov/Archives/edgar/data/1327567/000132756726000023/panw-20260731.htm
- Q3FY2026 10-Q: https://www.sec.gov/Archives/edgar/data/1327567/000132756726000015/panw-20260430.htm
- Q2FY2026 10-Q: https://www.sec.gov/Archives/edgar/data/1327567/000132756726000005/panw-20260131.htm
- Q1FY2026 10-Q: https://www.sec.gov/Archives/edgar/data/1327567/000132756725000035/panw-20251031.htm
