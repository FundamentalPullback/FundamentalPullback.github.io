import json,math
from pathlib import Path
D=Path(__file__).resolve().parent.parent; E=json.loads((D/'results.json').read_text()); P=E['inputs']; paths=E['paths']
def independently(a):
 q=paths[a['path']]; mk=2767*a['fx']; jc=632*a['fx']; prev=mk+jc; pv=0; cumulative=0; peak=0; rows=[]
 for t in range(10):
  k=min(t,4); w=max(0,t-4)/5
  mk*=1+q['mkg'][k]*(1-w)+.025*w;jc*=1+q['jcg'][k]*(1-w)+.025*w
  sales=mk+jc
  corp=q['corp'][k]+a.get('corpExtra',0)
  op=mk*q['mkm'][k]+jc*q['jcm'][k]-sales*corp+sales*a['shift']; n=op*(1-a['tax']) if op>0 else op
  invest=(a['capex']-.03)*sales+a['nwc']*max(0,sales-prev); cf=n-invest
  cumulative+=cf;peak=max(peak,-cumulative);pv+=cf/(1+a['rate'])**(t+1);rows.append(cf);prev=sales
 termn=n*1.025; ti=max((a['capex']-.03)*sales*1.025+a['nwc']*sales*.025,max(0,termn)*.025/.12)
 tf=termn-ti;tpv=tf/(a['rate']-.025)/(1+a['rate'])**10; ev=pv+tpv;bridge=125-a['reserve']-461-a['hedge']-5-a['claims']
 return dict(ev=ev,bridge=bridge,equity=ev+bridge,value_raw=(ev+bridge)/a['shares'],peak_operating_deficit=peak,terminal_fcff=tf,terminal_pv=tpv,rows=rows,terminal_margin=op/sales)
checks=[]
def chk(label,x,y):
 assert math.isclose(x,y,abs_tol=1e-7,rel_tol=1e-10),(label,x,y)
 checks.append(dict(label=label,independent=x,expected=y,passed=True))
for section in ('cases','sensitivities'):
 for label,a in E[section].items():
  o=independently(a)
  for field in ('ev','bridge','equity','value_raw','peak_operating_deficit','terminal_fcff','terminal_pv'):chk(section+':'+label+':'+field,o[field],a[field])
  for i,r in enumerate(a['rows']):chk(label+':FCFF'+str(i+1),o['rows'][i],r['fcff'])
inverses=[]
for inv in E['inverses']:
 a=dict(E['cases']['central10']);a.update(path=inv['path'],rate=inv['rate'])
 def f(shift):return independently(dict(a,shift=shift))['value_raw']-21.73
 grid=[f(-.15+.65*i/1000) for i in range(1001)];assert grid[0]<0<grid[-1] and all(y>x for x,y in zip(grid,grid[1:]))
 lo,hi=-.15,.5
 for _ in range(100):
  mid=(lo+hi)/2
  if f(mid)>0:hi=mid
  else:lo=mid
 root=(lo+hi)/2;o=independently(dict(a,shift=root));chk(str(inv)+':root',root,inv['required_incremental_margin']);chk(str(inv)+':terminalmargin',o['terminal_margin'],inv['terminal_group_margin']);chk(str(inv)+':first',o['rows'][0],inv['first_fcff'])
 inverses.append(dict(path=a['path'],rate=a['rate'],root=root,margin=o['terminal_margin'],monotonic_intervals=1000,residual=f(root)))
(D/'audit/output.json').write_text(json.dumps(dict(all_pass=True,checks_count=len(checks),checks=checks,inverses=inverses),indent=2));print('PASS',len(checks),'checks; 3000 monotonicintervals')
