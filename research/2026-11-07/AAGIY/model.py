"""AIA: reconciliación aseguradora, no valoración calibrada. USD millones salvo ADR."""
import json,pathlib,csv
P=pathlib.Path(__file__).parent
shares=10346.644870 # issued ordinary shares Oct31; not current fully diluted
adr=shares/4
price=40.39
netfsg=3935-732-163-282
fs=10972+netfsg+389-1906-1743
resources=fs+19630+11172
# 20 observations, rounded published volumes; uncertainty from 3.06M and1.48M precision
vol=[350750,386720,277870,230710,3060000,562070,340910,308740,1480000,970180,353480,432700,321470,236040,279650,422840,271810,412750,362140,309210]
# TTM derived using reported USD/AER comparable half-years; not new quarterly earnings
r={'ticker':'AAGIY','status':'material_partial','fair_value':None,'canonical_approved_value':None,'margin_of_safety':None,'entry_approved':False,'currency':'USD','units':'USD millions except per-ADR and ratios','price':price,'price_date':'2026-11-06','shares_ordinary_millions':shares,'share_basis':'issued at2026-10-31, not fully diluted','adr_ratio':4,'market_cap_derived_usdm':price*adr,'bridges':{'ufsg':3935,'new_business_investment':-732,'group_office':-163,'finance_other':-282,'net_fsg':netfsg,'opening_free_surplus':10972,'investment_other':389,'dividend':-1906,'buybacks':-1743,'closing_free_surplus':fs,'required_capital':19630,'eligible_tier2':11172,'capital_resources':resources,'shareholder_capital_ratio':resources/19630,'IFRS_shareholders_equity':40679,'allocated_equity':47686,'EV':80555,'EV_equity':83402,'goodwill_other_net_in_EV_equity':2847},'ttm_to_june2026':{'OPAT':7136+4163-3609,'net_profit_attributable':6234+4294-2534,'UFSG':6765+3935-3569,'net_FSG':4451+2758-2430,'not_projection':True},'context_not_fair_value':{'EV_equity_per_ADR':83402/adr,'price_to_EV_equity':price*adr/83402,'price_to_allocated_equity':price*adr/47686,'average_volume_20_rounded':sum(vol)/20,'volume_window':'2026-10-12 to2026-11-06','volume_threshold':500000,'volume_pass_from_rounded_data':sum(vol)/20>=500000,'normalised_distributable_cash':None},'valuation_architecture':{'formula':'V0 = sum(distributions_t/(1+ke)^t) + terminal_value/(1+ke)^T','distributions':'Dividend + repurchase pool, net issuance, subject to legal capital and remittances; no automatic free-surplus addback','ke':None,'terminal_growth':None,'terminal_value':None,'cash_bridge_status':'incomplete','residual_income_crosscheck':'Allocated equity only after IFRS reserve/OCI clean-surplus reconciliation; do not add EV/VIF/CSM to residual-income value.'},'EV_sensitivities_issuer_not_price_targets':{'base_EV':80555,'risk_discount_plus200bp':80555-11696,'risk_discount_minus200bp':80555+18077,'equity_prices_minus10pct':80555-2746,'mortality_morbidity_plus10pct':80555-6856,'USD_appreciates5pct':80555-766},'checks':{'net_fsg':netfsg==2758,'free_surplus':fs==10470,'resources':resources==41272,'EV_bridge':31248+49307==80555,'EV_equity_bridge':80555+2847==83402,'no_industrial_FCFF':True,'no_fabricated_quarterly_earnings':True}}
r['regulatory_LCSM']={'eligible_group_capital':85423,'prescribed_capital_requirement':37228,'coverage_ratio':85423/37228,'surplus':85423-37228,'not_shareholder_capital_ratio':True}
r['holding_company_resources']={'opening':10507,'subsidiary_capital_flows':1708,'corporate_activity':-82,'intercompany_loan_settlements':323,'borrowings_change':-316,'interest_payments':-285,'investment_and_other':29,'dividends':-1906,'buybacks':-1743,'closing':10507+1708-82+323-316-285+29-1906-1743,'not_unrestricted_cash':True,'jurisdiction_remittance_schedule_complete':False}
r['checks']['holding_company_resources']=r['holding_company_resources']['closing']==8235
r['checks']['LCSM_surplus']=r['regulatory_LCSM']['surplus']==48195
(P/'results.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
(P/'self_check.json').write_text(json.dumps({'all_pass':all(r['checks'].values()),'checks':r['checks'],'scope':'Arithmetic and guardrails, not independent underwriting approval'},indent=2)+'\n')
with (P/'financial_history.csv').open('w') as f:
 w=csv.writer(f);w.writerow(['period','OPAT','UFSG','net_FSG','net_profit_attributable','free_surplus_end']);w.writerows([['FY2025',7136,6765,4451,6234,10972],['H12025',3609,3569,2430,2534,9898],['H12026',4163,3935,2758,4294,10470]])
assert all(r['checks'].values())
print(json.dumps(r['context_not_fair_value'],indent=2))
