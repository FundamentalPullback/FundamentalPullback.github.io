# DyFlex disclosure correction

Corrected 2026-11-05. The earlier source review incorrectly stated that DyFlex financial details remained undisclosed. This is a review omission, not a disagreement between the issuer PDF and SEC HTML. Raw source files and the original A120 analysis remain unchanged. Previous derived-report versions are preserved in revisions/pre_dyflex_correction_20261105_0316UTC.

## Exact source context

**Q3 2026 Form 10-Q, Note 13 — Subsequent Events, Acquisition, printed page 28:**

> On October 21, 2026, we entered into a definitive agreement to acquire DyFlex Solutions, a leading SAP transformation firm headquartered in Australia, for approximately $210 million in cash payable upon closing, subject to customary closing adjustments. This acquisition is expected to strengthen our enterprise platform and AI and SAP capabilities in the region.

This exact normalized paragraph occurs in both the SEC HTML (S02, preserved text lines 5724–5726, with the inline-XBRL number broken across separate lines) and issuer-hosted PDF (S14, preserved text lines 1422–1425). The raw HTML did not omit the price. Both documents present approximately **USD210 million in cash payable at closing**, subject to customary closing adjustments. There is no disclosed net-acquired-cash figure or standalone DyFlex revenue/EBIT in these passages. Note 13 does not state the expected closing quarter.

SEC HTML: https://www.sec.gov/Archives/edgar/data/1058290/000105829026000041/ctsh-20260930.htm

Issuer PDF: https://cognizant.q4cdn.com/123993165/files/doc_earnings/2026/q3/filing/Form-10Q-Q3-2026.pdf

**October 21, 2026 acquisition announcement, closing paragraph (S09):**

> The transaction is expected to close in the first quarter of 2027, subject to required regulatory approvals and the satisfaction of other customary closing conditions. Until closing, Cognizant and DyFlex will continue to operate as separate businesses. Financial details were not disclosed.

**October 29, 2026 corrected earnings-call transcript, management outlook, preserved text lines 466–468 (S07):**

> Our revenue guidance includes approximately 150 basis points of inorganic growth, which is unchanged. Our M&A pipeline remains active. The DyFlex acquisition we announced last week is expected to close in the first quarter of 2027.

Thus the original announcement's nondisclosure wording was superseded by the later 10-Q's consideration disclosure. The Q1 2027 expected-close statement is consistent in the announcement and call and is not contradicted by the 10-Q.

## Model implications for parent integration

- Funded-growth case: approximately USD210m belongs within a 2027 acquisition budget already covering announced deals. Against the parent's illustrative USD994m budget, it uses about 21.1%, leaving USD784m for other transactions before adjustments. Do not add USD210m again on top of that budget.
- Owned-business cross-check: include DyFlex as an announced-deal exception with approximately USD210m cash at its expected Q1 2027 close, or explicitly label exclusion as a counterfactual. Carrying no future M&A cash outflow is not an accurate depiction of announced management plans.
- Cost recognition: choose forecast acquisition cash flow or a corresponding valuation bridge deduction, once. The amount was not a September 30 balance-sheet cash payment. It does not belong in the 2026 Q4 cash stub merely because the agreement was signed in October.
- Deal value: unknown standalone revenue, EBIT, acquired cash and allocation prevent assigning a sourced revenue increment, purchase multiple, amortization or value-accretive return. An assumed price/sales sensitivity may be used only as a clearly labeled scenario. Do not count growth from the deal as free, and do not present a pure cost-only stress as an unbiased estimate of its economic value.
- No main valuation model has been changed in this correction.

## Corrected artifacts and checks

Updated source_review.md, forecast_inputs.json, source_index.csv, qa_flags.csv and build_package.py; added primary PDF source S14 and made S09's nondisclosure note specific to its publication date. All historical financial values remain unchanged. validation_checks.json now has 23 checks, all passing, including PDF/HTML price agreement, announcement/call timing agreement and structured-input amount agreement.
