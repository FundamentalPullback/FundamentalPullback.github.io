import json,math
from pathlib import Path
D=Path(__file__).resolve().parent.parent
expected=json.loads((D/'results.json').read_text())
# Independent implementation; no production module import. Literal dated anchor and bridge.
def value(a):
 r=7152.; n=508*(1-a['tax']); c=294.; l=0. if a.get('separateHfi') else 70.; pv=0.; cumulative=0.; deficit=0.; rows=[]
 for t in range(10):
  yr=t+1
  g=a['growth'][t] if t<5 else a['growth'][4]*(9-t)/5+a['terminalGrowth']*(t-4)/5
  m=a['margins'][min(t,4)]+a.get('marginShift',0)
  rn=r*(1+g); nn=rn*m*(1-a['tax'])
  mix=1 if t<5 else (9-t)/5
  dc=mix*rn*a['commissionFunding']+(1-mix)*c*g
  dl=0 if a.get('separateHfi') else mix*rn*a['loanFunding']+(1-mix)*l*g
  physical=rn*(a['capex']-a['da']+a['capitalizedSbc'])+dc+dl+a['workingCapital']*(rn-r)
  econ=max(0,n*g if a.get('efficiencyMargin') else nn-n)/a['roic']
  spend=max(0,physical) if a.get('bottomUpOnly') else max(0,physical,econ)
  f=nn-spend;pv+=f/(1+a['discount'])**yr;cumulative+=f;deficit=max(deficit,-cumulative);rows.append(f)
  r,n,c,l=rn,nn,c+dc,l+dl
 g=a['terminalGrowth']; rn=r*(1+g); nn=rn*(a['margins'][4]+a.get('marginShift',0))*(1-a['tax'])
 p=rn*(a['capex']-a['da']+a['capitalizedSbc'])+g*(l+c)+a['workingCapital']*r*g
 inv=max(0,p) if a.get('bottomUpOnly') else max(0,p,nn*g/a['roic'])
 terminal=(nn-inv)/(a['discount']-g)/(1+a['discount'])**10
 ev=pv+terminal
 bridge=1885-a.get('operatingCashReserve',500)-13-7-a.get('legalCashStress',0)+a.get('nolAdded',0)+(70*(1-a.get('hfiHaircut',0)) if a.get('separateHfi') else 0)
 shares=a.get('shares',581+14+19*(1-13.98/34.52))
 return {'value':(ev+bridge)/shares,'enterpriseValue':ev,'bridge':bridge,'peak_deficit':deficit,'first_fcff':rows[0],'rows':rows,'terminal_pv':terminal}
checks=[]
def check(label,x,y):
 assert math.isclose(x,y,rel_tol=1e-10,abs_tol=1e-7),(label,x,y)
 checks.append({'label':label,'independent':x,'expected':y,'pass':True})
check('observedrate',.0498+1.71*.0441,expected['rates']['observed_discount'])
check('normalizedrate',.0498+.0441,expected['rates']['normalized_discount'])
check('shares',581+14+19*(1-13.98/34.52),expected['shares_proxy'])
for k,v in expected['cases'].items():
 o=value(v['assumptions'])
 for field,ref in [('value','conditionalResidualPerShare'),('enterpriseValue','enterpriseValue'),('bridge','bridge'),('peak_deficit','peakCumulativeCashDeficit')]:check(k+':'+field,o[field],v[ref])
 for t,row in enumerate(v['rows']):check(k+':fcff'+str(t+1),o['rows'][t],row['fcff'])
base=expected['cases']['central_separate_hfi']['assumptions']
for key,values in expected['sensitivities'].items():
 for v in values:
  a=dict(base);a[key]=v['input']
  if key=='loanFunding':a['separateHfi']=False
  check('sensitivity:'+key+':'+str(v['input']),value(a)['value'],v['value'])
inverses={}
for key,v in expected['inverses'].items():
 a=dict(base)
 if key=='normalized_bottomup':a['discount']=.0939
 if key in ('observed_economic','observed_efficiency'):a['bottomUpOnly']=False
 if key=='observed_efficiency':a['efficiencyMargin']=True
 def fun(z):return value(dict(a,marginShift=z))['value']-34.52
 grid=[fun(-.05+.55*i/1000) for i in range(1001)]
 assert grid[0]<0<grid[-1] and all(y>x for x,y in zip(grid,grid[1:]))
 low,high=-.05,.5
 for _ in range(100):
  z=(low+high)/2
  if fun(z)>0:high=z
  else:low=z
 z=(low+high)/2;o=value(dict(a,marginShift=z))
 check(key+':root',z,v['margin_shift']);check(key+':firstfcff',o['first_fcff'],v['first_fcff']);check(key+':deficit',o['peak_deficit'],v['peak_deficit'])
 inverses[key]={'margin_shift':z,'terminal_margin':.125+z,'first_fcff':o['first_fcff'],'peak_deficit':o['peak_deficit'],'residual':fun(z),'monotonic_intervals':1000}
(Path(__file__).parent/'output.json').write_text(json.dumps({'checks_count':len(checks),'all_pass':True,'checks':checks,'inverses':inverses},indent=2))
print('PASS',len(checks),'checks, 4000 monotonic intervals'); print(inverses)
