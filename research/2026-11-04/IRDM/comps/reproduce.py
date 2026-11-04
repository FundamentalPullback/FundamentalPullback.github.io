#!/usr/bin/env python3
"""Offline standard-library reproduction. No downloaded filings required."""
import json
from pathlib import Path
p=Path(__file__).resolve().parent
x=json.loads((p/'inputs.json').read_text()); v=x['VSAT']; g=x['GILT']
ttm={k:round(v['FY2026_Mar31'][k]+v['Q1FY2027_Jun30'][k]-v['Q1FY2026_Jun30'][k],6) for k in v['FY2026_Mar31']}
market_cap=v['price']*v['shares_actual']
ev=market_cap+v['gross_debt_including_finance_leases']-v['cash']+v['nci_book_value']
fcf=ttm['cfo']-ttm['capex']; adjusted_fcf=fcf-v['ligado_lump_sum_in_ttm_cfo']
out={'VSAT':{'basis':'Nov3 price; latest June balance sheet and July23 actual shares; screening-only EV including book NCI proxy', 'ttm_end':'2026-06-30','ttm':ttm,'market_cap':market_cap,'screening_ev':ev,'ev_revenue':ev/ttm['revenue'],'ev_ebit':ev/ttm['ebit'],'ev_ebitda_unadjusted':ev/(ttm['ebit']+ttm['depreciation']+ttm['amortization']),'ebit_margin':ttm['ebit']/ttm['revenue'],'capex_revenue':ttm['capex']/ttm['revenue'],'reported_cfo_less_capex':fcf,'reported_cfo_less_capex_less_sbc':fcf-ttm['sbc'],'reported_cfo_less_capex_equity_yield':fcf/market_cap,'cfo_less_capex_ex_ligado':adjusted_fcf,'cfo_less_capex_ex_ligado_less_sbc':adjusted_fcf-ttm['sbc'],'cfo_less_capex_ex_ligado_equity_yield':adjusted_fcf/market_cap},'GILT':{'basis':g['period'],'ebit_margin':g['ebit']/g['revenue'],'capex_revenue':g['capex']/g['revenue'],'cfo_less_capex':g['cfo']-g['capex'],'cfo_less_capex_less_sbc':g['cfo']-g['capex']-g['sbc'],'ev':None}}
assert abs(ttm['revenue']-4625.769)<1e-6
assert abs(ttm['ebit']-108.761)<1e-6
assert abs(fcf-578.286)<1e-6
i=x['IRDM'];im=i['price']*i['shares_actual'];ie=im+i['debt_principal']-i['cash'];out['IRDM']={'screening_ev':ie,'ev_revenue':ie/i['ttm_revenue'],'ev_ebit':ie/i['ttm_ebit'],'ev_ebitda_unadjusted':ie/(i['ttm_ebit']+i['ttm_da']),'ebit_margin':i['ttm_ebit']/i['ttm_revenue'],'unadjusted_fcf':i['ttm_cfo']-i['ttm_capex'],'fcf_less_all_sbc_proxy':i['ttm_cfo']-i['ttm_capex']-i['ttm_sbc_expensed']-i['ttm_sbc_capitalized']}
(p/'calculated.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
