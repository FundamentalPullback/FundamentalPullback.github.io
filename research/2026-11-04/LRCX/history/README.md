# LRCX financial history and normalization

As of 2026-11-04. All numeric JSON/CSV currency values are USD, not USD millions; shares are units; EPS is USD/share. Report dates are fiscal period ends. Filings were retrieved from SEC on 2026-11-04. Source URLs and filing dates are in source_facts.json. This is a factual history, not a recommendation or price-target model.

## Reproduce and inspect

- `python build_history.py` works offline with Python standard library, source_facts.json and supplemental_facts.json. Generates history.json, history.csv, checks.json.
- 64 checks pass: pretax less tax equals NI; diluted EPS rounding; annual quarter aggregation; both TTM flow identities.
- The factual extracts retain source URLs, XBRL tags and context IDs. Full third-party filings are not included; offline reproduction uses only the supplied factual inputs.
- Source selection prefers the latest filing's comparative for each exact metric/period. Every reported metric retains source ID, context ID and XBRL tag. Derived values retain the arithmetic method and input references.

## Financial conclusion

USD millions, FY24 / FY25 / FY26:
- Revenue: 14,905.386 / 18,435.591 / 23,232.690.
- EBIT: 4,263.913 / 5,900.968 / 8,199.795.
- NI: 3,827.772 / 5,358.217 / 7,265.396.
- CFO: 4,652.269 / 6,173.264 / 5,857.657.
- Cash capex including intangible assets: 396.670 / 759.186 / 966.405.
- SBC expense: 293.058 / 343.371 / 386.381.
- CFO less capex less SBC expense: 3,962.541 / 5,070.707 / 4,504.871.

TTM to 2026-09-27 versus TTM to 2025-09-28:
- Revenue 26,127.935 vs 19,591.788 (+33.36%); EBIT 9,654.434 vs 6,465.859 (+49.31%); NI 8,449.874 vs 5,810.433 (+45.43%).
- CFO 7,576.345 vs 6,383.757 (+18.68%); cash capex 1,038.981 vs 833.719; SBC 403.836 vs 360.601.
- FCF after SBC expense 6,133.528 vs 5,189.437 (+18.19%). Earnings growth materially exceeds cash growth. This metric is an analytical owner-cash proxy, not GAAP FCF or FCFF.
- FY26 CFO weakness was real, not erased by the strong latest quarter. Latest Q1 CFO 3,497.652 includes a positive 535.413 change in operating assets/liabilities. Annualizing that quarter would overstate a clean cash run rate without normalizing working capital and taxes.

## Normalization decisions and hard limits

1. SBC is a cost. EBIT and NI already include it; do not subtract SBC again from these earnings. CFO adds SBC back, so the analytical after-SBC FCF deducts reported SBC expense once. Capitalized SBC is **null**, not zero. Exact total economic SBC cannot be claimed without that disclosure.
2. Cash-flow capex is reported as capital expenditures **and intangible assets**, a positive outflow in this package. Physical gross capex and software gross capex individually are **null**. Do not call the whole total physical capex, net it against disposal proceeds, or add an invented software estimate. This cash-flow aggregate is not gross accrual additions: FY26 separately discloses $119.605m accrued capital payables and $125.691m inventory transfers to PPE; latest Q1 $141.965m and $37.053m. Neither noncash item should simply be added to cash capex as if it were an incremental cash outflow. Grant policy reduces asset cost basis; a full gross-before-grants capex reconciliation is not supplied here.
3. D&A FY24/FY25/FY26: $359.699m/$386.277m/$441.533m. Depreciation: $299.0m/$329.5m/$383.9m, rounded to $0.1m. Residual D&A less depreciation: $60.699m/$56.777m/$57.633m, with approximately $0.05m rounding uncertainty. This residual is **not** an exact acquired-intangible amortization figure. Annual filing describes intangible impact on operations, including amortization/impairment, as not material, not zero. Finance-lease amortization is included in depreciation. Quarterly depreciation and total intangible amortization remain **null**; the residual must not be added to earnings as an exact adjustment.
4. FY2024 contains 53 weeks; FY2025 and FY2026 have 52. Both TTMs and each latest quarter have 52/13 weeks. No mechanical weekly revenue adjustment is asserted as reported economics.
5. The 10:1 common-stock split was effected 2024-10-02. FY2025 and FY2026 comparative shares/EPS are retroactively adjusted. The final history always uses those split-adjusted comparatives, not original FY2024 per-share data. Do not apply the split twice.
6. Q4 income/cash metrics use FY less nine months when not directly reported. Implied Q4 weighted shares use 4*FY average minus 3*nine-month average; each period has equal 13-week quarters. Q4 EPS is NI/implied average shares and can differ from the independently rounded published quarter EPS by rounding. TTM EPS uses TTM NI / annual-plus-quarter weighted average shares, not a sum of rounded EPS.
7. Tax: effective rates are calculated from reported tax and pretax income. FY2025 includes releases from statutes expiring; FY2026 reflects full global minimum tax, geography and SBC excess tax benefits. Latest Q1 ETR is 16.9% versus 15.6% a year before. The 17% NI sensitivity is **an analyst assumption**, not a company normalized result or guidance. No tax one-off is removed without an attributable amount and sign.
8. No restructuring, FX, investment income or other normal recurring expense is silently added back. The primary EBIT/NI series remains GAAP.

## Supplemental debt boundary

FY2026 note 14 reports senior notes at par $3,750m, unamortized discount $23.854m, bond issuance costs $4.232m, other financing $0.147m, and total debt carrying value $3,722.061m. Balance-sheet debt plus finance leases is $3,734.563m, implying finance leases $12.502m at **2026-06-28**. As of **2026-09-27**, balance debt plus finance leases is $3,735.444m. Separate Q1 finance-lease liability and debt discounts are not disclosed in the inspected Q1 XBRL. The difference between par and balance debt is not a valid lease estimate. Neither June's lease amount nor June's discounts should be labelled exact September data.

## Principal source links

- FY2026 10-K, filed 2026-08-07, annual statements and notes 2, 5, 7, 11, 12, 14 and 15: https://www.sec.gov/Archives/edgar/data/707549/000070754926000037/lrcx-20260628.htm
- Q1FY2027 10-Q, filed 2026-10-22, statements and notes 4, 6 and 10: https://www.sec.gov/Archives/edgar/data/707549/000070754926000054/lrcx-20260927.htm
- FY2025 10-K, filed 2025-08-11, split retrospective adjustment: https://www.sec.gov/Archives/edgar/data/707549/000070754925000075/lrcx-20250629.htm
- All intermediate-quarter SEC URLs and filing dates are embedded in source_facts.json.

## Earnings-release supplement verified 2026-11-04

The [2026-10-21 earnings release](https://investor.lamresearch.com/2026-10-21-Lam-Research-Corporation-Reports-Financial-Results-for-the-Quarter-Ended-September-27,-2026) separately reports acquired-intangible amortization of $2.668m in COGS plus $0.348m in SG&A, total $3.016m, for both Q4FY26 and Q1FY27. `amortization_acquired` and `ebit_before_acquired_amortization` are populated only for those confirmed quarters; remaining periods are null. This acquired component is **not** total amortization. Latest Q1 EBIT before this sole adjustment is $3,286.743m; four times is $13,146.972m, a run-rate scenario, not a TTM or forecast. SBC and EDC are not removed. Q4 diluted shares/EPS are also confirmed directly by the release ($1.81 and 1,256.032m shares), superseding their arithmetic reconstruction. Supplemental facts carry a separate source ID and release URL.
