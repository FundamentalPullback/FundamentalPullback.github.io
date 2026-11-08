import pathlib,json,csv
p=pathlib.Path(__file__).parent;h=json.loads((p/'history.json').read_text());r=json.loads((p/'model_results.json').read_text());rows=list(csv.DictReader((p/'model_years.csv').open()))
for k in ['revenue','ebit','net_parent','cfo','sbc']:assert abs(h['TTM2026'][k]-sum(h[q][k] for q in ['Q42025','Q12026','Q22026','Q32026']))<1e-6
for name,s in r['scenarios'].items():
 a=[x for x in rows if x['case']==name];stock=6884.123;pv=0
 for i,x in enumerate(a,1):
  da=float(x['physical_da']);cap=float(x['funded_capex']);assert abs(stock+cap-da-float(x['physical_stock_end']))<1e-6;stock=float(x['physical_stock_end']);assert cap>=da;pv+=float(x['conditional_fcff'])/(1+s['wacc_RMB_assumed'])**i
 assert abs(pv-s['PV_years1_10'])<1e-6
 assert s['terminal_capex11']>s['terminal_da11']
 assert abs(s['terminal_fcff11']/(s['wacc_RMB_assumed']-s['g'])-s['terminal_year10_value'])<1e-6
 # Numeric long-horizon sum verifies funded steady-state terminal recurrence.
 numeric=sum(s['terminal_fcff11']*(1+s['g'])**(i-1)/(1+s['wacc_RMB_assumed'])**i for i in range(1,601))
 assert abs(numeric-s['terminal_year10_value'])<.01
assert r['approved_value'] is None and h['TTM2026']['cash_capex'] is None
(p/'checks.json').write_text(json.dumps({'four_quarter_TTM_tie':True,'physical_stock_rollforward':True,'terminal_funding':True,'terminal_numerical_600_year_check':True,'current_FCF_not_fabricated':True,'no_ADS_target':True},indent=2))
