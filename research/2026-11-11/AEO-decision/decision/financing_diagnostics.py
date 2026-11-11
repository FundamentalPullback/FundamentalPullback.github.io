"""Illustrative liquidity bridge, not funded DCF or credit availability certificate.
USD million. Assumes entire modeled annual deficit funded at year start, gross interest
capitalized for one year; ignores all other seasonal draws/dividends/fees/principal.
No incremental debt is subtracted from an FCFF DCF by this calculation.
"""
import json
from pathlib import Path
P=Path(__file__).parent
inputs={'published_year1_fcff_deficit':199.39,'dated_cash_all_reserved':147.954,'facility_nominal':700,'dated_drawn':55,'dated_letters_of_credit':10}
nominal=inputs['facility_nominal']-inputs['dated_drawn']-inputs['dated_letters_of_credit']
rows=[]
for fraction in [0,.5,1]:
 released=inputs['dated_cash_all_reserved']*fraction;draw=max(0,inputs['published_year1_fcff_deficit']-released)
 for rate in [.06,.08,.10]:
  interest=draw*rate;end=draw+interest
  rows.append({'reserve_release_fraction':fraction,'cash_released':released,'cash_reserve_remaining':inputs['dated_cash_all_reserved']-released,'hypothetical_rate':rate,'initial_incremental_draw':draw,'one_year_gross_interest':interest,'year_end_incremental_claim':end,'total_facility_draw_if_only_this_change':inputs['dated_drawn']+end,'nominal_headroom_after_initial_draw':nominal-draw,'nominal_headroom_after_year_end_claim':nominal-end})
out={'inputs':inputs,'nominal_unutilized_before_scenario':nominal,'scenarios':rows,'not_actual_availability':True,'not_funded_dcf':True,'limitations':['Borrowing base and covenant availability not certified','Debt rate hypothetical, not primary SOFR quote','Annual upfront draw and annual capitalized gross interest only','No financing fees, further seasonality, existing debt interest, dividends or repayments modeled','Cash release sacrifices reserved operating liquidity','New debt finances already modeled negativeFCFF; not a secondEVloss']}
(P/'financing_diagnostics.json').write_text(json.dumps(out,indent=2)+'\n')
