"""PFGC: reproducible conditional FCFF and reported-history schedules. USD millions.
No external packages. Scenario assumptions are not guidance or a certified target.
"""
import json,math,csv
from pathlib import Path
P=Path(__file__).resolve().parent
# q1 FY25 through q1 FY27; Q4 CFO/capex from FY minus nine-month cash statements.
keys=['sales','ebit','net_income','eps_gaap','eps_adjusted_issuer','cfo','cash_capex','da','sbc','interest']
rows=[
['Q1 FY25',15415.5,215.3,108,.69,1.16,53.5,96.5,152.9,11.3,66.8],
['Q2 FY25',15638.2,158.8,42.4,.27,.98,325.5,107.4,182.5,11.7,100.2],
['Q3 FY25',15306.3,174.4,58.3,.37,.79,448.1,128.8,186.9,12.6,96.9],
['Q4 FY25',16938.9,267.8,131.5,.84,1.55,383,173.3,195.6,12.2,94.5],
['Q1 FY26',17075.9,224.7,93.6,.60,1.18,-145.2,78.9,195.4,13,104.4],
['Q2 FY26',16444.7,190.1,61.7,.39,.98,601.2,113.4,199.9,12.6,104.5],
['Q3 FY26',16290,148.9,41.7,.27,.80,615.9,73.6,205,12.9,102.9],
['Q4 FY26',18028.9,323.8,162.3,1.03,1.59,341.8,118.2,213.6,13,101.9],
['Q1 FY27',18018.4,272.2,129.5,.82,1.32,-89.3,53.9,210.7,13.2,98.4]]
h=[dict(period=r[0],**dict(zip(keys,r[1:]))) for r in rows]
for r in h:r['fcf_reported']=round(r['cfo']-r['cash_capex'],2)
annual=[dict(period='FY24',sales=58281.2,ebit=826.4,net_income=435.9,eps_gaap=2.79,cfo=1163,cash_capex=395.6,da=556.7,sbc=41.9,finance_rou_additions=412.4),dict(period='FY25',sales=63298.9,ebit=816.3,net_income=340.2,eps_gaap=2.18,eps_adjusted_issuer=4.48,cfo=1210.1,cash_capex=506,da=717.9,sbc=47.8,finance_rou_additions=842),dict(period='FY26',sales=67839.5,ebit=887.5,net_income=359.3,eps_gaap=2.29,eps_adjusted_issuer=4.55,cfo=1413.7,cash_capex=384.1,da=813.9,sbc=51.5,finance_rou_additions=441.1)]
for r in annual:r['fcf_reported']=round(r['cfo']-r['cash_capex'],2)
ttms=[]
for label,rr,shares in [('TTM Sep25',h[1:5],156.575),('TTM Sep26',h[5:9],157.125)]:
 t={'period':label,**{k:round(sum(r[k] for r in rr),4) for k in keys if not k.startswith('eps')}}
 t.update(eps_gaap_derived=t['net_income']/shares,eps_adjusted_quarter_sum=sum(r['eps_adjusted_issuer'] for r in rr),weighted_diluted_shares=shares,fcf_reported=t['cfo']-t['cash_capex'])
 # Analytical reported-perimeter earnings, preserving SBC, LIFO, amortization and integration.
 t['eps_operating_after_interest_26pct_tax']=(t['ebit']-t['interest'])*.74/shares
 ttms.append(t)
# Debt face value rather than carrying amount; restricted cash excluded; operating leases remain expense.
bridge={'debt_face':5193.3,'finance_lease_liability':1779.1,'unrestricted_cash':35.9,'shares':159.0,'seller_consideration_latest_disclosed':23.4,'seller_consideration_date':'2026-06-27','seller_consideration_current_balance_verified':False,'reported_outstanding_20261028':157.784532,'reported_diluted_q1':157.5,'operating_leases_not_deducted':963.8}
netdebt=bridge['debt_face']+bridge['finance_lease_liability']-bridge['unrestricted_cash']+bridge['seller_consideration_latest_disclosed']
inputs={'riskfree':.0486,'erp':.0441,'observed_beta':.89,'cost_debt_assumed':.065,'tax':.26,'debt_weight_observed':(5193.3+1779.1)/(107.5*157.784532+5193.3+1779.1)}
inputs['cost_equity']=inputs['riskfree']+inputs['erp']*inputs['observed_beta']
inputs['mechanical_wacc']=inputs['cost_equity']*(1-inputs['debt_weight_observed'])+inputs['cost_debt_assumed']*.74*inputs['debt_weight_observed']
cases={'adverso':dict(growth=.025,m1=.014,m5=.0145,mt=.014,wacc=.09,g=.02,roic=.08,capex=.013,nwc=.05), 'central_condicional':dict(growth=.05,m1=.0155,m5=.019,mt=.018,wacc=.08,g=.025,roic=.11,capex=.012,nwc=.04),'favorable':dict(growth=.065,m1=.0165,m5=.022,mt=.021,wacc=.075,g=.0275,roic=.14,capex=.0118,nwc=.035)}
def calc(c):
 sales=ttms[1]['sales']; startmargin=ttms[1]['ebit']/sales; schedule=[];ev=0
 for y in range(1,11):
  growth=c['growth'] if y<=5 else c['growth']+(c['g']-c['growth'])*(y-5)/5
  prev=sales;sales*=1+growth
  margin=c['m1']+(c['m5']-c['m1'])*(y-1)/4 if y<=5 else c['m5']+(c['mt']-c['m5'])*(y-5)/5
  ebit=sales*margin;nopat=ebit*.74;da=sales*.012
  # Explicit investment funds both cash capex and financial-lease additions.
  raw_net=sales*c['capex']-da+(sales-prev)*c['nwc']
  fade=max(0,(y-5)/5)
  net=raw_net*(1-fade)+(nopat*c['g']/c['roic'])*fade
  capex=net+da-(sales-prev)*c['nwc']
  # Sourced accounting proxy, not a certified physical maintenance estimate.
  physical_floor=sales*541.9/67839.5
  intangible_reserve=sales*9.6/67839.5
  capex=max(capex,physical_floor+intangible_reserve)
  net=capex-da+(sales-prev)*c['nwc'];fcff=nopat-net
  pv=fcff/(1+c['wacc'])**y;ev+=pv
  schedule.append(dict(year=y,sales=sales,ebit=ebit,nopat=nopat,da=da,total_cash_and_finance_capex=capex,physical_maintenance_proxy=physical_floor,intangible_purchase_reserve=intangible_reserve,physical_investment_budget=capex-intangible_reserve,delta_nwc=(sales-prev)*c['nwc'],net_reinvestment=net,fcff=fcff,pv=pv))
 tn=schedule[-1]['nopat']*(1+c['g']);tfcff=tn*(1-c['g']/c['roic']);tv=tfcff/(c['wacc']-c['g']);pvtv=tv/(1+c['wacc'])**10;ev+=pvtv
 return {'assumptions':c,'schedule':schedule,'terminal_nopat':tn,'terminal_reinvestment':tn*c['g']/c['roic'],'terminal_fcff':tfcff,'pv_terminal':pvtv,'terminal_share_ev':pvtv/ev,'ev':ev,'equity':ev-netdebt,'value_per_share':(ev-netdebt)/bridge['shares'],'gap_vs_close':((ev-netdebt)/bridge['shares'])/107.5-1}
res={k:calc(v) for k,v in cases.items()}
sens=[dict(wacc=w,g=g,value=calc({**cases['central_condicional'],'wacc':w,'g':g})['value_per_share']) for w in [.07,.075,.08,.085,.09] for g in [.02,.025,.03]]
lo,hi=.01,.04
for _ in range(80):
 mid=(lo+hi)/2;r=calc({**cases['central_condicional'],'m5':mid,'mt':mid})
 if r['value_per_share']<107.5:lo=mid
 else:hi=mid
reverse={'flat_margin_year5_to_terminal_required_for_107_5':(lo+hi)/2,'other_assumptions':'central; initial margin fixed at 1.55%; identical funded transition'}
# CFO conversion diagnostic. Tax normalisation substitutes NOPAT for NI, so no extra tax addback.
bridge_cash={'fy26_reported_fcf':1029.6,'finance_asset_additions':441.1,'intangible_purchases':9.6,'sbc_charge':51.5,'cash_tax_paid':8.5,'income_tax_expense':126.5,'cfo_normalized_tax_increment':118.0,'after_finance_investment_sbc_intangibles_and_tax':1029.6-441.1-9.6-51.5-118.0,'not_fcff':'Residual remains after interest; NWC/tax timing are not steady-state. Do not capitalize.'}
alternative=calc({**cases['favorable'],'wacc':.07})
stress=calc({**cases['central_condicional'],'wacc':.09,'growth':.04,'m5':.017,'mt':.016})
out=dict(alternative_favorable_lower_wacc=alternative,integrated_stress=stress,status='conditional-screen-grade-not-investment-approved',valuation_certified=False,history=h,annual=annual,paired_ttm=ttms,capital_bridge=bridge,discount=inputs,cases=res,sensitivity=sens,reverse=reverse,cash_diagnostic=bridge_cash)
(P/'model_results.json').write_text(json.dumps(out,indent=2))
(P/'history.json').write_text(json.dumps({'quarters':h,'annual':annual,'paired_ttm':ttms},indent=2))
with (P/'history.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=list(h[0]));w.writeheader();w.writerows(h)
checks={'four_quarters_sales_tie_FY26':abs(sum(x['sales'] for x in h[4:8])-annual[2]['sales'])<.01,'cash_tie_FY26':abs(sum(x['cfo'] for x in h[4:8])-annual[2]['cfo'])<.01,'terminal_funded':all(r['terminal_reinvestment']>0 for r in res.values()),'physical_proxy_floor_funded':all(y['physical_investment_budget']+1e-9>=y['physical_maintenance_proxy'] for r in res.values() for y in r['schedule']),'fcff_identity_no_second_principal_or_sbc_addback':all(abs(y['fcff']-(y['nopat']+y['da']-y['total_cash_and_finance_capex']-y['delta_nwc']))<1e-7 for r in res.values() for y in r['schedule']),'seller_obligation_in_equity_bridge':abs(netdebt-6959.9)<1e-8}
assert all(checks.values());(P/'run_log.json').write_text(json.dumps({'checks':checks,'warnings':['Seller consideration23.4m is June27 latest disclosed, not verified Sep26 balance; Q1 acquisition payments not attributed reliably','Physical maintenance floor is depreciation proxy; not engineering proof of fleet replacement','No homogeneous current-perimeter EPS/FCF paired TTM established','Current market debt yield not directly observed; cost debt 6.5% assumption','Cash-flow normalization sensitive to tax and procurement timing','Share count 159m conditional dilution allowance, not treasury-stock method audit']},indent=2))
print(json.dumps({k:round(v['value_per_share'],2) for k,v in res.items()}));print(inputs);print(reverse);print(ttms)
