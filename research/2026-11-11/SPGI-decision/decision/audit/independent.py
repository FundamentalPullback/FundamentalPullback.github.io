import pathlib,json,math
P=pathlib.Path(__file__).resolve().parents[1];L=json.load(open(P/'legacy.json'));R=json.load(open(P/'results.json'));n=0
def eq(a,b):
 global n
 assert math.isclose(a,b,rel_tol=1e-9,abs_tol=1e-7),(a,b)
 n+=1
def v(m,r,c=0,s=None):
 g=m['parameters']['g'];annual=[x['fcff'] for x in m['rows']];end=m['terminal_value']*(m['parameters']['wacc']-g);ev=sum((x-c)/(1+r)**t for t,x in enumerate(annual,1))+(end-c*(1+g))/(r-g)/(1+r)**10
 return ev,(ev-m['net_claims'])/(s or m['shares'])
for k,z in R['legacyTieouts'].items():
 m=L['models'][k];a,b=v(m,z['wacc']);eq(a,z['enterprise_value']);eq(b,z['price'])
m=L['models']['base'];a=R['rateInputs'];w=(a['marketEquityProxy']*(a['riskFree']+a['ERP']*a['beta'])+a['bookDebtProxy']*a['costDebtAssumed']*(1-a['tax']))/(a['marketEquityProxy']+a['bookDebtProxy']);eq(w,a['wacc'])
for k,z in R['rateScenarios'].items():
 ev,p=v(m,z['wacc']);eq(ev,z['enterprise_value']);eq(p,z['price'])
for k,z in R['cashDrag'].items():
 ev,p=v(m,w,float(k));eq(ev,z['enterprise_value']);eq(p,z['price'])
eq(v(m,w,s=289.9)[1],R['sharesSensitivity']['price']);eq(v(m,R['priceImpliedWacc'])[1],R['price'])
prev=None
for i in range(1001):
 r=.04+.16*i/1000;p=v(m,r)[1]
 if prev is not None:assert p<prev
 prev=p
json.dump({'status':'PASS','arithmetic_checks':n,'monotonic_intervals':1000,'wacc':w,'inverse_wacc':R['priceImpliedWacc'],'production_imported':False},open(P/'audit/output.json','w'),indent=2)
print(n,'PASS')
