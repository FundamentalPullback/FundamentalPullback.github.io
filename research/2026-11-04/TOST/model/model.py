import json,copy,math
from pathlib import Path
P=Path(__file__).parent
I=json.loads((P/'inputs.json').read_text())
def calc(name='base',over=None):
 s=copy.deepcopy(I['scenarios'][name]);s.update(over or {});rev=I['revenue'];nopat=I['normalizedEbitBeforeAcquiredAmort']*(1-s['tax']);loan=I['loanAsset'];comm=I['commissionAsset'];rows=[]
 for y in range(1,11):
  g=s['growth'][y-1] if y<=5 else s['growth'][-1]+(s['terminalGrowth']-s['growth'][-1])*(y-5)/5
  margin=(s['margins'][y-1] if y<=5 else s['margins'][-1])+s.get('marginShift',0)
  newrev=rev*(1+g);ebit=newrev*margin;newnopat=ebit*(1-s['tax']);da=newrev*s['da'];capex=newrev*s['capex'];cap_sbc=newrev*s['capitalizedSbc']
  # Funding starts from observable stock; transition to stable asset/revenue at year10.
  w=1 if y<=5 else (10-y)/5
  loanfund=w*newrev*s['loanFunding']+(1-w)*loan*g
  commfund=w*newrev*s['commissionFunding']+(1-w)*comm*g
  wc=s['workingCapital']*(newrev-rev)
  physical=capex-da+cap_sbc+loanfund+commfund+wc
  economic=max(0,newnopat-nopat)/s['roic'] if not s.get('efficiencyMargin',False) else max(0,nopat*g)/s['roic']
  reinvest=max(physical,economic,0);fcff=newnopat-reinvest
  t=y # rolling annual periods from as-of date, not FY2027
  rows.append(dict(year=y,revenue=newrev,growth=g,margin=margin,ebit=ebit,nopat=newnopat,da=da,capex=capex,capitalizedSbc=cap_sbc,loanFunding=loanfund,commissionFunding=commfund,workingCapital=wc,physicalNetInvestment=physical,economicNetInvestment=economic,reinvestment=reinvest,fcff=fcff,pv=fcff/(1+s['discount'])**t))
  rev=newrev;nopat=newnopat;loan+=loanfund;comm+=commfund
 g=s['terminalGrowth'];r=rev*(1+g);n=r*(s['margins'][-1]+s.get('marginShift',0))*(1-s['tax']);phys=r*(s['capex']-s['da']+s['capitalizedSbc'])+loan*g+comm*g+s['workingCapital']*rev*g;econ=n*g/s['roic'];rein=max(phys,econ,0);f=n-rein;tv=f/(s['discount']-g);pvtv=tv/(1+s['discount'])**10;ev=sum(x['pv'] for x in rows)+pvtv
 bridge=I['cash']+I['securities']-s.get('operatingCashReserve',I['operatingCashReserve'])-I['warrantClaim']-I['historicalTaxReserve']-s.get('legalCashStress',0)+s.get('nolAdded',0)
 shares=s.get('shares',I['dilutedSharesProxy']);value=(ev+bridge)/shares
 return dict(scenario=name,assumptions=s,rows=rows,terminal=dict(revenue=r,nopat=n,physicalNetInvestment=phys,economicNetInvestment=econ,reinvestment=rein,fcff=f,value=tv,pv=pvtv,loanStockYear10=loan,commissionStockYear10=comm),enterpriseValue=ev,bridge=bridge,shares=shares,conditionalResidualPerShare=value,terminalPvFraction=pvtv/ev)
def inverse(eff=False):
 target=I['close'];lo=-.05;hi=.5
 fn=lambda x:calc('base',dict(marginShift=x,efficiencyMargin=eff))['conditionalResidualPerShare']-target
 assert fn(lo)*fn(hi)<0
 grid=[fn(lo+(hi-lo)*k/1000) for k in range(1001)]
 assert all(b>a for a,b in zip(grid,grid[1:])), 'inverse not strictly monotonic'
 for _ in range(100):
  m=(lo+hi)/2
  if fn(m)>0:hi=m
  else:lo=m
 x=(lo+hi)/2;o=calc('base',dict(marginShift=x,efficiencyMargin=eff));assert abs(fn(x))<1e-7
 return dict(marginShiftPp=x*100,terminalMargin=o['assumptions']['margins'][-1]+x,firstYearFcff=o['rows'][0]['fcff'],year10Revenue=o['rows'][-1]['revenue'],residualError=fn(x),efficiencyMargin=eff,monotonicGridChecks=1000,bracket=[-.05,.5])
out={'cases':{n:calc(n) for n in I['scenarios']},'inverseFinanced':inverse(),'inverseEfficiencyOnly':inverse(True),'sensitivities':{}}
for o in out['cases'].values():
 o['peakCumulativeCashDeficit']=max(0,-min(sum(r['fcff'] for r in o['rows'][:i]) for i in range(1,11)))
 o['selectedLiquidBridgeCoversModeledDeficit']=o['bridge']>=o['peakCumulativeCashDeficit']
for key,values in {'discount':[.105,.115,.125,.135,.145],'terminalGrowth':[.02,.025,.03,.035],'loanFunding':[0,.007,.014,.025],'commissionFunding':[.006,.012,.018],'operatingCashReserve':[300,500,800],'legalCashStress':[0,100,300,600],'shares':[595,I['dilutedSharesProxy'],614],'tax':[.21,.25,.28],'capitalizedSbc':[0,.0017,.003],'roic':[.15,.20,.25]}.items():
 out['sensitivities'][key]=[{'input':v,'value':calc('base',{key:v})['conditionalResidualPerShare']} for v in values]
out['sensitivities']['persistentLoansAndCommissions']=None # model uses explicit balance transition; see terminal stock rather than perpetual net originations.
out['sensitivities']['historicalNolUpperBound']={'amount':928*.21+873*.05+96,'value':calc('base',{'nolAdded':928*.21+873*.05+96})['conditionalResidualPerShare']}
out['sensitivities']['legalMarginMinus100bp']=calc('base',{'marginShift':-.01})['conditionalResidualPerShare']
checks=[]
for name,o in out['cases'].items():
 for r in o['rows']:
  assert abs(r['fcff']-(r['nopat']-r['reinvestment']))<1e-8;assert r['reinvestment']>=r['physicalNetInvestment']-1e-9;assert r['reinvestment']>=r['economicNetInvestment']-1e-9;checks.extend([True]*3)
 t=o['terminal'];assert t['reinvestment']>=max(t['physicalNetInvestment'],t['economicNetInvestment'])-1e-8;assert abs(o['enterpriseValue']-(sum(x['pv'] for x in o['rows'])+t['pv']))<1e-6;checks.extend([True]*2)
(P/'results.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');(P/'qa.json').write_text(json.dumps({'passed':len(checks),'allPass':all(checks)},indent=2)+'\n')
print({k:v['conditionalResidualPerShare'] for k,v in out['cases'].items()},out['inverseFinanced'])
