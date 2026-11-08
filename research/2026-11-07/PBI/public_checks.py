import pathlib,json
P=pathlib.Path(__file__).parent
h=json.loads((P/'history.json').read_text());b=json.loads((P/'bank_primary_input.json').read_text());m=json.loads((P/'market.json').read_text());s=json.loads((P/'status.json').read_text());checks=[]
def ck(name,value):checks.append({'check':name,'passed':bool(value)})
ck('Three annual periods',len(h['annual'])==3);ck('Four quarters',len(h['quarters'])==4)
for key in ['revenue','pbt','net_income','cfo','da','sbc','capex','finance_asset_release','loan_cash','deposit_change','interest','pension_nonservice','other_expense','rd']:
 ck('Paired TTM quarterly bridge: '+key,abs(sum(x[key] for x in h['quarters'].values())-h['paired_ttm']['2026'][key])<1e-6)
ck('FDIC June date',b['REPDTE']=='20260630');ck('FDIC assets',b['ASSET']==796327);ck('FDIC deposits',b['DEP']==676387);ck('FDIC equity',b['EQ']==77408);ck('FDIC H1 income',b['NETINC']==21677)
ck('Dated price and capitalization pass',m['price']>=15 and m['cap']>=2000);ck('Dated EMA failure',not m['ema_pass']);ck('No approved value or entry',s['approved_values'] is None and s['approved_entry'] is None)
assert all(x['passed'] for x in checks)
(P/'public_checks.json').write_text(json.dumps(checks,indent=2))
