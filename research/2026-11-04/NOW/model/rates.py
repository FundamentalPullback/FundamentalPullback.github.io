import json
from pathlib import Path
P=Path(__file__).resolve().parent
rf=.0495;erp=.0441;beta=.99;dw=.07;kd=rf+.012;ke=rf+beta*erp;w=ke*(1-dw)+kd*.75*dw
out={'marketDate':'2026-11-03','rf10y':rf,'erpMonth':'2026-11-01','erp':erp,'erpAssociatedRf':.0529,'providerBeta5y':beta,'capmKe':ke,'selectedDebtWeight':dw,'selectedCreditSpread':.012,'selectedPretaxKd':kd,'mechanicalWacc':w,'selectedWacc':.095,'discretionaryBufferBp':(.095-w)*10000,'sources':['https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?field_tdr_date_value=2026&type=daily_treasury_yield_curve','https://pages.stern.nyu.edu/adamodar/New_Home_Page/home.htm','https://stockanalysis.com/stocks/now/statistics/'],'notes':['Monthly ERP and daily Treasury not synchronized.','Credit spread and debt weight are selected assumptions, not observed bond yield or fixed capital structure.','9.5% WACC includes discretionary integration/model-risk allowance, not rounding.']}
(P/'rates_results.json').write_text(json.dumps(out,indent=2)+'\n')
