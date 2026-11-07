from pathlib import Path
import json,csv,math
from copy import deepcopy
P=Path(__file__).resolve().parents[1];h=json.loads((P/'history/periods.json').read_text())['TTM2026'];c=json.loads((P/'capital/inputs.json').read_text())
C={'bear':dict(growthStart=.03,growthEnd=.02,coreMarginStart=.23,coreMarginEnd=.22,floatFactor=.70,roic=.18,discount=.115,terminalGrowth=.02),'base':dict(growthStart=.07,growthEnd=.03,coreMarginStart=.29,coreMarginEnd=.30,floatFactor=.90,roic=.25,discount=.10,terminalGrowth=.025),'bull':dict(growthStart=.10,growthEnd=.04,coreMarginStart=.32,coreMarginEnd=.35,floatFactor=1.10,roic=.30,discount=.09,terminalGrowth=.03)}
COMMON=dict(tax=.28,grossCapitalResourceRate=.10,daRate=.09,contractAssetRatio=.48,otherWCIncrement=.02,stubYears=55/365,extraRecurringCost=0,bridgeDelta=0,shareFactor=1)
def model(case,**kw):
 a={**COMMON,**C[case],**kw};assert a['discount']>a['terminalGrowth'];rows=[];rev=h['recurring'];prevTotal=h['revenue'];prevN=h['ebit']*(1-a['tax']);float0=h['float_interest']*a['floatFactor'];flt=float0;pv=0
 for n in range(1,11):
  g=a['growthStart']+(a['growthEnd']-a['growthStart'])*(n-1)/9;margin=a['coreMarginStart']+(a['coreMarginEnd']-a['coreMarginStart'])*(n-1)/9
  old=rev;rev*=1+g;flt*=1+g;total=rev+flt;ebit=rev*margin+flt-a['extraRecurringCost']*(total/h['revenue']);nopat=ebit*(1-a['tax']);da=total*a['daRate'];gross=total*a['grossCapitalResourceRate'];contractNet=(rev-old)*a['contractAssetRatio'];wc=(total-prevTotal)*a['otherWCIncrement'];physical=max(0,gross-da+contractNet+wc);economic=max(0,(nopat-prevN)/a['roic']);net=max(physical,economic);fcff=nopat-net;disc=(1+a['discount'])**(n+a['stubYears']);pv+=fcff/disc
  rows.append(dict(year=2026+n,recurringRevenue=rev,floatRevenue=flt,totalRevenue=total,coreMargin=margin,ebit=ebit,nopat=nopat,da=da,grossCapitalResources=gross,netContractInvestment=contractNet,otherWCInvestment=wc,physicalNetFloor=physical,economicNetInvestment=economic,selectedNetInvestment=net,fcff=fcff,pv=fcff/disc));prevN=nopat;prevTotal=total
 g=a['terminalGrowth'];nt=nopat*(1+g);tt=total*(1+g);terminalPhysical=max(0,tt*(a['grossCapitalResourceRate']-a['daRate'])+rev*g*a['contractAssetRatio']+total*g*a['otherWCIncrement']);terminalEconomic=nt*g/a['roic'];terminalNet=max(terminalPhysical,terminalEconomic);terminalFCF=nt-terminalNet;tv=terminalFCF/(a['discount']-g);pvt=tv/(1+a['discount'])**(10+a['stubYears']);ev=pv+pvt;bridge=c['corporateCashSep30']-c['selectedOperatingCashReserve']-c['debtSep30']-c['selectedHistoricalTaxReserve']-c['selectedUpcomingDividendReserve']+a['bridgeDelta'];equity=ev+bridge;value=equity/(c['proxyDilutedShares']*a['shareFactor'])
 return dict(assumptions=a,years=rows,pvForecast=pv,pvTerminal=pvt,terminalFCF=terminalFCF,terminalNetInvestment=terminalNet,terminalPhysicalFloor=terminalPhysical,terminalEconomicFloor=terminalEconomic,enterpriseValue=ev,bridge=bridge,equityResidual=equity,illustrativePerShare=value,terminalShareOfEV=pvt/ev)
def inverse(target,key,lo,hi):
 f=lambda q:model('base',**{key:q})['illustrativePerShare'];fl=f(lo);fh=f(hi);assert fl<=target<=fh,(target,key,fl,fh)
 vals=[f(lo+(hi-lo)*i/1000)for i in range(1001)];assert all(b>=a-1e-8 for a,b in zip(vals,vals[1:]))
 for _ in range(100):
  mid=(lo+hi)/2
  if f(mid)<target:lo=mid
  else:hi=mid
 q=(lo+hi)/2;assert abs(f(q)-target)<1e-7
 return dict(target=target,parameter=key,value=q,residual=f(q)-target,monotoneIntervals=1000)
r={k:model(k)for k in C};s={}
s['discountGrowth']=[dict(discount=d,growth=g,result=model('base',discount=d,terminalGrowth=g)['illustrativePerShare'])for d in [.085,.10,.115,.13]for g in [.015,.025,.035]]
s['reinvestment']=[dict(grossCapitalResourceRate=a,roic=b,result=model('base',grossCapitalResourceRate=a,roic=b)['illustrativePerShare'])for a in [.09,.10,.12]for b in [.15,.25,.35]]
s['contractCapital']=[dict(contractAssetRatio=k,result=model('base',contractAssetRatio=k)['illustrativePerShare'])for k in [.30,.48,.70]]
s['tax']=[dict(tax=k,result=model('base',tax=k)['illustrativePerShare'])for k in [.25,.28,.31]]
s['float']=[dict(floatFactor=f,result=model('base',floatFactor=f)['illustrativePerShare'])for f in [0,.65,.90,1.15]]
s['rndRestoration']=[dict(extraRecurringCost=k,result=model('base',extraRecurringCost=k)['illustrativePerShare'])for k in [0,50,100]]
s['capital']=[dict(bridgeDelta=k,result=model('base',bridgeDelta=k)['illustrativePerShare'])for k in [-100,-50,0,50,100]]
s['dilution']=[dict(shareFactor=k,result=model('base',shareFactor=k)['illustrativePerShare'])for k in [1,1.025,1.05]]
s['stub']=[dict(stubYears=k,result=model('base',stubYears=k)['illustrativePerShare'])for k in [0,55/365]]
inv=[]
for target in [223.7803,237.32]:
 for key,lo,hi in [('growthStart',0,.40),('coreMarginEnd',.10,.80)]:
  try:inv.append(inverse(target,key,lo,hi))
  except AssertionError as e:inv.append(dict(target=target,parameter=key,status='not bracketed or monotonic',detail=str(e)))
checks=[]
for v in r.values():
 for z in v['years']:checks.extend([abs(z['fcff']-z['nopat']+z['selectedNetInvestment'])<1e-8,z['selectedNetInvestment']>=z['physicalNetFloor']-1e-8,z['selectedNetInvestment']>=z['economicNetInvestment']-1e-8])
 checks.extend([v['terminalNetInvestment']>=v['terminalPhysicalFloor']-1e-8,v['terminalNetInvestment']>=v['terminalEconomicFloor']-1e-8,abs(v['enterpriseValue']-v['pvForecast']-v['pvTerminal'])<1e-7])
assert all(checks)
out=dict(classification='illustrative_conditioned_operating_DCF_not_certified_total_value',cases=r,sensitivities=s,inverse=inv,checks=len(checks),passed=all(checks));(P/'model/results.json').write_text(json.dumps(out,indent=2)+'\n')
with (P/'model/forecast.csv').open('w')as f:
 w=csv.DictWriter(f,fieldnames=['case']+list(r['base']['years'][0]));w.writeheader();w.writerows({'case':k,**z}for k,v in r.items()for z in v['years'])
print({k:v['illustrativePerShare']for k,v in r.items()});print(inv)
