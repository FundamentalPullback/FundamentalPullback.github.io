"""Finite reserve/contract diagnostics. No current whole-company NAV or invented annual engineering schedule."""
import pathlib,json,csv
p=pathlib.Path(__file__).parent
res={'oil_mmbbl':479.210,'ngl_mmbbl':295.400,'gas_bcf':2050.131,'developed_mmboe':794.095,'pud_mmboe':322.203,'total_mmboe':1116.298,'future_dev_usdm':4253.827,'future_production_usdm':18026.302,'future_income_tax_usdm':1787.484,'future_inflows_usdm':38611.475,'future_net_cash_usdm':14543.862,'standardized_measure_usdm':8365.503,'pretax_pv10_usdm':9439.319}
assert abs(res['future_inflows_usdm']-res['future_dev_usdm']-res['future_production_usdm']-res['future_income_tax_usdm']-res['future_net_cash_usdm'])<1e-6
cases={'adverso':(65,18,.5,1.20),'central':(85,24,1.5,1.10),'favorable':(100,30,3,1.00)};out={}
# Reprice only disclosed year-end stock at unchanged reserve quantities; no discount factor invented.
for name,(oil,ngl,gas,cost) in cases.items():
 inflow=res['future_inflows_usdm']+res['oil_mmbbl']*(oil-64.69)+res['ngl_mmbbl']*(ngl-20.58)+res['gas_bcf']*(gas-.748)
 pretax=inflow-cost*(res['future_dev_usdm']+res['future_production_usdm'])
 out[name]={'realized_oil_usd_bbl':oil,'ngl_usd_bbl':ngl,'gas_usd_mcf':gas,'cost_multiplier':cost,'undiscounted_inflow_on_2025_stock':inflow,'undiscounted_pretax_project_surplus':pretax,'not_a_nav':True,'current_fair_value':None}
contracts=[]
for y,vols,prices in [(2027,[2.70,2.73,2.76,2.76],[79.86,76.81,74.66,73.10]),(2028,[.91,.91,.92,.92],[74.91,73.33,71.98,70.86])]:
 for name,(wti,_,__,___) in cases.items():
  for q,(v,k) in enumerate(zip(vols,prices),1):
   contingent=(18.75 if wti>80 else 9.375 if wti>70 else 0) if y==2027 else (12.5 if wti>80 else 6.25 if wti>70 else 0)
   contracts.append({'case':name,'year':y,'quarter':q,'wti_reference_scenario':wti,'oil_swap_mmbbl':v,'fixed_wti':k,'outright_wti_cash_usdm':v*(k-wti),'ridge_runner_earnout_usdm':contingent,'basis_roll_gas_contracts':'Excluded from this component diagnostic; not assumed zero.'})
w=csv.DictWriter((p/'contract_scenarios.csv').open('w'),fieldnames=contracts[0]);w.writeheader();w.writerows(contracts)
results={'scope':'Undiscounted fixed-reserve sensitivity of December31 2025 engineering perimeter plus standalone future oil swap/earnout component. Not current NAV, no whole-company price inverse.','reserves':res,'cases':out,'contracts_totals':{c:{'oil_swap_cash':sum(r['outright_wti_cash_usdm'] for r in contracts if r['case']==c),'earnout':sum(r['ridge_runner_earnout_usdm'] for r in contracts if r['case']==c)} for c in cases},'approved_value':None,'approved_entry':None,'current_corporate_nav':None,'unvalued_assets':['Post2025 additions and Ridge Runner','Unproved locations/royalty acreage beyond booked reserves'],'unresolved':['Production/ad valorem taxes are within aggregate costs but not repriced separately; price elasticity and economic-limit revisions unmodeled','Annual remaining reserve development/decline and price-dependent economic limits','Updated acquisition allocation and postclosing net debt','Gas/basis/roll scenario reference curves and contract valuation','Corporate taxes/NOLs/leases/environmental claims without double counting']}
(p/'results.json').write_text(json.dumps(results,indent=2));print(json.dumps(results,indent=2))
