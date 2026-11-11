import json
from pathlib import Path
r={'price':300.52,'price_date':'2026-11-10 16:00 EST','historic_standalone':{'bear':87.62,'base':124.53,'bull':184.06},'old_share_proxy_m':921,'new_notes_face_m':2000,'net_proceeds_approx_m':1987,'annual_coupon_m':sum(500*x for x in [.05,.0535,.055,.0575]),'issuance_net_debt_delta_approx_m':2000-1987,'target_q3_revenue_m':251,'target_q3_gaap_ebit_m':8,'target_q3_adjusted_ebit_m':40}
r['coupon_rate_face']=r['annual_coupon_m']/2000
r['issuance_cost_per_old_share_proxy']=13/921
r['old_value_comparison']={k:v/300.52-1 for k,v in r['historic_standalone'].items()}
r['target_gaap_margin']=8/251;r['target_adjusted_margin']=40/251
r['target_adjustment_gap_m']=40-8
# Financing only does not create transaction value; cash proceeds offset new debt.
r['illustrative_bridge_after_offering_only_m']=5413+13
r['illustrative_value_after_offering_cost_only']=124.53-13/921
r['combined_valuation']=None;r['entry_approved']=False
Path(__file__).with_name('results.json').write_text(json.dumps(r,indent=2)+'\n')
print(json.dumps(r,indent=2))
