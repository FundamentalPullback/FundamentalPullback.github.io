# Independent reconstruction from serialized scenario assumptions, no model import.
import json, math, copy
from pathlib import Path
P=Path(__file__).resolve().parents[1]
x=json.loads((P/'results.json').read_text())
def ev(a):
 r=a['revenue']; flows=[]; last=0
 for t in range(1,11):
  g=a['growth'] if t<=5 else a['growth']+(a['growth10']-a['growth'])*(t-5)/5
  old=r;r*=1+g
  m=a['margin0']+(a['margin5']-a['margin0'])*min(1,t/a.get('margin_year',5))
  rec=0 if a.get('restruct_reserved') and t<=3 else a['restruct']
  n=(r*(m-rec)+a.get('synergy',0)*min(t/3,1))*(1-a['tax'])
  investment=r*(a['capex']+a['lease_capex']-a['da'])+(r-old)*a['nwc']
  blend=max(0,(t-5)/5);investment=investment*(1-blend)+n*g/a['terminal_roic']*blend
  flows.append(n-investment-a.get('extra_costs',{}).get(str(t),0));last=n
 terminal=last*(1+a['tg'])*(1-a['tg']/a['terminal_roic'])/(a['wacc']-a['tg'])
 return sum(v/(1+a['wacc'])**t for t,v in enumerate(flows,1))+terminal/(1+a['wacc'])**10,flows

def calc(c):
 h,hf=ev(c['hpc']);f,ff=ev(c['foods']);_,pf=ev(c['pre'])
 w=c['hpc']['wacc'];d=c['delay'];fx=c['fx'];fw=c['foods']['wacc']
 v=pf[0]*d/(1+w)**(d/2)+h/(1+w)**d+15.7/fx/(1+w)**d+(.65*(f-4.6871-15.7-.75)/fx)/(1+fw)**d-c['claims']+c['assets']-.121533558*19.89/1.1214+.121533558*19.89/fx
 v-=sum(c['cost']*weight/(1+w)**(d+offset) for offset,weight in enumerate([.5,.3,.2]))
 return v/c['shares']*fx
checks={}
for name,c in x['cases'].items():
 value=calc(c['assumptions']);expected=c['result']['value_usd'];assert abs(value-expected)<1e-9
 checks[name]={'independent':value,'expected':expected,'delta':value-expected}
c=copy.deepcopy(x['cases']['central']['assumptions']);c['hpc']['margin5']=x['reverse_margin_year10'];c['hpc']['margin_year']=10
checks['reverse']={'value':calc(c),'target':x['price']};assert abs(calc(c)-x['price'])<1e-8
base=copy.deepcopy(x['cases']['central']['assumptions'])
for name,target in x['sensitivity'].items():
 c=copy.deepcopy(base)
 if name=='sales_roll_to_assumed_close':
  for k in ['hpc','foods']: c[k]['revenue']*= (1+c[k]['growth'])**c['delay']
 elif name.startswith('hpc_wacc_'): c['hpc']['wacc']=float(name.split('_')[-1])
 elif name.startswith('fx_'): c['fx']=float(name[3:])
 elif name.startswith('claims_delta_'): c['claims']+=float(name.split('_')[-1])
 elif name.startswith('cost_'): c['cost']=float(name[5:])
 elif name.startswith('margin_year10_'): c['hpc'].update(margin5=float(name.split('_')[-1]),margin_year=10)
 else: raise ValueError(name)
 value=calc(c);assert abs(value-target)<1e-8,(name,value,target)
 checks[name]={'independent':value,'expected':target}
(P/'audit/output.json').write_text(json.dumps(checks,indent=2));print(json.dumps(checks,indent=2))
