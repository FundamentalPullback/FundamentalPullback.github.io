import json,copy
from pathlib import Path
P=Path(__file__).resolve().parents[1];i=json.loads((P/'legacy_inputs.json').read_text());out=json.loads((P/'results.json').read_text())
weight=i['opcoDebtPrincipal']/(i['opcoDebtPrincipal']+(i['classA']+i['noncontrollingUnitsProxy'])*47.2)
def rate(b):return (.0498+b*.0441)*(1-weight)+.06*.74*weight
def paired(b,yrs):return (570.7-485.088)/yrs*sum((1+.0498+b*.0441)**-t for t in range(1,yrs+1))
def compute(a):
 r=i['revenue'];prev=(821.034-a.get('reversalNormalization',9.221))*(1-a['tax']);flows=[];rows=[]
 for t in range(1,12):
  g=a['growth'][t-1] if t<=5 else a['growth'][4]+(a['tg']-a['growth'][4])*(t-5)/5 if t<=10 else a['tg']
  new=r*(1+g);m=a['margin'][min(t,5)-1]+a.get('marginShift',0);n=new*m*(1-a['tax']);dep=16.48*new/i['revenue'];physical=max(dep*1.25,a['capexFloor']*new/i['revenue'])-dep+a['wc']*max(0,new-r)
  econ=n*g/a['roic'] if t==11 else max(0,prev*g if a.get('efficiency') else n-prev)/a['roic']
  f=n-max(0,physical,econ);flows.append(f);rows.append((new,n,f));r=new;prev=n
 ev=sum(v/(1+a['discount'])**t for t,v in enumerate(flows[:10],1))+flows[-1]/(a['discount']-a['tg'])/(1+a['discount'])**10
 awards=a.get('awards',12);A=119.694115+awards*a.get('awardShareA',1);U=119.694115+131.887106+awards;alloc=a.get('repurchaseParentFraction',1)
 op=123.311-a.get('operatingReserve',123.311)-3701.903-16.7-a.get('earnout',99.456)+3.004-a.get('legacyEmployeeReserve',103.258)+a.get('investmentCredit',0)-50*(1-alloc)-.424-.7-a.get('unitDistribution',.06)*131.887106
 par=45.5-50*alloc-8.7-a.get('tra',485.088)+a.get('dtaCredit',0)-3.097-.13*119.694115
 value=(ev+op)/U+par/A
 fund=max(0,-min(sum(flows[:k]) for k in range(1,11)))
 return dict(value=value,ev=ev,op=op,parent=par,peak=fund,first=flows[0])
checks={}
for key,c in out['cases'].items():
 q=compute(c['assumptions'])
 for k,j in [('value','conditionalClassAResidual'),('ev','ev'),('op','opcoBridge'),('parent','parentBridge'),('peak','peakFunding')]:assert abs(q[k]-c[j])<1e-8,(key,k)
 checks[key]=q
assert abs(rate(1)-out['rates']['normalized_beta_wacc'])<1e-12
assert abs(rate(.54)-out['rates']['observed_beta_wacc'])<1e-12
inverse={}
for b in [.54,1]:
 for eff in [False,True]:
  a=copy.deepcopy(out['cases']['normalized_beta']['assumptions']);a.update(discount=rate(b),dtaCredit=paired(b,10),efficiency=eff)
  def fn(z):a['marginShift']=z;return compute(a)['value']
  values=[fn(-.15+.95*k/1000) for k in range(1001)];assert all(v>w for w,v in zip(values,values[1:]))
  lo=-.15;hi=.8
  for _ in range(100):
   mid=(lo+hi)/2
   if fn(mid)>47.2:hi=mid
   else:lo=mid
  m=(lo+hi)/2;key=str((b,eff));assert abs(m-out['inverse'][key]['margin_shift'])<1e-9
  fn(m);inverse[key]=dict(shift=m,monotonic_intervals=1000,**compute(a))
result=dict(cases=checks,rates=dict(normalized=rate(1),observed=rate(.54)),inverse=inverse,all_pass=True,scope='Independent cashflow/capital/rate/inverse reconstruction, no model import; not audit of source actuals or exact legal capital census')
(P/'audit/output.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
