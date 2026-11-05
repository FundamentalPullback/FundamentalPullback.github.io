# CTSH independent valuation audit, November 5, 2026

## Conclusion

**Core model passes independent numerical and economic review, with material assumption caveats.** The revised funded-growth values are **$79.34 base, $51.76 bear and $109.12 bull**, at the **$65.78 November 4 regular close**. The already-owned business plus committed DyFlex transaction cross-check is **$84.95**. These are present-value estimates, not a dated price target, guaranteed floor, or order authorization.

A **conditional reasonable-price Stage 3 candidate** is defensible if that category explicitly permits a price near conservative fair value. A claim of robust cheapness or downside protection is not supported. The base has 20.6% upside, while the bear has 21.3% downside. A moderate operating combination at a market beta of 1 is worth about $64.20, or $63.58 with another five DSO days. Therefore, a partial-entry case must be justified by prospective business returns and risk tolerance, not presented as a large margin of safety. No Stage 3.5 technical trigger, position size, or executable purchase is approved here.

This review used a separate cohort-based implementation without importing the author's valuation or technical code. All **264 numerical tie-outs** pass, covering annual revenue, EBIT, reinvestment, FCFF, present values, and EV/equity/per-share bridges in all four cases. Price, moving averages, ATR, RSI and the 50-row source overlap independently reproduce. The original and revised audit results remain separate.

## Corrected findings

1. **DyFlex consideration was disclosed.** The October 21 announcement omitted financial terms, but the October 29 10-Q Note 13 states approximately **$210m cash at closing**, subject to adjustments. Both the SEC HTML and issuer PDF agree. Source-review language was corrected. The main 2027 acquisition budget includes that $210m, rather than adding it twice. The owned-business cross-check now includes only the committed deal and no speculative future transactions. DyFlex revenue and allocation to amortizable intangibles remain analyst estimates, not reported target data. [Q3 10-Q, Note 13](https://www.sec.gov/Archives/edgar/data/1058290/000105829026000041/ctsh-20260930.htm).

2. **Acquisition settlement now matches recognition timing.** DyFlex is assumed to close at the Q1 midpoint, 0.125 years after January 1, with 87.5% first-year recognition. Other acquisitions close at midyear and recognize 50%. Their purchase cash is discounted at those times, while ordinary annual operating cash retains the conservative year-end convention. This lowers the revised base from $79.74 to **$79.34**. The earlier $79.74 result is superseded.

3. **Owned-business fade presentation was repaired.** The original 2032 D&A display restarted from the funded 2.6% ratio and jumped upward despite amortization run-off. D&A canceled against aggregate reinvestment, so there was no valuation effect. The revised display fades from the actual year-five D&A ratio. Years six through ten remain aggregate reinvestment estimates, not literal property-capex and transaction forecasts.

## Cost of capital challenge

- Independent OLS using 58 complete monthly adjusted-close returns, January 2022 through October 2026, gives beta **0.806681**, normalized beta **0.871121**, and WACC **8.517570%**. The arithmetic and exclusion of incomplete November are correct.
- Beta is noisy: standard error **0.290377**, R-squared **0.121121**, reported 95% interval approximately **0.225–1.388**. Shorter samples do not establish precision: 24/36/48-month betas are approximately 0.446/0.662/0.768, with still larger standard errors. Shrinkage toward 1 is defensible, but it is an analyst method, not a proven permanent systematic risk.
- Treasury confirms November 4 ten-year yield **4.90%**. Damodaran's November 1 implied ERP is **4.41%**, with the source itself stating a **5.29%** Treasury calibration. Mixing the latest daily rate with a monthly ERP is a normal practical convention, but the result must not be represented as a single simultaneous observation. Using the ERP source's stated 5.29% rate gives WACC **8.8881%** and base value **$74.38**. That sensitivity is not a claim that 5.29% was the November 4 ten-year yield. [Treasury daily curve](https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?field_tdr_date_value=2026&type=daily_treasury_yield_curve); [Damodaran ERP](https://pages.stern.nyu.edu/~adamodar/New_Home_Page/home.htm).
- Debt cost 5.75% is a forward estimate, not the company's current floating coupon. The new facility's initial 0.875% spread is source-supported. With only about 5% debt weight, moderate debt-cost estimation error is much less important than equity-risk and operating assumptions.
- No independent peer-derived unlever/relever beta was supplied. The market-beta-1 sensitivity is therefore important. It produces WACC **9.0575%** and base value **$72.31**. The empirical beta is a reasonable central input, not a reason to omit the higher discount-rate case.

## Decision-relevant combined sensitivities

All values below use the revised acquisition settlement timing. The moderate operating combination means organic growth 2%, each explicit margin and terminal margin 50 bp below base, tax 27%, acquisition revenue multiple 3.5x, and capex 1.8% of revenue. It does not impose a recession or reduce terminal growth below 2.5%.

| WACC assumption | Base operations | Moderate operations | Moderate plus five DSO days |
|---|---:|---:|---:|
| Empirical/shrunk beta, 8.5176% | $79.34 | $70.65 | $70.02 |
| 9.00% | $73.00 | $64.83 | $64.21 |
| Market beta 1, 9.0575% | $72.31 | $64.20 | $63.58 |
| 9.50% | $67.36 | $59.67 | $59.05 |
| 10.00% | $62.48 | $55.20 | $54.59 |
| ERP-source stated RF, 8.8881% | $74.38 | $66.10 | $65.48 |

At $65.78, break-even WACC is **9.6546%** for base operations, **8.9160%** for moderate operations, and **8.8621%** for moderate operations plus five DSO days. It would be misleading to discuss only the 9.65% base break-even rate while ignoring reasonable combined operating and capital-cost changes. Conversely, stress cases below the market do not by themselves require rejection: no universal discount-rate hurdle or percentage margin-of-safety rule is imposed by this audit.

## Operating cash and reinvestment economics

### Acquisitions

The cohort construction is coherent. Base 2027 new acquired annual revenue is 1.5% of $22,095m, or $331.425m. At 3x sales, the acquisition budget is $994.275m, including DyFlex's $210m. Current-year recognition is partial and the rest carries into the next year. Organic growth is also applied to prior acquired operations. The separate 0.6% inherited 2027 growth is already purchased, so no second acquisition payment is required.

Charging new acquired operating NWC again at closing would double count capital included in the transaction price. The model avoids that. A very small uncharged NWC increment on organic growth of the prior-year unrecognized acquired-revenue fraction remains an approximation; its scale is well below decision materiality. Purchase multiples are approximate scenario anchors from rounded growth contributions, not exact standalone transaction revenue multiples.

The owned-business cross-check being worth more than the funded strategy is economically informative: the modeled acquisition prices do not automatically create value. It is not permission to remove management's acquisition bill while retaining the acquired growth.

### D&A, SBC and contract costs

Forecast EBIT retains SBC, restructuring/transformation allowances and acquired amortization. D&A is added back once. Software already in property capex is not separately charged. SBC is not added back while holding future shares constant. The current 1.8m incremental-dilution estimate is an estimate of outstanding awards, not a recurring buyback benefit.

Contract capitalization is a separate **net** cash-versus-expense allowance, 0.2% of revenue in the base. It is not gross capitalization; no second addition of contract-cost amortization is appropriate. Incremental NWC must exclude these same deferred costs. The model's arithmetic does so, though the 20% NWC coefficient is a forecast judgment rather than a precisely fitted reported ratio.

The acquired-intangible run-off in the owned case avoids a perpetual amortization credit without new acquisitions. Cash-tax treatment of acquired intangibles is still approximate because book and tax amortization can differ. The 25–27% tax scenarios partly address this; they are not a transaction-by-transaction tax-shield schedule.

### Cash conversion is a meaningful assumption

Revised 2027 operating FCFF before new M&A is **$2,725.18m**, versus the source review's **$2,143.36m** TTM economic cash proxy, an increase of approximately **27.1%**. The figures are not strictly comparable normalized cash measures, but the gap matters. No actual DSO release is booked. Instead, the model assumes much less new cash absorption than the recent period, plus normalization of taxes and operating profitability. This should be described as improved conversion that must be demonstrated, not as a value already guaranteed by recurring earnings.

After purchase cash, 2027 base FCFF is about $1.731bn. Cash generation, not adjusted EPS growth supported by repurchases, should validate the thesis. The principal proof points are Q4 cash conversion, DSO and contract assets, net contract capitalization, margins after FX benefit, acquired economics, and 2027 guidance.

### Terminal economics

The five-year transition properly ends at 2.5% growth and 12% marginal ROIC. Terminal reinvestment is NOPAT × g/ROIC, so growth is not free. In the base, terminal value is approximately **59.7% of EV**, still a material duration risk. The transition is an aggregate capital-allocation framework, not evidence of a disclosed post-2031 deal pipeline. It cannot be described as both a literal complete stop to M&A and a continuation of identical acquired growth without explaining replacement investment.

## Cash stub, debt and share bridge

- September cash plus the full Q4 cash estimate is acceptable when the model rolls that balance toward November/December. It would be wrong to retain September cash and include only the remaining November–December fraction without accounting for October cash generated.
- The $880m issuer-FCF midpoint is an estimate inferred from 90–100% conversion guidance, not an issuer dollar forecast. Subtracting $50m SBC and adding $3m after-tax net interest expense gives $832.22m economic FCFF. A simple split between accrued October cash and future stub cash raises value only about **$0.016/share**, so the conservative full-stub year-end discount is immaterial.
- $70m estimated post-September repurchases is explicitly deducted, preventing October's reduced share count from being free. Exact post-September cash, repurchases and award dilution remain unknown; the sensitivities are appropriately small relative to operating/WACC risk.
- Funded debt $1,552m, operating cash reserve $500m, pension/gratuity reserve $260m and Astreya contingent consideration $25m are counted once. The pension reserve is December 2025, not September 2026; it is an uncertainty reserve and not a precise current valuation of the obligation.
- The October refinancing replaces the prior facilities. Undrawn borrowing capacity is not cash. Escrow already spent and the Indian disputed-tax deposit are not excess cash. The unrecognized Syntel award receives no value.
- The November dividend remains in current equity value because the valuation is before its record/payment dates; deducting it merely because it will be paid later would understate the shareholder's current cum-dividend value.
- Operating leases remain an operating expense and are not also deducted as funded debt. Future buybacks do not generate costless per-share growth.

## Technical verification and limits

The 501-session series independently yields close $65.78, EMA20 $64.8868, EMA50 $62.1359, EMA200 $60.7607, ATR14 $2.8296, RSI14 53.6667, and 252-session high about $87.03. The 50 most recent StockAnalysis rows match the raw Yahoo OHLC source to floating-point precision. Prices are split-adjusted rather than dividend-total-return prices, appropriate for chart indicators. A rising EMA200 supports trend context; it does not establish a technical entry point or stop.

The proposed $66.10 future-close threshold requires special care: October 30 high $66.06 was followed by November 2 high $66.33 and November 4 high $66.77. Therefore, $66.10 is not a breakout above current rebound resistance. A genuine breakout above $66.77 is incompatible with a $66.50 entry cap. The appropriate response is to wait for a new structure or clearly justify a different recovery/pullback setup, not to raise the cap or relabel an old level as current resistance. November 4 volume divided by the 20 prior sessions is 1.6424; the 1.5747 summary includes November 4 within its 20-session average. A future trigger must use the explicitly specified convention.

## Remaining limitations and release scope

Missing exact facts are target standalone revenue/earnings, final DyFlex closing adjustments and acquired cash, current pension balance, exact post-September capital returns/current dilution, and future cash tax and contract-capitalization intensity. Each is disclosed or treated as a scenario. None is silently promoted to fact.

The core revised model can be used analytically with the above caveats and conditional reasonable-price classification. This audit does not publish, change the website, place an order, or certify a future technical entry. Final report.md, report.html and supporting controls passed 22 report/control checks. The author's 156 controls and 23 source checks also pass; the nine-step reproducibility log reports success. Exact hashes are recorded in final_report_audit.json. Footer-only additions require rehashing, not a new valuation.


## Final report and prospective setup review

The obsolete $66.10 proposal was withdrawn. The final report instead describes a future analyst-defined pullback/stabilization setup: a regular-session low at $62.50–64.00, close above $64.75 and no higher than $65.25, above the open and EMA50, and volume at least the prior 20-session average excluding the signal session. It is not statistically validated and no current signal is asserted. The last eligible signal is November 9, with any proposed next-session DAY order expiring November 10. There is no actual order authorization, portfolio P, verified cash or quantity. Genuine breakout above $66.77 remains suspended because it exceeds the $66.50 fundamental cap. This repair resolves the old-level selection concern.

The report's original after-close timing statement was also corrected. The issuer scheduled Q3 results before the October 29 open and the call at 8:30 a.m. Eastern, so that day's decline cannot be classified as pre-results. [Issuer scheduling announcement](https://news.cognizant.com/2026-10-02-Cognizant-Schedules-Third-Quarter-2026-Earnings-Release-and-Conference-Call).

Removing the entire economic Q4 FCFF stub gives $77.5096, now correctly reported as $77.51. This differs slightly from setting issuer FCF to zero while retaining the SBC and net-interest adjustments.

**Final analytical release status: PASS WITH MATERIAL ASSUMPTION CAVEATS.** Conditional reasonable-price Stage3 classification is supported. Stage3.5 and any financial transaction remain unapproved.

The final added FCF-per-share paragraph is independently verified: annual strict FCF divided by reported diluted averages rounds to $3.99/$3.68/$5.31; quarterly ratios round to $1.62/$0.42/$0.98/$2.06. Q2 is $459m/466m = $0.9849785, corrected from $0.99 to $0.98 before release. The TTM/current-share proxy is $2,363m/448.830425m = $5.2647946, correctly rounded to $5.26 and identified as not directly comparable historical per-share FCF. Ratios are now calculated dynamically in the author report rather than manually typed. Publication metadata preserves conditional fundamental approval and explicitly false execution/Stage3.5 flags. The final frozen report hashes match the author's last declared versions.
