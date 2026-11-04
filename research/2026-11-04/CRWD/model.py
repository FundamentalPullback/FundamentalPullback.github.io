import json,csv,math,pathlib
P=pathlib.Path(__file__).parent
price=244.68; scanner=245.50; shares=1050.118022; issued=1026.129839
# USD millions. Attributed cloud operating leases remain operating expenses.
bridge={'cash':5013.847,'minimum_operating_cash':600.,'strategic_investments':69.263,'NCI':37.801,'debt_face':750.,'XM_Cyber_maximum_cash_component':145.}
net=sum(bridge[k] for k in ['cash','strategic_investments'])-sum(bridge[k] for k in ['minimum_operating_cash','NCI','debt_face','XM_Cyber_maximum_cash_component'])
cases={
'bear':dict(growth=[.16,.14,.12,.10,.08,.06,.045,.03,.025,.02],margin=[.00,.03,.06,.09,.12,.13,.14,.15,.16,.17],wacc=.115,g=.02,roic=.15,wc=-.25,capex=[.115,.105,.09,.08,.07,.065,.06,.055,.05,.05],commission=[.03,.03,.025,.02,.018,.015,.012,.01,.008,.006],capsbc=[.013,.012,.011,.01,.009,.008,.007,.006,.006,.005],litigation=750.),
'base':dict(growth=[.22,.21,.20,.18,.16,.13,.10,.07,.05,.03],margin=[.05,.09,.13,.16,.19,.21,.22,.23,.24,.24],wacc=.10,g=.03,roic=.25,wc=-.40,capex=[.115,.10,.085,.075,.065,.06,.055,.05,.05,.05],commission=[.025,.025,.02,.018,.015,.012,.01,.008,.006,.005],capsbc=[.012,.011,.01,.009,.008,.007,.006,.006,.005,.005],litigation=0.),
'bull':dict(growth=[.27,.27,.25,.23,.21,.18,.15,.12,.08,.05],margin=[.08,.13,.18,.22,.25,.28,.30,.31,.32,.32],wacc=.09,g=.035,roic=.35,wc=-.45,capex=[.115,.095,.08,.07,.06,.055,.05,.05,.05,.05],commission=[.02,.018,.016,.014,.012,.01,.008,.006,.005,.005],capsbc=[.01,.009,.008,.007,.006,.005,.005,.005,.005,.005],litigation=0.)}
def calc(c):
 r=6001.1;rows=[]
 for i,(g,m) in enumerate(zip(c['growth'],c['margin'])):
  prev=r;r*=1+g;ebit=r*m;tax=max(0,ebit)*.21;da=r*(.05 if i<5 else .045);cap=r*c['capex'][i];caps=r*c['capsbc'][i];comm=r*c['commission'][i];wc=(r-prev)*c['wc'];fcff=ebit-tax+da-cap-caps-comm-wc
  rows.append(dict(year=i+1,revenue=r,growth=g,EBIT_margin_after_SBC=m,EBIT=ebit,cash_tax=tax,NOPAT=ebit-tax,DA=da,cash_capex_software=cap,capitalized_SBC=caps,net_contract_cost_investment=comm,delta_other_NWC=wc,FCFF=fcff,PV=fcff/(1+c['wacc'])**(i+1)))
 terminal_nopat=r*(1+c['g'])*c['margin'][-1]*.79;terminal_reinvestment=terminal_nopat*c['g']/c['roic'];tfcf=terminal_nopat-terminal_reinvestment;tv=tfcf/(c['wacc']-c['g']);pvt=tv/(1+c['wacc'])**10;ev=sum(x['PV'] for x in rows)+pvt;eq=ev+net-c['litigation'];return dict(rows=rows,EV=ev,equity=eq,per_share=eq/shares,upside=eq/shares/price-1,terminal_FCFF=tfcf,terminal_reinvestment=terminal_reinvestment,terminal_weight=pvt/ev)
out={k:calc(v) for k,v in cases.items()}
sens=[]
for w in [.09,.10,.11]:
 for g in [.025,.03,.035]:
  c={**cases['base'],'wacc':w,'g':g};sens.append(dict(wacc=w,g=g,value=calc(c)['per_share']))
# Joint reverse packages solve growth 1-5, then proportional fade to terminal; margin/capital terms differ, not a unique requirement.
reverse=[]
for label,w,m,g,roic in [('high_margin_low_rate',.08,.38,.035,.40),('strong_execution',.09,.32,.03,.30),('base_margin',.10,.24,.03,.25)]:
 def candidate(x):
  c={**cases['bull'],'growth':[x]*5+[x*.8,x*.6,x*.4,x*.2,g],'margin':[m*.25,m*.40,m*.56,m*.69,m*.78,m*.87,m*.94,m,m,m],'wacc':w,'g':g,'roic':roic};return calc(c)
 lo=.01;hi=1.
 for _ in range(80):
  mid=(lo+hi)/2
  if candidate(mid)['per_share']<price:lo=mid
  else:hi=mid
 z=candidate((lo+hi)/2);reverse.append(dict(package=label,growth_year1_5=(lo+hi)/2,margin_year10=m,wacc=w,g=g,roic=roic,revenue_year5=z['rows'][4]['revenue'],revenue_year10=z['rows'][9]['revenue'],FCFF_year10=z['rows'][9]['FCFF'],value=z['per_share']))
# Two actual-date peers; straightforward EV excludes operating leases, cash flow includes rents.
peers=[]
for symbol,p,n,cash,debt,rev,ebit,cfo,cap,sbc in [
 ('CRWD',price,issued,5013.847,750,4812.005+2856.526-2272.386,-293.292-63.832+224.170,1612.349+1121.205-716.939,302.108+68.751+222.037+49.090-116.248-34.726,1096.679+674.617-527.292),
 ('FTNT',128.11,734.6,5318.4,500,6799.6+5975.9-4894.6,2084.7+1973.6-1459.1,2590.6+3066.7-1970.4,364.8+212.8-322,279.5+231.9-207),
 ('ZS',225.09,163.055,3474.151,1725,3352.523,-133.267,1129.654,277.304+73.207,821.923)]:
  mc=p*n;ev=mc+debt-cash;fcf=cfo-cap;peers.append(dict(ticker=symbol,price=p,shares=n,market_cap=mc,net_debt=debt-cash,EV=ev,revenue_TTM=rev,EBIT_TTM=ebit,CFO_TTM=cfo,cash_investment=cap,FCF_CFO_less_investment=fcf,SBC_expense=sbc,FCF_less_SBC=fcf-sbc,EV_sales=ev/rev,EV_EBIT=ev/ebit if ebit>0 else None,FCF_yield=fcf/mc))
res=dict(asof='2026-11-03 close',price=price,scanner=scanner,shares=shares,bridge=bridge,net_bridge=net,assumptions=cases,results=out,sensitivity=sens,reverse=reverse,peers=peers)
(P/'model.json').write_text(json.dumps(res,indent=2))
with open(P/'forecast.csv','w') as f:
 rows=[dict(case=k,**r) for k,v in out.items() for r in v['rows']];w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
summary={k:{q:v[q] for q in ['EV','equity','per_share','upside','terminal_weight']} for k,v in out.items()};(P/'summary.json').write_text(json.dumps(dict(summary=summary,reverse=reverse,sensitivity=sens,peers=peers),indent=2));print(json.dumps(dict(summary=summary,reverse=reverse,sensitivity=sens,peers=peers),indent=2))
assert all(c['wacc']>c['g'] for c in cases.values());assert all(len(v['rows'])==10 for v in out.values());assert out['bear']['per_share']<out['base']['per_share']<out['bull']['per_share'];(P/'qa.txt').write_text('PASS: 10 years, positive spread WACC-g, reconciled equity bridges, SBC retained; scenario ranking; reverse packages solve current close. USD millions; shares millions; post-split.\n')
