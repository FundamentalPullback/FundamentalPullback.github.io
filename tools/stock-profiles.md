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


The main summary card intentionally omits a documented-close tile. Its three numeric tiles are the dated scanner price, estimated value and bear/bull scenarios. The provider quote is shown separately above them. Historical close records, source reports, provenance and conflict checks remain intact; they are not presented as the latest market close. At narrow widths the scenario tile spans both columns.

## Previous and next within search results

The stock card's previous/next controls use the same result builder as **Find a stock**. They retain the company/ticker query, the all/completed/no-completed-analysis filter, and the existing ticker A–Z order. The center shows the current position and cohort description. The first previous button and last next button are natively disabled; navigation never wraps.

Search state is encoded in the hash, for example `#fichas?q=holdings&filter=complete&sort=ticker` and `#ficha/WMG?q=holdings&filter=complete&sort=ticker`. Every result link, adjacent-stock link, and **Back to results** link carries these criteria. Search edits replace the current list's history entry, while opening or stepping between profiles creates normal browser history entries. Reload, copied links, Back, and Forward restore the criteria without depending on session storage. A legacy/direct `#ficha/WMG` bookmark explicitly uses **All stocks · Ticker A–Z**, not a previous search left in memory. Links specifying an unsupported filter/order disable cohort navigation until the user returns to search.

An exact ticker (or any nonempty query with one match) still shows its card inline. Its navigation displays **1 of 1**, with both arrows disabled, and **View research and history** retains that one-result context. No results shows the existing empty state, with no fabricated neighbors.

Each publication recomputes the results from the same criteria using current published data. Newly published profiles and completed analyses enter automatically; removed or no-longer-matching profiles leave automatically. If the current ticker disappears or no longer belongs to its saved results, both arrows are disabled with an explanation and a return-to-results link. The page never silently jumps to a different stock. The existing publication reload preserves the full hash.

The controls use native links and disabled buttons, translated English/Spanish labels, visible focus outlines, and at least 44px target height. At narrow widths the result context occupies its own row above the two controls. Below 421px, visible button labels shorten to the arrow and ticker while full translated accessible labels remain. Keyboard focus survives filter changes and stepping through profiles; at an endpoint it moves to the newly opened stock's heading. No global arrow-key shortcuts intercept typing or browser navigation. Each stock change re-renders and mounts the existing TradingView quote for the newly selected symbol; it does not retain a previous stock's widget.

Run the existing profile/card/quote suites plus `node tools/test-stock-navigation.cjs`. The navigation suite covers all currently published profiles in all/completed/other cohorts, both languages, A–Z adjacency and boundaries, multi-result queries, one/zero results, special-character URL encoding, direct/invalid links, state restoration, and changing publications (new profiles, new completions, removed/current-out-of-cohort symbols).

## Recorded-status filter

**Recorded status / Estado registrado** filters each profile by the exact `decision` value in its `latestReview` Decisions row. It does not infer state from scanner scores, completed-analysis flags, research prose, prices, position holdings, or trade history. The existing profile engine chooses that row by analysis date, with scanner date as its tie-breaker. A later missing/blank decision is **No recorded decision**, not a recovered older approval.

The six options come from the site's existing `DEC_ORDER`, using its existing translations and colors: Ready for Stage 3.5, Passed Stage 3, blocked, Held, Wait for price, On watch, and Rejected. They remain separate, including zero-count options. **No recorded decision** covers profiles without a usable Decisions status; their research-depth labels remain displayed separately. **All statuses** includes every category. No broad “Approved” filter is introduced, and neither approval-related category implies a current actionable entry.

Status is a historical record, not the current holdings ledger or trading permission. The search and cards state this explicitly, and cards display the recorded decision's analysis date without substituting a scanner date. This matters for old or conditional rows, such as ASO's October 12 status, AVY's expired plan, and EDU's suspended plan. Status filtering changes no rows, positions, execution flags, approvals, or valuation data.

The summary card, search result badge, and filter identity share `profileStatus()`; profile review/history badges use the same neutral-safe renderer for their own displayed source rows. Unknown future source labels receive distinct **Other recorded status: [source label]** options and neutral badges, never the legacy rejected fallback. Source wording is retained and HTML-escaped, including in English when no canonical translation exists.

Option counts apply the current search and completed-analysis filter **before** the selected status. Selecting a status then narrows the same result builder used by previous/next. Thus each count shows how many results that option would return without changing the other controls. A saved status that disappears from current published data remains selected as an explicit unavailable option with zero matches; it never resets to all stocks. New publications automatically update statuses and counts from their source rows.

URLs add `status=decision%3AEn+observaci%C3%B3n` (for example), or `status=none` for no recorded decision. Exact source labels are prefixed with `decision:` so even literal future values `all`, `none`, `constructor`, or `__proto__` cannot collide with control values. Default all-status URLs omit the new parameter, preserving earlier links. Search changes, filter changes, inline cards, profile arrows, Back to results, reload, and browser history retain the combined criteria.

The status select uses a native associated label and description, a 44px minimum height, visible focus, and focus restoration after render. Search controls stack at narrow widths. Run `node tools/test-stock-status.cjs` in addition to the four existing suites. Publication preparation now runs each of those five suites once. Status tests include canonical source counts, all combinations of query/analysis/status in ES/EN, exact neighbors, URL/history compatibility, focus, source immutability, historical-approval caveats, no-decision research labels, neutral escaped future values, disappearing categories, and subsequent published decisions.


## Research workspaces

The Research menu contains Find a stock, Daily review, Analysis and Hindsight. Daily review (`#revision`) keeps one selected date across its overview and scanner panes. Its URL stores the panel, query, Stage 2 filter and both sort orders. Legacy `#resumen` and `#escaner` links still open the appropriate pane, including links from stock scanner history.

Find a stock has saved `view=approvals`, `view=waiting` and `view=history` contexts. `history=all` compares all matching historical decision records; the default compares each company's latest decision. The existing recorded-status filter always uses the company's latest decision and is separate from holdings or current entry authorization. Source Decisions, Operations, Management and account data are unchanged. Legacy `#aprobadas` and `#descartadas` open the corresponding saved views.

The decision comparison and per-company history tables retain execution/expiry warnings, dated valuations, report sources, next event, reasons, return/excess fields and row-detail/calculation access. Hindsight retains its independent outcome cutoff. Run `node tools/test-research-workspace.cjs` alongside the stock-profile regression suites before publication.


## Scanner-session filter

The default All stocks option preserves the full directory with no scan restriction. All scanner sessions (`scans=any`) includes the union of tickers appearing in any valid published scan session. Latest scan (`scans=1`) and Last N scans (`scans=N`) use the newest N distinct published scan dates, not calendar days. The set is a union without duplicate tickers; it is not a requirement to appear in every session or to pass Stage 2. The filter intersects with search, research depth, recorded status and saved decision views.

All-stock URLs omit the parameter for backward compatibility. Selected scan scope flows through profiles, previous/next, Back, reload and history. Invalid/zero/fractional/unsafe counts return no cohort with a validation message; oversized N uses the available sessions and retains the requested value so later publications expand the window automatically. Empty scan data returns no scanner-filtered records, while unrestricted All stocks still exposes research-only records. Custom input mode stays visible while the user types a first digit 1. Run `node tools/test-stock-scan-filter.cjs` with the six other suites.


## Persistent profile navigation

Previous/next links remain the existing filtered ticker cohort. At desktop widths (900px+) with at least 600px height, fixed controls sit in reserved side gutters outside all main panels. Phones and short landscape viewports use deliberate left/right touch swipes, with localized labeled inline links as a screen-reader, keyboard and tap alternative. No mobile controls cover the reading area. Swipe left advances, swipe right goes back, using the exact existing URL context. Passive gestures reject vertical scroll, short or slow movements, screen edges, selection, multiple touches, inputs, links, tables and quote widgets. Browser QA covers 320/375/390px, landscape, multiple depths, boundaries and browser history.


## Evidence-backed Pros & Cons

Every selected profile (including an exact one-result search) includes a compact research balance: green labelled Pros and red labelled Cons, with research date and a link to its source report. It sits to the right inside the stock card at 1100px+, outside the reserved navigation gutters. At narrower widths it follows the main card in normal document flow, never overlays it. Labels, signs and headings carry meaning independently of color. All research/status/quote/chart/navigation data remain unchanged.

The engine selects the latest completed source. If a later partial or blocked analysis exists, the panel says its update is pending instead of presenting older conclusions as current. A source-text change, including an appended correction, invalidates a migrated or structured summary until its evidence selection has been reviewed against that source revision. Passing an event's time, new provider prices, and live chart data cannot update research. Missing evidence is explicitly pending; absence of a selected positive or concern does not prove no such point exists.

Source order:
1. `profiles[].prosCons` with the schema below, bound to the enclosing report and its full-text fingerprint.
2. Exact ticker-scoped `## Pros · TICKER` and `## Cons · TICKER` sections (also Spanish `Puntos a favor` / `Riesgos`), with 1–3 short bullets per side. Author metadata must set `prosConsSectionsFingerprint` to the fingerprint of the reviewed report text. General business, thesis, growth or risks discussions are never classified by word sentiment or assumed positive headings. Mixed caveats in an explicit bullet stay intact.
3. Audited one-time source migrations in `tools/research-balance-legacy.json`, compiled to `data/research-balance.js`. They are keyed by report and ticker, with exact whole-report fingerprint and contiguous source evidence for every bullet. Multi-company reports require company-specific evidence.

Each new/revised research publication must provide short evidence-backed pros/cons as part of authoring the research (or provide reviewed `prosConsUnavailable` metadata where the source is insufficient). The site does not autonomously research companies or invent opinions. Selection, validation, compilation, refresh and display are automatic once the research is published. A generic old source cannot automatically become a reliable new conclusion.

Author metadata example (derive `sourceFingerprint` using `FP_PROFILE_ENGINE.balanceFingerprint(report.text)` after final research corrections):

```json
{"ticker":"EXAMPLE","kind":"complete","completedAt":"2026-11-05","prosCons":{"schema":"fp.research-balance.v1","asOf":"2026-11-05","sourceFingerprint":"<fingerprint of reviewed report.text>","pros":[{"text":"Ingresos recurrentes crecen un 9%.","textEn":"Recurring revenue grows 9%.","evidence":"Exact contiguous statement from this report.","sourceUrl":"https://exact-source-url-already-in-this-report"}],"cons":[{"text":"Persisten las bajas de clientes.","textEn":"Customer losses remain a concern.","evidence":"Another exact contiguous statement from this report."}]}}
```

Dates must be documented analysis dates, not scanner dates or an assumed event completion. Each displayed bullet is a short paraphrase of the exact evidence and retains material caveats. Evidence spans are verified in the report; optional HTTPS source URLs must appear there as well. Use 1–3 bullets per side, at most 320 Spanish / 360 English characters each. Keep only the clearest company-specific merits and concerns. Do not turn approval status, a cheap-looking ratio, a model sensitivity or a pending condition into a factual positive. English/Spanish text is supported; explicitly scoped prose retains its original language rather than pretending to translate it.

Run `node tools/build-stock-balance.cjs` then `node tools/test-stock-balance.cjs`; both are part of the normal publication preparation. The builder prints actual coverage and pending symbols. Include the compiled data, manifest and new research in the same atomic publication. The existing one-minute visible-tab publication check refreshes the current hash, without a separate index rebuild.

Tests cover every current profile in both languages and inline/direct cards, exact provenance, future/new/same-ID revised sources, stale fingerprints, newer incomplete research, multi-company scope, safe links/HTML, immutability, no live-price/event inference and responsive in-flow styling. Browser geometry and rendering are checked separately before release.

Publication is blocked if a completed current source has missing or invalidated summary evidence. To intentionally publish a pending summary, the report author must provide `profiles[].prosConsUnavailable` with schema `fp.research-balance-unavailable.v1`, matching `asOf`, current `sourceFingerprint`, and a concrete `reason` (12–320 characters), optionally `reasonEn`. This is an explicit editorial assessment, not a hidden success. A later partial/blocked source remains pending without being promoted to completed. The browser also fails closed if publication preparation is bypassed.

### Zero valuation versus missing data

Published numeric zero is a valid common-equity scenario, including a zero central estimate. Profile cards preserve finite nonnegative model values and display zero ranges in both languages. Null, undefined, blank, boolean, string, negative and nonfinite structured values are not treated as zero. A newer explicit zero model supersedes an older positive model; a newer withheld/null model remains unavailable. Scanner and close prices still require finite positive numbers. This display rule does not modify financial inputs, decisions or execution permission. `test-stock-cards.cjs` covers live VFC/SSL fixtures, future decision/report paths, zero-base and all-zero ranges, missing data and source immutability.


### Fundamental-only refreshes with unchanged management

A report profile may provide `scanner: {date, price, source: "published-scanner"}` to pair its new valuation with an existing scanner observation without modifying Decisiones or management. The renderer accepts the pair only when both date and price match a stored scanner row for that ticker. It does not create a scanner session, change execution eligibility, or infer a trade. An absent or invalid pair retains the existing fallback. The dated report must disclose that master-data/Sheet reconciliation is pending.
