"""Preserved operating model with dated quote and explicit current rate contrasts."""
import json
from pathlib import Path
from model import run,I
B=Path(__file__).parent
p={'price':164.59,'price_date':'2026-11-10 16:00 EST','cover_shares':33.463396,'gross_financing':8179,'beta':1.99,'rf':.0498,'erp':.0441,'marginal_debt_rate_assumption':.07,'tax':.26}
e=p['price']*p['cover_shares'];we=e/(e+p['gross_financing']);ke=p['rf']+p['erp']*p['beta'];w=we*ke+(1-we)*p['marginal_debt_rate_assumption']*(1-p['tax'])
cases={'observed_beta_rate':run('base',{'wacc':w}),'rate9':run('base',{'wacc':.09}),'rate11':run('base',{'wacc':.11})}
out={'inputs':p,'weights':{'equity':we,'debt':1-we},'ke':ke,'wacc':w,'cases':cases,'limitations':['Historical beta and dated debt not certified forward capital risk','7% marginal debt is own assumption not executable quote','Operating trajectories and balance claims unchanged since prior analysis','No levered interest deduction inside FCFF']};(B/'rate_refresh.json').write_text(json.dumps(out,indent=2));print(w,{k:(v['enterprise_value'],v['value_per_share']) for k,v in cases.items()})
