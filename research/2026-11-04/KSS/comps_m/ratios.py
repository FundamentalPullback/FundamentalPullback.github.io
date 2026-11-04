"""Offline calculations; no network; exclusion from target median is mandatory."""
import json
from pathlib import Path
p=Path(__file__).parent
f=json.loads((p/'facts.json').read_text())
a,b,c=[f['periods'][k] for k in ['fy2025','h1_2026','h1_2025']]
keys=['net_sales','other_revenue','total_revenue','operating_income','real_estate_gains','impairment_restructuring_expense_signed_positive','interchange_settlement_gain','da','net_income','tax','net_interest','debt_extinguishment_loss','benefit_plan_income','pension_settlement_charge']
t={k:a[k]+b[k]-c[k] for k in keys}
t['normalized_operating_income_before_tariff_adjustment']=t['operating_income']-t['real_estate_gains']+t['impairment_restructuring_expense_signed_positive']-t['interchange_settlement_gain']
t['normalized_operating_income_gross_refund_stripped']=t['normalized_operating_income_before_tariff_adjustment']-f['tariff']['q2_gross_operating_refund']
t['ebit_net_income_plus_tax_plus_net_interest']=t['net_income']+t['tax']+t['net_interest']
t['ebit_excluding_debt_extinguishment']=t['ebit_net_income_plus_tax_plus_net_interest']+t['debt_extinguishment_loss']
cap=f['capital']; market_cap=f['market']['regular_close']*cap['shares_count']/1e6
ev=market_cap+cap['short_term_notes_debt']+cap['long_term_notes_debt_carrying']-cap['cash']
r={'ttm_ended':'2026-08-01','ttm':t,'market_cap_using_latest_filed_shares':market_cap,'ev_excluding_all_leases':ev,'ev_reported_operating_income':ev/t['operating_income'],'ev_normalized_operating_income_before_tariff':ev/t['normalized_operating_income_before_tariff_adjustment'],'ev_gross_refund_stripped_operating_income':ev/t['normalized_operating_income_gross_refund_stripped'],'reported_operating_margin':t['operating_income']/t['total_revenue'],'normalized_gross_refund_stripped_margin':t['normalized_operating_income_gross_refund_stripped']/t['total_revenue'],'include_in_target_median':False,'warning':'Indicative only: accrual-rent EBIT, not KSS all-cash-rent earnings. No lease-inclusive EV calculated; current lease split unavailable.'}
assert t['total_revenue']==t['net_sales']+t['other_revenue']
assert t['total_revenue']==22781 and t['operating_income']==1144
assert t['normalized_operating_income_gross_refund_stripped']==881
print(json.dumps(r,indent=2))
