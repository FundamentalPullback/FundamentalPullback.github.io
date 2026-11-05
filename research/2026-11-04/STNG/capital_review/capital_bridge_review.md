# STNG capital bridge source review
As-of information cutoff: November 4, 2026. Completed shortly after UTC midnight. Read-only research, not a price target.

## Findings that change model construction
1. $655.000M is contractual principal: $605M convertible notes and $50M secured facility. $718.621M is total noncurrent accounting liabilities, comprising $522.534M debt host/book debt and $196.087M embedded conversion derivative. Neither $718.621M nor $655M+$196.087M should be mechanically combined with full conversion dilution.
2. Actual indenture default is combination settlement, specified cash $1,000 per $1,000 principal. Issuer has discretion to choose physical shares, cash, or combination; default is not a mandatory cash-principal-only restriction. Changes/fixing of methods require public disclosure. No STNG change announcement found in targeted searches, but absence is not exhaustive proof.
3. October 26 issued/outstanding shares: 51,078,851. Do not add Q3 EPS restricted-stock dilution mechanically to these shares. Annual report identifies restricted shares as issued and includes unvested shares in ownership percentages based on total outstanding shares. Latest outstanding is a point-in-time denominator, unlike 45.699101M Q3 basic weighted average and 48.783074M Q3 diluted excluding notes. Exact unissued RSUs at October 26 remain unquantified; Q3 description newly refers to RSUs as well as restricted stock. Treat future awards as a separate explicit assumption.
4. Remaining newbuild/JV cash commitments $1,295.9M already INCLUDE the VLCC JV. They are not all value destruction: a NAV approach must include corresponding newbuilding value or net contract value; DCF must align associated future cash flows and capex. Do not both deduct all commitments from cash and include their capex again in DCF.

## Convertible note evidence and coherent scenarios
Primary legal source: https://www.sec.gov/Archives/edgar/data/1483934/000114036126014289/ef20070255_ex4-1.htm (April 10 indenture, definitions and section 5.03).
Primary issuance summary: https://www.sec.gov/Archives/edgar/data/1483934/000114036126014289/ef20070255_6k.htm .
Second tranche: https://www.scorpiotankers.com/scorpio-tankers-inc-announces-closing-of-convertible-senior-notes-due-2031-and-concurrent-stock-repurchase-2/ .

$375M issued April 10 plus $230M issued May 12; second tranche is same series, priced 110.25% of par. Coupon 1.75%, maturity April 15 2031; coupon dates April/October 15. The May premium is historical financing cash, not incremental principal owed. Conversion initially 9.9615 per $1,000; Q3 current rate 10.0791 implies $99.2152 conversion price and 6.0978555M shares on all $605M. Subsequent dividends may adjust rate further: do not preemptively use a future rate without issuer/legal calculation.

Before Jan15 2031 conversion requires specified conditions; stock-price condition is >130% conversion price on >=20 of preceding quarter's last30 trading days. Other conversion triggers exist. Physical-settlement dilution is a scenario, not an assertion that shares are currently issued or conversion is presently eligible. Make-whole changes can increase the rate in specified corporate events.

Suggested modeling alternatives, with N=51.078851M and C=6.0978555M:
- Debt/par case: equity value = operating EV + nonoperating assets + cash - $655M, divided by N. State that this is a simplified debt treatment, not a full option valuation if shares are above conversion price.
- Full physical conversion: subtract only $50M secured debt and divide by N+C=57.1767065M. Remove the entire convertible claim, including derivative; do not retain $605M principal debt.
- Default combination scenario at constant modeled price P above $99.2152: subtract $655M principal and add approximate incremental shares max(C-605/P,0) million. This is a simplifying scenario; contractual settlement actually uses 40-day VWAP observations. Below conversion value, holders would ordinarily retain the debt rather than voluntarily convert for less than par.
- Cash settlement: subtract a modeled conversion/option claim rather than merely par if material; no conversion shares. Accounting derivative fair value cannot be mixed indiscriminately with contractual par or inferred diluted shares.

## Cash, capital demands, and sales
Q3 source (tables supplied locally, direct primary source verified): https://www.scorpiotankers.com/scorpio-tankers-inc-announces-financial-results-for-the-third-quarter-of-2026-and-an-increase-to-its-quarterly-dividend/ . SEC equivalent https://www.sec.gov/Archives/edgar/data/1483934/000162828026067899/q32026earnings-exhibit991.htm .

Sep30 cash $2,042.088M; Oct26 unrestricted cash $2,051.865M; Oct26 principal debt $655M gives $1,396.865M net cash. $483.2M undrawn revolver is liquidity, not cash/equity. Separate undrawn $90M facility also not cash or current debt; commitment fee 0.42%, eligible borrowing until Oct31 2027. No scheduled debt principal payments through end2027; $8.7M in2028 and $646.3M thereafter. Interest and operational liquidity needs remain.

Future installment schedule ($M): Q4 2026 45.6; Q1 2027 45.0; Q2 104.2; Q3 96.9; Q4 52.1; 2028 481.9; 2029 379.2; 2030 91.0. Total 1,295.9. Company paid 185.7M to Oct26 including delivered STI Moxie. The future schedule covers eight LR2, five MR, four directly owned VLCC newbuilds plus minority VLCC JV contributions. No second deduction for original headline vessel order prices or paid deposits.

Illustrative liquidity reservation, not NAV: Oct26 cash - all debt principal - remaining installment commitments = $100.965M, before future operating cash, vessel sales, dividends, drydock and minimum cash needs. This deliberately conservative earmarking calculation is not 'surplus distributable cash'. Q4 drydock estimate $11.3M; 2027 $19.6M aggregate. Declared dividend $0.75 payable Dec4, record Nov13 implies ~$38.309M using Oct26 shares (actual record-date denominator can differ).

STI Dama $37.5M closed September and already included in cash. STI Elysees $70M and STI Veneto $73M expected to close Q4, still pending in Oct26 cash discussion. No later close announcement located by Nov4 targeted searches. $143M is gross agreed price; don't assert net proceeds or completed sale. For post-sale NAV either remove both ships from fleet and add net proceeds, or retain them as sale assets, not both. Sep30 assets held for sale are $72.804M book value: don't add this book asset on top of $143M sale proceeds. July sales $320.8M aggregate already reflected in Sept cash and fleet; do not add again.

## Investments and other assets
Volare: October purchase 2.4M shares for $38.4M, passive ~3.4% stake. Treat paid cost as provisional valuation only if no market price verified. Oct26 cash likely reflects October purchase disclosed in same release, but exact payment date not specified; flag reconciliation if using September cash. Never subtract purchase a second time from Oct cash without evidence that unpaid. September balance sheet excludes October stake.

Ampera: 9M CF investment $12.004M, versus $10M at H1. Do not use original $10M announcement as latest cost. Lack of current independently assessed fair value means cost/haircut sensitivity only.

VLCC minority JV: <15%; eight VLCCs delivering Q3 2029–Q2 2030. Invested 9M $7.381M; remaining contributions already in $1,295.9M schedule. Do not value all eight ships as STNG-owned or consolidate all JV debt. Separate from Volare and legacy dual-fuel JV.

Legacy dual-fuel JV: Dec2025 carrying value $13.023M; 9M income $2.113M and distributions $3.813M imply $11.323M carrying value absent other changes (inference, not reported Sept carrying figure). If capitalized separately, remove its earnings from operating value; if included in operating cash flow valuation, do not add entire stake again.

Sep30 Other assets $65.516M is composite, not a standalone investment portfolio to add alongside all above. Dec2025 $59.834M consisted of pool working-capital contributions $39.644M, dual-fuel JV $13.023M, capitalized loan fees $6.817M, other $0.350M. Q3 does not provide full updated breakdown. Pool capital belongs in operating working capital unless constructing a liquidation release; do not call it freely available cash. Ampera and VLCC JV plausibly enter composite Other assets, but classification not separately verified in Q3. Use named-investment addbacks and exclude composite Other assets or disclose inability to fully reconcile.

## Remaining limitations
- Latest awarded/unissued RSUs and full point-in-time restricted-share reconciliation not furnished in quarterly release. 51.078851M is verified outstanding, not a certification of all future contingent awards.
- Exact September other-assets composition unavailable in release. Legacy JV roll-forward inferred only.
- No verified market price for Volare, no external fair valuation for Ampera, no newbuilding market appraisal.
- No assertion of vessel-sale closing or changed default settlement after Oct28 based solely on failure to locate news.

## Saved source trail
Local original Q3 financial/CF/commitment tables remain ../sources_private/q3_table_02.txt, q3_table_04.txt, q3_table_05.txt, q3_table_09.txt and q3_table_10.txt. Local indenture.html and indenture_text.txt preserve legal contract; may_closing.html preserves second issuance. 2025_text.txt preserves annual ownership/other-assets footnotes; original 2025.html remains in sources_private. indenture_source_web.json records online verification.
