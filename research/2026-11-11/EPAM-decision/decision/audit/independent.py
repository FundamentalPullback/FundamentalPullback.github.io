from pathlib import Path
import json
P=Path(__file__).resolve().parents[1];m=json.loads((P/'legacy_model.json').read_text());r=json.loads((P/'results.json').read_text());n=0
def eq(a,b):
 global n
 assert abs(a-b)<max(1e-9,abs(b)*1e-12),(a,b)
 n+=1
s=m['bridge']['valuation_shares'];b=m['bridge']['equity_adjustment'];base=m['cases']['base'];e=base['equity']
for row in r['final_settlement_cases']:
 p=row['assumed_effective_final_price'];ret=500/p;ns=s-ret;v=(e-500)/ns
 for k,val in [('shares_retired_m',ret),('remaining_shares_m',ns),('equity_after_m',e-500),('value_after',v),('change_pct',(v/base['value']-1)*100)]:eq(val,row[k])
for f in r['funding_cases']:
 d=f['assumed_new_debt'];eq(500-d,f['cash_used']);eq(-(500-d)-d,f['net_cash_change']);eq(b-500,f['bridge_after'])
 for x in f['interest_service']:
  eq(d*x['assumed_rate'],x['annual_pretax']);eq(d*x['assumed_rate']*(1-.27),x['annual_aftertax_if_deductible'])
w=(4.98+1.27*4.41)/100
pv=sum(row['fcff']*(1+w)**(-row['year']) for row in base['rows'][:10]);tv=base['rows'][10]['fcff']/(w-.025)*(1+w)**-10
rr=r['rate_sensitivity'];eq(w,rr['simple_capm_rate']);eq((pv+tv+b)/s,rr['value_before_asr']);eq((pv+tv+b-500)/(s-500/164.14),rr['conditional_full_settlement_value']);eq(2550695*156.82,r['initial_shares_reference_dollars'])
eq((e-500)/(s-500/base['value']),base['value'])
(P/'audit/output.json').write_text(json.dumps({'status':'PASS','checks':n,'method':'Independent direct equations from archived inputs; no production import','conceptual_checks':['Full settlement equity less500 paired with500/effectiveprice share retirement; no free repurchase benefit','Netcash reduction500 independent of assumed financing split; no double-debt charge','Interest diagnostic separated from FCFF, conditionaltaxshield not guaranteed','10.5807% is observed-beta CAPM sensitivity, not post-ASR WACC certification','Finalprice scenarios ordinary hypothetical settlements subject to actual floor/cap/termination terms, not contractual bounds','Initial-only shares not treated as final; actualdelivery and funding split unverified','At200effectiveprice fewerfinalshares than initial implies companyreturnshares in simplifiedphysicalcase, allowed in contract subjectactualterms']},indent=2)+'\n');print('PASS',n)
