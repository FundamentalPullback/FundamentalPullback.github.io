# November 6 scanner: G, LMT, BZ, TDC and TRI

Prepared November 7, 2026. Decision horizon: 6–12 months. Scanner Last prices are the requested reference observations, not certified regular-session closes or live executable quotes. No trades or orders were made.

## Decision

**LMT is the only name in this group I would now elevate to a fundamental candidate at a reasonable price.** At $569.04 it is more attractive than at the $595.04 evaluated on November 5. This is a low-to-medium-conviction candidate, not a clear bargain: ordinary changes in both execution and discount rate can erase the apparent discount. The old conditional research is complete enough to make this judgment; it is not necessary to wait for perfect knowledge or an arbitrary 15-minute candle.

**G remains a collections-recovery watch, TDC remains a valuation pass, TRI remains a quality-at-too-high-a-price watch, and BZ remains conditional on capital allocation.** Their latest evidence does not establish a new compelling investment at the supplied prices. These conclusions do not impose one universal discount or required return across all five companies.

| Name | Scanner Last | Current assessment | What actually changed |
|---|---:|---|---|
| LMT | $569.04 | Reasonable-price fundamental candidate; limited conviction | Price improved materially since the completed Nov5 valuation; no new financial release superseding Oct22 found |
| G | $42.27 | Watch collections; no promotion | Nov5 earnings improved, but cash conversion deteriorated further; ERP-related collection delay now explicit |
| TDC | $31.80 | Pass at this valuation | Nov5 EPS guidance improvement, but quarterly revenue/margins weakened and adjusted cash still needs SBC/equipment deductions |
| TRI | $112.57 | Wait for better economics | Nov3 results already incorporated in Nov4 completed DCF; scanner price is higher, not cheaper |
| BZ | $17.65 | Conditional watch | No Q3 date or results found on current primary calendar/releases; earlier cash-distribution concerns remain |

## LMT: reasonable price, with a quantified reason for restraint

The [November 5 report](https://fundamentalpullback.github.io/research/2026-11-05/stocks/LMT.html) already incorporated Q3, the Ultra acquisition, program-loss cash payments, a finite CAS recovery schedule, pension obligations, economic SBC and reinvestment. Its model has been reproduced numerically in this review: base **$722.90**, full adverse **$273.80**, favorable **$1,159.67**. These are conditional long-term present values, not guaranteed 6–12-month prices or probability-weighted targets.

The business has a credible medium-term case: Q3 sales rose 11%; the $292bn backlog supports visibility; 2026 FCF guidance is $7.8–8.0bn. The offset is real: Q3 FCF declined to $3.0bn from $3.35bn, and management explicitly warns that incurred Lot20 costs exceed current contract authorization/funding. A multi-year framework is not the same as funded cash receipts. These facts were already known on November 5, not new scanner discoveries. [Company Q3 release](https://news.lockheedmartin.com/2026-10-22-Lockheed-Martin-Reports-Third-Quarter-2026-Financial-Results).

**Why not use $723 as an unquestioned target?** The original WACC is 6.2707%, from Treasury 4.90%, ERP 4.41%, normalized beta 0.3724, 5.75% pretax debt cost and approximately 13.6% debt weight. The raw monthly beta was just 0.0586, with standard error 0.2559 and R² 0.00094. Thus a near-zero realized market correlation is weak evidence about future economic risk. Conversely, simply imposing 9–10% WACC to reject the stock would also be arbitrary. Keeping the original inputs but testing beta 0.5/0.6 gives WACC approximately 6.76%/7.14%. These are uncertainty tests, not newly measured betas. [Published assumptions and calibration](https://github.com/FundamentalPullback/FundamentalPullback.github.io/blob/main/research/2026-11-05/LMT/assumptions.md), [model inputs](https://github.com/FundamentalPullback/FundamentalPullback.github.io/blob/main/research/2026-11-05/LMT/model/inputs.json).

| WACC | Published base operations | Moderate operating stress* |
|---:|---:|---:|
| 6.2707% | $722.90 | $603.77 |
| 6.5% | $676.00 | $564.42 |
| 7.0% | $590.23 | $492.40 |
| 7.5% | $521.52 | $434.65 |
| 8.0% | $465.24 | $387.30 |

*Growth two percentage points below the early base path, with that reduction fading during transition, and EBIT margin 50bp lower throughout, including terminal margin. This is the same published operating stress, now combined with the rate sensitivities. Reproduced from the [published model](https://github.com/FundamentalPullback/FundamentalPullback.github.io/blob/main/research/2026-11-05/LMT/model.py); no underlying business forecast or capital bridge was silently changed.

A useful working **base-operation reference is roughly $590–676**, with the original $723 retained as the more rate-sensitive central model result. This is not a confidence interval or a claim that everything outside it is implausible. Modest combined disappointments give roughly $492–564; the **actual full bear is $274, about 52% below scanner Last**, and includes slower growth, weaker margins, more reinvestment, pension/ULA risk and an 8% WACC. The $604 mild stress must not be labeled the bear.

For the user's horizon, revaluation to $590–676 over a year plus four dividends at the current $3.60 quarterly rate would illustrate about **6.3–21.3% total return**, before tax, if both revaluation and dividend continuation occurred. This is a scenario, not expected return. The lower endpoint is modest versus the risks; revaluation to $492 plus the same dividends would be around **−11%**. Do not add dividends to a DCF-derived IRR; this illustration instead uses hypothetical terminal stock prices.

The next 6–12-month evidence is contract funding, 2027 operating guidance and pension cash requirements, missile-production execution, and early Ultra integration. Exact next earnings date was not verified. A rebound can occur without a technical trigger, while a technically attractive bar would not solve funding or valuation risk. **Practical outcome: promote to portfolio-level fundamental comparison at a reasonable price, without calling it a strong buy or authorizing an entry.** Position sizing, current portfolio exposure and execution are outside this review.

Market-data caveat: current secondary histories show Nov6 close $567.08 on [MarketScreener](https://www.marketscreener.com/quote/stock/LOCKHEED-MARTIN-CORPORATI-13406/quotes/) and $567.05 on [ChartExchange](https://chartexchange.com/symbol/nyse-lmt/historical/). I retained the supplied $569.04 reference instead of silently relabeling it a close. The small difference does not alter the conclusion.

## G: improved earnings, but the reopening test has not passed

The completed October30 A121 review had base **$41.47**, adverse $19.95 and favorable $66.27 at reference $38.97. Its explicit reopening condition was better collections without greater factoring dependence, not a fixed margin-of-safety threshold. That old value is historical and **not** presented as a rebuilt post-Q3 valuation. [Prior public report archive, A121](https://github.com/FundamentalPullback/FundamentalPullback.github.io/blob/main/data/lib.js).

New Q3 revenue is $1,385.4m, +7.3%; ATS grew 30.3%, while core services were flat. GAAP operating income grew 10.1% to $211.0m, versus adjusted EPS growth of 10.3%. Full-year gross-margin and adjusted-EPS growth outlook increased; revenue guidance remains at least 7%. That is favorable business evidence. [November5 company release](https://media.genpact.com/2026-11-05-Genpact-Reports-Third-Quarter-2026-Results).

However, 9M CFO fell to **$142.0m from $526.2m**. Subtracting PPE and software gives **$62.5m versus $459.5m**; after subtracting economic SBC, the diagnostic is **−$17.3m versus $395.4m**. This is not a normalized forecast. Receivables consumed $405.8m versus $80.3m; the 10-Q attributes delayed invoicing and collections mainly to ERP implementation. Facility factoring outstanding was $53.6m, below $55.1m at December2025 and $77.1m at June2026: do not falsely claim greater quarter-end factoring propped up Q3. Other client-sponsored programs still require consideration. [Q3 10-Q, cash-flow statement and liquidity discussion](https://www.sec.gov/Archives/edgar/data/1398659/000139865926000019/g-20260930.htm).

Arithmetic from reported FY2025 and 9M2026/2025 gives TTM revenue **$5,344.2m**, EBIT **$798.0m**, CFO **$428.7m**, and strict FCF **$327.4m**. Cash pressure could reverse as the ERP problem clears, but it cannot yet be counted as available owner cash. Annualizing the weak nine-month cash number forever would be just as misleading as ignoring it. **At $42.27, retain as a collections-recovery watch, not a new bargain.** A full post-Q3 ten-year forecast, including the timing and recoverability of working capital, has not been rebuilt in this review. That is a specific remaining model task, not grounds to pretend the older fundamental review never completed.

## TDC: cash recovery is real, but adjusted figures overstate what owners retain

The completed October30 A122 FCFF model had adverse/base/favorable **$11.71/$22.50/$35.04**. Its base already assumed margin improvement and full equipment/software reinvestment. At $31.80 the old base is 29.2% below price, while even the favorable case is only 10.2% above. These remain historical scenarios, not a new DCF. [Prior public report archive, A122](https://github.com/FundamentalPullback/FundamentalPullback.github.io/blob/main/data/lib.js).

Q3 total ARR grew 1% reported/2% constant currency, cloud ARR 11%, but revenue fell 4%, recurring revenue 2%, and GAAP operating margin fell to 13.5% from14.7%. Q4 revenue is guided down4–6%. FY adjusted EPS improved to $2.86–2.90, but adjusted FCF guidance stays $330–350m. A low reported P/E is distorted by the SAP settlement; $0.70 adjusted quarterly EPS also removes SBC. [November5 release and reconciliations](https://www.sec.gov/Archives/edgar/data/816761/000162828026071034/tdc09302026exhibit991.htm).

The useful cash bridge is 9M reported FCF **$580m − $480m SAP receipts + $121m related costs + $33m settlement cash tax = $254m adjusted FCF**. Deduct **$95m SBC and $45m finance-lease payments** and the owner-cash diagnostic is **$114m**. Q3 alone is $96m − $33m − $13m = **$50m**, versus $41m comparable prior year. Thus cash improvement should not be denied, but neither should the headline $580m be capitalized. Lease-acquired assets were $39m in 9M, on top of $18m cash PPE/software. Do not also deduct those new leased assets on top of lease payments in this simple equity-cash diagnostic; a full FCFF model must consistently choose replacement capex and lease/debt treatment. [Q3 10-Q](https://www.sec.gov/Archives/edgar/data/816761/000162828026071377/tdc-20260930.htm).

**Conclusion: pass at $31.80.** No evidence here justifies enough extra growth/margin to erase the old valuation gap. A full post-Q3 DCF and complete current pension/lease bridge were not rebuilt; they are not required to force this name ahead of better candidates. Reopen if total ARR and recurring revenue establish sustained growth, with owner cash after SBC and equipment investment supporting a materially higher valuation.

## TRI: the strong print is already in the model

The [November4 completed research](https://github.com/FundamentalPullback/FundamentalPullback.github.io/blob/main/research/2026-11-04/TRI/report.md) incorporated the November3 print and Global Print separation. Its DCF is **$52.86/$92.26/$134.38**. At $112.57, base is18.0% below price and favorable19.4% above. Continued-growth valuation is possible, but it is not newly attractive simply because the screen flags a pullback.

Q3 organic revenue growth was10%; the Big3 guidance was unchanged. The $2.1bn FCF guidance includes discontinued Print and cannot be perpetuated as continuing owner cash. Capital expenditures remain8.5–9% of revenue. [Company Q3 release](https://www.sec.gov/Archives/edgar/data/1075124/000119312526444408/d65855dex991.htm).

The prior normalized work has continuing TTM FCF **$1.806bn** before subtracting economic SBC, with ~$120m SBC explicitly estimated, not verified current TTM. Its FCFF forecast already retains SBC in EBIT and pays for reinvestment. At scanner price the continuing FCF yield is only **3.69% before that economic SBC adjustment**, and adjusted TTM EPS multiple is around30.1×. **Keep waiting on price or stronger durable cash economics.** No full revaluation or new actual-SBC extraction was performed; no indication of a result newer than the already-modeled Nov3 quarter was found.

## BZ: capital-allocation issue remains; no artificial technical veto

The [November5 supplement](https://fundamentalpullback.github.io/research/2026-11-05/stocks/BZ.html) preserves the completed fundamental model at **$16.5244/ADS**, including a ~$6.27 financial-asset bridge per ADS. At $17.65 that model value is6.4% below price. This small gap alone is not a categorical rejection. The more important issue is return on, and distribution timing of, financial assets together with China/VIE and treasury-control risk.

The capital-return policy concerns at least50% of prior-year adjusted profit through **dividends plus buybacks**, subject to board/market conditions, not a guaranteed50% cash dividend or prompt release of all existing financial assets. The earlier model already subtracts the declared dividend; do not deduct it twice or add it as free value. [Q2 company release](https://ir.zhipin.com/news-releases/news-release-details/kanzhun-limited-announces-second-quarter-2026-financial-results).

Current [IR releases](https://ir.zhipin.com/news-events/news-releases) still run through the October23 board announcement, and the [event calendar](https://ir.zhipin.com/news-events/event-calendar) shows no announced Q3 date. This is a checked negative finding, not a claim that the event cannot occur soon. **Retain conditional watch.** No fresh balance-sheet mark-to-market, FX bridge or new DCF was performed. Neither $17.74 nor a short intraday candle is an investment rule; capital allocation and subsequent earnings are the meaningful 6–12-month tests.

## Exactly what is complete and what is not

- Complete: identified and reviewed relevant prior public research for all five; opened current G/TDC releases and filings; cross-checked TRI/LMT primary releases; checked BZ's current primary calendar/releases; rebuilt the stated G/TDC cash diagnostics; reproduced LMT base/bear and added combined rate/operating sensitivity; made a practical five-name fundamental prioritization.
- Not complete: five new standalone full valuation models. Specifically, G/TDC post-Q3 ten-year model rebuilds, fresh TRI actual SBC extraction, BZ current financial-asset/FX revaluation, and a refreshed LMT market beta/discount input dataset were not performed. Prior values are clearly dated above.
- LMT classification has improved based on price and reproduced sensitivity, not a newly claimed operating surprise. Remaining investor questions are economic uncertainties and portfolio selection, not a blanket statement that all research is unfinished.
- No unresolved source-access blocker prevented the stated conclusions.

Supporting arithmetic: `earnings_calculations.json` and `lmt_price_sensitivity.json` in this deliverable's directory. No purchase, position sizing, stop, technical entry trigger or publication is approved by this research.
