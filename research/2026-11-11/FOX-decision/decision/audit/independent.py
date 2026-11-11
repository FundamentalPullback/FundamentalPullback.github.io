import json,math
from pathlib import Path
B=Path(__file__).resolve().parents[1];l=json.load(open(B/'legacy_inputs.json'));o=json.load(open(B/'results.json'));n=0

def ck(a,b):
 global n
 assert math.isclose(a,b,rel_tol=1e-10,abs_tol=1e-9),(a,b)
 n+=1
claims=6.65+10.4-2.894+1.333+.5+.264-.335*.75
cash=.153316257*.70;sharesadd=.153316257*.0106
ck(claims,o['claims']);ck(cash,o['terms_cash_adjustment']);ck(sharesadd,o['terms_share_adjustment'])
values={}
for grp in ['cases','sensitivities']:
 for name,v in o[grp].items():
  c=l[v['case']];old=c['Closes'];w=v['rate'];g=c['g']
  delta=0 if v['legacy'] else c['roku_rev'][0]/2*(c['roku_margin'][0]*(1-.25)+.01-.012-.007)
  flows=[f-v['synergy_cut']*c['synergy']*.75*([.25,.5]+[1]*8)[i]+(delta if i==0 else 0) for i,f in enumerate(old['FCFF'])]
  for i,f in enumerate(flows):ck(f,v['fcff'][i]);ck(f/(1+w)**(i+1),v['pvs'][i])
  terminal=old['terminal_FCFF']-v['synergy_cut']*c['synergy']*.75*(1+g)*(1-g/c['roic'])
  tv=terminal/((w-g)*(1+w)**10);ev=sum(f/(1+w)**(i+1) for i,f in enumerate(flows))+tv
  cl=-old['bridge'] if v['legacy'] else claims-(cash if v['terms'] else 0)
  sh=old['shares'] if v['legacy'] else .580513853+(sharesadd if v['terms'] else 0)
  if name=='central_issued_share_proxy':sh=.428036905+.1445+.0038675
  tax=0 if v['zero_taxasset'] else c['taxasset'];eq=ev-cl-v['extra_claim']+tax
  for key,val in dict(firstperiod_increment=delta,terminal_fcff=terminal,terminal_pv=tv,ev=ev,claims=cl,shares=sh,taxasset=tax,equity=eq,value=eq/sh).items():ck(val,v[key])
  if v['legacy']:ck(eq/sh,old['per_share'])
  values[name]=eq/sh
json.dump(dict(status='PASS',comparisons=n,cases=len(o['cases']),sensitivity_count=len(o['sensitivities']),legacy_tieouts=3,values=values),open(B/'audit/output.json','w'),indent=2)
print(n)
