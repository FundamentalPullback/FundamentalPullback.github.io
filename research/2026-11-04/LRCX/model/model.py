from pathlib import Path
import json,copy,csv
P=Path(__file__).parent
I=json.loads((P/'inputs.json').read_text());C=json.loads((P.parent/'capital/facts.json').read_text())
def capital(c=C):
 claims={k:c[k] for k in ['operatingCashReserveSelected','notesPrincipal','financeLeaseProxySelected','debtExtraSelected','taxReserveSelected','additionalCurrentTaxReserveSelected','dividendPayable','buybackPayable','additionalCapexReserveSelected','definedBenefitOtherClaimReserveSelected']}
 return {'cash':c['cash'],'claims':claims,'netBridge':c['cash']+c['deferredCompNetAddedSelected']-sum(claims.values()),'selectedShares':c['coverShares']+c['incrementalAwardsSelected'],'notCertifiedCurrentCapitalization':True}
def value(case='base',overrides=None,c=None):
 i=copy.deepcopy(I);s=i['scenarios'][case]
 for k,v in (overrides or {}).items():
  if k in s:s[k]=v
  else:i[k]=v
 b=capital(c or C);rev0=i['anchorRevenue'];tax=i['tax'];np0=i['anchorEbit']*(1-tax); rows=[];pv=0
 for n in range(10):
  rev=s['revenue1'] if n==0 else rev*(1+s['growth'][n-1])
  margin=s['margins'][n]+i.get('marginShift',0);ebit=rev*margin;np=ebit*(1-tax)
  da=rev*s['physicalDaRatio'];am=i['acquiredAmortAnnual']*max(0,1-n/5);cash_tax=ebit*tax;gaap_ebit=ebit-am
  wc=max(0,rev-rev0)*i['workingCapitalRatio'];capex=rev*(s['capexRatio']+i.get('extraCapexRatio',0));physicalnet=max(0,capex-da)+wc
  economic=max(0,np-np0)/s['roic'];netinvest=max(physicalnet,economic)
  fundedcapex=da+netinvest-wc
  capSbc=rev*i['additionalCapitalizedSbcRatio'];fcff=gaap_ebit-cash_tax+da+am-fundedcapex-wc-capSbc
  # Both algebraic identities preserve no fictitious acquired-amortization tax shield.
  assert abs(fcff-(np-netinvest-capSbc))<1e-7
  t=n+1-i.get('midyearShift',0);p=fcff/(1+s['discount'])**t;pv+=p
  rows.append({'year':2027+n,'periodEnd':f'{2027+n}-11-04','revenue':rev,'marginBeforeAcquiredAmort':margin,'ebitBeforeAcquiredAmort':ebit,'acquiredAmort':am,'gaapEbitIllustrative':gaap_ebit,'cashTax':cash_tax,'nopatBeforeAcquiredAmort':np,'physicalSoftwareDa':da,'totalDa':da+am,'physicalCapexFloor':capex,'workingCapitalInvestment':wc,'physicalNetInvestmentFloor':physicalnet,'economicNetInvestmentFloor':economic,'selectedNetInvestment':netinvest,'fundedTotalCapexEquivalent':fundedcapex,'additionalCapitalizedSbcCost':capSbc,'fcff':fcff,'discountYears':t,'pv':p})
  rev0=rev;np0=np
 rt=rev*(1+s['g']);et=rt*(s['margins'][-1]+i.get('marginShift',0));nt=et*(1-i['terminalTax']);dt=rt*s['physicalDaRatio'];ct=rt*(s['capexRatio']+i.get('extraCapexRatio',0));wt=rev*s['g']*i['workingCapitalRatio'];econ=nt*s['g']/s['roic'];phys=max(0,ct-dt)+wt;reinv=max(econ,phys);sbc=rt*i['additionalCapitalizedSbcRatio'];tf=nt-reinv-sbc;tv=tf/(s['discount']-s['g']);pvt=tv/(1+s['discount'])**(10-i.get('midyearShift',0));ev=pv+pvt;eq=ev+b['netBridge']
 return {'scenario':case,'assumptions':s,'rows':rows,'terminal':{'revenue':rt,'cashTaxRate':i['terminalTax'],'nopat':nt,'physicalSoftwareDa':dt,'capexFloor':ct,'workingCapitalInvestment':wt,'economicNetFloor':econ,'physicalNetFloor':phys,'netInvestment':reinv,'additionalCapitalizedSbcCost':sbc,'fcff':tf,'value':tv,'pv':pvt},'pvExplicit':pv,'enterpriseValue':ev,'capitalBridge':b,'equityValueConditional':eq,'perShareConditional':eq/b['selectedShares'],'terminalPvShare':pvt/ev,'priceGap':eq/b['selectedShares']/i['price']-1,'economicDominatesYears':sum(r['economicNetInvestmentFloor']>=r['physicalNetInvestmentFloor'] for r in rows)}
def main():
 result={s:value(s) for s in I['scenarios']};(P/'results.json').write_text(json.dumps(result,indent=2)+'\n')
 for s,d in result.items():
  with (P/f'{s}_10years.csv').open('w') as f:
   w=csv.DictWriter(f,fieldnames=list(d['rows'][0]));w.writeheader();w.writerows(d['rows'])
 sens={}
 for key,vals in {'discount':[.10,.12,.14,.16,.18],'g':[.02,.025,.03,.035,.04],'roic':[.20,.25,.35,.45,.60],'tax':[.17,.21,.24,.28],'terminalTax':[.17,.21,.24,.26,.30],'workingCapitalRatio':[.10,.20,.30,.40],'extraCapexRatio':[0,.01,.025],'additionalCapitalizedSbcRatio':[0,.0025,.005],'marginShift':[-.05,-.025,0,.025,.05],'midyearShift':[0,.5]}.items():
  sens[key]=[{'input':v,'perShare':value(overrides={key:v})['perShareConditional']} for v in vals]
 for key,vals in {'operatingCashReserveSelected':[1000,1800,3000],'taxReserveSelected':[762.4,947.249,1200],'additionalCurrentTaxReserveSelected':[0,300,537.576,800.781],'financeLeaseProxySelected':[0,12.502,15,30],'incrementalAwardsSelected':[4.885,6.6,10,15],'additionalCapexReserveSelected':[0,141.965,283.93],'definedBenefitOtherClaimReserveSelected':[0,50,150],'deferredCompNetAddedSelected':[-100,0,13.3]}.items():
  sens[key]=[]
  for v in vals:
   c=copy.deepcopy(C);c[key]=v;sens[key].append({'input':v,'perShare':value(c=c)['perShareConditional']})
 sens['anchorTtmInsteadOfQuarter']={'label':'Unadjusted TTM EBIT9654.434/revenue26127.935 as investment-base stress, not alternate quarter actual','perShare':value(overrides={'anchorRevenue':26127.935,'anchorEbit':9654.434})['perShareConditional']}
 sens['acquiredAmortZero']={s:value(s,{'acquiredAmortAnnual':0})['perShareConditional'] for s in result}
 sens['chinaExportStress']={}
 for cut in [.10,.25,.50]:
  # Persistent loss from 35% China exposure; illustrative margin decline, not geography profit claim.
  s=copy.deepcopy(I['scenarios']['base']);s['revenue1']*=1-.35*cut;s['margins']=[m-.05*cut for m in s['margins']]
  sens['chinaExportStress'][str(cut)]={'chinaSalesHaircut':cut,'marginCompression':.05*cut,'perShare':value(overrides=s)['perShareConditional']}
 (P/'sensitivities.json').write_text(json.dumps(sens,indent=2)+'\n')
 inv={}
 for name,lo,hi in [('marginShift',0,.30),('growthShift',0,.40)]:
  def f(x):
   o={'marginShift':x} if name=='marginShift' else {'growth':[g+x for g in I['scenarios']['base']['growth']]}
   return value(overrides=o)['perShareConditional']
  grid=[{'input':lo+(hi-lo)*j/100,'value':f(lo+(hi-lo)*j/100)} for j in range(101)];mono=all(grid[j+1]['value']>=grid[j]['value']-1e-9 for j in range(100));target=I['price'];sol=None
  if mono and f(lo)<=target<=f(hi):
   for _ in range(100):
    mid=(lo+hi)/2
    if f(mid)<target:lo=mid
    else:hi=mid
   sol=(lo+hi)/2
  inv[name]={'target':target,'solution':sol,'monotone':mono,'grid':grid,'meaning':'Selected base economics only, not consensus or probability; growth shift applies years2–10 only.'}
 (P/'inverse.json').write_text(json.dumps(inv,indent=2)+'\n');print({s:d['perShareConditional'] for s,d in result.items()})
if __name__=='__main__':main()
