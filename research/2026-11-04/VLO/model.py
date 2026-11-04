"""Conditional 10-year industrial FCFF model. USD millions, explicit cycle normalization.
Assumptions are not issuer guidance. Source history is separate. No orders or entry approval.
"""
import json,pathlib
P=pathlib.Path(__file__).parent
CAP={'cash':9840,'operating_cash_reserve_assumption':3000,'nominal_debt_ex_finance_leases':8635,'finance_leases_derived':2422,'nci_book_proxy':3110,'income_taxes_payable_current':1579,'benefits_fy2025_gross_proxy':472,'utb_fy2025_balance_proxy':441,'aro_fy2025_less_known_settlements_proxy':193,'environmental_fy2025_proxy':275,'foreign_repatriation_extra_stress':100}
BRIDGE=CAP['cash']-sum(v for k,v in CAP.items() if k!='cash')
SHARES=285.0 # Q3 diluted average; actual Oct23 278.8844m, sensitivity only.
CASES={'bear':{'unit':[9,6,4,3.5,3.5],'rd':[200,100,0,0,0],'ethanol':[300,250,200,200,200],'throughput':2.8,'corporate':1200,'tax':.26,'wacc':.115,'g':.01,'roic':.09},'base':{'unit':[14,10,8,6,6],'rd':[600,400,200,0,0],'ethanol':[500,400,350,300,300],'throughput':2.95,'corporate':1150,'tax':.24,'wacc':.105,'g':.02,'roic':.12},'bull':{'unit':[20,16,13,10,10],'rd':[1000,800,600,300,300],'ethanol':[700,600,500,400,400],'throughput':3.05,'corporate':1100,'tax':.23,'wacc':.095,'g':.025,'roic':.15}}
def calc(case='base',unit_delta=0,bridge=BRIDGE,shares=SHARES,wacc_delta=0,rd_terminal_delta=0,capex_delta=0,roic_override=None):
 a=CASES[case]; rows=[]; pv=0; prev_revenue=153327; terminal_g=a['g']; w=a['wacc']+wacc_delta; roic=a['roic'] if roic_override is None else roic_override
 for y in range(1,11):
  i=min(y-1,4);infl=(1+terminal_g)**max(0,y-5)
  unit=(a['unit'][i]+unit_delta)*infl;vol=a['throughput']*365
  refining=unit*vol;rd=(a['rd'][i]+(rd_terminal_delta if y>=4 else 0))*infl;eth=a['ethanol'][i]*infl;cost_infl=(1.02**min(y-1,4))*infl;corp=a['corporate']*cost_infl;ebit=refining+rd+eth-corp;nopat=ebit*(1-a['tax'])
  # Revenues are context for working-capital funding, not a prediction of commodity prices.
  rev=(130000 if y==1 else 120000*(1.02**min(y-2,3))*infl)*(a['throughput']/2.95)
  da=2800*cost_infl;cash_capital=(2600+capex_delta)*cost_infl;new_finance_assets=350*cost_infl;capex=cash_capital+new_finance_assets
  nwc=.05*max(0,rev-prev_revenue);explicit=capex-da+nwc;economic=max(0,nopat)*terminal_g/roic;reinvest=max(explicit,economic);reserve=reinvest-explicit;fcff=nopat+da-capex-nwc-reserve
  discounted=fcff/(1+w)**y;pv+=discounted;rows.append(dict(year=y,revenue=rev,refining_throughput_million_barrels=vol,refining_ebit_per_barrel=unit,refining_ebit=refining,renewable_diesel_ebit=rd,ethanol_ebit=eth,corporate_expense=corp,ebit=ebit,nopat=nopat,da=da,cash_capital_including_turnarounds=cash_capital,new_finance_lease_assets=new_finance_assets,total_capital_investment=capex,delta_nwc=nwc,explicit_net_reinvestment=explicit,economic_floor=economic,additional_reinvestment_reserve=reserve,fcff=fcff,pv=discounted));prev_revenue=rev
 terminal_nopat=rows[-1]['nopat']*(1+terminal_g);terminal_economic=terminal_nopat*terminal_g/roic;terminal_physical=(rows[-1]['total_capital_investment']-rows[-1]['da'])*(1+terminal_g)+rows[-1]['revenue']*terminal_g*.05;terminal_reinvest=max(terminal_physical,terminal_economic);terminal_fcf=terminal_nopat-terminal_reinvest;tv=terminal_fcf/(w-terminal_g);pvtv=tv/(1+w)**10;ev=pv+pvtv
 return {'assumptions':a,'rows':rows,'pv_explicit':pv,'terminal_nopat':terminal_nopat,'terminal_physical_reinvestment_floor':terminal_physical,'terminal_economic_reinvestment_floor':terminal_economic,'terminal_reinvestment':terminal_reinvest,'terminal_fcff':terminal_fcf,'terminal_value':tv,'pv_terminal':pvtv,'ev':ev,'bridge':bridge,'equity':ev+bridge,'shares':shares,'value':(ev+bridge)/shares,'terminal_fraction_ev':pvtv/ev}
def root():
 lo,hi=-2,30;target=387.65
 if not calc(unit_delta=lo)['value'] <= target <= calc(unit_delta=hi)['value']:return {'root':None,'reason':'target outside tested range'}
 for _ in range(90):
  mid=(lo+hi)/2
  if calc(unit_delta=mid)['value']<target:lo=mid
  else:hi=mid
 return {'additional_refining_ebit_usd_per_barrel_all_years':(lo+hi)/2,'year5_refining_ebit_usd_per_barrel':6+(lo+hi)/2,'value':calc(unit_delta=(lo+hi)/2)['value'],'limitation':'Assumes higher cycle margin earned on existing capacity; not revenue growth or incremental plant ROIC.'}
out={'classification':'conditional_cycle_fcff_not_entry_approval','price':387.65,'price_date':'2026-11-03','capital':CAP,'bridge':BRIDGE,'cases':{k:calc(k) for k in CASES},'reverse':root(),'sensitivities':{'roic_9pct':calc(roic_override=.09)['value'],'roic_15pct':calc(roic_override=.15)['value'],'remove_all_historical_benefit_utb_environment_aro_reserves':calc(bridge=BRIDGE+472+441+275+193)['value'],'remove_current_income_tax_reserve':calc(bridge=BRIDGE+1579)['value'],'actual_oct23_share_denominator':calc(shares=278.8844)['value'],'no_extra_repatriation_stress':calc(bridge=BRIDGE+100)['value'],'aro_full_fy2025_reserve':calc(bridge=BRIDGE-189)['value'],'nci_proxy_plus_1000':calc(bridge=BRIDGE-1000)['value'],'nci_proxy_minus_1000':calc(bridge=BRIDGE+1000)['value'],'wacc_plus_1pp':calc(wacc_delta=.01)['value'],'wacc_minus_1pp':calc(wacc_delta=-.01)['value'],'annual_cash_capital_plus_500':calc(capex_delta=500)['value'],'renewable_diesel_loss_300_from_year4':calc(rd_terminal_delta=-300)['value'],'refining_unit_minus_1':calc(unit_delta=-1)['value'],'refining_unit_plus_1':calc(unit_delta=1)['value']}}
(P/'model.json').write_text(json.dumps(out,indent=2)+'\n')
print({k:round(v['value'],2) for k,v in out['cases'].items()},'bridge',BRIDGE,'reverse',out['reverse'])
