"""Reproduce the cross-review arithmetic and coverage from its public inputs.
This verifies the overlay, not every underlying DCF, market feed, account or order.
"""
from pathlib import Path
import json,math,datetime
P=Path(__file__).parent;read=lambda f:json.loads((P/f).read_text());u=read('universe.json');m=read('market_quotes.json');e=read('selected_economic_comparisons.json');meta=read('publication_record.json');checks=[]
def check(name,condition):
 checks.append({'name':name,'passed':bool(condition)})
 if not condition:raise AssertionError(name)
def eq(name,a,b):check(name,abs(a-b)<1e-8)
rows=u['rows'];quotes={q['ticker']:q for q in m['quotes']};check('seventy_unique',len(rows)==70==len({r['ticker']for r in rows})==len(quotes));check('scope_count_sum',sum(meta['scope_counts'].values())==70);check('no_individual_mutations',not meta['individual_records_to_modify']and not meta['individual_valuation_updates']and not meta['entry_state_updates']);check('no_new_entry',meta['new_entry_approvals']==0 and meta['orders_authorized']==0)
for r in rows:
 t=r['ticker'];q=quotes[t];check(t+'_same_quote',r['quote']==q);check(t+'_historical_gate',r['historical_scanner_opportunity']>=85);check(t+'_not_approved',not r['new_entry_approved']and not r['new_stage35_approval']and r['approved_new_quantity']==0);check(t+'_quote_not_analysis',not q['investment_analysis_updated']and not q['entry_approved_by_quote_capture']);check(t+'_explicit_market_status',q['status']in ['quote_received','error','dated_quote_not_current_regular_session']);check(t+'_no_executable_claim',not q.get('executable_bid_ask_verified',False))
for t,x in e.items():
 p=quotes[t].get('price');check(t+'_economic_quote',p==x['price']);check(t+'_economic_not_approval',not x['new_valuation_approval'])
 if p is None:continue
 if 'values'in x:
  for name,v in x['values'].items():
   eq(t+'_'+name+'_upside',(v['value_usd']/p-1)*100,v['upside_to_value_pct'])
   if v['value_usd']>0:eq(t+'_'+name+'_discount',(1-p/v['value_usd'])*100,v['discount_to_value_pct'])
 else:eq(t+'_base_upside',(x['base_value_usd']/p-1)*100,x['upside_to_base_pct'])
 c=x.get('isolated_current_CQP_bridge')
 if c:
  # Per-share denominator and old/new inputs are disclosed in the isolated bridge.
  check('CQP_no_duplicate_cashflow_change',c['wacc_and_operating_cashflows_unchanged']and c['not_new_approved_full_valuation'])
  eq('CQP_base_plus_change',x['values']['base']['value_usd']+c['value_change_per_LNG_share'],c['base_after_bridge_change_only'])
result={'status':'PASS','checks':len(checks),'failures':sum(not c['passed']for c in checks),'scope':'Public overlay arithmetic, source-data consistency and70-name coverage. Not a full underlying-model, live-market, account or order audit.','checks_detail':checks};(P/'reproduction_result.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items()if k!='checks_detail'}))
