"""EAT update: preserves A252 operating architecture; calibrates discount/capital.
USD million. No external packages/network; run writes calculations.json.
"""
import json, pathlib, copy
P=pathlib.Path(__file__).parent
f=json.loads((P/'legacy_facts_inputs.json').read_text())
# Load legacy function without executing old output/reverse writes.
src=(P/'legacy_model.py').read_text(); src=src[src.index('scenarios='):src.index('r={k:calc')]
exec(src)
legacy_cases={k:calc(s)['value_per_share'] for k,s in scenarios.items()}
old_bridge=bridge; old_shares=f['shares_diluted_q1']
price=206.57; shares=f['shares_oct22_basic']+.9
rf=.0486; erp=.0441; beta=1.34; kd=.0515; debt=f['revolver_debt']+f['finance_leases'];tax=.22
E=price*shares
wacc=(rf+beta*erp)*E/(E+debt)+kd*(1-tax)*debt/(E+debt)
shrink_beta=2/3*beta+1/3
wacc_shrink=(rf+shrink_beta*erp)*E/(E+debt)+kd*(1-tax)*debt/(E+debt)
# Source bridge retained incl65 subsequent buyback; unknown later cashflows bounded.
f['shares_diluted_q1']=shares
new_s={k:copy.deepcopy(s) for k,s in scenarios.items()}
new_s['base']['wacc']=wacc
new_s['bear']['wacc']=wacc+.015
new_s['bull']['wacc']=wacc_shrink
cases={k:calc(s) for k,s in new_s.items()}
for case in cases.values():
 t=case['terminal'];t['effective_terminal_roic']=t['nopat']*case['assumptions']['g']/t['reinvestment']
# Gradual margin-path inverse, not instantaneous margin jump. No funding assumed.
lo,hi=-.02,.25
for _ in range(100):
 d=(lo+hi)/2;s=copy.deepcopy(new_s['base']);s['margin5']+=d;s['margin10']+=d
 if calc(s)['value_per_share']<price:lo=d
 else:hi=d
s=copy.deepcopy(new_s['base']);s['margin5']+=(lo+hi)/2;s['margin10']+=(lo+hi)/2
reverse=calc(s)
sens={}
for w in [.08,.09,.10,.11,.12]:
 s=copy.deepcopy(new_s['base']);s['wacc']=w;sens[str(w)]=calc(s)['value_per_share']
base_old_cap=copy.deepcopy(new_s['base']);f['shares_diluted_q1']=old_shares
step_wacc=calc(base_old_cap)['value_per_share'];f['shares_diluted_q1']=shares
# Physical-spend-only contrast removes economic reserve; not selected automatically.
s=copy.deepcopy(new_s['base']);s['roic']=1000000
physical_only=calc(s)['value_per_share']
# Margins interpretation and reinvestment sensitivity use same base architecture.
roic_sens={}
for r in [.12,.15,.20,.25]:
 s=copy.deepcopy(new_s['base']);s['roic']=r;roic_sens[str(r)]=calc(s)['value_per_share']
# Alternate sustained profitability is sensitivity not adopted.
s=copy.deepcopy(new_s['base']);s.update(margin5=.13,margin10=.12,roic=.20)
strong=calc(s)
qa={'10_years':all(len(v['rows'])==10 for v in cases.values()),'ordered_scenarios':cases['bear']['value_per_share']<cases['base']['value_per_share']<cases['bull']['value_per_share'],'positive_base_flows':min(r['fcff'] for r in cases['base']['rows'])>0,'legacy_reproduced':abs(legacy_cases['base']-117.07676075172671)<1e-6}
assert all(qa.values())
out=dict(asof='2026-11-07',price=price,price_date='2026-11-06',shares_proxy=shares,bridge=bridge,calibration=dict(rf=rf,erp=erp,beta=beta,kd=kd,financial_debt=debt,market_equity=E,wacc=wacc,shrink_beta=shrink_beta,wacc_shrink=wacc_shrink),legacy_cases=legacy_cases,bridge_sequence=[['A252',legacy_cases['base']],['calibrated_wacc',step_wacc],['documented_dilution_proxy',cases['base']['value_per_share']]],cases=cases,wacc_sensitivity=sens,incremental_roic_sensitivity=roic_sens,gradual_reverse=dict(margin5=reverse['assumptions']['margin5'],margin10=reverse['assumptions']['margin10'],value=reverse['value_per_share'],minimum_fcff=min(r['fcff'] for r in reverse['rows']),first_fcff=reverse['rows'][0]['fcff'],rows=reverse['rows']),sustained_margin_sensitivity=strong['value_per_share'],physical_only_contrast=physical_only,cash_100m_sensitivity_per_share=100/shares,qa=qa,status='Valuation watch; bounded fundamental update, no entry approval')
(P/'calculations.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:round(v['value_per_share'],2) for k,v in cases.items()}));print('wacc',wacc,'inverse margins',reverse['assumptions']['margin5'],reverse['assumptions']['margin10'],'minfcff',min(r['fcff'] for r in reverse['rows']),'strong',strong['value_per_share'])
