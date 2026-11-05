"""Reproduce a CQP operating-surplus distribution waterfall, not FCFF valuation.
Sources: CQP 2025 10-K p35 and ownership p92; Q3 2026 cover + cash distributions.
Amounts USD millions except quarterly LP distribution per unit.
"""
import json
from pathlib import Path
p=Path(__file__).parent
units=484057704
parent_units=239872502 # precise Feb 20 2026 disclosure; Sep Q3 corroborates rounded 239.9m

def calc(d):
    tiers=[(0,.489,.02),(.489,.531,.15),(.531,.638,.25),(.638,float('inf'),.50)]
    gp=sum(max(0,min(d,hi)-lo)*units*share/(1-share) for lo,hi,share in tiers)
    lp=d*units;total=lp+gp
    base_gp=.02*total
    return {'lp_per_unit':d,'lp_total':lp/1e6,'gp_including_idr':gp/1e6,'base_gp':base_gp/1e6,'idr':(gp-base_gp)/1e6,'total':total/1e6,'parent_lp':d*parent_units/1e6,'parent_total':(d*parent_units+gp)/1e6,'outside_lp':d*(units-parent_units)/1e6,'parent_total_pct':100*(d*parent_units+gp)/total}
r={'caveat':'Uses exact parent holdings from Feb 20 2026, corroborated only to rounded 239.9m Sep 30. No new unit classes/arrearages; 2% GP maintained; excludes separate Tug Services payments. Not a forecast of available cash or valuation.','common_units_2026_10_23':units,'parent_lp_units_2026_02_20':parent_units,'parent_share_of_common_pct':parent_units/units*100,'distribution_cases':[calc(d) for d in [.79,.82,.83,.89]],'ex_cqp_mechanical':{'debt':24138-14523,'cash_unrestricted':1663-569,'restricted_cash':393-35,'net_debt_using_unrestricted_cash_only':24138-14523-(1663-569),'cash_including_restricted':1663+393-569-35},'spl_phase1_approx_cost_implied_by_loan_50pct':3250/.50}
(p/'waterfall_outputs.json').write_text(json.dumps(r,indent=2)+'\n')
print(json.dumps(r,indent=2))
