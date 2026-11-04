# CVI and refining peers: factual comparison, November 4, 2026

Run `python build.py` from any directory. Inputs are in `inputs.json`; generated `outputs.json` and `peer_facts.csv` contain the calculations. USD millions except shares, unit prices and EPS. No forecast, borrowed model, valuation target, median multiple or recommendation is embedded here.

## Scope and interpretation

Prices are November 3 closes, not November 4 intraday observations. Actual shares are dated separately: CVI October 30, PSX September 30, VLO October 23, MPC October 29. Market capitalizations therefore have share-count/price timing mismatch. Q3 means the three months ended September 30, not nine-month or trailing earnings. No Q3 annualization is used.

CVI is much smaller and combines concentrated inland refining with a controlled fertilizer partnership. PSX has midstream, chemicals, marketing and refining exposure; VLO includes renewable diesel and ethanol; MPC consolidates MPLX. These differences, minority interests, equity-method investments, tax presentation and turnaround accounting make a single seemingly homogeneous EV/EBIT or EV/EBITDA comparison misleading. We show factual scale and reported parent net income/EPS only. Sales are reported GAAP lines, not harmonized net-of-excise revenue: VLO specifically includes $1,658m of foreign excise sales taxes. Do not infer margins or relative cheapness from this table.

## CVI consolidation and UAN ownership

CVI consolidates all UAN operations, debt and cash despite owning roughly 37% of the units. The nonowned stake is total UAN units less CVI-owned units, including IEP's direct UAN interest as well as public holders. IEP's control of CVI does not make its direct UAN units CVI-owned.

UAN's Q3 cover reports exactly 10,569,637 units at October 30; September 30 total is identical. The exact 3,892,000 CVI-owned unit count is from the prior annual 10-K Item 13, corroborated by Q3 approximate 37% ownership and distributions ($23.663m/$6.08 and $40.671m/$10.45, both consistent within rounding). It is not falsely labeled a new exact Q3 ownership disclosure. Assuming unchanged ownership, November 3 $118.62 produces owned stake $461.669m and nonowned stake $792.101m (6,677,637 units). These are market values, not intrinsic value conclusions.

CVI indicative consolidated EV is $4,885.787m equity + $1,794m principal/finance-lease debt - $1,278m cash + $792.101m UAN minority market value = $6,193.888m. Omitting minorities understates this by $792.101m; substituting $172m book NCI understates it by $620.101m. Book NCI is not fair value. This bridge is not used to imply a peer multiple or valuation target.

For a separate parent/refining DCF plus the owned UAN market stake, remove UAN's cash $158.191m and full principal/finance-lease debt $570.862m from consolidated capital first. The latter consists of $550m notes + $20.015m noncurrent finance lease + $0.847m current finance lease. Carrying debt/leases are $569.741m after $1.121m debt issuance costs. UAN debt and cash are already reflected in the quoted UAN equity stake: do not deduct/add them twice. UAN cash is not freely parent-accessible cash. Distribution declared November 3 is $1.79/unit, payable November 23 to November 16 holders; implied CVI receipt $6.96668m. This is not perpetual distributable earning power and not cash already received at September 30.

## Earnings normalization and accounting controls

CVI Q3 GAAP operating income $724m includes a $253m SRE benefit for the 2025 compliance period. Removing that isolated benefit gives $471m, not normalized EBIT. Company's $314m favorable RFS reconciliation includes SRE and RVO revaluation; do not remove $253m a second time after the full $314m adjustment.

Company EBITDA $804m - $314m RFS + $127m unrealized derivative loss - $35m favorable inventory effect = adjusted EBITDA $582m. Petroleum EBITDA $787m uses the same adjustments to reach $565m. Neither is through-cycle earning power. SBC remains an expense; we make no SBC addback. CVI 9M SBC is $38m.

CVI capitalizes turnaround spending; nine-month cash flow separately reports $2m turnaround expenditures and $152m capex. Q3 turnaround amortization $17m (9M $57m) is included in D&A, and thus excluded from EBITDA. Sustainable cash economics must charge recurring turnarounds, not treat EBITDA as maintenance-free cash flow. Other peers' treatment must be harmonized before comparing adjusted EBITDA.

Announced acquisitions, $4.2bn asset price, acquisition financing and prospective new equity are not closed at the comparison date. They are not added to current CVI assets, shares or earnings; announced MPC divestiture proceeds are not subtracted from its debt. Any transaction valuation belongs in a separately labeled conditional scenario.

## Evidence and audit boundary

Every external source is an HTTPS URL in `inputs.json`. Financials are primary SEC statement facts, extracted from local primary archives already audited for PSX/VLO/MPC, then checked against statement labels. The original local archives are outside this deliverable; this directory contains only our own factual extracts and calculations, not full copied third-party models. Market histories are price-provider fallback, not issuer primary filings. CVI/PSX/VLO/UAN Nov3 rows were freshly checked November 4. MPC price retains the independently verified November 4 peer packet's Investing.com/ChartExchange provenance. Financials are unaudited company quarterly statements, not an assertion of independent assurance.
