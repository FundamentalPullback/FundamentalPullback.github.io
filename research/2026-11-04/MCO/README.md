# MCO research support

Conditional research as of 4 November 2026. No Stage3 integral certification, entry or execution approval. Values are scenarios, not guaranteed price ceilings.

Offline reproduction: python build_financials.py; python model.py; python comps/calculate.py; python peers.py; python report.py; python qa.py.

Python standard library only for these scripts. Financial history reads portable necessary numeric rows extracted from issuer tables. Full SEC filings are deliberately not redistributed. extract.py/fetch.py are local collection utilities, not required or included in the public package. Source URLs and table identifiers are provided; original filings remain available at the issuer/SEC.

Q4 cash/income amounts are annual minus 9M, but EPS Q4 is directly reported from the quarterly release. EPS TTM is the sum of quarterly EPS. Owner cash is not normalized distributable capital. Derivative/pension and perimeter reservations are material limitations of the analysis; see report.

prepare.py regenerates metadata and the English evidence appendix; not required for numeric reproduction. package.py creates ZIP and per-member checksums. Optional HTML rendering requires Pandoc. checksums.txt excludes its own hash. The external manifest additionally identifies ZIP, report, model and metadata.
