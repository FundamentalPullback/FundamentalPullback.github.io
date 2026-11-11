import pathlib,json,hashlib
P=pathlib.Path(__file__).parent
R=json.loads((P/'results_decision.json').read_text());BASE=json.loads((P.parent/'sources/results.json').read_text());C=BASE['assumptions']
errors=[];checks={}
def eq(name,x,y):
 checks[name]=abs(x-y)<1e-7
 if not checks[name]:errors.append(dict(check=name,actual=x,expected=y))
def calculate(beta=.52,erp=.0441,kd=.06253,tax=.25,replacement=0,cash=0,extra_shares=0,bridge_debt=7822,case='central'):
 c=C[case];e=71.89*331.691829;d=7292;w=(.0498+beta*erp)*e/(e+d)+kd*(1-tax)*d/(e+d)
 core=6458.;pv=[];fcff1=None
 for y in range(1,11):
  t=max(0,(y-5)/5);g=c['g'];o=c['organic'][min(y,5)-1]*(1-t)+g*t;a=c['acq']*(1-t)
  prior=core;core*=1+o+a;rec=core-.5*prior*a;revenue=rec/(1-c['contingent_share']);cont=revenue-rec
  m=c['margin'][min(y,5)-1]*(1-t)+c['terminal_margin']*t
  n=(rec*m+cont*c['contingent_margin']-replacement*revenue)*(1-tax)
  contract=28*revenue/6814;purchase=prior*a*c['acq_price'];budget=max(0,n*g/c['roic']-contract)
  reinvest=(1-t)*(.005*revenue+.15*max(0,prior*o))+t*budget+contract
  f=n-reinvest-purchase
  if y==1:fcff1=f
  pv.append((n-reinvest)/(1+w)**y-purchase/(1+w)**(y-.5))
 terminal=(n*(1+g)-max(n*(1+g)*g/c['roic'],contract*(1+g)))/(w-g)/(1+w)**10
 ev=sum(pv)+terminal;price=(ev-bridge_debt-326-18+cash)/(332.691829+extra_shares)
 return {'price':price,'wacc':w,'terminal_share':terminal/ev,'fcff1':fcff1}
for name,v in R['named_tests'].items():
 x=calculate(**v['parameters'])
 for field in x:eq('named.'+name+'.'+field,v[field],x[field])
for name,v in R['cases_at_reference_rate'].items():
 x=calculate(case=name)
 for field in x:eq('scenario.'+name+'.'+field,v[field],x[field])
for i,v in enumerate(R['cross_matrix']):
 x=calculate(beta=v['beta'],erp=v['ERP'],replacement=v['replacement'])
 for field in x:eq('matrix.'+str(i)+'.'+field,v[field],x[field])
for i,v in enumerate(R['debt_cost_sensitivity']):
 x=calculate(beta=v['beta'],kd=v['kd'])
 for field in x:eq('kd.'+str(i)+'.'+field,v[field],x[field])
for name,b in [('published_beta',.52),('shrink_convention',.68)]:
 for key,kw in [('low',{'extra_shares':4.4}),('high',{'cash':1099}),('high_with_sept_market_debt',{'cash':1099,'bridge_debt':7292})]:
  eq('bridge.'+name+'.'+key,R['bounded_bridge_test'][name][key],calculate(beta=b,**kw)['price'])
eq('E',R['inputs']['equity_value_for_weights'],71.89*331.691829)
eq('ERP_constant_market',R['named_tests']['constant_market_return_ERP']['parameters']['erp'],.0494+.0441-.0498)
eq('curve_roll',R['inputs']['kd_reference'],.06183+.0498-.0491)
eq('omitted_income.reference',R['omitted_other_income_flat_perpetuity_diagnostic']['increment_per_share_published_beta'],95*.75/calculate()['wacc']/332.691829)
eq('omitted_income.shrink',R['omitted_other_income_flat_perpetuity_diagnostic']['increment_per_share_shrink_beta'],95*.75/calculate(beta=.68)['wacc']/332.691829)
checks['no_trade']=R['execution_controls']['trade_authorized'] is False
checks['null']=R['execution_controls']['canonical_intrinsic_value'] is None and R['execution_controls']['max_buy_price'] is None
out={'status':'pass' if all(checks.values()) else 'fail','count':len(checks),'checks':checks,'errors':errors,'hashes':{f:hashlib.sha256((P/f).read_bytes()).hexdigest() for f in ['model_decision.py','results_decision.json']}}
(P/'checks_decision_independent.json').write_text(json.dumps(out,indent=2));print(json.dumps({k:out[k] for k in ['status','count','errors']},indent=2))
