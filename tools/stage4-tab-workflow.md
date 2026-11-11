# Stage 4 daily-review tab

The public `#stage4` route shows the newest published management review and a selector for its dated archive. `#stage4/A547` opens a specific published report, including on reload or browser history navigation.

## Publishing the next daily review

- Publish the original library report through the existing authorized workflow and register its chunk in `data/manifest.js`.
- Use category `Gestión de posiciones`, a title containing `Stage 4`, and the ISO `marketSession` date for the session reviewed. The normal report `date` remains the publication date. Add `effectiveSession` when the levels apply prospectively to another session.
- The tab discovers the new report automatically. It sorts on `marketSession` (otherwise the documented historical override or report date). On one date, closing reviews precede explicitly intraday reviews, then the higher report ID is shown first. No new signal or validity is inferred from this ordering.
- A `## Decisión de gestión` section appears verbatim in the alert summary. If absent, no automatic financial summary is invented. The full original report is always displayed.
- Historical combined reports are explicitly included in `stage4Reports()`; this does not turn partial, intraday or carried-forward material into a verified close. Their original titles and full limitations remain visible. A290 and A494 have explicit session-date overrides because their older records used later publication dates.
- Never add private account identifiers or unpublished data. The tab does not alter quantities, references, orders, or portfolio state.

Run `node tools/test-stage4-tab.cjs` and the full publication suite. Check the live tab, dropdown, original report link, mobile layout, and Back/Forward. Published reports must remain immutable. The exact UI predecessor contract supports dated historical regression tests; do not update hashes to hide unrelated changes.
