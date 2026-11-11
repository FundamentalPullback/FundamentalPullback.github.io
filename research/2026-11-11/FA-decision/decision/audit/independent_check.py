import json,math
from pathlib import Path
P=Path(__file__).parent
r=json.loads((P.parent/'results.json').read_text());S=r['shares'];D=r['debt'];C=r['cash']-r['operating_cash'];E=S*r['price']
w=(r['rf']+r['beta']*r['erp'])*E/(E+D)+r['kd_assumption']*(1-r['tax'])*D/(E+D)
def calculate(c,denom=S):
 revenues=[c['initial_revenue']]
 for y in range(2,11):
  growth=c['growth'] if y<=5 else c['growth']+(c['g']-c['growth'])*(y-5)/5
  revenues.append(revenues[-1]*(1+growth))
 cashflows=[]
 for idx,revenue in enumerate(revenues):
  year=idx+1;prior=revenues[idx-1] if idx else c['prior_revenue']
  margin=c['first_margin']+(c['final_margin']-c['first_margin'])*min(idx/4,1)
  growth=c['growth'] if year<=5 else c['growth']+(c['g']-c['growth'])*(year-5)/5
  operating=revenue*(margin-c['da'])*(1-c['tax'])
  cash_explicit=operating+revenue*c['da']-revenue*(c['investment']+c['acquisitions'])-(revenue-prior)*c['wc']
  cash_sustainable=operating*(1-growth/c['roic'])
  fade=max(0,(year-5)/5)
  cashflows.append(cash_explicit*(1-fade)+cash_sustainable*fade+c['ppa_shield']*max(0,1-idx/5))
 terminal=revenues[-1]*(1+c['g'])*(c['final_margin']-c['da'])*(1-c['tax'])*(1-c['g']/c['roic'])
 ev=sum(f/(1+c['wacc'])**(idx+1) for idx,f in enumerate(cashflows))+terminal/(c['wacc']-c['g'])/(1+c['wacc'])**10
 return (ev-D+C)/denom
checks=[{'case':n,'independent':calculate(v['inputs']),'model':v['value'],'error':calculate(v['inputs'])-v['value']} for n,v in r['cases'].items()]
b=r['cases']['base']['inputs'];no_shield_w=(r['rf']+r['beta']*r['erp'])*E/(E+D)+r['kd_assumption']*D/(E+D)
sens={'no_interest_tax_shield':calculate(b|{'wacc':no_shield_w}),'SBC50bp_all_years':calculate(b|{'first_margin':b['first_margin']-.005,'final_margin':b['final_margin']-.005}),'add_excluded_awards_1_116919m_fixed_EV':calculate(b, S+1.116919),'combined_no_interest_shield_SBC50bp_extra_awards':calculate(b|{'wacc':no_shield_w,'first_margin':b['first_margin']-.005,'final_margin':b['final_margin']-.005},S+1.116919)}
reverse=[{'wacc':x['wacc'],'calculated':calculate(b|{'wacc':x['wacc'],'final_margin':x['year5_ebitda_margin']})} for x in r['reverse']]
assert abs(w-r['wacc'])<1e-12
assert all(abs(x['error'])<1e-10 for x in checks)
assert all(abs(x['calculated']-r['price'])<1e-10 for x in reverse)
out={'method':'No import of model.py. Independently built annual cashflows as weighted explicit and sustainable cashflows.','wacc':w,'no_shield_wacc':no_shield_w,'cases':checks,'sensitivities':sens,'reverse':reverse,'passed':True}
(P/'independent_output.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
