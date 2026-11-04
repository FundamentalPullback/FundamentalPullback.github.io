from pathlib import Path
import json,csv
P=Path(__file__).parent;X=json.loads((P/'inputs.json').read_text())
def calculate(x):
 k=x['capital'];bridge=k['cash']+k['hedgeAssetSelected']-sum(k[a] for a in ['cashReserve','debtPrincipal','taxReserve','otherClaimsReserve','dividendPayable','additionalMergerCashCosts','terminationFee']);shares=k['actualShares']+k['selectedAwards'];out={}
 for name,p in x['scenarios'].items():
  rev0=x['revenueAnchor'];np0=x['ebitPreAcquiredAmortAnchor']*(1-x['taxRate']);rows=[];pv=0
  for i in range(10):
   year=2027+i;rev=p['year1Revenue'] if i==0 else rev0*(1+p['growth'][i-1]);ebit=rev*p['margins'][i];np=ebit*(1-x['taxRate']);da=p['physicalDa'][i];maintenance=rev*p['maintenanceRatio'];wc=max(0,rev-rev0)*x['wcRatio'];growthPhysical=rev*p['growthCapexRatio']+wc;growthEconomic=max(0,np-np0)/p['roic'];growth=max(growthPhysical,growthEconomic);replacement=p['replacementCost']/len(p['replacementYears']) if year in p['replacementYears'] else 0;prepaid=3.115 if year<=2035 else .327;capitalSbc=rev*x['capitalizedSbcOwnerChargeRatio'];fcff=np+da-maintenance-growth-replacement-prepaid-capitalSbc;discount=(1+p['wacc'])**(i+1);pv+=fcff/discount
   rows.append({'year':year,'periodEnd':f'{year}-11-03','revenue':rev,'ebitBeforeAcquiredAmortAfterSbc':ebit,'margin':p['margins'][i],'nopat':np,'physicalSoftwareDaSelected':da,'maintenanceCapex':maintenance,'wcInvestment':wc,'physicalGrowthIncludingWc':growthPhysical,'economicGrowthInvestment':growthEconomic,'growthInvestmentSelected':growth,'replacementCapex':replacement,'prepaidHostingCashAdjustment':prepaid,'capitalizedSbcOwnerCharge':capitalSbc,'fcff':fcff,'pv':fcff/discount});rev0=rev;np0=np
  g=p['g'];tr=rev0*(1+g);tn=tr*p['margins'][-1]*(1-x['taxRate']);tda=p['physicalDa'][-1]*(1+g);tm=tr*p['maintenanceRatio'];tw=(tr-rev0)*x['wcRatio'];tgPhysical=tr*p['growthCapexRatio']+tw;tgEconomic=tn*g/p['roic'];tg=max(tgPhysical,tgEconomic)
  # Selected annual renewal funding is charged in perpetuity, not omitted after the explicit build cycle.
  annualRenewal=p['replacementCost']/p['replacementLife']*(1+x['capexInflation'])**(2037-max(p['replacementYears']));terminalCapitalSbc=tr*x['capitalizedSbcOwnerChargeRatio'];terminal=tn+tda-tm-tg-annualRenewal-terminalCapitalSbc;pt=terminal/(p['wacc']-g)/(1+p['wacc'])**10;ev=pv+pt;res=ev+bridge
  out[name]={'rows':rows,'enterpriseValue':ev,'pvExplicit':pv,'pvTerminal':pt,'terminalShare':pt/ev if ev else None,'terminalNopat':tn,'terminalDa':tda,'terminalMaintenance':tm,'terminalPhysicalGrowth':tgPhysical,'terminalEconomicGrowth':tgEconomic,'terminalGrowthInvestment':tg,'terminalAnnualReplacementFunding':annualRenewal,'terminalCapitalizedSbcOwnerCharge':terminalCapitalSbc,'terminalFcff':terminal,'capitalBridge':bridge,'selectedShares':shares,'standaloneResidualEquity':res,'standaloneResidualPerShare':res/shares,'currentTotalFairValue':None,'negativeResidualIsNotNegativeStockPrice':res<0}
 return out
if __name__=='__main__':
 r=calculate(X);(P/'results.json').write_text(json.dumps(r,indent=2)+'\n')
 for n,a in r.items():
  with (P/f'{n}_10years.csv').open('w') as f:w=csv.DictWriter(f,fieldnames=a['rows'][0]);w.writeheader();w.writerows(a['rows'])
 print({n:a['standaloneResidualPerShare'] for n,a in r.items()})
