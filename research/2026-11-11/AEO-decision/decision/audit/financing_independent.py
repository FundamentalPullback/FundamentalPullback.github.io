from decimal import Decimal as D
from pathlib import Path
import json
P=Path(__file__).resolve().parents[1];r=json.load(open(P/'financing_diagnostics.json'));n=0
for x in r['scenarios']:
 cash=D('147.954');release=cash*D(str(x['reserve_release_fraction']));draw=D('199.39')-release;interest=draw*D(str(x['hypothetical_rate']));end=draw+interest
 for k,v in [('cash_released',release),('cash_reserve_remaining',cash-release),('initial_incremental_draw',draw),('one_year_gross_interest',interest),('year_end_incremental_claim',end),('total_facility_draw_if_only_this_change',D(55)+end),('nominal_headroom_after_initial_draw',D(635)-draw),('nominal_headroom_after_year_end_claim',D(635)-end)]:
  assert abs(float(v)-x[k])<1e-9,(k,v,x[k]);n+=1
json.dump({'status':'PASS','checks':n,'scenarios':len(r['scenarios']),'method':'Independent Decimal arithmetic, no production import','scope':'Liquidity illustrations only, no availability or fundedDCF validation'},open(P/'audit/output.json','w'),indent=2)
print(n,'PASS')
