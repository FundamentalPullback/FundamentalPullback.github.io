"""Independent HRB equations; no import or execution of model.py."""
import json, pathlib
p=pathlib.Path(__file__).resolve().parents[1]
r=json.loads((p/'results.json').read_text())
e=50.99*124.5;d=1500
w=lambda b:((.0498+.0441*b)*e+.065*.75*d)/(e+d)
def valuation(c):
    revenue=3966.177
    discounted=[]
    for t in range(1,11):
        old=revenue
        growth=c['growth'] if t<=5 else c['growth']+(c['g']-c['growth'])*(t-5)/5
        revenue=c['year1rev'] if t==1 else old*(1+growth)
        margin=c['startmargin']+(c['endmargin']-c['startmargin'])*min((t-1)/4,1)
        profit=revenue*margin*(1-c['tax'])
        explicit=revenue*(c['capex']+c['acq']-c['da'])+(revenue-old)*c['wc']
        blend=max(0,(t-5)/5)
        cashflow=profit-explicit*(1-blend)-profit*growth/c['roic']*blend
        discounted.append(cashflow/(1+c['wacc'])**t)
    terminal=revenue*(1+c['g'])*c['endmargin']*(1-c['tax'])*(1-c['g']/c['roic'])/(c['wacc']-c['g'])/(1+c['wacc'])**10
    return (sum(discounted)+terminal-1500+c['cash_credit']-c['otherclaims'])/124.5
checks=[]
for k,v in r['cases'].items():
    actual=valuation(v['inputs']);checks.append({'case':k,'independent':actual,'saved':v['value'],'difference':actual-v['value']});assert abs(actual-v['value'])<1e-9
base=r['cases']['normalized_beta_base']['inputs']
rev=[]
for q in r['reverse']:
    c=base|{'wacc':q['wacc'],'startmargin':q['constant_margin'],'endmargin':q['constant_margin']}
    value=valuation(c); assert abs(value-50.99)<1e-8
    rev.append({'wacc':q['wacc'],'margin':q['constant_margin'],'independent_value':value})
assert abs(w(1)-r['wacc_normalized'])<1e-12
assert abs(w(.41)-r['wacc_observed'])<1e-12
out={'wacc_normalized':w(1),'wacc_observed':w(.41),'six_cases':checks,'four_inverse':rev,'status':'PASS'}
(pathlib.Path(__file__).parent/'independent_output.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
