# Dell history, verified 2026-11-04

Run `python reproduce_history.py` in this directory. Offline reproduction uses only Python standard library and `source_numeric_facts.json`. No full filings are redistributed. `extract_facts.py` optionally refreshes the numeric subset from local `/tmp` copies, using lxml; it is not required for reproduction.

## Definitions and sources

- Values in USD millions, except GAAP diluted EPS in USD/share. `parent_net_income` uses us-gaap:NetIncomeLoss (attributable to Dell), not consolidated ProfitLoss. The difference in FY2024/FY2025 reflects noncontrolling losses. Zeroes only appear where explicitly reported.
- All annual comparatives come from FY2026 10-K, including revisions reflected in that filing. Fiscal years are not calendar years. FY2024 ended 2024-02-02; FY2025 ended 2025-01-31; FY2026 ended 2026-01-30. Latest quarter is Q2FY2027 ended 2026-07-31.
- GAAP EBIT = reported operating income. Segment EBIT is management's reported segment operating income, before corporate reconciliation; segment margins are not consolidated GAAP margins.
- Cash capex includes capitalized software and DFS operating-lease equipment. CFO includes DFS financing-receivable cash flows. A positive financing_receivables_cash_use is a use of operating cash, not balance-sheet growth alone.
- Q3 and Q2 cash flows = YTD less preceding YTD. Q4 revenue, operating income, parent NI, cash flows and segments = annual less nine months. TTM = FY2026 + H1FY2027 − H1FY2026; prior TTM = FY2025 + H1FY2026 − H1FY2025.
- EPS is NOT additive across YTD periods with different weighted share counts. Q4FY2026 actual published GAAP EPS 3.37 and Q4FY2025 2.15 are from https://investors.delltechnologies.com/news-events/press-releases/detail/93/dell-technologies-delivers-fourth-quarter-and-full-year-fiscal-2026-results . TTM EPS 17.23 = 2.28+3.37+5.24+6.34, prior TTM 6.86 = 1.64+2.15+1.37+1.70. This sum-of-reported-quarter EPS is an analytical trailing proxy, not a newly filed annual GAAP EPS calculation. Q3FY2025 1.64 is revised comparable in Q3FY2026 filing.
- `cfo_less_cash_capex` is strict cash CFO minus cash capex. Dell reported FCF includes proceeds from asset disposals, so FY2026 reported FCF 8555 differs from strict 8552 and FY2025 reported 1958 differs from strict 1869. `cfo_less_capex_and_sbc` is an analytical shareholder-cost sensitivity, not a cash-flow statement measure.
- Company adjusted FCF adds net DFS financing-receivable investment and net operating-lease equipment investment back to FCF. It must not be valued as unencumbered industrial FCF without matching DFS funding/debt/assets. See parent's DFS bridge.
- `finance_originations_rounded` follows PaymentsToAcquireFinanceReceivables tag in the financial services note: these are NEW financing originations reported at $0.1bn precision, not the financing-receivable net CFO line and not collections. Derived quarter/TTM values preserve that limited precision. Separate gross collections are not normalized here; no zero is invented. DFS sales-type origination is operating cash use, DFS operating-lease origination is investing cash use/capex. Subsequent financing debt movements are financing activities. Review parent's DFS bridge for equipment adjustments and collections classification.

## Primary filings

Each numeric fact records URL, fiscal dates, tag and context dimensions. Sources:
- FY2026 10-K: https://www.sec.gov/Archives/edgar/data/1571996/000157199626000008/dell-20260130.htm
- Q3FY2026 10-Q: https://www.sec.gov/Archives/edgar/data/1571996/000157199625000127/dell-20251031.htm
- Q1FY2027 10-Q: https://www.sec.gov/Archives/edgar/data/1571996/000157199626000030/dell-20260501.htm
- Q2FY2027 10-Q: https://www.sec.gov/Archives/edgar/data/1571996/000157199626000046/dell-20260731.htm
- Q2FY2026 10-Q: https://www.sec.gov/Archives/edgar/data/1571996/000157199625000102/dell-20250801.htm

## Readout

TTM revenue 151197 (+49.0%), EBIT 14252 (+109.0%), parent NI 11378 (+135.2%), CFO 12152 (+62.5%), strict cash FCF 8560 (+76.1%), diluted-quarter EPS sum 17.23 (+151.2%). EBIT margin 9.43% versus 6.72%. TTM SBC 727 and D&A 3041. ISG revenue 94500/EBIT12479; CSG revenue55615/EBIT3689. Rapid earnings growth exceeds CFO growth: latest H1 strict cash FCF 4104 versus4096 a year earlier, despite NI7571 versus2129. DFS financing-receivable investment, inventory and supplier financing materially affect cash conversion.
