# FRPT publication/reproduction packet

Cutoff: November 4, 2026, after the Q3 earnings release and before the 08:00 EST call.

Read FRPT_full_stage3_2026-11-04.md first. Values are USD/share; financial/model amounts are USD millions, except explicitly stated share counts and ratios. This completes the research as of released evidence. It does not approve an entry or predict call responses.

Python standard-library reproduction, in this folder:
1. python build_post_history.py: rebuild latest history from preserved prior history and exact issuer release table rows.
2. python model.py: regenerate three ten-year FCFF schedules, reverse and joint sensitivity, claim sensitivities and price-return grid.
3. python build_comps.py: regenerate dated comparable-company bridge, using NCI book proxies where market values are not disclosed.
4. python build_report.py: regenerate the report from the saved calculations and evidence narrative.

The independent audit reconciles final model outputs. The 51 historical checks are the prior-period source/arithmetic checks, not 51 checks of the final valuation. Supplementary reports carry their own earlier cutoff and are source appendices; the final report supersedes their pre-release status and initial model values. The raw issuer/SEC source documents are retained in the research workspace, with exact public links in the report and source maps. This compact publication packet includes extracted source rows/bridges, not every raw filing or prior unrelated site report.

Claims: principal and finance leases deducted; operating rents retained; convertible capped-call offset valued consistently; SBC stays an economic cost. Unreported Q3 notes, future call responses and post-release quotes are not invented. No fixed 15% discount rule applies.
