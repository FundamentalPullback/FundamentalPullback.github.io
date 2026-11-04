from pathlib import Path
from copy import deepcopy
import json,math
from model import X,calculate
P=Path(__file__).parent;R=calculate(X);checks=[]
def ck(n,c):
 assert c,n
 checks.append(n)
def val(x):return calculate(x)['base']['counterfactualPerShare']
s={}
for name,group,key,vs in [('cashReserve','capital','operatingCashReserve',[250,500,1000]),('debtFaceAdjustment','capital','selectedDebtFaceAdjustment',[0,150,300]),('historicTaxReserve','capital','historicTaxReserve',[0,1000,1518,1928,2500]),('nciClaim','capital','nciEconomicClaim',[47,100,200]),('awardDilution','capital','selectedNetAwards',[0,1,3,5]),('unverifiedInvestment','capital','unverifiedInvestmentsAdded',[0,92,250]),('postBalanceCapital','capital','postBalanceNetAdjustment',[-763,-410,-157.25,0,500]),('tax','common','taxRate',[.20,.24,.28]),('wc','common','workingCapitalRatio',[.15,.25,.35]),('annualAcquisitionTaxShield','common','acquisitionTaxShield',[0,50,100])]:
 s[name]=[]
 for v in vs:
  x=deepcopy(X);x[group][key]=v;s[name].append({'input':v,'value':val(x)})
s['wacc_g']=[]
for w in [.08,.0875,.0975,.11,.12]:
 for g in [.02,.025,.03,.035,.04]:
  x=deepcopy(X);x['scenarios']['base'].update(wacc=w,g=g);s['wacc_g'].append({'wacc':w,'g':g,'value':val(x)})
s['capex']=[]
for d in [0,.01,.02]:
 x=deepcopy(X);p=x['scenarios']['base'];p['capexStart']+=d;p['capexEnd']+=d;r=calculate(x)['base'];s['capex'].append({'extraRatio':d,'value':r['counterfactualPerShare']});ck('capex sensitivity terminal physical '+str(d),r['terminalInvestment']+1e-8>=r['terminalPhysicalFloor'])
s['intangibleReplacementMarginCharge']=[]
for charge in [0,.005,.01,.02]:
 x=deepcopy(X);x['scenarios']['base']['margins']=[m-charge for m in x['scenarios']['base']['margins']];s['intangibleReplacementMarginCharge'].append({'annualMarginCharge':charge,'value':val(x),'note':'Additional ongoing intangible replacement burden beyond existing R&D/capex, also retained in terminal.'})
s['roic']=[]
for v in [.10,.15,.20,.25,.30]:
 x=deepcopy(X);x['scenarios']['base']['roic']=v;s['roic'].append({'roic':v,'value':val(x)})
x=deepcopy(X);x['revenueAnchor']=31984;x['ebitPreIntangibleAmortAnchor']=6320;s['reportedTTMAnchor']={'value':val(x),'revenue':31984,'ebitPreAmort':6320,'note':'Alternative partial-year acquiree anchor; may charge additional growth investment already economically purchased.'}
x=deepcopy(X);x['common']['releaseWorkingCapital']=True;s['wcRelease']={'value':val(x)}
s['COLIllustrativeNetAssetDelta']=[]
price=810*1.1179
for ev in [0,price,1500]:s['COLIllustrativeNetAssetDelta'].append({'hypotheticalAcquiredEV':ev,'purchaseUSDAtNov3FX':price,'deltaEquity':ev-price,'counterfactualValueAfterDelta':R['base']['counterfactualPerShare']+(ev-price)/R['base']['sharesSelected'],'caveat':'No COL DCF or financing terms established. Algebraic sensitivity, not closed acquisition or current total value.'})
s['jointStrongDemand']=[]
for gs in [0,.02,.04]:
 x=deepcopy(X);p=x['scenarios']['bull'];p['margins']=[.28]*10;p['growth']=[a+gs for a in p['growth']];p['wacc']=.08;s['jointStrongDemand'].append({'margin':.28,'growthShift':gs,'wacc':.08,'value':calculate(x)['bull']['counterfactualPerShare']})
def solve(kind):
 def f(z):
  x=deepcopy(X);p=x['scenarios']['base']
  if kind=='margin':p['margins']=[m+z for m in p['margins']]
  else:p['growth']=[g+z for g in p['growth']]
  return val(x)
 hi=.5;grid=[f(hi*i/200) for i in range(201)];ck(kind+' inverse monotonic',all(b>=a-1e-8 for a,b in zip(grid,grid[1:])));
 if not grid[0]<=X['price']<=grid[-1]:return {'root':None,'maximumShift':hi,'valueAtMax':grid[-1]}
 a,b=0,hi
 for _ in range(80):
  mid=(a+b)/2
  if f(mid)<X['price']:a=mid
  else:b=mid
 return {'shift':(a+b)/2,'value':f((a+b)/2),'target':X['price']}
inv={k:solve(k) for k in ['margin','growth']}
for n,r in R.items():
 p=X['scenarios'][n];prev=X['ebitPreIntangibleAmortAnchor']*(1-X['common']['taxRate'])
 for a in r['rows']:
  pre=n+str(a['year']);ck(pre+' nopat',math.isclose(a['nopat'],a['ebitAfterSbcBeforeDisclosedIntangibleAmort']*(1-X['common']['taxRate']),rel_tol=1e-12));ck(pre+' financed growth',a['netReinvestment']+1e-8>=max(0,a['nopat']-prev)/p['roic']);ck(pre+' physical',a['netReinvestment']+1e-8>=a['physicalNetFloor']);ck(pre+' fcff',math.isclose(a['fcff'],a['nopat']-a['netReinvestment'],abs_tol=1e-8));ck(pre+' pv',math.isclose(a['pv'],a['fcff']/(1+p['wacc'])**(a['year']-2026),rel_tol=1e-12));prev=a['nopat']
 ck(n+' terminal both floors',r['terminalInvestment']+1e-8>=max(r['terminalPhysicalFloor'],r['terminalEconomicInvestment']));ck(n+' EV',math.isclose(r['enterpriseValue'],sum(a['pv'] for a in r['rows'])+r['pvTerminal'],rel_tol=1e-12));ck(n+' share bridge',math.isclose(r['counterfactualPerShare']*r['sharesSelected'],r['enterpriseValue']+r['capitalBridge'],rel_tol=1e-12));ck(n+' no total',r['currentTotalFairValue'] is None)
out={'central':{n:r['counterfactualPerShare'] for n,r in R.items()},'sensitivity':s,'inverse':inv,'checks':{'passed':len(checks),'labels':checks}};(P/'checks.json').write_text(json.dumps(out,indent=2)+'\n');print(len(checks),'valuation PASS')
