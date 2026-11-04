import json,pathlib
p=pathlib.Path(__file__).parent; a=json.loads((p/'inputs.json').read_text()); o={}
for t in ['ORLY','GWW']:
 x=a[t];o[t]={'q3_revenue_growth':x['q3_revenue']/x['q3_prior_revenue']-1,'q3_gaap_margin':x['q3_ebit']/x['q3_revenue'],'q3_prior_gaap_margin':x['q3_prior_ebit']/x['q3_prior_revenue'],'nine_month_cfo_less_capex':x['nine_month_cfo']-x['nine_month_capex'],'nine_month_cfo_less_capex_sbc_sensitivity':x['nine_month_cfo']-x['nine_month_capex']-x['nine_month_sbc'],'q3_cfo_less_capex':x['q3_cfo']-x['q3_capex']}
x=a['ORLY'];assert abs(x['nine_month_cfo']-x['nine_month_capex']-x['nine_month_excess_sbc_tax_benefit']-x['nine_month_return_tax_credit_equity_investment']-x['nine_month_reported_fcf'])<1e-8
(p/'outputs.json').write_text(json.dumps(o,indent=2)+'\n')
