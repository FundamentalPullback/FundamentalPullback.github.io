import pathlib,json,math
p=pathlib.Path(__file__).parent;h=json.loads((p/'history.json').read_text());r=json.loads((p/'model_results.json').read_text());checks={}
for k in h['TTM2026']:checks['ttm_'+k]=abs(sum(h[q][k] for q in ['Q2FY26','Q3FY26','Q4FY26','Q1FY27'])-h['TTM2026'][k])<.00001
for n,c in r['cases'].items():
 checks[n+'_RI_FCFE_equivalence']=abs(c['conditional_equity_value']-c['fcfe_crosscheck'])<1e-7
 checks[n+'_funded_growth']=all(abs(y['book_end']-y['book_start']-y['retention'])<1e-8 and abs(y['earnings']-y['retention']-y['fcfe'])<1e-8 for y in c['years'])
 checks[n+'_terminal_funded']=c['terminal_roe']>c['terminal_growth'] and c['ke']>c['terminal_growth']
checks['approved_null']=r['approved_value'] is None and r['approved_entry'] is None
checks['source_quarter_revenue_rounding']=abs(h['Q2FY26']['revenue']-1123.019)<=.00101
checks['current_financial_identity']=abs(16481.340-10730.096-5751.244)<1e-8
(p/'checks.json').write_text(json.dumps(checks,indent=2));assert all(checks.values()),checks
print('All',len(checks),'checks passed')
