# DuPont financial history: perimeter and reproducibility

As of November 4, 2026. Financial statement amounts are USD millions, EPS USD per share. Source numeric subsets contain selected rows from public SEC filings, with original table labels, table indices, URLs and SHA-256 fingerprints of the local extracted source table. No full filing is needed to reproduce the outputs.

## Offline reproduction

Run `python reproduce.py` from this folder (Python standard library only). It reads `source_numeric_subsets.json`, produces `financial_history.json`, `financial_history.csv`, and `segment_history.csv`, and validates the TTM bridge. `extract_subsets.py` is an optional provenance-refresh utility requiring the parent folder's original local extracted tables; it is NOT required for offline reproduction.

## Primary filings

- FY2025 10-K, operations and cash-flow statements and Notes on EPS, segments and quarterly data: https://www.sec.gov/Archives/edgar/data/1666700/000166670026000013/dd-20251231.htm
- Q1 2026 10-Q: https://www.sec.gov/Archives/edgar/data/1666700/000166670026000031/dd-20260331.htm
- Q2 2026 10-Q: https://www.sec.gov/Archives/edgar/data/1666700/000166670026000053/dd-20260630.htm
- Q3 2026 10-Q: https://www.sec.gov/Archives/edgar/data/1666700/000166670026000060/dd-20260930.htm

## Perimeter

The FY2025 10-K recasts FY2023/2024/2025 continuing operations to exclude Electronics/Qnity and Aramids. The newer 2026 quarterly filings present the same continuing-business perimeter. Qnity separation was completed November 1, 2025. Aramids divestiture was completed April 1, 2026. M&M discontinued businesses and associated legacy cash flows also must not be confused with current operating earnings.

Recast does not mean pro forma standalone economics. Indirect corporate and shared-services expenses remain in continuing operations. Future reimbursable indirect costs are excluded from company-defined Operating EBITDA; stranded costs remain included. Historical debt, interest, separation and restructuring costs are real reported expenses and are not replaced with a hypothetical current structure.

The pre-separation September 2025 filing is deliberately NOT used for current-perimeter 9M comparatives: we use the comparative columns in Q3 2026. Gross proceeds from sale of Aramids are investing receipts and are NOT added to FCF.

## EPS and denominator control

A 1-for-3 reverse split became effective June 24, 2026. Q2/Q3 2026 statements retroactively adjust all presented share and per-share figures. FY2025 and Q1 2026 original statements predate the split and use the old share scale. `diluted_eps_continuing_as_reported` is always the actual published direct EPS value from its source filing, including Q4 2025 direct quarterly EPS in the FY2025 note. `eps_split_multiplier` explicitly shows which values need x3 for comparison. `diluted_eps_split_adjusted_rounded` multiplies already-rounded reported EPS by three for the older sources: this is an approximate historical restatement, not a newly reported figure, and can differ by cents from full-precision restatement.

For example Q1 2026 reported $0.36 on the old scale becomes an approximate $1.08. Q2/Q3 2026 direct EPS is $1.37/$1.24 on the new scale. FY2025 direct $0.21 becomes approximately $0.63. Q4 2025 direct -$0.27 becomes approximately -$0.81. TTM direct reported EPS is null: an optional $2.88 sum of the four split-adjusted quarterly amounts is explicitly approximate, NOT annual EPS calculated from income and a selected denominator. Annual or quarterly EPS should never be subtracted to derive another quarter.

Continuing net income to common is sourced from the dedicated EPS note. It is not continuing NI less total consolidated NCI, because that NCI includes discontinued operations.

## Metric definitions and derived periods

- Annual figures are direct FY2025 comparative statement values.
- Q4 2025 monetary flows = FY2025 minus recast 9M2025. Q4 EPS is direct from the FY2025 quarterly note, not a subtraction.
- Q1/Q2/Q3 revenue, income and EPS are direct quarterly statement columns. Q2 cash flows = six months minus Q1; Q3 cash flows = nine months minus six months.
- TTM = FY2025 - 9M2025 + 9M2026, cross-checked against the four quarters.
- `ebit_pretax_plus_interest` = continuing pretax income plus reported interest expense. It is a transparent calculated non-GAAP subtotal based on GAAP inputs, not a separately reported company operating-income line. It includes equity/sundry income and interest income.
- `operating_profit_calculated` = sales less COGS, R&D, SG&A, intangible amortization, restructuring, goodwill impairment, acquisition/integration/separation costs. This calculated subtotal excludes equity and sundry income and excludes interest. Both measures are provided to avoid labeling one ambiguous EBIT as the other.
- FCF = actual continuing CFO minus positive continuing capital expenditure, with no adjustment for transaction costs, restructuring, working capital, swaps, acquisitions or separation. It is not company transaction-adjusted FCF and not a normalized run rate.
- Continuing D&A and SBC are direct cash-flow-statement adjustments. Segment D&A is a different aggregation; do not substitute it for consolidated continuing D&A.
- Segment Operating EBITDA and margins are company-defined management metrics, not GAAP EBIT. Corporate costs are excluded from each segment margin, and segment sums overstate consolidated company Operating EBITDA unless corporate expense is included.

## Cash caution

TTM continuing FCF is $793m, but discontinued operating cash flow is -$226m. The latter captures economically relevant legacy/disposal-related cash outflows that the continuing FCF definition excludes. Hence continuing FCF is not synonymous with cash freely distributable to common owners. Q3 2026 cash-flow discussion expressly notes MOU activity, insurance-proceeds MOU buyout and indemnification in discontinued cash. The accompanying report addresses PFAS, pension and balance-sheet claims; do not double count those if cash outflows are deducted and liabilities are also capitalized.

Annual continuing FCF: FY2023 $543m, FY2024 $480m, FY2025 $227m. Quarter continuing FCF: Q4 2025 $0m, Q1 2026 $130m, Q2 2026 $324m, Q3 2026 $339m. Thus current TTM strength is heavily 2026-driven and should not be extrapolated without examining working capital and remaining transaction/legacy cash leakage.
