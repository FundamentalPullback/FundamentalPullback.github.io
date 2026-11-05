from pathlib import Path
import json,copy
from scipy.optimize import brentq
from value import calc,A
P=Path(__file__).resolve().parent;b=calc('base');price=A['price'];c=A['cases']['base'];out={}
out['price']=price
out['reverse_wacc_fixed_base_cashflows']=brentq(lambda x:calc('base',{'wacc':x})['per_share']-price,.04,.14)
out['uniform_ebit_margin_shift']=brentq(lambda d:calc('base',{'ebit_margin':[x+d for x in c['ebit_margin']]})['per_share']-price,-.05,.1)
out['growth_shift_firstfive']=brentq(lambda d:calc('base',{'growth_detailed':{k:[x+d for x in v] for k,v in c['growth_detailed'].items()}})['per_share']-price,-.05,.15)
out['wacc_sensitivity']={str(x):calc('base',{'wacc':x})['per_share'] for x in [.075,.08,.085079018,.09,.095,.10,.105]}
out['strategic_capital_sensitivity']={str(x):calc('base',{'strategic_reinvestment_ratio':x})['per_share'] for x in [0,.005,.01,.015,.02]}
out['terminal_ROIC_sensitivity']={str(x):calc('base',{'terminal_roic':x})['per_share'] for x in [.12,.15,.18,.22,.25,.30]}
out['shares_sensitivity']={str(x):calc('base',{'shares':x})['per_share'] for x in [15.780750,16.1,16.4,16.7]}
out['wc_no_collection_recovery']=calc('base',{'nwc_ratio':[.10]*10})['per_share']
out['client_receivable_50pct_loss']=calc('base',{'oneoff_unbilled_loss':(218.893+263.196)*.111*.5})['per_share']
out['shorelight_zero']=calc('base',{'shorelight_recovery_fraction':0})['per_share']
out['shorelight_book']=calc('base',{'shorelight_recovery_fraction':1})['per_share']
out['other_claim_per_10m']=10/c['shares']
out['current_EV_reconciled_assumed_capital']=price*c['shares']-b['bridge']['total']
out['EV_normalized_EBIT_TTM']=out['current_EV_reconciled_assumed_capital']/(195.845+15.613+4.9-4.063)
out['EV_RBR_TTM']=out['current_EV_reconciled_assumed_capital']/1824.146
out['earnings_growth_normalized_limited']=(195.845+15.613+4.9-4.063)/(175.436-.015+4.6)-1
out['capital_buffer_all_upper_release_not_valuation']=b['per_share']+(8.728+9.492+25.618+(1-.65)*22.29)/16.1
(P/'analysis.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
# Joint sensitivities: do not treat individually plausible changes as mutually exclusive.
out['joint_scenarios']={
 'wc_4_5pct_no_strategic':calc('base',{'nwc_ratio':[.045]*10,'strategic_reinvestment_ratio':0})['per_share'],
 'wacc8_no_strategic':calc('base',{'wacc':.08,'strategic_reinvestment_ratio':0})['per_share'],
 'wc4_5_no_strategic_wacc8':calc('base',{'nwc_ratio':[.045]*10,'strategic_reinvestment_ratio':0,'wacc':.08})['per_share'],
 'moderate_stress_wacc9_wc10_margin_minus_50bps':calc('base',{'wacc':.09,'nwc_ratio':[.10]*10,'ebit_margin':[x-.005 for x in c['ebit_margin']]})['per_share']}
out['guide_anchor_timing_sensitivity']={str(x):calc('base',{'fy26_reported_fcf_guidance_case':x})['per_share'] for x in [110,150,160,170]}
out['q4_bridge']={k:calc(k)['stub'] for k in ['base','bear','bull']}
out['valuation_date_convention']='Nov4 after market close; Q4 stub at Nov15 and annual midyear; Q4 cash guide spans Oct-Dec while balance Sep30. No material October capital change claimed known; timing/claim sensitivities explicit.'
out['capital_classification_bounds']={'possible_deduction_if_8728_not_current':8.728/c['shares'],'possible_release_if_8728_already_net_other_bucket':8.728/c['shares'],'not_certified_balance':True}
(P/'analysis.json').write_text(json.dumps(out,indent=2))
