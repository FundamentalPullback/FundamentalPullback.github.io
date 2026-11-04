import pathlib,json
P=pathlib.Path(__file__).parent;i=json.loads((P/'band_q3_2026.json').read_text());rows=[]
for j,p in enumerate(i['period_order']):
 assert i['cfo'][j]-i['cash_capex_plus_software'][j]==i['fcf'][j]
 rows.append({'period':p,'revenue_m':i['revenue'][j]/1000,'ebit_m':i['ebit_gaap'][j]/1000,'operating_margin':i['ebit_gaap'][j]/i['revenue'][j],'cfo_m':i['cfo'][j]/1000,'fcf_m':i['fcf'][j]/1000,'sbc_plus_payroll_m':i['sbc_including_related_payroll_taxes'][j]/1000,'eps_diluted_direct':i['eps_diluted_direct'][j]})
(P/'band_comparison.json').write_text(json.dumps({'source':i['source'],'rows':rows,'warning':'SBC plus payroll is not cash-flow SBC; adjusted margins exclude messaging surcharge revenue. No normalized EV multiple.'},indent=2)+'\n')
