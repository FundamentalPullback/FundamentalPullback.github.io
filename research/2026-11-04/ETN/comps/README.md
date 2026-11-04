# Limited electrical peers, 4 November 2026

Prices are the 3 November 2026 completed US session. All dollars are USD millions except share prices. Run `python reproduce.py` offline to recreate `results.json` and `results.csv` using frozen `inputs.json`. `sources.json` lists public URLs, dates and SHA-256 hashes; raw source files are in the sibling `sources/` directory. ETN inputs are copied from the existing primary-source history/capital work without editing it.

## Results

| Company | Nov 3 price | EV | TTM revenue | TTM operating income | TTM EBIT* | EV/revenue | EV/operating income | EV/EBIT* |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Eaton | $391.70 | 171,510.45 | 31,984.0 | 5,537.0 | 5,490.0 | 5.36x | 30.98x | 31.24x |
| Hubbell | $449.27 | 28,514.60 | 6,593.7 | 1,332.6 | 1,308.2 | 4.32x | 21.40x | 21.80x |

*EBIT is pretax income plus net interest expense, derived from GAAP amounts and retaining other nonoperating items. Operating income is separately shown because it is not identical to this EBIT definition. Eaton operating income is calculated from revenue less cost of revenue, SG&A and R&D. No adjusted EBITDA substitution is made.

EV = price × actual shares + carrying debt − cash − short-term investments + book NCI. These are limited conventional EVs, excluding incremental pension/lease/tax/other economic-claim adjustments in a fuller valuation bridge. Long-term investments are not deducted without proving they are excess liquid assets. Actual share counts are dated September 30 for ETN and October 22 for HUBB; balance sheets are September 30. This is not a contemporaneous Nov 3 balance sheet or a diluted-options valuation.

HUBB TTM = FY2025 + nine months 2026 − nine months 2025: revenue 5,844.6 + 5,101.0 − 4,351.9; operating income 1,208.8 + 1,021.1 − 897.3. Pretax income is 1,119.1 + 885.4 − 837.6 and net interest is 64.1 + 119.1 − 41.9. Sources: [FY25 release](https://hubbell.gcs-web.com/news-releases/news-release-details/hubbell-reports-fourth-quarter-and-full-year-2025-results), [Q3 release](https://hubbell.gcs-web.com/news-releases/news-release-details/hubbell-reports-third-quarter-2026-results), [Q3 10-Q](https://www.sec.gov/Archives/edgar/data/48898/000162828026067729/hubb-20260930.htm), and [price history](https://stockanalysis.com/stocks/hubb/history/).

## Perimeter and interpretation

Hubbell's NSI acquisition closed June 9, 2026 for approximately $3 billion net cash. Reported results since closing include $197.9m revenue and $21.3m operating income. Current debt captures the acquisition financing while TTM income contains only partial NSI ownership. DMC/Nicor also affect growth comparability. Q3 organic growth was 11.3%, versus 13.2 percentage points of acquisition growth; Electrical Solutions organic growth was about 22%, Utility Solutions about 5%. These are reported-TTM multiples, not constant-perimeter or acquisition-pro-forma multiples. ETN likewise has acquisition timing and its announced Mobility transaction to reconcile; do not mix this current consolidated EV with a future separated-company denominator.

ETN trades above HUBB on both displayed denominators. This observation is not a peer-derived target price or proof of overvaluation: market mix, growth, financing, amortization, acquisition timing and future separation differ. Two companies do not establish a meaningful peer median. No homogeneous EBITDA, owner FCF, SBC-adjusted cash yield, or peer target is inferred.

## ABB operating contrast only

[ABB Q3 results](https://www.abb.com/global/en/news/139696/q3-2026-results) show revenue $9,701m, income from operations $1,846m (19.03% calculated margin), and Operational EBITA $2,026m (20.8% published margin). Comparable revenue grew 14%, orders 40%. Electrification revenue was $5,424m, operating income $1,356m and Operational EBITA margin 25.6%. The latter uses operational revenue and adjustments and must not be treated as the same measure as consolidated GAAP operating margin. Hubbell Q3 operating margin is 21.83%; ETN calculated consolidated margin 17.75%; mix and corporate allocations limit comparisons.

[ABB financial information](https://search.abb.com/library/Download.aspx?Action=Launch&DocumentID=9AKK108473A4463&DocumentPartId=&LanguageCode=en), pages 6, 13, 16 and 31: Robotics is discontinued, with conditional closing expected Q4 2026; related stranded corporate costs remain in continuing results. Rotork is pending, expected H1 2027, and the Mitsubishi Electric 51%-controlled JV is expected H2 2027. Do not add announced acquired earnings or subtract prospective Robotics proceeds from current operating figures. No ABB market multiple is offered because the share/ADR, CHF/USD and transaction perimeter bridge was not reconciled in this limited comparison.
