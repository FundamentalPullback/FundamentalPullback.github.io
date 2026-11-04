import json
from pathlib import Path
p=Path(__file__).parent;rf=.049;erp=.0441;beta=.28;ke=rf+erp*beta;d=4441;e=88.28*118.602638;kd=.055;tax=.26
x={'date':'2026-11-04','riskFree':rf,'equityRiskPremium':erp,'betaProvider5yr':beta,'costEquityMechanical':ke,'selectedDebtCost':kd,'mechanicalWacc':ke*e/(e+d)+kd*(1-tax)*d/(e+d),'selectedBaseDiscount':.09,'reason':'Discretionary premium for funding, acquisition perimeter and unstable backward beta; not rounding.','sources':['https://home.treasury.gov/resource-center-data-chart-center/interest-rates/TextView?type=daily_treasury_yield_curve&field_tdr_date_value=2026','https://pages.stern.nyu.edu/~adamodar/','https://stockanalysis.com/stocks/bah/statistics/']}
(p/'rates.json').write_text(json.dumps(x,indent=2,sort_keys=True)+'\n')
