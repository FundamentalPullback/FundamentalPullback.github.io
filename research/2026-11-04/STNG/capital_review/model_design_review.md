# Independent STNG fleet DCF design review
November 4 information cutoff; review completed Nov5 UTC. Model-design advice, not valuation output.

## Recommendation
Use a finite-life fleet DCF as the cleanest primary fundamental valuation. Forecast each vessel or class/year-built cohort to assumed retirement, not merely ten years. Each fleet asset earns normalized operating cash through its remaining economic life; then earns scrap/sale proceeds once. Existing ships have approximately 10–15 years remaining at a 25-year assumed life; 2027–2030 newbuilds run until approximately 2052–2055. No Gordon terminal or annual replacement reserve is necessary in a run-off model. This values contracted fleet assets, not uncontracted future fleet expansion. It is conservative in excluding future positive-NPV reinvestment opportunities but is not automatically a downside value.

If presentation requires ten-year forecasts, show ten years explicitly and compute a finite-life residual asset DCF at year10 for remaining ships. That residual is the present value at year10 of EACH remaining hull's future cashflows and scrap through retirement. It must not contain an unearned perpetuity. No annual economic reserve is deducted in explicit years; actual scheduled newbuild capex and drydock cashflows are deducted once. Paid deposits at valuation date are sunk, not another future cash charge. Future fleet income is included only from delivery dates. Distinguish the small 2026 valuation-date-to-year-end stub from 2027 full-year forecast; $45.6M Q4 remaining installment payment cannot disappear if model begins in 2027 with October cash.

A going-concern replacement model is a separate sensitivity, not mixed into runoff. At each modeled retirement date: scrap old hull, buy replacement at inflation-adjusted replacement price, incur delivery/offhire timing, and update cohort. Explicitly cover the 2038–2042 renewal wave BEFORE resorting to a normalized terminal. That prevents a ten-year forecast from conveniently ending immediately before capital expenditure accelerates. For a fixed-size 89-vessel fleet, replacement does not produce fleet-count growth. If newbuilds are explicitly designated to replace sold/retired ships, remove their predecessors once. Otherwise the documented plan moves72 post-sale hulls to89; speculative future sales must not be assumed implicitly to justify a reduced capital charge.

## Why the proposed annual reserve is problematic
Deducting (replacement price minus scrap)/25 each year is an undiscounted accounting-like economic charge, not actual FCFF. It shifts distant replacement payments forward, giving a different present value and understating early cash generation. Adding it alongside actual replacements for the SAME cohorts duplicates the renewal cost. Adding it alongside genuinely incremental growth capex can be conceptually coherent as a steady-state earnings proxy, but should not be called a timed fleet FCFF DCF and cannot use a no-replacement terminal simultaneously. It is particularly misleading for young newbuilds that are charged a reserve for years yet are then given only scrap in terminal value.

If a smooth maintainable-earnings crosscheck is desired, isolate it: normalized TCE less opex/G&A, drydock, and explicitly labeled replacement annuity. Do not mix this measure into actual free-cash-flow history or value it with an arbitrary growth multiple. Cohort-specific discounted replacement costs are superior to flat annual reserve for an unevenly aged shipping fleet.

## Rates, inflation, ROIC and terminal consistency
- Explicit period: honor each actual contracted charter through expiration, include only spot exposure at normalized class-level rates, and normalize exceptional Q4 quotes over a defensible transition. Apply delivery-day weighting, drydock/offhire and utilization separately; don't apply utilization twice to already net earnings-day rates.
- All nominal model: inflate long-term TCE, opex, G&A, drydock, replacement cost, scrap, and working-capital requirements consistently with separate labeled inflation assumptions. A common 2% inflation assumption is illustrative, not sourced guidance. Fixed nominal charter rates stay fixed during term.
- All real model: hold normalized real price/cost assumptions constant and use real WACC = (1+nominal WACC)/(1+inflation)-1. Do not mix nominal WACC with a real zero-growth terminal absent conversion.
- Runoff has no perpetual g and no terminal ROIC requirement because retirement dates and residual scrap explicitly close the model.
- Going concern can have zero real volume growth and nominal g approximately inflation only after fixed fleet is economically maintained. Maintenance replacement cost must still inflate with g. A normalized perpetuity only after the renewal wave should use unlevered cash after replacement and working-capital reinvestment, not EBITDA or depreciation as automatic capex proxy.
- If using NOPAT*(1-g/ROIC)/(WACC-g), ROIC must be sustainable incremental nominal ROIC with compatible capital base and reinvestment. Historical tanker returns in a spike do not establish that ROIC. Don't apply g/ROIC reinvestment on top of a fully explicit capex/NWC growth schedule for the same activity. Retain only one coherent terminal method.
- Do not tax all maritime operating profit at a generic domestic corporate rate without the filing's tax structure. Do not subtract interest in FCFF and then subtract debt again as if using FCFE.

## Capex schedule and tentative program crosscheck
Reported remaining capex includes minority VLCC JV investments: $1,295.9M. Actual per-year split by owned hulls versus JV is NOT disclosed in Q3. Keep combined outflow as a conservative burden but label output partial if excluding JV income/asset value. It is not a completed owned-fleet DCF until JV is segregated or consistently added back/valued.

Documented full program cost including the already-delivered STI Moxie:
- Eight LR2: 2*$70.8M (2027), 2*$68.5M (2029), 4*$72.8M (2029) = $569.8M.
- Four VLCC: 2*$128M and 2*$135M (2028) = $526M.
- Six MR: 4*$45M (including Moxie2026 and three2027) +2*$46.33M (2030) = $272.66M.
- Total18 hulls = $1,368.46M.
- Paid185.7+remaining1295.9=$1,481.6M. Residual ~$113.14M is a useful CHECK, plausibly JV funding and other cost differences; it is not an exact disclosed JV commitment. Paid installment wording includes Moxie, so use full18-hull cost in this crosscheck rather than only17 remaining. Do not conflate $182.188M cash-flow vessel acquisition/construction cash with disclosed installment payments185.7M: scopes/timing/capitalization differ.
- Two2030 MR contracts require10% initial deposit; other payments begin2028 or later. This constrains schedule but does not provide a full class-specific split.
Sources: 2025 annual report 'Vessels under construction' and subsequent events; Q2 release recent events; Q3 release recent events/remaining-installment table. All source extracts saved in capital_review and original sources_private.

## Minimum audit checks before any total value
1. Fleet count every year = prior year + owned deliveries - sales - retirements. JV hulls never join wholly owned fleet count.
2. Each hull receives exactly one initial acquisition/deposit schedule, no duplicate renewal charge, one retirement/sale realization, and no operating income after exit.
3. Future capex sums to disclosed1,295.9M including JV once; timing includes remaining Q4 stub.
4. Pending-sales143M is added as net expected proceeds only once after removing their hull cashflows; costs/timing disclosed.
5. Investments either valued separately with corresponding income/cashflows removed from operating valuation, or valued inside operating cashflows, never both.
6. Principal and convertible dilution scenarios reconcile as in capital_bridge_review.md.
7. Nominal/real basis and discount-date convention are explicit. Midyear convention appropriate for operating flow, payment dates for newbuild capex, charter start dates for deliveries.
8. October cash is explicitly dated, not labeled current as-of Nov4 without a source; unavailable RSUs/other assets remain flagged rather than silently zeroed.
