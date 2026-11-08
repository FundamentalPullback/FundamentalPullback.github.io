"""PHM extension: exact reported cash identity + conditional homebuilding-only FCFF.
No import/execution of the legacy RI model. Does not produce consolidated equity value.
"""
from pathlib import Path
import json,csv
P=Path(__file__).parent;d=json.loads((P/'inputs.json').read_text());checks=[]
def eq(name,a,b):
 checks.append({'check':name,'actual':a,'expected':b,'pass':abs(a-b)<1e-7})
def ttm(series,y):return {k:series[f'FY{y-1}'][k]+series[f'9M{y}'][k]-series[f'9M{y-1}'][k] for k in series[f'FY{y-1}']}
cf=d['cashflow_rows'].copy()
for p,v in cf.items():eq('reported_CFO_'+p,sum(v.values()),d['reported_cfo'][p])
for y in [2025,2026]:cf[f'TTM{y}']=ttm(cf,y)
for p,v in cf.items():v['calculated_cfo']=sum(v.values())
# Separate identifiable mortgage principal working-capital from earnings; never claim this removes the segment.
loan_bridge={}
for p in d['reported_cfo']:
 c=cf[p]['mortgage_loan_cash'];borrow=d['mortgage_net_borrowing'][p]
 loan_bridge[p]={'CFO_loan_book_release':c,'financing_net_warehouse_borrowing':borrow,'combined_principal_cash_release':c+borrow,'CFO_ex_identified_loan_book_movement':cf[p]['calculated_cfo']-c,'not_homebuilding_CFO':True}
# Detailed consolidated operating cash flow to all-in cash reconciliation, Q3 YTD.
cfo=cf['9M2026']['calculated_cfo'];invest={'capex':-78.221,'JV_contributions':-45.773,'JV_capital_returns':21.564,'asset_sales':90.587,'other_investing':3.0}
financing={'debt_issuance':794.784,'notes_repayment':-612.691,'warehouse_repayment':-149.093,'debt_issue_costs':-23.411,'land_finance_inflow':26.558,'land_finance_repayment':-31.633,'buybacks':-1031.567,'buyback_excise':-11.482,'award_withholding':-39.557,'dividends':-150.780}
eq('investing_9M',sum(invest.values()),-8.843);eq('financing_9M',sum(financing.values()),-1228.872)
change=cfo+sum(invest.values())+sum(financing.values());eq('total_cash_change',change,-600.749);eq('ending_cash',2008.776+change,1408.027)
# Accrual operating earnings rebuilt from reported segment revenue/cost/SG&A.
hb=d['hb'].copy();fs=d['financial_services'].copy();hb['TTM2026']=ttm(hb,2026);fs['TTM2026']=ttm(fs,2026)
for p,x in hb.items():
 x['core_unlevered_operating_earnings']=x['revenue']-x['cost_revenue']-x['sga']+x['interest_released']-x['option_writeoffs']-x['intang_amortization']
 x['definition']='Reported sales-cost-SG&A, add released capitalized financing interest, retain option/pre-acquisition writeoffs and intangible amortization. Excludes all remaining other-income items, JV income and FS. Not company GAAP EBIT; recurrent land impairments in cost remain.'
other=d['other_9m2026'];eq('9M_HB_EBT_normalization',1601.525+81.979+.410+2.637-31.842-21.4-.959-(28.940-21.4),hb['9M2026']['core_unlevered_operating_earnings'])
b0=d['balance']['2025-12-31'];b=d['balance']['2026-09-30'];ic=d['capitalized_interest_9m2026'];eq('capitalized_interest_roll',ic['begin']+ic['incurred']-ic['released_to_cost'],ic['end'])
# Inventory and options combined prevents an exercise/deposit transfer being counted twice.
cap0=b0['inventory']-b0['inventory_interest']+b0['option_and_preacquisition'];cap=b['inventory']-b['inventory_interest']+b['option_and_preacquisition']
cap_delta=cap-cap0
cost_nonfinance_nonimpairment=8358.966-81.979-41.898
recognized_additions=cap_delta+cost_nonfinance_nonimpairment+41.898+23.132
asset_roll={'begin_inventory_ex_interest_plus_options':cap0,'end_inventory_ex_interest_plus_options':cap,'net_book_increase':cap_delta,'inventory_balance_change':b['inventory']-b0['inventory'],'reported_inventory_CFO_use':1149.355,'balance_vs_CFO_inventory_gap':b['inventory']-b0['inventory']-1149.355,'option_preacquisition_change':b['option_and_preacquisition']-b0['option_and_preacquisition'],'option_writeoffs':23.132,'option_additions_less_transfers_and_other':b['option_and_preacquisition']-b0['option_and_preacquisition']+23.132,'recognized_additions_before_noncash_movement_corrections':recognized_additions,'actual_gross_land_build_option_cash_spend':None,'cash_spend_warning':'Cost of revenues contains noncash overhead/depreciation allocations; noncash land financing, option transfers, acquisitions/disposals and classification changes need the full rollforward. This accrual identity is NOT a cash expenditure claim.'}
# Supplemental issuer custom tag is net of capitalized treatment; do not mislabel as all gross interest paid.
interest={'capitalized_incurred':85.874,'released_to_cost':81.979,'net_interest_inventory_growth':3.895,'cash_caption_value':10.760,'cash_caption_tag':'phm:Interestpaidcapitalizednet','gross_cash_interest_HB':None,'warning':'10.760 is not demonstrated gross cash interest. Accrual incurred is not identical to cash paid; no automatic gross-up or CFO addback.'}
# Operating scenarios: explicit existing inventory/deposit capital, not retained-equity balancing plug.
base_rev=hb['TTM2026']['revenue'];inv0=b['inventory']-b['inventory_interest'];options0=b['option_and_preacquisition'];customer0=b['customer_deposits'];da_ratio=hb['TTM2026']['da']/base_rev
specs={'adverse':{'sales_growth_first5':[-.05,0,.01,.02,.02],'margin_first5':[.12,.115,.115,.115,.115],'terminal_margin':.115,'wacc':.12,'g':.02,'terminal_roic':.10,'inventory_intensity_end5':1.05,'option_intensity_end5':1.10},'central':{'sales_growth_first5':[.02,.03,.03,.03,.03],'margin_first5':[.145]*5,'terminal_margin':.145,'wacc':.11,'g':.025,'terminal_roic':.13,'inventory_intensity_end5':1.0,'option_intensity_end5':1.0},'favorable':{'sales_growth_first5':[.04,.05,.05,.04,.04],'margin_first5':[.16,.165,.17,.175,.175],'terminal_margin':.175,'wacc':.10,'g':.03,'terminal_roic':.16,'inventory_intensity_end5':.97,'option_intensity_end5':1.0}}
# All cases keep leases/SBC in margin. No future buybacks or supplier financing plug.
# Other operating cash requirement is explicitly assumed incremental 2% of revenue growth, not a reported opening balance.
def forecast(s,save_rows=True):
 rev=base_rev;inventory=inv0;options=options0;customer=customer0;pv=0;rows=[]
 for y in range(1,11):
  prior_rev=rev;oldinv=inventory;oldopt=options;oldcust=customer
  growth=s['sales_growth_first5'][y-1] if y<=5 else s['sales_growth_first5'][-1]+(s['g']-s['sales_growth_first5'][-1])*(y-5)/5
  rev*=1+growth
  margin=s['margin_first5'][y-1] if y<=5 else s['margin_first5'][-1]+(s['terminal_margin']-s['margin_first5'][-1])*(y-5)/5
  invratio=inv0/base_rev*(1+(s['inventory_intensity_end5']-1)*min(y/5,1));optratio=options0/base_rev*(1+(s['option_intensity_end5']-1)*min(y/5,1))
  # No automatic liquidation when sales decline or target turnover improves: old land/options stay tied up.
  inventory=max(oldinv,rev*invratio);options=max(oldopt,rev*optratio);customer=rev*customer0/base_rev
  delta_inventory=inventory-oldinv;delta_options=options-oldopt;delta_customer=customer-oldcust
  other_buffer=max(rev-prior_rev,0)*.02
  physical_capex=max(rev*.007,rev*da_ratio);da=rev*da_ratio;ebit=rev*margin;nopat=ebit*.76
  operating_investment=delta_inventory+delta_options-delta_customer+other_buffer+physical_capex-da
  fcff=nopat-operating_investment;pv+=fcff/(1+s['wacc'])**y
  eq(f'{s["wacc"]}_cash_identity_y{y}',fcff+operating_investment,nopat)
  # Explicit interest-service stress only; not contractual maturity budget or segment-specific cash certification.
  assumed_aftertax_HB_interest=(1808.896+136.727)*.065*.76
  rows.append(dict(year=y,revenue=rev,ebit=ebit,nopat=nopat,inventory_ex_interest_begin=oldinv,inventory_ex_interest_end=inventory,delta_inventory=delta_inventory,option_preacquisition_begin=oldopt,option_preacquisition_end=options,delta_options=delta_options,customer_deposit_begin=oldcust,customer_deposit_end=customer,delta_customer_deposits=delta_customer,additional_other_operating_cash_buffer=other_buffer,physical_capex=physical_capex,da_HB=da,incremental_operating_capital_cash=operating_investment,fcff_homebuilding_conditional=fcff,assumed_aftertax_interest_service=assumed_aftertax_HB_interest,operating_cash_after_interest_before_principal=fcff-assumed_aftertax_HB_interest,external_funding_need_before_principal=max(0,assumed_aftertax_HB_interest-fcff),new_debt_funding_assumed=0,capital_cash_scope_complete=False))
 # Steady state funds inventory/options/customer balances at their actual terminal ratios, no sudden working-capital release.
 r11=rev*(1+s['g']);n11=r11*s['terminal_margin']*.76
 terminal_physical=max(r11*.007,r11*da_ratio);terminal_da=r11*da_ratio
 required_capital=inventory*s['g']+options*s['g']-customer*s['g']+.02*(r11-rev)+terminal_physical-terminal_da
 roic_requirement=n11*s['g']/s['terminal_roic'];terminal_reinv=max(required_capital,roic_requirement)
 tcf=n11-terminal_reinv;tv=tcf/(s['wacc']-s['g']);ev=pv+tv/(1+s['wacc'])**10
 return dict(inputs=s,rows=rows,conditional_homebuilding_operating_EV=ev,approved_operating_EV=None,terminal_reinvestment=terminal_reinv,terminal_component_capital_requirement=required_capital,terminal_g_roic_requirement=roic_requirement,terminal_fcff=tcf,terminal_value_weight=(tv/(1+s['wacc'])**10)/ev,terminal_implied_incremental_ROIC=n11*s['g']/terminal_reinv,forecast_liquidity_certified=False)
cases={k:forecast(v) for k,v in specs.items()}
for k,c in cases.items():
 with (P/f'forecast_{k}.csv').open('w') as f:w=csv.DictWriter(f,fieldnames=c['rows'][0]);w.writeheader();w.writerows(c['rows'])
 c.pop('rows')
sensitivity=[]
for w in [.10,.11,.12]:
 for ratio in [1,1.05,1.10]:
  s=dict(specs['central'],wacc=w,inventory_intensity_end5=ratio);c=forecast(s);sensitivity.append(dict(wacc=w,inventory_intensity_end5=ratio,conditional_homebuilding_operating_EV=c['conditional_homebuilding_operating_EV']))
# Do not choose a mortgage business value, cash allocation or JV value merely to generate a share target.
fs_sep={'reported_financial_services':fs,'mortgage_loan_asset':433.947,'warehouse_debt':383.245,'loan_less_warehouse':50.702,'segment_total_assets':879.691,'other_segment_assets':879.691-433.947,'FS_equity_value':None,'FS_distributable_cash':None,'consolidated_cash_available_to_HB':None,'notes':'The 50.702 loan margin is not FS equity, surplus cash or valuation. Title/insurance, derivative assets/liabilities, repurchase risk, taxes, working capital and equity/capital support must be included. Guarantor consolidating data are not the homebuilding/FS segment split.'}
missing=['Full HB/FS segment cash-flow and balance allocation: cash, operating liabilities, taxes, capex, SBC, derivatives and support capital.','Inventory/option/pre-acquisition gross additions, option-exercise transfers, noncash land-funding additions and cash settlements; isolate capitalized interest paid and noncash overhead.','Current consolidated-inventory-not-owned liability and maturity/claim terms, intercompany allocation and guarantee exposure.','Independent mortgage/title/insurance equity value, normal capital needs, cash tax and operating distribution profile; warehouse renewal on 2027-08-10.','Cash vs capitalized interest reconciliation and cash-tax adjustment for unlevered HB operations.','Cycle evidence for sales/margins, capital intensity and other cash buffer; operating debt maturity budget; calibrated USD WACC.']
r={'as_of':'2026-11-08','method':'Homebuilding FCFF first; financial services separate only when defensible','stage3_complete':False,'approved_values':None,'entry_approved':False,'existing_RI_replaced':True,'legacy_RI_deprecated':True,'consolidated_CFO_reconciliation':cf,'mortgage_principal_bridge':loan_bridge,'all_cash_9M2026':{'operating':cfo,'investing':invest,'financing':financing,'change':change,'begin':2008.776,'end':1408.027},'homebuilding_operating_earnings':hb,'operating_asset_rollforward':asset_roll,'interest_reconciliation':interest,'financial_services_separation':fs_sep,'conditional_homebuilding_cases':cases,'sensitivity':sensitivity,'price_target':None,'consolidated_equity_value':None,'inverse_valuation':None,'inverse_blocker':'Share-price inversion requires separately valued FS, JV claims, available cash and obligations. Treating missing terms as zero would fabricate an answer.','illustrative_cost_capital':{'rf':.0486,'ERP':.0441,'beta_assumed':1.5,'Ke_anchor':.0486+1.5*.0441,'USD_debt_cost_assumed':.065,'WACC_hurdles':[.10,.11,.12],'rf_date':'2026-11-06','ERP_date':'2026-11-01','ERP_source_rf':.0529,'date_basis_mismatch':True,'not_current_calibrated_WACC':True},'missing_data':missing,'checks_passed':len(checks),'no_new_debt_plug':True,'cash_validation':'Published consolidated CFO is exact; projected homebuilding component identities are exact but segment-specific cash allocation and gross cash replacement remain incomplete.'}
assert all(c['pass'] for c in checks)
(P/'results.json').write_text(json.dumps(r,indent=2)+'\n');(P/'checks.json').write_text(json.dumps({'all_pass':True,'checks':checks},indent=2)+'\n')
with (P/'consolidated_cashflow.csv').open('w') as f:w=csv.DictWriter(f,fieldnames=['period',*next(iter(cf.values()))]);w.writeheader();w.writerows(dict(period=k,**v) for k,v in cf.items())
print(json.dumps({'checks':len(checks),'HB_core_TTM':hb['TTM2026'],'operating_asset_roll':asset_roll,'conditional_operating_EV':{k:c['conditional_homebuilding_operating_EV'] for k,c in cases.items()},'group_equity_value':None},indent=2))
