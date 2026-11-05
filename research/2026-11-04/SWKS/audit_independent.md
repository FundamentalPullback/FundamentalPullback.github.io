# Independent audit: SWKS research, November 4 cutoff

Reviewed November 5, 2026 at approximately 00:11 UTC. Verdict: **PASS for partial-conditioned research only**, not a complete Stage 3 analysis, actual stock valuation, or entry authorization.

## Results

107 independent arithmetic, source-record, timing, and gate checks passed. Audit code reads the input and result files and recomputes the DCF separately; it does not execute the author's model or alter the main report. Machine-readable checks and reviewed-file hashes are in `audit_independent_checks.json`.

- History: annual FY23–25 and FY26 Q1–Q3 values match SEC companyfacts for exact periods through the cutoff. Cash-flow quarters derived from YTD are consistent. FY25 spans 371 days/53 weeks; FY26 spans 364 days/52 weeks. Disclosed year-on-year changes are not calendar-normalized. Q4/FY26 values were cross-checked against the primary earnings release. Quarter sum differences of0.1m are preserved and disclosed, not silently forced to tie.
- FCF: CFO less PPE and purchased intangibles is arithmetic-consistent. It is an analyst measure, not company-defined FCF or normalized FCFF. SBC subtraction is a separate diagnostic only. Three negative FY26 quarters and annual198.8m reconcile to the stated definition.
- Profit normalization: revised selected EBIT490.3m correctly adds140.7m acquired amortization and132.9m acquisition expense to216.7m GAAP EBIT, retaining SBC. FY25 comparator658.7m gives a25.6% decline. The556.5m impairment sensitivity is now expressly unverified, not a certified normalized profit. No precise category mapping of the66.2m impairment is asserted.
- Capital: October2 standalone balances, October5 closing, October7 exchange, and July illustrative pro forma are clearly separated. August financing is not counted twice. Exchanged Qorvo notes are canceled rather than added to the original debt. Reconstructed face principal4,048.421m is correctly distinguished from carrying value. Hypothetical3,500m claims are not represented as sourced actual closing net debt.
- Dilution: approximately241m diluted shares are Q1 guidance, not an actual point-in-time cap table. Common-stock exchange and awards conversion are not conflated. No per-share valuation uses the151m standalone denominator.
- FCFF: ten explicit years, end-year discounting, taxes, productive D&A, necessary capex, incremental working capital and extraordinary integration cash reconcile. SBC is retained in margins, and no duplicate SBC deduction occurs. Acquired amortization is excluded from margins and not added back again. Integration cash is separately deducted, with no tax benefit assumed. Assumed operating leases stay in costs without another lease-debt deduction.
- Terminal: year10 net reinvestment equals NOPAT×g/ROIC. Terminal FCFF equals year11 NOPAT×(1−g/ROIC), and grows continuously from year10 FCFF. WACC exceeds g in all cases. Terminal weights and all displayed operating EVs/residuals independently match.
- Reverse DCF: each solved growth/mature-margin pair reproduces target operating EV23,418.65m to within1e-6m. The growth path holds year1 fixed and changes years2–5, then transitions to terminal growth, as disclosed. It is not a unique inference of market expectations.
- Sensitivities: all nine WACC/g cases independently match. Hypothetical capital and share sensitivity are not promoted to actual fair value.
- Sources: prepared remarks support rounded combined sales categories, Q1 operating guide, synergies,62% customer concentration, and February earnings-call window. Price-history snapshot supports82.96 regular close and−2.86%; statistics snapshot supports historical beta1.48. Primary Treasury search confirms November4 ten-year4.90%, while the WACC weights, premium, marginal debt cost and final selection remain assumptions.
- Gates: actual fairValue, fairValueTotal, bear/base/bull, conditionalDcfCases, maximumConditioned, and technicalGate are null. Entry, Stage3 completion, Stage3.5 completion and latest-completed eligibility are false. Nested operating scenario labels do not represent actual fair-value fields.

## Issues raised and disposition

1. Medium, resolved: original table heading described analyst-calculated FCF as published. Revised heading correctly says calculated FCF after intangibles.
2. Medium, resolved: original normalization asserted an unsupported exact mapping between CFO impairment66.2m and the67.8m reconciliation category. Revised report uses490.3m selected EBIT and isolates556.5m as unverified sensitivity.
3. Low, documented and nonblocking: `model.py` hardcodes its source inputs and writes `inputs.json`; changing JSON alone does not change a rerun. Current results are reproducible and correct. The documented convention designates Python as the canonical editable model and JSON as its regenerated snapshot. This is not a current arithmetic or publication blocker.

## Limits of this approval

There is no closing consolidated balance sheet or September Qorvo full cash-flow reconciliation in the reviewed pack. Full historical normalization and homogeneous public comps are incomplete. Productive D&A, capex, working capital, sustainable tax, integration costs, margins and capital claims remain explicit scenario choices. Numerically coherent scenarios do not establish investment value. The low base scenario and high reverse requirements must not be treated as a short recommendation or quantified downside bound.

The present report honestly acknowledges these limits. Approval is limited to sharing partial research with its warnings intact and preserving all null/false investment gates. Any subsequent extraction of44.55 or99.44 as a fair-value target would invalidate this approval.
