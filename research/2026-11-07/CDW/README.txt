CDW research · 7 November 2026

Open report.html first. This is preliminary research, not a completed Stage 3 review or an approved valuation. No entry, stop, position size or trade is authorized.

Reproduce using Python 3 with its standard library:
  python calculate.py
  python audit.py

calculate.py reads inputs.json and regenerates historical calculations, the original ten-year scenarios, a separate full-period economic-reinvestment stress, inverse calculation, sensitivity and numerical QA. audit.py checks local links and public-content hygiene and deterministically restores readiness and quote-provenance annotations. report.html is the reviewed narrative snapshot; scripts do not regenerate its prose. If inputs change, update narrative and captions and obtain a new review before using them.

The original cases use physical/software net investment plus incremental operating working capital in explicit years, and an economic reinvestment floor in terminal. The stress separately applies the economic floor to every explicit year. Neither is a certified fair value. Full-period stress uses opening NOPAT 1,401.856 and max(max(0, change in NOPAT)/case ROIC, physical net investment plus working capital). Terminal formula is unchanged.

Source-ledger records only public document URLs, titles, dates and purposes. Only own analysis, derived inputs and reproducible calculations are included. Original filings are not redistributed. Evidence captions are verbatim contiguous report sentences; they are derived research conclusions, not management quotations.

Visual review was not completed. Structural and numerical checks do not replace it.

Readiness: stage3Complete=false; approvedValuation=null; entryApproved=false.
