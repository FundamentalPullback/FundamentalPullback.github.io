# VLO conditional cycle-normalized research
No trade approval and no fully certified Stage 3. DCF is a new analyst scenario model, not issuer guidance or a replication of A123.

Reproduce offline with Python standard library:
1. python history/portable/portable_builder.py
2. python history/portable/segments_and_caveats.py
3. python comps/mpc/calculate_mpc.py
4. python model.py
5. python peers.py
6. python report.py
7. python prepare.py
8. python qa.py

Numerical statements and filing URLs are included in history/portable/sourcefacts.json; no full filings are redistributed. facts/ contains numerical source-table rows from the September 2026 10-Q. Capital caveats and dated FY2025 proxies are in the report and segments_and_caveats.json. The model separately funds cash capex, turnaround/catalysts, new finance lease assets and economic reinvestment. No future subsidized credit extension is assumed automatically. Unknown total interim SBC remains null; expense stays in EBIT.

The report is generated from scripts and inputs. Changes must be made in source scripts as well as regenerated artifacts. checksums.txt covers packaged files except itself; manifest.json outside ZIP records final key hashes. package.py needs Pandoc only for the optional HTML rendering, not financial reproduction.
