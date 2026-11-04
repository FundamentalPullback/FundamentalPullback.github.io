# Moody's adjacent peer comparison
Research: 2026-11-04. Prices: 2026-11-03 regular close, independently checked in Stock Analysis historical rows; financial evidence from SEC/issuer primary sources.

Run `python calculate.py` from any directory. It reads sibling `inputs.json`, writes `results.json` and `numeric_rows.csv`, and uses no network or non-standard Python dependencies. All financial data in USD millions; share counts in millions. Raw full filings under `raw/` are local research only: do not upload/publish them. Portable numeric facts, source URLs and calculation code suffice to reproduce results.

## Findings
- MSCI: $639.78; 71.5m actual shares Oct 13; nominal debt $6,760m; unrestricted cash $257.4m after excluding $3.6m restricted. TTM Sep 2026 revenue $3,432.359m, EBIT $1,910.167m, CFO $1,614.846m, physical capex $39.619m, software $120.542m, SBC $126.143m. EV/EBIT 27.35x; owner FCF $1,328.542m / equity $45,744.27m = 2.904%. Mixed source precision warrants rounding output to millions.
- SPGI: $466.03; 289.9m actual shares Oct 23; continuing revenue $14,546m and EBIT $7,256m. Use FY2025 continuing operations subtotal $6,105m from July 6 Article 11 reconciliation, not $6,140m including a hypothetical $35m TSA adjustment. TTM EBIT includes $656m disposition gains, leaving $6,600m after only these gains are removed. Carrying-debt EV proxy $151,191.097m gives 20.84x/22.91x respectively.

## Material limitations: do not hide these
SPGI nominal debt has not been reconciled. $13,062m is carrying amount, not an independently established nominal principal amount. Results are explicitly carrying-debt proxies. $5,348m redeemable NCI plus $120m nonredeemable NCI are included in EV to match consolidated EBIT. Neither is a market-value estimate. No pension or lease addition, and no investee deduction.

SPGI TTM continuing CFO/capex/SBC and owner-FCF yield remain null. Its original FY2025 10-K cash flow includes Mobility; Q3 2026 comparative 9M cash flows exclude it. Naively using FY2025 + 9M2026 - 9M2025 would overstate retained-business cash flow. July 6 recast supplies historical income/balance sheets, not a full continuing cash-flow statement. Verified 9M2026 continuing CFO3,661 - total capex93 - SBC127 - NCI distributions269 = owner cash3,172m. This is nine-month cash, not TTM or an annualized yield. Missing item is a verified FY2025 retained cash-flow bridge, not access denial.

Mobility spun off July 1, 2026, one MBGL share per SPGI share. The Nov 3 SPGI price is ex-Mobility; retained income must likewise exclude Mobility. Capital IQ strategic review on Oct 27 is not a completed divestiture. Keep Capital IQ in current perimeter and do not count sale proceeds. Current source facts verified in Q3 10-Q and earnings release.

## Primary evidence locations
MSCI Q3 10-Q: cover (shares), statements of financial condition (restricted cash), income/cash flow statements, Note7 (nominal/carrying debt). FY2025 10-K: consolidated income and cash-flow statements.
SPGI Q3 10-Q: cover, income/balance/cash-flow statements, Note4 debt, NCI and lease notes. July6 8-K/A: Exhibit99.2 FY2025 income reconciliation, continuing-operations subtotal. FY2025 original 10-K proves why the unrecast cash-flow bridge is unusable. Exact links in inputs.json and numeric_rows.csv.

Status: MSCI complete. SPGI usable limited EV/EBIT comparison; nominal debt and clean TTM owner cash unresolved. Do not describe the two-company comparison as fully standardized.
