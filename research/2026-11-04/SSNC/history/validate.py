import json,pathlib,math
p=json.load(open(pathlib.Path(__file__).parent/'history.json'))['periods']
for n,d in p.items():
 assert abs(d['fcf_strict']-(d['cfo']-d['ppe_capex']-d['software_capex']))<.0001,n
 assert abs(d['fcf_after_sbc_diagnostic']-(d['fcf_strict']-d['sbc']))<.0001,n
 if d['acquired_amortization'] is not None:assert abs(d['da']-d['acquired_amortization']-d['software_amortization']-d['depreciation'])<.11,n
for key in ['revenue','ebit_gaap','net_income_parent','cfo','ppe_capex','software_capex','fcf_strict']:
 assert abs(sum(p[q][key] for q in ['Q42025','Q12026','Q22026','Q32026'])-p['TTM092026'][key])<.11,key
assert p['TTM092026']['acquired_amortization'] is None
print('PASS: FCF identities, D&A splits, last-four-quarter/TTM reconciliation, and missing split guard.')
