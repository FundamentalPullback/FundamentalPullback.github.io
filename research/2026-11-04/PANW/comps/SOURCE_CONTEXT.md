# Fortinet operating context: Check Point and Palo Alto Networks

As of November 4, 2026. All monetary values are USD millions. Run `python reproduce.py` offline with Python 3 to regenerate the JSON, CSV and reconciliation checks from compact source-mapped inputs. Source excerpts are included; full filings are excluded.

## Calendar and perimeter

FTNT and CHKP latest quarters both cover July 1–September 30, 2026. CHKP published its Q3 2026 results November 2. PANW's latest published quarter is fiscal Q4 2026, covering May 1–July 31, released September 1. On November 3, PANW announced that its October 31 quarter will be released November 18, after the US close. Do not label PANW's July figures as September-quarter results or imply its October results are already available. Calendar source: the `panw_calendar` URL in inputs.json.

CHKP quarterly and nine-month 2026/2025 figures and PANW quarterly/full-fiscal-year 2026/2025 figures are provided. FY and nine-month data have different durations and must not be directly ranked against each other. No valuation multiples, DCF or inferred organic-growth comparison is included.

## Latest-quarter observations

- FTNT: revenue 2,078.4; GAAP EBIT 704.3 (33.9%); CFO 946.0; cash PPE 64.2; cash-flow SBC 80.1; CFO less capex 881.8; company FCF 864.8 after removing 17.0 escrow proceeds.
- CHKP: revenue 669.8; GAAP EBIT 177.2 (26.5%); CFO 264.3; PPE 6.4; no prepaid-lease or capitalized-software cash spending in this quarter; SBC 54.8; FCF and adjusted FCF both 257.9.
- PANW: revenue 3,410; GAAP EBIT 172 (5.0%); CFO 1,357; property/equipment/other-assets spending 103; cash-flow equity-award SBC 460; FCF 1,254; adjusted FCF 1,289.

The latest-quarter cash-flow SBC/revenue ratios are 3.9%, 8.2% and 13.5%, respectively, but the fiscal dates and acquisition scope differ. These are descriptive indicators, not a normalized ranking. FCF less SBC is only a dilution-cost sensitivity and is not reported FCF or a complete per-share ownership model.

## Cash-flow definitions matter

CHKP subtracts property/equipment, prepaid-lease payments and capitalized internal-use software before reporting FCF. It then adds acquisition-related cash costs for adjusted FCF. Q3 2025 FCF of 74.8 included a 159.9 prepaid-lease outlay: CFO less ordinary PPE alone was 234.7. Consequently Q3 2026 FCF growth greatly overstates improvement in recurring cash generation if that prior lease payment is ignored. Nine-month 2026 capital spending includes PPE 22.9 and software 3.6; adjusted FCF 875.9 adds 21.4 acquisition-related costs to FCF 854.5. These are not acquisition purchase-price cash payments, which are separately reported.

PANW subtracts purchases of property, equipment and other assets. The latest quarter adds back 7 corporate-asset spending and 28 acquisition-related cash costs to reach adjusted FCF. FY2026 adjustments total 301: headquarters land 91, corporate assets 42, acquisition-related payments 164, and litigation payment 4. Comparing PANW adjusted FCF directly with FTNT's unadjusted capital spending overstates relative cash conversion. Both base and adjusted figures are retained.

PANW capitalizes internally developed security software. Its FY2026 net software balance was 266 versus 167 a year earlier, with annual software amortization 104. This is a net book-value disclosure, not a separate cash-additions figure. A distinct quarterly software cash amount is not disclosed in the reviewed schedules; do not assign zero or infer cash spending from the balance difference. Retain the reported property/equipment/other-assets cash subtotal of 103 for the quarter and 440 for the year.

PANW's latest quarter SBC-related operating adjustment of 487 includes a broader definition than cash-flow equity-award SBC. The latter is 1,774 annual less 1,314 nine-month = 460. The prior quarter comparator is 1,295 less 941 = 354. Both definitions are retained in inputs; do not substitute 487 for 460 without relabeling. Even cash-flow SBC definitions can differ in liability-award treatment across companies.

## Earnings and acquisitions

CHKP Q3 EBIT includes a 25 reduction in R&D expense for expected Israeli grants; the nine-month benefit is 80. Subtracting that benefit as an isolated sensitivity gives Q3 EBIT of 152.2 (22.7%), not a company-reported adjusted result. The grant's accounting recognition does not by itself prove current cash receipt. Q3 2025 net income also contained a one-time tax benefit, so raw EPS growth is not a clean operating comparison.

CHKP acquired Cyata and Cyclops in February 2026 and Rotate's talent that month, following Lakera in October 2025 and Veriti in June 2025. The 2026 nine-month cash-flow statement shows 94.4 net acquisition cash payments. Do not infer an organic revenue bridge from total reported growth; acquisition revenue contributions were not separately quantified in the reviewed quarterly release. Primary acquisition chronology source: `chkp_acquisitions`.

PANW acquired Chronosphere January 29, 2026 for 2,951 total consideration, and CyberArk February 11 for 21,061. It also acquired Koi April 14 and Portkey May 29. Thus prior-year quarterly comparisons exclude businesses and acquired-intangible amortization now in the group. FY2026 acquisition contributions and costs, rather than an invented organic bridge, support the perimeter caveat. Embrace and Console closed after fiscal year-end, August 27 and September 1, respectively; neither belongs in FY2026 historical operations. Source: PANW 2026 10-K, Note 8 and subsequent-events note.

FTNT's Linksys consolidation started January 31, 2025. Unlike its current/prior TTM comparison, both September quarters include a full quarter of Linksys, but that does not establish organic growth or eliminate other acquisition effects. The separate Fortinet history package documents these limitations.

## Files

`inputs.json` contains reported numbers, primary URLs and table/row/column provenance. `operating_comparables.json` and `.csv` contain explicit start/end dates and derived margins. `checks.json` verifies every base and adjusted FCF bridge. `excerpts/` holds the compact evidence, including grants, software capitalization and acquisition disclosures. None of these calculations is a trading recommendation.
