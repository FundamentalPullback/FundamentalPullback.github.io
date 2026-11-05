# STNG fleet valuation

Market date: 4 November 2026. Research completed 5 November 2026.

## Decision

No Stage 3 approval at the 85.05 USD regular close. The 95.44 USD continuity base is plausible but not robust enough for the risk. Around 75 USD, with an indicative 72–76 review zone, merits a fresh assessment if the thesis survives. This is not a limit order, fair-value band or automatic buy. No trade is authorized. Technical eligibility must be rebuilt if the price changes.

## Read first

1. `report/STNG_valoracion_flotas.md`: complete investment conclusion, assumptions, FCFF, equity bridge, sensitivities, sources and exact remaining uncertainty.
2. `independent_audit.md`: independent arithmetic and economic review, including corrections.
3. `technical/review_draft.md`: current technical evidence and explicitly unapproved ticket.
4. `outputs/stng_fleet/STNG_fleet_FCFF.xlsx`: custom formula-supported audit workbook. The vessel engine supplies operating inputs; spreadsheet formulas calculate FCFF, discounting and equity bridge. It is not an end-to-end editable vessel simulator or a banker-formula-template workbook.

## Portable numerical reproduction

Requirements: Python 3.10+ with NumPy and SciPy. No network or connected account is needed. All primary inputs consumed by the engine are in this package.

From this directory:

    python model/build.py
    python model/analyze.py
    python report/build_package.py
    python report/make_report.py
    python technical/calculate_technicals.py
    python audit/independent_tests.py
    python audit/workbook_qa.py

The first two commands overwrite only the generated model results in this copy. They do not edit archived sources. Expected v2 values before rounding: base95.4435700563; bear forced-continuity17.8775075976; bull raw184.8730717272; coherent full-conversion bull176.8504291982. Runoff bear49.4025754043 is a sensitivity, not a liquidation floor.

`model/analysis.json` contains reverse valuations, structural sensitivities and the finite-runoff comparison. `model/decision_sensitivities.json` includes future replacement payment lead-time tests. `audit_checks.json` contains independent tests and marginal project IRR diagnostics. The 11-year displayed FCFF includes Q4 2026 plus ten full forecast years, not eleven full forecast years.

## Workbook reproduction and limits

The workbook creation script is `outputs/stng_fleet/build_workbook.mjs`. It requires Node.js and the @oai/artifact-tool runtime used for the export. It reads the numerical JSON generated above. Recreating the XLSX is optional for reproducing the economics. It does not fetch sources, send messages or publish anything. Its preview PNGs and inspections are QA only.

The generic formula template does not support the required vessel-by-vessel cohort renewal and contract-expiry architecture. This package uses a custom deterministic fleet engine with live spreadsheet FCFF/discount/bridge formulas instead of a generic CAGR substitution. The export is labeled honestly and does not claim banker_formula_workbook certification.

## Integrity and scope

`manifest.json` records SHA256 hashes of final files. The prior audited dossier was not changed. `model/v1_unreviewed` preserves the corrected draft for audit history only; do not use its values. `sources/primary_archive` includes the original hull and guidance extracts. The larger prior history package remains separately available; this package includes the normalized history used in the review.

Current limitations are explicit: normal TCE is an estimate; discretionary renewals assume payment at delivery (lead-time tested); new JV economics receive zero positive value after all disclosed commitments are paid; convertible claim proxy is dated; future drydock dates are inferred. These are not invented fatal accounting alerts. The final no-approval decision is a price-versus-risk judgment under the plan, not a fixed margin rule.

## Export quality checks

The workbook has 11 visually reviewed sheets and 2,619 live formulas, with no cached errors or missing formula caches. 1,552 numeric checks tie the FCFF, discounting and bridge values to the audited engine. `outputs/stng_fleet/model_citations.json` maps cells to the source ledger. Reproduction overwrites generated outputs in the working copy, so verify the release manifest before running it.
