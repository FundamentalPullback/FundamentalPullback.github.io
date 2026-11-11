import json,pathlib,math
P=pathlib.Path(__file__).resolve().parents[1]
d=json.loads((P/'results_decision.json').read_text()); inputs=json.loads((P.parent/'prior/model_inputs.json').read_text());checks={}
for name in ['base','bear','bull']:
 c=inputs[name];w=d['wacc'] if name=='base' else c['wacc'];rev=31152;pv=0
 for t in range(1,11):
  prev=rev
  growth=(c['rev1']/rev-1) if t==1 else c['growth'][t-2] if t<=5 else c['growth'][-1]+(c['g']-c['growth'][-1])*(t-5)/5
  rev*=1+growth
  margin=c['margin'][t-1] if t<=5 else c['margin'][-1]+(c['terminal_margin']-c['margin'][-1])*(t-5)/5
  n=rev*margin*.74;a=max(0,(t-5)/5)
  ri=(rev*(c['capex']-c['da'])+(rev-prev)*c['nwc'])*(1-a)+n*growth/c['roic']*a
  pv+=(n-ri)/(1+w)**(t-d['offset'])
  checks[f'{name}_year{t}']=abs((n-ri)-d['cases'][name]['rows'][t-1]['fcff'])<1e-8
 tv=n*(1+c['g'])*(1-c['g']/c['roic'])/(w-c['g'])/(1+w)**(10-d['offset'])
 val=(pv+tv-1610)/62.153154
 checks[name+'_price']=abs(val-d['cases'][name]['price'])<1e-8
 checks[name+'_current_upside']=abs(d['cases'][name]['upside']-(val/47.28-1))<1e-8
checks['wacc']=abs(d['wacc']-(.0498+1.08*.0441)*.65-.07*.74*.35)<1e-12
for n,value in d['finite_gap_years'].items():
 expected=d['cases']['base']['price']+sum(105.78/(1+d['wacc'])**(t-d['offset']) for t in range(1,int(n)+1))/62.153154
 checks['finite'+n]=abs(expected-value)<1e-8
checks['null_fair']=d['canonical_fair_value'] is None
result={'independent':True,'checks':checks,'count':len(checks),'passed':all(checks.values())}
(P/'audit/independent_results.json').write_text(json.dumps(result,indent=2)); print(result)
