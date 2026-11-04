import json,pathlib
P=pathlib.Path(__file__).parent
h=json.loads((P/'history/normalized_history.json').read_text())
c=json.loads((P/'facts/capital_inputs.json').read_text())
a={'ticker':'AMD','cutoff':'2026-11-04 19:20 UTC','units':'USD millions except share price and per-share quantities','price':483.90,'price_date':'2026-11-03','price_pre_announcement':True,'history':h,'capital':c,'valuation':dict.fromkeys(['bear','base','bull','owner_fcf','equity_bridge','buy_ceiling']),'next_earnings_date':None}
a['diagnostics']={'liquid_assets':c['cash']+c['short_investments'],'book_lease_liability':c['lease_current']+c['lease_long'],'full_warrant_exercise_cash':c['warrant_max_shares_m']*c['warrant_strike'],'illustrative_existing_claim_ratio':c['q3_diluted_shares_m']/(c['q3_diluted_shares_m']+c['warrant_max_shares_m']),'warrant_cashflow_less_remeasurement':1179-1097,'q4_guidance_low':17000*.97,'q4_guidance_high':17000*1.03,'q4_guidance_sequential':17000/h['periods']['Q3FY2026']['revenue']-1}
if (P/'comps/operating_comps.json').exists():a['peers']=json.loads((P/'comps/operating_comps.json').read_text())
(P/'analysis.json').write_text(json.dumps(a,indent=2,ensure_ascii=False)+'\n')
