import json
from pathlib import Path
P=Path(__file__).resolve().parent
rf=.0495;erp=.0441;beta=.81;ke=rf+erp*beta;kd=.08;dw=.35;tax=.245
x={'riskFree':rf,'riskFreeDate':'2026-11-03','erp':erp,'erpDate':'2026-11-01','erpAssociatedRiskFree':.0529,'beta5Y':beta,'costEquityMechanical':ke,'selectedMarginalDebtCost':kd,'selectedDebtWeight':dw,'taxRate':tax,'mechanicalWacc':ke*(1-dw)+kd*(1-tax)*dw,'parentSelectedWacc':.10,'targetSelectedWacc':.105,'sources':{'treasury':'https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?field_tdr_date_value=2026&type=daily_treasury_yield_curve','erp':'https://pages.stern.nyu.edu/adamodar/New_Home_Page/home.htm','beta':'https://stockanalysis.com/stocks/cvi/statistics/','debtCoupons':'https://www.sec.gov/Archives/edgar/data/1376139/000137613926000043/cvi-20260930.htm'},'meaning':'Mechanical historical-beta reference, not a certified post-acquisition WACC. Selected discounts include discretionary transaction, normalization and execution risk. Debt weight and marginal debt cost selected; Existing parent coupons7.5%/7.875%; new debt8% is a proforma assumption, not final terms. Monthly ERP uses a different dated Treasury.'}
x['parentCushionBasisPoints']=(.10-x['mechanicalWacc'])*10000
(P/'rates_results.json').write_text(json.dumps(x,indent=2)+'\n');print(x['mechanicalWacc'],x['parentCushionBasisPoints'])
