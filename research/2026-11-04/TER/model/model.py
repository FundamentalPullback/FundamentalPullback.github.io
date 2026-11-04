from pathlib import Path
import json,csv
P=Path(__file__).parent
X=json.loads((P/'inputs.json').read_text())
def calculate(x):
 c=x['common'];k=x['capital'];out={};stake=k['technoprobeShares']*k['technoprobePriceEur']*k['eurUsd'];stakeTax=max(0,stake-k['stakeSelectedTaxCostProxy'])*k['stakeSelectedExitTaxRate'];stakeNet=(stake-stakeTax)*(1-k['stakeLiquidityHaircut'])
 formCash=k['formfactorCashCommitment'] if k['formfactorClosingAssumed'] else 0;formMark=k['formfactorPurchasedShares']*k['formfactorPrice']*(1-k['formfactorLiquidityHaircut']) if k['formfactorClosingAssumed'] else 0
 industrialBridge=k['cashAndSecurities']-k['operatingCashReserve']-k['borrowings']-k['pensionLiabilities']+k['pensionSurplusAdded']-k['historicalTaxReserve']-k['derivativesNetLiability']-k['unpaidCapex']-k['nciSelectedEconomicClaim']+k['otherUnverifiedInvestmentsAdded']+k['postBalanceCashAdjustment']-formCash;shares=k['actualShares']+k['selectedNetAwardDilution']
 for name,p in x['scenarios'].items():
  rev0=x['revenueAnchor'];nopat0=x['ebitPreAcqAmortAnchor']*(1-x['initialTax']);rows=[];pv=0
  for i in range(10):
   rev=p['year1Revenue'] if i==0 else rev0*(1+p['growthAfterYear1'][i-1]);margin=p['margins'][i];ebit=rev*margin;tax=c['taxBefore2036'] if i<9 else c['tax2036AndTerminal'];nopat=ebit*(1-tax);da=rev*c['depreciationRatio'];capexratio=p['capexRatioYear1']+(p['capexRatioYear10']-p['capexRatioYear1'])*i/9;capex=max(da,rev*capexratio);wc=(rev-rev0)*c['incrementalWorkingCapitalRatio'];wc=wc if c['releaseWorkingCapitalOnDecline'] else max(0,wc);physical=capex-da+wc;growth=max(0,nopat-nopat0)/p['roic'];net=max(physical,growth);fcff=nopat-net+c['annualAcquisitionTaxShield'];discount=(1+p['wacc'])**(i+1);pv+=fcff/discount
   rows.append({'year':2027+i,'periodEnd':f'{2027+i}-11-03','revenue':rev,'growth':rev/rev0-1,'marginAfterSbcBeforeAcquiredAmort':margin,'ebitAfterSbcBeforeAcquiredAmort':ebit,'taxRate':tax,'nopat':nopat,'physicalOtherDa':da,'grossCapexFloor':capex,'workingCapitalInvestment':wc,'physicalNetInvestmentFloor':physical,'positiveNopatGrowthInvestment':growth,'additionalGrowthInvestment':net-physical,'netReinvestment':net,'fcff':fcff,'pv':fcff/discount});rev0=rev;nopat0=nopat
  g=p['g'];tr=rev0*(1+g);tn=tr*p['margins'][-1]*(1-c['tax2036AndTerminal']);tda=tr*c['depreciationRatio'];tcap=max(tda,tr*p['capexRatioYear10']);twc=(tr-rev0)*c['incrementalWorkingCapitalRatio'];ti=max(tcap-tda+twc,tn*g/p['roic']);tf=tn-ti;tpv=tf/(p['wacc']-g)/(1+p['wacc'])**10;ev=pv+tpv;oper=ev+industrialBridge
  out[name]={'rows':rows,'pvExplicit':pv,'pvTerminal':tpv,'terminalNopat':tn,'terminalReinvestment':ti,'terminalFcff':tf,'enterpriseValueIndustrial':ev,'industrialCapitalBridge':industrialBridge,'industrialResidualEquity':oper,'technoprobeGrossMarkedValue':stake,'selectedStakeExitTax':stakeTax,'technoprobeNetSelectedMark':stakeNet,'formfactorConditionalCashOutflow':formCash,'formfactorConditionalMarkedAsset':formMark,'hybridConditionalEquity':oper+stakeNet+formMark,'sharesMillions':shares,'industrialConditionalPerShare':oper/shares,'hybridConditionalPerShare':(oper+stakeNet+formMark)/shares,'terminalShareOfIndustrialEV':tpv/ev,'certifiedTotalFairValue':None}
 return out
if __name__=='__main__':
 r=calculate(X);(P/'results.json').write_text(json.dumps(r,indent=2)+'\n')
 for n,a in r.items():
  with (P/f'{n}_10years.csv').open('w') as f:
   w=csv.DictWriter(f,fieldnames=a['rows'][0]);w.writeheader();w.writerows(a['rows'])
 print({n:round(a['hybridConditionalPerShare'],4) for n,a in r.items()})
