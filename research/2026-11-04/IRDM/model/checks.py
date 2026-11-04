from pathlib import Path
import json,copy,math
from model import X,calculate
P=Path(__file__).parent;tests=[]
def ck(n,b):assert b,n;tests.append(n)
def vals(x):return {n:a['standaloneResidualPerShare'] for n,a in calculate(x).items()}
r=calculate(X)
for n,a in r.items():
 ck(n+' total null',a['currentTotalFairValue'] is None)
 ck(n+' 10 years',len(a['rows'])==10)
 ck(n+' all explicit replacement funded',math.isclose(sum(z['replacementCapex'] for z in a['rows']),X['scenarios'][n]['replacementCost']))
 for z in a['rows']:
  ck(f'{n}{z["year"]} growth physical',z['growthInvestmentSelected']>=z['physicalGrowthIncludingWc'])
  ck(f'{n}{z["year"]} growth economic',z['growthInvestmentSelected']>=z['economicGrowthInvestment'])
  ck(f'{n}{z["year"]} FCFF',math.isclose(z['fcff'],z['nopat']+z['physicalSoftwareDaSelected']-z['maintenanceCapex']-z['growthInvestmentSelected']-z['replacementCapex']-z['prepaidHostingCashAdjustment']-z['capitalizedSbcOwnerCharge']))
 ck(n+' perpetual renewal funded',a['terminalAnnualReplacementFunding']>0)
 ck(n+' terminal growth funded',a['terminalGrowthInvestment']>=max(a['terminalPhysicalGrowth'],a['terminalEconomicGrowth']))
 ck(n+' terminal cash',math.isclose(a['terminalFcff'],a['terminalNopat']+a['terminalDa']-a['terminalMaintenance']-a['terminalGrowthInvestment']-a['terminalAnnualReplacementFunding']-a['terminalCapitalizedSbcOwnerCharge']))
 ck(n+' EV PV',math.isclose(a['enterpriseValue'],a['pvExplicit']+a['pvTerminal']))
 ck(n+' residual bridge',math.isclose(a['standaloneResidualPerShare']*a['selectedShares'],a['enterpriseValue']+a['capitalBridge']))
s={}
for key,vs in {'cashReserve':[30,60,100],'taxReserve':[0,3.947,10],'otherClaimsReserve':[0,25,50],'selectedAwards':[.612,1.5,2.5,4.282,5],'additionalMergerCashCosts':[0,25,50,100],'terminationFee':[0,223.62],'hedgeAssetSelected':[0,3.7]}.items():
 s[key]=[]
 for v in vs:
  x=copy.deepcopy(X);x['capital'][key]=v;s[key].append({'input':v,'values':vals(x)})
for key,vs in {'taxRate':[.15,.21,.24,.28],'wcRatio':[.05,.12,.2],'capitalizedSbcOwnerChargeRatio':[0,.005,.01]}.items():
 s[key]=[]
 for v in vs:
  x=copy.deepcopy(X);x[key]=v;s[key].append({'input':v,'values':vals(x)})
for key,vs in {'replacementCost':[2000,2800,3500,4500,5500],'replacementLife':[12.5,17.5,22.5],'maintenanceRatio':[.06,.075,.10],'growthCapexRatio':[.01,.025,.04],'roic':[.12,.18,.25],'wacc':[.075,.085,.095,.11,.125],'g':[.015,.025,.035]}.items():
 s[key]=[]
 for v in vs:
  x=copy.deepcopy(X)
  for p in x['scenarios'].values():p[key]=v
  s[key].append({'input':v,'values':vals(x)})
s['marginShift']=[]
for shift in [-.05,0,.05,.10]:
 x=copy.deepcopy(X)
 for p in x['scenarios'].values():p['margins']=[v+shift for v in p['margins']]
 s['marginShift'].append({'input':shift,'values':vals(x)})
s['daScale']=[]
for scale in [.75,1,1.25]:
 x=copy.deepcopy(X)
 for p in x['scenarios'].values():p['physicalDa']=[v*scale for v in p['physicalDa']]
 s['daScale'].append({'input':scale,'values':vals(x)})
s['emssLossOperatingStress']=[]
for haircut in [.5,1]:
 x=copy.deepcopy(X)
 for p in x['scenarios'].values():
  rev=p['year1Revenue'];new=[]
  for i,m in enumerate(p['margins']):
   if i:rev*=1+p['growth'][i-1]
   new.append(m-(110.5*.65*haircut)/rev)
  p['margins']=new
 s['emssLossOperatingStress'].append({'fractionOfContractLost':haircut,'assumedContributionMargin':.65,'scope':'Revenue path unchanged but EBIT reduced by lost contract contribution; sensitivity only, not forecast or complete restructuring response','values':vals(x)})
x=copy.deepcopy(X)
for p in x['scenarios'].values():p['replacementCost']=0
rr=calculate(x)
s['illustrativeRunoffNoRenewalNoTerminal']={n:{'enterprisePV':sum(z['pv'] for z in a['rows'] if z['year']<=2035),'residualPerShare':(sum(z['pv'] for z in a['rows'] if z['year']<=2035)+a['capitalBridge'])/a['selectedShares']} for n,a in rr.items()}
s['unfundedReplacementOmissionDiagnostic_NOT_VALID_VALUE']=vals(x)
inv={}
for kind in ['margin','growth']:
 def f(v):
  x=copy.deepcopy(X);p=x['scenarios']['base'];p['margins']=[a+v for a in p['margins']] if kind=='margin' else p['margins'];p['growth']=[a+v for a in p['growth']] if kind=='growth' else p['growth'];return vals(x)['base']
 lo=0;hi=.30 if kind=='margin' else .20;scan=[f(lo+(hi-lo)*i/100) for i in range(101)];mono=all(b>=a for a,b in zip(scan,scan[1:]));ck(kind+' monotonic inverse bracket',mono)
 if scan[0]<=X['price']<=scan[-1]:
  for _ in range(85):
   mid=(lo+hi)/2
   if f(mid)<X['price']:lo=mid
   else:hi=mid
  inv[kind]={'requiredAdditional':(lo+hi)/2,'reproduced':f((lo+hi)/2),'target':X['price'],'standaloneOnlyNotMergerProbability':True}
 else:inv[kind]={'solutionInBracket':False,'bracketValues':[scan[0],scan[-1]]}
(P/'sensitivities.json').write_text(json.dumps(s,indent=2)+'\n');(P/'inverse.json').write_text(json.dumps(inv,indent=2)+'\n');(P/'checks.json').write_text(json.dumps({'passed':len(tests),'tests':tests},indent=2)+'\n');print('PASS',len(tests),inv)
