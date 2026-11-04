from pathlib import Path
import json,copy,math
from model import calculate,X
P=Path(__file__).parent
checks=[]
def check(name,a):
 assert a,name
 checks.append(name)
def values(x):return {n:a['conditionalIndustrialPerShare'] for n,a in calculate(x).items()}
r=calculate(X)
for n,a in r.items():
 check(n+' null total',a['currentTotalFairValue'] is None)
 check(n+' ten years',len(a['rows'])==10)
 for i,z in enumerate(a['rows']):
  check(f'{n}{i} financed physical',z['netReinvestment']>=z['physicalNetFloor']-1e-9)
  check(f'{n}{i} financed growth',z['netReinvestment']>=z['growthNetInvestment']-1e-9)
  check(f'{n}{i} cash identity',math.isclose(z['fcff'],z['nopat']-z['netReinvestment']))
 check(n+' terminal physical',a['terminalInvestment']>=a['terminalPhysicalFloor'])
 check(n+' terminal growth',a['terminalInvestment']>=a['terminalEconomicInvestment'])
 check(n+' enterprise PV',math.isclose(a['enterpriseValue'],a['pvExplicit']+a['pvTerminal']))
 check(n+' equity bridge',math.isclose(a['conditionalIndustrialPerShare']*a['sharesSelected'],a['enterpriseValue']+a['capitalBridge']))
s={}
def sweep(section,key,vs):
 out=[]
 for v in vs:
  x=copy.deepcopy(X);x[section][key]=v;out.append({'input':v,'values':values(x)})
 s[key]=out
for k,vs in {'financingClosingAssumed':[False,True],'financingFeesSelected':[0,3,5],'selectedNetAwards':[0,.65,1.16,1.5,2],'operatingCashReserve':[100,150,250],'historicTaxReserve':[27,55.4,56.397,70],'grantRepaymentReserve':[0,9,18],'promissoryNoteSelectedValue':[0,.75,1.5],'fictStakeSelectedValue':[0,70.467,150],'postBalanceNetAdjustment':[-100,0,100]}.items():sweep('capital',k,vs)
for k,vs in {'taxRate':[.20,.24,.28],'workingCapitalRatio':[.15,.22,.35],'physicalDaRatio':[.025,.03,.035]}.items():sweep('common',k,vs)
for key,vs in {'roic':[.15,.25,.35],'wacc':[.09,.1075,.125],'g':[.02,.03,.04]}.items():
 s[key]=[]
 for v in vs:
  x=copy.deepcopy(X)
  for p in x['scenarios'].values():p[key]=v
  s[key].append({'input':v,'values':values(x)})
s['persistentCapexExtra']=[]
for extra in [0,.02,.04]:
 x=copy.deepcopy(X)
 for p in x['scenarios'].values():p['capexRatios']=[v+extra for v in p['capexRatios']]
 rr=calculate(x)
 for n,a in rr.items():check(f'capex {extra} {n} terminal financed',a['terminalInvestment']>=a['terminalPhysicalFloor'])
 s['persistentCapexExtra'].append({'input':extra,'values':values(x)})
s['marginShift']=[]
for extra in [-.05,-.025,0,.025,.05]:
 x=copy.deepcopy(X)
 for p in x['scenarios'].values():p['margins']=[v+extra for v in p['margins']]
 s['marginShift'].append({'input':extra,'values':values(x)})
x=copy.deepcopy(X);x['revenueAnchor']=980.096;x['ebitPreIntangibleAmortAnchor']=173.012
s['TTMAnchorSameFuturePath']=values(x)
s['waccGGrid']=[]
for w in [.09,.10,.1075,.115,.125]:
 for g in [.02,.025,.03,.035,.04]:
  x=copy.deepcopy(X);x['scenarios']['base'].update(wacc=w,g=g)
  s['waccGGrid'].append({'wacc':w,'g':g,'base':values(x)['base']})
def marginvalue(shift):
 x=copy.deepcopy(X);x['scenarios']['base']['margins']=[v+shift for v in X['scenarios']['base']['margins']];return values(x)['base']
def growthvalue(extra):
 x=copy.deepcopy(X);x['scenarios']['base']['growth']=[v+extra for v in X['scenarios']['base']['growth']];return values(x)['base']
inverses={}
for name,fn,lo,hi in [('marginShift',marginvalue,-.1,.3),('extraAnnualGrowthY2to10',growthvalue,-.02,.25)]:
 vals=[fn(lo+(hi-lo)*i/100) for i in range(101)];mono=all(b>=a for a,b in zip(vals,vals[1:]));check(name+' monotonic bracket',mono)
 if vals[0]<=X['price']<=vals[-1]:
  for _ in range(90):
   mid=(lo+hi)/2
   if fn(mid)<X['price']:lo=mid
   else:hi=mid
  inverses[name]={'requiredAddition':(lo+hi)/2,'reproducedPrice':fn((lo+hi)/2),'target':X['price'],'scope':'Industrial component only, FICT omitted, conditional financing and selected awards; not total-company reverse DCF.'}
 else:inverses[name]={'solution':None,'bracketPrices':[vals[0],vals[-1]]}
(P/'sensitivities.json').write_text(json.dumps(s,indent=2)+'\n');(P/'inverse.json').write_text(json.dumps(inverses,indent=2)+'\n');(P/'checks.json').write_text(json.dumps({'passed':len(checks),'checks':checks},indent=2)+'\n');print('PASS',len(checks),inverses)
