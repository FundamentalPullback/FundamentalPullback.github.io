# SHOP portable financial history
As of 2026-11-04. USD millions except diluted EPS (USD/share). Offline reproduction: `python3 reproduce.py`. Only Python standard library is required. The source numeric subsets, script, output JSON/CSV and this note are sufficient; original filings are not needed to rerun. `build_inputs.py` is an optional extraction utility requiring the separately retained source table files and is not required for reproduction.

## Source index
All are Shopify primary SEC filings. Table numbers identify the zero-based HTML tables in the corresponding downloaded filing, not SEC page numbers.
- fy25: [FY2025 10-K](https://www.sec.gov/Archives/edgar/data/1594805/000159480526000007/shop-20251231.htm), tables38 (2023–25 income/EPS),40 (2023–25 cash flows).
- q3: [Q3 2026 10-Q](https://www.sec.gov/Archives/edgar/data/1594805/000159480526000068/shop-20260930.htm), table54 (eight quarters income/EPS), table14 (cash flows). MD&A Changes in Merchant Cash Advances and Cash Flows From Investing Activities.
- q2: [Q2 2026 10-Q](https://www.sec.gov/Archives/edgar/data/1594805/000159480526000047/shop-20260630.htm), table14, MD&A Changes in Merchant Cash Advances.
- q1: [Q1 2026 10-Q](https://www.sec.gov/Archives/edgar/data/1594805/000159480526000019/shop-20260331.htm), table14.
- q3prior: [Q3 2025 10-Q](https://www.sec.gov/Archives/edgar/data/1594805/000159480525000089/shop-20250930.htm), table14 (9M2024 and 9M2025 cash flows).

## Method and labels
- GAAP EBIT here means reported income from operations, not pretax income. Direct diluted EPS is read from the filing, including Q4; no EPS is subtracted from annual EPS.
- Q4 additive cash flow items are FY minus nine months. TTM additive financials sum the latest four quarters, with prior TTM the preceding four. Rounded sums of quarterly diluted EPS are provided separately; they are NOT a company-reported or recalculated GAAP TTM diluted EPS denominator. Direct TTM diluted EPS remains null.
- CFO minus cash PPE is a mechanical company-style FCF proxy, not cash fully distributable to shareholders. SBC and lending funding are material. No claim is made that reported PPE equals maintenance investment.
- Positive cash spending fields are deductions. Signed fields retain cash flow statement signs. D&A is the cash-flow-statement amortization/depreciation adjustment; SBC is the cash-flow-statement SBC adjustment, not SBC plus payroll taxes.
- Cash after PPE and investing lending = CFO minus cash PPE minus (investing originations/purchases less repayments/sales). Pre-April2026 MCAs are already inside CFO. NEVER deduct historical MCA operating use again from this combined measure.
- SBC deduction is an economic dilution sensitivity, not another cash outflow. It is not owner earnings and should not be combined with a separate SBC dilution penalty without explaining the potential overlap.
- Intangible cash spending records only the separately disclosed acquisition-of-intangible-assets line (Q3 2026:99). Earlier records show zero for that separate line, not a claim that no intangible investment exists anywhere in acquisitions or other investing. Its purpose, expected life and maintenance/growth split are not disclosed in these retrieved filing passages. Do not treat all99 as maintenance capex or silently exclude it as unquestionably nonrecurring. Show it separately.

## April2026 presentation change and comparability
FY2025 annual cash flows place merchant cash advances/related receivables within CFO: cash effects FY2025 −141, FY2024 −82, FY2023 +214. Loans are separately in investing. Q1 2026 investing rows still describe loans only. Starting April2026, merchant cash advance cash flows are presented in investing alongside loans, concurrent with Canadian Capital's transition from MCAs to loans after regulation changes. Q2 MD&A identifies37 of net cash use in investing from these changes; Q3 identifies30. These disclosures support a67 current-TTM bridge, not a reconstructed historical gross MCA funding series.

The Q3 2026 filing repeats prior-year CFO513 (quarter) and1308 (nine months), exactly matching the original Q3 2025 filing, rather than restating those comparatives to the new presentation. The filing says the change starts in April2026; no further reason for not retrospectively recasting has been established. Do not invent one.

The legacy-presentation sensitivity moves the disclosed37/30 cash use back into current CFO. It compares reported current CFO-minus-PPE on the prior layout, but does not establish identical lending product economics or regulatory treatment. A full retrospective new-presentation restatement is unavailable because historical quarterly MCA cash flow detail is not supplied here.

The classification-neutral cash-after-lending calculation works across the boundary: pre-change MCA funding is already in CFO, while post-change funding enters the investing deduction. It is still an analyst-defined cash measure, not steady-state distributable cash or a GAAP subtotal. Credit losses, growth in the lending book, purchases/sales, timing and capital needs still matter.

## Key results
- TTM revenue14167 vs10696; GAAP operating income2069 vs1302; net income2126 vs1781; CFO2682 vs1923; PPE21 vs20; SBC515 vs443; D&A28 vs32.
- TTM CFO−PPE2661 vs1903. Legacy-presentation sensitivity2594 vs1903. Investing lending net funding789 vs594; cash after PPE and lending1872 vs1309. After separate intangible spend1773 vs1309; after SBC sensitivity1258 vs866.
- Q3 CFO818−PPE2 =816. Moving MCA30 back to the legacy operating layout gives786. Total investing lending net use229 gives cash after PPE/lending587; deducting the separate99 intangible purchase gives488; SBC140 sensitivity gives348. Subtracting both229 and30 from816 would double-count the30.
- FY2025 CFO−PPE2007; after investing loan funding579 =1428; after SBC449 sensitivity979. FY2024 corresponding1597,1133,703. FY2023 corresponding905,382,−233; FY2023 operating loss is distorted by the1340 logistics-sale impairment, not normalized away in this dataset.
