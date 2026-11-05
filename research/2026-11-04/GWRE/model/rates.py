from pathlib import Path
import json
p=Path(__file__).parent
rf=.049;erp=.0441;beta=1.03;ke=rf+erp*beta;eq=170.5*81.992669;debt=690;kd=.06;tax=.24
x={'riskFree':rf,'equityRiskPremium':erp,'historicalBeta':beta,'mechanicalCostEquity':ke,'selectedDebtRefinancingCost':kd,'proxyPreDealWacc':ke*eq/(eq+debt)+kd*(1-tax)*debt/(eq+debt),'selectedBaseDiscount':.095,'selection':'9.5% selected with capital/perimeter risk; not rounding or a certified post-acquisition WACC. Coupon1.25% not marginal debt cost. New loan floating SOFR +1–2%; no observed yield assumed.','sources':['https://home.treasury.gov/resource-center-data-chart-center/interest-rates/TextView?type=daily_treasury_yield_curve&field_tdr_date_value=2026','https://pages.stern.nyu.edu/~adamodar/','https://stockanalysis.com/stocks/gwre/statistics/']}
(p/'rates.json').write_text(json.dumps(x,indent=2)+'\n')
