Valero primary financial facts reconstruction
Offline requirements: Python 3 standard library only. No full filings, network access, lxml, pandas, or companyfacts API download required.
Run: python portable_builder.py
Run: python segments_and_caveats.py
sourcefacts.json contains 218 raw reported numeric facts, tagged with source URL, filing, dates, units context, and consolidation dimensions. Calculations derive fiscal/quarter/TTM results from those primary inputs. Supplemental quarterly EPS comes from the cited SEC earnings release. segments_and_caveats.py contains manually transcribed primary annual segment inputs and calculates per-barrel metrics.
financial_history.json and segments_and_caveats.json are outputs, not inputs. They may be deleted and rebuilt.
FY2025 Note 8 book liability for unrecognized tax benefits is441m; Note15 gross UTB rollforward is315m. The126m difference remains unreconciled. Do not add both or attribute difference to immaterial interest/penalties. Environmental liabilities275m, ARO382m, benefit liabilities472m are separate balances.
