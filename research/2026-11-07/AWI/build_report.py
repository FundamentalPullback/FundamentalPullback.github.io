import json,pathlib,html,copy,importlib.util
P=pathlib.Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('calc',P/'model.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
H,A,O=m.H,m.A,m.OUT
sources=[
('https://s202.q4cdn.com/826259286/files/doc_financials/2025/ar/2025-Annual-Report-Final.pdf','Armstrong World Industries 2025 Annual Report','2026-02-24','FY2023–2025 financial statements; segments; WAVE; pension, software, leases, cash taxes and acquisition notes; supplemental 2021–25 context.'),
('https://www.sec.gov/Archives/edgar/data/7431/000119312525252201/awi-20250930.htm','Armstrong World Industries Q3 2025 Form 10-Q','2025-10-28','Nine-month 2024 and 2025 comparatives for prior TTM.'),
('https://www.sec.gov/Archives/edgar/data/7431/000119312526183484/awi-20260331.htm','Armstrong World Industries Q1 2026 Form 10-Q','2026-04-28','Q1 actuals and cash-flow seasonality.'),
('https://www.sec.gov/Archives/edgar/data/7431/000119312526318838/awi-20260630.htm','Armstrong World Industries Q2 2026 Form 10-Q','2026-07-28','Q2 actuals; six-month cash flow used to derive standalone quarterly cash flow.'),
('https://www.sec.gov/Archives/edgar/data/7431/000119312526432651/awi-20260930.htm','Armstrong World Industries Q3 2026 Form 10-Q','2026-10-27','Latest actuals and balance sheet; operating drivers, acquisitions, WAVE, tax, debt, shares and contingencies.'),
('https://investors.armstrong.com/news/news-details/2026/Armstrong-World-Industries-Reports-Third-Quarter-2026-Results/default.aspx','Armstrong World Industries Q3 2026 results','2026-10-27','Current guidance, price/volume/organic acquisition bridge and cash-flow commentary.'),
('https://investors.armstrong.com/news/news-details/2026/Armstrong-World-Industries-Reports-Record-Setting-Fourth-Quarter-and-Full-Year-2025-Results/default.aspx','Armstrong World Industries FY2025 results','2026-02-24','Adjusted FCF reconciliation, including $20m full-year and $10m fourth-quarter nonrecurring cash tax benefits.'),
('https://investors.armstrong.com/events-and-presentations/default.aspx','Armstrong World Industries events and presentations','2026-11-07','Calendar verification; no upcoming earnings date surfaced in retrieved primary page.'),
('https://investors.armstrong.com/overview/default.aspx','Armstrong World Industries investor relations overview','2026-11-07','Latest confirmed results and call occurred October 27, 2026.'),
('https://stockanalysis.com/stocks/awi/statistics/','Armstrong World Industries statistics and valuation','2026-11-07','November 6 regular closing price, beta and non-controlling standardized ratio cross-check.'),
('https://stockanalysis.com/stocks/csl/statistics/','Carlisle Companies statistics and valuation','2026-11-07','November 6 price and trailing P/E; building-envelope comparable.'),
('https://stockanalysis.com/stocks/wts/statistics/','Watts Water Technologies statistics and valuation','2026-11-07','November 6 price and trailing P/E; specification-led building-products comparable.'),
('https://stockanalysis.com/stocks/oc/statistics/','Owens Corning statistics and valuation','2026-11-07','Cyclical building-products comparator; negative trailing earnings exclude P/E comparison.'),
('https://www.federalreserve.gov/releases/H15/Current/','Federal Reserve H.15 selected interest rates, November 6 release','2026-11-06','Risk-free anchor of 4.84%, latest observation available in retrieved release; not labeled November 6 closing yield.')]
(P/'source-ledger.json').write_text(json.dumps([dict(url=u,title=t,date=d,purpose=p) for u,t,d,p in sources],indent=2))
def fmt(v):return f'{v:,.1f}'
def tbl(periods):
 s='Period | Sales | EBIT incl. affiliates | Core EBIT | Net income | CFO | Capex | WAVE cash | FCF incl. WAVE | SBC\n---|---:|---:|---:|---:|---:|---:|---:|---:|---:\n'
 for p in periods:s+=p+' | '+' | '.join(fmt(H[p][k]) for k in ['revenue','ebit','core_ebit','net_income','cfo','capex','jv_distribution','fcf_including_jv','sbc'])+'\n'
 return s
extra=[]
for maint in [.045,.05,.055,.06]:
 c=copy.deepcopy(m.CASES['base']);c['maintenance_ratio']=maint;extra.append({'maintenance_capex_sales':maint,'value':m.valuation(c)['value']})
# Separate sensitivity: WAVE current earned cash can be distributed rather than retained, not the approved base model.
jv_zero_retention=copy.deepcopy(m.CASES['base']);jv_zero_retention['jv_roe']=1000000
extra.append({'diagnostic':'Near-zero WAVE retention, same growth; optimistic investment-efficiency diagnostic','value':m.valuation(jv_zero_retention)['value']})
(P/'additional-sensitivity.json').write_text(json.dumps(extra,indent=2))
report=f'''# AWI · Armstrong World Industries
## Fundamental Pullback · Review as of November 7, 2026

**Decision: observe; not approved at $171.23.** The business is profitable, cash generative and adequately financed. The current price, however, is above the central FCFF value and even slightly above the favorable case. Neither Opportunity 80 nor a 16.9% pullback demonstrates a margin of safety. No order, trade or Stage 3.5 approval follows from this report.

**Values today:** adverse **$67.84**, base **$109.50**, favorable **$164.90**. The narrower central range is approximately **$99–122**, from WACC 9.7–10.7% and terminal growth 2–3%, not the full adverse-to-favorable envelope. Base confidence is **medium**: primary financial evidence is strong; physical reinvestment, mix and WAVE growth remain underwriting assumptions. A 15% initial uncertainty allowance gives a **conditional review ceiling of $93**, rounded from $93.07. This is a valuation review level, not a technical entry, stop or buy order. Base-value margin of safety at spot is **−56.4%**; price-to-base downside is **−36.1%**. These use different denominators.

The case fails on price support, not a fabricated data blocker. Reconsider only after a material price change or substantiated improvement in organically funded growth, margins or capital efficiency. This does not direct sale of any existing position: Stage 4 needs its separate decision and current holding context.

## What is good, what is not

- **Pricing and product breadth are real strengths.** Q3 Mineral Fiber sales grew 6.6%; approximately $16m of the $18m increase was average unit value, with only $2m volume. Architectural Specialties grew 21.5%, with $25m organic growth and $8m acquired growth. That supports a premium business, but not a uniform high-volume growth assumption. [Q3 results]({sources[5][0]})
- **WAVE is an important cash asset, not a free accounting add-on.** TTM affiliate income is $118.2m, approximately 26% of reported EBIT. WAVE cash distributions are $120.1m. Their investing classification makes ordinary CFO-minus-capex screen data incomplete. The model removes affiliate earnings from core EBIT, values taxed WAVE equity cash separately and adds no JV book value. [Q3 filing]({sources[4][0]})
- **Sustainable earnings are growing, but cash is not accelerating in parallel.** TTM sales grew 9.1%, core EBIT 7.6%, GAAP net income 5.1%; tax-normalized earnings excluding nonoperating income and asset-sale effects grew approximately 9.1%. Weighted-average share reduction lifts normalized EPS growth to about 11.5%. TTM comparable FCF including WAVE declined 3.2%, and the SBC/tax-normalized cash proxy declined about 3.7%. [FY2025 annual report]({sources[0][0]}) and [2025 comparative filing]({sources[1][0]}).
- **Acquisitions do not yet provide clean incremental profit.** Eventscape, Parallel and Geometrik contributed $25.1m of nine-month sales but an operating loss of $4.6m, including $3m D&A. Current acquired businesses remain in the sales base; no future acquisition growth or free buybacks are assumed. [Q3 filing]({sources[4][0]})
- **Financing is not the reason to reject the price.** Gross loan principal $472.9m plus finance leases $35.2m is modest beside the current earnings base; $430m of undrawn revolver availability provides liquidity. The facility matures December 2030. Higher rates, construction cyclicality and buybacks still consume optionality. [Q3 filing]({sources[4][0]})

## Primary financial history

USD millions; December fiscal year; no ADR. Quarter and TTM figures derived by subtraction retain the source rounding. Core EBIT = reported EBIT less net affiliate earnings, with SBC and amortization retained.

{tbl(['FY2023','FY2024','FY2025'])}
{tbl(['Q42025','Q12026','Q22026','Q32026'])}
{tbl(['TTM2025','TTM2026'])}

The most recent four quarters are Q4 2025 through Q3 2026. Q4 = FY2025 minus nine-month 2025; Q2 and Q3 cash flows are cumulative differences. TTM2026 = FY2025 + nine-month 2026 − nine-month 2025; prior TTM = FY2024 + nine-month 2025 − nine-month 2024. No seasonal quarter is annualized. Three-year source: [annual report]({sources[0][0]}). Quarter sources: [Q1]({sources[2][0]}), [Q2]({sources[3][0]}), [Q3]({sources[4][0]}), and [prior comparatives]({sources[1][0]}).

Reported core margins were 18.1%, 18.7% and 19.7% in FY2023–25, then 19.1% TTM. Reported EBIT margins include WAVE earnings but not its underlying sales, so the 25.8% TTM consolidated margin is not a stand-alone manufacturing margin. Nine-month working-capital cash use from receivables, inventory and payables was $55.8m, versus $32.3m a year ago. Receivable cash use rose from $31.5m to $66.0m; actual income-tax payments rose from $53.4m to $74.7m. A forecast cannot assume both persistent growth and permanent working-capital release.

Supplemental longer context: company-reported operating income was about $260m in 2021 and $279m in 2022, while operating cash flow was about $187m/$182m and adjusted FCF about $190m/$221m. This five-year view supports durability but is not a full trough-to-peak recession study. The adverse case explicitly contemplates stagnation and margin compression rather than treating the recent expansion as permanent.

## Normalization and exact cash definitions

1. **Earnings:** leave SBC, recurring cost pressure and acquisition amortization in EBIT. For a consistent sustainable comparison, remove fixed-asset sale gains/losses, exclude other nonoperating income, and apply 25% tax to EBIT less interest. This gives FY2023–25 normalized earnings $216.3m/$251.3m/$297.8m; current TTM $315.7m against approximately $289.4m prior TTM. The difference from GAAP is tax and nonoperating effects, not a claim that every adjusted-EPS add-back is economically free.
2. **Cash proxy:** CFO + cash distributions from WAVE − cash PP&E purchases. This is $338.0m TTM; standard CFO minus capex alone is $217.9m. The $120.1m difference is the JV cash classification. No double addition of affiliate earnings is made.
3. **Economic cash diagnostic:** subtract SBC $20.0m; add after-tax interest $22.7m; remove after-tax nonoperating income $2.7m. Then remove $10m of Q4-2025 nonrecurring tax-reform cash benefit still inside the current TTM. Result approximately **$328.0m**, versus **$340.6m** prior TTM. The result is a cash-conversion diagnostic, not the forecast FCFF input: actual cash-tax timing, JV distributions and financing-related investment timing differ from normalized operating cash flow.
4. **Company adjusted FCF bridge:** FY2025 raw CFO + WAVE − capex was $359.1m. Adding $5.7m company-owned life-insurance proceeds and approximately $1m acquisition compensation adjustment, then removing $20m nonrecurring tax benefit, produces about $345.8m, consistent with the rounded $346m company figure. Its published reconciliation begins instead with CFO plus investing cash and adds back acquisitions while removing asset-sale proceeds. The release specifies $10m of the tax benefit in Q4, so the current/prior TTM allocations above are not guessed. [FY release]({sources[6][0]}).
5. **Capex and software:** cash capex was $83.8m/$82.8m/$109.4m in FY2023–25 and $114.2m TTM. Company capex includes capitalized computer software within PP&E; gross PP&E software increased from $86.7m to $98.4m in 2025. Acquired software also exists in intangibles. No extra software expense is added on top of capex without a separate disclosure. The forward maintenance budget explicitly covers systems renewal, software and leased-asset renewal.
6. **Noncash capital and leases:** FY2025 finance-lease ROU additions were $7.7m; vendor-financed PP&E purchases $3.1m. Cash capex alone thus understates all-in asset investment. These items are disclosed separately rather than falsely calling the historical cash proxy economic FCFF. Financing-lease principal repayments are not subtracted again in the forward FCFF because finance-lease debt is deducted in the equity bridge and renewal investment is budgeted. Operating rent stays in EBIT; operating lease liabilities $49.5m are not also deducted.
7. **Pensions:** remove non-service pension returns through excluding other nonoperating income. Core service costs remain expenses. Deduct $59.8m in pension/postretirement claims, including the $6.3m current component. Give the $104.7m prepaid pension asset zero surplus-cash value because it is not unrestricted cash. Recurring workforce service cost is distinct from already-accrued deficit claims; do not deduct deficit settlement again in forecast operating costs.
8. **Acquisitions and dilution:** TTM acquisition cash $72.1m is historical allocation, not recurring organic capex. The existing asset base, sales and debt already reflect it; deducting it again from value would double charge sunk consideration. Future acquired sales are zero. The forecast retains SBC in margins, makes no free repurchases, and divides by 41.900177m September shares plus 0.3m outstanding-award dilution. This existing-award allowance is not a second deduction of future SBC. Higher actual dilution is a review trigger.

## Current outlook and cause of the pullback

October 27 guidance was sales **$1,788–1,803m**, adjusted EBITDA **$602–612m**, adjusted EPS **$8.30–8.40**, and adjusted FCF **$380–390m**. These are management guidance, not reported actuals or analyst consensus. The model uses the sales midpoint as the scale anchor; it does not call adjusted FCF unlevered FCFF. It uses $123m JV earnings and approximately 20% core EBIT margin as explicit analytical estimates, consistent in broad scale with EBITDA less D&A and WAVE, not a company-issued segment forecast.

Management explicitly cited accelerating input costs, Mineral Fiber mix headwinds and softer recent acquisition contributions. Q3 operating improvement included $13m volume benefit, $9m AUV benefit and $4m WAVE improvement, offset by approximately $10m manufacturing cost increase. These are evidenced operating risks that can explain investor caution; the report **does not assert that they explain every day of the 16.9% peak-to-price fall**. No verified single-cause attribution is required to recognize valuation risk. [Q3 release]({sources[5][0]}).

## Valuation design: ten years, organically funded growth

The primary method is **core operating FCFF plus the WAVE equity interest**. This is not a replacement of FCFF with a P/E model. Core FCFF = EBIT after tax + D&A − maintenance and growth investment − incremental working capital. WAVE cash is equity-level, after the venture's own financing costs and after a 25% parent-tax allowance; it is discounted at cost of equity. Do not subtract WAVE debt again. Do not add the $29.5m affiliate balance-sheet carrying value. Overcast is assigned no separate value.

The first forecast year is a rolling-year operating-capacity proxy labeled 2027, scaled from 2026 guidance. End-of-year discounting is used consistently for all ten years; this is not a precise stub-period dividend entitlement calculation. There is no invented pending 2026 result. The latest September balance sheet is used explicitly, not portrayed as a November balance sheet.

Case | First five sales growth rates | Core margin year 5 / terminal | WACC / JV cost of equity | Terminal growth | Core terminal ROIC | Value | Terminal share
---|---|---|---|---|---|---|---
Adverse | 0%, 2%, 2.5%, 3%, 3% | 18.5% / 18% | 11.2% / 11.6% | 2% | 15% | $67.84 | 40.2%
Base | 6.5%, 6%, 5.5%, 5%, 4.5% | 22% / 22% | 10.2% / 10.54% | 2.5% | 20% | $109.50 | 49.6%
Favorable | 9%, 8.5%, 8%, 7.5%, 6.5% | 24% / 23.5% | 9.2% / 9.6% | 3% | 25% | $164.90 | 57.8%

**Growth evidence:** nine-month sales growth is 10.2%, of which $25.1m is recent acquisitions against $125.2m total increase, leaving roughly 8.1% approximate organic growth on reported prior-year sales. Base growth begins below that recent pace and fades. Mineral Fiber's limited volume growth and AS project/tariff sensitivity argue against extrapolating AS's 21.5% headline growth across the whole company. The favorable case assumes better execution and product mix; it is not the default.

**Margins require investment:** 22% core margin by year five compares with 19.1% TTM and 19.7% FY2025. It requires pricing/mix and AS operating leverage to overcome freight, metal costs and acquisition losses. SBC remains included. Base year-one sales are $1,912.2m, NOPAT $292.6m, D&A $127.5m, maintenance investment $105.2m, growth capex $46.7m and working-capital investment $14.0m, leaving core FCFF $254.3m. WAVE contributes $80.6m of modeled after-tax distributable cash after retention. Total investment rises ahead of sales; the base does not assume high growth at maintenance-only capex.

**Capital intensity:** maintenance capex is 5.8%/5.5%/5.2% of sales in adverse/base/favorable. Growth fixed capital = incremental sales divided by 2.0/2.5/3.0; working capital consumes 14%/12%/10% of incremental sales. These are explicit analyst assumptions anchored by roughly $629m net PP&E and the recent $109–114m annual cash capex, plus noncash asset investment. Base first-year all-in capex $151.9m is intentionally above recent cash capex because future growth is organic and funded, unlike acquired growth that arrives with purchased assets. It is not a disclosed company budget. The maintenance/expansion split is not separately reported, so it is tested rather than represented as a fact.

D&A fades from 6.8% of sales to 5.5% over ten years as acquisition amortization runs down. Terminal depreciation equals maintenance replacement investment. Terminal core reinvestment is the **greater of NOPAT × g / ROIC and the physical growth investment plus working-capital requirement**. Base terminal NOPAT reinvestment is $58.3m versus physical growth floor $35.9m; terminal FCFF is $408.4m. Consequently zero reinvestment or permanently unreplaced assets cannot inflate terminal value. JV retained earnings fund growth using incremental equity-return assumptions of 20%/25%/30%; all are underwriting judgments, not historical ROE forecasts. WAVE's actual 2025 distributions of $113m against AWI equity income $113.2m show high cash conversion, but the model does not extrapolate virtually 100% payout alongside growth indefinitely.

## Cost of capital, enterprise-to-equity bridge and comparables

The base cost of equity is 4.84% risk-free + 1.14 beta × 5.0% equity-risk premium = 10.54%. The risk-free input is the latest observation in the November 6 Federal Reserve release, not a claim about the final Friday close. AWI's reported five-year beta is 1.14. A 6.5% analytical marginal borrowing cost, 25% tax and 6.5% debt weight imply approximately 10.17% WACC, rounded to 10.2%. The debt rate allows some spread/refinancing risk above the current SOFR +125bp facility; the ERP and target weights are assumptions. Scenario WACCs vary ±100bp, not unexplained risk haircuts. [Federal Reserve]({sources[13][0]}); [AWI market statistics]({sources[9][0]}).

Base bridge, USD millions:
- Core operating enterprise value: $4,037.1.
- WAVE equity cash value: $1,118.4.
- Excess cash: $36.4, from $71.4 cash less $35 operating reserve.
- Claims: $472.9 loan principal + $35.2 finance leases + $59.8 pension/postretirement + $3.1 contingent acquisition consideration = $571.0.
- Common equity: $4,620.9; diluted economic shares 42.200177m; value $109.50.

The loan principal exceeds carrying value $469.6m by $3.3m of deferred financing costs. Ordinary deferred taxes are not deducted as if all were due cash today while also taxing the forecast; 25% normalized cash tax and the explicit one-off benefit correction handle timing conservatively. No unrestricted benefit is assumed from pension assets or life-insurance cash value.

**Comparable cross-check, November 6 regular closes:** AWI $171.23 and 22.85× reported trailing P/E; CSL $375.74 and 21.36×; WTS $346.14 and 25.95×; OC $121.31 with negative trailing earnings, hence no meaningful trailing P/E. These are same-provider trailing ratios, not a mixture of adjusted-forward and GAAP-trailing earnings. Carlisle has building-envelope/repair exposure but different margins, leverage and buybacks; Watts has specification-driven products and a stronger net-cash balance; Owens Corning has more housing/roofing cyclicality and accounting distortions. None is a pure ceiling/WAVE twin. [CSL]({sources[10][0]}), [WTS]({sources[11][0]}), [OC]({sources[12][0]}).

AWI's provider EV/EBIT excludes affiliate earnings from EBIT while its EV still contains the market value of those affiliates; comparing that ratio mechanically with peers is misleading. The cash model reconciles this instead of choosing a high peer multiple. Spot is about 20.5× 2026 adjusted EPS guidance midpoint, explicitly a different basis from the trailing P/E table. Peer prices show what investors pay, not a floor under intrinsic value. No multiple average overrides the FCFF result.

## Sensitivity and reverse valuation

Base operating assumptions, with both discount rates shifted together; JV equity discount is WACC +0.34 percentage point:

WACC | g 2.0% | g 2.5% | g 3.0%
---|---:|---:|---:
9.2% | $123.45 | $128.06 | $133.36
9.7% | $114.35 | $118.14 | $122.45
10.2% | $106.36 | $109.50 | $113.04
10.7% | $99.28 | $101.91 | $104.84
11.2% | $92.97 | $95.18 | $97.63

A permanent +2 percentage point core-margin shift raises value to $118.80; +4 points to $128.09. Those sensitivities move all forecast and terminal margins, so they are more favorable than a late-year-only improvement. Maintenance-capex sensitivity, keeping terminal economics disciplined: '''
report+='; '.join(f'{x["maintenance_capex_sales"]:.1%} of sales → ${x["value"]:.2f}' for x in extra if 'maintenance_capex_sales' in x)+'.\n\n'
report+=f'''At $171.23, the **same** base model requires approximately **16.5% revenue growth annually for five years** before transition to 2.5%, with the base 22% terminal core margin. A +2-point margin path lowers that requirement to **14.3%**; a +4-point path lowers it to **12.3%**. Working capital and physical growth capex increase automatically in these backsolves; no free acquisition growth is inserted. These are combinations of expectations, not unique market forecasts and not independent confirmation of the direct DCF. They substantially exceed current whole-company organic growth, particularly Mineral Fiber volume. WAVE growth is held at its base path in the reverse analysis; claiming growth there could reduce required core growth but would need separate evidence and reinvestment.

## What would change the decision

- **Upgrade evidence:** repeated organic sales growth above the base path, a durable core margin above 22% without stripping SBC or necessary investment, improved acquisition profitability, receivable conversion, and demonstrated high growth at less incremental capital. A cheaper price can also change expected return without changing business quality.
- **Downside first breaks:** project/volume demand and working-capital collection, followed by price-cost spread and WAVE distributions. A cash downturn combined with continued repurchases can erode liquidity faster than EPS suggests.
- **Review triggers:** organic deceleration below 3% over more than one quarter; core EBIT margin below 18% without a credible recovery; worsening collection alongside revenue growth; WAVE distributions persistently below earnings; acquisition earn-outs or dilution above the allowance; material pension/contingent claims; new debt-funded acquisitions; a confirmed financing or accounting concern.
- **Calendar:** Q3 results/call were October 27. The retrieved primary events page supplies no confirmed future earnings date. Do not label a vendor estimate as a confirmed date or claim that an event is imminent. Check the next official release when announced; no future monitoring or trade is claimed here.

## Disclosure gaps and readiness

Maintenance versus growth capex, forward unit volume by specialty, WAVE's detailed incremental capital needs and future noncash asset additions are not disclosed at the precision of this model. These are addressed with explicit assumptions and sensitivities rather than invented facts or indefinite blocking. The actual margin and cash inputs, debt/share bridge, and guidance are sourced. The model is **senior-review-ready; medium valuation confidence**, not a guarantee of realizable value. Its executable analytical export is not represented as a banker formula workbook.

The current cycle view is limited to the available three-year audited financials, quarterly comparatives and five-year summary; a recession trough study would sharpen downside calibration. Reported acquired-business results and the software/lease classifications are preserved. No reliance on a refreshed point-in-time balance sheet after September, a private consensus feed, a full market-price history or an invented technical stop is made.

## English summary

AWI is a durable, profitable building-products franchise with valuable WAVE cash distributions and manageable debt. Current organic growth and normalized earnings are respectable, but cash conversion, cost inflation and acquired-business losses merit attention. A ten-year funded FCFF plus WAVE equity-cash model gives $68/$109/$165 against $171.23. The stock is not approved at that price; $99–122 is the central sensitivity range and approximately $93 is only a conditional valuation-review ceiling, not an entry order.

## Resumen en español

AWI es una empresa rentable de productos para construcción, con una aportación valiosa de caja de WAVE y deuda manejable. El crecimiento orgánico y el beneficio normalizado son sólidos, pero preocupan la conversión en caja, la inflación de costes y las pérdidas de las adquisiciones recientes. El modelo de FCFF a diez años, más la caja del capital propio de WAVE sin duplicarla, arroja $68/$109/$165 frente a $171,23. **Observación: no aprobada al precio actual.** El rango central es $99–122; unos $93 son solamente un techo condicionado para revisar la valoración, no una entrada técnica ni una orden.

## Evidence and calculations

The supporting derived-input, historical, forecast, scenario, sensitivity and QA files preserve source-versus-assumption labels and calculation identities. All primary periods are USD millions except per-share amounts. Source links below point to public documents; no private research inventory or full filing copies are published.

'''
for u,t,d,p in sources:report+=f'- [{t}]({u}) · {d}. {p}\n'
(P/'report.md').write_text(report)
# Portable HTML avoids dependencies. Preformatted body preserves all evidence and calculation tables without hidden content.
(P/'report.html').write_text('<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>AWI Fundamental Pullback Review</title><style>body{font:16px/1.65 system-ui;background:#f3f6f8;color:#152b3c;margin:0}main{max-width:1100px;padding:40px;margin:auto;background:white}h1{font-size:36px;color:#123f57}pre{white-space:pre-wrap;overflow-wrap:anywhere;font:inherit}a{color:#126b8d}</style><main><h1>AWI | Fundamental Pullback</h1><p>7 November 2026 · $171.23 reference close · Observe / Observación</p><pre>'+html.escape(report)+'</pre></main></html>')
(P/'summary.json').write_text(json.dumps({'ticker':'AWI','asOf':'2026-11-07','status':'completed_research_not_approved_at_price','price':171.23,'priceDate':'2026-11-06','opportunity':80,'qualityPoints':70,'values':{n:round(x['value'],2) for n,x in O.items()},'reasonableRange':[99,122],'conditionalReviewCeiling':93,'confidence':'medium','method':'Ten-year core FCFF plus separately discounted WAVE equity cash; no double capitalization','es':'Observación: no aprobada a $171,23. Negocio rentable y deuda manejable; el precio exige crecimiento superior al respaldado. Valor central $109; rango central $99–122; techo condicionado de revisión $93, sin orden ni entrada técnica.','en':'Observe: not approved at $171.23. Profitable business and manageable debt, but price requires growth above the evidenced path. Base value $109; central range $99–122; conditional review ceiling $93, with no order or technical entry.'},indent=2))
print('Report and public-source ledger created.')

# Coordinated audit clarifications: these disclosures do not alter valuation assumptions or case outputs.
clarification='''## Conditional status and independent-review clarifications

**Stage 3 is not complete; no entry is approved; there is no approved valuation.** Values in this package are conditional analytical scenarios, not an authorized fair value or executable price ceiling. The $93 figure remains a conditional review calculation only. Opportunity 80 and quality points 70 are supplied scanner inputs, not independently certified fundamental scores.

A homogeneous historical-multiple study has not been completed. The same-date peer P/E cross-check is not a substitute for comparing AWI's own through-cycle multiples on a consistent earnings and affiliate basis. This missing Stage 3 check, plus the WAVE capital-coverage qualification below, prevents describing this package as completed Stage 3 research. The report is ready for conditional analytical review, with medium model confidence, not for portfolio execution.

**WAVE cash classification matters.** FY2025 Annual Report Note 2 says AWI applies the cumulative-earnings approach. Prior cumulative distributions, excluding amounts already classified as returns of investment, exceeded cumulative equity earnings adjusted for basis amortization. The distributions were therefore classified as returns of investment in investing cash flows for the years presented. This is more than a data-provider omission: not every distributed dollar is established as recurring earned cash. It does not, by itself, prove the current payout is unsustainable. Historical distribution conversion supports cash generation but does not certify future maintenance, growth, debt-service or legal distribution capacity.

FY2025 Note 10 discloses combined unconsolidated-affiliate assets of $199.5m and liabilities of $394.1m, including $360.3m noncurrent liabilities. Those are **combined affiliate** balances, not a verified WAVE-only debt schedule. They reveal capital-structure exposure requiring judgment; do not attribute every liability to WAVE, treat those balances as unrestricted cash, or deduct them again from the modeled equity cash value. The exact future financing and distribution constraints remain unverified.

The JV model assumes maintenance replacement approximately equals the depreciation already charged against JV earnings. It also assumes 25% parent-level taxation and incremental **after-parent-tax** equity returns of 20%/25%/30% in adverse/base/favorable. Growth retention derived from these returns is not independent proof of distributability. A separate audit-only 25% reduction of the base JV value lowers the total value from $109.50 to about $102.87; it is not a revised base scenario. No arithmetic defect was found in the separate core/JV structure, but these assumptions materially qualify economic confidence.

**Terminal maintenance reconciliation:** year-ten maintenance is 5.8%/5.5%/5.2% of sales, while D&A has converged to 5.5%. At the terminal boundary, maintenance and D&A both reset to 5.5% in all three cases. Relative to carrying forward each year-ten maintenance ratio, adverse annual terminal FCFF is approximately 0.3% of terminal sales higher; favorable FCFF is approximately 0.3% lower; base has no reset. These are explicit steady-state normalization conventions, not evidence of a sudden operational efficiency change. The additional NOPAT/ROIC reinvestment requirement remains at least the physical growth and working-capital floor. Readers should not interpret the nonbase boundary as a seamless historical forecast.

**Provenance:** financial statements and declared guidance are primary issuer facts; the November 6 price, beta and peer ratios are dated public market-provider observations. Margins, growth, discount rates, reinvestment returns, operating cash reserve, award-dilution allowance, tax normalization, central range and conditional review level are analyst estimates or calculations. No consensus feed or current balance sheet later than September 30 is claimed. Historical raw source documents are not redistributed.

## Estado condicionado y aclaraciones de revisión

**Stage 3 no está completo; no hay entrada aprobada ni valoración aprobada.** Los escenarios son cálculos analíticos condicionados. Falta el estudio homogéneo de múltiplos históricos; el contraste actual con pares no lo sustituye. Opportunity 80 y QP 70 proceden del scanner, no son puntuaciones fundamentales certificadas por esta revisión.

Las distribuciones de WAVE se clasifican como devolución de inversión mediante el método de beneficios acumulados. Su conversión histórica en caja no demuestra por sí sola que toda distribución sea recurrente ni que estén cubiertas las necesidades futuras de mantenimiento, crecimiento, financiación y distribución. Los $199,5m de activos y $394,1m de pasivos de 2025 corresponden al conjunto de afiliadas no consolidadas, no a una deuda exclusiva de WAVE que deba restarse de nuevo.

El modelo supone mantenimiento de WAVE aproximadamente igual a su depreciación, impuestos al nivel de AWI del 25% y rentabilidad incremental del capital después de esos impuestos del 20%/25%/30%. Son hipótesis, no restricciones financieras verificadas. El ajuste de auditoría de −25% al valor de WAVE llevaría el valor central total a unos $102,87, sin sustituir el escenario central.

En el año diez, mantenimiento/ventas es 5,8%/5,5%/5,2%; en el terminal se normaliza a 5,5%, igual que la depreciación. Esto aumenta la caja terminal adversa y reduce la favorable en aproximadamente 0,3% de las ventas terminales frente a prolongar sus porcentajes del año diez. No hay cambio en el caso central. La convención queda explícita y no es una mejora operativa demostrada.

'''
report=report.replace('The model is **senior-review-ready; medium valuation confidence**','The model is **conditional-review-ready; medium valuation confidence**')
report=report.replace('## What is good, what is not',clarification+'## What is good, what is not')
report=report.replace('**Decision: observe; not approved at $171.23.**','**Decision: observe; Stage 3 incomplete and no entry approved at $171.23.**')
(P/'report.md').write_text(report)
(P/'report.html').write_text('<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>AWI Conditional Fundamental Review</title><style>body{font:16px/1.65 system-ui;background:#f3f6f8;color:#152b3c;margin:0}main{max-width:1100px;padding:40px;margin:auto;background:white}h1{font-size:36px;color:#123f57}pre{white-space:pre-wrap;overflow-wrap:anywhere;font:inherit}</style><main><h1>AWI | Conditional fundamental review</h1><p>7 November 2026 · Stage 3 incomplete · No entry approved</p><pre>'+html.escape(report)+'</pre></main></html>')
s=json.loads((P/'summary.json').read_text());s.update(status='conditional_research_stage3_incomplete',stage3Complete=False,entryApproved=False,approvedValuation=None,valuationScope='Conditional analytical scenarios only; historical-multiple study incomplete and WAVE capital/distribution coverage qualified',scoreProvenance='Opportunity 80 and QP 70 are supplied scanner inputs, not audit-certified fundamental scores',readiness='Ready for conditional analytical review; not approved for portfolio action',gaps=['Homogeneous historical-multiple study incomplete','Future JV maintenance, funding and distribution constraints unverified; explicit analytical assumptions used'])
s['en']+=' Stage 3 remains incomplete; no approved valuation. Historical-multiple work and WAVE capital/distribution qualification remain open.'
s['es']+=' Stage 3 sigue incompleto; no hay valoración aprobada. Quedan pendientes los múltiplos históricos homogéneos y la verificación de las restricciones de capital y distribución de WAVE.'
(P/'summary.json').write_text(json.dumps(s,indent=2,ensure_ascii=False))
cards=[
{'type':'pro','en':'Q3 Architectural Specialties sales rose 21.5%, including $25m organic growth and $8m acquired growth.','es':'Las ventas de Architectural Specialties aumentaron un 21,5% en el tercer trimestre, con $25m de crecimiento orgánico y $8m por adquisiciones.','provenance':'Reported issuer results; amounts rounded in company commentary.','url':sources[5][0]},
{'type':'pro','en':'AWI had $430m of undrawn revolver availability at September 30, 2026; current loan principal was $472.9m.','es':'AWI disponía de $430m no utilizados en su línea de crédito al 30 de septiembre de 2026; el principal de los préstamos era de $472,9m.','provenance':'Reported Q3 2026 debt and liquidity disclosures; no inference of unrestricted borrowing under all future conditions.','url':sources[4][0]},
{'type':'pro','en':'Reported WAVE distributions were $113.0m in 2025, supporting historical cash conversion but not certifying future capital coverage.','es':'Las distribuciones de WAVE fueron de $113,0m en 2025: respaldan la conversión histórica en caja, pero no certifican la cobertura futura de capital.','provenance':'Reported annual distribution amount plus explicit analyst limitation.','url':sources[0][0]},
{'type':'con','en':'Nine-month operating cash flow fell from $245.5m to $222.1m as receivable cash use and cash tax payments increased.','es':'La caja operativa de nueve meses bajó de $245,5m a $222,1m al aumentar el consumo de caja por cobros pendientes y los pagos fiscales.','provenance':'Reported comparative cash-flow statements; cash timing is not assumed permanently impaired.','url':sources[4][0]},
{'type':'con','en':'Recent acquisitions contributed $25.1m of nine-month sales but an operating loss of $4.6m, including $3.0m D&A.','es':'Las adquisiciones recientes aportaron $25,1m de ventas en nueve meses, pero una pérdida operativa de $4,6m, incluidos $3,0m de depreciación y amortización.','provenance':'Reported acquired-business disclosure, Q3 2026 Note 4.','url':sources[4][0]},
{'type':'con','en':'WAVE distributions are classified as returns of investment under the cumulative-earnings approach; high payouts do not prove sustainable distributable cash.','es':'Las distribuciones de WAVE se clasifican como devolución de inversión mediante el método de beneficios acumulados; un pago elevado no prueba caja distribuible sostenible.','provenance':'Reported FY2025 Note 2 classification plus analyst interpretation.','url':sources[0][0]},
{'type':'valuation','en':'The analyst model gives $67.84/$109.50/$164.90 against $171.23. These are conditional scenarios, not an approved valuation or entry.','es':'El modelo del analista arroja $67,84/$109,50/$164,90 frente a $171,23. Son escenarios condicionados, no una valoración ni una entrada aprobadas.','provenance':'Analyst-derived ten-year core FCFF plus WAVE equity-cash model; market close verified separately.','url':sources[9][0]}]
(P/'evidence-cards.json').write_text(json.dumps(cards,indent=2,ensure_ascii=False))
q=json.loads((P/'qa.json').read_text());q.update(stage3Complete=False,entryApproved=False,approvedValuation=None,status='Ready with caveats for conditional review only',economicQualifications=s['gaps']+['Terminal maintenance explicitly resets to 5.5% of sales in all cases; nonbase discontinuity disclosed.','JV after-parent-tax incremental ROE and maintenance coverage are assumptions.'])
(P/'qa.json').write_text(json.dumps(q,indent=2))
(P/'README.md').write_text('''# AWI conditional research package

As of November 7, 2026. USD millions except per-share amounts. No trades or execution approval.

Start with report.md or report.html, then summary.json and evidence-cards.json. Stage 3 is incomplete: a homogeneous historical-multiple study is not complete and future WAVE capital/distribution constraints remain qualified. Values are analyst scenarios, not an approved valuation. The report explains the historical cash classification and the explicit terminal maintenance reset.

Reproduction: run `python build_report.py` in this directory using standard-library Python. It imports model.py, rebuilds the numerical inputs, historical and forecast schedules, cases, inverse valuation, sensitivities, arithmetic QA, bilingual report and conditional flags. Alternatively `python model.py` rebuilds numerical calculations only; it does not replace the full report's economic-readiness qualifications. No network access or third-party package is needed.

Provenance: source-ledger.json contains only public URLs, titles, dates and purposes. Primary historical figures and company guidance are distinguished from analyst forecast assumptions. Scanner scores are supplied screening inputs, not fundamental approval. evidence-cards.json contains exact bilingual card text, provenance and public supporting URLs. No complete source filing, private source inventory or private-source hash is included.

The public manifest names only the explicitly permitted generated research files. Its hashes identify generated public deliverables, never private source documents. Case values remain unchanged after independent review. No remote publication is performed by these scripts.
''')
print('Conditional status, bilingual evidence and provenance corrections applied; case calculations unchanged.')

# Render the exact bilingual evidence text with provenance and underlying public URL.
# The card text is substantive sourced evidence, not a claim of approval.
report+='\n## Bilingual evidence cards / Fichas de evidencia bilingües\n\n'
for number,card in enumerate(cards,1):
 report+=f'### {number}. {card["type"]}\n\n{card["en"]}\n\n{card["es"]}\n\nProvenance: {card["provenance"]}\n\nPublic source: {card["url"]}\n\n'
for card in cards:
 assert card['en'] in report and card['es'] in report
 assert card['url'] in report
(P/'report.md').write_text(report)
(P/'report.html').write_text('<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>AWI Conditional Fundamental Review</title><style>body{font:16px/1.65 system-ui;background:#f3f6f8;color:#152b3c;margin:0}main{max-width:1100px;padding:40px;margin:auto;background:white}h1{font-size:36px;color:#123f57}pre{white-space:pre-wrap;overflow-wrap:anywhere;font:inherit}</style><main><h1>AWI | Conditional fundamental review</h1><p>7 November 2026 · Stage 3 incomplete · No entry approved</p><pre>'+html.escape(report)+'</pre></main></html>')
for card in cards:
 assert card['en'] in html.unescape((P/'report.html').read_text())
 assert card['es'] in html.unescape((P/'report.html').read_text())
q=json.loads((P/'qa.json').read_text());q['publicationChecks']={'exactBilingualEvidenceStrings':14,'allExactStringsPresentInReportMarkdown':True,'allExactStringsPresentInDecodedReportHtml':True,'allSupportingPublicUrlsPresent':True};(P/'qa.json').write_text(json.dumps(q,indent=2))
print('All 14 bilingual evidence captions and supporting URLs are present verbatim in the generated report.')
