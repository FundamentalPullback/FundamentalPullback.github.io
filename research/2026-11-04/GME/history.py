import json,csv,pathlib
P=pathlib.Path(__file__).parent
fields=['sales','EBIT','net_income','net_interest_income','DA','SBC','asset_impairments_net','CFO','cash_capex']
rows={
'FY2024':[3823,-26.2,131.3,163.4,38.9,16.4,9.7,145.7,16.1],
'FY2025':[3629.9,232.1,418.4,271.5,14.6,26.7,53.8,614.8,17.5],
'H1FY2024':[1680.1,-72.6,-17.5,54.4,24.4,6.,0.,-41.2,8.],
'H1FY2025':[1704.6,55.6,213.4,136.5,10.3,11.8,33.4,309.9,7.],
'H1FY2026':[1625.5,303.5,688.3,160.8,9.1,15.8,-6.9,399.8,6.2]}
h={k:dict(zip(fields,v)) for k,v in rows.items()}
for name,annual,new,old in [('TTM2025','FY2024','H1FY2025','H1FY2024'),('TTM2026','FY2025','H1FY2026','H1FY2025')]:
 h[name]={f:h[annual][f]+h[new][f]-h[old][f] for f in fields}
for v in h.values():
 v['reported_FCF']=v['CFO']-v['cash_capex'];v['EBIT_ex_impairment']=v['EBIT']+v['asset_impairments_net'];v['operating_margin']=v['EBIT']/v['sales'];v['normalized_operating_Nopat_25pct']=v['EBIT_ex_impairment']*.75
 v['normalized_earnings_with_net_interest_25pct']=(v['EBIT_ex_impairment']+v['net_interest_income'])*.75
 v['FCFF_before_NWC_at_observed_capex']=v['normalized_operating_Nopat_25pct']+v['DA']-v['cash_capex']
 v['cash_diagnostic_less_SBC_and_aftertax_interest']=v['reported_FCF']-v['SBC']-v['net_interest_income']*.75
q={'Q3FY2025':dict(sales=821.,EBIT=41.3,net_income=77.1,CFO=111.3,cash_capex=4.3),'Q4FY2025':dict(sales=1104.3,EBIT=135.2,net_income=127.9,CFO=193.6,cash_capex=6.2),'Q1FY2026':dict(sales=835.3,EBIT=143.3,net_income=389.6,CFO=337.4,cash_capex=4.5),'Q2FY2026':dict(sales=790.2,EBIT=160.2,net_income=298.7,CFO=62.4,cash_capex=1.7)}
for f in q['Q3FY2025']:assert abs(sum(v[f] for v in q.values())-h['TTM2026'][f])<1e-7
sources={'FY2024_FY2025':'https://www.sec.gov/Archives/edgar/data/1326380/000132638026000013/gme-20260131.htm','H1FY2024_H1FY2025':'https://www.sec.gov/Archives/edgar/data/1326380/000132638025000075/gme-20250802.htm','H1FY2026':'https://www.sec.gov/Archives/edgar/data/1326380/000132638026000055/gme-20260801.htm','Q3FY2025':'https://www.sec.gov/Archives/edgar/data/1326380/000132638025000098/gme-20251101.htm','Q1FY2026':'https://www.sec.gov/Archives/edgar/data/1326380/000132638026000025/gme-20260502.htm'}
change={k:h['TTM2026'][k]/h['TTM2025'][k]-1 for k in h['TTM2026'] if h['TTM2025'][k]>0}
out=dict(units='USD millions',sources=sources,history=h,current_last_four_quarters=q,TTM_changes=change,methods='TTM2026=FY2025+H1FY2026-H1FY2025; TTM2025=FY2024+H1FY2025-H1FY2024. Normalized earnings retain SBC; remove impairment reversals/charges and all noninterest investing/other income, apply hypothetical25% tax. Historical capex is not a sustainable future maintenance estimate.')
(P/'history.json').write_text(json.dumps(out,indent=2))
with open(P/'history.csv','w')as f:
 w=csv.DictWriter(f,fieldnames=['period']+list(h['FY2024']));w.writeheader();w.writerows(dict(period=k,**v)for k,v in h.items())
for f in h['TTM2026']:print(f,round(h['TTM2025'][f],3),round(h['TTM2026'][f],3),round(change.get(f,0)*100,2))
