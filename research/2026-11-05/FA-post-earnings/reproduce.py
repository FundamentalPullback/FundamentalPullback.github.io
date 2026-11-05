from pathlib import Path
import json
P=Path(__file__).resolve().parent
x=json.loads((P/'inputs.json').read_text())
def growth(new,old):return (new/old-1)*100
def cash_after_investment_sbc(r):return r['cfo']-r['ppe']-r['software']-r['sbc']
if 'acquisition_nov5' in x:
 out={};q={}
 for yr in ['2025','2026']:
  a=x['nine_months_'+yr];b=x['h1_'+yr]
  q[yr]={k:a[k]-b[k] for k in ['cfo','ppe','software','sbc']}
  q[yr]['cash_after_investment_and_sbc']=cash_after_investment_sbc(q[yr])
  out['nine_months_'+yr+'_cash_after_investment_and_sbc']=cash_after_investment_sbc(a)
 out['quarter_cash_bridge']=q
 out['q3_cfo_growth_pct']=growth(q['2026']['cfo'],q['2025']['cfo'])
 out['q3_cash_after_investment_and_sbc_growth_pct']=growth(q['2026']['cash_after_investment_and_sbc'],q['2025']['cash_after_investment_and_sbc'])
 out['q3_revenue_growth_pct']=growth(x['q3_2026']['revenue'],x['q3_2025']['revenue'])
 out['q3_ebit_growth_pct']=growth(x['q3_2026']['ebit'],x['q3_2025']['ebit'])
 out['q3_2026_ebit_margin_pct']=100*x['q3_2026']['ebit']/x['q3_2026']['revenue']
 out['q3_2025_ebit_margin_pct']=100*x['q3_2025']['ebit']/x['q3_2025']['revenue']
 out['adjusted_ebitda_after_sbc_q3']=x['q3_2026']['adjusted_ebitda']-x['q3_2026']['sbc']
 out['adjusted_ebitda_after_sbc_margin_q3_pct']=out['adjusted_ebitda_after_sbc_q3']/x['q3_2026']['revenue']*100
 a=x['nine_months_2026'];b=x['nine_months_2025'];c=x['fy2025']
 out['ttm_sept2026']={k:c[k]+a[k]-b[k] for k in ['cfo','ppe','software','sbc','net_income']}
 out['ttm_sept2026']['revenue']=c['revenue']+x['h1_2026']['revenue']+x['q3_2026']['revenue']-b['revenue']
 out['ttm_sept2026']['ebit']=c['ebit']+x['h1_2026']['ebit']+x['q3_2026']['ebit']-b['ebit']
 out['ttm_sept2026']['cash_after_investment_and_sbc']=cash_after_investment_sbc(out['ttm_sept2026'])
 h={k:c[k]+x['h1_2026'][k]-x['h1_2025'][k] for k in ['cfo','ppe','software','sbc']}
 out['ttm_june2026_cash_after_investment_and_sbc']=cash_after_investment_sbc(h)
 out['ttm_rolling_cash_change_pct']=growth(out['ttm_sept2026']['cash_after_investment_and_sbc'],out['ttm_june2026_cash_after_investment_and_sbc'])
 out['principal_debt_sept30']=x['capital_sept30']['debt_carrying']+x['capital_sept30']['unamortized_debt_costs']
 out['net_principal_debt_before_cash_reserve_and_deal']=out['principal_debt_sept30']-x['capital_sept30']['cash']
 assert abs(out['ttm_june2026_cash_after_investment_and_sbc']-175.027)<1e-8
elif 'tariff_items' in x:
 t=x['tariff_items'];a=x['fy2026'];b=x['fy2025'];q=x['q4_fy2026'];p=x['q4_fy2025']
 out={'fy_revenue_growth_pct':growth(a['revenue'],b['revenue']),'q4_revenue_growth_pct':growth(q['revenue'],p['revenue']),'fy_fcf_company_growth_pct':growth(a['fcf_company'],b['fcf_company']),'fy_cfo_without_identified_refund':a['cfo']-t['cash_refund_and_interest'],'fy_fcf_without_identified_refund':a['fcf_company']-t['cash_refund_and_interest'],'q4_fcf_without_identified_refund':q['fcf_company']-t['cash_refund_and_interest'],'fy_adjusted_eps_without_identified_refund':a['adjusted_eps']-t['adjusted_and_gaap_eps_benefit'],'q4_adjusted_eps_without_identified_refund':q['adjusted_eps']-t['adjusted_and_gaap_eps_benefit'],'pension_contribution_reduction':b['pension_contributions']-a['pension_contributions'],'net_debt_carrying_before_reserves':x['capital_sept30']['short_debt_carrying']+x['capital_sept30']['long_debt_carrying']-x['capital_sept30']['cash'],'dividends_and_treasury_purchases':a['cash_dividends']+a['cash_treasury_purchases']}
 out['fy_fcf_without_identified_refund_growth_pct']=growth(out['fy_fcf_without_identified_refund'],b['fcf_company'])
 out['fy_fcf_minus_refund_and_pension_timing_sensitivity']=out['fy_fcf_without_identified_refund']-out['pension_contribution_reduction']
 out['tariff_operating_profit_arithmetic']=t['cost_of_sales_reduction_refund']-t['revenue_reduction_customer_program']-t['related_nonrecurring_charges']
 assert a['cfo']-a['capex']==a['fcf_company']
else:
 a=x['nine_months_2026'];b=x['nine_months_2025'];q=x['q3_2026'];p=x['q3_2025']
 out={'q3_revenue_growth_pct':growth(q['revenue'],p['revenue']),'q3_ebit_growth_pct':growth(q['ebit'],p['ebit']),'q3_ebit_margin_pct':q['ebit']/q['revenue']*100,'odyssey_share_q3_box_office_pct':q['odyssey_box_office']/q['box_office']*100,'systems_installed_growth_pct':growth(q['systems_installed'],p['systems_installed']),'backlog_growth_pct':growth(x['capital_sept30']['backlog'],x['capital_sept30']['backlog_previous_year']),'tax_benefit_after_excluding_full_allowance_release':q['income_tax_recovery']-q['valuation_allowance_release'],'net_income_parent_after_removing_allowance_release_only':q['net_income_parent']-q['valuation_allowance_release']}
 for yr in ['2025','2026']:
  r=x['nine_months_'+yr];inv=sum(r[k] for k in ['ppe','jrsa_equipment','intangible_investment']);out['nine_months_'+yr]={'cash_investment':inv,'cash_after_investment':r['cfo']-inv,'cash_after_investment_and_reported_noncash_comp':r['cfo']-inv-r['sbc_and_other_noncash_comp']}
 out['cfo_growth_pct']=growth(a['cfo'],b['cfo']);out['cash_after_investment_and_reported_noncash_comp_growth_pct']=growth(out['nine_months_2026']['cash_after_investment_and_reported_noncash_comp'],out['nine_months_2025']['cash_after_investment_and_reported_noncash_comp'])
 assert abs(q['pretax_income']+q['income_tax_recovery']-q['net_income_consolidated'])<1e-9
out['interpretation']='Cash diagnostics are not FCFF or complete normalization. No valuation, price ceiling, stop or quantity approved.'
(P/'calculations.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n')
print(json.dumps(out,indent=2,ensure_ascii=False))
