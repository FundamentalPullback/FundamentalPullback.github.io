# SHOP operating comparisons, 2026-11-04
Run `python3 reproduce.py` offline with Python standard library. Inputs are `comps_numeric_subsets.json`; outputs `operating_comps.json` and `.csv`. USD millions; WIX source thousands converted by /1000. Source table numbers are zero-based HTML-table indices. Original full HTML is excluded from this portable subset; hashes and URLs are in source_integrity.json.

## WIX
Primary source: [Q2 2026 release](https://www.sec.gov/Archives/edgar/data/1576789/000162828026052108/secondquarter2026results.htm). Tables1 (income),5 (cash flow),20 (EBIT reconciliation),24 (FCF reconciliation). Input order: Q2 2026,Q2 2025,H1 2026,H1 2025.

Q2 revenue563.058; GAAP EBIT−58.799; CFO55.562; PPE/lease2.648 plus software0.272 gives FCF52.642. SBC53.372 yields −0.730 dilution-cost sensitivity. Non-GAAP EBIT64.827 excludes123.626: SBC53.372, amortization2.034, restructuring27.109, tax/G&A0.052 and acquisition-related41.059. Adjusted FCF61.176 adds8.534 cash restructuring; acquisition cash addback is zero this quarter,37.279 in H1. Do not substitute accrual acquisition expenses for cash adjustments. Cash-flow D&A8.000 differs from non-GAAP amortization2.034.

Wix combines subscriptions, business solutions and Base44, acquired2025. Q2 is latest available here, not Q3. [Company announcement](https://www.wix.com/press-room/home/post/wix-to-announce-third-quarter-2026-results-on-november-10-2026) schedules Q3 for November10 before market open. No future results are filled in.

## EBAY
Primary source: [Q3 2026 release, October28](https://investors.ebayinc.com/investor-news/press-release-details/2026/eBay-Inc--Reports-Third-Quarter-2026-Results/default.aspx). Tables4 (income),5 (cash flow),11 (EBIT reconciliation),13 (FCF reconciliation). Input order: Q3 2026,Q3 2025,9M2026,9M2025.

Continuing revenue3206; EBIT616; CFO875; PPE126; FCF749; SBC173 yields576 sensitivity. Continuing prior CFO900, not consolidated862, matches FCF803. Non-GAAP EBIT843 adds227: SBC/payroll177, acquired amortization25, restructuring/executive bonuses−3 and transaction costs28. Cash-flow SBC173 excludes the extra payroll component. Depop closed July30; acquisition cash1321 net of acquired cash is outside FCF. Internal-use-software ASU2025-06 adopted retrospectively January2026 means the supplied prior comparatives are recast. The release gives no separate software-cash amount; null is not zero, and no additional software deduction is invented.

## Interpretation
These are operating reference points, not valuation comparables. Different periods, revenue recognition/mix, acquisition scope, credit funding, software treatment and non-GAAP exclusions prevent a simple multiple ranking. No EV multiples are supplied. SBC deductions are economic sensitivities, not cash outflows or owner earnings; do not also impose the same dilution cost elsewhere without explanation. SHOP's lending-adjusted cash measure must not be compared as if identical to either company's headline FCF. No normalizing acquisition or restructuring addbacks are automatically accepted as nonrecurring.
