from pathlib import Path
import json,csv
from operating_model import operating
P=Path(__file__).resolve().parent
X=json.loads((P/'inputs.json').read_text())
def calculate(x):
 c=x['capital'];t=x['transaction'];common=x['common'];result={}
 bridge=c['cashExUanRounded']-c['nominalDebtAndFinanceLeasesExUan']-c['selectedOperatingCashReserve']-c['rfsHistoricalLiability']-c['derivativeNetLiabilityAfterCollateralAndAssets']-c['historicalIncomeTaxPayable']-c['historicalCashCompensationLiability']-c['historicalAccruedInterestExUan']-c['environmentalLegacyReserve']-c['utbLegacyReserve']+c['uanQuotedEquityStake']-c['selectedUanExitTaxReserve']+c['unknownPostSeptemberCapital']
 for case,pars in x['scenarios'].items():
  parent=operating(pars['parent'],common);target=operating(pars['target'],common)
  sypars=pars['synergy'];pr=0;sy=[];sypv=0
  for n in range(1,11):
   cash=sypars['annualSynergy']*([0,.5,1][min(n-1,2)])*(1+common['inflation'])**(n-1)
   nopat=cash*(1-common['tax']);invest=max(0,nopat-pr)/sypars['roic'];integration=sypars['integrationCosts'][n-1] if n<=len(sypars['integrationCosts']) else 0
   f=nopat-invest-integration*(1-common['tax']);pv=f/(1+pars['target']['wacc'])**n
   sy.append(dict(year=n,pretaxSynergy=cash,nopat=nopat,reinvestment=invest,integrationCost=integration,fcff=f,pv=pv));sypv+=pv;pr=nopat
  g=pars['target']['g'];sn=pr*(1+g);sinvest=max(sn,0)*g/sypars['roic'];st=(sn-sinvest)/(pars['target']['wacc']-g)/(1+pars['target']['wacc'])**10;sypv+=st
  old=parent['operatingEV']+bridge
  failure=old+t['commonNetProceeds']-t['nonrefundableIepFee']-t['failureSunkCosts']-t['failureTerminationFee']
  failshares=c['existingShares']+t['newCommonShares']
  close=old+target['operatingEV']+sypv+t['commonNetProceeds']+t['pipeProceeds']-t['purchasePriceIncludingWorkingCapital']-t['debtFinancingFrictionProxy']-t['futureAcquisitionCosts']-t['nonrefundableIepFee']-t['targetLegacyEnvironmentalAndAro']-t['additionalClosingAdjustmentReserve']
  pipesh=t['pipeProceeds']/t['pipePriceIllustration'];shares=failshares+pipesh
  result[case]={'parent':parent,'target':target,'capitalBridge':bridge,'synergy':{'pv':sypv,'rows':sy,'terminalNopat':sn,'terminalReinvestment':sinvest,'pvTerminal':st},'standaloneBeforeOfferingSignedResidual':old,'standaloneBeforeOfferingSignedPerShare':old/c['existingShares'],'failureAfterCommonOffering':{'signedEquityResidual':failure,'shares':failshares,'signedResidualPerShare':failure/failshares,'financingFeasibleCertified':False},'immediateClosing':{'signedEquityResidual':close,'shares':shares,'pipeSharesIllustration':pipesh,'signedResidualPerShare':close/shares,'financingFeasibleCertified':False}}
 return result
if __name__=='__main__':
 r=calculate(X);(P/'results.json').write_text(json.dumps(r,indent=2))
 for c,v in r.items():
  for unit in ['parent','target']:
   rows=v[unit]['rows']
   with (P/f'{c}_{unit}_10years.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
 print({c:{'failure':v['failureAfterCommonOffering']['signedResidualPerShare'],'closing':v['immediateClosing']['signedResidualPerShare']} for c,v in r.items()})
