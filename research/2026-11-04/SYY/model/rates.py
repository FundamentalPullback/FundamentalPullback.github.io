import json
from pathlib import Path
P=Path(__file__).resolve().parent
rf=.0495;erp=.0441;beta=.64;ke=rf+erp*beta;kd=.062;dw=.35;tax=.25
x={'riskFree':rf,'riskFreeDate':'2026-11-03','erp':erp,'erpDate':'2026-11-01','erpAssociatedRiskFree':.0529,'beta5Y':beta,'costEquityMechanical':ke,'selectedMarginalDebtCost':kd,'selectedDebtWeight':dw,'taxRate':tax,'mechanicalWacc':ke*(1-dw)+kd*(1-tax)*dw,'syySelectedWacc':.085,'jrdSelectedWacc':.09,'sources':{'treasury':'https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?field_tdr_date_value=2026&type=daily_treasury_yield_curve','erp':'https://pages.stern.nyu.edu/adamodar/New_Home_Page/home.htm','beta':'https://stockanalysis.com/stocks/syy/statistics/','debtCoupons':'https://www.sec.gov/Archives/edgar/data/96021/000009602126000050/syy-20260926.htm'},'meaning':'Mechanical historical-beta reference, not a certified post-acquisition WACC. Selected discounts include discretionary transaction, normalization and execution risk. Debt weight and marginal debt cost selected; October coupons span5.45–7.35%USD and6%EUR, not one uniform risk-free spread. Monthly ERP uses a different dated Treasury.'}
x['syyCushionBasisPoints']=(.085-x['mechanicalWacc'])*10000
(P/'rates_results.json').write_text(json.dumps(x,indent=2)+'\n');print(x['mechanicalWacc'],x['syyCushionBasisPoints'])
