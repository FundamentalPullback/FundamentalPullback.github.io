from pathlib import Path
import json,copy,math
p=Path(__file__).parent
x=json.loads((p/'inputs.json').read_text())
def run(case='base',margin_add=0,growth_add=0,discount=None,g=None,roic=None,capex=None,first_fraction=None,bridge_extra=0,shares=None):
 c=copy.deepcopy(x['scenarios'][case]);d=c['discount'] if discount is None else discount;g=c['terminalGrowth'] if g is None else g;roic=c['roic'] if roic is None else roic;capex=x['capexRevenue'] if capex is None else capex
 frac=x['remainingFY27Fraction'] if first_fraction is None else first_fraction
 prevrev=x['revenue'];prevnop=x['ebitBeforeAcquiredAmort']*(1-x['tax']);rows=[]
 for i in range(10):
  growth=c['growth'][i]+growth_add;rev=prevrev*(1+growth);m=c['margin'][i]+margin_add;ebit=rev*m;nop=ebit*(1-x['tax']);da=x['productiveDA']*rev/x['revenue'];cx=capex*rev;wc=x['workingCapitalGrowthRatio']*max(0,rev-prevrev)
  physical=cx-da+wc;economic=max(0,nop-prevnop)/roic;reinvest=max(physical,economic,0);fcff=nop-reinvest;t=x['remainingFY27Fraction']+i;cash=fcff*(frac if i==0 else 1);pv=cash/(1+d)**t
  rows.append(dict(year=2027+i,revenue=rev,growth=growth,margin=m,ebitBeforeAcquiredAmort=ebit,nopat=nop,productiveDA=da,productiveCapex=cx,workingCapitalInvestment=wc,physicalNetInvestment=physical,economicNetInvestment=economic,netInvestment=reinvest,fcffFullYear=fcff,recognizedCash=cash,discountYears=t,pv=pv));prevrev=rev;prevnop=nop
 tr=prevrev*(1+g);tn=prevnop*(1+g);tda=rows[-1]['productiveDA']*(1+g);tc=tr*capex;twc=x['workingCapitalGrowthRatio']*(tr-prevrev);tp=tc-tda+twc;te=tn*g/roic;ti=max(tp,te,0);tf=tn-ti;tv=tf/(d-g);tpv=tv/(1+d)**rows[-1]['discountYears'];ev=sum(r['pv'] for r in rows)+tpv
 pre=sum(x['capitalBridge'].values())+bridge_extra;sh=x['selectedShares'] if shares is None else shares;close=pre-x['transaction']['basePurchase']-x['transaction']['selectedEarnoutReserve']-x['transaction']['selectedFees']
 return dict(rows=rows,terminal=dict(revenue=tr,nopat=tn,productiveDA=tda,capex=tc,workingCapital=twc,physicalNetInvestment=tp,economicNetInvestment=te,netInvestment=ti,fcff=tf,value=tv,pv=tpv),operatingEV=ev,preDealBridge=pre,fundedClosingBridge=close,standaloneCounterfactualPerShare=(ev+pre)/sh,fundedLegacyResidualPerShare=(ev+close)/sh,unknownTargetEVRequiredAtPrice=x['price']*sh-ev-close,selectedShares=sh,terminalShareOfEV=tpv/ev,discount=d,terminalGrowth=g,roic=roic)
def inverse(kind):
 lo,hi=(0,.8) if kind=='margin' else (0,.45)
 def f(v):return run(margin_add=v if kind=='margin' else 0,growth_add=v if kind=='growth' else 0)['fundedLegacyResidualPerShare']-x['price']
 assert f(lo)*f(hi)<0
 samples=[f(lo+(hi-lo)*i/1000) for i in range(1001)];assert all(b>a for a,b in zip(samples,samples[1:]))
 for _ in range(100):
  mid=(lo+hi)/2
  if f(mid)>0:hi=mid
  else:lo=mid
 v=(lo+hi)/2;r=run(margin_add=v if kind=='margin' else 0,growth_add=v if kind=='growth' else 0);assert abs(f(v))<1e-7
 return dict(parameter=v,residual=f(v),monotoneIntervals=1000,year10Revenue=r['rows'][-1]['revenue'],year10Margin=r['rows'][-1]['margin'],firstYearFCFF=r['rows'][0]['fcffFullYear'],interpretation='Legacy business alone funds acquisition and explains price; excludes unknown target value, not a combined-company forecast')
o={'scope':'Partial legacy-business DCF counterfactual and funded legacy residual. Neither is current total equity fair value. Target value unknown, not zero.','scenarios':{c:run(c) for c in x['scenarios']},'inverse':{k:inverse(k) for k in ['margin','growth']},'sensitivities':{}}
s=o['sensitivities'];s['discountGrowth']=[dict(discount=d,g=g,value=run(discount=d,g=g)['fundedLegacyResidualPerShare']) for d in [.085,.095,.105,.115] for g in [.02,.025,.03]]
s['capex']=[dict(ratio=c,value=run(capex=c)['fundedLegacyResidualPerShare']) for c in [.025,.04,.06]]
s['roic']=[dict(roic=r,value=run(roic=r)['fundedLegacyResidualPerShare']) for r in [.15,.2,.25,.3]]
s['firstYearFraction']=[dict(fraction=f,value=run(first_fraction=f)['fundedLegacyResidualPerShare']) for f in [.5,x['remainingFY27Fraction'],1]]
s['bridge']=[dict(additionalBridge=a,value=run(bridge_extra=a)['fundedLegacyResidualPerShare']) for a in [-100,-31.9,0,28.906,35.029,100]]
s['shares']=[dict(shares=a,value=run(shares=a)['fundedLegacyResidualPerShare']) for a in [81.992669,84.2,86]]
s['earnout']=[dict(earnout=e,value=(o['scenarios']['base']['operatingEV']+o['scenarios']['base']['preDealBridge']-1700-e-25)/x['selectedShares']) for e in [0,200,400]]
checks=[]
for k,r in o['scenarios'].items():
 for row in r['rows']:
  for label,ok in [('physical',row['netInvestment']>=row['physicalNetInvestment']-1e-9),('economic',row['netInvestment']>=row['economicNetInvestment']-1e-9),('fcff',abs(row['fcffFullYear']-(row['nopat']-row['netInvestment']))<1e-8)]:assert ok;checks.append(k+str(row['year'])+label)
 t=r['terminal'];assert t['netInvestment']>=max(t['physicalNetInvestment'],t['economicNetInvestment'])-1e-9;checks.append(k+'terminal')
 assert abs((r['standaloneCounterfactualPerShare']-r['fundedLegacyResidualPerShare'])*r['selectedShares']-1925)<1e-8
 assert abs(r['operatingEV']+r['fundedClosingBridge']+r['unknownTargetEVRequiredAtPrice']-x['price']*r['selectedShares'])<1e-8
(p/'results.json').write_text(json.dumps(o,indent=2)+'\n');(p/'qa.json').write_text(json.dumps({'pass':True,'checks':len(checks),'inverses':'bracket,residual,1000 monotone intervals each'},indent=2)+'\n')
print({k:(r['standaloneCounterfactualPerShare'],r['fundedLegacyResidualPerShare']) for k,r in o['scenarios'].items()})
