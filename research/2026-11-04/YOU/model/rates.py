import json
from pathlib import Path
x={'riskFree':.049,'riskFreeDate':'2026-11-04','erp':.0441,'erpDate':'2026-11-01','beta5Y':.92,'mechanicalCostEquity':.049+.0441*.92,'selectedDiscount':.10,'debtDrawn':0,'sources':['https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?field_tdr_date_value=2026&type=daily_treasury_yield_curve','https://pages.stern.nyu.edu/adamodar/New_Home_Page/home.htm','https://stockanalysis.com/stocks/you/statistics/'],'limits':['10% is selected risk premium above8.9572%, not a rounded issuer WACC.','Beta/ERP combination is analytical; partnership concentration, TSA rules and Up-C allocation remain uncertain.']}
(Path(__file__).parent/'rates_results.json').write_text(json.dumps(x,indent=2)+'\n')
