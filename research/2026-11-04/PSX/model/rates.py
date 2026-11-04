import json
from pathlib import Path
P=Path(__file__).resolve().parent
rf=.0495;erp=.0441;beta=.67;tax=.24;dw=.15;spread=.015
rawke=rf+beta*erp;selectedke=rf+1*erp;kd=rf+spread
mechanical=selectedke*(1-dw)+kd*(1-tax)*dw
out={'treasuryDate':'2026-11-03','treasury10y':rf,'erpDate':'2026-11-01','erp':erp,'erpAssociatedTreasury':.0529,'provider5YearBeta':beta,'providerBetaKe':rawke,'selectedCyclicalBeta':1,'selectedBetaKe':selectedke,'financialDebtWeightAssumed':dw,'creditSpreadAssumed':spread,'pretaxKdAssumed':kd,'mechanicalWacc':mechanical,'selectedBaseWacc':.095,'selectionCushionBp':(.095-mechanical)*10000,'monthlyRfAlternativeWacc':.0529+erp*.85+spread*(1-tax)*dw-.0529*tax*dw,'notes':['Monthly ERP and daily Treasury are not same-date implied risk estimates.','Beta1 is a selected cycle-risk proxy, not measured bottom-up beta. Credit spread150bp and debt weight15% are assumptions, not bond quote or market capitalization normalization.','Selected9.5% WACC is discretionary cushion, not rounding. Affiliate equity cash flows discounted11%, not WACC.'], 'sources':['https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?field_tdr_date_value=2026&type=daily_treasury_yield_curve','https://pages.stern.nyu.edu/adamodar/New_Home_Page/home.htm','https://stockanalysis.com/stocks/psx/statistics/']}
(P/'rates_results.json').write_text(json.dumps(out,indent=2)+'\n')
