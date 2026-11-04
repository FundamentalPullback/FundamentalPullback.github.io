# HURN / Huron Consulting Group: historical financial package

Cut-off: November 4, 2026. Sources include the November 3, 2026 Q3 10-Q and earnings release. Huron is a professional-services, consulting and managed-services business. Healthcare describes a client-industry segment, not a reclassification of Huron into healthcare provision or pharmaceuticals.

## Reproduction

Run `python rebuild_history.py` from any working directory. Only Python's standard library and the adjacent reduced `numeric_inputs.json` are needed. There is no network call, absolute input path, full filing, companyfacts dataset, third-party package or dependence on another company folder. `python verify_offline.py` creates an isolated temporary folder containing only the script and numeric inputs, disables socket connections and reproduces seven output files byte for byte. Checksums cover the delivered files.

16 periods: FY2023, FY2024, FY2025; eight quarters from Q4 2024 to Q3 2026; 9M 2024/2025/2026; TTM September 2025/2026. Calendar-year dates, no 52/53-week conversion. Quarterly revenue, operating income, NI and EPS are directly reported. Q4 income statements come from the FY2025 earnings release, including Q4 2024 comparatives. Cash flow quarters are YTD differences, and Q4 is FY minus nine months. TTM is prior FY plus current 9M minus prior 9M. EPS and weighted shares are never subtracted; TTM values for these non-additive metrics remain null.

All currency values are USD millions, EPS USD/share, weighted shares millions. Source identifiers, filing dates, tags, precision, labels and context dates remain in numeric_inputs.json. Ledger rows reference those original facts or child ledger nodes. Selection uses the latest comparative and then greatest precision. Rounding tolerance accounts for narrative values expressed to 0.1 million. Missing means unknown/not separately reported, never zero. All 84 accounting and quarter-to-year/TTM identity tests pass; no material source-value conflicts were found.

## Critical definitions

- `revenue_rbr` is revenue BEFORE reimbursable expenses. `revenue_gaap` is TOTAL revenue including reimbursements. Both are direct statement lines. The standard XBRL revenue-from-contract tag corresponds to RBR here, so a generic tag-based pull would mislabel it. EBIT margins are supplied on both denominators with explicit names. Revenue identity is tested.
- Gross cash investment includes TWO investing lines: purchases of PP&E AND capitalization of internally developed software. `fcf_after_ppe_software` deducts both. `fcf_ppe_only_incomplete` is labeled incomplete and must not be treated as full FCF. Software supports cloud products sold to clients, not merely office equipment.
- `da_income` is the operating-income-statement line. `da_cf` is the cash-flow addback. They can differ. The company's non-GAAP EBITDA reconciliation has yet another D&A amount; it is not substituted into either GAAP series. Acquired-intangible amortization is separate, with exact figures from earnings-release reconciliation tables when available and 0.1-million narrative precision in other periods. Subtracting acquired amortization from total D&A leaves a mixed residual, not pure tangible depreciation.
- Acquisition purchase cash and deferred acquisition cash classified in financing are separate from PP&E/software. The deferred payments still consume cash. Capital expenditures accrued but unpaid are not silently added to current-period cash capex.
- SBC remains an expense economically. CFO deducts neither SBC nor repurchase spending; the after-SBC proxy makes that dilution cost visible without claiming buybacks are maintenance capex. Repurchases and borrowing are separate financing metrics.
- Net debt is provided both at balance-sheet carrying amount and stated principal when available. Latest principal debt 815.000 differs from carrying debt 813.886 because of unamortized financing costs. Operating leases are separately shown. Equity is parent consolidated equity; no NCI addback has been invented.
- Seven working-capital cash lines are signed as CFO contributions: accounts receivable, unbilled services, tax receivable/payable, other assets, accounts payable/accruals, payroll, deferred revenue. Asset increase/decrease tags are explicitly converted to cash-contribution polarity. CFO before WC is diagnostic, not normalized cash earnings.

## Current TTM result and comparison

TTM September 2026: RBR 1,824.146; GAAP total revenue 1,860.223; operating EBIT 195.845; NI 113.538; CFO 141.736; PP&E/software cash investment 36.738; FCF 104.998; SBC 50.220; after-SBC proxy 54.778. Acquired-intangible amortization is 15.272, using exact FY/9M reconciliation amounts. Latest cash 25.618; principal debt 815.000; net principal debt 789.382.

Prior TTM: RBR 1,618.977; EBIT 175.436; NI 108.375; CFO 206.602; total cash capex 30.479; FCF 176.123; SBC 47.430; after-SBC proxy 128.693; net principal debt 587.111. Operating growth has not translated into comparable cash growth. Working-capital cash contribution deteriorated to -93.372 from -6.904.

CFO is strongly seasonal: Q1 2026 was -162.168 and Q4 2025 was +126.407. It would be misleading to annualize nine-month cash flow alone. Nevertheless the TTM also declined. Management attributes lower nine-month CFO to higher payroll/related costs, annual bonuses, SG&A and interest, plus large performance-fee engagements not yet eligible for billing. That explanation does not establish a collection date or prove all unbilled work will convert on schedule. At September 2026, net unbilled services were 263.196 and client receivables 218.893.

## Normalization and scope limits

These outputs are reported, not a pro forma organic reconstruction. Acquisitions and divestitures alter the perimeter; consult the Business Combinations note before extrapolating organic growth. Financial statements and earnings-release adjustments are not merged into an adjusted-earnings series. In particular, lease-modification gains, changes in acquisition-contingent consideration, investment credit losses and transaction costs require classification and durability judgment, not indiscriminate addbacks. Annual and quarterly restructuring appears repeatedly and is not presumed nonrecurring.

Maintenance/growth allocation for software and PP&E is unavailable. Sustainable owner earnings therefore remains null. The after-SBC FCF measure is transparent cash arithmetic, not a Buffett owner-earnings assertion. Do not normalize away unfavorable working-capital movements merely to recover prior cash flow.
