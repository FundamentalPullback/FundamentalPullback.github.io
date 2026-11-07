import json,math,csv
from pathlib import Path
P=Path(__file__).parent
# USD millions. Reported rows transcribed from continuing-operation statements.
cols=['revenue','ebit','net_cont','cfo','capex','da','sbc']
a={
'FY2023':[7684.476,1219.340,943.864,1219.546,183.406,305.046,30.766],
'FY2024':[7745.909,1206.355,1399.968,1087.833,167.533,337.842,40.359],
'FY2025':[8092.571,1373.361,1097.429,1338.005,220.263,379.577,43.981],
'9M2024':[5816.043,911.291,1161.585,648.881,113.626,251.179,32.297],
'9M2025':[5993.492,1028.059,822.663,794.059,163.274,280.262,37.605],
'9M2026':[6477.483,1116.884,888.114,865.931,163.005,292.203,33.412],
'Q12026':[2053.623,305.909,238.749,190.997,59.808,97.421,20.960],
'H12026':[4243.644,697.696,551.294,427.168,107.591,194.233,27.759]}
def comb(*terms):return [sum(a[k][i]*m for k,m in terms) for i in range(len(cols))]
a['Q42025']=comb(('FY2025',1),('9M2025',-1));a['Q22026']=comb(('H12026',1),('Q12026',-1));a['Q32026']=comb(('9M2026',1),('H12026',-1));a['TTM2025']=comb(('FY2024',1),('9M2024',-1),('9M2025',1));a['TTM2026']=comb(('FY2025',1),('9M2025',-1),('9M2026',1))
actuals={k:dict(zip(cols,v)) for k,v in a.items()}
for k,v in actuals.items():v.update(fcf=v['cfo']-v['capex'],margin=v['ebit']/v['revenue'])
price=203.85;shares=133.007687+.8
bridge={'debt_carrying':3264.590,'debt_discount_and_costs':15.1,'finance_leases_FY25_proxy':9.649,'net_nonUS_pension_and_other_benefit_funded_status_FY25_proxy':74.536,'operating_cash_reserve_assumption':300,'cash':-1693.175}
deduction=sum(bridge.values())
scenarios={
'adverse':{'growth':[0,.01,.02,.025,.025], 'm1':.155,'m5':.17,'wacc':.11,'g':.02,'roic':.12,'capex':.032},
'central':{'growth':[.05,.05,.045,.04,.035], 'm1':.175,'m5':.19,'wacc':.10,'g':.025,'roic':.15,'capex':.03},
'favorable':{'growth':[.075,.07,.065,.06,.05], 'm1':.185,'m5':.215,'wacc':.09,'g':.03,'roic':.20,'capex':.032}}
baseline=8092.571*1.075;tax=.23;dep=.021;nwc=.20
# Terminal tax/margin stay consistent. Amortization and SBC remain expenses in EBIT.
def value(s):
 r=baseline;oldnop=r*.17*(1-tax);rows=[]
 for y in range(1,11):
  gr=s['growth'][y-1] if y<=5 else s['growth'][-1]+(s['g']-s['growth'][-1])*(y-5)/5
  m=s['m1']+(s['m5']-s['m1'])*min(y-1,4)/4
  nr=r*(1+gr);nop=nr*m*(1-tax);physical=nr*(s['capex']-dep)+(nr-r)*nwc;economic=max(0,nop-oldnop)/s['roic'];reinv=max(physical,economic);fcff=nop-reinv
  rows.append(dict(year=y,revenue=nr,margin=m,nopat=nop,physical_and_nwc=physical,economic_growth_reinvestment=economic,reinvestment=reinv,fcff=fcff,pv=fcff/(1+s['wacc'])**y));r=nr;oldnop=nop
 nr=r*(1+s['g']);nop=nr*s['m5']*(1-tax);physical=nr*(s['capex']-dep)+(nr-r)*nwc;economic=nop*s['g']/s['roic'];rein=max(physical,economic);term=(nop-rein)/(s['wacc']-s['g']);pvt=term/(1+s['wacc'])**10;ev=sum(q['pv'] for q in rows)+pvt
 return {'value':(ev-deduction)/shares,'ev':ev,'terminal_weight':pvt/ev,'terminal':{'revenue':nr,'nopat':nop,'physical_and_nwc':physical,'economic':economic,'reinvestment':rein},'years':rows}
out={k:value(v) for k,v in scenarios.items()}
sens=[{'wacc':w,'g':g,'value':value(dict(scenarios['central'],wacc=w,g=g))['value']} for w in [.09,.095,.10,.105,.11] for g in [.02,.025,.03]]
# Reverse solve a parallel shift of the first-five-year growth path, fade to same g.
lo,hi=-.05,.30
initial_bracket=[lo,hi]
inverse_grid=[value(dict(scenarios['central'],growth=[x+shift for x in scenarios['central']['growth']]))['value'] for shift in [lo+(hi-lo)*j/700 for j in range(701)]]
assert inverse_grid[0]<price<inverse_grid[-1]
assert all(y>x for x,y in zip(inverse_grid,inverse_grid[1:]))
for _ in range(90):
 z=(lo+hi)/2;s=dict(scenarios['central'],growth=[x+z for x in scenarios['central']['growth']]);v=value(s)['value']
 if v<price:lo=z
 else:hi=z
inverse={'additional_growth_each_first_five_years':z,'growth_path':[x+z for x in scenarios['central']['growth']],'value':v,'warning':'Conditional on fixed margins, WACC, reinvestment and September bridge; not a forecast.'}
qa={'four_quarters_tie_ttm':all(abs(sum(actuals[q][c] for q in ['Q42025','Q12026','Q22026','Q32026'])-actuals['TTM2026'][c])<1e-7 for c in cols),'all_terminal_wacc_above_g':all(s['wacc']>s['g'] for s in scenarios.values()),'all_terminal_reinvestment_funded':all(o['terminal']['reinvestment']>=max(o['terminal']['physical_and_nwc'],o['terminal']['economic']) for o in out.values()),'case_values_ordered':out['adverse']['value']<out['central']['value']<out['favorable']['value'],'no_certified_entry':True,'status':'screen-grade','stage3Complete':False,'entryApproved':False,'approvedValuation':None,'inverse_bracket_values':[inverse_grid[0],inverse_grid[-1]],'inverse_grid_strictly_increasing':all(y>x for x,y in zip(inverse_grid,inverse_grid[1:])),'inverse_residual':abs(v-price),'inverse_residual_pass':abs(v-price)<1e-8,'sensitivity_monotonic_wacc':all(value(dict(scenarios['central'],wacc=w1,g=g))['value']>value(dict(scenarios['central'],wacc=w2,g=g))['value'] for w1,w2 in zip([.09,.095,.10,.105],[.095,.10,.105,.11]) for g in [.02,.025,.03]),'sensitivity_monotonic_terminal_growth':all(value(dict(scenarios['central'],wacc=w,g=g1))['value']<value(dict(scenarios['central'],wacc=w,g=g2))['value'] for w in [.09,.095,.10,.105,.11] for g1,g2 in [(.02,.025),(.025,.03)]),'hard_failures':[],'limitations':['Unreconciled November financing and tender settlement cash bridge','Spot award dilution estimated','Maintenance capex/software split and full-cycle retained perimeter not independently established','No numerical current peer multiple panel']}
inputs={'price':price,'price_date':'2026-11-06','price_source':'https://www.dovercorporation.com/investors','actuals':actuals,'bridge':bridge,'bridge_total':deduction,'shares':shares,'baseline_revenue':baseline,'tax':tax,'depreciation_ratio':dep,'nwc_increment_ratio':nwc,'scenarios':scenarios,'classification':{'historical':'reported or arithmetic-derived; see report source mapping','forecast':'analyst_estimate','baseline':'derived FY2025 revenue times guidance midpoint','bridge':'September 2026 snapshot plus labeled annual proxies and assumptions'}}
for n,d in [('inputs.json',inputs),('results.json',{'cases':out,'sensitivity':sens,'inverse':inverse}),('qa.json',qa)]: (P/n).write_text(json.dumps(d,indent=2))
with (P/'actuals.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=['period']+list(next(iter(actuals.values())).keys()));w.writeheader();w.writerows(dict(period=k,**v) for k,v in actuals.items())
assert all(qa[k] for k in ['four_quarters_tie_ttm','all_terminal_wacc_above_g','all_terminal_reinvestment_funded','case_values_ordered','inverse_grid_strictly_increasing','inverse_residual_pass','sensitivity_monotonic_wacc','sensitivity_monotonic_terminal_growth'])
print(json.dumps({'values':{k:round(v['value'],2) for k,v in out.items()},'bridge':deduction,'inverse':inverse,'growth':{c:actuals['TTM2026'][c]/actuals['TTM2025'][c]-1 for c in ['revenue','ebit','fcf']},'qa':qa},indent=2))
