"""Re-price preserved, explicitly dated KR cash flows; no new earnings or legal liability assumptions.
USD millions, shares millions. Current market quote supplies market equity weight only.
"""
import json
from pathlib import Path
B=Path(__file__).parent;L=json.loads((B/'legacy_inputs.json').read_text())
P=dict(price=68.60,price_date='2026-11-10 16:00 EST',basic_shares=590.5887,diluted_proxy=L['shares'],rf=.0498,erp=.0441,beta=.36,debt_cost=.06,tax=.23,debt=L['bridge']['debt_and_finance_leases'])
E=P['price']*P['basic_shares'];D=P['debt'];WE=E/(E+D);WD=1-WE
R={'observed_beta':WE*(P['rf']+P['beta']*P['erp'])+WD*P['debt_cost']*(1-P['tax']),'normalized_beta':WE*(P['rf']+P['erp'])+WD*P['debt_cost']*(1-P['tax'])}
def value(path='base',rate=None,extra_capex=0,extra_claim=0,claim_discount_year=0):
 c=L['case_assumptions'][path];w=c['wacc'] if rate is None else rate;old=L['results'][path];g=c['g'];rows=[]
 for r in old['rows']:
  out=dict(r);out['FCFF']=r['FCFF']-extra_capex;out['PV_FCFF']=out['FCFF']/(1+w)**r['year'];rows.append(out)
 term=old['terminal_FCFF']-extra_capex*(1+g);pvterm=term/(w-g)/(1+w)**10;ev=sum(r['PV_FCFF'] for r in rows)+pvterm;legalpv=extra_claim/(1+w)**claim_discount_year;eq=ev-L['netclaims']-legalpv;p=eq/L['shares']
 return dict(path=path,rate=w,extra_capex=extra_capex,extra_claim=extra_claim,claim_discount_year=claim_discount_year,extra_claim_pv=legalpv,rows=rows,terminal_fcff=term,terminal_pv=pvterm,terminal_fraction=pvterm/ev,ev=ev,netclaims=L['netclaims'],equity=eq,value=p,incremental_claim_capacity_at_quote=(p-P['price'])*L['shares'])
if __name__=='__main__':
 cases={n:value(**a) for n,a in {'legacy_adverse':{'path':'bear'},'legacy_base':{},'legacy_favorable':{'path':'bull'},'base_observed':{'rate':R['observed_beta']},'base_normalized':{'rate':R['normalized_beta']},'base_hurdle9':{'rate':.09},'base_normalized_capex300':{'rate':R['normalized_beta'],'extra_capex':300},'base_observed_capex300':{'rate':R['observed_beta'],'extra_capex':300}}.items()}
 sens={f'{rate_name}_claim{n}':value(rate=rate,extra_claim=n) for rate_name,rate in [('observed',R['observed_beta']),('normalized',R['normalized_beta']),('old8',.08)] for n in [0,600,3000,9300]}
 # Defer selected hypothetical payment, no asserted timing or legal probability.
 sens.update(claim3000_year3=value(rate=R['normalized_beta'],extra_claim=3000,claim_discount_year=3))
 out=dict(inputs=P,market_equity=E,weights={'equity':WE,'debt':WD},rates=R,cases=cases,legal_sensitivity=sens,legacy_giant_eagle=L['giant_eagle'],limitations=['No legal probability or new bookedliability','OriginalopioidPV750 remainsinbridge; legalextra amountsnot presumedopioidincrement','Marketweights use datedbalance and latestprice, not postOctbond certifiedbalance','Cashflows remain Nov3assumptions; not new issuer forecast','Deferredpayment illustration ignores possible fundingcostchange'])
 (B/'results.json').write_text(json.dumps(out,indent=2));print(R);print({k:round(v['value'],2) for k,v in cases.items()});print({k:round(v['incremental_claim_capacity_at_quote'],2) for k,v in cases.items()})
