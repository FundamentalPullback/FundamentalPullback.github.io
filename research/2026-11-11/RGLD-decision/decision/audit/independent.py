import json
from pathlib import Path
P=Path(__file__).resolve().parents[1];r=json.loads((P/'results.json').read_text());checks=[]
def check(a,b):
 assert abs(a-b)<1e-9,(a,b)
 checks.append([a,b])
bridge=184.538-150+46.1-50+233.875+70-45.807-69.211-46.1-50
shares=84.493627+.270170
check(bridge,r['net_bridge'])
check(bridge,184.538-150+46.1-50-50+233.875+70-45.807-115.311)
def value(w,repl,g=.02,metal=1,margin=.65,roic=.12):
 v=1859.064*metal;pv=0
 for t in range(1,11):
  q=g if t<=5 else g+(.02-g)*(t-5)/5
  nv=v*(1+q)
  cf=nv*(margin*.78+.18-repl)-max(0,nv-v)*margin*.78/roic
  pv+=cf*(1+w)**(-t);v=nv
 terminal=v*1.02*(margin*.78*(1-.02/roic)+.18-repl)
 return (pv+terminal/(w-.02)*(1+w)**-10+bridge)/shares
for k,b in [('raw_beta',.46),('shrunk_beta',.64)]:
 w=.0498+b*.0441;check(w,r['rates'][k])
 for x,target in r['grid'][k].items():check(value(w,float(x)),target)
check(value(.070086,.18,.035,1.1,.67,.15),r['favorable_updated_rate'])
check((value(.070086,0)/274.57-1)*100,r['zero_replacement_raw_discount_pct'])
(P/'audit/output.json').write_text(json.dumps({'status':'PASS','checks':len(checks),'method':'Independent FCFF equations and bridge arithmetic, no production import','zero_replacement_raw':value(.070086,0),'notes':['Warintza reserve replaced by paid cash once; no change in net bridge','Old dated capital bridge, not current cash certification','Zero replacement produces negative net reinvestment terminal, deliberately non-sustainable counterfactual, not global price ceiling','Rate reference4.98 primary verified, ERP4.41 assumption; historical beta does not certify forward risk']},indent=2)+'\n')
print('PASS',len(checks))
