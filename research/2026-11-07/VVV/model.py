import json,csv,copy,math,pathlib
D=pathlib.Path(__file__).parent
sources={
'FY25':'https://www.sec.gov/Archives/edgar/data/1674910/000167491025000135/vvv-20250930.htm',
'Q326':'https://www.sec.gov/Archives/edgar/data/1674910/000167491026000066/vvv-20260630.htm',
'Q226':'https://www.sec.gov/Archives/edgar/data/1674910/000167491026000045/vvv-20260331.htm',
'Q126':'https://investors.valvoline.com/news/news-details/2026/Valvoline-Inc--Reports-First-Quarter-Results/default.aspx',
'Q325':'https://www.sec.gov/Archives/edgar/data/1674910/000167491025000119/vvv-20250630.htm',
'REFI':'https://www.sec.gov/Archives/edgar/data/1674910/000162828026058633/vvv-20260824.htm',
'H15':'https://www.federalreserve.gov/releases/H15/Current/',
'BETA':'https://stockanalysis.com/stocks/vvv/statistics/'}
# Millions USD, except ratios/EPS/shares millions. Preserve reported economics; no annualization of quarters.
fields=['revenue','ebit','continuing_income','da','cfo_cont','capex_cash','sbc','net_sale_loss']
raw={
'FY2023':[1443.5,247.2,199.4,88.8,353,180.5,12.2,0],
'FY2024':[1619,367.2,214.5,105.9,282.9,224.4,12,-41.8],
'FY2025':[1710.3,389.9,214.8,119.4,307.1,259.2,10.5,-71.1],
'9M2024':[1183.5,232.6,125.4,77.1,170,153,9.4,0],
'9M2025':[1256.5,305.4,189.2,86.6,180,160.3,7.4,-71.6],
'9M2026':[1510.2,216.5,78.1,109.3,284.6,172.3,9.3,43.6],
'6M2026':[965.6,104.3,13.1,71.1,160.2,115.2,5.9,43.6],
'Q12026':[461.8,18.3,-32.2,33.5,64.8,57.4,2.4,43.1]}
h={k:dict(zip(fields,v)) for k,v in raw.items()}
for name,plus,minus in [('Q42025','FY2025','9M2025'),('Q22026','6M2026','Q12026'),('Q32026','9M2026','6M2026')]:h[name]={f:h[plus][f]-h[minus][f] for f in fields}
for name,fy,now,old in [('TTM2026','FY2025','9M2026','9M2025'),('TTM2025','FY2024','9M2025','9M2024')]:h[name]={f:h[fy][f]+h[now][f]-h[old][f] for f in fields}
for k,v in h.items():
 v['fcf_cont_reported']=v['cfo_cont']-v['capex_cash'];v['ebit_margin']=v['ebit']/v['revenue'];v['ebit_ex_net_disposals']=v['ebit']+v['net_sale_loss'];v['net_cont_margin']=v['continuing_income']/v['revenue']
# Only 16.7 disclosed third-party Breeze transaction cost excluded additionally. IT, SBC and legacy expense remain in EBIT; no unproven legacy expense addback.
base_revenue=h['TTM2026']['revenue'];base_ebit=h['TTM2026']['ebit_ex_net_disposals']+16.7
bridge={'face_debt':1621.,'finance_lease_proxy':305.4,'pension_net_FY25':151.7,'legacy_tax_proxy':64.5,'cash_reported':84.2,'operating_cash_reserve':40.,'diluted_shares':128.4}
claims=bridge['face_debt']+bridge['finance_lease_proxy']+bridge['pension_net_FY25']+bridge['legacy_tax_proxy']-max(0,bridge['cash_reported']-bridge['operating_cash_reserve'])
params={'base_revenue':base_revenue,'base_normalized_ebit':base_ebit,'starting_company_stores':1232,'tax':.25,'da_sales':.072,'cloud_net_growth_sales':.0025,'nwc_incremental_sales':.04,'gross_closure_replacement_rate':.005,'all_in_opening_cost':2.5,'opening_cost_inflation':.02,'bridge':bridge,'claims':claims,'scanner_price':34.81,'scanner_date':'2026-11-06','risk_free':.0484,'risk_free_date':'2026-11-05','observed_beta':1.02,'erp_assumption':.055,'debt_rate_proxy':.06125}
cases={
'bear':{'growth':[.04,.03,.03,.03,.03,.025,.025,.025,.02,.02],'margins':[.175,.175,.175,.175,.18,.18,.18,.18,.18,.18],'units':[.02,.02,.02,.015,.015,.01,.01,.01,.005,.005],'roic':.12,'terminal_roic':.10,'terminal_units':.005,'wacc':.11,'g':.02},
'base':{'growth':[.08,.08,.07,.07,.06,.05,.05,.04,.04,.03],'margins':[.19,.195,.20,.205,.21,.21,.21,.21,.21,.21],'units':[.04,.04,.04,.035,.03,.025,.025,.02,.02,.01],'roic':.16,'terminal_roic':.14,'terminal_units':.005,'wacc':.0975,'g':.025},
'bull':{'growth':[.11,.10,.09,.08,.07,.06,.06,.05,.04,.035],'margins':[.20,.21,.215,.22,.225,.23,.23,.23,.23,.23],'units':[.05,.05,.045,.04,.035,.03,.03,.025,.02,.015],'roic':.20,'terminal_roic':.17,'terminal_units':.01,'wacc':.0875,'g':.03}}
def run(c,margin_shift=0,extra_growth=0,claims_delta=0,opening_cost=None):
 rev=base_revenue;nopat=base_ebit*(1-params['tax']);units=params['starting_company_stores'];rows=[];pv=0
 for i in range(10):
  nr=rev*(1+c['growth'][i]+extra_growth);m=c['margins'][i]+margin_shift;ebit=nr*m;nn=ebit*(1-params['tax']);da=nr*params['da_sales'];dnwc=max(0,nr-rev)*params['nwc_incremental_sales']
  gross=units*(c['units'][i]+params['gross_closure_replacement_rate']);cost=(opening_cost or params['all_in_opening_cost'])*(1+params['opening_cost_inflation'])**(i+1);growth_capex=gross*cost;maint=da
  cloud_net=nr*params['cloud_net_growth_sales'];physical=maint+growth_capex+cloud_net-da+dnwc;economic=max(0,nn-nopat)/c['roic'];reinvest=max(physical,economic);fcff=nn-reinvest;disc=fcff/(1+c['wacc'])**(i+1);pv+=disc
  rows.append(dict(year=i+1,revenue=nr,margin=m,ebit=ebit,tax=ebit*params['tax'],nopat=nn,delta_nopat=nn-nopat,da=da,maintenance_floor=maint,gross_openings=gross,net_company_stores=units*(1+c['units'][i]),growth_capex=growth_capex,cloud_net_investment=cloud_net,delta_nwc=dnwc,physical_reinvestment=physical,economic_reinvestment=economic,reinvestment=reinvest,fcff=fcff,pv=disc,binding='physical' if physical>=economic else 'ROIC'))
  rev=nr;nopat=nn;units*=1+c['units'][i]
 tr=rev*(1+c['g']);tn=nopat*(1+c['g']);tda=tr*params['da_sales'];tgross=units*(c['terminal_units']+params['gross_closure_replacement_rate']);tcost=(opening_cost or params['all_in_opening_cost'])*(1+params['opening_cost_inflation'])**11
 tecon=(tn-nopat)/c['terminal_roic'];tphysical=tgross*tcost+tr*params['cloud_net_growth_sales']+(tr-rev)*params['nwc_incremental_sales'];treinv=max(tecon,tphysical);tfcf=tn-treinv;tv=tfcf/(c['wacc']-c['g']);pvtv=tv/(1+c['wacc'])**10;ev=pv+pvtv;eq=ev-claims-claims_delta
 return {'value':max(0,eq)/bridge['diluted_shares'],'raw_equity':eq,'ev':ev,'pv_explicit':pv,'pv_terminal':pvtv,'terminal_share':pvtv/ev,'terminal':{'revenue':tr,'nopat':tn,'da':tda,'maintenance':tda,'gross_openings':tgross,'growth_capex':tgross*tcost,'cloud_net_investment':tr*params['cloud_net_growth_sales'],'delta_nwc':(tr-rev)*params['nwc_incremental_sales'],'steady_state_opening_cost_inflation':(1+c['g'])/(1+c['terminal_units'])-1,'physical_reinvestment':tphysical,'economic_reinvestment':tecon,'reinvestment':treinv,'fcff':tfcf},'rows':rows}
results={k:run(v) for k,v in cases.items()}
def solve(which,lo,hi):
 def price(x):return run(cases['base'],**{which:x})['value']
 if price(lo)>params['scanner_price'] or price(hi)<params['scanner_price']:return {'bracketed':False,'low_price':price(lo),'high_price':price(hi)}
 for _ in range(100):
  mid=(lo+hi)/2
  if price(mid)<params['scanner_price']:lo=mid
  else:hi=mid
 return {'bracketed':True,'shift':(lo+hi)/2,'value':price((lo+hi)/2)}
sens=[]
for w in [.0875,.0975,.1075,.1175]:
 for g in [.02,.025,.03]:
  c=copy.deepcopy(cases['base']);c.update(wacc=w,g=g);sens.append({'wacc':w,'g':g,'value':run(c)['value']})
# two inverse routes: margin shift with margin-driven reinvestment funded; revenue shift includes NWC and ROIC cost.
inverse={'margin_shift':solve('margin_shift',-.02,.15),'annual_growth_shift':solve('extra_growth',-.01,.15)}
roic_sensitivity=[]
for r in [.12,.16,.20,.25]:
 c=copy.deepcopy(cases['base']);c.update(roic=r);roic_sensitivity.append({'incremental_roic':r,'value':run(c)['value']})
closure_sensitivity=[]
oldclosure=params['gross_closure_replacement_rate']
params['gross_closure_replacement_rate']=0
for name,case in cases.items():closure_sensitivity.append({'case':name,'value':run(case)['value']})
params['gross_closure_replacement_rate']=oldclosure
outputs={'zero_closure_sensitivity':closure_sensitivity,'roic_sensitivity':roic_sensitivity,'cases':results,'sensitivity':sens,'inverse':inverse,'claim_plus50_value':run(cases['base'],claims_delta=50)['value'],'claim_minus50_value':run(cases['base'],claims_delta=-50)['value'],'opening_cost3_value':run(cases['base'],opening_cost=3)['value'],'opening_cost2_value':run(cases['base'],opening_cost=2)['value']}
cap=34.81*128.4;dw=(1621+305.4)/(cap+1621+305.4);ke=.0484+1.02*.055;params['capm_wacc_before_judgment']=ke*(1-dw)+.06125*.75*dw
(D/'model_inputs.json').write_text(json.dumps({'parameters':params,'cases':cases,'sources':sources,'basis':'conditional controlled support model; assumptions explicit, no automatic entry'},indent=2));(D/'model_results.json').write_text(json.dumps(outputs,indent=2));(D/'historicals.json').write_text(json.dumps(h,indent=2))
with (D/'historicals.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=['period']+list(next(iter(h.values())).keys()));w.writeheader();w.writerows({'period':k,**v} for k,v in h.items())
for k,r in results.items():
 with (D/('forecast_'+k+'.csv')).open('w') as f:
  w=csv.DictWriter(f,fieldnames=list(r['rows'][0]));w.writeheader();w.writerows(r['rows'])
checks=[]
def test(name,condition):
 assert condition,name;checks.append({'test':name,'passed':True})
test('TTM revenue',abs(base_revenue-1964)<1e-8);test('TTM EBIT',abs(h['TTM2026']['ebit']-301)<1e-8);test('Normalized EBIT',abs(base_ebit-361.8)<1e-8)
for f in fields:test('four quarters sum '+f,abs(sum(h[q][f] for q in ['Q42025','Q12026','Q22026','Q32026'])-h['TTM2026'][f])<1e-8)
for name,r in results.items():
 for row in r['rows']:
  test(name+' year'+str(row['year'])+' reinvestment funds both floors',row['reinvestment']+1e-9>=max(row['physical_reinvestment'],row['economic_reinvestment']))
  test(name+' year'+str(row['year'])+' FCFF identity',abs(row['fcff']-(row['nopat']+row['da']-(row['da']+row['reinvestment']-row['delta_nwc'])-row['delta_nwc']))<1e-8)
 test(name+' terminal opening cost grows with revenue',abs((1+cases[name]['terminal_units'])*(1+r['terminal']['steady_state_opening_cost_inflation'])-(1+cases[name]['g']))<1e-10)
 test(name+' terminal funded',r['terminal']['reinvestment']>=max(r['terminal']['physical_reinvestment'],r['terminal']['economic_reinvestment']))
 test(name+' bridge',abs(r['value']-max(0,r['ev']-claims)/bridge['diluted_shares'])<1e-8)
test('scenario order',results['bear']['value']<results['base']['value']<results['bull']['value'])
inverse_checks={}
for route,lo,hi in [('margin_shift',-.02,.15),('extra_growth',-.01,.15)]:
 grid=[run(cases['base'],**{route:lo+(hi-lo)*i/1000})['value'] for i in range(1001)]
 key='margin_shift' if route=='margin_shift' else 'annual_growth_shift'
 monotonic=all(b+1e-10>=a for a,b in zip(grid,grid[1:]))
 bracket=grid[0]<=params['scanner_price']<=grid[-1]
 test(route+' inverse grid monotonic',monotonic)
 test(route+' inverse bracket agrees',bracket==inverse[key]['bracketed'])
 residual=None
 if bracket:
  residual=run(cases['base'],**{route:inverse[key]['shift']})['value']-params['scanner_price']
  test(route+' inverse solved residual',abs(residual)<1e-8)
 inverse_checks[key]={'grid_points':1001,'lower_shift':lo,'upper_shift':hi,'lower_value':grid[0],'upper_value':grid[-1],'monotonic_nondecreasing':monotonic,'bracketed':bracket,'solved_residual':residual,'interpretation':'No solution in tested margin range' if not bracket else 'Funded revenue-productivity shift, not additional store count'}
(D/'model_qa.json').write_text(json.dumps({'status':'screen-grade conditional; bridge proxies and funded driver assumptions require review','checks':checks,'inverse_checks':inverse_checks},indent=2))
print(json.dumps({'values':{k:v['value'] for k,v in results.items()},'inverse':inverse,'bridge_claims':claims,'CAPM':params['capm_wacc_before_judgment'],'checks':len(checks)},indent=2))
