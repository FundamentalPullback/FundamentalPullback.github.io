from pathlib import Path
import json,copy
p=Path(__file__).resolve().parent
inputs=json.loads((p/'inputs.json').read_text())
def calc(name,x=None,margin_shift=0,growth_shift=0):
 x=copy.deepcopy(inputs if x is None else x);c=x['cases'][name];a=x['anchor'];cap=x['capital'];rate=c['wacc'];g=c['terminalGrowth'];tax=x['tax'];roic=c['marginalRoic'];wc=x['workingCapitalPerIncrementalRevenue'];floor=x['physicalCapexToResidualDdaFloor'];da_rate=a['ddaResidual']/a['revenue'];rentextra=x['rentalCashFactor']-1
 prevrev=a['revenue'];prevnop=a['ebitAfterFullCashRent']*(1-tax);rows=[];rev=c['firstRevenue'];pv=0
 for i in range(10):
  if i:rev*=1+c['growth'][i-1]+growth_shift
  margin=c['margins'][i]+margin_shift;rent=a['fullCashRent']*rev/a['revenue']*rentextra;ebit=rev*margin-rent;cash_tax=max(ebit,0)*tax;nop=ebit-cash_tax;da=rev*da_rate
  physical=da*floor;d_wc=max(rev-prevrev,0)*wc;nopat_gain=max(nop-prevnop,0);volume_gain=max(prevnop,0)*max(rev/prevrev-1,0);margin_gain=max(nopat_gain-volume_gain,0);economic=max(nopat_gain-(1-x.get("marginRecoveryCapitalFundingFraction",1))*margin_gain,0)/roic
  netfloor=max(physical-da+d_wc+x['otherInvestingAnnualStress'],0)
  reinvest=max(economic,netfloor);fcff=nop-reinvest;discount=(1+rate)**(i+1);pv+=fcff/discount
  rows.append({'year':2027+i,'revenue':rev,'marginAfterFullCashRent':margin,'rentalStressExtra':rent,'ebitAfterRent':ebit,'tax':cash_tax,'nopat':nop,'residualDda':da,'physicalCapexFloor':physical,'incrementalWc':d_wc,'positiveNopatGrowthCapital':economic,'netPhysicalReinvestmentFloor':netfloor,'reinvestment':reinvest,'impliedGrossCapex':da+reinvest-d_wc-x['otherInvestingAnnualStress'],'otherInvestingStress':x['otherInvestingAnnualStress'],'fcff':fcff,'pv':fcff/discount})
  prevrev=rev;prevnop=nop
 revt=rev*(1+g);ebitt=revt*(c['margins'][-1]+margin_shift)-a['fullCashRent']*revt/a['revenue']*rentextra;nopt=ebitt-max(ebitt,0)*tax;dat=revt*da_rate
 eco=max(nopt*g,0)/roic;phy=max(dat*floor-dat+max(revt-rev,0)*wc+x['otherInvestingAnnualStress'],0);reint=max(eco,phy);fcfft=nopt-reint;tv=fcfft/(rate-g);pvt=tv/(1+rate)**10;ev=pv+pvt
 bridge=cap['cashAugust1']-cap['operatingCashReserveSelected']-cap['notesPrincipal']-cap['septemberDividendProxy']-cap['unreconciledClaimReserveSelected'];eq=ev+bridge
 return {'name':name,'rows':rows,'terminal':{'revenue':revt,'ebit':ebitt,'nopat':nopt,'dda':dat,'economicReinvestment':eco,'physicalReinvestmentFloor':phy,'reinvestment':reint,'fcff':fcfft,'value':tv,'pv':pvt},'operatingEvAfterFullRent':ev,'pvExplicit':pv,'capitalBridgeSelected':bridge,'equityResidual':eq,'equityResidualPerShare':eq/cap['sharesProxy'],'conditionalPriceIfPositive':eq/cap['sharesProxy'] if eq>=0 else None,'fairValueTotal':None}
if __name__=='__main__':
 out={name:calc(name) for name in inputs['cases']};(p/'results.json').write_text(json.dumps(out,indent=2)+'\n')
 for name,r in out.items():print(name,r['equityResidualPerShare'])
