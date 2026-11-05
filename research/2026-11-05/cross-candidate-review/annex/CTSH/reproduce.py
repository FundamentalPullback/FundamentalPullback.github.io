"""Replay price/risk math and prospective parameters, not a signal or order engine."""
from pathlib import Path
import json
p=Path(__file__).parent;c=json.loads((p/'current_comparison.json').read_text());q=json.loads((p/'proposal.json').read_text());t=json.loads((p/'technical_reference.json').read_text());ck=[]
def check(k,x):ck.append((k,bool(x)));assert x,k
price=c['quote']['price'];S=c['S'];base=c['scenarios']['base']['value']
for k,z in c['scenarios'].items():
 check('return_'+k,abs(z['return_pct']-100*(z['value']/price-1))<1e-8)
 check('MOS_'+k,abs(z['MOS_pct']-100*(1-price/z['value']))<1e-8)
for name,r in [('current',c['risk_at_current']),('max',c['risk_at_maximum'])]:
 E=r['E'];check(name+'_R',abs(r['R']-(E-S))<1e-8);check(name+'_stop_pct',abs(r['stop_pct']-100*(E-S)/E)<1e-8);check(name+'_base_R',abs(r['base_R']-(base-E)/(E-S))<1e-8)
check('fixed_caps',q['fundamental_maximum']==q['technical_maximum']==67.5);check('stable_previous_close',q['lower_price_validity_strict']==t['previous_close']==65.78);check('unchanged_M_S',q['M']==61.55 and q['S']==61.2);check('last_daily_above_ema50',t['previous_close']>t['EMA50']);check('no_activation',q['first_eligible_bar_start_UTC'] is None and q['first_eligible_bar_end_UTC'] is None and not q['entryApproved'] and not q['stage35Approved']);check('no_rearm',q['prior_proposal_is_not_reactivated']);check('quantity_zero',q['approvedQuantity']==0);check('position_not_assumed_zero',q['broker_position_zero_inferred'] is False);check('DAY',q['execution_validity'].startswith('DAY'));check('session_end',q['expires_UTC']=='2026-11-05T21:00:00Z')
print(json.dumps({'passed':True,'checks':len(ck),'scope':'Price/risk arithmetic and prospective parameter checks; no observed signal, certified account or order.'}))
