# TSM partial fundamental refresh
No DCF or certified intrinsic value. Unknown values remain null. This is not a completed Stage 3 or an approved trade.

Reproduce offline in this order:
1. python history/build_history.py
2. python comps/build_peer_fundamentals.py
3. python build_analysis.py
4. python report.py
5. python prepare.py
6. python qa.py

Use NTD millions in financial history, explicit USD only where labeled. ADR represents five ordinary shares. Ordinary diluted shares are an average denominator, not current outstanding shares. IFRS CFO excludes interest paid/received, and Q3 omits intangible/lease/SBC details. CFO less PPE is never labeled owner FCF.

Full original statements and licensed transcript are retained locally for review but are not distributed. history/SOURCES.md and analysis.json link issuer documents. Scripts contain transcribed numerical facts and null propagation. comps/ contains only numerical facts, original analysis and source links. checksums.txt covers each packaged file except itself. Package includes no raw copyrighted filings.
