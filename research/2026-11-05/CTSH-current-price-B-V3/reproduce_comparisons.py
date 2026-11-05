"""Replay current-price comparisons and risk arithmetic, not a new DCF or an order engine."""
from pathlib import Path
import json,math
p=Path(__file__).parent;c=json.loads((p/'current_price_calculations.json').read_text());q=json.loads((p/'proposal.json').read_text());E=c['quote']['comparison_price_rounded_up_to_cent'];S=c['current_metrics']['manual_stop'];base=c['frozen_valuation']['base'];checks=[]
def ck(k,x):checks.append((k,bool(x)));assert x,k
ck('price_round_up',E==math.ceil(c['quote']['price']*100-1e-9)/100)
for k,z in c['scenario_returns'].items():
 ck('return_'+k,abs(z['return_pct']-100*(z['value']/E-1))<1e-9)
 ck('RR_'+k,abs(z['R_multiple']-(z['value']-E)/(E-S))<1e-9)
ck('current_MOS',abs(c['current_metrics']['MOS_pct']-100*(1-E/base))<1e-9)
r=q['risk_at_maximum'];em=r['E'];sm=r['S'];rr=em-sm
for k,w in {'R':rr,'stop_pct':rr/em*100,'one_R':em+rr,'two_R':em+2*rr,'base_upside_pct':100*(base/em-1),'base_MOS_pct':100*(1-em/base),'base_R':(base-em)/rr}.items():ck('max_'+k,abs(r[k]-w)<1e-9)
ck('caps_fixed',q['fundamental_maximum']==q['technical_maximum']==q['authorized_maximum_if_all_checks_pass']==67.50)
ck('no_entry',q['entryApproved'] is False and q['stage35Approved'] is False and q['approvedQuantity']==0)
ck('future_start_unassigned',q['first_eligible_bar_start_UTC'] is None and q['first_eligible_bar_end_UTC'] is None)
ck('no_old_reactivation',q['prior_proposal_is_not_reactivated'] is True)
print(json.dumps({'passed':all(x[1] for x in checks),'checks':len(checks),'scope':'Price and risk arithmetic; no market signal, account verification or execution approval.'}))
