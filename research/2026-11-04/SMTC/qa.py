import pathlib,json,math
p=pathlib.Path(__file__).parent;a=json.loads((p/'analysis.json').read_text());x=json.loads((p/'facts/capital_guidance.json').read_text());h={r['period']:r for r in json.loads((p/'history/financial_history.json').read_text())['periods']};pub=json.loads((p/'publication.json').read_text());checks=[]
def test(k,v):checks.append({'check':k,'pass':bool(v)})
def eq(k,a,b):test(k,abs(a-b)<1e-6)
for k in ['bear','base','bull','owner_fcf','equity_bridge','buy_ceiling']:test('null_'+k,a[k] is None and pub[k] is None)
for k in ['stage35_approved','approved_entry']:test(k,not a[k] and not pub[k])
test('latest_completed_not_set',not pub['latestCompleted']);eq('debt_503',a['capital_arithmetic_not_certified_bridge']['nominal_debt'],503);eq('cost_bridge',a['capital_arithmetic_not_certified_bridge']['book_debt']+x['debt_costs'],503);eq('cash_net_debt',a['capital_arithmetic_not_certified_bridge']['nominal_net_debt'],298.949);eq('held_sale_net',a['capital_arithmetic_not_certified_bridge']['held_for_sale_net_book_assets'],61.542);eq('shares_components',a['capital_arithmetic_not_certified_bridge']['q2_diluted_share_reconciliation'],100.841);eq('utp_reconcile',x['utp_offset_DTA']+x['utp_liability'],x['utp_total']);eq('revolver_net',x['credit_capacity']-x['letters_of_credit'],x['undrawn_revolver']);eq('q2ebit',h['Q2FY27']['ebit'],55.772);eq('q2tax',h['Q2FY27']['tax_expense'],-101.361)
t=h['TTM_Q2FY27'];eq('ttm_fcf',t['cfo']-t['capex_ppe'],193.108);eq('ttm_all_capex',t['cfo']-t['capex_ppe']-t['capex_intangibles'],183.879);eq('sbc_sensitivity',t['fcf_ppe_and_intangibles']-t['sbc_cf'],99.996)
for r in h.values():
 eq(r['period']+'_cash',r['cfo']-r['capex_ppe'],r['fcf_ppe'])
for text in pub['pros_es']+pub['cons_es']:test('excerpt_'+str(len(checks)),text in (p/'report.md').read_text())
for text in pub['pros_en']+pub['cons_en']:test('english_excerpt_'+str(len(checks)),text in (p/'english_evidence.md').read_text())
test('history_checks_pass',json.loads((p/'history/qa_summary.json').read_text())['fail']==0)
q={'checks':len(checks),'passed':sum(c['pass'] for c in checks),'failed':[c for c in checks if not c['pass']],'results':checks};(p/'qa.json').write_text(json.dumps(q,indent=2)+'\n');assert not q['failed'],q['failed'];print(q['checks'],'QA passed')
