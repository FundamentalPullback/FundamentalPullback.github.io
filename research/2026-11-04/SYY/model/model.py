import json,copy,csv
from pathlib import Path
P=Path(__file__).resolve().parent;INPUT=json.loads((P/'inputs.json').read_text())
def business(x,case,who):
 b=x['businesses'][who];s=x['scenarios'][case][who];rows=[];rev=b['revenueAnchor'];nop=b['ebitAnchor']*(1-b['tax']);pv=0
 assert s['wacc']>s['g']>=0
 for z in range(10):
  prev=rev;pn=nop;rev*=1+s['growth'][z];margin=s['margin1']+(s['margin5']-s['margin1'])*z/4 if z<5 else s['margin5']+(s['margin10']-s['margin5'])*(z-4)/5
  ebit=rev*margin-b.get('additionalAnnualCompPreTax',0);nop=ebit*(1-b['tax']);da=rev*b['daRatio'];capex=max(da,rev*b['grossCapexRatio']);wc=max(rev-prev,0)*b['wcPerIncrementalRevenue'];growth=max(nop-pn,0)/s['roic'] if b.get('growthFundingMode','fullNopat')=='fullNopat' else max(pn*(rev/prev-1),0)/s['roic'];net=max(capex-da+wc,growth);extra=net-(capex-da+wc);fcff=nop-net;v=fcff/(1+s['wacc'])**(z+1);pv+=v
  rows.append(dict(period=z+1,endDate=f'{2027+z}-11-03',revenue=rev,margin=margin,ebitAfterSbcBeforeAcquiredAmort=ebit,nopat=nop,daPhysical=da,grossCapitalSpending=capex,wcInvestment=wc,otherGrowthInvestment=extra,netReinvestment=net,fcff=fcff,pv=v))
 nr=rev*(1+s['g']);nn=nop*(1+s['g']);physical=max(nr*b['grossCapexRatio']-nr*b['daRatio'],0)+(nr-rev)*b['wcPerIncrementalRevenue'];tnet=max(nn*s['g']/s['roic'],physical);tf=nn-tnet;tpv=tf/(s['wacc']-s['g'])/(1+s['wacc'])**10
 return dict(rows=rows,explicitPv=pv,terminalPv=tpv,terminalNopat=nn,terminalNetReinvestment=tnet,terminalFcff=tf,enterpriseValue=pv+tpv)
def run(case='base',override=None):
 x=copy.deepcopy(INPUT)
 for key,v in (override or {}).items():
  d=x;parts=key.split('.')
  for p in parts[:-1]:d=d[p]
  d[parts[-1]]=v
 syy=business(x,case,'syy');jrd=business(x,case,'jrd');c=x['capital'];t=x['transaction'];bridge=c['cashSeptember']-sum(c[k] for k in ['debtCarryingSeptember','bookToPrincipalAndHedgeReserve','operatingCashReserve','pensionGrossDeficitJune','utbAndInterest','historicalTaxTimingReserve','octoberFinancingCostReserve'])+c['postSeptemberOtherNetCapital'];s=x['scenarios'][case];w=s['jrd']['wacc'];g=s['jrd']['g'];tax=x['businesses']['jrd']['tax'];roic=s['jrd']['roic'];synrows=[];synpv=0;prevn=0
 for z,(benefit,cost) in enumerate(zip(s['synergyAnnual'],s['integrationAnnual'])):
  # Synergy margin uplift is not free: finance incremental positive normalized after-tax savings at the same incremental return.
  n=benefit*(1-tax);rein=max(n-prevn,0)/roic;flow=n-cost*(1-tax)-rein;v=flow/(1+w)**(z+1);synpv+=v;prevn=n;synrows.append(dict(period=z+1,pretaxSavings=benefit,integrationCost=cost,afterTaxSavings=n,growthReinvestment=rein,fcff=flow,pv=v))
 tn=prevn*(1+g);tfcf=tn*(1-g/roic);synterm=tfcf/(w-g)/(1+w)**10;synvalue=synpv+synterm
 common=x['sharesStandalone'];standalone=(syy['enterpriseValue']+bridge)/common;failurecost=t['conditionalRegulatoryFailureFee']+t['specialRedemptionEligiblePrincipalProxy']*t['redemptionPremiumFraction']+t['failureOtherCostReserve'];failure=(syy['enterpriseValue']+bridge-failurecost)/common
 closeequity=syy['enterpriseValue']+jrd['enterpriseValue']+synvalue+bridge-t['economicCashFreeDebtFreeBase']-t['buyerCostReserve']-t['closingAdjustmentReserve'];closevalue=closeequity/(common+x['conditionalSellerShares'])
 return dict(case=case,syy=syy,jrd=jrd,synergyRows=synrows,synergyValue=synvalue,synergyTerminalPv=synterm,capitalBridgeProxy=bridge,standaloneBeforeFailureCosts=standalone,conditionalRegulatoryFailureCosts=failurecost,conditionalFailureValuePerShare=failure,conditionalImmediateCloseEquity=closeequity,conditionalImmediateCloseShares=common+x['conditionalSellerShares'],conditionalImmediateCloseValuePerShare=closevalue,totalCurrentFairValue=None,noProbabilityAssigned=True,valuationMeaning='Separate conditional economic cases assuming immediate resolution; not final actual closing funds flow, current target, or probability interval.')
if __name__=='__main__':
 out={c:run(c) for c in INPUT['scenarios']};(P/'results.json').write_text(json.dumps(out,indent=2)+'\n')
 for c,r in out.items():
  for who in ['syy','jrd']:
   with (P/f'{c}_{who}_10_years.csv').open('w',newline='') as f:
    wr=csv.DictWriter(f,fieldnames=r[who]['rows'][0].keys());wr.writeheader();wr.writerows(r[who]['rows'])
 print({c:{'failure':v['conditionalFailureValuePerShare'],'close':v['conditionalImmediateCloseValuePerShare']} for c,v in out.items()})
