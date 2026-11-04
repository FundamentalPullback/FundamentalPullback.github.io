# CVI historical financial audit through September 30, 2026

All financial values are USD millions, except shares and explicitly identified ratios. This package covers the existing businesses before the pending Marathon asset acquisition and its equity/debt funding. The latest primary filing was published November 3, 2026.

## Consolidated results and cash conversion

FY2023/FY2024/FY2025 revenue was 9,247/7,610/7,162; EBIT 1,123/58/182; parent-attributable income 769/7/27; CFO 948/404/144. Gross cash PP&E capex was 205/179/185 and additional cash refinery-turnaround investment 57/53/197. CFO less both cash investment categories was 686/172/−238.

TTM September 2026 versus prior TTM: revenue 9,810 versus 7,299; EBIT 562 versus 298; parent income 265 versus 166; CFO 1,026 versus 242. Gross PP&E cash capex is 207 versus 185, and cash turnaround spending 3 versus 203. CFO less these investments is 816 versus −146. Company FCF adds investment-capital returns of 7 versus 10, reaching 823 versus −136. Neither measure is automatically attributable wholly to CVI common equity: both include 100% of consolidated CVR Partners/UAN.

The swing is not simply sustained earnings growth. TTM cash turnaround investment fell 200, and 9M2026 cash income taxes were zero while tax payable increased 132. TTM cash taxes were net refunds of 8 versus 3. RIN liability releases and derivatives remeasurement complicate the earnings/CFO bridge. Recurring modeling must retain a through-cycle refinery-turnaround cash reserve even when a particular trailing year has only 3 of cash spending.

## Ex-UAN operating history and normalization anchors

Consolidated EBIT less UAN EBIT, retaining corporate costs, eliminations, and the former Renewables segment:

- FY2023: 922 EBIT; 218 D&A; 1,140 EBIT plus D&A.
- FY2024: −32 EBIT; 210 D&A; 178 EBIT plus D&A.
- FY2025: 53 EBIT; 321 D&A; 374 EBIT plus D&A.
- TTM September 2026: 426 EBIT; 294 D&A; 720 EBIT plus D&A.
- Prior TTM September 2025: 141 EBIT; 249 D&A; 390 EBIT plus D&A.

Pure Petroleum company EBITDA was 1,185/223/411 for FY2023/24/25 and 747 for TTM September 2026. This company EBITDA begins with segment net income and can contain below-operating items, so it is distinct from EBIT plus D&A. Subtracting only the specific 488 waiver from FY2025 produces −77; subtracting the 253 waiver from current TTM produces 494. A waiver-only bridge is incomplete because it leaves other RFS remeasurements, inventory effects, and derivative gains/losses.

Company-adjusted Petroleum EBITDA, which also removes RFS remeasurement, unrealized derivative marks and inventory valuation effects, was 903/138/199 in FY2023/24/25, and 693 in the current TTM versus 137 in the prior TTM. This remains before a recurring cash turnaround reserve, maintenance capital, corporate cash costs, and cash taxes. The very wide range argues for a through-cycle anchor rather than annualizing the latest quarter. Petroleum quarterly EBIT was −13/−193/5/738 in Q4 2025/Q1 2026/Q2 2026/Q3 2026.

Consolidated commodity derivative P&L was +5/+13/+22 in FY2023/24/25. Unrealized P&L was +32/−22/+4; total minus unrealized implies realized −27/+35/+18. Current TTM total P&L is −513, including unrealized −268 and inferred realized −245. In 9M2026, total loss516 minus unrealized loss278 implies realized loss238. Company-adjusted EBITDA removes unrealized marks but retains realized hedge losses. Do not add back all hedging losses as if they were noncash; do not attribute consolidated derivative residuals entirely to Petroleum without checking segment allocation.

Renewables D&A increased 90 in FY2025 primarily because of accelerated depreciation after reverting the Wynnewood renewable diesel unit to hydrocarbon service. The filing does not quantify all 90 as a single separately measured nonrecurring charge; use 90 as the disclosed increase, not an exact impairment addback. D&A403 consolidated in FY2025 is not a maintenance-capex forecast.

## Turnaround classification and segment boundaries

Petroleum capitalizes turnarounds, while Nitrogen Fertilizer expenses them in direct operating costs. Nitrogen turnaround expense was 27 in Q3 2026 and 29 in 9M2026, versus 1 and 2 in the comparative periods. Do not subtract it again as investing capex or remove it permanently from normalized earnings. The East Dubuque turnaround completed in October with an approximately 37 total project cost.

Refinery turnaround capitalized additions and cash payments are different: 9M2026 additions5 versus cash2; 9M2025 additions189 versus cash196. Segment capex tables are accrual additions excluding capitalized turnarounds, not the cash capital expenditures in the consolidated cash-flow statement. For example, FY2025 consolidated segment capex197 versus cash PP&E capex185; 9M2026 segment capex147 versus cash152.

2025 had separate Petroleum, Renewables and Nitrogen segments. The 2026 presentation retains renewable-fuel activity in other/reconciling items. Ex-UAN consolidated operating history retains that activity and corporate costs, while pure Petroleum history does not. Preserve source dimensions and do not sum overlapping product, intersegment and consolidation-axis observations.

## Cash, debt, NCI, shares and compensation

September 2026 cash is 1,278 including UAN158; total carrying debt including finance leases1,781; NCI book equity172. UAN is consolidated because of control, despite CVR owning approximately37% of common units; IEP's separate3% does not belong to CVI. Book NCI is not a fair-value deduction for a listed minority stake. A sum-of-parts model should consistently exclude UAN cash/debt/earnings and add only CVR's own stake, or use a fully consolidated approach with appropriate minority fair value.

FY2023 ending cash-flow cash total1,186 included unrestricted cash581, reserved debt funds598 and restricted cash7. The reserved/restricted amounts were released in Q1 2024 and must not be treated as new operating cash. Cash-flow cash totals and freely available cash are not interchangeable.

All FY2025 share-based awards were liability-classified, remeasured with share/unit prices, and not potentially dilutive. The optional FCF-minus-SBC sensitivity in history.json is not owner FCF and can double count cash settlements already reflected in CFO. Negative quarterly SBC may reflect remeasurement, not a windfall recurring operating benefit. Q3 2026 cash-flow-derived SBC27 differs from separately reported compensation expense26 due to reported-period rounding; retain the distinction.

Actual cover shares and weighted shares remain in observations.json. Do not derive Q4 weighted shares by subtraction; do not use historical weighted shares as the forward denominator after the announced financing. Current acquisition restrictions and any financing proceeds belong in the separate capital/pro-forma bridge, not these historical statements.

## Rebuild, checks and limitations

Run `python rebuild_history.py` then `python check_history.py`. Only standard Python and selected local observations/normalization facts are needed. No filings, internet, extraction libraries or copied source tables are required. Each calculated financial record retains source observation IDs/URLs; ex-UAN adjusted records point to normalization observation IDs.

Cash-flow quarters use YTD differences and Q4 uses annual less nine months. Income-statement quarters prefer directly reported figures. Q3 2026 reported revenue3,281 differs from YTD-derived3,282; current TTM9,810 follows annual plus current9M minus prior9M. Quarterly cash-flow D&A78 differs from income-statement79. These are retained reported rounding differences, not balanced away. Missing values stay null.

Only public_whitelist.json files are distributable. The sources directory contains downloaded filings and extraction work and must remain private.
