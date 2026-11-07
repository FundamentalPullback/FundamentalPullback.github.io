import json,pathlib,re
p=pathlib.Path(__file__).resolve().parent
x=json.loads((p/'derived_inputs_and_model.json').read_text());h=x['historical'];q=['Q42025','Q12026','Q22026','Q32026'];checks=x['checks'].copy()
for k in ['ebit','net_income','da','sbc','capex','fcf']:
 checks['quarter_sum_'+k]=abs(sum(h[z][k] for z in q)-h['TTM2026'][k])<1e-6
checks['ledger_public_fields_only']=all(set(z)=={'url','title','date','purpose'} and z['url'].startswith('https://') for z in json.loads((p/'source_ledger.json').read_text()))
checks['report_no_private_paths']=not bool(re.search(r'/workspace/|/tmp/|/home/|sha256|file_size', (p/'report.md').read_text()))
checks['sensitivity_wacc_monotonic']=all(x['sensitivities'][i]['value']>x['sensitivities'][i+4]['value'] for i in range(16))
checks['terminal_fcf_nonnegative']=all(c['rows'][-1]['fcff']>=0 for c in x['cases'].values())
checks['report_main_values']=all(f"${x['cases'][case]['value']:.2f}" in (p/'report.md').read_text() for case in ['bear','base','bull'])
qa=json.loads((p/'qa.json').read_text());qa['checks']=checks;qa['hard_failures']=[k for k,v in checks.items() if not v];qa['review']='Numeric tie-outs, source-field privacy, terminal funding, scenario ordering and disclosure QA completed. No remote publication performed.';(p/'qa.json').write_text(json.dumps(qa,indent=2));print(json.dumps(qa,indent=2));assert not qa['hard_failures']
# Additional release checks preserve all preceding numerical checks.
text=(p/'report.md').read_text()
checks['inverse_brackets_target']=x['reverse_dcf']['qa']['target_bracketed']
checks['inverse_grid_monotonic']=x['reverse_dcf']['qa']['strictly_monotonic']
checks['inverse_residual']=abs(x['reverse_dcf']['qa']['residual'])<1e-8
checks['no_stage3_or_entry_approval']=x['stage3_complete'] is False and x['entry_approved'] is False
checks['approved_values_unset']=all(x[k] is None for k in ['approved_value','approved_target','approved_entry','approved_stop','approved_quantity'])
checks['eps_proxy_not_quarter_sum']=abs(h['TTM2026']['eps']-7.97)<1e-8 and abs(sum(h[z]['eps'] for z in q)-8)<1e-8 and 'It is not a sum of quarterly EPS' in text
checks['literal_primary_excerpts_in_report']=all(e['quote'] in text for e in json.loads((p/'contiguous_evidence.json').read_text()))
checks['historical_multiple_gap_disclosed']='homogeneous historical EPAM/peer' in text
checks['no_stub_convention_disclosed']='No partial-year stub' in text
checks['no_library_workflow_narration']='library was checked' not in text
qa['checks']=checks;qa['hard_failures']=[k for k,v in checks.items() if not v];(p/'qa.json').write_text(json.dumps(qa,indent=2));assert not qa['hard_failures'];print('Final release checks:',len(checks),'passed')
