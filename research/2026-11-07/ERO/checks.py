import json,csv,pathlib,math
p=pathlib.Path(__file__).parent;h=json.loads((p/'history.json').read_text());q=h[3:7];t=h[7]
for k in ['revenue','operating','net','parent_net','cfo','ppe','exploration']:
 assert abs(sum(x[k] for x in q)-t[k])<1e-7,(k,sum(x[k] for x in q),t[k])
assert h[1]['net']==-67.79
assert abs(t['cash_after_capex_interest_lease_other_and_advance_exclusion']-179.229)<1e-7
s=json.loads((p/'status.json').read_text());assert s['approved_value'] is None and s['whole_company_nav'] is None
r=json.loads((p/'finite_results.json').read_text());a=list(csv.DictReader((p/'finite_schedule.csv').open()))
for c in r['cases']:
 rows=[x for x in a if x['case']==c];assert [int(x['year']) for x in rows]==list(range(2027,2037));assert float(rows[-1]['payable_copper_mlb'])==0
 assert abs(sum(float(x['pv']) for x in rows)-r['cases'][c]['conditional_project_diagnostic_usdm'])<1e-6
print('PASS: financial TTM identity, finite schedule, no approved values, no perpetual terminal.')
