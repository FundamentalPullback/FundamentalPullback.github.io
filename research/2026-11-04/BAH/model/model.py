import json,copy
from pathlib import Path
P=Path(__file__).parent;I=json.loads((P/'inputs.json').read_text());B=json.loads((P.parent/'capital/verified.json').read_text())['selectedBridge']
def calc(case='base',ov=None):
 s=copy.deepcopy(I['scenarios'][case]);s.update(ov or {});rev=I['revenue'];np=I['ebitBeforeAcquiredAmort']*(1-s['tax']);rows=[]
 for y in range(1,11):
  g=s['growth'][y-1] if y<=5 else s['growth'][-1]+(s['tg']-s['growth'][-1])*(y-5)/5;m=(s['margin'][y-1] if y<=5 else s['margin'][-1])+s.get('marginShift',0);r=rev*(1+g);n=r*m*(1-s['tax']);da=r*I['physicalSoftwareDa']/I['revenue'];capex=max(da*1.25,s['capexFloor']*r/I['revenue']);wc=max(0,s['wc']*(r-rev)) # no assumed workingcapital release in contraction
  phy=capex-da+wc;econ=max(0,n-np)/s['roic'] if not s.get('efficiency',False) else max(0,np*g)/s['roic'];ri=max(phy,econ,0);f=n-ri
  rows.append(dict(year=y,revenue=r,margin=m,growth=g,ebitBeforeAcquiredAmort=r*m,nopat=n,physicalSoftwareDa=da,capex=capex,wc=wc,physicalFloor=phy,economicFloor=econ,reinvestment=ri,fcff=f,pv=f/(1+s['discount'])**y));rev=r;np=n
 g=s['tg'];r=rev*(1+g);n=r*(s['margin'][-1]+s.get('marginShift',0))*(1-s['tax']);da=r*I['physicalSoftwareDa']/I['revenue'];phy=max(1.25*da,s['capexFloor']*r/I['revenue'])-da+s['wc']*rev*g;ec=n*g/s['roic'];ri=max(phy,ec,0);f=n-ri;tv=f/(s['discount']-g)/(1+s['discount'])**10;ev=sum(x['pv'] for x in rows)+tv;bridge=B+s.get('assetCredit',0)+s.get('bridgeAdjustment',0);shares=s.get('shares',I['shares']);val=(ev+bridge)/shares
 return dict(case=case,assumptions=s,rows=rows,terminal=dict(revenue=r,nopat=n,physicalFloor=phy,economicFloor=ec,reinvestment=ri,fcff=f,pv=tv),ev=ev,bridge=bridge,shares=shares,conditionalResidual=val,terminalShare=tv/ev)
def inv(eff=False):
 lo=-.07;hi=.5;fn=lambda x:calc('base',{'marginShift':x,'efficiency':eff})['conditionalResidual']-I['close'];assert fn(lo)*fn(hi)<0
 grid=[fn(lo+(hi-lo)*k/1000) for k in range(1001)];assert all(b>a for a,b in zip(grid,grid[1:]))
 for _ in range(100):
  m=(lo+hi)/2
  if fn(m)>0:hi=m
  else:lo=m
 x=(lo+hi)/2;o=calc('base',{'marginShift':x,'efficiency':eff});assert abs(fn(x))<1e-7
 return dict(marginShiftPp=x*100,terminalMargin=o['assumptions']['margin'][-1]+x,firstFcff=o['rows'][0]['fcff'],residual=fn(x),monotonicChecks=1000,efficiency=eff)
out={'cases':{n:calc(n) for n in I['scenarios']},'inverseFinanced':inv(),'inverseEfficiency':inv(True),'sensitivities':{}}
for k,vs in {'discount':[.07,.08,.09,.10,.11],'tg':[.015,.02,.025,.03],'capexFloor':[100,200,300],'wc':[.06,.12,.18],'tax':[.19,.23,.26,.28],'roic':[.15,.20,.25],'assetCredit':[0,182,519,701],'bridgeAdjustment':[-171,-100,-53,0,249,334],'shares':[118.602638,120,122]}.items():out['sensitivities'][k]=[dict(input=v,value=calc('base',{k:v})['conditionalResidual']) for v in vs]
checks=[]
for o in out['cases'].values():
 for q in o['rows']:
  assert abs(q['fcff']-(q['nopat']-q['reinvestment']))<1e-8;assert q['reinvestment']>=max(q['physicalFloor'],q['economicFloor']);assert q['capex']>=1.25*q['physicalSoftwareDa'];checks.extend([True]*3)
 assert o['terminal']['reinvestment']>=max(o['terminal']['physicalFloor'],o['terminal']['economicFloor']);checks.append(True)
(P/'results.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');(P/'qa.json').write_text(json.dumps({'checks':len(checks),'allPass':True},indent=2)+'\n');print({n:o['conditionalResidual'] for n,o in out['cases'].items()},out['inverseFinanced'])
