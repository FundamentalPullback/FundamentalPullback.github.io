# OKTA financial history, information available 2026-11-04

All dollar amounts are USD millions except per-share data. Fiscal year ends January 31. Latest reported quarter is Q2 FY2027, ended July 31, 2026; Q3 ended October 31 is not yet reported. No valuation or investment conclusion is provided.

## Deliverables
- raw_inputs.json: compact numeric extracts with source URL, original source line, and zero-based column; no full filings.
- normalized_history.json and normalized_history.csv: three full fiscal years, four latest quarters and year-earlier comparatives, YTD bridge periods, latest TTM and previous-year TTM.
- rebuild.py: Python standard-library-only offline generator. Run `python rebuild.py` in this directory. All set-derived output ordering is explicitly sorted.
- qa.json: FCF and TTM reconciliation assertions.

## Useful results
FY2024 / FY2025 / FY2026 revenue: 2,263 / 2,610 / 2,919; GAAP operating income: -516 / -74 / 149; GAAP net income: -355 / 28 / 235; CFO: 512 / 750 / 884; company-definition FCF: 489 / 730 / 863.

Latest four quarters (Q3 FY2026, Q4 FY2026, Q1 FY2027, Q2 FY2027): revenue 742 / 761 / 765 / 805; GAAP operating income 23 / 46 / 56 / 107; net income 43 / 63 / 74 / 116; directly reported diluted EPS 0.24 / 0.35 / 0.42 / 0.65. CFO 218 / 258 / 277 / 234; FCF 211 / 252 / 271 / 227.

TTM through July 31, 2026 versus July 31, 2025: revenue 3,073 vs 2,763; GAAP operating income 232 vs 72; net income 296 vs 168; CFO 987 vs 853; FCF 961 vs 838; SBC 503 vs 538. Operating margins 7.55% vs 2.61%. SBC/revenue 16.37% vs 19.47%. FCF minus SBC sensitivity 458 vs 300; this is a sensitivity, not a company or GAAP measure.

## Accounting and calculation safeguards
- Latest TTM = FY2026 + H1 FY2027 - H1 FY2026. Previous TTM = FY2025 + H1 FY2026 - H1 FY2025. Quarterly cash-flow items not directly reported are derived by YTD differences; provenance marks these bridges.
- EPS is always the directly disclosed period EPS. Annual or YTD EPS is NEVER differenced to generate a quarter and NEVER summed to assert GAAP TTM EPS. No TTM EPS is produced. GAAP diluted FY2025 EPS is 0.06 and Q3 FY2025 EPS is 0.00 as published; these should not be replaced with net-income/basic-share approximations.
- Operating income is labeled EBIT GAAP for this workflow. It is not net income plus interest expense; interest income and other, net remains separate, as does total interest and other, net.
- D&A includes acquired intangible amortization; do not add acquired amortization again. Deferred commission amortization is a separate cash-flow adjustment, not included in reported D&A. The residual D&A minus acquired amortization is labeled as a calculated residual, not as depreciation alone.
- Annual acquired intangible amortization: FY2024 78, FY2025 73, FY2026 68. These are the operating-income reconciliation figures. Do not substitute total intangible amortization (87, 85, 83), which also includes internally capitalized software amortization.
- Q2 FY2027 acquired intangible amortization fell to 3 versus 17 a year earlier; H1 21 versus 34. Some GAAP margin improvement consequently reflects declining amortization, alongside SBC reduction.
- Company FCF subtracts cash property/equipment purchases and capitalized software from CFO. Additional intangible purchases of 2 in H1 FY2027 are excluded from that definition and retained separately in this dataset. Latest TTM FCF less these purchases is 959, before acquisitions. FY2024 separately reports intangible purchases of 1.
- Cash acquisitions are not operating capex: latest TTM 53; FY2026 56, FY2025 56, FY2024 22. These are cash-flow figures, not transaction enterprise values or total acquisition consideration.
- Deferred commission capitalization is a real recurring cash use: latest TTM 261 vs commission amortization 177; prior TTM 207 vs 144. Deferred-revenue cash-flow benefit is 206 vs 160. Do not treat all CFO improvement as earnings conversion independent of working capital.
- Expense interest and interest income/other are included; separate cash interest received/paid was not independently established and is not imputed from expense. Supplemental balance-sheet and capital-structure work is outside this history module.
- Raw reported financials are rounded to whole millions; derived differences inherit rounding. Percentage growth is suppressed where the comparison denominator is nonpositive. Derived TTM is not itself a separately filed audited financial statement.

## Primary evidence
[SEC FY2026 10-K, covering all three full years](https://www.sec.gov/Archives/edgar/data/1660134/000166013426000020/okta-20260131.htm)

[Q2 FY2027 earnings release](https://investor.okta.com/news-and-events/news-releases/news-details/2026/Okta-Announces-Second-Quarter-Fiscal-Year-2027-Financial-Results/default.aspx)

[Q1 FY2027 earnings release](https://investor.okta.com/news-and-events/news-releases/news-details/2026/Okta-Announces-First-Quarter-Fiscal-Year-2027-Financial-Results/default.aspx)

[Q4 FY2026 earnings release](https://investor.okta.com/news-and-events/news-releases/news-details/2026/Okta-Announces-Fourth-Quarter-And-Fiscal-Year-2026-Financial-Results/)

[Q3 FY2026 earnings release](https://investor.okta.com/news-and-events/news-releases/news-details/2025/Okta-Announces-Third-Quarter-Fiscal-Year-2026-Financial-Results/default.aspx)

[Q2 FY2026 earnings release, prior H1 bridge](https://investor.okta.com/news-and-events/news-releases/news-details/2025/Okta-Announces-Second-Quarter-Fiscal-Year-2026-Financial-Results/default.aspx)

[Q4 FY2025 earnings release, FY2024 acquired-amortization check](https://investor.okta.com/news-and-events/news-releases/news-details/2025/Okta-Announces-Fourth-Quarter-And-Fiscal-Year-2025-Financial-Results/default.aspx)
