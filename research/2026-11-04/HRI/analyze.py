from pathlib import Path
import json
p=Path(__file__).parent;f=json.loads((p/'facts/inputs.json').read_text());o={}
for k in ['q3','q3_prior','ytd','ytd_prior']:
 r=f[k];x={'ebit':r['pretax']+r['interest_net']+r['other_expense_net']};x['margin']=x['ebit']/r['revenue'];x['ebit_plus_transaction']=x['ebit']+r['transaction'];x['limited_ebit_ex_transaction_disposal_impairment']=x['ebit']+r['transaction']+r.get('held_for_sale_loss',0)
 if 'cfo' in r:
  x['cash_after_gross_capex']=r['cfo']-r['rental_capex_cash']-r['nonrental_capex_cash'];x['cash_after_rental_disposals']=x['cash_after_gross_capex']+r['rental_disposal_cash'];x['fcf_issuer']=x['cash_after_rental_disposals']+r['ppe_disposal_cash'];x['fcf_less_sbc_proxy']=x['fcf_issuer']-r['sbc'];x['fleet_ap_increase']=r['fleet_ap_end']-r['fleet_ap_start'];x['illustrative_cash_fcf_less_fleet_ap_increase']=x['fcf_issuer']-x['fleet_ap_increase'];x['illustrative_gross_accrual_fleet_capex']=r['rental_capex_cash']+x['fleet_ap_increase']
 o[k]=x
c=f['capital'];o['capital']={'nominal_debt_incl_finance_leases':sum(c[k] for k in ['notes','abl','term','ar','finance_leases']),'operating_leases':c['operating_leases_current']+c['operating_leases_noncurrent'],'liquidity_cash_plus_abl':c['cash']+c['abl_available']};o['capital']['nominal_debt_financing_less_cash']=o['capital']['nominal_debt_incl_finance_leases']+c['financing_obligations_gross']-c['cash'];o['capital']['floating_debt_principal']=c['abl']+c['term']+c['ar'];o['capital']['one_pct_rate_stress_annual_pretax']=o['capital']['floating_debt_principal']*.01
o['reported_ytd_rental_growth_pct']=(3307/2731-1)*100;o['issuer_proforma_ytd_rental_growth_pct']=4;o['ytd_operating_assets_liabilities_cash_change']=sum(f['ytd'][k] for k in ['receivables_change','other_assets_change','ap_change','accrued_other_change'])
o.update(bear=None,base=None,bull=None,owner_fcf=None,equity_bridge=None,latestCompleted=False,approved_entry=False,stage35_approved=False,full_valuation=False)
(p/'analysis.json').write_text(json.dumps(o,indent=2)+'\n')
