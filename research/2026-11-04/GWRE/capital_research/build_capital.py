#!/usr/bin/env python3
"""Offline stdlib baseline. USD millions; shares millions; prices USD. No acquisition pro forma."""
import json,csv
from pathlib import Path
p=Path(__file__).resolve().parent
x={'as_of_balance':'2026-07-31','cash':372.887,'short_term_investments':380.175,'long_term_investments':462.223,'convert_principal':690.0,'convert_carrying_value':678.094,'convert_fair_value':709.9,'revolver_drawn':0,'revolver_commitment':300,'lease_current':11.687,'lease_noncurrent':25.206,'shares_outstanding':81.992467,'shares_august_31':81.992669,'fy26_basic_wavg':84.186951,'fy26_diluted_wavg':85.405177,'q4_diluted_wavg':83.620224,'stock_awards_outstanding':2.146189,'options_outstanding':.096573,'options_weighted_strike':65.42,'unrecognized_sbc_stock_awards':303.141,'unrecognized_sbc_espp':4.727,'unrecognized_stock_awards_years':1.9,'convert_strike':244.65,'convert_rate_shares_per_1000':4.0875,'capped_call_cap':329.33,'capped_call_cost_historical':58.788,'convert_coupon':.0125,'convert_maturity':'2029-11-01','repurchases_fy26_cash':606.309,'repurchases_fy26_shares':4.085350,'repurchases_average_price':148.41,'repurchase_authorization_remaining':31.9,'repurchase_excise_tax_accrued_approx':3.1,'source':'https://www.sec.gov/Archives/edgar/data/1528396/000152839626000046/gwre-20260731.htm'}
x['liquid_cash_and_investments']=sum(x[k] for k in ['cash','short_term_investments','long_term_investments'])
x['net_cash_principal']=x['liquid_cash_and_investments']-x['convert_principal']
x['net_cash_after_leases']=x['net_cash_principal']-x['lease_current']-x['lease_noncurrent']
(p/'capital_facts.json').write_text(json.dumps(x,indent=2))
rows=[]
for price in [169.66,170.50,244.65,329.33,400]:
 # Principal always remains cash-settled: only conversion excess can dilute.
 underlying=x['convert_principal']*x['convert_rate_shares_per_1000']/1000
 gross_excess=underlying*max(0,price-x['convert_strike'])/price
 hedge_offset=underlying*max(0,min(price,x['capped_call_cap'])-x['convert_strike'])/price
 options_tsm=x['options_outstanding']*max(0,price-x['options_weighted_strike'])/price
 full_awards=x['shares_outstanding']+x['stock_awards_outstanding']+options_tsm+max(0,gross_excess-hedge_offset)
 rows.append({'price':price,'basic_market_cap':price*x['shares_outstanding'],'basic_ev_ex_leases':price*x['shares_outstanding']-x['net_cash_principal'],'gross_conversion_excess_shares':gross_excess,'capped_call_offset_equivalent_shares':hedge_offset,'net_convert_dilution_equivalent':max(0,gross_excess-hedge_offset),'options_tsm':options_tsm,'full_awards_sensitivity_shares':full_awards,'full_awards_ev_ex_leases':price*full_awards-x['net_cash_principal']})
with (p/'capital_sensitivities.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
assert abs(x['liquid_cash_and_investments']-1215.285)<1e-9
assert abs(x['net_cash_principal']-525.285)<1e-9
print(json.dumps({'liquidity':x['liquid_cash_and_investments'],'net_cash':x['net_cash_principal'],'price170.50':rows[1]},indent=2))
