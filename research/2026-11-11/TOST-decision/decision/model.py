import json,copy,math
from pathlib import Path
P=Path(__file__).parent
I=json.loads((P/'legacy_inputs.json').read_text())
def calc(name='base',over=None):
 s=copy.deepcopy(I['scenarios'][name]);s.update(over or {});rev=I['revenue'];nopat=I['normalizedEbitBeforeAcquiredAmort']*(1-s['tax']);loan=0 if s.get('separateHfi') else I['loanAsset'];comm=I['commissionAsset'];rows=[]
 for y in range(1,11):
  g=s['growth'][y-1] if y<=5 else s['growth'][-1]+(s['terminalGrowth']-s['growth'][-1])*(y-5)/5
  margin=(s['margins'][y-1] if y<=5 else s['margins'][-1])+s.get('marginShift',0)
  newrev=rev*(1+g);ebit=newrev*margin;newnopat=ebit*(1-s['tax']);da=newrev*s['da'];capex=newrev*s['capex'];cap_sbc=newrev*s['capitalizedSbc']
  # Funding starts from observable stock; transition to stable asset/revenue at year10.
  w=1 if y<=5 else (10-y)/5
  loanfund=0 if s.get('separateHfi') else w*newrev*s['loanFunding']+(1-w)*loan*g
  commfund=w*newrev*s['commissionFunding']+(1-w)*comm*g
  wc=s['workingCapital']*(newrev-rev)
  physical=capex-da+cap_sbc+loanfund+commfund+wc
  economic=max(0,newnopat-nopat)/s['roic'] if not s.get('efficiencyMargin',False) else max(0,nopat*g)/s['roic']
  reinvest=max(physical,0) if s.get('bottomUpOnly') else max(physical,economic,0);fcff=newnopat-reinvest
  t=y # rolling annual periods from as-of date, not FY2027
  rows.append(dict(year=y,revenue=newrev,growth=g,margin=margin,ebit=ebit,nopat=newnopat,da=da,capex=capex,capitalizedSbc=cap_sbc,loanFunding=loanfund,commissionFunding=commfund,workingCapital=wc,physicalNetInvestment=physical,economicNetInvestment=economic,reinvestment=reinvest,fcff=fcff,pv=fcff/(1+s['discount'])**t))
  rev=newrev;nopat=newnopat;loan+=loanfund;comm+=commfund
 g=s['terminalGrowth'];r=rev*(1+g);n=r*(s['margins'][-1]+s.get('marginShift',0))*(1-s['tax']);phys=r*(s['capex']-s['da']+s['capitalizedSbc'])+loan*g+comm*g+s['workingCapital']*rev*g;econ=n*g/s['roic'];rein=max(phys,0) if s.get('bottomUpOnly') else max(phys,econ,0);f=n-rein;tv=f/(s['discount']-g);pvtv=tv/(1+s['discount'])**10;ev=sum(x['pv'] for x in rows)+pvtv
 bridge=I['cash']+I['securities']-s.get('operatingCashReserve',I['operatingCashReserve'])-I['warrantClaim']-I['historicalTaxReserve']-s.get('legalCashStress',0)+s.get('nolAdded',0)+(I['loanAsset']*(1-s.get('hfiHaircut',0)) if s.get('separateHfi') else 0)
 shares=s.get('shares',I['dilutedSharesProxy']);value=(ev+bridge)/shares
 return dict(scenario=name,assumptions=s,rows=rows,terminal=dict(revenue=r,nopat=n,physicalNetInvestment=phys,economicNetInvestment=econ,reinvestment=rein,fcff=f,value=tv,pv=pvtv,loanStockYear10=loan,commissionStockYear10=comm),enterpriseValue=ev,bridge=bridge,shares=shares,conditionalResidualPerShare=value,terminalPvFraction=pvtv/ev)
price=34.52
I['dilutedSharesProxy']=I['basicOct30']+I['rsuExpectedVest']+I['optionsExpectedVest']*max(0,1-I['optionExercise']/price)
observed=.0498+1.71*.0441;normalized=.0498+1*.0441
def run(name,case='base',over=None):
 args={'discount':observed,'separateHfi':True,'bottomUpOnly':True}
 args.update(over or {})
 v=calc(case,args);v['label']=name;v['peakCumulativeCashDeficit']=max(0,-min(sum(r['fcff'] for r in v['rows'][:k]) for k in range(1,11)));return v
cases={
 'central_separate_hfi':run('central_separate_hfi'),
 'central_fully_funded_zero_hfi_return':run('central_fully_funded_zero_hfi_return',over={'separateHfi':False}),
 'central_economic_floor':run('central_economic_floor',over={'bottomUpOnly':False}),
 'central_efficiency_floor':run('central_efficiency_floor',over={'bottomUpOnly':False,'efficiencyMargin':True}),
 'central_beta_one':run('central_beta_one',over={'discount':normalized}),
 'recovery_observed_beta':run('recovery_observed_beta','bull'),
 'recovery_10_5_discount':run('recovery_10_5_discount','bull',{'discount':.105}),
 'recovery_beta_one':run('recovery_beta_one','bull',{'discount':normalized}),
 'adverse':run('adverse','bear',{'discount':.145,'legalCashStress':300,'hfiHaircut':.2}),
}
sens={}
for key,vals in {'discount':[.0939,.105,.115,.125211,.135,.145],'loanFunding':[.007,.014,.025],'commissionFunding':[.006,.012,.018],'capex':[.0075,.01,.015],'capitalizedSbc':[0,.0017,.003],'hfiHaircut':[0,.2,1],'legalCashStress':[0,100,300,600],'shares':[595,I['dilutedSharesProxy'],614],'operatingCashReserve':[300,500,800],'marginShift':[-.01,0,.01,.02],'nolAdded':[0,335.53]}.items():
 sens[key]=[]
 for val in vals:
  ov={key:val}
  if key=='loanFunding':ov['separateHfi']=False
  a=run('sensitivity',over=ov);sens[key].append({'input':val,'value':a['conditionalResidualPerShare']})
inverses={}
for k,args in {'observed_bottomup':{},'normalized_bottomup':{'discount':normalized},'observed_economic':{'bottomUpOnly':False},'observed_efficiency':{'bottomUpOnly':False,'efficiencyMargin':True}}.items():
 lo=-.05;hi=.5
 def fn(q):return run('inverse',over=dict(args,marginShift=q))['conditionalResidualPerShare']-price
 assert fn(lo)*fn(hi)<0
 for _ in range(100):
  mid=(lo+hi)/2
  if fn(mid)>0:hi=mid
  else:lo=mid
 q=(lo+hi)/2;v=run('inverse',over=dict(args,marginShift=q))
 inverses[k]={'margin_shift':q,'terminal_margin':.125+q,'first_fcff':v['rows'][0]['fcff'],'peak_deficit':v['peakCumulativeCashDeficit'],'residual':fn(q)}
out={'date':'2026-11-11','quote_date':'2026-11-10','price':price,'rates':{'rf':.0498,'erp_assumption':.0441,'observed_beta':1.71,'observed_discount':observed,'normalized_beta':1,'normalized_discount':normalized},'shares_proxy':I['dilutedSharesProxy'],'method':'Conditional core DCF plus net HFI book-value scenario; future owned-loan activity zero incremental NPV, no free loan interest. Alternative integrated funding case without loan-income separately labelled conservative.','cases':cases,'sensitivities':sens,'inverses':inverses}
(P/'results.json').write_text(json.dumps(out,indent=2));print({k:round(v['conditionalResidualPerShare'],3) for k,v in cases.items()});print(inverses)
