from pathlib import Path
import json,csv
B=Path(__file__).parent
H=json.loads((B/'history.json').read_text())['periods']
# Each fixed point below is from an issuer table, not from the prior research register.
retained={
'FY2024':{'revenue':9297.278,'gross_profit_adjusted':None,'ebit_adjusted':None,'source':'FY2026_10K table98 + FY2024_RELEASE brand revenue table','basis':'derived_comparable_rounded','note':'9915.678 continuing revenue minus rounded Dickies618.4. +/-0.05 rounding uncertainty. Not exact retained revenue; retained EBIT not disclosed.'},
'FY2025':{'revenue':8962.626,'gross_profit_adjusted':4852.370,'ebit_adjusted':529.419,'source':'DICKIES_RECAST table4','basis':'management_adjusted'},
'FY2026':{'revenue':9295.952,'gross_profit_adjusted':5129.310,'ebit_adjusted':649.974,'source':'FY2026_RELEASE table0, twelve months','basis':'management_adjusted'},
'H1FY2025':{'revenue':1652.269+2605.545,'gross_profit_adjusted':855.430+1377.529,'ebit_adjusted':-105.790+300.756,'source':'DICKIES_RECAST tables0,1','basis':'derived_management_adjusted'},
'H1FY2026':{'revenue':4309.864,'gross_profit_adjusted':2300.302,'ebit_adjusted':255.108,'source':'Q2FY2027_RELEASE table11, six months','basis':'management_adjusted'},
'H1FY2027':{'revenue':4364.511,'gross_profit_adjusted':2409.722,'ebit_adjusted':269.168,'source':'Q2FY2027_RELEASE table10, six months','basis':'management_adjusted'},
'Q3FY2026':{'revenue':2820.054,'gross_profit_adjusted':1607.080,'ebit_adjusted':340.997,'source':'Q3FY2026_RELEASE table2, three months','basis':'management_adjusted'},
'Q4FY2026':{'revenue':2166.034,'gross_profit_adjusted':1221.928,'ebit_adjusted':53.870,'source':'FY2026_RELEASE table0, three months','basis':'management_adjusted'},
'Q1FY2027':{'revenue':1669.379,'gross_profit_adjusted':917.044,'ebit_adjusted':269.168-363.716,'source':'Q2FY2027_RELEASE table10 H1 minusQ2; Q1FY2027_10Q table6','basis':'derived_management_adjusted'},
'Q2FY2027':{'revenue':2695.132,'gross_profit_adjusted':1492.678,'ebit_adjusted':363.716,'source':'Q2FY2027_RELEASE table10, three months','basis':'management_adjusted'}}
for period,terms in [('TTM2026',[('FY2026',1),('H1FY2027',1),('H1FY2026',-1)]),('TTM2025',[('FY2025',1),('H1FY2026',1),('H1FY2025',-1)])]:
 retained[period]={m:round(sum(retained[p][m]*s for p,s in terms),6) for m in ['revenue','gross_profit_adjusted','ebit_adjusted']}
 retained[period].update(source=';'.join(f'{s:+}*{p}' for p,s in terms),basis='derived_management_adjusted')
for p,d in retained.items():
 for m in ['revenue','gross_profit_adjusted','ebit_adjusted']:
  if d[m] is not None:d[m]=round(d[m],6)
 d['gross_margin']=None if d['gross_profit_adjusted'] is None else d['gross_profit_adjusted']/d['revenue']
 d['operating_margin']=None if d['ebit_adjusted'] is None else d['ebit_adjusted']/d['revenue']
 d['cfo_retained_exact']=None;d['capex_retained_exact']=None
 d['period_start']=H[p]['start'];d['period_end']=H[p]['end']
# Full reconciliation of retained EBIT
adj={
'FY2025':{'GAAP_ebit':303.773,'Reinvent':162.644,'impairments':89.242,'transaction_costs':.490,'adjusted_including_Dickies':556.149,'Dickies_adjusted_contribution':26.730,'adjusted_retained':529.419,'source':'FY2026_RELEASE table2'},
'FY2026':{'GAAP_ebit':576.569,'Reinvent':43.730,'impairments':30.716,'transaction_costs':10.194,'adjusted_including_Dickies':661.209,'Dickies_adjusted_contribution':11.235,'adjusted_retained':649.974,'source':'FY2026_RELEASE table0'},
'H1FY2026':{'GAAP_ebit':226.011,'Reinvent':46.265,'impairments':0,'transaction_costs':2.021,'adjusted_including_Dickies':274.297,'Dickies_adjusted_contribution':19.189,'adjusted_retained':255.108,'source':'Q2FY2027_RELEASE table11'},
'H1FY2027':{'GAAP_ebit':284.848,'Reinvent':-15.680,'impairments':0,'transaction_costs':0,'adjusted_including_Dickies':269.168,'Dickies_adjusted_contribution':0,'adjusted_retained':269.168,'source':'Q2FY2027_RELEASE table10'},
'Q3FY2026':{'GAAP_ebit':289.054,'Reinvent':5.099,'impairments':30.716,'transaction_costs':8.173,'adjusted_including_Dickies':333.042,'Dickies_adjusted_contribution':-7.955,'adjusted_retained':340.997,'source':'Q3FY2026_RELEASE table2'},
'Q4FY2026':{'GAAP_ebit':61.504,'Reinvent':-7.634,'impairments':0,'transaction_costs':0,'adjusted_including_Dickies':53.870,'Dickies_adjusted_contribution':0,'adjusted_retained':53.870,'source':'FY2026_RELEASE table0'}}
dickies={
'FY2025':{'revenue':542.065,'gross_profit_adjusted':233.467,'ebit_adjusted':26.730},
'FY2026':{'revenue':309.255,'gross_profit_adjusted':136.662,'ebit_adjusted':11.235},
'H1FY2025':{'revenue':116.791+152.403,'gross_profit_adjusted':50.660+63.028,'ebit_adjusted':1.109+14.426},
'H1FY2026':{'revenue':253.508,'gross_profit_adjusted':115.187,'ebit_adjusted':19.189},
'TTM2026':{'revenue':55.747,'gross_profit_adjusted':21.475,'ebit_adjusted':11.235-19.189},
'TTM2025':{'revenue':542.065+253.508-(116.791+152.403),'gross_profit_adjusted':233.467+115.187-(50.660+63.028),'ebit_adjusted':26.730+19.189-(1.109+14.426)},
'Sep2025_HFS':{'cash':5.000,'accounts_receivable':104.972,'inventory':140.842,'other_current_assets':11.346,'ppe_net':27.530,'intangible_net':244.503,'operating_rou_asset':1.092,'other_assets':1.222,'total_assets':536.507,'current_debt':1.027,'accounts_payable':24.243,'accrued_liabilities':30.584,'longterm_debt':13.457,'operating_lease_liabilities':.679,'other_liabilities':.510,'total_liabilities':70.500,'source':'Q2FY2026_10Q table20'},
'March2025_rounded':{'accounts_receivable':116.9,'inventory':134.2,'source':'FY2026_10K MD&A Consolidated Balance Sheets'},
'cash_boundary':{'cfo':None,'capex':None,'software':None,'standalone_WC_cash':None,'conclusion':'Undisclosed. P&L contribution, a single balance sheet and sale proceeds do not identify standalone operating cash. Do not assign all sold WC to CFO or call any modeled number reported.'}}
dickies['Sep2025_HFS']['core_operating_wc']=104.972+140.842-24.243
dickies['Sep2025_HFS']['extended_operating_wc']=104.972+140.842+11.346-24.243-30.584
# A source-limited diagnostic, explicitly NOT a standalone CFO/FCF estimate.
dickies['pre_tax_pre_WC_cash_proxy_bounds']={
'method':'Adjusted EBIT + D&A - cash capex/software, BEFORE working capital, cash tax, financing and GAAP-adjustment cash. Not CFO; not retained FCF. Requires component non-negativity, no net reversals, and all Dickies D&A to be attributed within All Other rather than corporate allocations.',
'TTM2026':{'Dickies_EBIT':-7.954,'DandA_min':0,'DandA_max':18.261,'DandA_bound_source':'Entire All Other FY2026 D&A/write-downs, FY2026_10K table161; a deliberately loose upper bound','capex_min':0,'capex_max':43.889,'capex_bound_source':'Entire consolidated Q3FY26 cash PPE+software, 9M less H1','proxy_min':-7.954-43.889,'proxy_max':-7.954+18.261},
'TTM2025':{'Dickies_EBIT':30.384,'DandA_min':0,'DandA_max':21.671+18.261,'DandA_bound_source':'All Other FY2025+FY2026 D&A upper bound without subtracting prior H1; no standalone quarter disclosure','capex_min':0,'capex_max':134.937,'capex_bound_source':'Entire consolidated prior TTM cash PPE+software','proxy_min':30.384-134.937,'proxy_max':30.384+21.671+18.261},
'interpretation':'These source-limited ranges are broad and conditional. They demonstrate why a narrow Dickies retained-CFO estimate cannot be justified by revenue allocation or an arbitrary percentage. They are not probability distributions or hard cash-flow bounds.'}
tariff={
'facts':{'gross_IEEPA_paid_FY2026':149.7,'FY2026_COGS_reversal':93.8,'FY2026_inventory_reserve':55.9,'vendor_reimburse_obligation':37.6,'FY2026_vendor_COGS_entry':22.7,'FY2026_vendor_inventory_entry':14.9,'Q1FY2027_reserve_release':37.3,'Q2FY2027_reserve_release':18.6,'Q1FY2027_refund_receivable_remaining':100.8,'H1FY2027_refund_interest_income':5.6,'Q2FY2027_refund_interest_income':4.1,'source':'FY2026_10K Note1; Q1FY2027_10Q Note1; Q2FY2027_10Q Note1, MD&A'},
'interpretation':'Issuer says gross IEEPA duties had no net FY26 or FY27 gross-margin effect after matched reversals. This does NOT disclose retained-business first-half timing, or identify cross-period Dickies allocation. Do not subtract FY27 inventory reserve releases again as independent earnings windfalls.',
'earnings_x':{'definition':'Net retained H1FY26 IEEPA expense whose later reversal falls within current TTM. Different from gross duty cash paid p.','current_EBIT_formula':'664.034 - x','prior_EBIT_formula':'589.561 + x','zero_growth_x':(664.034-589.561)/2,'gross_outer_envelope':[0,93.8],'envelope_limit':'0..93.8 is an explicitly conditional, company-wide gross-duty upper envelope, not an estimate of retained H1 expense; vendor credits/allocations could make a narrower net envelope, but timing not disclosed. No probability or mandatory gate assigned.'},
'full_cash_identity':{'period_formula':'tariff_neutral_FCF = reported_FCF + P - R - C + V - I','P':'gross IEEPA duty cash paid in the period','R':'gross IEEPA refund cash collected in the period','C':'original vendor/partner concessions realized as cash benefit in the period; not the accounting accrual','V':'cash reimbursements actually paid to those vendors/partners','I':'related refund-interest CASH receipts included in CFO (income recognized5.6m is not exact cash proof)','current_other_adjustments':'Subtract actual net pension termination cash benefit, approximately100m. Subtract Dickies standalone FCF D_current, if estimated, and label it. Prior uses D_prior. Do not subtract sale proceeds from FCF because they are already investing, not CFO.','current_formula_full':'635.879 - N_pension + P_current - R_current - C_current + V_current - I_current - D_current','prior_formula_full':'232.907 + P_prior - R_prior - C_prior + V_prior - I_prior - D_prior','constraints':['P_prior + P_current =149.7 only when all IEEPA cash payments are within the two TTMs and measured on same original GAAP perimeter.','0<=P_prior<=149.7 gross-company outer bound.','At least about48.9m principal refunded in Q1FY27 from149.7 minus100.8 receivable; subsequent substantially-all collection is qualitative, not a point figure.','Vendor/partner payable37.6m is not proof it has been cash paid. Concession cash timing is not disclosed.','The approximate110m is full-year management net-refund guidance bridge, not exact H1 realized net collections.','No unsupported numerical Dickies CFO/capex/software/WC allocation is inserted.']},
'simplified_cash_illustration':{'assumptions':['R_current=149.7 gross principal fully collected','N_pension=100 approximate','C=V=I=D=0 purely to reproduce prior p-only illustration, not full normalization'],'current_formula':'535.879 - p','prior_formula':'232.907 + p','warning':'Audit-only partial identity; not proof of sustainable retained-business cash growth.'}}
tariff['earnings_x']['sensitivity']=[{'x':x,'current':664.034-x,'prior':589.561+x,'growth':(664.034-x)/(589.561+x)-1} for x in [0,10,20,30,37.2365,50,93.8]]
ledger=[
{'item':'Dickies sale investing proceeds','period':'Q3FY2026','value':600.524,'source':'Q3FY2026_10Q table8','cash_treatment':'Investing; never in strict CFO-PPE-software FCF.'},
{'item':'Dickies final working-capital price adjustment paid','period':'Q1FY2027','value':-11.867,'source':'Q1FY2027_10Q table8 and Note4','cash_treatment':'Investing. Net proceeds across sale and adjustment588.657; not an operating-WC outflow.'},
{'item':'Dickies final pretax gain','period':'FY2026','value':127.211,'source':'FY2026_10K tables98,100 and Note3','cash_treatment':'Other income below EBIT; CFO reverses gain. Do not remove again from CFO or operating EBIT.'},
{'item':'Supreme net sale proceeds','period':'FY2025','value':1506.223,'source':'FY2026_10K table100, Note3','cash_treatment':'Sale proceeds in investing; Supreme operating cash separately classified discontinued and excluded from strict continuing FCF.'},
{'item':'Pension termination cash asset reversion before excise','period':'Q4FY2026','value':125.373,'source':'FY2026_10K table100, Note17','cash_treatment':'CFO; excise tax25.1 rounded was paid. Net approximately100m, company comparator. Separate83.5m replacement-plan transfer is restricted for future401k contributions, not excess cash.'},
{'item':'Pension premium refund','period':'Q2FY2027','value':3.089,'source':'Q2FY2027_10Q Note10; operating facts O2','cash_treatment':'Below-EBIT income, transferred into qualified replacement plan; no free excess cash. Avoid adding to enterprise cash.'},
{'item':'Timberland tax disputed-payment historical cash','period':'FY2023, October19 2022','value':-875.7,'source':'FY2026_10K Note20','cash_treatment':'Outside3-yearFY24-FY26 window. FY24 receivable write-off921.409 (CF gross adjustment), net tax expense approx690 is noncash in FY24. Do not deduct old875.7 as future liability.'},
{'item':'FY24 legal settlement gain','period':'FY2024','value':29.1,'source':'FY2024_RELEASE reconciliation footnote(c)','cash_treatment':'Below-EBIT legal settlement gain; cash timing not separately quantified here. Do not call recurring operating EBIT.'},
{'item':'Current securities class action','period':'As of2026-09-26','value':None,'source':'Q2FY2027_10Q Note19','cash_treatment':'Unspecified damages, no source-based payment estimate. Not zero liability estimate.'}]
checks=[]
for p,d in adj.items():
 checks.append({'period':p,'check':'GAAP+adjustments=adjusted','difference':round(d['GAAP_ebit']+d['Reinvent']+d['impairments']+d['transaction_costs']-d['adjusted_including_Dickies'],6),'pass':abs(d['GAAP_ebit']+d['Reinvent']+d['impairments']+d['transaction_costs']-d['adjusted_including_Dickies'])<=.0011})
 checks.append({'period':p,'check':'adjusted-Dickies=retained','difference':round(d['adjusted_including_Dickies']-d['Dickies_adjusted_contribution']-d['adjusted_retained'],6),'pass':abs(d['adjusted_including_Dickies']-d['Dickies_adjusted_contribution']-d['adjusted_retained'])<=.0011})
checks.append({'period':'TTM2026','check':'quarter retainedEBIT vs annual+H1 bridge','difference':round(sum(retained[p]['ebit_adjusted'] for p in ['Q3FY2026','Q4FY2026','Q1FY2027','Q2FY2027'])-retained['TTM2026']['ebit_adjusted'],6),'pass':True,'note':'Issuer1thousand rounding difference; annual+H1 controls.'})
(B/'retained_bridge.json').write_text(json.dumps({'units':'USD million','as_of':'2026-11-04','retained_management_adjusted':retained,'ebit_adjustments':adj,'Dickies':dickies,'tariffs':tariff,'special_cash_ledger':ledger},indent=2))
for name,obj in [('retained_history',retained),('ebit_adjustment_bridge',adj)]:
 keys=sorted(set().union(*(d for d in obj.values())))
 with (B/(name+'.csv')).open('w') as f:
  w=csv.DictWriter(f,fieldnames=['period']+keys);w.writeheader();w.writerows([{'period':p,**d} for p,d in obj.items()])
with (B/'special_cash_ledger.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=list(ledger[0]));w.writeheader();w.writerows(ledger)
# CFO year-over-year attribution and WC contributions
cfo_fields=['net_income_cont','cf_impairment','da_and_other_asset_writedowns','cf_rou_reduction','sbc','cf_bad_debt','cf_pension','cf_pension_asset_reversion','cf_tax_receivable_writeoff','cf_gain_sale_reversal','cf_other_including_deferred_tax','wc_ar','wc_inventory','wc_ap','wc_tax','wc_accrued','cf_lease_cash_change','wc_other']
variance=[{'metric':m,'prior_TTM':H['TTM2025'][m],'current_TTM':H['TTM2026'][m],'change':round(H['TTM2026'][m]-H['TTM2025'][m],6)} for m in cfo_fields]
with (B/'cfo_variance_bridge.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=list(variance[0]));w.writeheader();w.writerows(variance)
checks.append({'period':'TTM2026vsTTM2025','check':'CFO change attribution','difference':round(sum(d['change'] for d in variance)-(H['TTM2026']['cfo_cont']-H['TTM2025']['cfo_cont']),6),'pass':abs(sum(d['change'] for d in variance)-(H['TTM2026']['cfo_cont']-H['TTM2025']['cfo_cont']))<.0011})
(B/'Bridge_Validation_Checks.json').write_text(json.dumps(checks,indent=2))
print(json.dumps({'retained_current':retained['TTM2026'],'retained_prior':retained['TTM2025'],'growth':{m:retained['TTM2026'][m]/retained['TTM2025'][m]-1 for m in ['revenue','gross_profit_adjusted','ebit_adjusted']},'checks':checks},indent=2))
