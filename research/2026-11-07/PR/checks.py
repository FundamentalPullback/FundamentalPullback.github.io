import pathlib,json,csv
p=pathlib.Path(__file__).parent;h=json.loads((p/'history.json').read_text());r=json.loads((p/'results.json').read_text());s=json.loads((p/'status.json').read_text())
for k in ['revenue','operating','net','parent_net','cfo','development','other_capex','acquisitions']:assert abs(sum(x[k] for x in h[3:7])-h[7][k])<1e-7,k
assert abs(h[6]['cfo_less_dev_othercapex']-718.992)<1e-7
for name,v in r['contracts_totals'].items():assert 0<=v['earnout']<=125
assert r['approved_value'] is None and r['current_corporate_nav'] is None and s['current_exact_net_debt'] is None
assert not s['price_above_ema50'] and s['ema20_above_50']
print('PASS: paired TTM, full capex cash bridge, capped contractual earnout, no fabricated NAV or current net debt.')
