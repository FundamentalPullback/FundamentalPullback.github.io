import json,sys,copy,csv,hashlib
from pathlib import Path
P=Path(__file__).parent;sys.path.insert(0,str(P/'model'));import model
I=model.I;I['asOf']='2026-11-11';I['close']=55.74
# Pure nominal USD capital cost: refreshed risk-free, frozen monthly ERP and observed beta.
rf=.0498;erp=.0441;beta=.92;capm=rf+erp*beta
I['scenarios']['bull']['discount']=capm
# Historical tax shield and corresponding TRA are matched once, not separately capitalized again.
def taxpv(rate,years=15):return sum((I['parentDta']-I['parentTra'])/years/(1+rate)**y for y in range(1,years+1))
def case(name='base',extra=None):
 d=I['scenarios'][name]['discount'];ov={'parentTra':0,'parentDtaCredit':taxpv(d),'legacyPartnerCashStress':83.639};ov.update(extra or {})
 x=model.calc(name,ov);x['taxTimingAssumptionYears']=15;x['fundingCushion']=x['selectedLiquid']-x['peakFunding'];x['conditionalFunded']=x['fundingCushion']>=0;x['status']='screen-grade';return x
def reverse(efficiency=False):
 lo=0;hi=1
 def c(v):return case('base',{'marginShift':v,'rampShift':True,'efficiency':efficiency})
 assert c(lo)['conditionalClassAResidual']<I['close']<c(hi)['conditionalClassAResidual']
 for _ in range(100):
  mid=(lo+hi)/2
  if c(mid)['conditionalClassAResidual']>I['close']:hi=mid
  else:lo=mid
 x=c((hi+lo)/2);return {'terminalMargin':.30+(hi+lo)/2,'firstMargin':x['rows'][0]['margin'],'value':x['conditionalClassAResidual'],'fundingNeed':x['peakFunding'],'cashAvailableUnderOpcoAssumption':x['selectedLiquid'],'conditionalFunded':x['conditionalFunded'],'rows':x['rows'],'residual':x['conditionalClassAResidual']-I['close']}
cases={k:case(k) for k in ['bear','base','bull']}
# Structural range excludes impossible free TRA: realized tax relief and TRA travel together.
bounds={}
for k in cases:
 vals=[]
 for share in [0,1]:
  for credit in [0,I['parentDta']-I['parentTra']]:
   x=case(k,{'parentCashShare':share,'parentDtaCredit':credit})
   vals.append(x['conditionalClassAResidual'])
 bounds[k]={'min':min(vals),'max':max(vals),'scope':'fixed operating assumptions; cash location and historical net tax benefit only, not intrinsic value confidence bounds'}
out={'price':55.74,'scannerAfterHours':56.50,'rate':{'riskFree':rf,'erp':erp,'beta':beta,'mechanicalCapm':capm,'selectedBase':.10},'cases':cases,'structuralBounds':bounds,'reverseRamp':reverse(),'fullValue':None,'decision':'wait for proof','status':'not-decision-ready','changes':['Price regular-session corrected','Historical tax shield and TRA valued jointly once','Legacy partnership liability83.639 reserved separately','Bull cost of equity refreshed','Reverse margin improvement ramped over10years and funding feasibility disclosed']}
out['valuationBasis']='conditional ex-distribution residual, not cum-dividend total shareholder value'
out['economicSensitivities']={'bullAtBase10pct':case('bull',{'discount':.10,'parentDtaCredit':taxpv(.10)})['conditionalClassAResidual'],'withoutGrossAwards':{k:case(k,{'awards':0})['conditionalClassAResidual'] for k in cases},'efficiencyReverse':reverse(True),'notEndorsedAlternative':True}
(P/'results.json').write_text(json.dumps(out,indent=2))
with (P/'forecast.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=['scenario']+list(cases['base']['rows'][0]));w.writeheader()
 for n,x in cases.items():
  for r in x['rows']:w.writerow({'scenario':n,**r})
checks=[]
for n,x in cases.items():
 for r in x['rows']:
  assert abs(r['nopat']-r['reinvestment']-r['fcff'])<1e-8
  assert r['reinvestment']>=r['physicalFloor']-1e-8
  checks.append(True)
 assert x['conditionalFunded'];checks.append(True)
assert abs(out['reverseRamp']['residual'])<1e-7
(P/'audit.json').write_text(json.dumps({'mathChecksPassed':len(checks)+1,'economicReady':False,'scope':'formula consistency and conditional aggregate funding only; entity liquidity and economic assumptions not certified'},indent=2))
print(json.dumps({k:{'value':v['conditionalClassAResidual'],'ev':v['ev'],'funding':v['peakFunding']} for k,v in cases.items()},indent=2));print(bounds);print({k:v for k,v in out['reverseRamp'].items() if k!='rows'})
