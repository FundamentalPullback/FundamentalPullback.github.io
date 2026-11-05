from pathlib import Path
import json
p=Path(__file__).parent;f=json.loads((p/'facts/inputs.json').read_text());h=json.loads((p/'history/history.json').read_text());o={}
for k in ['q3','q3_prior','ytd','ytd_prior']:
 r=f[k];x={'limited_ebit_ex_mark_and_npns_amort':r['ebit']+r['fair_value_adjustment']+r['npns_amort_adjustment']};x['reconciled_adj_ebitda']=x['limited_ebit_ex_mark_and_npns_amort']+r['da']+r['noncash_comp_adjusted']+r.get('other_ebitda_adjustment',0)
 if k.startswith('ytd'):
  x['adjusted_ni_reconciliation']=r['ni_parent']+r['fair_value_adjustment']+r['npns_amort_adjustment']+r['adj_ni_tax']+r['adj_ni_nci'];x['consolidated_cash_less_net_ppe']=r['cfo']-r['capex_net_commissioning'];x['consolidated_cash_less_net_ppe_sbc']=x['consolidated_cash_less_net_ppe']-r['sbc_cf'];x['cash_less_net_ppe_actual_nci_distributions']=x['consolidated_cash_less_net_ppe']-r['nci_distributions'];x['cash_less_net_ppe_actual_nci_sbc']=x['cash_less_net_ppe_actual_nci_distributions']-r['sbc_cf'];x['gross_cash_ppe_before_commissioning_receipts']=r['capex_net_commissioning']+r['commissioning_receipts']
 o[k]=x
c=f['capital'];o['capital']={'debt_carrying':c['nominal_debt']-c['debt_cost'],'nominal_debt_less_consolidated_unrestricted_cash':c['nominal_debt']-c['cash'],'cash_outside_cqp_not_parent_excess_cash':c['cash']-c['cqp_cash'],'liquidity_including_restricted_and_credit':c['cash']+c['restricted_cash']+c['undrawn_facilities'],'net_derivative_asset_not_cash':c['derivative_assets']-c['derivative_liabilities'],'net_npns_asset_not_cash':c['npns_assets']-c['npns_liabilities']}
n=f['notes_nov2'];o['notes_announced']={'issue_proceeds_before_fees':n['principal']*n['issue_price_pct']/100,'annual_coupon':n['principal']*n['coupon'],'added_to_current_cash_or_debt':False}
o['ttm_tax_refund_sensitivity']={'reported_cash_less_net_ppe':h['TTM2026Q3']['cfo_less_net_capex']['value'],'minus_nonrecurring_2025_camt_refund':h['TTM2026Q3']['cfo_less_net_capex']['value']-380,'caveat':'Sensitivity removes prior-year tax refund; not a full normalized cash flow.'}
o.update(bear=None,base=None,bull=None,buy_ceiling=None,owner_fcf=None,equity_bridge=None,latestCompleted=False,approved_entry=False,stage35_approved=False,full_valuation=False)
(p/'analysis.json').write_text(json.dumps(o,indent=2)+'\n')
