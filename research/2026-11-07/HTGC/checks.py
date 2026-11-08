import pathlib,json,csv
p=pathlib.Path(__file__).parent;h=json.loads((p/'history.json').read_text());r=json.loads((p/'results.json').read_text());s=json.loads((p/'status.json').read_text());a=list(csv.DictReader((p/'model_schedule.csv').open()))
for k in ['investment_income','nii','pik','realized','unrealized','net_income']:assert abs(sum(x[k] for x in h[3:7])-h[7][k])<1e-7
for x in a:
 assert abs(float(x['cash_residual']))<1e-8
 assert abs(float(x['nav_open'])+float(x['nii'])-float(x['loss'])-float(x['dividend'])-float(x['nav_end']))<1e-8
for v in r['cases'].values():assert abs(v['conditional_value']-v['ri_crosscheck'])<1e-7 and v['ke']>v['terminal_g_funded']
assert r['approved_value'] is None and s['approved_entry'] is None
assert s['dividend']['quote_is_cum_dividend'] and s['dividend']['ex_record']=='2026-11-10'
print('PASS TTM, funded capital, cash identity, dividend/RI equivalence, cum-dividend and null approvals.')
