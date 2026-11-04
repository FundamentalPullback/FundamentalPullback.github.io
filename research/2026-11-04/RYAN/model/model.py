import json,copy
from pathlib import Path
p=Path(__file__).parent;i=json.loads((p/'inputs.json').read_text())
def calc(case='base',over=None):
 s=copy.deepcopy(i['scenarios'][case]);s.update(over or {});rev=i['revenue'];np=(i['ebitBeforeDisclosedIntangibleAmortExRemeasurement']-s.get('reversalNormalization',i['selectedReversalNormalization']))*(1-s['tax']);rows=[]
 for y in range(1,11):
  g=s['growth'][y-1] if y<=5 else s['growth'][-1]+(s['tg']-s['growth'][-1])*(y-5)/5;m=(s['margin'][y-1] if y<=5 else s['margin'][-1])+s.get('marginShift',0);r=rev*(1+g);n=r*m*(1-s['tax']);da=i['depreciation']*r/i['revenue'];capex=max(1.25*da,s['capexFloor']*r/i['revenue']);wc=max(0,s['wc']*(r-rev));physical=capex-da+wc;economic=max(0,n-np)/s['roic'] if not s.get('efficiency',False) else max(0,np*g)/s['roic'];ri=max(physical,economic,0);f=n-ri
  rows.append(dict(year=y,revenue=r,growth=g,margin=m,ebitBeforeIntangibleAmort=r*m,nopat=n,depreciation=da,capex=capex,wc=wc,physicalFloor=physical,economicFloor=economic,reinvestment=ri,fcff=f,pv=f/(1+s['discount'])**y));rev=r;np=n
 g=s['tg'];r=rev*(1+g);n=r*(s['margin'][-1]+s.get('marginShift',0))*(1-s['tax']);da=i['depreciation']*r/i['revenue'];physical=max(1.25*da,s['capexFloor']*r/i['revenue'])-da+s['wc']*rev*g;economic=n*g/s['roic'];ri=max(physical,economic,0);f=n-ri;tv=f/(s['discount']-g)/(1+s['discount'])**10;ev=sum(x['pv'] for x in rows)+tv
 awards=s.get('awards',i['selectedAwards']);a=i['classA']+awards*s.get('awardShareA',1);u=i['classA']+i['noncontrollingUnitsProxy']+awards
 # Repurchase cash timing and legal-entity funding are not fully reconciled. Stress allocation, never omit cash outflow.
 alloc=s.get('repurchaseParentFraction',1);opco= -s.get('legacyEmployeeReserve',i['legacyDeferredComp']+i['legacyAcquisitionIncentiveLiability'])+s.get('investmentCredit',0)+i['opcoCash']-s.get('operatingReserve',i['selectedOpcoOperatingReserve'])-i['opcoDebtPrincipal']-i['accruedInterestFees']-s.get('earnout',i['contingentLiability'])+i['contingentAsset']-i['postSeptemberRepurchaseCash']*(1-alloc)-i['declaredTaxDistributionsOpco']-i['selectedLegacyUnitDistributionReserve']-s.get('unitDistribution',i['selectedFutureUnitDistribution'])*i['noncontrollingUnitsProxy']
 parent=i['parentCash']-i['postSeptemberRepurchaseCash']*alloc-i['parentApAndOtherLiabilities']-s.get('tra',i['parentTra'])+s.get('dtaCredit',0)-i['exciseTaxReserveParent']-i['nextDividendA']*i['classA']
 residual=(ev+opco)/u+parent/a
 return dict(case=case,assumptions=s,rows=rows,terminal=dict(revenue=r,nopat=n,depreciation=da,physicalFloor=physical,economicFloor=economic,reinvestment=ri,fcff=f,pv=tv),ev=ev,parentBridge=parent,opcoBridge=opco,classAProxy=a,allEconomicUnitsProxy=u,conditionalClassAResidual=residual,terminalShare=tv/ev,peakFunding=max(0,-min(sum(x['fcff'] for x in rows[:k]) for k in range(1,11))))
def inverse(eff=False):
 lo=-.15;hi=.8;fn=lambda x:calc('base',{'marginShift':x,'efficiency':eff})['conditionalClassAResidual']-i['close'];assert fn(lo)*fn(hi)<0
 z=[fn(lo+(hi-lo)*k/1000) for k in range(1001)];assert all(b>a for a,b in zip(z,z[1:]))
 for _ in range(100):
  mid=(lo+hi)/2
  if fn(mid)>0:hi=mid
  else:lo=mid
 x=(lo+hi)/2;o=calc('base',{'marginShift':x,'efficiency':eff});assert abs(fn(x))<1e-7
 return dict(marginShiftPp=x*100,terminalMargin=o['assumptions']['margin'][-1]+x,firstFcff=o['rows'][0]['fcff'],peakFunding=o['peakFunding'],residual=fn(x),monotonicIntervals=1000,efficiency=eff)
o={'cases':{k:calc(k) for k in i['scenarios']},'inverseFinanced':inverse(),'inverseEfficiency':inverse(True),'sensitivities':{}}
for k,vs in {'discount':[.08,.09,.095,.10,.11],'tg':[.015,.02,.025,.03],'roic':[.15,.20,.25],'tax':[.21,.26,.30],'capexFloor':[70,100,150],'wc':[0,.10,.20],'awards':[0,10,12,16],'awardShareA':[0,.5,1],'repurchaseParentFraction':[0,.5,1],'earnout':[99.456,200,500.2],'dtaCredit':[0,125.6,251.2],'tra':[0,485.088,727.632],'operatingReserve':[0,100,123.311,200],'unitDistribution':[0,.06,.13],'reversalNormalization':[0,9.221,18.442],'legacyEmployeeReserve':[0,72.8,103.258],'investmentCredit':[0,47,109.9],'marginShift':[-54.295/3253.052,-27.1475/3253.052,0]}.items():o['sensitivities'][k]=[dict(input=v,value=calc('base',{k:v})['conditionalClassAResidual']) for v in vs]
checks=0
for q in o['cases'].values():
 for r in q['rows']:
  assert abs(r['nopat']-r['reinvestment']-r['fcff'])<1e-8;assert r['reinvestment']>=max(r['physicalFloor'],r['economicFloor']);assert r['capex']>=1.25*r['depreciation'];checks+=3
 assert q['terminal']['reinvestment']>=max(q['terminal']['physicalFloor'],q['terminal']['economicFloor']);checks+=1
 assert abs(q['conditionalClassAResidual']-((q['ev']+q['opcoBridge'])/q['allEconomicUnitsProxy']+q['parentBridge']/q['classAProxy']))<1e-8;checks+=1
(p/'results.json').write_text(json.dumps(o,indent=2,sort_keys=True)+'\n');(p/'qa.json').write_text(json.dumps({'checks':checks,'allPass':True},indent=2)+'\n');print({k:v['conditionalClassAResidual'] for k,v in o['cases'].items()},o['inverseFinanced'])
