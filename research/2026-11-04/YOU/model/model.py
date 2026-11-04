import json,copy
from pathlib import Path
P=Path(__file__).parent;I=json.loads((P/'inputs.json').read_text())
def calc(case='base',ov=None):
 s=copy.deepcopy(I['scenarios'][case]);s.update(ov or {});rev=I['revenue'];np=I['ebit']*(1-s['tax']);rows=[]
 for y in range(1,11):
  g=s['growth'][y-1] if y<=5 else s['growth'][-1]+(s['tg']-s['growth'][-1])*(y-5)/5
  m=(s['margin'][y-1] if y<=5 else s['margin'][-1])+s.get('marginShift',0);newrev=rev*(1+g);newnp=newrev*m*(1-s['tax']);da=newrev*s['da'];capex=max(1.25*da,newrev*s['capex']);wc=s['wc']*(newrev-rev);capsbc=newrev*s['capsbc'];phys=capex-da+wc+capsbc;econ=max(0,newnp-np)/s['roic'] if not s.get('efficiency',False) else max(0,np*g)/s['roic'];ri=max(phys,econ,0);fcf=newnp-ri
  rows.append(dict(year=y,revenue=newrev,growth=g,margin=m,ebit=newrev*m,nopat=newnp,da=da,capex=capex,capitalizedSbc=capsbc,wc=wc,physicalFloor=phys,economicFloor=econ,reinvestment=ri,fcff=fcf,pv=fcf/(1+s['discount'])**y));rev=newrev;np=newnp
 g=s['tg'];r=rev*(1+g);n=r*(s['margin'][-1]+s.get('marginShift',0))*(1-s['tax']);da=r*s['da'];phy=max(1.25*da,r*s['capex'])-da+r*s['capsbc']+s['wc']*rev*g;ec=n*g/s['roic'];ri=max(phy,ec,0);f=n-ri;pvterm=f/(s['discount']-g)/(1+s['discount'])**10;ev=sum(x['pv'] for x in rows)+pvterm
 # Parent-only claims must never be shared with existing noncontrolling units.
 a=I['classA']+s.get('awards',I['awards']);u=a+I['noncontrollingUnits'];alpha=a/u
 liquid=I['cashSecurities']-s.get('operatingCash',I['operatingCash'])-I['dividendPerUnit']*(I['classA']+I['noncontrollingUnits'])-s.get('legacyPartnerCashStress',0)
 parentCashShare=s.get('parentCashShare',alpha);parentCash=liquid*parentCashShare;opCash=liquid*(1-parentCashShare)
 # For proportional ownership default, all liquid amount is treated as OpCo, not split pro-rata twice.
 if 'parentCashShare' not in s:parentCash=0;opCash=liquid
 parentDta=s.get('parentDtaCredit',0);tra=s.get('parentTra',I['parentTra']);claim=(ev+opCash)/u+(parentCash+parentDta-tra)/a
 return dict(case=case,assumptions=s,rows=rows,terminal=dict(revenue=r,nopat=n,physicalFloor=phy,economicFloor=ec,reinvestment=ri,fcff=f,pv=pvterm),ev=ev,pvTerminalShare=pvterm/ev,classAWithAwards=a,economicUnits=u,selectedLiquid=liquid,parentCash=parentCash,opcoCash=opCash,parentTra=tra,parentDtaCredit=parentDta,conditionalClassAResidual=claim,peakFunding=max(0,-min(sum(x['fcff'] for x in rows[:k]) for k in range(1,11))))
def inverse(eff=False):
 lo=-.10;hi=1.;target=I['close'];fn=lambda x:calc('base',{'marginShift':x,'efficiency':eff})['conditionalClassAResidual']-target
 assert fn(lo)*fn(hi)<0
 grid=[fn(lo+(hi-lo)*i/1000) for i in range(1001)];assert all(b>a for a,b in zip(grid,grid[1:]))
 for _ in range(100):
  m=(lo+hi)/2
  if fn(m)>0:hi=m
  else:lo=m
 x=(lo+hi)/2;o=calc('base',{'marginShift':x,'efficiency':eff});assert abs(fn(x))<1e-7
 return dict(shiftPp=x*100,terminalMargin=o['assumptions']['margin'][-1]+x,firstFcff=o['rows'][0]['fcff'],peakFunding=o['peakFunding'],residual=fn(x),monotonicIntervals=1000,efficiency=eff)
out={'cases':{n:calc(n) for n in I['scenarios']},'inverseFinanced':inverse(),'inverseEfficiency':inverse(True),'sensitivities':{}}
for k,vs in {'discount':[.09,.10,.11,.12],'tg':[.02,.025,.03,.035],'wc':[-.10,0,.05,.10],'capex':[.025,.035,.05],'operatingCash':[100,200,315,400],'parentCashShare':[0,.5,1],'parentDtaCredit':[0,I['parentTra'],I['parentDta']],'parentTra':[0,I['parentTra'],I['parentTra']*1.5],'awards':[0,I['awards'],I['awards']*1.5],'legacyPartnerCashStress':[0,83.639,163.391],'tax':[.21,.25,.28],'roic':[.15,.20,.25]}.items():
 out['sensitivities'][k]=[dict(input=v,value=calc('base',{k:v})['conditionalClassAResidual']) for v in vs]
checks=[]
for o in out['cases'].values():
 for q in o['rows']:
  assert abs(q['fcff']-(q['nopat']-q['reinvestment']))<1e-8;assert q['reinvestment']>=max(q['physicalFloor'],q['economicFloor'])-1e-8;assert q['capex']>=1.25*q['da']-1e-8;checks.extend([True]*3)
 assert o['terminal']['reinvestment']>=max(o['terminal']['physicalFloor'],o['terminal']['economicFloor'])-1e-8;checks.append(True)
(P/'results.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');(P/'qa.json').write_text(json.dumps({'passed':len(checks),'allPass':True},indent=2)+'\n');print({n:o['conditionalClassAResidual'] for n,o in out['cases'].items()},out['inverseFinanced'])
