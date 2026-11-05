# Additional primary-source verification: CQP waterfall and growth funding

2026-11-05. The CQP ownership and operating-surplus distribution waterfall are verified below. All amounts USD millions except stated units/percentages.

## CQP ownership and waterfall: resolved

CQP Q3 10-Q cover: 484,057,704 common units outstanding October 23, 2026. Note 1 states LNG held 239.9 million common units September 30. CQP 2025 10-K Item 12, p.92, gives exact LNG holding **239,872,502 common units** and **9,878,316 GP units**, dated February 20, 2026. The exact older parent holding is corroborated by the rounded Q3 disclosure, not independently re-established to a single unit for September/October.

Ownership percentages need clear denominators: LNG's quoted 48.6% LP interest is as a share of total partnership securities, with the entire 2% GP held separately. Its common-unit ownership is approximately **49.5545% of the LP common-unit pool** using the exact counts above. Outside holders own approximately 50.4455% of common units, corresponding to the quoted 49.4% of total partnership securities. Do not use 48.6% to allocate the LP-only distribution pool.

CQP annual p.35 states the operating-surplus waterfall, assuming no additional distribution-bearing classes, no arrearages, and maintenance of the 2% GP interest. Marginal distribution splits are:
- Initial $0.425 per common unit: LP 98%, GP 2%.
- Above $0.425 through $0.489: LP 98%, GP 2%.
- Above $0.489 through $0.531: LP 85%, GP 15%.
- Above $0.531 through $0.638: LP 75%, GP 25%.
- Above $0.638: LP 50%, GP 50%.

The GP percentage includes both base GP and IDRs. These are marginal tiers, not a 50% claim on all distributions. For a given common-unit distribution d, each tier's GP/IDR cash is LP cash in that tier multiplied by GP% / LP%. Base GP equals 2% of total distributed cash; IDR is the remaining GP allocation.

Reproduction in waterfall.py ties to the rounded Q3 filing payment table:
- d=$0.790: LP 382.406, base GP 9.633, IDR 89.627. Filing rounds to 382 / 10 / 90.
- d=$0.820: LP 396.927, base GP 10.214, IDR 103.567. Filing rounds to 397 / 10 / 104.
- d=$0.830: LP 401.768, base GP 10.408, IDR 108.214. Filing rounds to 402 / 10 / 108.

For declared Q3 d=$0.890, calculation yields LP 430.811, base GP 11.570, IDR 136.096, total 578.477. Parent LP plus GP/IDR = approximately 361.152 and outside LP = 217.325. This is a mechanical distribution allocation, not an estimate of FCFF or full economic equity value. It uses the dated exact parent unit count above. The filing states October 23 declaration, November 3 record and November 13 payment; base $0.775 plus variable $0.115.

Separate Tug Services payments to Cheniere Terminals were 8 million YTD 2026 and are recognized as part of distributions to the GP holder. They are outside this unit-based waterfall. Reconcile them and intercompany eliminations rather than treating every GP cash receipt as an IDR.

## Project disclosures newly resolved by Q3 slides

Slide 6 gives SPL Phase 1 **approximately $4.7 billion lump-sum turnkey EPC contract**, signed with LNTPs beginning May 2026. It also gives **$3.25 billion senior secured delayed-draw term-loan commitments**, intended to finance approximately 50% of expected Phase 1 total costs. Mechanically that implies approximately $6.5 billion total cost; label this as an inference from the rounded financing percentage, not an independently exact management budget. The approximate $1.8 billion difference from EPC is not itself an itemized verified non-EPC budget. The loan remains conditional on FID/closing requirements per 10-Q, not funded debt.

Slide 6 targets FERC permit late 2026 to enable late 2026/early 2027 FID. CCL first-phase expansion is >5 mtpa and targets late 2027/early 2028 FID following regulatory approvals. Trains 8 & 9 remain 2H 2028 completion, procurement/construction described ahead of schedule. Neither slides nor the captured filings provide a current full project-by-project remaining cash-to-completion schedule. Do not infer remaining capex from percentage completion or subtract consolidated spending from EPC contract values.

Slide 5 says approximately 740 million of Q3 growth capex funded, approximately 600 million with equity cash flow and 100 million with debt (rounded). This is quarter spending, not remaining funding. Slide 19's run-rate cases provide additional model anchors but not a ten-year forecast: 60–63 mtpa case with consolidated adjusted EBITDA 7.3–8.0 billion and parent DCF 4.1–4.7 billion; 71–75 mtpa expansion case with EBITDA 8.6–9.4 billion and DCF 4.9–5.6 billion. Assumptions include 80/20 profit-sharing tariffs with SPL/CCH, Henry Hub $3, CMI margin $2.50–$3/MMBtu before lifting margin, 10–15% effective cash tax as percentage of DCF, 5% refinancing rates and 500 million future CQP debt paydown. These are management scenarios, not current GAAP earnings or independently underwritten valuation cash flow.

## Parent-only net debt: still not established; ex-CQP is computable

Slide 18 labels LNG cash approximately 1.5 billion, but footnote 1 expressly includes restricted cash and excludes CQP's approximately 0.6 billion cash. It does not establish stand-alone holding-company cash. Exact balance-sheet subtraction gives ex-CQP cash 1,452, of which 358 restricted and 1,094 unrestricted. This reconciles to the slide's rounded 1.5 billion.

Ex-CQP nominal debt is 9,615 (parent 4,750 plus CCH 4,865), and ex-CQP nominal debt less unrestricted cash is **8,521**. This is a consistent deconsolidated arithmetic metric, not holding-company-only net debt or excess-cash determination. Current stand-alone parent cash was not located in the Q3 or annual captures, and project cash restrictions remain relevant. Parent gross debt 4,750 is known; parent net debt remains unestablished. Do not subtract 1.5 billion of ex-CQP/restricted cash from parent-only debt and call the result parent net debt.

## New primary sources

CQP Q3 10-Q: https://www.sec.gov/Archives/edgar/data/1383650/000138365026000038/cqp-20260930.htm
CQP annual 10-K (waterfall p.35, exact ownership p.92): https://www.sec.gov/Archives/edgar/data/1383650/000138365026000005/cqp-20251231.htm
LNG Q3 slides: https://lngir.cheniere.com/_assets/_c825fb77538e72bc5ef0338780618c98/cheniere/db/778/7578/pdf/10_29_2026_3Q_2026_Earnings_Presentation_vF.pdf
