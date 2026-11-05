# Cheniere: committed reinvestment and terminal assumptions

**Evidence cut-off: 5 November 2026. USD millions unless specified.** This is a focused input review for consolidated FCFF, not a completed valuation. Exact historical amounts, management planning figures and analyst estimates are deliberately separated. A missing precise cash-to-complete schedule is a reason for a range, not for leaving valuation blank.

## Findings that change the model

1. **An issuer total-cost anchor exists.** The June 24, 2025 FID presentation, slide 8, shows approximately **$7bn for Stage 3 and $3bn for Midscale 8&9 plus debottlenecking**. These are rounded planning envelopes, not current contractual cash balances. The separate $2.9bn 8&9 EPC contract is not the only available cost evidence. [S1]
2. **Routine and major maintenance is already partly in EBITDA.** The 2025 accounting policy generally expenses maintenance and repairs, including planned major maintenance. The reported maintenance-capex number covers only qualifying capitalized sustaining work. Do not subtract all O&M again as replacement capex. Equally, $120–200m of capitalized maintenance cannot support a claim of perpetual operation without eventual asset renewal. [S2]
3. **Finance-lease acquisitions need explicit treatment.** New finance ROU assets were $472m in FY2025 and $545m in 9M2026. This is economically meaningful capital formation that is absent from cash PP&E. Finance ROU amortization and interest are excluded from EBITDA; operating rents are not. A financing treatment requires new finance-lease asset acquisitions in FCFF reinvestment, alongside existing finance debt in the equity bridge. [S2, S3]
4. **Contract protection ends at different times.** Consolidated production coverage is about 95% through the mid-2030s, with about 15 years weighted remaining life. CQP alone reports about 90% third-party coverage/13 years; CCH alone reports over 80%/15 years. They are different perimeters. Those figures do not guarantee 95% of perpetual EBITDA. [S3–S5]

## Recommended working schedule

All future annual figures below are **analyst estimates, not management guidance or disclosed commitments payable in those years**. They exclude capitalized interest. Optional SPL Phase 1 and CCL Phase 1 are excluded from both capex and earnings.

| Base case | 2027 | 2028 | 2029 | 2030 | 2031 |
|---|---:|---:|---:|---:|---:|
| 8&9 plus debottlenecking, residual project spending | 650 | 400 | 50 | 0 | 0 |
| Stage 3 closeout/retentions allowance | 50 | 25 | 0 | 0 | 0 |
| Gregory Power Plant improvements | 250 | 150 | 50 | 0 | 0 |
| **Committed-project allowance** | **950** | **575** | **100** | **0** | **0** |
| Capitalized owned-asset sustaining work | 200 | 225 | 250 | 275 | 300 |
| New finance-lease ROU acquisitions, cash equivalent | 300 | 300 | 250 | 200 | 200 |
| **Total reinvestment before working capital** | **1,450** | **1,100** | **600** | **475** | **500** |

Project-only low/base/high cumulative 2027–31: **$0.975bn / $1.625bn / $2.500bn**. Including sustaining work and finance ROU acquisitions, the corresponding cumulative envelopes are **$2.575bn / $4.125bn / $6.925bn**. These are scenario bounds, not probabilities or statistical confidence intervals. `inputs.json` contains component-level low/base/high arrays.

The parent model's more cautious project schedule of **$1.10bn/$0.75bn/$0.15bn/zero/zero** is also inside a defensible range. It is approximately $375m above this working base cumulatively, mainly a reserve for Gregory, owner costs, completion timing and cash/accrual uncertainty. It should not be called an issuer forecast.

### Basis and uncertainty of the project schedule

- At December 2025, the remaining EPC obligations were approximately $700m for Stage 3 and $1.6bn for 8&9. The 9M2026 project cash spending was approximately $1.1bn and $709m respectively. The categories do not match: project cash includes more than EPC work and settlement of past accruals; the annual commitments represent outstanding contractual work. Subtracting $1.1bn from $700m to conclude negative Stage 3 capex is invalid. [S2, S3]
- FY2025 consolidated spending was approximately $1.3bn for Stage 3 and $1.0bn for 8&9. Together with $709m in 9M2026 and the rounded $3bn project envelope, 8&9 clearly has a finite, estimable residual rather than an unknown multi-billion-dollar blank. But pre-2025 expenditure, owner costs, changes, accruals and financing costs prevent an exact simple subtraction. [S1–S3]
- CCH's June 2025 internal contribution of $373m construction-in-process plus $124m other non-current assets is evidence of pre-existing project investment, **not an extra consolidated cash payment to add again**. The transfer and the $244m difference between consolidated and CCH 9M2025 project cash spending do not establish exact pre-2025 cash spending because cash, prepayments and capitalized cost bases differ. [S4]
- 8&9 was 58.6% complete overall but only 14.5% through construction at September 2026. Engineering/procurement was much further advanced. Neither 58.6% nor 14.5% is a cash-spend percentage. The expected substantial-completion date remains H2 2028, and no 2027 production contribution should be modeled. Base spending is concentrated in 2027–28 with a modest 2029 retention allowance. [S3, S4, S6]
- All seven Stage 3 trains were operating by August 2026, so future Stage 3 spending is closeout, not another free capacity expansion. A $25–150m cumulative 2027–28 allowance is a judgment range, not a disclosed payable.
- Gregory spent $245m in 9M2026 versus $82m in 9M2025, with continuing procurement and facility improvements disclosed. A **$200–750m cumulative 2027–29 allowance** is intentionally broad because no current total budget was found. The $136m January 2026 acquisition of the remaining ownership interest is historical financing/equity activity, not another future improvement cost. [S2, S3]
- No incremental commissioning proceeds are assumed in the table. If 2028 commissioning cargo cash offsets capex, recognize it once and avoid also counting that same pre-commercial margin in operating EBITDA. The table excludes capitalized interest because this is unlevered FCFF; do not add financing expenditure back into project capex while also valuing financing separately.

## Maintenance, depreciation and the terminal

### What is reported

The terminal/pipeline asset useful-life range is **6–50 years**, other fixed assets 3–10 years, and finance-leased marine assets 5–20 years. September 2026 gross terminal/pipeline assets were **$41.313bn**, construction-in-process $3.243bn and gross marine finance ROU assets $1.605bn. FY2025 depreciation was $1.320bn; Q3 2026 depreciation was $391m and total D&A was $393m. Annualizing the latter gives **$1.572bn**, before a full year of the last Stage 3 trains and later 8&9 capacity. [S2, S3]

### Practical assumptions

A D&A schedule of **$1.65/$1.72/$1.80/$1.82/$1.84bn for 2027–31** is a reasonable working estimate, not a source-disclosed forecast. Useful ranges are $1.55–1.80bn for 2027, $1.65–1.95bn for 2029, and $1.75–2.05bn for 2031. Approximately $1.9–2.2bn at a 2036 terminal is defensible as a modeling range after renewal and inflation, but cannot be mechanically derived from the broad 6–50-year lives.

The $200–300m explicit owned-asset capitalized sustaining schedule is above recent annualized maintenance capex and leaves ordinary/major expensed maintenance within the operating-cost forecast. It is reasonable for the next five years **only if the later forecast recognizes economic renewal**. It is not a validated engineering forecast of every replacement cycle.

For a going-concern terminal, use a coherent convention:

**Gross capex + change in operating working capital = D&A + NOPAT × g / incremental ROIC.**

Then terminal FCFF is NOPAT × (1 − g/ROIC), assuming no other adjustments. An incremental ROIC range of 8–12% is an analyst sensitivity; project management's >10% unlevered IRR is a different metric and should not be relabeled terminal ROIC. Fade the **combined owned-asset sustaining and finance-lease replacement** toward depreciation over 2032–36. Do not fade owned sustaining to all D&A and add a second full marine-replacement allowance on top: marine depreciation is already included.

This is a valuation convention ensuring the business pays for its productive assets. It is not proof that the cash replacement need equals accounting depreciation every year. For infrastructure with long-lived civil works, substantial expensed maintenance and lumpy refurbishments, a finite-life asset/runoff valuation is a useful cross-check, particularly if the perpetual case dominates enterprise value.

## Lease accounting: avoid the two opposite errors

The 2025 10-K identifies **$796m operating lease cost in operating expenses**, versus **$90m finance ROU amortization in D&A and $52m finance interest in interest expense**. September 2026 finance-lease PV was **$1.385bn**, versus operating-lease PV of $2.370bn. Existing finance cash payments for 2027–30 are $205m/$207m/$208m/$208m. [S2, S3]

Under the parent's chosen financing convention:

- Subtract the existing $1.385bn finance liability once in the EV-to-equity bridge. Do not also subtract its financing principal payments in FCFF.
- Add future new finance ROU acquisitions to capex as cash-equivalent asset investment. This prevents new ships' service capacity entering EBITDA without an acquisition/replacement cost. The base $300m/$300m/$250m/$200m/$200m path is below the recent expansion pace and includes tapering growth plus continued renewal. The first three years' reasonable broad sensitivity is approximately $150–600m a year, falling later. Exact annual additions are not disclosed.
- Keep operating rents, renewal rents and shipping operating expenses in EBITDA. Do not additionally subtract operating ROU acquisitions or the full operating liability unless the whole model is converted to capitalized operating leases, with matching earnings and reinvestment adjustments.
- The approximately **$6bn of future uncommenced lease payments** has no disclosed annual commencement ladder or finance/operating split in the reviewed Q3 note. It is undiscounted. An illustrative 10–15-year level-payment lease at about 6.2% has an inception PV around 64–73% of nominal payments, **before** discounting deferred commencement. Even that $3.8–4.4bn illustration must be split between operating and finance contracts. It is not another $6bn of current net debt.
- The decline in the existing operating payment ladder from $626m in 2027 to $300m in 2030 is not free EBITDA growth. Expiring charter coverage must be replaced where production/customer delivery requires it, or the associated business also declines.

The accounting split is strongly evidenced; the forecast finance-ROU schedule remains a disclosed modeling judgment.

## Contract renewal and terminal risk

The historical anchor is specific: Cheniere's **2016 10-K says first commercial delivery under BG's first-train fixed-price 20-year SPA occurred in November 2016**. The original term thus points to late 2036, absent later amendments or extension. This is an earliest-legacy illustration, not a reconstructed current contract ladder. Later trains and the QatarEnergy contracts through 2054 extend other cash flows much further. The conditional 1 mtpa tied to SPL Phase 1 is not free base-case capacity. [S6, S7]

For 2027–31, use current contracted cash economics and normalize exposed marketing margins. Do not impose a blanket expiry cliff solely because the forecast begins. For the terminal, test **0% favorable / 5% central / 12–15% adverse** aggregate normalized EBITDA reductions for contract rollover, competition, customer retention and cost recovery. These are analyst scenarios, not management guidance. For intuition, repricing 35% of a normalized profit base at 15% lower contribution gives a 5.25% aggregate reduction. An illustrative percentage of profits is not a statement that exactly 35% of current contracted volumes expires in 2036.

Apply the haircut to a sustainable future margin/earnings base, separately from a near-term marketing normalization already made. Do not accidentally charge the same normalizing LNG spread decline both through the earnings forecast and through an identical terminal risk overlay. Also avoid attaching the entire haircut abruptly to 2031. A long-horizon transition or a terminal sensitivity is more faithful to the disclosures.

Two additional checks:

- **Regasification expiry is mostly gross, not net.** The TotalEnergies TUA is a 20-year arrangement commencing in 2009. FY2025 regasification revenue was $136m, but related partial-assignment O&M paid to TotalEnergies was $134m. Automatically removing $136m of EBITDA in 2029 would materially overstate this particular expiry risk. Future renegotiation of service access still requires attention. [S2, S8]
- The 2025 filing lists major existing terminal export authorizations through **December 31, 2050**. A perpetual operating value assumes ongoing regulatory renewal, customer demand, feedstock access and adequate capital renewal beyond that date; it is not a claim that current permits guarantee perpetual operation. A 2050 runoff/finite-life sensitivity can show the consequence without asserting forced closure in 2050. [S2]

## Model checks

- Base post-8&9 capacity stays within management's **60–63 mtpa**, not the optional 71–75 mtpa expansion case.
- Base long-run operating economics anchor to **$7.3–8.0bn adjusted EBITDA** and management's **$4.1–4.7bn parent distributable cash flow** as a cross-check. Neither is FCFF. The exceptional $6.3bn midpoint of 2026 parent DCF is not a perpetual cash flow. [S6]
- Do not deduct NCI distributions from consolidated FCFF if the bridge already subtracts outside CQP common equity at market value.
- Do not grant debt proceeds, expansion EBITDA or tax shields for excluded unfunded projects. Already-incurred SPL development cost is sunk; any unavoidable future termination/remaining LNTP obligations require a separate reserve if identifiable, not the entire optional full-build budget.
- Forecast residual capex, finance acquisitions and renewal scenarios with visible ranges. Precise future cash and a complete amended contract ladder are unavailable in the reviewed sources, but the ranges above are sufficient for a transparent, sensitivity-tested valuation.

## Sources

S1. [Cheniere June 24, 2025 FID and corporate update, slides 7–8 and 13](https://www.sec.gov/Archives/edgar/data/3570/000000357025000088/a20250624chenierecapital.htm).
S2. [Cheniere 2025 10-K](https://www.sec.gov/Archives/edgar/data/3570/000000357026000005/lng-20251231.htm), accounting policy p66, PP&E note 5 pp71–72, leases note 11 pp84–85, regasification note 12 p86, commitments note 19 pp95–96, business pp8–9.
S3. [Cheniere Q3 2026 10-Q](https://www.sec.gov/Archives/edgar/data/3570/000000357026000038/lng-20260930.htm), PP&E note 4, leases note 9, operating model and investing cash flows.
S4. [CCH Q3 2026 10-Q](https://www.sec.gov/Archives/edgar/data/1693317/000169331726000011/cch-20260930.htm), note 1, PP&E note 4, business p21, construction/investing cash flows p28.
S5. [CQP Q3 2026 10-Q](https://www.sec.gov/Archives/edgar/data/1383650/000138365026000038/cqp-20260930.htm), business p22.
S6. [Cheniere Q3 2026 presentation](https://lngir.cheniere.com/_assets/_c825fb77538e72bc5ef0338780618c98/cheniere/db/778/7578/pdf/10_29_2026_3Q_2026_Earnings_Presentation_vF.pdf), slides 5–6, 12, 19, 21.
S7. [Cheniere 2016 10-K](https://lngir.cheniere.com/sec-filings/all-sec-filings/content/0000003570-17-000052/cei2016form10-k.htm), significant events p41. Historical anchor only.
S8. [CQP 2025 10-K](https://www.sec.gov/Archives/edgar/data/1383650/000138365026000005/cqp-20251231.htm), regasification revenues pp75–76.

Machine-readable inputs and source locations: `inputs.json` and `source_register.json`. No changes were made to the main valuation model.
