# Stock research profiles

The `#fichas` search and `#ficha/TICKER` profiles are built in the browser from the existing published scanner, decisions, management, operations and library data. No generated ticker index or per-ticker HTML page needs to be rebuilt.

## Normal daily publication

1. Publish new scanner rows in the scanner chunks listed in `data/manifest.js` (`files`). Keep historical rows.
2. Publish new/updated decisions in `data/dec.js`, preserving its header schema and explicit analysis depth, analysis date and report IDs. Full Stage 3, quick/blocked research and limited/list reviews are distinct.
3. Publish the report in the loaded library. The existing library loader is supported. Alternatively set `libraryFiles` in the manifest to the complete ordered list, starting with `data/lib.js`, followed by every extension file.
4. Update `manifest.generated` for every data/research publication, including research-only updates. Commit the related files atomically so a deployment represents one publication.

The website fetches the manifest without using its browser cache at startup, checks for a new version every 60 seconds while visible and when the tab becomes visible, then reloads the current profile/search URL. Data and library scripts use the publication version as a cache key. GitHub Pages deployment/CDN propagation still occurs before a publication is available. A profile's “Check now” control checks the manifest immediately. No external spreadsheet edits appear until the normal website publication step runs.

## Standalone reports and precise completion dates

For a report without a Decisions row, or when publication date differs from research completion, give the report an optional `profiles` array:

```js
{
  id: 'A149',
  date: '2026-11-04',
  cat: 'Selección y valoración',
  title: 'EXAMPLE — research update',
  text: 'The original report...',
  profiles: [
    {ticker: 'EXAMPLE', company: 'Example Inc', kind: 'complete', completedAt: '2026-11-04', label: 'Stage 3 completo'}
  ]
}
```

Kinds: `complete` (completed analysis), `review` (completed research review, qualification in `label`), `partial` (substantive but unfinished research), `management` (position management only). Use `completedAt` only when that date is documented; for partial/management it identifies the documented source event, not a completed-analysis claim. A report may cover multiple tickers with different kinds. Mere ticker mentions and a mixed report's overall category are not completion evidence.

The search engine contains a small documented migration annotation for legacy reports whose original rows lack reliable source/completion metadata. New reports should carry their own metadata rather than expanding a separate ticker index. All original text and data remain unchanged.

## Date and research semantics

- First/last scanner dates come only from actual dated scanner appearances in the available archive, not decision rows or report timestamps.
- Latest available research may be partial or blocked. Last completed analysis is shown separately.
- Limited/list reviews, Stage 1, pending research, administrative exclusions, Stage 4 management and trade records do not establish completed fundamental analysis.
- Completion dates come from explicit metadata, explicit valuation date for the source, source report date, or a dated analysis row when no report exists. Known legacy publication/completion discrepancies are annotated. Missing and invalid dates remain unknown; a scanner date never fills the gap.
- Linked reports use explicit source references or ticker subjects in titles. Other body mentions are kept in a separate clearly labelled section and do not establish completion.
- The feature is a read-only view. It does not modify strategy rules, valuations, positions or trades.

## Card-first search summary

An exact ticker or a company query yielding one match shows the visual stock card immediately. The same card is the first section of every stock profile.

The card derives its numbers from the current source records. The scanner price is paired with the displayed model's historical scanner observation; a later scanner observation is shown separately. Model dates and research-completion dates are independent. A later review that explicitly says no new valuation retains a dated earlier model. A later record withholding or withdrawing valuation does not restore an earlier numeric estimate on the main card. Bear/base/bull numbers always come from one model record; they are not probability bounds or guaranteed price targets.

Closing prices are read only from published closing-price history, strict structured regular-close records in reports, or audited legacy report metadata. The card never relabels delayed live prices, scanner Last, sale execution prices or account snapshot prices as a regular close. Dates are always visible; absent and conflicting closes are withheld. Report-documented closes are described as such, not as fresh market checks. The close display may be older than the latest market session.

Optional per-report `profiles` metadata supports standalone sources without a Decisions row:

```json
{"ticker":"EXAMPLE","kind":"partial","summary":"Concise qualified conclusion","summaryEn":"English qualified conclusion","valuation":{"status":"conditional","currency":"USD","asOf":"2026-11-05","bear":20,"base":30,"bull":40,"label":"Modelo condicional","labelEn":"Conditional model"},"close":{"price":25,"sessionDate":"2026-11-04","priceType":"regular-close","currency":"USD","source":"Published source URL or report ID","note":"Límites de la fuente","noteEn":"Source limits"}}
```

`valuation.status:"unavailable"` explicitly withholds valuation and suppresses older numeric models. Never populate valuation fields with an unapproved sensitivity table that the research does not regard as a usable model. Numeric metadata takes precedence over legacy annotations. USD is the journal's existing currency; explicit other currencies are rejected until supported.

A137's bounded-priority JSON records are parsed with a strict schema match (`fundamental_pullback.bounded_priority_record.v1`) and ticker, regular_close, regular_close_date. Free-text dollar amounts are never inferred. Four existing prose-only sources (A111, A143, A145, A146) have audited migration annotations; these do not form a static ticker index and newer report metadata supersedes them.

The normal manifest refresh and new-publication behavior remains unchanged. New tickers, new models and new structured close facts appear from newly published data without a separate search-index rebuild.
