"""Nov4 2026 history-based DINO re-underwrite. Original model preserved as alternate.
Units USD billions except $/share, $/barrel; million produced barrels.
"""
from pathlib import Path
from copy import deepcopy
import json
import refiners_core_original as m
P=Path(__file__).parent
C=deepcopy(m.D);C['margins']=m.extend([22.87,21,20,19,19])
cases={'normalized_base':C,'original_elevated_spread':deepcopy(m.D),'severe_joint_bear':deepcopy(m.DB),'upcycle_joint_bull':deepcopy(m.DU)}
q=deepcopy(C);q['margins']=m.extend([25,23,21,20,19]);cases['firmer_normal_cycle']=q
q=deepcopy(C);q['margins']=m.extend([20,19,19,19,19]);cases['lower_normal_cycle']=q
for label,deck in [('joint_better_nonref',[22.87,21,20,19,19]),('joint_constructive',[25,23,21,20,19])]:
 q=deepcopy(C);q['margins']=m.extend(deck);q['wacc']=.10;q['other_ebitda']={'renewables':.2,'marketing':.13,'lubricants':.425,'midstream_ex_jvs_before_nci':.42};cases[label]=q
q=deepcopy(C);q['stub']['gross_margin']=30;cases['normalized_with_softer_stub']=q
out={'research_date_et':'2026-11-04 00:34 EST','reference_price':113.36,'history_anchor':22.87,'cases':{k:{'inputs':v,'valuation':m.calc(v),'equity_return':m.equity_return(v)} for k,v in cases.items()}}
out['wacc_sensitivity']=[dict(wacc=w,value=m.calc(C,wacc=w)['price']) for w in [.095,.1,.105,.11,.115]]
out['joint_sensitivity']=[dict(margin_delta=d,wacc=w,extra_rin=rin,extra_capex=cap,value=m.calc(C,delta_margin=d,wacc=w,rin=rin,extra_capex=cap)['price']) for d in [-2,0,2] for w in [.095,.105,.115] for rin,cap in [(0,0),(.15,.1)]]
out['reverse']=[dict(wacc=w,all_year_margin_delta=m.solve(lambda d:m.calc(C,wacc=w,delta_margin=d)['price'],C['price'],-10,20),steady_only_delta=m.solve(lambda d:m.steady_shift(C,d,w)['price'],C['price'],-10,20)) for w in [.095,.105,.115]]
# Increasing variable is negative WACC, preserving original monotone solve convention.
out['firm_discount_rate_at_market']=-m.solve(lambda neg:m.calc(C,wacc=-neg)['price'],C['price'],-.20,-.03)
(P/'DINO_normalized_model_results.json').write_text(json.dumps(out,indent=2))
for k,v in out['cases'].items():print(k,round(v['valuation']['price'],3),v['equity_return']['irr'])
print('reverse',out['reverse'],'firm',out['firm_discount_rate_at_market'])
assert abs(out['cases']['original_elevated_spread']['valuation']['price']-110.74284616703363)<1e-8
assert abs(out['cases']['normalized_base']['valuation']['price']-90.95008229329063)<1e-8
