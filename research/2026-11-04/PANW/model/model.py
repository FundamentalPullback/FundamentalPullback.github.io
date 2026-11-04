from pathlib import Path
from copy import deepcopy
import json,csv
P=Path(__file__).resolve().parent
X=json.loads((P/'inputs.json').read_text())
def calculate(x):
 out={};c=x['common'];cap=x['capital']
 bridge=cap['cashAndMarketableInvestments']-cap['subsequentAcquisitionsHeadlineCash']-cap['operatingCashReserve']-cap['convertibleFairValueProxy']+cap['cappedCallFairValueProxy']-cap['contingentConsideration']-cap['deferredCompensationEconomicLiability']-cap['selectedHistoricalTaxRiskReserve']-cap['recordedSeverance']+cap['unknownPostJulyCapital']
 shares=cap['actualSharesOctober9']+cap['selectedExistingAwardNetDilution']
 for name,p in x['scenarios'].items():
  rev0=x['proformaRevenueAnchor'];prior=x['normalizedOperatingEbitAnchor']*(1-c['tax']);rows=[];pv=0
  for i in range(10):
   rev=p['year1Revenue'] if i==0 else rev0*(1+p['growthAfterYear1'][i-1])
   margin=p['marginYear1']+(p['marginYear5']-p['marginYear1'])*i/4 if i<=4 else p['marginYear5']+(p['marginYear10']-p['marginYear5'])*(i-4)/5
   ebit=rev*margin;tax=max(ebit,0)*c['tax'];nopat=ebit-tax
   da=rev*c['physicalAndInternalSoftwareDaRatio'];capexratio=p['grossCapexRatioYear1']+(p['grossCapexRatioYear10']-p['grossCapexRatioYear1'])*i/9;gross=max(da,rev*capexratio)
   comm=max(0,rev-rev0)*c['netCommissionPerIncrementalRevenue'];wc=max(0,rev-rev0)*c['otherWcPerIncrementalRevenue']
   reinvestfloor=gross-da+comm+wc
   if c.get('fundAllPositiveNopatGrowth',True):growth=max(0,nopat-prior)/p['roic']
   else:growth=max(0,rev-rev0)/rev0*max(0,nopat)/p['roic']
   investment=max(reinvestfloor,growth);extra=investment-reinvestfloor
   shield=c['annualSelectedAcquisitionTaxShield'] if i<c['taxShieldYears'] else 0
   fcff=nopat-investment+shield
   df=(1+p['wacc'])**(i+1);pv+=fcff/df
   sbcratio=p['sbcMemoRatioYear1']+(p['sbcMemoRatioYear10']-p['sbcMemoRatioYear1'])*i/9
   rows.append({'year':2027+i,'periodEnd':f'{2027+i}-11-03','revenue':rev,'growth':rev/rev0-1,'operatingMarginAfterSbcBeforeAcquiredAmort':margin,'sbcExpenseMemo':rev*sbcratio,'ebitAfterSbcBeforeAcquiredAmort':ebit,'taxWithoutUnverifiedAmortShield':tax,'nopat':nopat,'physicalAndInternalSoftwareDa':da,'grossCapitalInvestmentFloor':gross,'netCommissionInvestment':comm,'otherWorkingCapitalInvestment':wc,'growthReinvestmentFloor':growth,'additionalGrowthInvestment':extra,'netReinvestment':investment,'selectedAcquisitionTaxShield':shield,'fcff':fcff,'pv':fcff/df})
   rev0=rev;prior=nopat
  g=p['g'];tr=rev0*(1+g);tn=prior*(1+g);tda=tr*c['physicalAndInternalSoftwareDaRatio'];tc=max(tda,tr*p['grossCapexRatioYear10']);tcomm=(tr-rev0)*c['netCommissionPerIncrementalRevenue'];twc=(tr-rev0)*c['otherWcPerIncrementalRevenue'];ti=max(tc-tda+tcomm+twc,tn*g/p['roic']);tf=tn-ti;tv=tf/(p['wacc']-g);tpv=tv/(1+p['wacc'])**10;ev=pv+tpv
  out[name]={'rows':rows,'pvExplicit':pv,'terminalNopat':tn,'terminalReinvestment':ti,'terminalFcff':tf,'pvTerminal':tpv,'enterpriseValue':ev,'capitalBridge':bridge,'equityValue':ev+bridge,'sharesMillions':shares,'conditionalValuePerShare':(ev+bridge)/shares,'terminalShareOfEV':tpv/ev,'actualCapitalCertified':False}
 return out
if __name__=='__main__':
 r=calculate(X);(P/'results.json').write_text(json.dumps(r,indent=2))
 for name,v in r.items():
  with (P/f'{name}_10years.csv').open('w',newline='') as f:
   w=csv.DictWriter(f,fieldnames=v['rows'][0]);w.writeheader();w.writerows(v['rows'])
 print({n:round(v['conditionalValuePerShare'],4) for n,v in r.items()})
