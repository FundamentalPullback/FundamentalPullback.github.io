# Reviewed market-close ingestion

`import-account-history.py` accepts a reviewed JSON market-price snapshot and appends new sessions. It never reads private transaction exports or authenticates, schedules or publishes anything. The source, retrieval timestamp and date must be recorded. Input ticker closes must cover SPY and every position held on each new date. Existing dates are immutable. Run against a working copy and review the diff, sources and accounting tests before an atomic deployment.

The Nov7 reconciliation was authorized for minimized CTSH41@$66.69, HRB estimated fee$0.04 and explicitly provisional strategy totals. Do not infer authorization to publish new private trades from this example. Public data files must not include broker identifiers, source screenshots, private sheet IDs, raw exports or execution timestamps.

Import example: `python tools/import-account-history.py --site-root . --input /path/to/reviewed-market-closes.json`. JSON has `asOf`, `source`, `retrievedAt`, and `sessions` mapping ISO days to ticker/positive-number pairs. The input must contain successive expected regular trading sessions, with vendor discrepancies resolved and documented separately. The importer checks position coverage and rejects replacing historical dates. It does not decide market holidays or certify exchange prices. Run test-hrb-partial-sale.cjs and the full prepare-publication checks.

A future scheduled ingestion must separately fetch verified closes after the provider publishes them, reconcile approved transactions, validate expected session dates and all held tickers, preserve provenance, run tests and publish atomically. A failed/incomplete fetch must retain the last verified dataset and expose its date. No daily scheduler is configured by this change.
