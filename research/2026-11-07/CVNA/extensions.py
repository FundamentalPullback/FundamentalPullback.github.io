"""Extensiones reproducibles: fuentes obtenidas; no aprueban valoración."""
import json,pathlib
from model import calc,CASES,SALES,IC0,SHARES
P=pathlib.Path(__file__).parent
rf=.0484;erp=.0441;kd=.065;tax=.25;dw=.10
betas={'sector_relevered':.71*(1+(1-tax)*dw/(1-dw)),'analyst_normalized_unvalidated':1.25,'observed_5y_monthly':3.65}
waccs={k:(rf+b*erp)*(1-dw)+kd*(1-tax)*dw for k,b in betas.items()}
rate_cases={k:{'beta':betas[k],'wacc':w,'base_value':calc({**CASES['base'],'wacc':w})['value']} for k,w in waccs.items()}
# Conditional scheduled claims, not a prediction of tax realization.
claims={}
for years in [5,10,15]:
 ann=sum(1/(1+.095)**t for t in range(1,years+1))/years
 claims[str(years)]={'PV_DTA':2905*ann,'PV_TRA':2230*ann,'value':calc(CASES['base'],tra=2230*ann,dta=2905*ann)['value']}
# Cyclical stress permits losses; no cash-tax rebate on negative EBIT.
sales=SALES;ic=IC0;pv=0;rows=[]
gs=[-.15,-.05,.05,.10,.10,.08,.06,.04,.03,.025]
ms=[-.05,-.02,.02,.05,.07,.08,.08,.08,.08,.08]
for y,(g,m) in enumerate(zip(gs,ms),1):
 old=sales;sales*=1+g;nopat=sales*m*(.75 if m>0 else 1)
 da=.01*sales;capex=.018*sales;acq=.002*sales;wc=.16*(sales-old);reinv=capex+acq-da+wc;ic+=reinv;fcff=nopat-reinv;pv+=fcff/1.095**y
 rows.append(dict(year=y,revenue=sales,margin=m,nopat=nopat,capex_including_financed=capex,da=da,acquisitions=acq,delta_working_capital=wc,fcff=fcff,capital_end=ic))
tfcff=nopat*1.025-ic*.025;tv=tfcff/(.095-.025)/1.095**10;ev=pv+tv;v=(ev+2049-5161-100-2230)/SHARES
out={'status':'conditional_not_approved','rates':{'rf':rf,'rf_observation_date':'2026-11-05','rf_source':'Fed H15 release 2026-11-06','erp':erp,'erp_date':'2026-11-01','erp_source':'Damodaran adjusted payout TTM; source itself uses Treasury 5.29%, not same date as rf','debt_cost_assumption':kd,'debt_cost_support':'Term Loan B contractual SOFR+225bp, issue price99.75; SOFR overnight not interchangeable with Term SOFR','target_debt_weight_assumption':dw,'cases':rate_cases},'tax_timing_only_same_schedule':claims,'cycle_stress':{'value':v,'rows':rows,'caveat':'Not worst case. Does not model loss of loan buyers, forced recapitalization, insolvency or liquidation. Negative free cash can require financing. Historical2022 exgoodwill operating margin was worse.'}}
(P/'extension_results.json').write_text(json.dumps(out,indent=2));print(json.dumps({'rates':rate_cases,'tax':claims,'cycle_stress_value':v},indent=2))
