# IRDM peer comparison support

Valuation date: November 3, 2026 closing prices. Research cutoff November 4, 2026. USD millions except share prices. **Screening-only, not a median-derived target.**

## Read-through

Viasat is a useful secondary capital-intensity comparison, not an equivalent business. Its June-2026 TTM revenue is $4,625.769m and GAAP EBIT $108.761m (2.35% margin). At $75.24 and 137.755810m last-disclosed actual shares, equity value is $10,364.747m. Adding $6,570.503m principal debt including finance leases and $77.839m book NCI, and subtracting $1,735.819m cash, gives **screening EV $15,277.270m: 3.30x revenue, 140.47x GAAP EBIT, 10.64x unadjusted EBITDA**. The last figure is EBIT plus cash-flow depreciation/amortization, not management Adjusted EBITDA. Do not compare it directly with IRDM OEBITDA.

Viasat reported CFO less cash capex is $578.286m, or 5.58% of this equity value. However, it includes a $420m October-2025 Ligado lump-sum receipt. Simple subtraction reduces that cash-flow proxy to $158.286m (1.53% equity yield), or $67.732m after subtracting reported SBC. This is an analytical sensitivity, **not a fully tax- and working-capital-normalized owner-earnings measure**. Keep ordinary recurring Ligado payments; do not strip the entire arrangement.

A low price/revenue ratio relative to IRDM does not establish cheapness: Viasat's depreciation, leverage, acquisition amortization, satellite construction cycle, and service/equipment mix differ. Its TTM cash capex is 21.91% of revenue. Using a peer multiple without reconciling these economics can manufacture an IRDM target rather than inform one. IRDM's own low current replacement spending cannot be assumed permanent either.

Gilat is included only as a **partial six-month operating comparison**: revenue $233.137m, GAAP EBIT $9.078m (3.89% margin), CFO -$14.085m, cash capex $4.175m (1.79% of revenue), SBC $10.402m and CFO less capex -$18.260m. It is primarily ground technology/equipment, defense and network services rather than an owned global replacement-satellite fleet. Its lower capex is not a valid maintenance-capex assumption for IRDM.

## EV conventions and remaining limits

- VSAT price: $75.24 November 3 close, agreed by StockAnalysis and YCharts. These are **secondary market-data sources**, not an exchange-certified primary-price record. Discard November 4 intraday quotes.
- VSAT shares: 137,755,810 actual shares at July 23, from the June 10-Q cover. Not EPS weighted-average shares. Later option/RSU activity is unmodeled.
- VSAT debt/cash/NCI: June 30, the latest quarter available before its scheduled November 5 after-close results. This is a current-price/latest-reported-balance-sheet screen, not a November 3 balance sheet. No claim is made that cash/debt were unchanged thereafter.
- Debt includes finance leases ($142.678m) once. Operating leases are excluded consistently from this EV. NCI uses book value as a disclosed proxy, not fair value. Other financial investments are not revalued or deducted. Hence EV is explicitly screening-only.
- VSAT GAAP EBIT includes acquired-intangible amortization. Its unadjusted EBITDA is economically incomplete because it adds back the depreciation of assets that eventually need replacement. Cash capex includes purchases of property, equipment, satellites and other assets, including capitalized costs under the company's presentation; finance-lease principal is not separately deducted in the displayed CFO-capex proxy.
- VSAT CFO-SBC uses reported expensed SBC only; capitalized SBC and other stock-settled employee liabilities can impose further dilution. This is not a diluted per-share valuation.
- GILT June cash $144.805m and deposits $14.350m predate a $100m convertible issuance completed September 7. Restricted cash $0.064m is not free cash. No EV is presented because a current actual-share count and comprehensive post-financing bridge were not reconciled. Six-month EPS weighted shares are explicitly not used for EV.
- GILT's pending Comtech satellite/space acquisition changes future business mix and financing; quarter results said expected year-end close. The next results were scheduled November 10. Do not combine pro-forma revenue with pre-deal EV.
- No SES multiple is supplied because a reconciled post-transaction EV/denominator was not established in this pass. No peer median, discount/premium target, or unjustified forward estimates are supplied.
- GSAT/Amazon and IRDM/Rocket Lab transaction effects are treated in the parent transaction analysis, not asserted or quantified independently here. An event-driven price should not be read mechanically as a standalone trading multiple.

## Sources and reproduction

`inputs.json` contains only the small factual dataset, dates, locators and source URLs. `reproduce.py` uses Python's standard library, works offline, and regenerates `calculated.json` via FY plus current quarter minus prior-year quarter. Command: `python reproduce.py`.

VSAT primary financial sources:
- [June 2026 Form 10-Q](https://investors.viasat.com/static-files/a848547d-28e1-483a-80e9-b766e518cff0): cover shares; printed pp.3-5 statements; printed p.22 Note 6 debt.
- [March 2026 Form 10-K](https://investors.viasat.com/static-files/e88eca72-2893-4380-81b5-54afa107a46d): printed F-4/F-5 financials; printed pp.57-58 and F-52 for Ligado receipt; F-10 capitalized interest.
- [Next results date](https://investors.viasat.com/node/28241/pdf).
- Secondary price checks: [StockAnalysis](https://stockanalysis.com/stocks/vsat/history/), [YCharts](https://ycharts.com/companies/VSAT/price).

GILT primary sources:
- [June 2026 results and financial tables](https://www.gilat.com/wp-content/uploads/Gilat-PR-2026-08-05-Financial-Q2-Results-Accessible.pdf): PDF pp.8-14.
- [September convertible closing 6-K](https://www.sec.gov/Archives/edgar/data/897322/000117891326004427/zk2636044.htm).
- [Quarter release and pending acquisition context](https://www.gilat.com/newsroom/press-releases/gilat-reports-second-quarter-2026-results/).

Full third-party filings are linked, not copied into this deliverable folder. Small factual inputs and our arithmetic are the reproducible evidence package. Numerical QA assertions pass for VSAT TTM revenue, EBIT and CFO-capex. Primary HTML retrieval initially returned 403; the issuer's linked public PDF copies succeeded. No action was denied and no external state changed.
