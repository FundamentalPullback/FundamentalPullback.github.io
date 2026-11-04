"""Conditional operations economics. Not total certified share valuation."""
from pathlib import Path
import json,copy,csv
P=Path(__file__).parent
I=json.loads((P/'inputs.json').read_text())
def run(case='base',overrides=None):
 x=copy.deepcopy(I); c=x['cases'][case]
 for k,v in (overrides or {}).items():
  if k in c:c[k]=v
  else:x[k]=v
 rows=[];prevrev=x['anchorRevenue'];prevnop=x['anchorEbitBeforeAcquiredAmort']*(1-c['tax'])
 for j in range(10):
  rev=c['firstRevenue'] if j==0 else prevrev*(1+c['growth'][j])
  margin=c['margins'][j]+x.get('marginUplift',0)
  ebit=rev*margin+x.get('matchedPlanAnnualAdd',0)
  tax=ebit*c['tax'];nop=ebit-tax
  da=rev*x['physicalSoftwareDaRatio']; capfloor=da*x['capexDaFloor']
  wc=max(0,rev-prevrev)*x['incrementalWcRatio']
  legacy=x['legacyWcFunding'][j]+x.get('recurringWcLeakage',0)
  delta=max(0,nop-prevnop); revenue_component=max(0,rev-prevrev)*max(0,prevnop/prevrev)
  unfunded_efficiency=max(0,delta-revenue_component)*(1-x.get('marginRecoveryFunding',1))
  econ=(delta-unfunded_efficiency)/c['roic']
  physical=max(0,capfloor-da)+wc+x['otherInvestmentAnnual']
  reinv=max(econ,physical)+legacy
  capex=da+reinv-wc-legacy-x['otherInvestmentAnnual']
  fcf=nop-reinv;pv=fcf/(1+c['discount'])**(j+1)
  rows.append(dict(year=j+1,periodEnd=f'{2027+j}-11-04',revenue=rev,margin=margin,ebitBeforeAcquiredAmort=ebit,selectedCashTax=tax,nopat=nop,physicalSoftwareDa=da,grossCapexFloor=capfloor,workingCapitalGrowth=wc,legacyWcFunding=legacy,otherInvestment=x['otherInvestmentAnnual'],economicNetInvestment=econ,physicalNetInvestment=physical,totalNetInvestment=reinv,impliedGrossCapex=capex,fcff=fcf,pv=pv))
  prevrev,prevnop=rev,nop
 g=c['terminalGrowth'];rev=rows[-1]['revenue']*(1+g);nop=rows[-1]['nopat']*(1+g);da=rows[-1]['physicalSoftwareDa']*(1+g)
 wc=max(0,rev-rows[-1]['revenue'])*x['incrementalWcRatio'];econ=max(0,nop-rows[-1]['nopat'])/c['roic'];phys=max(0,da*x['capexDaFloor']-da)+wc+x['otherInvestmentAnnual']*(1+g)
 reinv=max(econ,phys)+x.get('recurringWcLeakage',0)*(1+g); fcf=nop-reinv
 tv=fcf/(c['discount']-g);pvtv=tv/(1+c['discount'])**10
 ev=sum(r['pv'] for r in rows)+pvtv
 b=x['bridge'];bridge=b['cash']-b['selectedOperatingCash']-b['debtCarryingProxy']-b['grossPensionAndRetireeReserve']-b['selectedTaxReserve']-b['netInvestmentSwaps']-b['selectedOtherClaims']-b['nci']
 residual=ev+bridge;per=residual/x['sharesProxy']
 return {'case':case,'rows':rows,'terminal':dict(revenue=rev,nopat=nop,da=da,wc=wc,economicReinvestment=econ,physicalReinvestment=phys,netInvestment=reinv,fcff=fcf,value=tv,pv=pvtv),'operatingEV':ev,'selectedBridge':bridge,'economicResidual':residual,'economicResidualPerShareProxy':per,'conditionalPositivePrice':per if per>0 else None,'totalFairValue':None,'assumptions':c}
if __name__=='__main__':
 out={k:run(k) for k in I['cases']};(P/'results.json').write_text(json.dumps(out,indent=2)+'\n')
 for k,r in out.items():
  with (P/f'{k}_10years.csv').open('w') as f:
   w=csv.DictWriter(f,fieldnames=r['rows'][0]);w.writeheader();w.writerows(r['rows'])
 print({k:v['economicResidualPerShareProxy'] for k,v in out.items()})
