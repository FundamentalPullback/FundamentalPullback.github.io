"""FOX post-close update. USD billions and shares billions; preserve legacy
operating scenario cash flows, adjust first-period ownership and expose claims.
Pro forma is not an actual Nov10 balance; no duplicate purchase-price deduction.
"""
import json
from pathlib import Path
B=Path(__file__).parent;L=json.loads((B/'legacy_inputs.json').read_text())
P={'existing_debt_principal':6.650,'new_debt_drawn':10.4,'proforma_cash':2.894,'cash_reserve':1.333,'nci_economic':.5,'pensions':.264,'other_investments_aftertax':.335*.75,'proforma_diluted_shares':.580513853,'old_terms_cash':96,'closing_terms_cash':95.30,'old_exchange':.9693,'closing_exchange':.9799,'roku_share_proxy':.153316257}
# Illustrative terms adjustment on disclosed proforma count, not asserted actual
# postclosing register or cash. All other proforma balance movements unchanged.
TERMS_CASH=P['roku_share_proxy']*(P['old_terms_cash']-P['closing_terms_cash'])
TERMS_SHARES=P['roku_share_proxy']*(P['closing_exchange']-P['old_exchange'])
CLAIMS=P['existing_debt_principal']+P['new_debt_drawn']-P['proforma_cash']+P['cash_reserve']+P['nci_economic']+P['pensions']-P['other_investments_aftertax']
def value(case='Central',rate=None,legacy=False,terms=False,extra_claim=0,synergy_cut=0,zero_taxasset=False,shares_override=None):
 c=L[case];x=c['Closes'];w=c['wacc'] if rate is None else rate;g=c['g'];flows=x['FCFF'].copy();term=x['terminal_FCFF']
 delta=0 if legacy else .5*c['roku_rev'][0]*(c['roku_margin'][0]*.75+.01-.012-.007)
 flows[0]+=delta
 # Fraction of scenario synergy removed, retaining original ramp25/50/100%.
 for i in range(10):flows[i]-=synergy_cut*c['synergy']*([.25,.5][i] if i<2 else 1)*.75
 term-=synergy_cut*c['synergy']*.75*(1+g)*(1-g/c['roic'])
 pvs=[f/(1+w)**(i+1) for i,f in enumerate(flows)];pvt=term/(w-g)/(1+w)**10;ev=sum(pvs)+pvt
 claims=-x['bridge'] if legacy else CLAIMS-(TERMS_CASH if terms else 0);shares=x['shares'] if legacy else P['proforma_diluted_shares']+(TERMS_SHARES if terms else 0);shares=shares if shares_override is None else shares_override;tax=0 if zero_taxasset else c['taxasset'];equity=ev-claims-extra_claim+tax
 return dict(case=case,rate=w,legacy=legacy,terms=terms,extra_claim=extra_claim,synergy_cut=synergy_cut,zero_taxasset=zero_taxasset,firstperiod_increment=delta,fcff=flows,pvs=pvs,terminal_fcff=term,terminal_pv=pvt,ev=ev,claims=claims,shares=shares,taxasset=tax,equity=equity,value=equity/shares)
if __name__=='__main__':
 cases={f'legacy_{c}':value(case=c,legacy=True) for c in L}
 cases.update({f'updated_{c}':value(case=c) for c in L})
 cases.update(central_terms=value(terms=True),central_zero_taxasset=value(zero_taxasset=True),central_no_synergy=value(synergy_cut=1),central_half_synergy=value(synergy_cut=.5),central_issued_share_proxy=value(shares_override=.428036905+.1445+.0038675))
 sens={f'w{w}_extra{e}':value(rate=w,extra_claim=e) for w in [.085,.09,.095,.10,.11] for e in [0,.5,1,2.7]}
 out={'inputs':P,'claims':CLAIMS,'terms_cash_adjustment':TERMS_CASH,'terms_share_adjustment':TERMS_SHARES,'cases':cases,'sensitivities':sens,'limitations':['Pro forma cash and weighted shares not certified actual postclose','Legacy operating trajectories retained except full firstyear ownership','No automatic acceleration of synergies','No failure-to-close option after completed deal','Interest not separately deducted from FCFF','Discount rates remain explicit scenarios, not new CAPM or final funding certification']};(B/'results.json').write_text(json.dumps(out,indent=2));print({k:round(v['value'],2) for k,v in cases.items()})
