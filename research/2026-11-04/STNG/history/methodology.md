# STNG financial-history reconstruction

As of 4 November 2026. USD millions unless indicated; weighted share counts are actual shares, EPS is USD/share, daily TCE is USD/day. Expenses and cash capex are positive magnitudes; vessel-sale gains/losses and cash-flow changes retain signs.

## Reproduce

Run `python build_history.py` in this folder. Python standard library only, offline. The script reads `selected_inputs.json`, containing selected numerical facts with original row labels and source IDs, and regenerates `normalized_history.json` and `summary.csv`. Source IDs resolve to verified primary filing/release URLs in both JSON files. No full filings or private raw transcripts are included here.

## Coverage and basis

- FY2023–25: FY2025 audited 20-F consolidated statements and financial-expense note. FY2020–22 cyclic extension: FY2022 audited 20-F comparatives.
- Q4 2025 income/EPS: directly reported Q4 release, not subtraction of annual EPS. Q1–Q3 2026 income/EPS: directly reported quarterly releases.
- Q4 cash flows = FY2025 minus 9M2025; Q2 cash flows = H1 2026 minus Q1 2026; Q3 cash flows = 9M2026 minus H1 2026.
- Current TTM = FY2025 + 9M2026 − 9M2025, covering October 2025–September 2026. Prior TTM = FY2024 + 9M2025 − 9M2024, covering October 2024–September 2025. Source provenance is retained per field.
- TCE revenue = vessel revenue minus voyage expenses. Daily TCE is taken directly from reported operating data, not averaged across quarters. Average fleet count is not a period-end fleet count.
- D&A combines vessel/drydock depreciation with right-of-use vessel depreciation for historical periods. Financing-fee amortization stays in financial expenses, not operating D&A.
- EBIT ex vessel gains = operating income minus reported signed gain/loss on vessel sales. This is a narrow bridge, not management adjusted earnings: FY2020 vessel/goodwill impairment, FY2022 impairment reversal and FY2023 scrubber write-off remain in it.
- Financial expense is broader than interest expense. The separate FY2020–25 interest-expense note is included. Quarterly financial income/expense is retained under its reported label and is not represented as pure cash interest.
- EPS is not additive. Reported basic/diluted EPS and weighted shares are preserved by quarter/year. TTM basic shares are day-weighted from FY/9M share counts (FY2024 366 days and 9M2024 274 days; other FYs 365 and 9M 273); TTM basic EPS is calculated NI/basic shares, not company-reported. TTM diluted EPS and diluted shares are intentionally null because the if-converted numerator and anti-dilution test must be reassessed over the full TTM. In Q3 2026 the convertible was anti-dilutive, but in 9M2026 it was dilutive; simply adding quarterly EPS or dividing NI by a mechanically averaged diluted denominator is invalid.

## Key reconstruction

| Period | Revenue | Reported EBIT | Vessel gains/(losses) | EBIT ex vessel gains | NI | CFO | Drydock/other capex | Acquisition/construction capex |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| FY2020 | 915.892 | 245.334 | 0.000 | 245.334 | 94.124 | 419.381 | 174.477 | 0.000 |
| FY2021 | 540.786 | -90.508 | 0.000 | -90.508 | -234.435 | 73.300 | 47.102 | 0.000 |
| FY2022 | 1,562.873 | 797.706 | -66.486 | 864.192 | 637.251 | 769.333 | 34.480 | 0.000 |
| FY2023 | 1,341.222 | 705.150 | 12.019 | 693.131 | 546.898 | 865.492 | 23.089 | 0.000 |
| FY2024 | 1,243.951 | 764.603 | 176.537 | 588.066 | 668.774 | 825.180 | 93.367 | 0.000 |
| FY2025 | 938.222 | 355.184 | 45.486 | 309.698 | 344.292 | 491.226 | 74.383 | 0.000 |
| Q4 2025 | 252.652 | 133.055 | 45.486 | 87.569 | 128.118 | 164.775 | 9.220 | 0.000 |
| Q1 2026 | 312.860 | 219.515 | 65.930 | 153.585 | 216.264 | 163.158 | 8.128 | 68.735 |
| Q2 2026 | 408.734 | 398.328 | 154.149 | 244.179 | 387.536 | 320.341 | 4.076 | 20.662 |
| Q3 2026 | 266.467 | 269.100 | 152.550 | 116.550 | 224.316 | 185.024 | 6.012 | 92.791 |
| TTM Sep2025 | 889.539 | 316.958 | 52.576 | 264.382 | 284.731 | 439.689 | 104.206 | 0.000 |
| TTM Sep2026 | 1,240.713 | 1,019.998 | 418.115 | 601.883 | 956.234 | 833.298 | 27.436 | 182.188 |

## Cash and cycle diagnostics

- TTM2026 CFO $833.298m includes a $4.653m net working-capital cash benefit, versus a $26.841m use in prior TTM. CFO before working-capital changes is $828.645m vs $466.530m. This improvement is not principally a working-capital release.
- TTM2026 SBC is $75.592m vs $69.679m prior TTM. CFO less drydock/other capex is $805.862m; less reported acquisition/construction capex as well is $623.674m. Deducting SBC again as an economic dilution charge gives $548.082m. These are analyst cash diagnostics, not IFRS line items and not sustainable owner earnings.
- 9M2026 vessel disposal proceeds of $1,025.010m are investing inflows, distinct from $372.629m accounting gains and $668.523m CFO. Cash also reflects $628.575m convertible issuance proceeds and financing outflows. Ending September cash is $2,042.088m, not all operating cash generation.
- Daily fleet TCE: Q4 2025 $28,066; Q1 2026 $37,697; Q2 $52,661; Q3 $37,508. Average fleet: 96.5, 91.0, 84.5, 75.1 respectively. Q3 EBIT excluding gains dropped to $116.550m from Q2 $244.179m as rates and earning fleet changed; do not annualize Q2 or TTM without fleet/rate normalization.
- Cyclic context matters: FY2021 EBIT was negative $90.508m, versus FY2022 $864.192m excluding sale losses. Historical trough/peak cash flow also reflects changing fleet size, financial leverage, working capital and drydock timing, not a constant-asset business.

## Limits and checks

Drydock/other capex bundles drydock, scrubbers, ballast-water treatment and other vessel-related spending as reported. It is not a pure maintenance measure. Zero acquisition capex means no separately reported vessel acquisition/construction investing cash flow; it does not mean no fleet investment. Lease-financed vessel purchases, lease principal, and changes from lease financing to conventional debt can appear in financing rather than investing cash flows. Newbuild obligations, economic replacement reserves, equity/JV investments and future fleet reinvestment are not deducted by the displayed capex diagnostic.

Financial income can contain more than bank-deposit interest. Historical financial expenses can include extinguishment costs, fees and accretion. Net income is exposed to asset-disposal gains and, in 2026, convertible fair-value changes; EBIT ex vessel gains is the cleanest bridge delivered here, but still requires cycle normalization for valuation.

The build asserts operating-income component reconciliations, cash-flow statement reconciliations and agreement of the four latest quarters with current TTM for revenue, EBIT, NI, CFO, SBC and drydock capex, permitting at most $0.002m source rounding. Every check passes. Full statements remain in the private source folder; selected facts and calculation code are sufficient to reproduce the derived history offline.
