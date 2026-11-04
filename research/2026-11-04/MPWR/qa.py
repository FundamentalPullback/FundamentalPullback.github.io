import pathlib,json
p=pathlib.Path(__file__).parent;a=json.loads((p/'analysis.json').read_text());h=a['history'];x=json.loads((p/'facts/capital.json').read_text());pub=json.loads((p/'publication.json').read_text());q=[]
def test(k,v):q.append({'check':k,'pass':bool(v)})
def eq(k,v,z,tol=1e-6):test(k,abs(v-z)<tol)
for k in ['bear','base','bull','owner_fcf','equity_bridge','buy_ceiling']:test(k+'_absent',a[k] is None and pub[k] is None)
for k in ['approved_entry','stage35_approved']:test(k+'_false',not a[k] and not pub[k])
test('completed_false',not pub['latestCompleted']);test('control_still_open',not a['internal_control_remediated']);eq('price_reference',pub['price'],1262.19);test('price_date',pub['price_timestamp'].startswith('2026-11-04'));eq('scanner_preserved',pub['scanner_price'],1349.99)
for k,r in h.items():
 if r.get('cfo') is not None and r.get('ppe_cash_capex') is not None:
  eq(k+'_FCF_PPE',r['cfo']-r['ppe_cash_capex'],r['fcf_ppe_only'])
  if r.get('ppe_extended_terms_financing_cash') is not None:eq(k+'_equipment',r['cfo']-r['ppe_cash_capex']-r['ppe_extended_terms_financing_cash'],r['fcf_ppe_extended_terms'])
  if r.get('sbc_cashflow') is not None:eq(k+'_SBC',r['cfo']-r['ppe_cash_capex']-r['sbc_cashflow'],r['fcf_ppe_less_equity_sbc'])
for metric in ['revenue','ebit_reported','net_income','cfo','ppe_cash_capex','ppe_extended_terms_financing_cash','sbc_cashflow','da']:
 eq(metric+'_ttm_bridge',h['FY2025'][metric]+h['9M2026'][metric]-h['9M2025'][metric],h['TTM_September_2026'][metric])
eq('restated_FY24',h['FY2024']['net_income'],1592.058);eq('restated_EPS24',h['FY2024']['eps_diluted'],32.60);eq('direct_Q4_25',h['Q4_2025']['eps_diluted'],3.49);eq('current_q3_EBIT',h['Q3_2026']['ebit_reported'],x['q3_ebit']);eq('ebt_vs_ebit',x['q3_ebit']+x['q3_other_income'],x['q3_ebt']);eq('tax_to_NI',x['q3_ebt']-x['q3_tax'],h['Q3_2026']['net_income']);eq('cash_sum',x['cash']+x['short_investments'],1091.234);eq('commitments',sum(x[k] for k in ['purchase_commitments_q4','purchase_commitments_2027','purchase_commitments_2028','purchase_commitments_2029']),x['purchase_commitments']);eq('deferred_plan_asset',x['life_insurance_asset']+x['plan_funds'],x['deferred_comp_assets']);eq('cash_after_extended_andSBC',a['cash_quality']['after_extended_equipment_and_SBC_sensitivity'],352.079)
test('intangible_current_unknown',h['TTM_September_2026']['intangible_cash_capex'] is None);test('allin_current_unknown',a['cash_quality']['all_in_FCF'] is None)
c=json.loads((p/'comparables/outputs.json').read_text());eq('TXN_reportedFCF',c['TXN']['ttm_company_fcf_reconcile'],8422);eq('TXN_withoutCHIPS',c['TXN']['ttm_no_CHIPS_sensitivity'],6849);eq('ADI_cash',c['ADI']['cfo_less_ppe'],1458.297)
for v in pub['pros_es']+pub['cons_es']:test('spanish_evidence_'+str(len(q)),v in (p/'report.md').read_text())
for v in pub['pros_en']+pub['cons_en']:test('english_evidence_'+str(len(q)),v in (p/'english_evidence.md').read_text())
test('history_checks',all(v['result']=='PASS' for v in json.loads((p/'history/validation_checks.json').read_text())))
o={'checks':len(q),'passed':sum(v['pass'] for v in q),'failed':[v for v in q if not v['pass']],'results':q};(p/'qa.json').write_text(json.dumps(o,indent=2)+'\n');assert not o['failed'],o['failed'];print(len(q),'QA passed')
