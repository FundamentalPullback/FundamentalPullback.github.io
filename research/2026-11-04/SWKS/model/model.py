from pathlib import Path
import json,csv,copy
P=Path(__file__).parent
CASES={
'bear':{'growth':[-.08,0,.02,.02,.02],'margin':[.12,.12,.125,.13,.13],'terminalMargin':.13,'tax':.23,'daPct':.06,'capexPct':.08,'nwcPct':.17,'integrationCash':[200,150,100,0,0],'wacc':.12,'g':.02,'roic':.12},
'base':{'growth':[7400/7500-1,.02,.04,.05,.05],'margin':[.145,.175,.20,.215,.22],'terminalMargin':.22,'tax':.20,'daPct':.06,'capexPct':.07,'nwcPct':.15,'integrationCash':[150,100,50,0,0],'wacc':.105,'g':.025,'roic':.16},
'bull':{'growth':[.02,.07,.08,.08,.07],'margin':[.16,.21,.25,.275,.28],'terminalMargin':.28,'tax':.18,'daPct':.06,'capexPct':.065,'nwcPct':.14,'integrationCash':[100,75,25,0,0],'wacc':.095,'g':.03,'roic':.20}}
INPUT={'units':'USD millions except per share; shares millions','asOf':'2026-11-04','revenueAnchor':7500,'anchorSource':'Company rounded combined FY2026 business categories, not audited combined financial statements','assumedNetFinancialClaims':3500,'assumedDilutedShares':241,'scanPrice':82.65,'vendorClose':82.96,'cases':CASES,'fairValueTotal':None,'warning':'All model outputs are illustrative operating cases and capital sensitivities. Missing actual consolidated closing cash, PPA, complete combined cash-flow normalization and homogeneous comps prevent current total equity valuation and entry approval.'}
def calc(c,claims=3500,shares=241):
 rev=7500.;rows=[]
 for t in range(1,11):
  a=max(0,(t-5)/5); g=c['growth'][t-1] if t<=5 else c['growth'][-1]*(1-a)+c['g']*a; m=c['margin'][t-1] if t<=5 else c['margin'][-1]*(1-a)+c['terminalMargin']*a
  old=rev;rev*=1+g;ebit=rev*m;nopat=ebit*(1-c['tax']);da=rev*c['daPct'];rawcap=rev*c['capexPct'];rawdnwc=max(0,rev-old)*c['nwcPct']; target=nopat*g/c['roic']
  # Years 6–10 transition net reinvestment to sustainable g/ROIC, preserving explicit components.
  dnwc=rawdnwc; netraw=rawcap-da+dnwc;netreinvest=netraw*(1-a)+target*a; capex=da+netreinvest-dnwc
  integration=c['integrationCash'][t-1] if t<=5 else 0;fcff=nopat+da-capex-dnwc-integration;pv=fcff/(1+c['wacc'])**t
  rows.append({'year':t,'revenue':rev,'growth':g,'marginAfterSBC':m,'ebit':ebit,'taxRate':c['tax'],'nopat':nopat,'daProductive':da,'capexAllNecessary':capex,'changeNWC':dnwc,'netReinvestment':netreinvest,'integrationCashExtra':integration,'fcff':fcff,'pv':pv})
 n=rows[-1]['nopat']*(1+c['g']);ri=n*c['g']/c['roic'];fcff=n-ri;tv=fcff/(c['wacc']-c['g']);pvtv=tv/(1+c['wacc'])**10;ev=sum(x['pv'] for x in rows)+pvtv;equity=ev-claims
 return {'operatingEV':ev,'terminalNOPAT':n,'terminalReinvestment':ri,'terminalFCFF':fcff,'terminalValue':tv,'pvTerminal':pvtv,'terminalWeight':pvtv/ev,'hypotheticalClaims':claims,'hypotheticalShares':shares,'illustrativeEquityResidualPerShare':equity/shares,'isCurrentFairValue':False,'rows':rows}
def solve(fn,target,lo,hi):
 if (fn(lo)-target)*(fn(hi)-target)>0:return None
 for _ in range(100):
  mid=(lo+hi)/2
  if fn(mid)<target:lo=mid
  else:hi=mid
 return (lo+hi)/2
R={k:calc(v) for k,v in CASES.items()}
for k,d in R.items():
 with open(P/(k+'_schedule.csv'),'w') as f:w=csv.DictWriter(f,fieldnames=d['rows'][0]);w.writeheader();w.writerows(d['rows'])
target=82.65*241+3500;base=CASES['base']
def growth_case(g,m):
 c=copy.deepcopy(base);c['growth']=[base['growth'][0]]+[g]*4;c['margin']=[base['margin'][0],(base['margin'][0]+m)/2,m,m,m];c['terminalMargin']=m;return c
reverse=[]
for m in [.18,.22,.26,.28]:
 g=solve(lambda x:calc(growth_case(x,m))['operatingEV'],target,-.05,.4);reverse.append({'matureMarginAfterSBC':m,'growthYears2to5':g,'impliedTargetEV':target,'claimsAssumed':3500,'sharesAssumed':241,'solveResidual':None if g is None else calc(growth_case(g,m))['operatingEV']-target})
sens=[]
for w in [.095,.105,.115]:
 for g in [.02,.025,.03]:
  c=copy.deepcopy(base);c['wacc']=w;c['g']=g;r=calc(c);sens.append({'wacc':w,'g':g,'operatingEV':r['operatingEV'],'illustrativeResidualPerShare':r['illustrativeEquityResidualPerShare']})
cap=[{'netFinancialClaimsAssumption':n,'dilutedSharesAssumption':s,'baseIllustrativeResidualPerShare':calc(base,n,s)['illustrativeEquityResidualPerShare']}for n in [2500,3500,4500]for s in [238,241,245]]
(P/'inputs.json').write_text(json.dumps(INPUT,indent=2)+'\n');(P/'results.json').write_text(json.dumps({'cases':R,'reverse':reverse,'waccGrowthSensitivity':sens,'capitalSensitivity':cap},indent=2)+'\n')
checks={'tenYears':all(len(r['rows'])==10 for r in R.values()),'waccGreaterThanG':all(c['wacc']>c['g']for c in CASES.values()),'fcffIdentity':all(abs(x['fcff']-(x['nopat']+x['daProductive']-x['capexAllNecessary']-x['changeNWC']-x['integrationCashExtra']))<1e-8 for r in R.values()for x in r['rows']),'year10TerminalTransition':all(abs(r['rows'][-1]['netReinvestment']-r['rows'][-1]['nopat']*CASES[k]['g']/CASES[k]['roic'])<1e-8 for k,r in R.items()),'positiveCapex':all(x['capexAllNecessary']>=0 for r in R.values()for x in r['rows']),'orderedCases':R['bear']['operatingEV']<R['base']['operatingEV']<R['bull']['operatingEV'],'nullTotalValuation':INPUT['fairValueTotal'] is None,'inverseResidual':all(x['solveResidual']is None or abs(x['solveResidual'])<1e-6 for x in reverse)}
(P/'qa.json').write_text(json.dumps(checks,indent=2)+'\n');print(json.dumps({k:{a:d[a]for a in ['operatingEV','illustrativeEquityResidualPerShare','terminalWeight']}for k,d in R.items()},indent=2));print(reverse);assert all(checks.values())
