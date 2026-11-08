"""Close reported bridges and cost-of-capital evidence without issuing fair value."""
from pathlib import Path
from datetime import date
import json,math
P=Path(__file__).resolve().parent
price=68.05; shares=64.423225; equity_market=price*shares
assert abs(775.157+259.523-34.603-322.579-677.498)<1e-8
assert abs(5195.643+213.723+16.788-94.224-287.572-5044.358)<1e-8
assert 68168923+355590-4101288==64423225
settle=date(2026,9,30);prev=date(2026,9,15);nxt=date(2027,3,15)
# Indicative yield from the 10-Q aggregate fair value; clean-price assumption remains.
# Prospectus 2025-02-27: March/September 15 coupons, maturity March 15 2035, 30/360 interest.
def days30360(a,b):
 return (b.year-a.year)*360+(b.month-a.month)*30+min(b.day,30)-min(a.day,30)
clean=474.350/500*100; coupon=5.65/2;accrued=coupon*days30360(prev,settle)/180
payments=[date(y,m,15) for y in range(2027,2036) for m in [3,9] if date(y,m,15)<=date(2035,3,15)]
def pv(y):return sum((coupon+(100 if d==date(2035,3,15) else 0))/(1+y/2)**(days30360(settle,d)/180) for d in payments)
lo,hi=0,.3
for _ in range(100):
 mid=(lo+hi)/2
 if pv(mid)>clean+accrued:lo=mid
 else:hi=mid
kd=(lo+hi)/2
beta=1.32;erp=.0441;rf=.0486;ke=rf+beta*erp;market_debt=299.250+550.034+430.335+474.350+42.351
out={'as_of':'2026-11-08','not_a_valuation':True,'approved_value':None,'confirmed_bridges':{'cash_begin':775.157,'cfo':259.523,'cfi':-34.603,'cff':-322.579,'cash_end':677.498,'equity_begin':5195.643,'earnings':213.723,'sbc':16.788,'dividends':94.224,'repurchase_equity_cost_including_excise':287.572,'repurchase_cash':285.000,'repurchase_excise_accrual_derived':2.572,'equity_end':5044.358,'shares_begin':68168923,'net_shares_issued_derived':355590,'shares_rebought':4101288,'shares_end':64423225,'q3_weighted_diluted_shares_m':65.127,'q3_rsu_increment_m':.429,'current_basic_plus_q3_rsu_proxy_m':64.852225,'proxy_not_current_actual_diluted_sharecount':True},'land':{'asset':126.684,'liability':115.215,'financing_cash_inflow':59.947,'noncash_inventory_increase':61.525,'asset_less_liability':11.469,'arithmetic_residual_not_explained':59.947+61.525-115.215,'no_claim_residual_is_settlement':True},'debt':{'notes_principal':1825,'land_notes_principal':42.351,'book_debt':1851.752,'book_debt_minus_cash':1174.254,'non_owned_land_liability':115.215,'leases':57.671,'gross_principal_including_land_liability_and_leases':2040.237,'no_excess_cash_valuation_assumed':True,'revolver_available_after_locs':896.734,'revolver_rate_2026_09_30':.05013},'joint_ventures':{'combined_assets':232.568,'combined_ap_other_liabilities':8.782,'separate_borrowing_line_disclosed':False,'meritage_share_jv_equity':63.817,'carrying_value':64.225,'unallocated_carrying_basis_difference':.408,'guarantees_quantified_zero':False,'public_note_cannot_prove_no_guarantees':True},'capital_cost_evidence':{'rf_2026_11_06':rf,'erp_2026_11_01':erp,'erp_source_rf':.0529,'observed_5y_beta_2026_11_08':beta,'ke_mixed_dates_diagnostic':ke,'ke_monthly_source_rf_diagnostic':.0529+beta*erp,'sofr_effective_2026_11_05':.0392,'daily_sofr_revolver_range':[.0392+.011,.0392+.0175],'current_long_debt_yield':None,'q3_2035_note_fair_value_clean_percent_assumed':clean,'q3_2035_note_approx_ytm':kd,'q3_ytm_limit':'Not a November quote or yield-to-worst; assumes aggregate fair value is clean price, 30/360 coupon accrual and semiannual discounting; clean fair value is assumed','illustrative_market_debt_m_mixed_dates':market_debt,'conditional_wacc_tax25_ex_landbank_leases':ke*equity_market/(equity_market+market_debt)+kd*.75*market_debt/(equity_market+market_debt),'wacc_approved':None}}
(P/'extended_results.json').write_text(json.dumps(out,indent=2));print(json.dumps(out['capital_cost_evidence'],indent=2))
