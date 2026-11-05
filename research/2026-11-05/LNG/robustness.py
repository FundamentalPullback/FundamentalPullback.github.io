from pathlib import Path
from copy import deepcopy
import json
from model import value,I,C
P=Path(__file__).parent;c=I['cases']['base'];b=value(c);m=json.loads((P/'minority_check.json').read_text());out={}
for name,updates in [('zero_transient_premium',{'temporary_marketing_premium':[0]*5}),('high_committed_capex',{'growth_capex':[1400,850,250,0,0]}),('high_new_finance_assets',{'new_finance_asset_capex':[600,600,400,300,250]}),('lower_tax_15pct_terminal',{'terminal_tax':.15,'tax_rates':[.10,.12,.14,.15,.15]}),('terminal_roic_10pct',{'terminal_roic':.10}),('terminal_roic_15pct',{'terminal_roic':.15}),('flat_five_year_sustaining600',{'maintenance_capex':[600]*5}),('postquarter_cash1500',{'post_quarter_cash_adjustment':1500})]:
 z=deepcopy(c);z.update(updates);out[name]=value(z)['value_per_share']
# Regulatory-expiry illustration only: no operations, salvage or extension after2050.
fcf36=b['rows'][-1]['fcff'];pv_finite=sum(fcf36*(1+c['terminal_growth'])**k/(1+c['wacc'])**(10+57/365+k)for k in range(1,15));equity=b['equity']-b['pv_terminal']+pv_finite
out['hard_stop2050_zero_residual_not_prediction']=equity/C['shares_proxy_m']
out['using_cashflow_value_of_outside_CQP']={k:json.loads((P/'results.json').read_text())['cases'][k]['value_per_share']+v['parent_valuation_delta_using_this_check']for k,v in m.items()}
out['implied_market_operating_ev']=C['parent_market_equity']+C['total_financial_debt']+C['nci_market_equity']-b['cash_excess_proxy']
out['implied_ev_to_runrate_ebitda']=out['implied_market_operating_ev']/7650
out['implied_ev_to_peak2026_ebitda']=out['implied_market_operating_ev']/9000
out['implied_ev_to_normalized_TTM_ebitda']=out['implied_market_operating_ev']/7714
out['current_market_cap_to_TTM_parent_GAAP_net_income']=C['parent_market_equity']/3038
out['price_to_sum_quarter_diluted_EPS']=C['price']/14.33
out['reverse_2029_runrate_ebitda']=json.loads((P/'results.json').read_text())['reverse']['normalized_ebitda_multiplier']*7650
(P/'robustness.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
