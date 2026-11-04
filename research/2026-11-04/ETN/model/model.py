from pathlib import Path
import json,csv
P=Path(__file__).parent
X=json.loads((P/'inputs.json').read_text())
def calculate(x):
 c=x['common'];k=x['capital'];out={};bridge=k['cashAndShortInvestments']-sum(k[n] for n in ['operatingCashReserve','debtCarrying','selectedDebtFaceAdjustment','pensionAndOtherBenefits','historicTaxReserve','nciEconomicClaim','restructuringPayable'])+k['unverifiedInvestmentsAdded']+k['postBalanceNetAdjustment'];shares=k['actualShares']+k['selectedNetAwards']
 for n,p in x['scenarios'].items():
  rev0=x['revenueAnchor'];np0=x['ebitPreIntangibleAmortAnchor']*(1-c['taxRate']);rows=[];pv=0
  for i in range(10):
   rev=p['year1Revenue'] if i==0 else rev0*(1+p['growth'][i-1]);ebit=rev*p['margins'][i];np=ebit*(1-c['taxRate']);da=rev*c['physicalDaRatio'];capex=max(da,rev*(p['capexStart']+(p['capexEnd']-p['capexStart'])*i/9));wc=(rev-rev0)*c['workingCapitalRatio'];wc=wc if c['releaseWorkingCapital'] else max(0,wc);physical=capex-da+wc;growth=max(0,np-np0)/p['roic'];investment=max(physical,growth);fcff=np-investment+c['acquisitionTaxShield'];discount=(1+p['wacc'])**(i+1);pv+=fcff/discount
   rows.append({'year':2027+i,'periodEnd':f'{2027+i}-11-03','revenue':rev,'growth':rev/rev0-1,'ebitAfterSbcBeforeDisclosedIntangibleAmort':ebit,'margin':p['margins'][i],'nopat':np,'physicalDA':da,'grossCapexFloor':capex,'wcInvestment':wc,'physicalNetFloor':physical,'growthNetInvestment':growth,'netReinvestment':investment,'additionalGrowthInvestment':investment-physical,'fcff':fcff,'pv':fcff/discount});rev0=rev;np0=np
  g=p['g'];tr=rev0*(1+g);tn=tr*p['margins'][-1]*(1-c['taxRate']);tda=tr*c['physicalDaRatio'];tcap=max(tda,tr*p['capexEnd']);twc=(tr-rev0)*c['workingCapitalRatio'];physical=tcap-tda+twc;growth=tn*g/p['roic'];ti=max(physical,growth);tf=tn-ti;tpv=tf/(p['wacc']-g)/(1+p['wacc'])**10;ev=pv+tpv
  out[n]={'rows':rows,'enterpriseValue':ev,'pvExplicit':pv,'pvTerminal':tpv,'terminalShare':tpv/ev,'terminalNopat':tn,'terminalPhysicalFloor':physical,'terminalEconomicInvestment':growth,'terminalInvestment':ti,'terminalFcff':tf,'capitalBridge':bridge,'equityCounterfactual':ev+bridge,'sharesSelected':shares,'counterfactualPerShare':(ev+bridge)/shares,'currentTotalFairValue':None}
 return out
if __name__=='__main__':
 r=calculate(X);(P/'results.json').write_text(json.dumps(r,indent=2)+'\n')
 for n,a in r.items():
  with (P/f'{n}_10years.csv').open('w') as f:
   w=csv.DictWriter(f,fieldnames=a['rows'][0]);w.writeheader();w.writerows(a['rows'])
 print({n:a['counterfactualPerShare'] for n,a in r.items()})
