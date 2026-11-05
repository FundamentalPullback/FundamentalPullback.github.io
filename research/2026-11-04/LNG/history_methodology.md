# LNG historical earnings and cash normalization review

Review date: 2026-11-05. Units: USD millions unless specified. Historical reconstruction and specific normalization adjustments; not a completed valuation.

## Conclusions

1. Existing FY2023–FY2025, last-four-quarter and TTM GAAP history arithmetic is sound. Q4 is FY minus nine months; Q2/Q3 cash-flow data are successive YTD differences; TTM is FY minus prior YTD plus current YTD. EPS is correctly not derived by subtracting periods with different share bases. `history_extended.csv` adds actual NCI distributions, net cash taxes and cash interest, with tagged primary-source observations in `observations.json` and reproducible calculations in `reproduce.py`.
2. Existing signs for fair-value and NPNS adjustments are correct. However, the limited earnings bridge still contains the $370 historical alternative-fuel excise-tax credit recognized in Q1 2026. Remove this separately before interpreting 9M growth as recurring operating growth.
3. Issuer DCF, consolidated CFO minus net PPE cash expenditure, residual cash after actual NCI distributions, parent owner FCF and FCFF are different measures. None should be relabeled as another.
4. The source discrepancy for 9M2025 adjusted NI is real: release says $1,883 and arithmetic supports it; slide 11 visually says $1,833. Use the fully reconciled release figure with a discrepancy footnote, not a silent overwrite.
5. Historical GAAP and cash history is established. Fully normalized 3-year/4-quarter earnings, recurring owner FCF, and FCFF are NOT established. Historical issuer non-GAAP reconciliations for all older periods are not in the source set. Fair-value removal does not resolve all contract economics, settlements, temporary margins, taxes, working capital, maintenance requirements, cash-settled compensation or ownership allocation.

## Earnings bridge with exact signs

Source: October 29, 2026 earnings release, “Reconciliation of Non-GAAP Measures,” tables “Consolidated Adjusted EBITDA” and “Adjusted Net Income.” URL in source register below.

| Metric | Q3 2026 | Q3 2025 | 9M2026 | 9M2025 |
|---|---:|---:|---:|---:|
| GAAP operating income | 1,915 | 1,817 | 2,717 | 5,308 |
| Add issuer loss/(gain) before delivery/termination | (432) | (574) | 2,077 | (1,491) |
| Add deferred NPNS amortization adjustment | (26) | 0 | (31) | 0 |
| Limited EBIT excluding these two accounting items | 1,457 | 1,243 | 4,763 | 3,817 |
| Add D&A | 393 | 338 | 1,146 | 979 |
| Add issuer noncash compensation adjustment | 50 | 27 | 128 | 99 |
| Add other issuer operating adjustment | 0 | 0 | 0 | 1 |
| Issuer adjusted EBITDA | 1,900 | 1,608 | 6,037 | 4,896 |
| Less historical excise credit | 0 | 0 | (370) | 0 |
| EBITDA after this additional specific exclusion | 1,900 | 1,608 | 5,667 | 4,896 |
| EBIT after accounting items and historical credit | 1,457 | 1,243 | 4,393 | 3,817 |

The $432/$574 gains increase GAAP operating income, so must be SUBTRACTED. The $2,077 loss reduces GAAP operating income, so must be ADDED. The NPNS amortization is a net reduction to cost of sales (earnings benefit) in these periods, so must also be SUBTRACTED. D&A here is the separate operating expense, not the deferred NPNS amortization.

9M limited EBIT growth is 24.8% before excluding the historical credit, versus 15.1% after that exclusion. Issuer EBITDA growth is 23.3%, versus 15.7% after the credit exclusion. These are specific adjustments, not proof of sustainable earnings.

Adjusted NI bridges:
- Q3 2026: 1,170 − 432 − 26 + 21 tax + 17 NCI = 750.
- Q3 2025: 1,049 − 574 + 124 tax − 8 NCI = 591.
- 9M2026: 736 + 2,077 − 31 − 357 tax − 37 NCI = 2,388.
- 9M2025: 3,028 − 1,491 + 295 tax + 51 NCI = 1,883.

Do not subtract $370 directly from parent adjusted NI as an after-tax, after-NCI adjustment without determining its appropriate tax and ownership effects. The issuer calculates tax effects of the mark/NPNS adjustments on a with-and-without basis, not using a single flat percentage.

## Historical-credit and tax cash effects

2025 10-K pp47–48, Liquidity and Capital Resources, states:
- Alternative-fuel excise claims totaled $370 for 2018–2024, before the program expired December 31, 2024.
- Claims were NOT recognized at December 31, 2025 because realizability was uncertain.
- Subsequent to December 31, 2025, IRS issued a closing letter confirming eligibility and “issuing final cash payment.”
- The company would recognize a $370 reduction to cost of sales in Q1 2026.
Q1 2026 MD&A confirms recognition, and Q3 2026 10-Q pp34–35 confirms the $370 first-quarter benefit in 9M results. The 10-K was filed in February 2026, placing the described final payment in Q1, rather than 2025. There is no separately labeled $370 cash-flow-statement line; treating the payment as a Q1 operating cash benefit follows the primary disclosure and operating-cost classification. Do not confuse this excise-tax receipt with the income-tax supplemental cash line.

2025 10-K p50, Operating Cash Flows, and Note 14 p91 separately identify a $380 refund of previously paid CAMT received December 2025. That refund is in Q4 2025 and TTM September 2026 CFO, not 9M2026 CFO. Removing it only from the current 9M period would be a date error.

Specific cash sensitivities, not normalized FCF:
- TTM CFO less net PPE = 7,179 − 3,392 = 3,787.
- Remove December CAMT receipt only: 3,407.
- Remove CAMT380 and Q1 historical excise receipt370: 3,037.
- Further subtract actual NCI distributions797: 2,240.
- Further subtract total CFO-statement SBC211 as a deliberately conservative sensitivity: 2,029, NOT a validated equity-compensation or owner-FCF estimate.
- 9M2026 CFO less net PPE = 2,476; after historical excise receipt370 = 2,106; after actual NCI594 = 1,512. The CAMT380 refund does not belong in this 9M calculation.

Net income taxes paid: FY2023 117; FY2024 (92); FY2025 32; Q4 2025 (383); 9M2026 36; TTM September2026 (347). Negative means net refunds. TTM refunds are not a sustainable negative tax rate.

Tax normalization requires separate parent/CQP taxable income, FDDEI eligibility, NOL utilization, accelerated depreciation, capital spending and cash payment timing. 2025 10-K Note14 reports $1.2bn federal and $2.2bn state NOLs and explains bonus depreciation deferred current taxes; 2026 Q3 Note12 p23 reports GAAP ETR10.2% quarter and10.1% YTD vs18.9%/18.0% prior. CQP income partially not taxable to Cheniere and increased FDDEI deduction explain the rate. Do not apply 10.1%, 14% FDDEI qualifying-sales rate, or 21% federal statutory rate blindly to consolidated operating profit.

## Cash-flow bridge and limits

Q3 10-Q p7 Consolidated Statements of Cash Flows: 9M2026 CFO5,124 ties by summing every reported adjustment/working-capital line. Derivative adjustment3,015 and cash settlements(659) are NOT the same measure as the issuer pre-delivery fair-value adjustment2,077. Using the CFO derivative row as an EBIT mark reversal would conflate realized/settled and mark components.

9M2026:
- CFO 5,124 − cash PPE net commissioning2,648 = 2,476.
- Less actual NCI distributions594 = 1,882.
- Less CFO-statement total SBC190 sensitivity = 1,692.
- Net PPE2,648 includes commissioning receipts115, so gross cash PPE before those receipts is2,763. Removing receipts from capital spending without separately retaining the economic inflow distorts the consolidated cash calculation.
- Redemption of redeemable NCI136 is an acquisition/ownership cash use, separate from distributions; if measuring residual cash after this transaction, deduct separately. It is not recurring NCI DCF.
- Capitalized interest138 is outside CFO net interest payment664; preserve consistency if converting to unlevered cash flow. Adding cash interest back without considering capitalized interest, tax shield and lease treatment is not a complete FCFF bridge.
- Unpaid PPE178, finance-lease additions545 and lease principal obligations mean CFO minus cash PPE alone does not measure the full economic investment burden.

TTM actual-NCI cash residual 2,990 is not parent owner FCF: cash retained within subsidiaries, economic NCI claims rather than paid distributions, maintenance vs growth spending, future tax payments, financing leases, ongoing compensation and working capital must still be resolved. All-growth-capex deductions depress near-term cash residual but do not automatically imply poor steady-state profitability; maintenance-only issuer DCF can overstate immediately distributable cash while construction remains committed.

## Issuer DCF reconciliation and classification

Release table “Consolidated Adjusted EBITDA and Distributable Cash Flow,” amounts rounded in billions:
9M6.04 EBITDA −0.72 interest −0.09 maintenance capex −0.20 current-tax measure −0.10 other =4.93 consolidated DCF; minus0.86 NCI economic DCF =4.07 Cheniere DCF. Q3:1.90−0.24−0.03−0.10−0.04=1.49; minus0.26=1.23. Rounding warning applies.

The $860 NCI DCF allocation is not the $594 actual NCI distributions. The issuer assumes100% distribution and applies economic ownership plus IDRs. Its tax deduction200 is not cash income taxes paid36. Maintenance capex90 is not all cash PPE2,648. It is after interest and therefore not FCFF. It excludes growth capex and therefore is not all-in cash available to stockholders. Issuer guidance and DCF should retain their exact label.

## Compensation

Q3 release issuer EBITDA noncash addback is50 quarter/128 YTD vs CFO-statement SBC75/190. Prior quarter27 vs35; prior YTD99 vs140. The differences are25/62 and8/41, respectively. Do not replace one with the other without reconciliation.

2025 10-K Note15 pp92–93 shows total SBC expense161/215/250 in FY2025/2024/2023 and cash paid on liability-classified awards108/109/84. Equity and liability awards, cash-settlement options, timing, remeasurement, capitalized awards and modifications all matter. The CFO SBC row is total expense adjusted in the cash reconciliation; it is not an assertion that all compensation is ultimately noncash or dilutive. Subtracting that entire row again from CFO can penalize already cash-settled compensation as well, depending on settlements embedded elsewhere. Existing “less SBC” columns should be sensitivities only, never declared true owner FCF. Proper owner treatment needs equity-only economic cost plus cash-liability-award treatment without double counting.

## NPNS and remaining uncertainty

Q3 10-Q Note1 pp8–9: June2026 designation covered73% of fixed minimum contractual IPM volumes, not73% of all business risk. Remaining27% upstream-delivery contracts stay outside designation. Deferred basis amortizes with deliveries, not linearly; failure to qualify can reinstate fair-value recognition. NPNS removes mark-to-market recognition for qualifying contracts, not commodity exposure or contractual obligations. The $349 net balance at designation and $313 net balance at quarter-end are not cash or distributable assets. Keep historical comparisons qualified across this accounting-policy transition.

## Source register and reproduction

- FY2025 SEC 10-K: https://www.sec.gov/Archives/edgar/data/3570/000000357026000005/lng-20251231.htm . Cash-flow statement p62; historical tax tables Note14 pp88–92; compensation Note15 pp92–93; historical-credit narrative pp47–48; CAMT p50/p91.
- Q3 2026 SEC 10-Q: https://www.sec.gov/Archives/edgar/data/3570/000000357026000038/lng-20260930.htm . Cash-flow statement p7; NPNS Note1 pp8–9; income tax Note12 p23; historical excise benefit MD&A pp34–35; CFO commentary p39; supplemental cash-flow note.
- Q2 2026 SEC 10-Q: https://www.sec.gov/Archives/edgar/data/3570/000000357026000028/lng-20260630.htm . Consolidated Statements of Cash Flows and supplemental cash-flow note; direct tagged observations provide exact context IDs.
- Q1 2026 SEC 10-Q: https://www.sec.gov/Archives/edgar/data/3570/000000357026000014/lng-20260331.htm . Consolidated Statements of Cash Flows p6; MD&A Results of Operations historical credit; Note16 p23 supplemental cash-flow information.
- Q3 2025 SEC 10-Q: https://www.sec.gov/Archives/edgar/data/3570/000000357025000107/lng-20250930.htm . Consolidated Statements of Cash Flows and quarterly equity distribution rows.
- October29 2026 release: https://lngir.cheniere.com/news-events/press-releases/detail/349/cheniere-reports-third-quarter-2026-results-raises-full . Unpaginated primary HTML, exact table titles specified above.
- Q3 slide deck: https://lngir.cheniere.com/_assets/_c825fb77538e72bc5ef0338780618c98/cheniere/db/778/7578/pdf/10_29_2026_3Q_2026_Earnings_Presentation_vF.pdf . Slide11 visually checked; stored rendering `slide11.png` establishes genuine1,833/1,883 discrepancy.

Run `python history_review/reproduce.py` from the project root. Existing history and selected source-tagged observations are offline inputs; those observations were checked against inline XBRL. NCI YTD missing from a chosen tag is reconstructed from same-source quarterly equity distribution rows, checked against financing cash-flow table totals (6M394;9M594 current;6M400/9M600 prior;9M2024 648). The support archive reproduces the calculations from selected source-tagged numerical observations; full filings are linked rather than redistributed.
