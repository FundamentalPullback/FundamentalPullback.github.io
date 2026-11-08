import pathlib,json
P=pathlib.Path(__file__).resolve().parent
h=json.loads((P/'history.json').read_text());s=json.loads((P/'status.json').read_text());checks={}
for k in ['revenue','ebit','cfo']:
 checks['Quarterly TTM bridge '+k]=abs(sum(q[k] for q in h['quarters'].values())-h['paired_ttm_july']['2026'][k])<1e-7
checks['No approved value']=s['approved_values'] is None
assert all(checks.values())
(P/'public_checks.json').write_text(json.dumps(checks,indent=2))
