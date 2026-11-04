# Freshpet FCFF audit: final recheck

November 4, 2026, 11:52 UTC, after earnings release and prepared remarks, before call/Q&A. **Ready with caveats for scenario research.** No arithmetic blockers remain in the reviewed model. This audit does not independently recommend a trade. All parent-model edits were made by the parent, not silently by this auditor.

## Verified latest results

| Scenario | Value/share | Fixed-exit business IRR | Stylized equity-distribution/refinancing IRR | Reverse WACC |
|---|---:|---:|---:|---:|
| Adverse | $10.92 | −9.08% | −13.08% | 3.90% |
| Central | $44.38 | 4.52% | 4.59% | 7.82% |
| Favorable | $84.79 | 12.07% | 12.91% | 10.64% |

The supplied comparison price is the parent's November 3 close of $69.60; this audit did not independently verify market data. Reverse WACC is not an expected shareholder return because changing the discount rate also changes terminal value. The equity metric assumes immediate excess-cash distribution, later cash distributions, debt refinancing, assumed interest/tax shields and an option-settlement proxy. Do not label it actual stock CAGR or promised dividends.

Recalculation matches model_results.json. Each year's economic EBITDA bridge, EBIT, FCFF, capacity ceiling and the final common-equity/options/debt/cash reconciliation pass. The latest code SHA256 is c824f68356ea9793d5b6d259149a6f3dbc0654183836faed50e2bfed574b56f8.

## A reasonable joint alternative, independently matched

A 9.97% decade revenue CAGR, $3.120bn year-10 sales, 23.27m households and $210.18 retail buy rate, issuer-style EBITDA margin rising from 20.5% to 27%, 3% SBC and 6% total D&A, plus the explicit D&A bridge, produce 18.236% mature EBIT margin. At 9.5% WACC, 3% terminal growth and 20% terminal ROIC, this is worth **$68.34**. Business/equity proxy returns are **9.27%/9.86%**. Under the central 10.25% WACC and 18% ROIC, the same demand/margin path is worth **$58.92**.

This is a plausible but execution-dependent joint path, not a claim that all favorable assumptions will occur. It nearly supports $69.60 without demanding a fixed 15% return. The central 6.84% demand fade is cautious versus current 12.7% measured consumption, but its first-period 4% household growth already assumes recovery from rounded 1% panel growth, and its 25% mature EBITDA margin exceeds the 2027 target. Describe which assumptions are cautious and which require improvement rather than calling the entire case conservative.

## Required caveats retained

- Use rolling NTM1–NTM10. First-period $1,342.37m sales are 11.28% above September TTM but 8.28% above FY2026 guidance midpoint. The household-to-net-sales calibration is an assumption across differently scoped data, not a disclosed conversion ratio.
- Ongoing SBC is an economic cost and is not added back; no annual future-dilution layer is added. Existing ordinary-award dilution is only a weighted-average EPS-based proxy, not an exact current award inventory. Potential overlap with future expense on old unvested awards remains a small precision limitation, not a proven material double count.
- Principal plus a residual upper-strike option is internally coherent for matching convertible/capped-call terms. Do not also add gross convertible shares. Settlement, make-whole, counterparty and volatility assumptions remain. The risk-neutral option settlement proxy is not demonstrably a conservative physical expectation.
- Cash reserve, tax shelter, WACC, maintenance split, effective capacity, sales-capacity per investment dollar, working-capital ratio and terminal ROIC are analyst inputs. Operating rent stays in margins, finance leases stay in the debt bridge, and future leased assets still need an economic cost.
- Central capex remains approximately $1.5bn over ten years, with explicit terminal reinvestment. The installed-capacity and young-asset treatment does not create free perpetual growth. Current 16 production lines and productivity-released capacity do not independently verify the model's$1.6bn effective starting capacity.
- There is no exact ongoing company-guided D&A bridge: the corrected 0.23634 percentage-point uplift is a transparent normalization based on the present TTM difference, extended as an analyst assumption.

## Appendix: preserve original versus corrected outputs

| Item | Initial model | After explicit D&A bridge |
|---|---:|---:|
| Adverse value/share | $10.48 | $10.92 |
| Central value/share | $43.63 | $44.38 |
| Favorable value/share | $83.70 | $84.79 |
| Joint alternative value/share | $67.31 | $68.34 |
| Central, illustrative FY26-midpoint rebase | $44.68 | $45.45 |

The correction adds (TTM CFO D&A $96.668m minus issuer-reconciliation D&A $93.817m)/TTM revenue $1,206.299m =0.23634 percentage points to economic EBITDA before subtracting total D&A. It does not increase the issuer-style guide margin. The initial adverse IRRs were also outside the original root bracket; that reporting defect was corrected and never affected per-share valuation.

The rebasing countercheck increases starting sales and the household-to-net-sales calibration proportionally to FY26 guidance midpoint $1,239.767m. It is a sensitivity only, not a silent recasting of observed households/buy rates. The $1.07 corrected valuation increase does not remove the main operating-assumption debate.

Sources: [Q3 release and statements](https://investors.freshpet.com/news-releases/news-release-details/freshpet-inc-reports-third-quarter-2026-financial-results); [Q3 prepared remarks, pp5–7](https://investors.freshpet.com/static-files/c7c74ec5-1ed3-410b-8411-deca2f2f769e); [Q3 presentation](https://investors.freshpet.com/static-files/f82d5c97-c5cc-4996-bcf7-5114ee716771); [Q2 10-Q](https://www.sec.gov/Archives/edgar/data/1611647/000161164726000018/frpt-20260630.htm). Local copies of these primary sources were inspected. Full diagnostic history is in audit_memo.md; its initial-model figures are superseded by this final recheck. Reproducible latest checks are in final_checks.py and final_checks.json; bridge/rebase details are in da_bridge_update.json.
