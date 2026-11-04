# EAT exploratory conditional FCFF
Run offline in order:
1. python history/rebuild_history.py
2. python comparables/reproduce.py
3. python model.py
4. python report.py
5. python prepare.py
6. python qa.py
Optional package.py writes manifest andsupport.zip. No network/externalpackages. Original filings and fullcompanyfacts omitted; selected numerical observations retain SECaccession/date/tag/unit/start/end. Model finances positive change inNOPAT and physical capex including newfinanceleaseassets; terminal preserves both floors. Operatingleaseexpense stays inEBIT, financeleasedebt is deducted. WACC/ROIC are assumed, not calibrated. Postquarter65buybackreserve and historicaltax/guaranteeitems are not a certifiedcurrentbalance. Allhistorical/scannerprices remain identified separately. No entry or latestCompleted.
