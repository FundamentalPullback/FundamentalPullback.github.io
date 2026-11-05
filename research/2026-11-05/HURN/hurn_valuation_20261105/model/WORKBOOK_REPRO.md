# HURN workbook reproduction

Run from any directory:

1. python model/build_workbook.py
2. node model/verify_workbook.mjs
3. python model/qa_workbook.py

The build reads assumptions.json, results.json, analysis.json and ../source_ledger.json. It does not modify the canonical economic model. Python xlsxwriter writes the deliverable and an independent recursive spreadsheet evaluator caches all formulas. Artifact Tool imports and recalculates the workbook, verifies a strategic-capital change and restores it, renders every sheet, and exports a QA-only roundtrip copy. The original source-formatted HURN_DCF.xlsx is the deliverable. Excel and LibreOffice were not available and native application recalculation is not claimed.

The bundled formula builder was smoke-tested separately on its illustrative example. Its six-column template cannot represent the canonical ten-year-plus-Q4 model. Its output is diagnostic only and must not be distributed as HURN or included in the user-facing package. The HURN deliverable is custom_formula_first, not banker_formula_workbook.

All three main cases are live formula schedules. The four joint scenarios on Cover are explicitly labeled static Python snapshots. Changes made only inside Excel do not update these snapshots or the Python canonical-control values in Checks.
