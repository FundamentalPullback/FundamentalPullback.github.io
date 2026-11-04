# LSCC historical financial ledger
As of November 4, 2026. USD millions except diluted EPS. GAAP reported, not management-adjusted.

| Period | Weeks | revenue | ebit | net_income | eps_diluted | cfo | capex | software_ip_cash | fcf | cash_after_ppe_software_ip | sbc | da | tax_expense |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| FY2023 | 52.0 | 737.154 | 212.270 | 259.061 | 1.850 | 269.588 | 20.098 | 13.152 | 249.490 | 236.338 | 70.197 | 34.432 | -44.205 |
| FY2024 | 52.0 | 509.401 | 34.457 | 61.131 | 0.440 | 140.876 | 20.985 | 16.708 | 119.891 | 103.183 | 52.985 | 38.737 | -24.902 |
| FY2025 | 53.0 | 523.262 | 11.232 | 3.084 | 0.020 | 175.107 | 42.527 | 19.781 | 132.580 | 112.799 | 115.613 | 35.481 | 10.293 |
| Q4FY2024 | 13 | 117.419 | -12.209 | 16.514 | 0.120 | 45.421 | 5.754 | 4.216 | 39.667 | 35.451 | 14.674 | 10.316 | -30.086 |
| Q1FY2025 | 13 | 120.150 | 6.974 | 5.022 | 0.040 | 31.892 | 8.616 | 3.462 | 23.276 | 19.814 | 20.373 | 8.880 | 2.959 |
| Q2FY2025 | 13 | 123.971 | 4.706 | 2.913 | 0.020 | 38.531 | 7.230 | 4.320 | 31.301 | 26.981 | 24.086 | 8.659 | 2.169 |
| Q3FY2025 | 13 | 133.349 | -1.534 | 2.794 | 0.020 | 47.100 | 13.074 | 4.431 | 34.026 | 29.595 | 35.774 | 9.028 | -3.748 |
| Q4FY2025 | 14 | 145.792 | 1.086 | -7.645 | -0.060 | 57.584 | 13.607 | 7.568 | 43.977 | 36.409 | 35.380 | 8.914 | 8.913 |
| Q1FY2026 | 13 | 170.897 | 26.068 | 21.817 | 0.160 | 50.255 | 10.533 | 4.891 | 39.722 | 34.831 | 28.072 | 9.357 | 5.449 |
| Q2FY2026 | 13 | 201.079 | 22.353 | 19.359 | 0.140 | 88.302 | 7.020 | 19.099 | 81.282 | 62.183 | 44.400 | 9.628 | -2.142 |
| Q3FY2026 | 13 | 291.035 | 23.968 | 11.206 | 0.080 | 95.037 | 17.414 | 11.158 | 77.623 | 66.465 | 50.292 | 24.697 | 2.602 |
| TTMQ3FY2025 | 52 | 494.889 | -2.063 | 27.243 | 0.200 | 162.944 | 34.674 | 16.429 | 128.270 | 111.841 | 94.907 | 36.883 | -28.706 |
| TTMQ3FY2026 | 53 | 808.803 | 73.475 | 44.737 | 0.320 | 291.178 | 48.574 | 42.716 | 242.604 | 199.888 | 158.144 | 52.596 | 14.822 |

## Comparability and accounting

- Cash after PP&E and software/IP is distinct from CFO less PP&E alone. Neither is owner earnings. Noncash accrued purchases in YTD2026Q3: PP&E $4.982m, IP licenses $15.000m; not counted as cash capex or presumed financing debt.
- FY2025 and TTM to Q3FY2026 contain 53 weeks; Q4FY2025 contains 14 weeks. FY2023/24, 2025 comparative TTM and FY2026 quarters contain 52/13 weeks. No per-week normalization applied.
- Historical consolidated perimeter: AMI included only from July 27, 2026. TTM is not full-year pro forma and cannot be treated as organic growth. AMI Q3 contribution: revenue $39.1m; net loss $14.4m.
- PPA preliminary: net assets acquired $1589.664m; intangibles $551m; goodwill $1054.139m. Valuation and tax balances can change during measurement period.
- Q3FY2026 total intangible amortization $13.855m versus $0.597m Q3FY2025: $6.987m cost of revenue + $5.891m separately presented operating expense + $0.977m included in R&D. The two separately presented acquired-intangible lines sum to $12.878m; scope differs, not a reconciliation error. D&A is the full cash-flow adjustment excluding ROU asset and financing costs, not the narrower PP&E depreciation note.
- TTM EPS is sum of four directly reported quarterly diluted EPS rounded to cents. It is not issuer-reported TTM EPS or annual EPS minus YTD EPS; different share counts, Q4 loss antidilution and rounding prevent exact reconciliation to TTM NI/shares.
- Tax is retained as GAAP reported, not normalized: Q3FY2026 expense approximately $2.6m vs $3.7m benefit Q3FY2025; AMI valuation allowance release $1.2m. SBC, foreign rates and credits affect effective rates.
- Debt_gross is principal; debt_net_costs is reported carrying amount net of issuance costs. Missing balances are null, never assumed zero. Operating leases are separate.
- FY2023/FY2024 net income includes tax benefits of $44.205m/$24.902m. FY2025 has $10.293m tax expense; earnings multiples are tax-sensitive.
- CFO less cash PP&E capex is a defined analytical FCF measure, not owner earnings: no deduction for SBC or software/IP licenses. `cash_after_ppe_software_ip` separately deducts cash software/IP. `cash_after_investment_less_sbc_diagnostic` further deducts SBC as a diagnostic, not owner earnings. AMI acquisition spending is separate investing cash flow. Noncash YTD2026Q3 accrued PPE purchases $4.982m and accrued IP licenses $15.000m are not cash capex and must not be treated as financial debt.

## Reproduction and evidence
Run `python reproduce.py` from this folder, or invoke its absolute path; no network or third-party packages. Inputs are adjacent: `inline_numeric_extract.json`, `companyfacts_subset.json`, `urls.json`, and `q4_direct_eps_excerpt.txt`. No original filings or full companyfacts are required. `source_manifest.json` documents hashes of original archived sources, for provenance only. `ledger.json` preserves nested calculation inputs; CSV is a flat navigation view. `inline_numeric_extract.json` preserves tag/context/value/precision and exact filing fragment links. Q4 EPS is corroborated by `q4_direct_eps_excerpt.txt`.

QA: 278 checks; 0 failures. Checks cover completeness, balance identities and agreement of direct inline facts with SEC companyfacts. Additional assertion verifies direct Q4 EPS release row.

## Direct sources
- q3: https://www.sec.gov/Archives/edgar/data/855658/000119312526445613/d34154d10q.htm
- q2: https://www.sec.gov/Archives/edgar/data/855658/000143774926025657/lscc20260704_10q.htm
- release: https://www.sec.gov/Archives/edgar/data/855658/000143774926034452/ex_1012509.htm
- companyfacts: https://data.sec.gov/api/xbrl/companyfacts/CIK0000855658.json
- fy25: https://www.sec.gov/Archives/edgar/data/855658/000143774926004100/lscc20260103_10k.htm
- q1: https://www.sec.gov/Archives/edgar/data/855658/000143774926014686/lscc20260404_10q.htm
- q4_release: https://www.sec.gov/Archives/edgar/data/855658/000143774926003634/ex_882667.htm
- q3_2025: https://www.sec.gov/Archives/edgar/data/855658/000143774925032777/lscc20250927_10q.htm
