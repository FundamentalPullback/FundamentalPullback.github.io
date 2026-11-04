# VFC financial history and retained-perimeter normalization

As of 4 November 2026. USD millions, except EPS and ratios. Research support only: no valuation, trading decision or publication. Original issuer/SEC-hosted evidence only. No external 200-symbol comparison used.

## What can be loaded

The reported continuing-operation income and cash-flow schedules are source-linked and arithmetically reconciled. FY2024, FY2025 and FY2026 use the latest FY2026 10-K's recast comparative statements. Four latest quarters are Q3 FY2026 (27 December 2025), Q4 FY2026 (28 March 2026), Q1 FY2027 (27 June 2026) and Q2 FY2027 (26 September 2026). The current TTM is 28 September 2025 through 26 September 2026; prior TTM is 29 September 2024 through 27 September 2025. Both are 52 weeks. FY2027's additional 53rd week occurs later, in Q4, and is not yet in this TTM.

Income, GP, EBIT, NI, CFO, PPE and software capex, SBC, D&A/write-downs, each working-capital component and discontinued flows are in `history.json` and the long/wide CSVs. Annual cash taxes and interest are included. Quarter/TTM cash taxes and interest are not separately disclosed in the reviewed interim statements and are null, not invented from P&L expense.

The retained revenue/management-adjusted GP/EBIT series is in `retained_history.csv` and `retained_bridge.json`. It is not an economically certified normal-earnings series. Exact retained CFO/capex/software remain null because Dickies standalone cash flows are not disclosed. That does not itself prevent an explicitly assumption-based forecast of the future retained business; it prevents presenting historical retained cash as a reported fact.

## Three annual years

| Metric | FY2024 | FY2025 | FY2026 |
|---|---:|---:|---:|
| GAAP continuing revenue | 9,915.678 | 9,504.691 | 9,605.207 |
| Gross profit | 5,112.300 | 5,083.865 | 5,261.715 |
| GAAP EBIT | −143.935 | 303.773 | 576.569 |
| Continuing NI | −1,018.477 | 69.324 | 254.920 |
| Discontinued NI | 49.595 | −259.040 | 0 |
| Continuing diluted EPS | −2.62 | 0.18 | 0.64 |
| Continuing CFO | 884.714 | 438.489 | 671.274 |
| Cash PPE | 135.762 | 86.274 | 114.707 |
| Cash software | 61.483 | 39.749 | 51.099 |
| Strict continuing FCF | 687.469 | 312.466 | 505.468 |
| SBC | 57.829 | 73.247 | 76.954 |
| D&A and other write-downs | 307.528 | 259.616 | 280.529 |
| Cash tax paid, total operations | 349.978 | 162.562 | 171.775 |
| Cash interest paid | 175.822 | 162.918 | 145.110 |

Source: [FY2026 10-K](https://www.vfc.com/investors/financial-information/sec-filings/content/0000103379-26-000030/vfc-20260328.htm), tables 98, 100, 177 in the preserved extraction. Cash tax specifically includes continuing **and discontinued** operations (Note26 footnote a). D&A row includes other asset write-downs; do not relabel it pure recurring D&A. FY2024's 732.792 trade-working-capital cash release and tax-receivable write-off make earnings-to-cash conversion nonrepresentative.

## Four latest quarters

| Metric | Q3FY26 | Q4FY26 | Q1FY27 | Q2FY27 |
|---|---:|---:|---:|---:|
| GAAP continuing revenue | 2,875.801 | 2,166.034 | 1,669.379 | 2,695.132 |
| Gross profit | 1,628.341 | 1,221.928 | 917.044 | 1,492.678 |
| GAAP EBIT | 289.054 | 61.504 | −83.072 | 367.920 |
| Continuing NI | 300.845 | −119.282 | −97.152 | 285.251 |
| Continuing diluted EPS | 0.76 | −0.30 | −0.25 | 0.71 |
| Continuing CFO | 1,010.436 | 33.306 | −62.496 | −151.534 |
| PPE + software | 43.889 | 41.323 | 53.266 | 55.355 |
| Continuing FCF | 966.547 | −8.017 | −115.762 | −206.889 |
| SBC | 18.737 | 19.870 | 22.832 | 17.444 |
| Retained revenue | 2,820.054 | 2,166.034 | 1,669.379 | 2,695.132 |
| Retained management-adjusted EBIT | 340.997 | 53.870 | −94.548 | 363.716 |

Q3 cash = nine months less first half; Q4 = year less nine months; Q2FY27 = H1 less Q1. No seasonal quarter is annualized. Q4 EPS is directly disclosed, not calculated by subtracting EPS. Source locations for every component and derivation are in `Normalized_Financials_Long.csv`. Original [Q3FY26 10-Q](https://www.vfc.com/investors/financial-information/sec-filings/content/0000103379-26-000011/vfc-20251227.htm), [Q1FY27 10-Q](https://www.vfc.com/investors/financial-information/sec-filings/content/0000103379-26-000114/vfc-20260627.htm), [Q2FY27 10-Q](https://www.vfc.com/investors/financial-information/sec-filings/content/0000103379-26-000135/vfc-20260926.htm).

## TTM comparison

| Metric | Prior TTM | Current TTM |
|---|---:|---:|
| GAAP continuing revenue | 9,541.055 | 9,406.346 |
| GAAP gross profit | 5,149.076 | 5,259.991 |
| GAAP EBIT | 378.901 | 635.406 |
| Continuing NI | 92.199 | 369.662 |
| Continuing CFO | 367.844 | 829.712 |
| PPE + software | 134.937 | 193.833 |
| Continuing FCF | 232.907 | 635.879 |
| FCF less SBC diagnostic | 151.961 | 556.996 |
| Cash contribution from AR + inventory + AP | −128.259 | 90.917 |
| All cash working-capital changes excluding lease | −94.516 | −49.471 |
| Retained revenue | 9,014.676 | 9,350.599 |
| Retained adjusted gross profit | 4,919.713 | 5,238.730 |
| Retained adjusted EBIT | 589.561 | 664.034 |

Retained revenue rises 3.73%, adjusted gross profit 6.48% and adjusted EBIT 12.63%, mechanically. These are not constant-currency growth rates or tariff-neutral sustainable growth. The working-capital swing contributes 219.176 to trade-WC cash improvement but only 45.045 after tax, accrued and other working-capital changes. All-in cash reinvestment rises 58.896. The detailed CFO variance reconciles exactly in `cfo_variance_bridge.csv`.

## Perimeter and divestiture bridge

- **Supreme:** sold 1 October 2024. Retrospectively discontinued for income and operating cash in all annual periods used here. Certain shared corporate and segment overhead remains in continuing operations. FY2025 discontinued CFO is 26.747; FY2024 is 129.867. Total discontinued investing outflow is 4.413/13.576, respectively. Sale proceeds 1,506.223 are investing cash, not recurring FCF. The sale's final pretax loss 134.225 is in discontinued operations; its final after-tax sale loss is approximately126.6.
- **Dickies:** sold 12 November 2025, but not discontinued under GAAP. Historical continuing statements still include Dickies through sale. [Issuer's November2025 recast](https://www.vfc.com/investors/financial-information/sec-filings/content/0000103379-25-000066/vfcex992supplementalfininf.htm) and subsequent results remove its adjusted P&L, not its cash flows. FY2025 adjusted Dickies EBIT26.730; FY2026 11.235; prior TTM30.384; current TTM−7.954. Direct Q3FY26 contribution is −7.955, a one-thousand-dollar rounding difference.
- Dickies cash sale proceeds600.524 less final price adjustment11.867 paid in Q1FY27 =588.657 cash net of cash sold and the final WC adjustment, before any separately undisclosed deal tax/cost cash. Final GAAP gain127.211 is below operating EBIT and reversed from CFO. Neither proceeds nor adjustment belong in operating FCF.
- Sep2025 Dickies held-for-sale assets include AR104.972, inventory140.842, AP24.243, other current assets11.346 and accruals30.584. Core WC is221.571; extended operating WC202.333. Removing these assets/liabilities at disposal is not an operating cash release. March2025 Dickies AR116.9 and inventory134.2 are rounded disclosures, not a complete opening WC schedule.
- FY2024 retained sales can only be approximated from9915.678 continuing sales less the rounded618.4 Dickies brand sales, yielding9297.278 ±0.05. No FY2024 retained GP/adjusted EBIT has been invented.

**Source-limited Dickies cash diagnostic:** current-TTM Dickies adjusted EBIT−7.954, combined with a deliberately loose D&A upper bound18.261 (the entire All Other FY26 amount) and capex upper bound43.889 (the entire Q3 cash reinvestment), gives a conditional pre-tax, pre-WC operating-cash proxy range−51.843 to10.307. Prior TTM's equivalent loose range is−104.553 to70.316. These require nonnegative component allocations, assume all Dickies D&A is inside All Other rather than corporate allocations, and omit WC, tax, financing and restructuring cash. They are neither standalone CFO estimates nor hard FCF bounds. No narrower cash range is justified by the reviewed source disclosures; revenue-pro-rata cash allocation would be an assumption, not evidence.

## Tariffs: preserve both sides of the bridge

The FY2026 duty/refund receivable is149.7. Of this,93.8 reversed FY2026 COGS and55.9 reduced inventory. The latter reversed COGS by37.3 in Q1FY27 and18.6 in Q2FY27 as matching inventory sold. The issuer says these matched entries create no net FY2026 or FY2027 gross-margin effect for IEEPA duties. Do **not** subtract the FY2027 reserve releases once more as independent windfalls. This annual total does not reveal the retained H1FY26 timing or any cross-period Dickies allocation.

If x is retained H1FY26 net IEEPA expense later reversed in the current TTM, the conditional comparable EBIT bridge is:

- Current:664.034−x.
- Prior:589.561+x.
- Equal growth occurs at x37.2365. A deliberately broad company-gross envelope x0..93.8 produces growth+12.63%..−16.55%; it is not an estimate of x and does not impose an investment-plan growth threshold.

The complete cash identity for each period is:

**Tariff-neutral FCF = reported FCF + gross duty cash paid − gross refund cash collected − original vendor/partner concession cash benefit + vendor/partner reimbursement cash paid − refund-interest cash received.**

Then subtract the net pension termination cash benefit in the current period and the separately estimated Dickies FCF contribution in each period, if the model makes such an estimate. Vendor timing matters: the issuer recorded37.6 of reimbursement obligations (22.7 in FY26 COGS and14.9 in inventory) and still identifies37.6 payable at September2026. The original cash concessions and actual reimbursement timing are not disclosed. Refund-interest income5.6 in H1FY27 is nonrecurring, but income recognition is not exact cash-receipt evidence. Gross refunds are described as substantially all collected, not an exact amount.

The call's approximate110 net cash-refund number is the **full-year guidance bridge**, not an exact H1 received-net-cash table. The earlier simplified current535.879−p/prior232.907+p formula omits vendor, interest and Dickies terms; it is kept only as an audit illustration, not as proof of sustainable retained cash improvement.

## Pension, legal, software and ownership costs

- FY26 CFO includes125.373 pension asset reversion before the separately paid excise tax of approximately25.1. Net benefit is approximately100, consistent with the company's FCF comparator. The83.5 transferred into a qualified replacement plan is not unrestricted corporate cash.
- Q2FY27 pension premium refund3.089 was transferred into that replacement plan for incremental future401k contributions. Do not add it as excess cash while ignoring the related future contribution funding.
- FY24 tax loss largely reflects the Timberland dispute. The875.7 tax/interest cash payment occurred19 October2022, outside FY24–FY26. FY24's tax-receivable/interest write-off is a noncash CFO adjustment921.409; the net tax-expense impact is approximately690 after related effects. Do not book875.7 again as a future cash liability.
- FY24 legal settlement gains29.1 were below EBIT; cash timing is not separately established here. Current Colorado securities litigation has unspecified damages and an uncertain outcome, not an evidence-based zero or payable estimate.
- PPE and capitalized software are both deducted in strict FCF. Annual PPE/software accrued but unpaid are separately retained in the source rows and not added to cash capex again. The small historical Dickies finance lease is separate from ordinary cash capex: finance-lease principal cash663thousand/1.109m/1.079m in FY26/FY25/FY24 (10-K Note9 table120) is financing classification and should be handled consistently if the valuation includes finance-lease debt.
- SBC remains an economic ownership cost. The FCF-less-SBC diagnostic is not FCFF and does not authorize a second SBC deduction from an EBIT-based NOPAT model where SBC was never added back.
- FY26 D&A/write-downs280.529 includes charges. If EBIT is adjusted upward for the excluded write-downs/accelerated depreciation, remove matching noncash additions from adjusted D&A to prevent double counting. Note27 separately reports Reinvent asset write-down2.170, accelerated depreciation0.322 and other restructuring accelerated depreciation0.455. The complete pure recurring D&A carve-out is not separately disclosed.

## Audit and remaining limits

`Validation_Checks.json`:120 performed checks, all passed. `Bridge_Validation_Checks.json`:14 performed bridge checks, all passed, with the disclosed0.001 retained-EBIT presentation difference. `QA_Flags.json` logs material comparability limits. There is no claim of independent human audit.

All11 raw HTML documents, table extracts, source URLs and SHA256 hashes are retained. `build_history.py` and `build_bridges.py` reproduce the schedules. FY2024 release raw evidence was reused from the prior primary-source collection, then parsed/verified again; the remaining central filings/releases were refreshed. Nothing from the unavailable cash disaggregation is silently filled with zero or a narrow estimate.


## Prospective model handoff supplement

`model_inputs_supplement.json` adds the principal-versus-carrying debt bridge, clean post-sale D&A/SBC/reinvestment anchors and pension treatment. March principal3540.905 minus discount10.094 and issuance cost10.941 reconciles to reported long-term carrying3519.870. September exact debt-cost split is not disclosed. Using documented unchanged note principals and the [Fed25September reference of1.1400USD/EUR](https://www.federalreserve.gov/releases/h10/20260928/), estimated total financial principal is3558.123 versus carrying3538.589; estimated principal net debt3115.172. The difference19.534 is not an audited September discount/cost split.

Clean H1FY27 post-sale D&A116.143, SBC40.276 and cash PPE/software108.621 are preferable forecast anchors to a fictitious historical Dickies carve-out. H1x2 quantities232.286/80.552/217.242 are magnitude references only. Net pension deficit77.265 remains the last measured balance at March2026; if deducted debt-like in the equity bridge, avoid deducting the same legacy deficit funding again in FCFF. Keep ordinary service cost in EBIT and keep replacement-plan assets outside unrestricted cash.
