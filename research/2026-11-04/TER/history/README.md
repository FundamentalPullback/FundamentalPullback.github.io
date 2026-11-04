# Teradyne reported history and normalization

As of 4 November 2026. USD millions except percentage metrics. All inputs come from SEC 10-K/10-Q filings. This is an original factual dataset and derived analytical work, not a redistribution of filings.

Run `python3 reproduce.py` offline in this directory. Only the Python standard library is required. It rebuilds normalized CSV/JSON, working-capital CSV, and 31 reconciliation checks from the small factual input files. The numerical inputs are immutable reported facts with source IDs, XBRL tags and exact source anchors. `sources.json` resolves source IDs to SEC URLs. Raw filings are deliberately excluded.

## Coverage

- FY2023–FY2025, latest four quarters Q4FY2025–Q3FY2026, comparable Q4FY2024–Q3FY2025, 3M/6M/9M support schedules, and TTM September 2026 versus September 2025.
- Revenue, GAAP operating profit (EBIT), attributable net income, CFO, cash capex, depreciation, CF amortization, D&A, SBC, restructuring/other, acquisition-intangible amortization, tax and equity-method earnings.
- Semiconductor Test, Product Test and Robotics revenue, segment pretax earnings, D&A and capital additions, including derived margins and trailing periods.
- Working-capital balance facts are supplied separately, without pretending that balance-sheet movements equal cash-flow movements. Acquisition, FX and classification changes can affect that comparison.

## Calculation conventions and limitations

1. Q4 = annual minus nine months. Quarterly cash-flow items = year-to-date change. Q2/Q3 income-statement and segment values prefer directly reported three-month values; missing cash flows remain YTD differences. TTM = previous full year + current nine months − prior nine months. No annualization of one exceptional quarter.
2. `ebit` is GAAP OperatingIncomeLoss. `net_income` is the reported attributable NI. Noncontrolling interests are explicitly recognized where disclosed. Equity-method income is separate and not included in industrial EBIT or EBITDA.
3. `da` = depreciation + cash-flow amortization. Acquisition-intangible amortization is a separate subset, not added twice. EBITDA = EBIT + D&A; SBC remains an expense.
4. `sbc_cf` is the cash-flow adjustment. Annual FY2023–FY2025 expense is independently verified in the SBC note and equals $57.682m/$60.122m/$63.999m. Interim standalone expense is not separately established in this package; missing expense fields are absent, not zero. `sbc_apic` is the stockholders-equity credit and must not be substituted for P&L expense or CF SBC. No separately disclosed capitalized SBC balance was identified in the reviewed filings; do not assume zero or infer it from APIC differences.
5. `fcf` = CFO − cash capex. `fcf_after_sbc_cf` subtracts the CF SBC adjustment as a conservative economic-cost proxy, not a GAAP measure or independently verified quarterly P&L SBC amount. Maintenance and growth capex are not split, so all cash capex is deducted.
6. Segment profitability is income before income taxes and equity in affiliate earnings, NOT consolidated EBIT. Corporate/eliminations include interest, FX, intercompany eliminations, severance, pension actuarial effects and acquisition/divestiture expenses. Segment capital additions differ from cash capex. These distinctions are intentional.
7. `ebit_before_restructuring_and_acquisition_amortization` is a sensitivity bridge only. Recurring restructuring and acquisition activity means it is not automatically normalized sustainable profit. Inventory write-downs remain a recurring operating cost; no automatic addback is made.
8. No normalized tax-rate assumption is imposed. Reported effective rates are calculated on pretax income before affiliate earnings. FY2024's 9.77% and FY2025's 12.14% are below 9M2026's 14.37%; forecasting from the lowest historical rate would be optimistic.
9. Most source facts are precise to $0.001m. The extraction selects the primary financial-statement occurrence before rounded narrative repetitions. Segment history uses the latest comparative presentation where available; taxonomy labels and historical reorganizations warrant caution in interpreting long-run segment trends.

## Material accounting and cycle findings

- TTM revenue $5,000.771m, EBIT $1,605.983m, CFO $1,329.514m, cash capex $304.650m and FCF $1,024.864m. After CF SBC of $80.087m, the economic FCF proxy is $944.777m, versus $394.411m a year earlier.
- The earnings jump is real in reported figures but cyclical extrapolation is unsafe: Semiconductor Test segment pretax margin moved from 42.14% in Q1FY2026 to 38.09% in Q2 and 34.23% in Q3. Robotics improved to approximately breakeven in Q3, but TTM pretax margin remains −7.78%.
- FY2025 restructuring/other was $38.554m, including rounded narrative severance $29.4m, asset impairment $4.9m and acquisition/divestiture expenses $2.3m. Those narrative components are not an exact full reconciliation. Note Q and MD&A differ in their rounded Product Test severance allocation ($2.0m versus $1.8m); do not rely on that sub-allocation.
- 9M2026 restructuring/other was $8.455m, including rounded $4.5m acquisition/divestiture expense and $3.4m severance. Q3 total was $1.997m. TTM restructuring/other $23.537m and acquisition-intangible amortization $15.897m are separately visible.
- Important XBRL trap: the Q3FY2026 tag ImpairmentOfIntangibleAssetsFinitelived carries $42.6m, but the note describes fully amortized assets removed from gross cost and accumulated amortization, explicitly saying no intangible impairment occurred in 9M2026. It is NOT an impairment addback and is excluded.
- Technoprobe is equity-accounted on a three-month reporting lag; the earnings line includes TER's share of income/loss and amortization of the equity-method basis difference. FY2024/FY2025 contribution was −$7.211m/−$19.914m; 9M2026 −$3.277m; Q3 +$3.281m; latest TTM −$6.482m. Do not include affiliate accounting earnings in industrial operating income, or double-count them when valuing the stake separately.

## QA

All 31 checks pass: segment revenues reconcile to consolidated revenue, applicable pretax/tax/affiliate/NCI bridges reconcile to attributable NI, and latest TTM equals the four-quarter sum for seven core metrics. Checks validate arithmetic, not economic sustainability. Missing data are deliberately not fabricated.
