# ServiceNow factual history, research cutoff 2026-11-04

## Portable files
- observations.json: minimal factual observations, USD millions or million shares. Every row has primary source URL and filing XBRL context or printed-table context. Unspecified is not zero.
- history.json / history.csv: observed and derived periods; each derived number points to its inputs.
- build_history.py: standard-library-only rebuild from observations.json, no network or private filings required. Run `python build_history.py`.
- sources.json: primary filing URL index. Full filings are not bundled.
- check_history.py: independent arithmetic and split-adjustment QA.

## Period rules and shares
FY2023-25 are reported annual figures. Latest four quarters are Q4 2025 and Q1-3 2026. Q4 flows = FY25 minus 9M25. Q2/Q3 CF flows = YTD less previous YTD. TTM Sep26 = FY25 + 9M26 - 9M25; prior TTM = FY24 + 9M25 - 9M24. Balance-sheet amounts are instants and never summed into TTM.

5-for-1 split effective December 17, 2025; record date December 16. 2026 10-Q and FY25 10-K retrospectively restate share references. Only observations sourced from pre-split FY24 10-K or Q3 2025 10-Q are multiplied by five. Q4 2025 weighted shares are directly reported, rounded million shares from earnings release (basic 1,039; diluted 1,047), not derived by subtracting averages. No TTM weighted-share average is manufactured. Sep26 exact balance-sheet outstanding shares: 1,037.917 million; Q3 diluted average 1,043.011 million. Source: Q3 2026 10-Q Note2 and balance sheet; Q4 2025 earnings release.

## Cash flow, depreciation and software
`ppe_depreciation` is the PP&E note's depreciation, including computer equipment AND SOFTWARE, leasehold/other improvements and furniture. It is not physical-equipment-only depreciation. TTM PP&E depreciation is 608 versus prior 472; purchased-intangible amortization 535 versus 102; total cash-flow D&A 1,267 versus 680. The residual 124 (prior 106) is UNALLOCATED: do not treat it as physical depreciation or assert a category without more evidence. FY25 Note2 and Note7; Q3 2026 Note6-7.

Cash PP&E purchases of 584 TTM are aggregate PP&E additions paid, not a separate internal-use software series. No separately quantified internal-use software additions were identified. FY25 Note2 says costs between technological feasibility and release for software sold/leased/marketed have not been material, and all such software development costs were charged to R&D. Do not confuse tax-capitalized R&D deferred tax assets with cash software capitalization. PP&E computer-software gross balance rises from 126 at YE25 to 170 at Sep26, but balance changes are NOT cash additions.

Deferred commission cash contribution is negative: TTM -885, versus -714. Amortization is 686 versus 601, hence net cash investment beyond expense 199 versus 113. This is already inside CFO and must not be subtracted twice. Working-capital cash-effect metric sums the six reported operating asset/liability changes, net of acquisitions; it includes commissions, prepaid/other assets, accruals/other liabilities and deferred revenue. It is not a narrow trade-working-capital balance delta.

Raw FCF = GAAP CFO minus cash PP&E, with no management adjustments. Q3 2026 raw FCF = 839-91=748; company non-GAAP FCF is 822 after adding back 74 of business-combination/other cash costs. 9M raw FCF = 3,096-346=2,750; company adjusted = 3,121 after adding 371. These are materially different definitions. Source: https://www.sec.gov/Archives/edgar/data/1373715/000137371526000092/erq3fy26.htm, FCF reconciliation.

## SBC economics
P&L SBC and CFO SBC addback differ in 2026 and are kept separate. Q1/Q2/Q3 P&L expense = 558/655/633 versus CFO addbacks 547/652/630; 9M expense 1,846 versus CFO 1,829. TTM expense 2,340 versus CFO 2,323. Do not replace one series with the other or double subtract either. Raw FCF less P&L SBC (2,410 TTM versus 2,043 prior) is merely a diagnostic, not a valuation or reported GAAP metric. SBC is a recurring compensation/dilution economic cost even when noncash. Cash stock repurchases and employee tax withholding are financing outflows, not proof that SBC is costless. Source: 2026 quarterly MD&A stock-compensation tables and cash-flow statements. FY2023-25 P&L and CFO SBC agree.

## Acquisition perimeter and non-recurring claims
Q3 2026 10-Q Note5: https://www.sec.gov/Archives/edgar/data/1373715/000137371526000096/now-20260930.htm
- Moveworks closed December 15, 2025; consideration 2,407: stock 1,467, cash 905, pre-existing loan 31, pre-combination awards 4. About 9.6m post-split shares. Acquired intangible 770 and goodwill 1,748. Thus almost all FY25 comparisons lack its results.
- Logik.io closed May 30, 2025; consideration 506 including about 2.1m shares valued 434 and cash 62. Developed technology 85 and customer/backlog 14; goodwill 404.
- Veza closed March 2, 2026; consideration 1,237, substantially cash; acquired intangible 356 and goodwill 826.
- Armis closed April 20, 2026; preliminary consideration 7,637, cash; acquired intangible 2,530 and goodwill 5,323.
- Five other 9M 2026 acquisitions, total consideration 612 and goodwill 474. All acquisitions included from their acquisition dates. Filing says operating results and pro forma effects not material; that does not mean balance-sheet or amortization effects are immaterial. No reliable standalone organic-revenue bridge supplied here.
- 9M acquisition-related costs 118 included G&A. Separately, deferred compensation 211 for key employees associated with 2026 acquisitions recorded in assets and amortized over service periods through R&D. Do not call all acquisition-related cash costs one-time expense or add them all back automatically.
- Q3/9M 2026 severance expense 87/167, versus 24/53 comparatives (earnings-release reconciliation). Recurring restructuring risk remains a judgment for any valuation model.

## Taxes and other gains
FY23 net income 1,731 includes large tax benefit: tax provision is -723; valuation-allowance release approximately 1,050. FY25 10-K Note17 is the authority; avoid extrapolating FY23 net margins. Q3/9M26 tax expense 93/437. 9M26 includes a discrete valuation-allowance-release benefit 51, per Q3 earnings release footnote 4. 9M26 unrealized strategic-investment gains 367 are removed in CFO and not core operating income. 2026 tax also reflects stock-compensation shortfalls, whereas 2025 benefited from excess SBC tax benefits. No invented normalized tax rate.

## Balance sheet and backlog
Sep26 cash 2,393 + short/long marketable debt securities 2,214+2,354 =6,961. Strategic investments 2,050 are a different asset class, not cash. Debt carrying amount 2,086+5,438=7,524; principal is separately described by issuer as 7,600 (rounding/discount/issuance-cost differences). Operating lease liabilities 118+773=891. Deferred revenue 7,600+133=7,733. RPO 29,700, cRPO 13,650 from latest earnings release. cRPO is directly observed from releases, never computed as rounded RPO times rounded percentage. Backlog has currency, contract-duration, self-hosted timing and US federal 12-month-renewal seasonality effects; not identical to ARR or certain cash receipts.

## Limitations
No separately observed capitalized internal-use software flow. Residual D&A is not classified. No synthetic TTM diluted share average. Latest balance-sheet figures include major newly acquired businesses; no apples-to-apples organic operating series is invented. This dataset contains no market-price input or valuation.
