import json,copy
from pathlib import Path
p=Path(__file__).parent;i=json.loads((p/'legacy_inputs.json').read_text())
def calc(case='base',over=None):
 s=copy.deepcopy(i['scenarios'][case]);s.update(over or {});rev=i['revenue'];np=(i['ebitBeforeDisclosedIntangibleAmortExRemeasurement']-s.get('reversalNormalization',i['selectedReversalNormalization']))*(1-s['tax']);rows=[]
 for y in range(1,11):
  g=s['growth'][y-1] if y<=5 else s['growth'][-1]+(s['tg']-s['growth'][-1])*(y-5)/5;m=(s['margin'][y-1] if y<=5 else s['margin'][-1])+s.get('marginShift',0);r=rev*(1+g);n=r*m*(1-s['tax']);da=i['depreciation']*r/i['revenue'];capex=max(1.25*da,s['capexFloor']*r/i['revenue']);wc=max(0,s['wc']*(r-rev));physical=capex-da+wc;economic=max(0,n-np)/s['roic'] if not s.get('efficiency',False) else max(0,np*g)/s['roic'];ri=max(physical,economic,0);f=n-ri
  rows.append(dict(year=y,revenue=r,growth=g,margin=m,ebitBeforeIntangibleAmort=r*m,nopat=n,depreciation=da,capex=capex,wc=wc,physicalFloor=physical,economicFloor=economic,reinvestment=ri,fcff=f,pv=f/(1+s['discount'])**y));rev=r;np=n
 g=s['tg'];r=rev*(1+g);n=r*(s['margin'][-1]+s.get('marginShift',0))*(1-s['tax']);da=i['depreciation']*r/i['revenue'];physical=max(1.25*da,s['capexFloor']*r/i['revenue'])-da+s['wc']*rev*g;economic=n*g/s['roic'];ri=max(physical,economic,0);f=n-ri;tv=f/(s['discount']-g)/(1+s['discount'])**10;ev=sum(x['pv'] for x in rows)+tv
 awards=s.get('awards',i['selectedAwards']);a=i['classA']+awards*s.get('awardShareA',1);u=i['classA']+i['noncontrollingUnitsProxy']+awards
 # Repurchase cash timing and legal-entity funding are not fully reconciled. Stress allocation, never omit cash outflow.
 alloc=s.get('repurchaseParentFraction',1);opco= -s.get('legacyEmployeeReserve',i['legacyDeferredComp']+i['legacyAcquisitionIncentiveLiability'])+s.get('investmentCredit',0)+i['opcoCash']-s.get('operatingReserve',i['selectedOpcoOperatingReserve'])-i['opcoDebtPrincipal']-i['accruedInterestFees']-s.get('earnout',i['contingentLiability'])+i['contingentAsset']-i['postSeptemberRepurchaseCash']*(1-alloc)-i['declaredTaxDistributionsOpco']-i['selectedLegacyUnitDistributionReserve']-s.get('unitDistribution',i['selectedFutureUnitDistribution'])*i['noncontrollingUnitsProxy']
 parent=i['parentCash']-i['postSeptemberRepurchaseCash']*alloc-i['parentApAndOtherLiabilities']-s.get('tra',i['parentTra'])+s.get('dtaCredit',0)-i['exciseTaxReserveParent']-i['nextDividendA']*i['classA']
 residual=(ev+opco)/u+parent/a
 return dict(case=case,assumptions=s,rows=rows,terminal=dict(revenue=r,nopat=n,depreciation=da,physicalFloor=physical,economicFloor=economic,reinvestment=ri,fcff=f,pv=tv),ev=ev,parentBridge=parent,opcoBridge=opco,classAProxy=a,allEconomicUnitsProxy=u,conditionalClassAResidual=residual,terminalShare=tv/ev,peakFunding=max(0,-min(sum(x['fcff'] for x in rows[:k]) for k in range(1,11))))
def inverse(eff=False):
 lo=-.15;hi=.8;fn=lambda x:calc('base',{'marginShift':x,'efficiency':eff})['conditionalClassAResidual']-i['close'];assert fn(lo)*fn(hi)<0
 z=[fn(lo+(hi-lo)*k/1000) for k in range(1001)];assert all(b>a for a,b in zip(z,z[1:]))
 for _ in range(100):
  mid=(lo+hi)/2
  if fn(mid)>0:hi=mid
  else:lo=mid
 x=(lo+hi)/2;o=calc('base',{'marginShift':x,'efficiency':eff});assert abs(fn(x))<1e-7
 return dict(marginShiftPp=x*100,terminalMargin=o['assumptions']['margin'][-1]+x,firstFcff=o['rows'][0]['fcff'],peakFunding=o['peakFunding'],residual=fn(x),monotonicIntervals=1000,efficiency=eff)

# Existing tax attributes: matched benefit/payments, not gross TRA plus zero asset.
price=47.20
rf=.0498;erp=.0441;debt_cost=.06;tax=.26
capital_proxy=(i['classA']+i['noncontrollingUnitsProxy'])*price
debt_weight=i['opcoDebtPrincipal']/(i['opcoDebtPrincipal']+capital_proxy)
def discount(beta=1,weight=debt_weight,kd=debt_cost):
 ke=rf+beta*erp
 return ke*(1-weight)+kd*(1-tax)*weight,ke
def paired(years=10,ke=.0939):
 # Timing is an analytical illustration; no payment schedule is disclosed.
 return sum((570.7-i['parentTra'])/years/(1+ke)**y for y in range(1,years+1))
def run(name,case='base',beta=1,over=None,years=10):
 w,ke=discount(beta)
 args={'discount':w,'tra':0,'dtaCredit':paired(years,ke)}
 args.update(over or {})
 x=calc(case,args);x.update(name=name,price_reference=price,ke=ke,proxy_debt_weight=debt_weight,paired_tax_years_assumed=years)
 return x
cases={
 'normalized_beta':run('normalized_beta'),
 'observed_beta':run('observed_beta',beta=.54),
 'normalized_beta_efficiency':run('normalized_beta_efficiency',over={'efficiency':True}),
 'observed_beta_efficiency':run('observed_beta_efficiency',beta=.54,over={'efficiency':True}),
 'adverse':run('adverse','bear',over={'discount':.10,'tra':i['parentTra'],'dtaCredit':0,'earnout':200}),
 'recovery':run('recovery','bull'),
 'observed_beta_recovery':run('observed_beta_recovery','bull',beta=.54),
 'generous_claims_observed_beta':run('generous_claims_observed_beta',beta=.54,over={'efficiency':True,'operatingReserve':0,'legacyEmployeeReserve':0,'investmentCredit':109.9,'awards':0,'dtaCredit':85.612}),
}
sens={}
for k,vs in {'discount':[.065,.07,.075,.08,.085,.095], 'tax_years':[5,10,15], 'tax':[.21,.26,.30], 'awards':[8,12,16], 'capexFloor':[70,100,150], 'tra_stress':[0,485.088,727.632], 'roic':[.15,.20,.25]}.items():
 sens[k]=[]
 for v in vs:
  if k=='tax_years': x=run(k,years=v)
  elif k=='tra_stress': x=run(k,over={'tra':v,'dtaCredit':0})
  else:x=run(k,over={k:v})
  sens[k].append({'input':v,'conditional_value':x['conditionalClassAResidual']})
inverses={}
for beta in [.54,1]:
 for eff in [False,True]:
  lo=-.15;hi=.8
  def fun(q):return run('inverse',beta=beta,over={'marginShift':q,'efficiency':eff})['conditionalClassAResidual']-price
  assert fun(lo)*fun(hi)<0
  for _ in range(100):
   mid=(lo+hi)/2
   if fun(mid)>0:hi=mid
   else:lo=mid
  v=(lo+hi)/2;x=run('inverse',beta=beta,over={'marginShift':v,'efficiency':eff})
  inverses[str((beta,eff))]={'margin_shift':v,'terminal_margin':.27+v,'first_fcff':x['rows'][0]['fcff'],'peak_funding':x['peakFunding'],'residual':fun(v)}
out={'method':'Conditional economic class-A values, not execution approval; dated October26 capital proxies and analytical tax timing','date':'2026-11-11','quote_date':'2026-11-10','quote':price,'rates':{'risk_free':rf,'erp':erp,'debt_cost_assumption':debt_cost,'debt_weight_proxy':debt_weight,'normalized_beta_wacc':discount(1)[0],'observed_beta_wacc':discount(.54)[0]},'cases':cases,'sensitivities':sens,'inverse':inverses}
(p/'results.json').write_text(json.dumps(out,indent=2))
print({k:round(v['conditionalClassAResidual'],3) for k,v in cases.items()});print(inverses)
